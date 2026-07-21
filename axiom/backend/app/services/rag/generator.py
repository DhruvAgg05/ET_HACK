"""
Answer Generator — takes retrieved context and generates a grounded,
cited answer using an LLM with strict citation enforcement.
Uses FREE local LLM (Ollama) by default, with OpenAI/Groq as optional API providers.
"""

import httpx
from dataclasses import dataclass
import structlog
import json

from app.config import settings
from app.services.rag.retriever import RetrievalResult
from app.models.schemas import QueryResponse, RetrievedContext

logger = structlog.get_logger()

SYSTEM_PROMPT = """You are AXIOM, an AI-powered Industrial Knowledge Intelligence assistant.
You help maintenance engineers, field technicians, and operations teams find answers
from their industrial document corpus (SOPs, work orders, inspection reports, P&IDs,
incident reports, and regulatory documents).

CRITICAL RULES:
1. ONLY answer based on the provided context. If the context doesn't contain enough
   information, say "I don't have sufficient information to answer this confidently."
2. ALWAYS cite your sources using [Source N] notation where N corresponds to the
   context chunk number.
3. If you see conflicting information across sources, note the discrepancy.
4. For safety-critical information (procedures, limits, regulatory requirements),
   be explicit about your confidence level.
5. When mentioning equipment tags, parameters, or standards, preserve exact values.
6. Suggest follow-up questions that might help the user get more specific information.

RESPONSE FORMAT:
- Lead with a direct, concise answer
- Support with details and citations
- End with confidence assessment and suggested follow-ups
"""

class AnswerGenerator:
    """Generates grounded, cited answers from retrieved context.
    Uses Ollama (FREE local) by default, OpenAI/Groq as optional API providers."""

    def __init__(self):
        self.provider = settings.llm_provider  # "ollama" or "openai"

    async def generate(
        self,
        query: str,
        retrieved_chunks: list[RetrievalResult],
        graph_context: dict | None = None,
    ) -> QueryResponse:
        """Generate an answer from retrieved context."""

        # Nothing cleared the relevance floor and there's no graph context either —
        # answer honestly instead of sending the LLM an empty context and hoping
        # it follows the "say you don't know" instruction in the system prompt.
        if not retrieved_chunks and not graph_context:
            return QueryResponse(
                answer="I don't have sufficient information in the document corpus to answer this confidently. "
                       "No sufficiently relevant sources were found for this question.",
                confidence="low",
                sources=[],
                related_entities=[],
                suggested_followups=[],
            )

        # Build context string with numbered sources
        context_parts = []
        sources = []

        for i, chunk in enumerate(retrieved_chunks, 1):
            source_label = f"[Source {i}]"
            context_parts.append(
                f"{source_label}\n"
                f"Document: {chunk.filename}\n"
                f"Page: {chunk.page_number or 'N/A'}\n"
                f"Content: {chunk.content}\n"
                f"Retrieval Method: {chunk.source_type}\n"
            )
            sources.append(RetrievedContext(
                chunk_id=chunk.chunk_id,
                document_id=chunk.document_id,
                filename=chunk.filename,
                content=chunk.content,
                page_number=chunk.page_number,
                relevance_score=chunk.score,
                source_type=chunk.source_type,
            ))

        # Add graph context if available
        if graph_context:
            context_parts.append(
                f"\n[Knowledge Graph Context]\n{json.dumps(graph_context, indent=2, default=str)}"
            )

        full_context = "\n---\n".join(context_parts)

        # Generate answer
        if self.provider == "openrouter" and settings.openrouter_api_key:
            answer, confidence = await self._openrouter_generate(query, full_context)
        elif self.provider == "ollama":
            answer, confidence = await self._ollama_generate(query, full_context)
        elif self.provider == "openai" and settings.openai_api_key:
            answer, confidence = await self._openai_generate(query, full_context)
        elif self.provider == "groq" and settings.groq_api_key:
            answer, confidence = await self._groq_generate(query, full_context)
        elif self.provider == "openrouter" and not settings.openrouter_api_key:
            answer = "OPENROUTER_API_KEY is not set. Add your OpenRouter API key to .env and restart the backend."
            confidence = "low"
        else:
            # Fallback: return context summary without LLM
            answer = self._fallback_answer(query, retrieved_chunks)
            confidence = "low"

        # Generate follow-up suggestions
        followups = self._generate_followups(query, retrieved_chunks)

        # Extract related entities from context
        related_entities = self._extract_related_entities(retrieved_chunks)

        return QueryResponse(
            answer=answer,
            confidence=confidence,
            sources=sources,
            related_entities=related_entities,
            suggested_followups=followups,
        )

    async def _ollama_generate(self, query: str, context: str) -> tuple[str, str]:
        """Generate answer using Ollama (FREE local LLM)."""
        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                response = await client.post(
                    f"{settings.ollama_base_url}/api/chat",
                    json={
                        "model": settings.ollama_chat_model,
                        "messages": [
                            {"role": "system", "content": SYSTEM_PROMPT},
                            {
                                "role": "user",
                                "content": f"Context:\n{context}\n\nQuestion: {query}",
                            },
                        ],
                        "stream": False,
                        "options": {
                            "temperature": 0.1,
                            "num_predict": 1500,
                        },
                    },
                )

                if response.status_code == 200:
                    result = response.json()
                    answer = result["message"]["content"]
                    confidence = self._assess_confidence(answer, context)
                    return answer, confidence
                else:
                    logger.error("Ollama request failed", status=response.status_code)
                    return self._fallback_answer(query, []), "low"

        except Exception as e:
            logger.error("Ollama generation failed", error=str(e))
            return f"LLM unavailable. Ensure Ollama is running: `ollama serve`\nError: {str(e)}", "low"

    async def _openai_generate(self, query: str, context: str) -> tuple[str, str]:
        """Generate answer using OpenAI (PAID fallback)."""
        try:
            from openai import AsyncOpenAI
            client = AsyncOpenAI(api_key=settings.openai_api_key)
            response = await client.chat.completions.create(
                model=settings.openai_chat_model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {
                        "role": "user",
                        "content": f"Context:\n{context}\n\nQuestion: {query}",
                    },
                ],
                temperature=0.1,
                max_tokens=1500,
            )

            answer = response.choices[0].message.content
            confidence = self._assess_confidence(answer, context)
            return answer, confidence

        except Exception as e:
            logger.error("OpenAI generation failed", error=str(e))
            return f"Error generating answer: {str(e)}", "low"

    def _fallback_answer(self, query: str, chunks: list[RetrievalResult]) -> str:
        """Generate a basic answer without LLM (fallback mode)."""
        if not chunks:
            return "No relevant documents found for your query."

        answer_parts = [
            f"Based on {len(chunks)} relevant document(s) found:\n"
        ]

        for i, chunk in enumerate(chunks[:3], 1):
            answer_parts.append(
                f"\n**[Source {i}]** From '{chunk.filename}'"
                f"{f' (Page {chunk.page_number})' if chunk.page_number else ''}:\n"
                f"{chunk.content[:300]}{'...' if len(chunk.content) > 300 else ''}\n"
            )

        answer_parts.append(
            "\n*Note: Running in fallback mode without LLM. "
            "Configure GROQ_API_KEY or OPENAI_API_KEY for full answer generation.*"
        )
        return "\n".join(answer_parts)

    async def _openrouter_generate(self, query: str, context: str) -> tuple[str, str]:
        """Generate answer using OpenRouter (OpenAI-compatible, routes to many models)."""
        try:
            from openai import AsyncOpenAI
            client = AsyncOpenAI(
                api_key=settings.openrouter_api_key,
                base_url=settings.openrouter_base_url,
            )
            response = await client.chat.completions.create(
                model=settings.openrouter_chat_model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {
                        "role": "user",
                        "content": f"Context:\n{context}\n\nQuestion: {query}",
                    },
                ],
                temperature=0.1,
                max_tokens=1500,
            )

            answer = response.choices[0].message.content
            confidence = self._assess_confidence(answer, context)
            return answer, confidence

        except Exception as e:
            logger.error("OpenRouter generation failed", error=str(e))
            return f"Error generating answer with OpenRouter: {str(e)}", "low"

    async def _groq_generate(self, query: str, context: str) -> tuple[str, str]:
        """Generate answer using Groq's OpenAI-compatible API."""
        try:
            from openai import AsyncOpenAI
            client = AsyncOpenAI(
                api_key=settings.groq_api_key,
                base_url=settings.groq_base_url,
            )
            response = await client.chat.completions.create(
                model=settings.groq_chat_model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {
                        "role": "user",
                        "content": f"Context:\n{context}\n\nQuestion: {query}",
                    },
                ],
                temperature=0.1,
                max_tokens=1500,
            )

            answer = response.choices[0].message.content
            confidence = self._assess_confidence(answer, context)
            return answer, confidence

        except Exception as e:
            logger.error("Groq generation failed", error=str(e))
            return f"Error generating answer with Groq: {str(e)}", "low"

    def _assess_confidence(self, answer: str, context: str) -> str:
        """Assess confidence level of the generated answer."""
        # High confidence: answer contains citations and context is rich
        citation_count = answer.count("[Source")
        if citation_count >= 2 and len(context) > 1000:
            return "high"
        elif citation_count >= 1:
            return "medium"
        else:
            return "low"

    def _generate_followups(
        self, query: str, chunks: list[RetrievalResult]
    ) -> list[str]:
        """Generate suggested follow-up questions."""
        followups = []

        # Extract equipment tags from results
        import re
        all_content = " ".join(c.content for c in chunks)
        equipment_tags = set(re.findall(r"\b[A-Z]{1,4}-\d{2,5}[A-Z]?\b", all_content))

        if equipment_tags:
            tag = list(equipment_tags)[0]
            followups.append(f"What is the maintenance history of {tag}?")
            followups.append(f"Are there any open work orders for {tag}?")

        # Generic follow-ups based on query type
        if "maintenance" in query.lower() or "repair" in query.lower():
            followups.append("What spare parts are needed?")
            followups.append("What is the recommended maintenance interval?")
        elif "inspection" in query.lower():
            followups.append("When is the next inspection due?")
            followups.append("What were the findings from the last inspection?")
        elif "procedure" in query.lower() or "sop" in query.lower():
            followups.append("What PPE is required for this procedure?")
            followups.append("What are the safety precautions?")

        return followups[:4]

    def _extract_related_entities(self, chunks: list[RetrievalResult]) -> list[dict]:
        """Extract entities mentioned across retrieved chunks."""
        import re
        entities = []
        seen = set()

        all_content = " ".join(c.content for c in chunks)

        # Equipment
        for tag in re.findall(r"\b[A-Z]{1,4}-\d{2,5}[A-Z]?\b", all_content):
            if tag not in seen:
                entities.append({"type": "equipment", "value": tag})
                seen.add(tag)

        # Regulations
        for reg in re.findall(r"\b(?:OISD|API|ISO)[-\s]?\d+\b", all_content):
            if reg not in seen:
                entities.append({"type": "regulation", "value": reg})
                seen.add(reg)

        return entities[:10]
