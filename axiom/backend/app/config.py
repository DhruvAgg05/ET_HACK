from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    # LLM Provider: "openrouter", "ollama" (free local), "openai", or "groq"
    llm_provider: str = "openrouter"

    # OpenRouter (OpenAI-compatible chat completions, routes to many models)
    openrouter_api_key: str = ""
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    openrouter_chat_model: str = "openai/gpt-4o-mini"

    # Ollama (FREE - local)
    ollama_base_url: str = "http://localhost:11434"
    ollama_chat_model: str = "llama3.1:8b"  # or mistral, qwen2.5, phi3, gemma2
    ollama_embedding_model: str = "nomic-embed-text"  # free embedding model

    # OpenAI (optional fallback - PAID)
    openai_api_key: str = ""
    openai_embedding_model: str = "text-embedding-3-small"
    openai_chat_model: str = "gpt-4o"

    # Groq (OpenAI-compatible chat completions)
    groq_api_key: str = ""
    groq_base_url: str = "https://api.groq.com/openai/v1"
    groq_chat_model: str = "llama-3.1-8b-instant"

    # Local Embeddings (FREE - sentence-transformers)
    local_embedding_model: str = "all-MiniLM-L6-v2"  # fast, 384 dims
    # Alternative: "BAAI/bge-small-en-v1.5" (384 dims, better quality)

    # Neo4j (FREE - Community Edition)
    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: str = "axiom_password"

    # FAISS (FREE - offline vector index)
    faiss_index_dir: str = "./data/faiss"

    # Qdrant (legacy, kept for backward compatibility)
    qdrant_host: str = "localhost"
    qdrant_port: int = 6333
    qdrant_collection: str = "axiom_documents"

    # Redis (FREE - open source)
    redis_url: str = "redis://localhost:6379/0"

    # App
    upload_dir: str = "./data/uploads"
    log_level: str = "INFO"

    # Embedding dimension (384 for MiniLM/BGE-small, 768 for nomic-embed-text)
    embedding_dimension: int = 384

    # Chunking: 300-600 tokens, 50-80 overlap (per GraphRAG pipeline spec)
    chunk_size: int = 500
    chunk_overlap: int = 70

    # Retrieval scoring weights
    semantic_weight: float = 0.6
    graph_weight: float = 0.4

    # Minimum combined score for a result to be considered relevant at all.
    # Below this, we'd rather tell the user nothing was found than hand the
    # LLM (and the citation UI) chunks that only "won" by being the least bad
    # of an irrelevant candidate pool.
    min_relevance_score: float = 0.15

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()

# Ensure directories exist
Path(settings.upload_dir).mkdir(parents=True, exist_ok=True)
Path(settings.faiss_index_dir).mkdir(parents=True, exist_ok=True)
