"""Application configuration for the AXIOM platform.

This module provides strongly validated, environment-driven settings for the
backend. It supports multiple LLM providers, graph/vector/cache backends,
chunking and embedding controls, logging configuration, and automatic creation
of required upload/report directories.
"""

from __future__ import annotations

from enum import Enum
from functools import lru_cache
from pathlib import Path
from typing import Annotated
from urllib.parse import urlparse

from pydantic import BaseModel, ConfigDict, Field, SecretStr, computed_field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DATA_DIR = PROJECT_ROOT / "data"


class Environment(str, Enum):
    """Runtime environment for the backend application."""

    DEVELOPMENT = "development"
    TESTING = "testing"
    STAGING = "staging"
    PRODUCTION = "production"


class LogLevel(str, Enum):
    """Supported application log levels."""

    CRITICAL = "CRITICAL"
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"
    DEBUG = "DEBUG"
    NOTSET = "NOTSET"


class LLMProvider(str, Enum):
    """LLM provider options supported by AXIOM."""

    OLLAMA = "ollama"
    OPENAI = "openai"


class EmbeddingProvider(str, Enum):
    """Embedding provider options supported by AXIOM."""

    SENTENCE_TRANSFORMERS = "sentence_transformers"
    OLLAMA = "ollama"
    OPENAI = "openai"


class BaseConfigModel(BaseModel):
    """Base model for nested settings objects."""

    model_config = ConfigDict(extra="forbid", validate_assignment=True, str_strip_whitespace=True)


class AppConfig(BaseConfigModel):
    """Top-level application runtime settings."""

    name: Annotated[str, Field(min_length=1, max_length=128)]
    version: Annotated[str, Field(min_length=1, max_length=32)]
    environment: Environment
    debug: bool
    api_v1_prefix: Annotated[str, Field(min_length=1, max_length=64, pattern=r"^/.*")]
    host: Annotated[str, Field(min_length=1, max_length=255)]
    port: Annotated[int, Field(ge=1, le=65535)]

    @property
    def is_production(self) -> bool:
        """Return whether the service is running in production mode."""
        return self.environment == Environment.PRODUCTION


class LoggingConfig(BaseConfigModel):
    """Structured logging settings."""

    level: LogLevel
    json_logs: bool


class Neo4jConfig(BaseConfigModel):
    """Neo4j connectivity settings."""

    uri: Annotated[str, Field(min_length=1, max_length=512)]
    username: Annotated[str, Field(min_length=1, max_length=128)]
    password: SecretStr
    database: Annotated[str, Field(min_length=1, max_length=128)]
    max_connection_pool_size: Annotated[int, Field(ge=1, le=1_000)]
    connection_timeout_seconds: Annotated[float, Field(gt=0.0, le=300.0)]
    max_transaction_retry_time_seconds: Annotated[float, Field(gt=0.0, le=300.0)]
    max_retry_attempts: Annotated[int, Field(ge=1, le=20)]

    @field_validator("uri")
    @classmethod
    def validate_uri(cls, value: str) -> str:
        """Validate the Neo4j connection URI."""
        parsed = urlparse(value)
        if parsed.scheme not in {"bolt", "bolt+s", "neo4j", "neo4j+s"}:
            raise ValueError("NEO4J_URI must use bolt, bolt+s, neo4j, or neo4j+s.")
        if not parsed.hostname:
            raise ValueError("NEO4J_URI must include a hostname.")
        return value


class QdrantConfig(BaseConfigModel):
    """Qdrant vector store settings."""

    url: Annotated[str, Field(min_length=1, max_length=512)]
    api_key: SecretStr | None = None
    collection: Annotated[str, Field(min_length=1, max_length=128)]
    timeout_seconds: Annotated[float, Field(default=30.0, gt=0.0, le=300.0)]
    prefer_grpc: bool = False
    pool_size: Annotated[int, Field(ge=1, le=1_000)]
    max_retry_attempts: Annotated[int, Field(ge=1, le=20)]
    retry_backoff_seconds: Annotated[float, Field(gt=0.0, le=60.0)]

    @field_validator("url")
    @classmethod
    def validate_url(cls, value: str) -> str:
        """Validate the Qdrant endpoint URL."""
        parsed = urlparse(value)
        if parsed.scheme not in {"http", "https"}:
            raise ValueError("QDRANT_URL must use http or https.")
        if not parsed.hostname:
            raise ValueError("QDRANT_URL must include a hostname.")
        return value.rstrip("/")


class RedisConfig(BaseConfigModel):
    """Redis and Celery transport settings."""

    url: Annotated[str, Field(min_length=1, max_length=512)]
    celery_broker_url: Annotated[str, Field(min_length=1, max_length=512)]
    celery_result_backend: Annotated[str, Field(min_length=1, max_length=512)]
    max_connections: Annotated[int, Field(ge=1, le=10_000)]
    socket_connect_timeout_seconds: Annotated[float, Field(gt=0.0, le=300.0)]
    socket_timeout_seconds: Annotated[float, Field(gt=0.0, le=300.0)]
    health_check_interval_seconds: Annotated[int, Field(ge=0, le=3_600)]
    max_retry_attempts: Annotated[int, Field(ge=1, le=20)]
    retry_backoff_seconds: Annotated[float, Field(gt=0.0, le=60.0)]
    key_prefix: Annotated[str, Field(min_length=0, max_length=128)]

    @field_validator("url", "celery_broker_url", "celery_result_backend")
    @classmethod
    def validate_redis_url(cls, value: str) -> str:
        """Validate Redis DSNs used by the platform."""
        parsed = urlparse(value)
        if parsed.scheme not in {"redis", "rediss"}:
            raise ValueError("Redis URLs must use redis or rediss schemes.")
        if not parsed.hostname:
            raise ValueError("Redis URLs must include a hostname.")
        return value


class OllamaConfig(BaseConfigModel):
    """Local Ollama runtime settings."""

    base_url: Annotated[str, Field(min_length=1, max_length=512)]
    model: Annotated[str, Field(min_length=1, max_length=255)]
    timeout_seconds: Annotated[float, Field(default=120.0, gt=0.0, le=600.0)]

    @field_validator("base_url")
    @classmethod
    def validate_base_url(cls, value: str) -> str:
        """Validate the Ollama base URL."""
        parsed = urlparse(value)
        if parsed.scheme not in {"http", "https"}:
            raise ValueError("OLLAMA_BASE_URL must use http or https.")
        if not parsed.hostname:
            raise ValueError("OLLAMA_BASE_URL must include a hostname.")
        return value.rstrip("/")


class OpenAIConfig(BaseConfigModel):
    """OpenAI provider settings."""

    api_key: SecretStr | None = None
    model: Annotated[str, Field(min_length=1, max_length=255)]
    timeout_seconds: Annotated[float, Field(default=120.0, gt=0.0, le=600.0)]


class ChunkingConfig(BaseConfigModel):
    """Semantic chunking parameters used during ingestion and retrieval."""

    max_chars: Annotated[int, Field(default=512, ge=128, le=8_192)]
    overlap_chars: Annotated[int, Field(default=64, ge=0, le=2_048)]
    min_chars: Annotated[int, Field(default=120, ge=32, le=4_096)]
    preserve_headings: bool = True
    preserve_sentences: bool = True

    @model_validator(mode="after")
    def validate_chunk_ranges(self) -> ChunkingConfig:
        """Ensure chunk sizing parameters are internally consistent."""
        if self.min_chars >= self.max_chars:
            raise ValueError("CHUNK_MIN_CHARS must be smaller than CHUNK_MAX_CHARS.")
        if self.overlap_chars >= self.max_chars:
            raise ValueError("CHUNK_OVERLAP_CHARS must be smaller than CHUNK_MAX_CHARS.")
        return self


class EmbeddingConfig(BaseConfigModel):
    """Embedding model and vectorization settings."""

    provider: EmbeddingProvider
    model_name: Annotated[str, Field(min_length=1, max_length=255)]
    vector_size: Annotated[int, Field(default=384, ge=32, le=16_384)]
    batch_size: Annotated[int, Field(default=32, ge=1, le=1_024)]
    normalize_embeddings: bool = True
    device: Annotated[str, Field(default="cpu", min_length=1, max_length=64)]


class StorageConfig(BaseConfigModel):
    """Filesystem storage and upload path settings."""

    data_dir: Path
    uploads_dir: Path
    processed_dir: Path
    failed_dir: Path
    temp_dir: Path
    reports_dir: Path
    sample_documents_dir: Path
    sensor_reports_dir: Path
    fault_reports_dir: Path
    predictive_reports_dir: Path
    shift_handover_reports_dir: Path

    @property
    def upload_dirs(self) -> tuple[Path, ...]:
        """Return upload-related directories to provision."""
        return (
            self.uploads_dir,
            self.processed_dir,
            self.failed_dir,
            self.temp_dir,
        )

    @property
    def all_dirs(self) -> tuple[Path, ...]:
        """Return all managed storage directories."""
        return (
            self.data_dir,
            self.uploads_dir,
            self.processed_dir,
            self.failed_dir,
            self.temp_dir,
            self.reports_dir,
            self.sample_documents_dir,
            self.sensor_reports_dir,
            self.fault_reports_dir,
            self.predictive_reports_dir,
            self.shift_handover_reports_dir,
        )


class Settings(BaseSettings):
    """Environment-backed runtime settings for the AXIOM backend."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        validate_default=True,
    )

    app_name: Annotated[str, Field(default="AXIOM Platform", alias="APP_NAME", min_length=1, max_length=128)]
    app_version: Annotated[str, Field(default="0.1.0", alias="APP_VERSION", min_length=1, max_length=32)]
    environment: Environment = Field(default=Environment.DEVELOPMENT, alias="ENVIRONMENT")
    debug: bool = Field(default=False, alias="DEBUG")
    api_v1_prefix: Annotated[str, Field(default="/api/v1", alias="API_V1_PREFIX", min_length=1, max_length=64)]
    host: Annotated[str, Field(default="0.0.0.0", alias="HOST", min_length=1, max_length=255)]
    port: Annotated[int, Field(default=8000, alias="PORT", ge=1, le=65535)]

    log_level: LogLevel = Field(default=LogLevel.INFO, alias="LOG_LEVEL")
    structlog_json: bool = Field(default=False, alias="STRUCTLOG_JSON")

    llm_provider: LLMProvider = Field(default=LLMProvider.OLLAMA, alias="LLM_PROVIDER")
    ollama_base_url: Annotated[str, Field(default="http://localhost:11434", alias="OLLAMA_BASE_URL", min_length=1, max_length=512)]
    ollama_model: Annotated[str, Field(default="llama3.1:8b", alias="OLLAMA_MODEL", min_length=1, max_length=255)]
    ollama_timeout_seconds: Annotated[float, Field(default=120.0, alias="OLLAMA_TIMEOUT_SECONDS", gt=0.0, le=600.0)]
    openai_api_key: SecretStr | None = Field(default=None, alias="OPENAI_API_KEY")
    openai_model: Annotated[str, Field(default="gpt-4o-mini", alias="OPENAI_MODEL", min_length=1, max_length=255)]
    openai_timeout_seconds: Annotated[float, Field(default=120.0, alias="OPENAI_TIMEOUT_SECONDS", gt=0.0, le=600.0)]

    embedding_provider: EmbeddingProvider = Field(
        default=EmbeddingProvider.SENTENCE_TRANSFORMERS,
        alias="EMBEDDING_PROVIDER",
    )
    embedding_model: Annotated[
        str,
        Field(
            default="sentence-transformers/all-MiniLM-L6-v2",
            alias="EMBEDDING_MODEL",
            min_length=1,
            max_length=255,
        ),
    ]
    embedding_vector_size: Annotated[int, Field(default=384, alias="EMBEDDING_VECTOR_SIZE", ge=32, le=16_384)]
    embedding_batch_size: Annotated[int, Field(default=32, alias="EMBEDDING_BATCH_SIZE", ge=1, le=1_024)]
    normalize_embeddings: bool = Field(default=True, alias="NORMALIZE_EMBEDDINGS")
    embedding_device: Annotated[str, Field(default="cpu", alias="EMBEDDING_DEVICE", min_length=1, max_length=64)]

    chunk_max_chars: Annotated[int, Field(default=512, alias="CHUNK_MAX_CHARS", ge=128, le=8_192)]
    chunk_overlap_chars: Annotated[int, Field(default=64, alias="CHUNK_OVERLAP_CHARS", ge=0, le=2_048)]
    chunk_min_chars: Annotated[int, Field(default=120, alias="CHUNK_MIN_CHARS", ge=32, le=4_096)]
    chunk_preserve_headings: bool = Field(default=True, alias="CHUNK_PRESERVE_HEADINGS")
    chunk_preserve_sentences: bool = Field(default=True, alias="CHUNK_PRESERVE_SENTENCES")

    neo4j_uri: Annotated[str, Field(default="bolt://localhost:7687", alias="NEO4J_URI", min_length=1, max_length=512)]
    neo4j_username: Annotated[str, Field(default="neo4j", alias="NEO4J_USERNAME", min_length=1, max_length=128)]
    neo4j_password: SecretStr = Field(alias="NEO4J_PASSWORD")
    neo4j_database: Annotated[str, Field(default="neo4j", alias="NEO4J_DATABASE", min_length=1, max_length=128)]
    neo4j_max_connection_pool_size: Annotated[
        int,
        Field(default=50, alias="NEO4J_MAX_CONNECTION_POOL_SIZE", ge=1, le=1_000),
    ]
    neo4j_connection_timeout_seconds: Annotated[
        float,
        Field(default=30.0, alias="NEO4J_CONNECTION_TIMEOUT_SECONDS", gt=0.0, le=300.0),
    ]
    neo4j_max_transaction_retry_time_seconds: Annotated[
        float,
        Field(default=15.0, alias="NEO4J_MAX_TRANSACTION_RETRY_TIME_SECONDS", gt=0.0, le=300.0),
    ]
    neo4j_max_retry_attempts: Annotated[int, Field(default=3, alias="NEO4J_MAX_RETRY_ATTEMPTS", ge=1, le=20)]

    qdrant_url: Annotated[str, Field(default="http://localhost:6333", alias="QDRANT_URL", min_length=1, max_length=512)]
    qdrant_api_key: SecretStr | None = Field(default=None, alias="QDRANT_API_KEY")
    qdrant_collection: Annotated[str, Field(default="axiom_documents", alias="QDRANT_COLLECTION", min_length=1, max_length=128)]
    qdrant_timeout_seconds: Annotated[float, Field(default=30.0, alias="QDRANT_TIMEOUT_SECONDS", gt=0.0, le=300.0)]
    qdrant_prefer_grpc: bool = Field(default=False, alias="QDRANT_PREFER_GRPC")
    qdrant_pool_size: Annotated[int, Field(default=25, alias="QDRANT_POOL_SIZE", ge=1, le=1_000)]
    qdrant_max_retry_attempts: Annotated[int, Field(default=3, alias="QDRANT_MAX_RETRY_ATTEMPTS", ge=1, le=20)]
    qdrant_retry_backoff_seconds: Annotated[
        float,
        Field(default=1.0, alias="QDRANT_RETRY_BACKOFF_SECONDS", gt=0.0, le=60.0),
    ]

    redis_url: Annotated[str, Field(default="redis://localhost:6379/0", alias="REDIS_URL", min_length=1, max_length=512)]
    celery_broker_url: Annotated[
        str,
        Field(default="redis://localhost:6379/1", alias="CELERY_BROKER_URL", min_length=1, max_length=512),
    ]
    celery_result_backend: Annotated[
        str,
        Field(default="redis://localhost:6379/2", alias="CELERY_RESULT_BACKEND", min_length=1, max_length=512),
    ]
    redis_max_connections: Annotated[int, Field(default=200, alias="REDIS_MAX_CONNECTIONS", ge=1, le=10_000)]
    redis_socket_connect_timeout_seconds: Annotated[
        float,
        Field(default=5.0, alias="REDIS_SOCKET_CONNECT_TIMEOUT_SECONDS", gt=0.0, le=300.0),
    ]
    redis_socket_timeout_seconds: Annotated[
        float,
        Field(default=5.0, alias="REDIS_SOCKET_TIMEOUT_SECONDS", gt=0.0, le=300.0),
    ]
    redis_health_check_interval_seconds: Annotated[
        int,
        Field(default=30, alias="REDIS_HEALTH_CHECK_INTERVAL_SECONDS", ge=0, le=3_600),
    ]
    redis_max_retry_attempts: Annotated[int, Field(default=3, alias="REDIS_MAX_RETRY_ATTEMPTS", ge=1, le=20)]
    redis_retry_backoff_seconds: Annotated[
        float,
        Field(default=0.5, alias="REDIS_RETRY_BACKOFF_SECONDS", gt=0.0, le=60.0),
    ]
    redis_key_prefix: Annotated[str, Field(default="axiom", alias="REDIS_KEY_PREFIX", min_length=0, max_length=128)]

    data_dir: Path = Field(default=DEFAULT_DATA_DIR, alias="DATA_DIR")
    uploads_dir: Path = Field(default=DEFAULT_DATA_DIR / "uploads", alias="UPLOADS_DIR")
    processed_dir: Path = Field(default=DEFAULT_DATA_DIR / "uploads" / "processed", alias="PROCESSED_DIR")
    failed_dir: Path = Field(default=DEFAULT_DATA_DIR / "uploads" / "failed", alias="FAILED_DIR")
    temp_dir: Path = Field(default=DEFAULT_DATA_DIR / "uploads" / "tmp", alias="TEMP_DIR")
    reports_dir: Path = Field(default=DEFAULT_DATA_DIR / "reports", alias="REPORTS_DIR")
    sample_documents_dir: Path = Field(default=DEFAULT_DATA_DIR / "sample_documents", alias="SAMPLE_DOCUMENTS_DIR")
    sensor_reports_dir: Path = Field(default=DEFAULT_DATA_DIR / "reports" / "sensor_analysis", alias="SENSOR_REPORTS_DIR")
    fault_reports_dir: Path = Field(default=DEFAULT_DATA_DIR / "reports" / "fault_diagnosis", alias="FAULT_REPORTS_DIR")
    predictive_reports_dir: Path = Field(default=DEFAULT_DATA_DIR / "reports" / "predictive", alias="PREDICTIVE_REPORTS_DIR")
    shift_handover_reports_dir: Path = Field(
        default=DEFAULT_DATA_DIR / "reports" / "shift_handover",
        alias="SHIFT_HANDOVER_REPORTS_DIR",
    )

    spacy_model: Annotated[str, Field(default="en_core_web_sm", alias="SPACY_MODEL", min_length=1, max_length=255)]
    gliner_model: Annotated[str, Field(default="urchade/gliner_medium-v2.1", alias="GLINER_MODEL", min_length=1, max_length=255)]
    tesseract_cmd: Path = Field(default=Path("/usr/bin/tesseract"), alias="TESSERACT_CMD")

    @field_validator(
        "data_dir",
        "uploads_dir",
        "processed_dir",
        "failed_dir",
        "temp_dir",
        "reports_dir",
        "sample_documents_dir",
        "sensor_reports_dir",
        "fault_reports_dir",
        "predictive_reports_dir",
        "shift_handover_reports_dir",
        "tesseract_cmd",
        mode="before",
    )
    @classmethod
    def normalize_path(cls, value: str | Path) -> Path:
        """Resolve configured paths relative to the repository root when needed."""
        path = Path(value).expanduser()
        if not path.is_absolute():
            path = (PROJECT_ROOT / path).resolve()
        return path

    @field_validator("neo4j_uri")
    @classmethod
    def validate_neo4j_uri(cls, value: str) -> str:
        """Validate Neo4j DSN values."""
        parsed = urlparse(value)
        if parsed.scheme not in {"bolt", "bolt+s", "neo4j", "neo4j+s"}:
            raise ValueError("NEO4J_URI must use bolt, bolt+s, neo4j, or neo4j+s.")
        if not parsed.hostname:
            raise ValueError("NEO4J_URI must include a hostname.")
        return value

    @field_validator("qdrant_url", "ollama_base_url")
    @classmethod
    def validate_http_urls(cls, value: str) -> str:
        """Validate HTTP(S) endpoint URLs."""
        parsed = urlparse(value)
        if parsed.scheme not in {"http", "https"}:
            raise ValueError("Configured service URL must use http or https.")
        if not parsed.hostname:
            raise ValueError("Configured service URL must include a hostname.")
        return value.rstrip("/")

    @field_validator("redis_url", "celery_broker_url", "celery_result_backend")
    @classmethod
    def validate_redis_urls(cls, value: str) -> str:
        """Validate Redis URLs."""
        parsed = urlparse(value)
        if parsed.scheme not in {"redis", "rediss"}:
            raise ValueError("Redis URLs must use redis or rediss.")
        if not parsed.hostname:
            raise ValueError("Redis URLs must include a hostname.")
        return value

    @model_validator(mode="after")
    def validate_provider_requirements(self) -> Settings:
        """Validate cross-field provider requirements and create storage folders."""
        if self.environment == Environment.PRODUCTION and self.debug:
            raise ValueError("DEBUG must be false in production.")

        if self.llm_provider == LLMProvider.OPENAI:
            if self.openai_api_key is None or not self.openai_api_key.get_secret_value().strip():
                raise ValueError("OPENAI_API_KEY is required when LLM_PROVIDER=openai.")

        if self.embedding_provider == EmbeddingProvider.OPENAI:
            if self.openai_api_key is None or not self.openai_api_key.get_secret_value().strip():
                raise ValueError("OPENAI_API_KEY is required when EMBEDDING_PROVIDER=openai.")

        if self.embedding_provider == EmbeddingProvider.OLLAMA and not self.ollama_model.strip():
            raise ValueError("OLLAMA_MODEL is required when EMBEDDING_PROVIDER=ollama.")

        if self.chunk_overlap_chars >= self.chunk_max_chars:
            raise ValueError("CHUNK_OVERLAP_CHARS must be smaller than CHUNK_MAX_CHARS.")
        if self.chunk_min_chars >= self.chunk_max_chars:
            raise ValueError("CHUNK_MIN_CHARS must be smaller than CHUNK_MAX_CHARS.")

        self._create_storage_directories()
        return self

    def _create_storage_directories(self) -> None:
        """Create required storage directories if they do not yet exist."""
        directories = (
            self.data_dir,
            self.uploads_dir,
            self.processed_dir,
            self.failed_dir,
            self.temp_dir,
            self.reports_dir,
            self.sample_documents_dir,
            self.sensor_reports_dir,
            self.fault_reports_dir,
            self.predictive_reports_dir,
            self.shift_handover_reports_dir,
        )
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)

    @computed_field(return_type=AppConfig)
    @property
    def app(self) -> AppConfig:
        """Return grouped application settings."""
        return AppConfig(
            name=self.app_name,
            version=self.app_version,
            environment=self.environment,
            debug=self.debug,
            api_v1_prefix=self.api_v1_prefix,
            host=self.host,
            port=self.port,
        )

    @computed_field(return_type=LoggingConfig)
    @property
    def logging(self) -> LoggingConfig:
        """Return grouped logging settings."""
        return LoggingConfig(level=self.log_level, json_logs=self.structlog_json)

    @computed_field(return_type=Neo4jConfig)
    @property
    def neo4j(self) -> Neo4jConfig:
        """Return grouped Neo4j settings."""
        return Neo4jConfig(
            uri=self.neo4j_uri,
            username=self.neo4j_username,
            password=self.neo4j_password,
            database=self.neo4j_database,
            max_connection_pool_size=self.neo4j_max_connection_pool_size,
            connection_timeout_seconds=self.neo4j_connection_timeout_seconds,
            max_transaction_retry_time_seconds=self.neo4j_max_transaction_retry_time_seconds,
            max_retry_attempts=self.neo4j_max_retry_attempts,
        )

    @computed_field(return_type=QdrantConfig)
    @property
    def qdrant(self) -> QdrantConfig:
        """Return grouped Qdrant settings."""
        return QdrantConfig(
            url=self.qdrant_url,
            api_key=self.qdrant_api_key,
            collection=self.qdrant_collection,
            timeout_seconds=self.qdrant_timeout_seconds,
            prefer_grpc=self.qdrant_prefer_grpc,
            pool_size=self.qdrant_pool_size,
            max_retry_attempts=self.qdrant_max_retry_attempts,
            retry_backoff_seconds=self.qdrant_retry_backoff_seconds,
        )

    @computed_field(return_type=RedisConfig)
    @property
    def redis(self) -> RedisConfig:
        """Return grouped Redis and Celery settings."""
        return RedisConfig(
            url=self.redis_url,
            celery_broker_url=self.celery_broker_url,
            celery_result_backend=self.celery_result_backend,
            max_connections=self.redis_max_connections,
            socket_connect_timeout_seconds=self.redis_socket_connect_timeout_seconds,
            socket_timeout_seconds=self.redis_socket_timeout_seconds,
            health_check_interval_seconds=self.redis_health_check_interval_seconds,
            max_retry_attempts=self.redis_max_retry_attempts,
            retry_backoff_seconds=self.redis_retry_backoff_seconds,
            key_prefix=self.redis_key_prefix,
        )

    @computed_field(return_type=OllamaConfig)
    @property
    def ollama(self) -> OllamaConfig:
        """Return grouped Ollama settings."""
        return OllamaConfig(
            base_url=self.ollama_base_url,
            model=self.ollama_model,
            timeout_seconds=self.ollama_timeout_seconds,
        )

    @computed_field(return_type=OpenAIConfig)
    @property
    def openai(self) -> OpenAIConfig:
        """Return grouped OpenAI settings."""
        return OpenAIConfig(
            api_key=self.openai_api_key,
            model=self.openai_model,
            timeout_seconds=self.openai_timeout_seconds,
        )

    @computed_field(return_type=ChunkingConfig)
    @property
    def chunking(self) -> ChunkingConfig:
        """Return grouped chunking settings."""
        return ChunkingConfig(
            max_chars=self.chunk_max_chars,
            overlap_chars=self.chunk_overlap_chars,
            min_chars=self.chunk_min_chars,
            preserve_headings=self.chunk_preserve_headings,
            preserve_sentences=self.chunk_preserve_sentences,
        )

    @computed_field(return_type=EmbeddingConfig)
    @property
    def embeddings(self) -> EmbeddingConfig:
        """Return grouped embedding settings."""
        return EmbeddingConfig(
            provider=self.embedding_provider,
            model_name=self.embedding_model,
            vector_size=self.embedding_vector_size,
            batch_size=self.embedding_batch_size,
            normalize_embeddings=self.normalize_embeddings,
            device=self.embedding_device,
        )

    @computed_field(return_type=StorageConfig)
    @property
    def storage(self) -> StorageConfig:
        """Return grouped storage and upload directory settings."""
        return StorageConfig(
            data_dir=self.data_dir,
            uploads_dir=self.uploads_dir,
            processed_dir=self.processed_dir,
            failed_dir=self.failed_dir,
            temp_dir=self.temp_dir,
            reports_dir=self.reports_dir,
            sample_documents_dir=self.sample_documents_dir,
            sensor_reports_dir=self.sensor_reports_dir,
            fault_reports_dir=self.fault_reports_dir,
            predictive_reports_dir=self.predictive_reports_dir,
            shift_handover_reports_dir=self.shift_handover_reports_dir,
        )

    @property
    def active_llm_model(self) -> str:
        """Return the currently active LLM model name."""
        if self.llm_provider == LLMProvider.OPENAI:
            return self.openai_model
        return self.ollama_model

    @property
    def active_llm_timeout_seconds(self) -> float:
        """Return the timeout for the active LLM provider."""
        if self.llm_provider == LLMProvider.OPENAI:
            return self.openai_timeout_seconds
        return self.ollama_timeout_seconds


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return a cached settings instance for dependency injection."""
    return Settings()
