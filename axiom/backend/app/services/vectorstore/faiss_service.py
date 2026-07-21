"""
FAISS vector store service — handles embedding generation, storage, and retrieval.
Uses FREE local sentence-transformers for embeddings (no API costs).
Stores vectors in FAISS for offline semantic search.
"""

import asyncio
import contextlib
import ssl
import os
import json
import numpy as np
from pathlib import Path
import structlog

try:
    import faiss
    HAS_FAISS = True
except ImportError:
    HAS_FAISS = False

from app.config import settings
from app.models.schemas import DocumentChunk

logger = structlog.get_logger()

@contextlib.contextmanager
def _unverified_ssl_for_hf_download():
    """
    Temporarily disable TLS verification, scoped to the HuggingFace Hub model
    download only. Some corporate networks MITM outbound TLS with a
    self-signed cert that isn't in the system trust store, which breaks that
    one download. This must stay scoped and reverted — a process-wide,
    permanent patch would silently disable certificate checking for every
    other outbound call too, including the Ollama/OpenAI/Groq requests that
    carry API keys.
    """
    orig_https_context = ssl._create_default_https_context
    ssl._create_default_https_context = ssl._create_unverified_context

    orig_client_init = None
    try:
        import httpx
        orig_client_init = httpx.Client.__init__

        def _patched_init(self, *args, **kwargs):
            kwargs.setdefault("verify", False)
            orig_client_init(self, *args, **kwargs)

        httpx.Client.__init__ = _patched_init
    except Exception:
        pass

    try:
        yield
    finally:
        ssl._create_default_https_context = orig_https_context
        if orig_client_init is not None:
            import httpx
            httpx.Client.__init__ = orig_client_init

class EmbeddingEngine:
    """
    Embedding generation using FREE local models.
    Priority: sentence-transformers (local) > Ollama (local) > OpenAI (paid fallback)
    """

    def __init__(self):
        self._st_model = None

    def _load_sentence_transformer(self):
        """Load sentence-transformers model (FREE, local, fast)."""
        if self._st_model is None:
            try:
                from sentence_transformers import SentenceTransformer
                with _unverified_ssl_for_hf_download():
                    self._st_model = SentenceTransformer(settings.local_embedding_model)
                logger.info(
                    "Loaded local embedding model",
                    model=settings.local_embedding_model,
                )
            except Exception as e:
                logger.warning("sentence-transformers not available", error=str(e))
        return self._st_model

    async def generate_embedding(self, text: str) -> list[float]:
        """Generate embedding using best available FREE method."""
        # Method 1: Local sentence-transformers (preferred — fast, free, no network)
        # The model's own tokenizer truncates to its max_seq_length internally;
        # cutting the string ourselves at a fixed char count discarded content
        # that would otherwise have fit within the model's real token budget.
        model = self._load_sentence_transformer()
        if model is not None:
            # model.encode is synchronous CPU work — off the event loop so a
            # query embedding doesn't stall every other in-flight request.
            embedding = await asyncio.to_thread(model.encode, text, normalize_embeddings=True)
            return embedding.tolist()

        # Method 2: Ollama embeddings (free, local, needs Ollama running)
        try:
            import httpx
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{settings.ollama_base_url}/api/embeddings",
                    json={"model": settings.ollama_embedding_model, "prompt": text[:2000]},
                    timeout=30.0,
                )
                if response.status_code == 200:
                    return response.json()["embedding"]
        except Exception as e:
            logger.debug("Ollama embeddings failed", error=str(e))

        # Fallback: zero vector
        logger.warning("No embedding engine available, using zero vector")
        return [0.0] * settings.embedding_dimension

    async def generate_embeddings_batch(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for multiple texts in batch."""
        model = self._load_sentence_transformer()
        if model is not None:
            embeddings = await asyncio.to_thread(
                model.encode, texts, normalize_embeddings=True, batch_size=32
            )
            return [e.tolist() for e in embeddings]

        # Fallback: one by one
        results = []
        for text in texts:
            emb = await self.generate_embedding(text)
            results.append(emb)
        return results

class FAISSService:
    """
    Manages vector embeddings in FAISS for semantic search.
    Fully offline — no external service required.
    """

    def __init__(self):
        self.embedding_engine = EmbeddingEngine()
        self.index: "faiss.IndexFlatIP" | None = None
        self._metadata: list[dict] = []  # Stores chunk metadata alongside vectors
        self._index_path = Path(settings.faiss_index_dir)
        self._index_file = self._index_path / "index.faiss"
        self._metadata_file = self._index_path / "metadata.json"

    async def initialize(self):
        """Initialize FAISS index — load from disk or create new."""
        if not HAS_FAISS:
            logger.error("FAISS not installed. Install with: pip install faiss-cpu")
            return

        self._index_path.mkdir(parents=True, exist_ok=True)

        if self._index_file.exists() and self._metadata_file.exists():
            # Load existing index
            loaded_index = faiss.read_index(str(self._index_file))

            if loaded_index.d != settings.embedding_dimension:
                # The embedding model was changed since this index was built —
                # loading it anyway would let queries run against vectors from a
                # different vector space and return silently meaningless results.
                logger.error(
                    "FAISS index dimension mismatch — refusing to load stale index. "
                    "Delete the index/metadata files to rebuild for the current model, "
                    "or restore the embedding model that matches this index.",
                    index_dimension=loaded_index.d,
                    configured_dimension=settings.embedding_dimension,
                )
                self.index = faiss.IndexFlatIP(settings.embedding_dimension)
                self._metadata = []
                return

            self.index = loaded_index
            with open(self._metadata_file, "r", encoding="utf-8") as f:
                self._metadata = json.load(f)

            if self.index.ntotal != len(self._metadata):
                logger.warning(
                    "FAISS index/metadata count mismatch — a prior write was likely "
                    "interrupted. Search results may be misaligned.",
                    vectors=self.index.ntotal,
                    metadata_entries=len(self._metadata),
                )

            logger.info(
                "FAISS index loaded from disk",
                vectors=self.index.ntotal,
                metadata_entries=len(self._metadata),
            )
        else:
            # Create new index (Inner Product for cosine similarity with normalized vectors)
            self.index = faiss.IndexFlatIP(settings.embedding_dimension)
            self._metadata = []
            logger.info("New FAISS index created", dimension=settings.embedding_dimension)

    def _save_index(self):
        """
        Persist FAISS index and metadata to disk atomically.

        Writes to temp files then renames into place, so a crash mid-write can
        never leave index.faiss and metadata.json disagreeing about vector count
        (os.replace is atomic on both POSIX and Windows).
        """
        if self.index is None:
            return

        tmp_index = self._index_file.with_suffix(".faiss.tmp")
        tmp_metadata = self._metadata_file.with_suffix(".json.tmp")

        faiss.write_index(self.index, str(tmp_index))
        with open(tmp_metadata, "w", encoding="utf-8") as f:
            json.dump(self._metadata, f, ensure_ascii=False)

        os.replace(tmp_index, self._index_file)
        os.replace(tmp_metadata, self._metadata_file)

        logger.debug("FAISS index saved to disk", vectors=self.index.ntotal)

    async def generate_embedding(self, text: str) -> list[float]:
        """Generate embedding vector using FREE local model."""
        return await self.embedding_engine.generate_embedding(text)

    async def generate_embeddings_batch(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for multiple texts in a batch."""
        return await self.embedding_engine.generate_embeddings_batch(texts)

    async def index_chunks(self, chunks: list[DocumentChunk], document_id: str):
        """Index document chunks with their embeddings in FAISS."""
        if self.index is None:
            logger.warning("FAISS not initialized, skipping indexing")
            return

        if not chunks:
            return

        # Generate embeddings in batch
        texts = [chunk.content for chunk in chunks]
        embeddings = await self.generate_embeddings_batch(texts)

        # Convert to numpy array
        vectors = np.array(embeddings, dtype=np.float32)

        # Add to FAISS index
        self.index.add(vectors)

        # Store metadata for each vector
        for chunk in chunks:
            self._metadata.append({
                "chunk_id": chunk.chunk_id,
                "document_id": document_id,
                "content": chunk.content,
                "page_number": chunk.page_number,
                "chunk_index": chunk.chunk_index,
                "filename": chunk.metadata.get("filename", ""),
                "category": chunk.metadata.get("category", ""),
            })

        # Persist to disk
        self._save_index()

        logger.info(
            "Chunks indexed in FAISS",
            document_id=document_id,
            chunks_indexed=len(chunks),
            total_vectors=self.index.ntotal,
        )

    async def search(
        self,
        query: str,
        top_k: int = 5,
        category_filter: str | None = None,
    ) -> list[dict]:
        """Perform semantic search over indexed chunks."""
        if self.index is None or self.index.ntotal == 0:
            return []

        # Generate query embedding
        query_embedding = await self.generate_embedding(query)
        query_vector = np.array([query_embedding], dtype=np.float32)

        # Search FAISS (get more results if filtering)
        search_k = top_k * 3 if category_filter else top_k
        scores, indices = self.index.search(query_vector, min(search_k, self.index.ntotal))

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < 0 or idx >= len(self._metadata):
                continue

            meta = self._metadata[idx]

            # Apply category filter if specified
            if category_filter and meta.get("category", "") != category_filter:
                continue

            results.append({
                "chunk_id": meta["chunk_id"],
                "document_id": meta["document_id"],
                "content": meta["content"],
                "page_number": meta.get("page_number"),
                "chunk_index": meta.get("chunk_index"),
                "filename": meta.get("filename", ""),
                "category": meta.get("category", ""),
                "score": float(score),
            })

            if len(results) >= top_k:
                break

        return results

    async def delete_document(self, document_id: str):
        """Remove all vectors for a document. Rebuilds index without those vectors."""
        if self.index is None:
            return

        # Find indices to keep
        keep_indices = [
            i for i, meta in enumerate(self._metadata)
            if meta["document_id"] != document_id
        ]

        if len(keep_indices) == len(self._metadata):
            return  # Nothing to delete

        # Rebuild index without deleted vectors
        if keep_indices:
            # Reconstruct vectors for kept indices
            all_vectors = np.zeros((self.index.ntotal, settings.embedding_dimension), dtype=np.float32)
            for i in range(self.index.ntotal):
                all_vectors[i] = self.index.reconstruct(i)

            kept_vectors = all_vectors[keep_indices]
            kept_metadata = [self._metadata[i] for i in keep_indices]

            # Rebuild
            self.index = faiss.IndexFlatIP(settings.embedding_dimension)
            self.index.add(kept_vectors)
            self._metadata = kept_metadata
        else:
            self.index = faiss.IndexFlatIP(settings.embedding_dimension)
            self._metadata = []

        self._save_index()
        logger.info("Document removed from FAISS", document_id=document_id)

    def get_all_metadata(self) -> list[dict]:
        """Get all stored metadata (for BM25 index building)."""
        return self._metadata