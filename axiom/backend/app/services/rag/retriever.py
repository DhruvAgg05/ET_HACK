"""
Hybrid Retriever — combines FAISS vector search, Neo4j knowledge graph traversal,
and keyword (BM25) search for comprehensive document retrieval.

Scoring: 0.6 * Semantic Similarity + 0.4 * Graph Relevance
"""

import re
from rank_bm25 import BM25Okapi
from dataclasses import dataclass
import structlog

from app.config import settings
from app.services.vectorstore.faiss_service import FAISSService
from app.services.knowledge_graph.neo4j_client import Neo4jClient

logger = structlog.get_logger()

@dataclass
class RetrievalResult:
    chunk_id: str
    document_id: str
    filename: str
    content: str
    page_number: int | None
    score: float
    source_type: str  # "vector", "graph", "keyword"

class HybridRetriever:
    """
    Multi-strategy retrieval engine (GraphRAG hybrid approach):

    1. Embedding → FAISS Top-k (semantic similarity)
    2. Extract query entities → Neo4j neighborhood expansion (graph relevance)
    3. Merge graph context + semantic chunks
    4. Re-rank using: Score = 0.6 * Semantic + 0.4 * Graph
    5. Return final ranked context

    Also supports BM25 keyword search for exact term matching.
    """

    def __init__(self, faiss_service: FAISSService, neo4j: Neo4jClient):
        self.faiss = faiss_service
        self.neo4j = neo4j
        self._bm25_corpus: list[dict] | None = None
        self._bm25_index: BM25Okapi | None = None
        self.semantic_weight = settings.semantic_weight  # 0.6
        self.graph_weight = settings.graph_weight  # 0.4

    async def retrieve(
        self,
        query: str,
        top_k: int = 5,
        use_vector: bool = True,
        use_graph: bool = True,
        use_keyword: bool = True,
        category_filter: str | None = None,
    ) -> list[RetrievalResult]:
        """
        Perform hybrid retrieval:
        1. FAISS semantic search → top-k candidates
        2. Extract entities from query → Neo4j neighborhood expansion
        3. Merge and re-rank using weighted scoring

        Score = 0.6 * semantic_similarity + 0.4 * graph_relevance
        """
        vector_results: list[RetrievalResult] = []
        graph_results: list[RetrievalResult] = []
        keyword_results: list[RetrievalResult] = []

        # 1. FAISS vector search (semantic similarity)
        if use_vector:
            vector_results = await self._vector_search(query, top_k * 2, category_filter)
            logger.debug("FAISS search", results=len(vector_results))

        # 2. Neo4j knowledge graph neighborhood expansion
        if use_graph:
            graph_results = await self._graph_search(query, top_k * 2)
            logger.debug("Graph search", results=len(graph_results))

        # 3. BM25 keyword search
        if use_keyword and self._bm25_index:
            keyword_results = self._keyword_search(query, top_k * 2)
            logger.debug("Keyword search", results=len(keyword_results))

        # Merge and re-rank with weighted scoring
        final_results = self._weighted_rerank(
            vector_results, graph_results, keyword_results, top_k
        )

        logger.info("Hybrid retrieval complete", total_results=len(final_results))
        return final_results

    def _weighted_rerank(
        self,
        vector_results: list[RetrievalResult],
        graph_results: list[RetrievalResult],
        keyword_results: list[RetrievalResult],
        top_k: int,
    ) -> list[RetrievalResult]:
        """
        Re-rank results using weighted scoring:
        Score = 0.6 * Semantic Similarity + 0.4 * Graph Relevance

        Keyword results boost the semantic score.
        """
        scores: dict[str, float] = {}
        result_map: dict[str, RetrievalResult] = {}

        # Normalize vector scores to [0, 1]
        max_vector_score = max((r.score for r in vector_results), default=1.0) or 1.0
        for result in vector_results:
            key = result.chunk_id
            normalized_score = result.score / max_vector_score
            scores[key] = self.semantic_weight * normalized_score
            result_map[key] = result

        # Normalize graph scores and add graph weight
        max_graph_score = max((r.score for r in graph_results), default=1.0) or 1.0
        for result in graph_results:
            key = result.chunk_id
            normalized_score = result.score / max_graph_score
            graph_contribution = self.graph_weight * normalized_score
            scores[key] = scores.get(key, 0) + graph_contribution
            if key not in result_map:
                result_map[key] = result

        # Keyword results add a boost (treated as part of semantic)
        if keyword_results:
            max_kw_score = max((r.score for r in keyword_results), default=1.0) or 1.0
            for result in keyword_results:
                key = result.chunk_id
                normalized_score = result.score / max_kw_score
                # Keyword contributes as a boost to semantic score
                keyword_boost = 0.1 * normalized_score
                scores[key] = scores.get(key, 0) + keyword_boost
                if key not in result_map:
                    result_map[key] = result

        # Sort by final weighted score
        sorted_keys = sorted(scores.keys(), key=lambda x: scores[x], reverse=True)

        # Build final results
        final_results = []
        for key in sorted_keys[:top_k]:
            result = result_map[key]
            result.score = scores[key]
            final_results.append(result)

        return final_results

    async def _vector_search(
        self, query: str, top_k: int, category_filter: str | None
    ) -> list[RetrievalResult]:
        """Semantic search via FAISS."""
        results = await self.faiss.search(
            query=query, top_k=top_k, category_filter=category_filter
        )
        return [
            RetrievalResult(
                chunk_id=r["chunk_id"],
                document_id=r["document_id"],
                filename=r["filename"],
                content=r["content"],
                page_number=r.get("page_number"),
                score=r["score"],
                source_type="vector",
            )
            for r in results
        ]

    async def _graph_search(self, query: str, top_k: int) -> list[RetrievalResult]:
        """
        Extract entities from query and traverse the knowledge graph
        to find related document chunks.
        """
        # Extract potential equipment tags from the query
        equipment_tags = re.findall(r"\b[A-Z]{1,4}-\d{2,5}[A-Z]?\b", query)
        regulation_refs = re.findall(r"\b(?:OISD|API|ISO|ASME)[-\s]?\d+\b", query)

        results = []

        # Search for equipment context
        for tag in equipment_tags:
            context = await self.neo4j.get_equipment_context(tag)
            if context:
                # Build a text representation of the graph context
                context_text = self._format_graph_context(tag, context)
                results.append(RetrievalResult(
                    chunk_id=f"graph_{tag}",
                    document_id="knowledge_graph",
                    filename="Knowledge Graph",
                    content=context_text,
                    page_number=None,
                    score=0.9,
                    source_type="graph",
                ))

        # Search for regulation context
        for ref in regulation_refs:
            neighbors = await self.neo4j.get_neighbors("Regulation", "standard_id", ref)
            if neighbors:
                context_text = f"Regulation {ref} applies to: "
                context_text += "; ".join(
                    f"{n['node_type']}: {n['properties']}" for n in neighbors[:5]
                )
                results.append(RetrievalResult(
                    chunk_id=f"graph_{ref}",
                    document_id="knowledge_graph",
                    filename="Knowledge Graph",
                    content=context_text,
                    page_number=None,
                    score=0.85,
                    source_type="graph",
                ))

        # General graph search
        search_terms = self._extract_search_terms(query)
        for term in search_terms[:3]:  # Limit to avoid too many queries
            nodes = await self.neo4j.search_nodes(term, limit=5)
            for node in nodes:
                props = node.get("props", {})
                results.append(RetrievalResult(
                    chunk_id=f"graph_{term}_{len(results)}",
                    document_id="knowledge_graph",
                    filename=props.get("filename", "Knowledge Graph"),
                    content=str(props),
                    page_number=None,
                    score=0.7,
                    source_type="graph",
                ))

        return results[:top_k]

    def _keyword_search(self, query: str, top_k: int) -> list[RetrievalResult]:
        """BM25 keyword search over indexed corpus."""
        if not self._bm25_index or not self._bm25_corpus:
            return []

        tokenized_query = query.lower().split()
        scores = self._bm25_index.get_scores(tokenized_query)

        # Get top results
        top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]

        results = []
        for idx in top_indices:
            if scores[idx] > 0:
                doc = self._bm25_corpus[idx]
                results.append(RetrievalResult(
                    chunk_id=doc.get("chunk_id", f"bm25_{idx}"),
                    document_id=doc.get("document_id", ""),
                    filename=doc.get("filename", ""),
                    content=doc.get("content", ""),
                    page_number=doc.get("page_number"),
                    score=float(scores[idx]),
                    source_type="keyword",
                ))

        return results

    def update_bm25_index(self, documents: list[dict]):
        """Update the BM25 index with new documents."""
        self._bm25_corpus = documents
        tokenized_corpus = [doc["content"].lower().split() for doc in documents]
        if tokenized_corpus:
            self._bm25_index = BM25Okapi(tokenized_corpus)
            logger.info("BM25 index updated", documents=len(documents))

    def _reciprocal_rank_fusion(
        self, result_lists: list[list[RetrievalResult]], k: int = 60
    ) -> list[RetrievalResult]:
        """
        Fuse multiple ranked lists using Reciprocal Rank Fusion.
        RRF score = sum(1 / (k + rank_i)) for each list where the doc appears.
        """
        scores: dict[str, float] = {}
        result_map: dict[str, RetrievalResult] = {}

        for result_list in result_lists:
            for rank, result in enumerate(result_list):
                key = result.chunk_id
                rrf_score = 1.0 / (k + rank + 1)
                scores[key] = scores.get(key, 0) + rrf_score

                # Keep the result with highest individual score
                if key not in result_map or result.score > result_map[key].score:
                    result_map[key] = result

        # Sort by fused score
        sorted_keys = sorted(scores.keys(), key=lambda x: scores[x], reverse=True)

        # Update scores in results
        fused_results = []
        for key in sorted_keys:
            result = result_map[key]
            result.score = scores[key]
            fused_results.append(result)

        return fused_results

    def _format_graph_context(self, equipment_tag: str, context: dict) -> str:
        """Format knowledge graph context into readable text."""
        parts = [f"Equipment: {equipment_tag}"]

        equipment = context.get("equipment", {})
        if equipment:
            parts.append(f"Properties: {equipment}")

        work_orders = context.get("work_orders", [])
        if work_orders:
            parts.append(f"Work Orders ({len(work_orders)}): {work_orders[:3]}")

        incidents = context.get("incidents", [])
        if incidents:
            parts.append(f"Incidents ({len(incidents)}): {incidents[:3]}")

        regulations = context.get("regulations", [])
        if regulations:
            parts.append(f"Applicable Regulations: {regulations}")

        inspections = context.get("inspections", [])
        if inspections:
            parts.append(f"Inspections ({len(inspections)}): {inspections[:3]}")

        return "\n".join(parts)

    def _extract_search_terms(self, query: str) -> list[str]:
        """Extract meaningful search terms from a natural language query."""
        # Remove common stop words and extract key terms
        stop_words = {
            "what", "is", "the", "a", "an", "of", "for", "in", "on", "at",
            "to", "from", "by", "with", "how", "when", "where", "which",
            "show", "me", "tell", "find", "get", "list", "all", "any",
        }
        words = query.split()
        terms = [w for w in words if w.lower() not in stop_words and len(w) > 2]
        return terms