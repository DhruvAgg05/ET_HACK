"""Async Redis manager for caching, state, and lightweight queues."""

from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable, Mapping, Sequence
import json
import logging
from typing import Any

from redis import ConnectionError as RedisConnectionError
from redis import TimeoutError as RedisTimeoutError
import redis.asyncio as redis

from backend.app.config import Settings, get_settings


logger = logging.getLogger(__name__)


class RedisManagerError(RuntimeError):
    """Raised when a Redis operation fails."""


class RedisManager:
    """High-level async Redis manager with pooling, retries, and namespacing."""

    def __init__(self, settings: Settings | None = None) -> None:
        """Initialize the Redis manager."""
        self._settings = settings or get_settings()
        self._pool: redis.ConnectionPool | None = None
        self._client: redis.Redis | None = None
        self._lock = asyncio.Lock()
        self._logger = logger.getChild(self.__class__.__name__)

    async def __aenter__(self) -> RedisManager:
        """Open the Redis client in an async context."""
        await self.connect()
        return self

    async def __aexit__(self, exc_type: type[BaseException] | None, exc: BaseException | None, tb: Any) -> None:
        """Close Redis resources on context exit."""
        await self.close()

    async def connect(self) -> None:
        """Create the Redis connection pool and verify connectivity."""
        if self._client is not None:
            return

        async with self._lock:
            if self._client is not None:
                return

            config = self._settings.redis
            self._pool = redis.ConnectionPool.from_url(
                config.url,
                max_connections=config.max_connections,
                socket_connect_timeout=config.socket_connect_timeout_seconds,
                socket_timeout=config.socket_timeout_seconds,
                health_check_interval=config.health_check_interval_seconds,
                decode_responses=True,
                retry_on_timeout=True,
            )
            client = redis.Redis(connection_pool=self._pool)
            try:
                await client.ping()
            except (RedisConnectionError, RedisTimeoutError, OSError) as exc:
                await client.aclose()
                await self._pool.aclose()
                self._pool = None
                self._logger.exception("Redis connectivity verification failed")
                raise RedisManagerError("Failed to connect to Redis.") from exc
            self._client = client
            self._logger.info("Redis connection established", extra={"url": config.url})

    async def close(self) -> None:
        """Close Redis client and connection pool resources."""
        if self._client is None and self._pool is None:
            return

        async with self._lock:
            if self._client is not None:
                await self._client.aclose()
                self._client = None
            if self._pool is not None:
                await self._pool.aclose()
                self._pool = None
            self._logger.info("Redis connection closed")

    async def ping(self) -> bool:
        """Verify that Redis is reachable."""
        async def operation() -> bool:
            client = await self._get_client()
            return bool(await client.ping())

        return bool(await self._with_retry(operation, "ping"))

    async def get_value(self, key: str) -> str | None:
        """Get a string value by key."""
        redis_key = self._prefix_key(key)
        async def operation() -> str | None:
            client = await self._get_client()
            return await client.get(redis_key)

        return await self._with_retry(operation, "get_value")

    async def set_value(
        self,
        key: str,
        value: str,
        *,
        expire_seconds: int | None = None,
        nx: bool = False,
        xx: bool = False,
    ) -> bool:
        """Set a string value with optional expiration and existence semantics."""
        if expire_seconds is not None and expire_seconds <= 0:
            raise ValueError("expire_seconds must be greater than zero when provided.")
        redis_key = self._prefix_key(key)

        async def operation() -> bool:
            client = await self._get_client()
            result = await client.set(redis_key, value, ex=expire_seconds, nx=nx, xx=xx)
            return bool(result)

        return bool(await self._with_retry(operation, "set_value"))

    async def get_json(self, key: str) -> Any:
        """Get and deserialize a JSON value by key."""
        raw_value = await self.get_value(key)
        if raw_value is None:
            return None
        try:
            return json.loads(raw_value)
        except json.JSONDecodeError as exc:
            raise RedisManagerError(f"Stored Redis value for key {key!r} is not valid JSON.") from exc

    async def set_json(
        self,
        key: str,
        value: Any,
        *,
        expire_seconds: int | None = None,
        nx: bool = False,
        xx: bool = False,
    ) -> bool:
        """Serialize and store a JSON value."""
        return await self.set_value(
            key,
            json.dumps(value, separators=(",", ":"), ensure_ascii=False),
            expire_seconds=expire_seconds,
            nx=nx,
            xx=xx,
        )

    async def delete(self, *keys: str) -> int:
        """Delete one or more keys."""
        if not keys:
            return 0
        prefixed_keys = [self._prefix_key(key) for key in keys]

        async def operation() -> int:
            client = await self._get_client()
            return int(await client.delete(*prefixed_keys))

        return int(await self._with_retry(operation, "delete"))

    async def exists(self, key: str) -> bool:
        """Return whether a key exists."""
        redis_key = self._prefix_key(key)

        async def operation() -> bool:
            client = await self._get_client()
            return bool(await client.exists(redis_key))

        return bool(await self._with_retry(operation, "exists"))

    async def expire(self, key: str, seconds: int) -> bool:
        """Set a TTL on a key."""
        if seconds <= 0:
            raise ValueError("seconds must be greater than zero.")
        redis_key = self._prefix_key(key)

        async def operation() -> bool:
            client = await self._get_client()
            return bool(await client.expire(redis_key, seconds))

        return bool(await self._with_retry(operation, "expire"))

    async def increment(self, key: str, amount: int = 1) -> int:
        """Atomically increment an integer key."""
        redis_key = self._prefix_key(key)

        async def operation() -> int:
            client = await self._get_client()
            return int(await client.incrby(redis_key, amount))

        return int(await self._with_retry(operation, "increment"))

    async def hset_mapping(self, key: str, mapping: Mapping[str, str]) -> int:
        """Set multiple fields on a Redis hash."""
        if not mapping:
            return 0
        redis_key = self._prefix_key(key)

        async def operation() -> int:
            client = await self._get_client()
            return int(await client.hset(redis_key, mapping=mapping))

        return int(await self._with_retry(operation, "hset_mapping"))

    async def hget(self, key: str, field: str) -> str | None:
        """Get a single field from a Redis hash."""
        redis_key = self._prefix_key(key)

        async def operation() -> str | None:
            client = await self._get_client()
            return await client.hget(redis_key, field)

        return await self._with_retry(operation, "hget")

    async def hgetall(self, key: str) -> dict[str, str]:
        """Get all fields from a Redis hash."""
        redis_key = self._prefix_key(key)

        async def operation() -> dict[str, str]:
            client = await self._get_client()
            return dict(await client.hgetall(redis_key))

        return await self._with_retry(operation, "hgetall")

    async def hdel(self, key: str, *fields: str) -> int:
        """Delete one or more fields from a Redis hash."""
        if not fields:
            return 0
        redis_key = self._prefix_key(key)

        async def operation() -> int:
            client = await self._get_client()
            return int(await client.hdel(redis_key, *fields))

        return int(await self._with_retry(operation, "hdel"))

    async def enqueue(self, queue_name: str, value: str) -> int:
        """Push an item onto a Redis list queue."""
        redis_key = self._prefix_key(queue_name)

        async def operation() -> int:
            client = await self._get_client()
            return int(await client.lpush(redis_key, value))

        return int(await self._with_retry(operation, "enqueue"))

    async def dequeue(self, queue_name: str) -> str | None:
        """Pop an item from the tail of a Redis list queue."""
        redis_key = self._prefix_key(queue_name)

        async def operation() -> str | None:
            client = await self._get_client()
            return await client.rpop(redis_key)

        return await self._with_retry(operation, "dequeue")

    async def publish(self, channel: str, message: str) -> int:
        """Publish a message to a Redis pub/sub channel."""
        redis_channel = self._prefix_key(channel)

        async def operation() -> int:
            client = await self._get_client()
            return int(await client.publish(redis_channel, message))

        return int(await self._with_retry(operation, "publish"))

    async def get_ttl(self, key: str) -> int:
        """Return the TTL for a key in seconds."""
        redis_key = self._prefix_key(key)

        async def operation() -> int:
            client = await self._get_client()
            return int(await client.ttl(redis_key))

        return int(await self._with_retry(operation, "get_ttl"))

    async def flush_namespace(self) -> int:
        """Delete all keys within the configured namespace prefix."""
        pattern = self._prefix_key("*")

        async def operation() -> int:
            client = await self._get_client()
            cursor = 0
            deleted = 0
            while True:
                cursor, keys = await client.scan(cursor=cursor, match=pattern, count=500)
                if keys:
                    deleted += int(await client.delete(*keys))
                if cursor == 0:
                    break
            return deleted

        return int(await self._with_retry(operation, "flush_namespace"))

    async def _get_client(self) -> redis.Redis:
        """Return an initialized Redis client."""
        await self.connect()
        if self._client is None:
            raise RedisManagerError("Redis client is not initialized.")
        return self._client

    async def _with_retry(
        self,
        operation: Callable[[], Awaitable[Any]],
        operation_name: str,
    ) -> Any:
        """Retry transient Redis operations with bounded backoff."""
        max_attempts = self._settings.redis.max_retry_attempts
        delay_seconds = self._settings.redis.retry_backoff_seconds
        for attempt in range(1, max_attempts + 1):
            try:
                return await operation()
            except (RedisConnectionError, RedisTimeoutError, OSError) as exc:
                if attempt >= max_attempts:
                    self._logger.exception(
                        "Redis operation exhausted retries",
                        extra={"operation": operation_name, "attempt": attempt},
                    )
                    raise
                self._logger.warning(
                    "Retrying Redis operation after transient failure",
                    extra={"operation": operation_name, "attempt": attempt, "error": str(exc)},
                )
                await asyncio.sleep(delay_seconds)
                delay_seconds *= 2

    def _prefix_key(self, key: str) -> str:
        """Prefix a logical key with the configured namespace."""
        normalized = key.strip()
        if not normalized:
            raise ValueError("Redis key must not be empty.")
        prefix = self._settings.redis.key_prefix.strip(":")
        if not prefix:
            return normalized
        return f"{prefix}:{normalized}"
