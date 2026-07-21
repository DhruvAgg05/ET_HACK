"""
Knowledge Graph API — direct graph exploration, FAISS index stats, and search endpoints.
"""

from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
import structlog

from app.services.knowledge_graph.neo4j_client import Neo4jClient
from app.services.vectorstore.faiss_service import FAISSService

logger = structlog.get_logger()
router = APIRouter()

class GraphSearchRequest(BaseModel):
    query: str
    node_type: str | None = None
    depth: int = 2
    limit: int = 50

@router.post("/search")
async def search_graph(request: Request, search: GraphSearchRequest):
    """Search the knowledge graph and FAISS index for matching results."""
    neo4j: Neo4jClient = request.app.state.neo4j
    faiss_service: FAISSService = request.app.state.faiss

    results = []

    # Try Neo4j search
    neo4j_results = await neo4j.search_nodes(search.query, limit=search.limit)
    for r in neo4j_results:
        results.append({**r, "source": "neo4j"})

    # Also search FAISS metadata for document/chunk matches
    faiss_matches = []
    for meta in faiss_service.get_all_metadata():
        term = search.query.lower()
        if (term in meta.get("filename", "").lower()
            or term in meta.get("content", "").lower()
            or term in meta.get("category", "").lower()):
            faiss_matches.append({
                "label": "Chunk",
                "props": {
                    "chunk_id": meta["chunk_id"],
                    "document_id": meta["document_id"],
                    "filename": meta.get("filename", ""),
                    "page": meta.get("page_number"),
                    "category": meta.get("category", ""),
                    "preview": meta["content"][:150],
                },
                "source": "faiss",
            })
            if len(faiss_matches) >= search.limit:
                break

    results.extend(faiss_matches)
    return {"results": results, "total": len(results)}

@router.post("/search/semantic")
async def semantic_search(request: Request, search: GraphSearchRequest):
    """Semantic vector search over FAISS index."""
    faiss_service: FAISSService = request.app.state.faiss
    results = await faiss_service.search(query=search.query, top_k=search.limit)
    return {
        "results": [
            {
                "chunk_id": r["chunk_id"],
                "document_id": r["document_id"],
                "filename": r.get("filename", ""),
                "page_number": r.get("page_number"),
                "category": r.get("category", ""),
                "content": r["content"][:300],
                "score": round(r["score"], 4),
            }
            for r in results
        ],
        "total": len(results),
    }

@router.get("/equipment/{tag}")
async def get_equipment(request: Request, tag: str):
    """Get full context for a piece of equipment from the knowledge graph."""
    neo4j: Neo4jClient = request.app.state.neo4j
    context = await neo4j.get_equipment_context(tag.upper())
    if not context:
        raise HTTPException(status_code=404, detail=f"Equipment {tag} not found")
    return context

@router.get("/neighbors/{node_type}/{key}/{value}")
async def get_neighbors(
    request: Request, node_type: str, key: str, value: str, depth: int = 2
):
    """Get neighboring nodes in the knowledge graph."""
    neo4j: Neo4jClient = request.app.state.neo4j
    neighbors = await neo4j.get_neighbors(node_type, key, value, depth)
    return {"node": {"type": node_type, key: value}, "neighbors": neighbors}

@router.get("/stats")
async def graph_stats(request: Request):
    """Get knowledge graph and vector index statistics."""
    neo4j: Neo4jClient = request.app.state.neo4j
    faiss_service: FAISSService = request.app.state.faiss

    # FAISS stats (always available)
    all_meta = faiss_service.get_all_metadata()
    total_chunks = len(all_meta)
    unique_docs = len(set(m["document_id"] for m in all_meta)) if all_meta else 0
    unique_files = len(set(m.get("filename", "") for m in all_meta if m.get("filename"))) if all_meta else 0

    # Category breakdown
    categories = {}
    for m in all_meta:
        cat = m.get("category", "unknown")
        categories[cat] = categories.get(cat, 0) + 1

    # Document list
    docs_map = {}
    for m in all_meta:
        doc_id = m["document_id"]
        if doc_id not in docs_map:
            docs_map[doc_id] = {
                "document_id": doc_id,
                "filename": m.get("filename", ""),
                "category": m.get("category", ""),
                "chunks": 0,
                "pages": set(),
            }
        docs_map[doc_id]["chunks"] += 1
        if m.get("page_number"):
            docs_map[doc_id]["pages"].add(m["page_number"])

    documents = [
        {**d, "pages": len(d["pages"]), "page_list": sorted(d["pages"])}
        for d in docs_map.values()
    ]

    # Neo4j stats (may be empty if not connected)
    neo4j_nodes = 0
    neo4j_rels = 0
    neo4j_connected = False
    node_types = []

    try:
        nodes = await neo4j.execute_query("MATCH (n) RETURN count(n) as count")
        rels = await neo4j.execute_query("MATCH ()-[r]->() RETURN count(r) as count")
        if nodes:
            neo4j_nodes = nodes[0]["count"]
            neo4j_connected = True
        if rels:
            neo4j_rels = rels[0]["count"]

        # Get node type breakdown
        types_result = await neo4j.execute_query(
            "MATCH (n) RETURN labels(n)[0] as label, count(n) as count ORDER BY count DESC"
        )
        node_types = [{"label": r["label"], "count": r["count"]} for r in types_result] if types_result else []
    except Exception:
        pass

    return {
        "neo4j_connected": neo4j_connected,
        "total_nodes": neo4j_nodes,
        "total_relationships": neo4j_rels,
        "node_types": node_types,
        "faiss_total_chunks": total_chunks,
        "faiss_total_documents": unique_docs,
        "faiss_total_files": unique_files,
        "faiss_dimension": faiss_service.index.d if faiss_service.index else 0,
        "categories": categories,
        "documents": documents,
    }