"""
Qdrant vector store service — handles embedding generation, storage, and retrieval.
Uses FREE local sentence-transformers for embeddings (no API costs).
Optionally supports Ollama embeddings or OpenAI (paid) as fallback.
"""

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance, VectorParams, PointStruct,
    Filter, FieldCondition, MatchValue,
)
import uuid
import structlog

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
        self._ollama_available = False

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

        # Method 3: OpenAI (PAID fallback — only if key configured)
        if settings.openai_api_key:
            try:
                from openai import AsyncOpenAI
                client = AsyncOpenAI(api_key=settings.openai_api_key)
                response = await client.embeddings.create(
                    model=settings.openai_embedding_model,
                    input=text[:8000],
                )
                return response.data[0].embedding
            except Exception as e:
                logger.error("OpenAI embedding failed", error=str(e))

        # Fallback: zero vector
        logger.warning("No embedding engine available, using zero vector")
        return [0.0] * settings.embedding_dimension

    async def generate_embeddings_batch(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for multiple texts in batch."""
        # sentence-transformers supports efficient batching
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

class QdrantService:
    """Manages vector embeddings in Qdrant for semantic search."""

    def __init__(self):
        self.client: QdrantClient | None = None
        self.embedding_engine = EmbeddingEngine()
        self.collection_name = settings.qdrant_collection

    async def initialize(self):
        """Initialize Qdrant client and create collection if needed."""
        try:
            self.client = QdrantClient(
                host=settings.qdrant_host,
                port=settings.qdrant_port,
            )

            # Create collection if it doesn't exist
            collections = self.client.get_collections().collections
            collection_names = [c.name for c in collections]

            if self.collection_name not in collection_names:
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(
                        size=settings.embedding_dimension,
                        distance=Distance.COSINE,
                    ),
                )
                logger.info("Qdrant collection created", name=self.collection_name)
            else:
                logger.info("Qdrant collection exists", name=self.collection_name)

        except Exception as e:
            logger.error("Qdrant initialization failed", error=str(e))
            self.client = None

    async def generate_embedding(self, text: str) -> list[float]:
        """Generate embedding vector using FREE local model."""
        return await self.embedding_engine.generate_embedding(text)

    async def generate_embeddings_batch(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for multiple texts in a batch."""
        return await self.embedding_engine.generate_embeddings_batch(texts)

    async def index_chunks(self, chunks: list[DocumentChunk], document_id: str):
        """Index document chunks with their embeddings in Qdrant."""
        if not self.client:
            logger.warning("Qdrant not connected, skipping indexing")
            return

        if not chunks:
            return

        # Generate embeddings in batch
        texts = [chunk.content for chunk in chunks]
        embeddings = await self.generate_embeddings_batch(texts)

        # Create Qdrant points
        points = []
        for chunk, embedding in zip(chunks, embeddings):
            point_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, chunk.chunk_id))
            points.append(PointStruct(
                id=point_id,
                vector=embedding,
                payload={
                    "chunk_id": chunk.chunk_id,
                    "document_id": document_id,
                    "content": chunk.content,
                    "page_number": chunk.page_number,
                    "chunk_index": chunk.chunk_index,
                    "filename": chunk.metadata.get("filename", ""),
                    "category": chunk.metadata.get("category", ""),
                },
            ))

        # Upsert in batches of 100
        batch_size = 100
        for i in range(0, len(points), batch_size):
            batch = points[i:i + batch_size]
            self.client.upsert(
                collection_name=self.collection_name,
                points=batch,
            )

        logger.info(
            "Chunks indexed in Qdrant",
            document_id=document_id,
            chunks_indexed=len(points),
        )

    async def search(
        self,
        query: str,
        top_k: int = 5,
        category_filter: str | None = None,
    ) -> list[dict]:
        """Perform semantic search over indexed chunks."""
        if not self.client:
            return []

        # Generate query embedding
        query_embedding = await self.generate_embedding(query)

        # Build filter if needed
        search_filter = None
        if category_filter:
            search_filter = Filter(
                must=[
                    FieldCondition(
                        key="category",
                        match=MatchValue(value=category_filter),
                    )
                ]
            )

        # Search
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            limit=top_k,
            query_filter=search_filter,
        )

        # Format results
        formatted = []
        for hit in results:
            formatted.append({
                "chunk_id": hit.payload.get("chunk_id", ""),
                "document_id": hit.payload.get("document_id", ""),
                "filename": hit.payload.get("filename", ""),
                "content": hit.payload.get("content", ""),
                "page_number": hit.payload.get("page_number"),
                "score": hit.score,
            })

        return formatted

    async def delete_document(self, document_id: str):
        """Delete all chunks belonging to a document."""
        if not self.client:
            return

        self.client.delete(
            collection_name=self.collection_name,
            points_selector=Filter(
                must=[
                    FieldCondition(
                        key="document_id",
                        match=MatchValue(value=document_id),
                    )
                ]
            ),
        )
        logger.info("Document vectors deleted", document_id=document_id)