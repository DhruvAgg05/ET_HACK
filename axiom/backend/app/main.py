from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import structlog

from app.config import settings
from app.routers import ingest, query, graph, agents
from app.services.knowledge_graph.neo4j_client import Neo4jClient
from app.services.vectorstore.faiss_service import FAISSService
from app.services.rag.retriever import HybridRetriever

logger = structlog.get_logger()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize and cleanup resources on startup/shutdown."""
    logger.info("Starting AXIOM platform...")

    # Initialize Neo4j
    neo4j_client = Neo4jClient()
    await neo4j_client.initialize()
    app.state.neo4j = neo4j_client

    # Initialize FAISS vector index
    faiss_service = FAISSService()
    await faiss_service.initialize()
    app.state.faiss = faiss_service

    # Single shared retriever — holds the BM25 index in memory, which a fresh
    # HybridRetriever built per-request would never have (update_bm25_index
    # must be called after ingest to keep it in sync with FAISS).
    retriever = HybridRetriever(faiss_service=faiss_service, neo4j=neo4j_client)
    retriever.update_bm25_index(faiss_service.get_all_metadata())
    app.state.retriever = retriever

    logger.info("AXIOM platform ready.")
    yield

    # Cleanup
    await neo4j_client.close()
    logger.info("AXIOM platform shut down.")

app = FastAPI(
    title="AXIOM - Industrial Knowledge Intelligence",
    description="AI-powered platform for industrial document ingestion, knowledge graph construction, and intelligent retrieval.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    # No auth/cookie-based session exists in this app, so there's nothing that
    # needs allow_credentials — and wildcard origin + credentials is a combo
    # browsers reject outright (and one you don't want if auth is added later).
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ingest.router, prefix="/api/v1/ingest", tags=["Ingestion"])
app.include_router(query.router, prefix="/api/v1/query", tags=["Query"])
app.include_router(graph.router, prefix="/api/v1/graph", tags=["Knowledge Graph"])
app.include_router(agents.router, prefix="/api/v1/agents", tags=["Multi-Agent Intelligence"])

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "AXIOM"}