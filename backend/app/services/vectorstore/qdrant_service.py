"""Async Qdrant service for vector indexing and retrieval."""

from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable, Sequence
import logging
from typing import Any

from httpx import HTTPError
from qdrant_client import AsyncQdrantClient, models
from qdrant_client.http.exceptions import ResponseHandlingException, UnexpectedResponse

from backend.app.config import Settings, get_settings
from backend.app.models.schemas import DocumentChunk


logger = logging.getLogger(__name__)


class QdrantServiceError(RuntimeError):
    """Raised when a Qdrant operation fails."""


class QdrantService:
    """High-level async Qdrant service with collection lifecycle helpers."""

    def __init__(self, settings: Settings | None = None) -> None:
        """Initialize the Qdrant service."""
        self._settings = settings or get_settings()
        self._client: AsyncQdrantClient | None = None
        self._lock = asyncio.Lock()
        self._logger = logger.getChild(self.__class__.__name__)

    async def __aenter__(self) -> QdrantService:
        """Open the Qdrant client in an async context."""
        await self.connect()
        return self

    async def __aexit__(self, exc_type: type[BaseException] | None, exc: BaseException | None, tb: Any) -> None:
        """Close the Qdrant client on context exit."""
        await self.close()

    async def connect(self) -> None:
        """Create the async Qdrant client."""
        if self._client is not None:
            return

        async with self._lock:
            if self._client is not None:
                return

            config = self._settings.qdrant
            self._logger.info("Connecting to Qdrant", extra={"url": config.url, "collection": config.collection})
            client = AsyncQdrantClient(
                url=config.url,
                api_key=config.api_key.get_secret_value() if config.api_key else None,
                timeout=int(config.timeout_seconds),
                prefer_grpc=config.prefer_grpc,
                check_compatibility=True,
                pool_size=config.pool_size,
            )
            try:
                await client.get_collections()
            except (ResponseHandlingException, UnexpectedResponse, HTTPError, OSError) as exc:
                await client.close()
                self._logger.exception("Qdrant connectivity verification failed")
                raise QdrantServiceError("Failed to connect to Qdrant.") from exc
            self._client = client
            self._logger.info("Qdrant connection established")

    async def close(self) -> None:
        """Close the async Qdrant client."""
        if self._client is None:
            return

        async with self._lock:
            if self._client is None:
                return
            await self._client.close()
            self._client = None
            self._logger.info("Qdrant connection closed")

    async def health_check(self) -> dict[str, Any]:
        """Return a health summary for Qdrant."""
        collections = await self.get_collections()
        return {"status": "ok", "collections": collections}

    async def get_collections(self) -> list[str]:
        """Return all available Qdrant collection names."""
        async def operation() -> list[str]:
            client = await self._get_client()
            response = await client.get_collections()
            return [collection.name for collection in response.collections]

        try:
            return await self._with_retry(operation, "get_collections")
        except (ResponseHandlingException, UnexpectedResponse, HTTPError, OSError) as exc:
            self._logger.exception("Failed to fetch Qdrant collections")
            raise QdrantServiceError("Failed to fetch Qdrant collections.") from exc

    async def collection_exists(self, collection_name: str | None = None) -> bool:
        """Return whether the target collection exists."""
        name = collection_name or self._settings.qdrant.collection

        async def operation() -> bool:
            client = await self._get_client()
            return await client.collection_exists(collection_name=name)

        return bool(await self._with_retry(operation, "collection_exists"))

    async def ensure_collection(
        self,
        *,
        collection_name: str | None = None,
        vector_size: int | None = None,
        distance: models.Distance = models.Distance.COSINE,
    ) -> None:
        """Create the target collection when it does not already exist."""
        name = collection_name or self._settings.qdrant.collection
        size = vector_size or self._settings.embeddings.vector_size
        if await self.collection_exists(name):
            return

        async def operation() -> None:
            client = await self._get_client()
            await client.create_collection(
                collection_name=name,
                vectors_config=models.VectorParams(size=size, distance=distance),
            )

        try:
            await self._with_retry(operation, "ensure_collection")
            self._logger.info("Created Qdrant collection", extra={"collection": name, "vector_size": size})
        except (ResponseHandlingException, UnexpectedResponse, HTTPError, OSError) as exc:
            self._logger.exception("Failed to create Qdrant collection", extra={"collection": name})
            raise QdrantServiceError("Failed to create Qdrant collection.") from exc

    async def upsert_chunks(
        self,
        chunks: Sequence[DocumentChunk],
        vectors: Sequence[Sequence[float]],
        *,
        collection_name: str | None = None,
        wait: bool = True,
        batch_size: int | None = None,
    ) -> int:
        """Upsert document chunks and vectors into Qdrant in batches."""
        if len(chunks) != len(vectors):
            raise ValueError("chunks and vectors must have the same length.")
        if not chunks:
            return 0

        name = collection_name or self._settings.qdrant.collection
        await self.ensure_collection(collection_name=name)
        batch_size = batch_size or self._settings.embeddings.batch_size

        processed = 0
        for start in range(0, len(chunks), batch_size):
            chunk_batch = chunks[start : start + batch_size]
            vector_batch = vectors[start : start + batch_size]
            points = [
                models.PointStruct(
                    id=str(chunk.chunk_id),
                    vector=list(vector),
                    payload=self._build_chunk_payload(chunk),
                )
                for chunk, vector in zip(chunk_batch, vector_batch, strict=True)
            ]
            await self.upsert_points(points, collection_name=name, wait=wait)
            processed += len(points)
        return processed

    async def upsert_points(
        self,
        points: Sequence[models.PointStruct],
        *,
        collection_name: str | None = None,
        wait: bool = True,
    ) -> None:
        """Upsert a collection of Qdrant points."""
        if not points:
            return
        name = collection_name or self._settings.qdrant.collection

        async def operation() -> None:
            client = await self._get_client()
            await client.upsert(collection_name=name, points=points, wait=wait)

        try:
            await self._with_retry(operation, "upsert_points")
        except (ResponseHandlingException, UnexpectedResponse, HTTPError, OSError) as exc:
            self._logger.exception("Failed to upsert Qdrant points", extra={"collection": name})
            raise QdrantServiceError("Failed to upsert Qdrant points.") from exc

    async def search(
        self,
        vector: Sequence[float],
        *,
        collection_name: str | None = None,
        limit: int = 10,
        score_threshold: float | None = None,
        query_filter: models.Filter | None = None,
        with_payload: bool = True,
    ) -> list[dict[str, Any]]:
        """Search the vector collection and return normalized hits."""
        if limit < 1:
            raise ValueError("limit must be greater than zero.")
        name = collection_name or self._settings.qdrant.collection

        async def operation() -> list[dict[str, Any]]:
            client = await self._get_client()
            response = await client.query_points(
                collection_name=name,
                query=list(vector),
                query_filter=query_filter,
                limit=limit,
                score_threshold=score_threshold,
                with_payload=with_payload,
            )
            return [
                {
                    "id": point.id,
                    "score": point.score,
                    "payload": point.payload,
                    "vector": point.vector,
                }
                for point in response.points
            ]

        try:
            return await self._with_retry(operation, "search")
        except (ResponseHandlingException, UnexpectedResponse, HTTPError, OSError) as exc:
            self._logger.exception("Qdrant search failed", extra={"collection": name})
            raise QdrantServiceError("Qdrant search failed.") from exc

    async def retrieve(
        self,
        point_ids: Sequence[str],
        *,
        collection_name: str | None = None,
        with_payload: bool = True,
        with_vectors: bool = False,
    ) -> list[dict[str, Any]]:
        """Retrieve specific points by their IDs."""
        if not point_ids:
            return []
        name = collection_name or self._settings.qdrant.collection

        async def operation() -> list[dict[str, Any]]:
            client = await self._get_client()
            records = await client.retrieve(
                collection_name=name,
                ids=list(point_ids),
                with_payload=with_payload,
                with_vectors=with_vectors,
            )
            return [
                {
                    "id": record.id,
                    "payload": record.payload,
                    "vector": record.vector,
                }
                for record in records
            ]

        return await self._with_retry(operation, "retrieve")

    async def scroll(
        self,
        *,
        collection_name: str | None = None,
        limit: int = 100,
        query_filter: models.Filter | None = None,
        with_payload: bool = True,
        with_vectors: bool = False,
    ) -> tuple[list[dict[str, Any]], Any]:
        """Scroll through collection points."""
        if limit < 1:
            raise ValueError("limit must be greater than zero.")
        name = collection_name or self._settings.qdrant.collection

        async def operation() -> tuple[list[dict[str, Any]], Any]:
            client = await self._get_client()
            records, next_page_offset = await client.scroll(
                collection_name=name,
                scroll_filter=query_filter,
                limit=limit,
                with_payload=with_payload,
                with_vectors=with_vectors,
            )
            items = [
                {
                    "id": record.id,
                    "payload": record.payload,
                    "vector": record.vector,
                }
                for record in records
            ]
            return items, next_page_offset

        return await self._with_retry(operation, "scroll")

    async def count(self, *, collection_name: str | None = None, query_filter: models.Filter | None = None) -> int:
        """Count points in a collection with an optional filter."""
        name = collection_name or self._settings.qdrant.collection

        async def operation() -> int:
            client = await self._get_client()
            response = await client.count(collection_name=name, count_filter=query_filter, exact=True)
            return int(response.count)

        return await self._with_retry(operation, "count")

    async def delete_points(self, point_ids: Sequence[str], *, collection_name: str | None = None, wait: bool = True) -> None:
        """Delete points by ID."""
        if not point_ids:
            return
        name = collection_name or self._settings.qdrant.collection

        async def operation() -> None:
            client = await self._get_client()
            await client.delete(
                collection_name=name,
                points_selector=models.PointIdsList(points=list(point_ids)),
                wait=wait,
            )

        await self._with_retry(operation, "delete_points")

    async def delete_by_filter(
        self,
        query_filter: models.Filter,
        *,
        collection_name: str | None = None,
        wait: bool = True,
    ) -> None:
        """Delete points that match a filter."""
        name = collection_name or self._settings.qdrant.collection

        async def operation() -> None:
            client = await self._get_client()
            await client.delete(
                collection_name=name,
                points_selector=models.FilterSelector(filter=query_filter),
                wait=wait,
            )

        await self._with_retry(operation, "delete_by_filter")

    async def _get_client(self) -> AsyncQdrantClient:
        """Return an initialized Qdrant client."""
        await self.connect()
        if self._client is None:
            raise QdrantServiceError("Qdrant client is not initialized.")
        return self._client

    async def _with_retry(
        self,
        operation: Callable[[], Awaitable[Any]],
        operation_name: str,
    ) -> Any:
        """Retry transient Qdrant operations with bounded exponential backoff."""
        max_attempts = self._settings.qdrant.max_retry_attempts
        delay_seconds = self._settings.qdrant.retry_backoff_seconds
        for attempt in range(1, max_attempts + 1):
            try:
                return await operation()
            except (ResponseHandlingException, UnexpectedResponse, HTTPError, OSError) as exc:
                if attempt >= max_attempts:
                    self._logger.exception(
                        "Qdrant operation exhausted retries",
                        extra={"operation": operation_name, "attempt": attempt},
                    )
                    raise
                self._logger.warning(
                    "Retrying Qdrant operation after transient failure",
                    extra={"operation": operation_name, "attempt": attempt, "error": str(exc)},
                )
                await asyncio.sleep(delay_seconds)
                delay_seconds *= 2

    @staticmethod
    def _build_chunk_payload(chunk: DocumentChunk) -> dict[str, Any]:
        """Convert a document chunk into a JSON-serializable payload."""
        payload = chunk.model_dump(mode="json")
        payload["chunk_id"] = str(chunk.chunk_id)
        payload["document_id"] = str(chunk.document_id)
        return payload
