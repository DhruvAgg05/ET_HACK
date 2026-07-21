"""
Query API — handles user questions with hybrid retrieval and LLM answer generation.
Includes streaming endpoint that visualizes retrieval and generation steps.
"""

from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import StreamingResponse
import json
import time
import asyncio
import structlog

from app.models.schemas import QueryRequest, QueryResponse
from app.services.rag.retriever import HybridRetriever
from app.services.rag.generator import AnswerGenerator
from app.services.vectorstore.faiss_service import FAISSService
from app.services.knowledge_graph.neo4j_client import Neo4jClient

logger = structlog.get_logger()
router = APIRouter()

@router.post("/ask", response_model=QueryResponse)
async def ask_question(request: Request, query: QueryRequest):
    """
    Ask a question and get an AI-generated answer with source citations.

    Pipeline:
    1. Parse and classify the user query
    2. Hybrid retrieval (vector + graph + keyword)
    3. Context assembly with source metadata
    4. LLM answer generation with citations
    5. Confidence scoring
    6. Follow-up suggestions
    """
    if not query.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    logger.info("Query received", question=query.question[:100])

    # Get services from app state
    faiss_service: FAISSService = request.app.state.faiss
    neo4j: Neo4jClient = request.app.state.neo4j

    # Initialize retriever (FAISS + Neo4j hybrid)
    retriever = HybridRetriever(faiss_service=faiss_service, neo4j=neo4j)

    # Perform hybrid retrieval
    category_filter = query.filters.get("category") if query.filters else None
    retrieved = await retriever.retrieve(
        query=query.question,
        top_k=query.top_k,
        use_graph=query.include_graph_context,
        category_filter=category_filter,
    )

    # Get additional graph context for equipment-specific queries
    graph_context = None
    if query.include_graph_context:
        graph_context = await _get_graph_context(neo4j, query.question)

    # Generate answer
    generator = AnswerGenerator()
    response = await generator.generate(
        query=query.question,
        retrieved_chunks=retrieved,
        graph_context=graph_context,
    )

    logger.info(
        "Query answered",
        confidence=response.confidence,
        sources=len(response.sources),
    )

    return response

@router.post("/search")
async def search_documents(request: Request, query: QueryRequest):
    """
    Search documents without answer generation — returns ranked chunks.
    Useful for exploring the document corpus.
    """
    faiss_service: FAISSService = request.app.state.faiss
    neo4j: Neo4jClient = request.app.state.neo4j

    retriever = HybridRetriever(faiss_service=faiss_service, neo4j=neo4j)

    category_filter = query.filters.get("category") if query.filters else None
    retrieved = await retriever.retrieve(
        query=query.question,
        top_k=query.top_k,
        category_filter=category_filter,
    )

    return {
        "query": query.question,
        "results": [
            {
                "chunk_id": r.chunk_id,
                "document_id": r.document_id,
                "filename": r.filename,
                "content": r.content,
                "page_number": r.page_number,
                "relevance_score": r.score,
                "source_type": r.source_type,
            }
            for r in retrieved
        ],
        "total_results": len(retrieved),
    }

async def _get_graph_context(neo4j: Neo4jClient, question: str) -> dict | None:
    """Extract graph context relevant to the question."""
    import re

    # Look for equipment tags in the question
    equipment_tags = re.findall(r"\b[A-Z]{1,4}-\d{2,5}[A-Z]?\b", question)

    if equipment_tags:
        # Get context for the first equipment tag found
        context = await neo4j.get_equipment_context(equipment_tags[0])
        if context:
            return context

    return None

def _sse_event(event: str, data: dict) -> str:
    """Format a Server-Sent Event."""
    return f"event: {event}\ndata: {json.dumps(data)}\n\n"

@router.post("/ask/stream")
async def ask_question_stream(request: Request, query: QueryRequest):
    """
    Stream the query pipeline steps: embedding → FAISS search → graph expansion →
    re-ranking → context assembly → LLM generation.
    """
    if not query.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    faiss_service: FAISSService = request.app.state.faiss
    neo4j: Neo4jClient = request.app.state.neo4j

    async def generate_events():
        pipeline_start = time.time()

        # === STEP 1: Query Analysis ===
        yield _sse_event("step", {
            "step": 1, "name": "Query Analysis",
            "status": "running",
            "description": "Parsing query and extracting search terms..."
        })
        await asyncio.sleep(0.05)

        import re
        equipment_tags = re.findall(r"\b[A-Z]{1,4}-\d{2,5}[A-Z]?\b", query.question)
        regulation_refs = re.findall(r"\b(?:OISD|API|ISO|ASME)[-\s]?\d+\b", query.question)
        stop_words = {"what", "is", "the", "a", "an", "of", "for", "in", "on", "at", "to", "from", "by", "with", "how", "when", "where", "which", "show", "me", "tell", "find", "get"}
        key_terms = [w for w in query.question.split() if w.lower() not in stop_words and len(w) > 2]

        yield _sse_event("step", {
            "step": 1, "name": "Query Analysis",
            "status": "complete",
            "result": {
                "question": query.question,
                "equipment_tags": equipment_tags,
                "regulation_refs": regulation_refs,
                "key_terms": key_terms[:10],
                "will_use_graph": bool(equipment_tags or regulation_refs),
            },
            "duration_ms": int((time.time() - pipeline_start) * 1000),
        })

        # === STEP 2: Query Embedding ===
        step2_start = time.time()
        yield _sse_event("step", {
            "step": 2, "name": "Query Embedding",
            "status": "running",
            "description": "Generating query vector with sentence-transformers..."
        })

        from app.config import settings
        query_embedding = await faiss_service.generate_embedding(query.question)

        yield _sse_event("step", {
            "step": 2, "name": "Query Embedding",
            "status": "complete",
            "result": {
                "model": settings.local_embedding_model,
                "dimension": len(query_embedding),
                "vector_preview": [round(v, 4) for v in query_embedding[:8]] + ["..."],
            },
            "duration_ms": int((time.time() - step2_start) * 1000),
        })

        # === STEP 3: FAISS Semantic Search ===
        step3_start = time.time()
        yield _sse_event("step", {
            "step": 3, "name": "FAISS Semantic Search",
            "status": "running",
            "description": f"Searching top-{query.top_k * 2} similar chunks..."
        })

        category_filter = query.filters.get("category") if query.filters else None
        vector_results = await faiss_service.search(
            query=query.question, top_k=query.top_k * 2, category_filter=category_filter
        )

        vector_chunks = [
            {
                "chunk_id": r["chunk_id"],
                "filename": r.get("filename", ""),
                "page": r.get("page_number"),
                "score": round(r["score"], 4),
                "preview": r["content"][:120],
            }
            for r in vector_results
        ]

        yield _sse_event("step", {
            "step": 3, "name": "FAISS Semantic Search",
            "status": "complete",
            "result": {
                "chunks_found": len(vector_results),
                "top_score": vector_chunks[0]["score"] if vector_chunks else 0,
                "chunks": vector_chunks[:6],
            },
            "duration_ms": int((time.time() - step3_start) * 1000),
        })

        # === STEP 4: Neo4j Graph Expansion ===
        step4_start = time.time()
        yield _sse_event("step", {
            "step": 4, "name": "Neo4j Graph Expansion",
            "status": "running",
            "description": "Expanding entity neighborhoods in knowledge graph..."
        })

        graph_context_parts = []
        graph_nodes_found = 0

        for tag in equipment_tags:
            try:
                context = await neo4j.get_equipment_context(tag)
                if context:
                    graph_context_parts.append({
                        "entity": tag,
                        "type": "equipment",
                        "neighbors": str(context)[:200],
                    })
                    graph_nodes_found += 1
            except Exception:
                pass

        for ref in regulation_refs:
            try:
                neighbors = await neo4j.get_neighbors("Regulation", "standard_id", ref)
                if neighbors:
                    graph_context_parts.append({
                        "entity": ref,
                        "type": "regulation",
                        "neighbors": str(neighbors[:3])[:200],
                    })
                    graph_nodes_found += 1
            except Exception:
                pass

        # General search
        for term in key_terms[:3]:
            try:
                nodes = await neo4j.search_nodes(term, limit=3)
                for node in nodes:
                    graph_nodes_found += 1
            except Exception:
                pass

        yield _sse_event("step", {
            "step": 4, "name": "Neo4j Graph Expansion",
            "status": "complete",
            "result": {
                "entities_searched": len(equipment_tags) + len(regulation_refs) + min(len(key_terms), 3),
                "graph_nodes_found": graph_nodes_found,
                "graph_context": graph_context_parts[:5],
            },
            "duration_ms": int((time.time() - step4_start) * 1000),
        })

        # === STEP 5: Re-Ranking ===
        step5_start = time.time()
        yield _sse_event("step", {
            "step": 5, "name": "Hybrid Re-Ranking",
            "status": "running",
            "description": f"Scoring: {settings.semantic_weight} × Semantic + {settings.graph_weight} × Graph..."
        })

        retriever = HybridRetriever(faiss_service=faiss_service, neo4j=neo4j)
        final_results = await retriever.retrieve(
            query=query.question,
            top_k=query.top_k,
            use_graph=query.include_graph_context,
            category_filter=category_filter,
        )

        ranked_chunks = [
            {
                "rank": i + 1,
                "chunk_id": r.chunk_id,
                "filename": r.filename,
                "page": r.page_number,
                "final_score": round(r.score, 4),
                "source_type": r.source_type,
                "content": r.content[:200],
            }
            for i, r in enumerate(final_results)
        ]

        yield _sse_event("step", {
            "step": 5, "name": "Hybrid Re-Ranking",
            "status": "complete",
            "result": {
                "scoring_formula": f"{settings.semantic_weight} × Semantic + {settings.graph_weight} × Graph",
                "final_chunks": len(ranked_chunks),
                "ranked_results": ranked_chunks,
            },
            "duration_ms": int((time.time() - step5_start) * 1000),
        })

        # === STEP 6: Context Assembly ===
        step6_start = time.time()
        yield _sse_event("step", {
            "step": 6, "name": "Context Assembly",
            "status": "running",
            "description": "Building context prompt for LLM..."
        })

        context_text = ""
        for i, r in enumerate(final_results):
            context_text += f"\n[Source {i+1}: {r.filename} p.{r.page_number}]\n{r.content}\n"

        yield _sse_event("step", {
            "step": 6, "name": "Context Assembly",
            "status": "complete",
            "result": {
                "context_length": len(context_text),
                "sources_included": len(final_results),
                "context_preview": context_text[:500],
            },
            "duration_ms": int((time.time() - step6_start) * 1000),
        })

        # === STEP 7: LLM Generation ===
        step7_start = time.time()
        yield _sse_event("step", {
            "step": 7, "name": "LLM Generation",
            "status": "running",
            "description": f"Sending to {settings.ollama_chat_model} via Ollama..."
        })

        generator = AnswerGenerator()
        graph_ctx = None
        if equipment_tags:
            try:
                graph_ctx = await neo4j.get_equipment_context(equipment_tags[0])
            except Exception:
                pass

        response = await generator.generate(
            query=query.question,
            retrieved_chunks=final_results,
            graph_context=graph_ctx,
        )

        yield _sse_event("step", {
            "step": 7, "name": "LLM Generation",
            "status": "complete",
            "result": {
                "model": settings.ollama_chat_model,
                "answer_length": len(response.answer) if hasattr(response, 'answer') else 0,
                "confidence": response.confidence if hasattr(response, 'confidence') else "unknown",
                "sources_cited": len(response.sources) if hasattr(response, 'sources') else 0,
            },
            "duration_ms": int((time.time() - step7_start) * 1000),
        })

        # === FINAL ===
        total_duration = int((time.time() - pipeline_start) * 1000)
        yield _sse_event("complete", {
            "answer": response.answer if hasattr(response, 'answer') else str(response),
            "confidence": response.confidence if hasattr(response, 'confidence') else "unknown",
            "sources": [{"filename": s.filename, "page_number": s.page_number} for s in response.sources] if hasattr(response, 'sources') else [],
            "suggested_followups": response.suggested_followups if hasattr(response, 'suggested_followups') else [],
            "total_duration_ms": total_duration,
            "chunks_retrieved": len(final_results),
        })

    return StreamingResponse(
        generate_events(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )