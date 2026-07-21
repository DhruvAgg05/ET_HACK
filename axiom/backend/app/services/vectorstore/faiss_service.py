"""
FAISS vector store service — handles embedding generation, storage, and retrieval.
Uses FREE local sentence-transformers for embeddings (no API costs).
Stores vectors in FAISS for offline semantic search.
"""

# Disable SSL verification globally for HuggingFace model downloads
# (required on corporate networks with self-signed certificates)
import ssl
import os
os.environ["HF_HUB_DISABLE_SSL_VERIFY"] = "1"
os.environ["CURL_CA_BUNDLE"] = ""
try:
    ssl._create_default_https_context = ssl._create_unverified_context
except AttributeError:
    pass
try:
    import httpx
    _orig_client_init = httpx.Client.__init__
    def _patched_client_init(self, *args, **kwargs):
        kwargs.setdefault("verify", False)
        _orig_client_init(self, *args, **kwargs)
    httpx.Client.__init__ = _patched_client_init
except Exception:
    pass

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
        model = self._load_sentence_transformer()
        if model is not None:
            embedding = model.encode(text[:512], normalize_embeddings=True)
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
            truncated = [t[:512] for t in texts]
            embeddings = model.encode(truncated, normalize_embeddings=True, batch_size=32)
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
            self.index = faiss.read_index(str(self._index_file))
            with open(self._metadata_file, "r", encoding="utf-8") as f:
                self._metadata = json.load(f)
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
        """Persist FAISS index and metadata to disk."""
        if self.index is None:
            return
        faiss.write_index(self.index, str(self._index_file))
        with open(self._metadata_file, "w", encoding="utf-8") as f:
            json.dump(self._metadata, f, ensure_ascii=False)
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