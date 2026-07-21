"""
LLM-powered entity and relationship extraction for complex/ambiguous cases.
Uses FREE local LLM (Ollama) by default, with OpenAI/Groq as optional API providers.
"""

import httpx
import json
import structlog

from app.config import settings

logger = structlog.get_logger()

EXTRACTION_PROMPT = """You are an industrial document entity extraction system.
Extract structured entities and relationships from the following text.

Extract these entity types:
- equipment: Equipment tags, names, types (pumps, valves, compressors, etc.)
- personnel: People mentioned (operators, engineers, inspectors)
- parameter: Process parameters with values and units
- regulation: Standards, codes, regulatory references (OISD, API, ISO, BIS)
- date: Dates and time references
- location: Plant areas, units, buildings
- failure_mode: Equipment failure descriptions
- action: Maintenance/operational actions taken

Also extract relationships between entities in the format:
{source_entity} -[RELATIONSHIP_TYPE]-> {target_entity}

Common relationship types:
- FAILED_DUE_TO, MAINTAINED_BY, GOVERNED_BY, LOCATED_AT,
- PERFORMED_ON, CAUSED, REPLACED_WITH, CONNECTED_TO

Return as JSON with this structure:
{
  "entities": [
    {"type": "equipment", "value": "P-101A", "confidence": 0.95}
  ],
  "relationships": [
    {"source": "P-101A", "relation": "FAILED_DUE_TO", "target": "bearing wear", "confidence": 0.85}
  ]
}

ONLY extract entities that are clearly present in the text. Do not infer or hallucinate.
"""

class LLMEntityExtractor:
    """Uses an LLM for complex entity and relationship extraction."""

    def __init__(self):
        self.provider = settings.llm_provider

    async def extract(self, text: str) -> dict:
        """Extract entities and relationships using LLM."""
        text_chunk = text[:4000]

        if self.provider == "ollama":
            return await self._extract_ollama(text_chunk)
        elif self.provider == "openai" and settings.openai_api_key:
            return await self._extract_openai(text_chunk)
        elif self.provider == "groq" and settings.groq_api_key:
            return await self._extract_groq(text_chunk)
        else:
            return {"entities": [], "relationships": []}

    async def _extract_ollama(self, text: str) -> dict:
        """Extract using Ollama (FREE local)."""
        try:
            async with httpx.AsyncClient(timeout=90.0) as client:
                response = await client.post(
                    f"{settings.ollama_base_url}/api/chat",
                    json={
                        "model": settings.ollama_chat_model,
                        "messages": [
                            {"role": "system", "content": EXTRACTION_PROMPT},
                            {"role": "user", "content": f"Extract entities from:\n\n{text}"},
                        ],
                        "stream": False,
                        "format": "json",
                        "options": {"temperature": 0.0, "num_predict": 2000},
                    },
                )

                if response.status_code == 200:
                    content = response.json()["message"]["content"]
                    result = json.loads(content)
                    logger.info(
                        "LLM extraction complete (Ollama)",
                        entities=len(result.get("entities", [])),
                        relationships=len(result.get("relationships", [])),
                    )
                    return result
                else:
                    return {"entities": [], "relationships": []}

        except Exception as e:
            logger.error("Ollama extraction failed", error=str(e))
            return {"entities": [], "relationships": []}

    async def _extract_openai(self, text: str) -> dict:
        """Extract using OpenAI (PAID fallback)."""
        try:
            from openai import AsyncOpenAI
            client = AsyncOpenAI(api_key=settings.openai_api_key)
            response = await client.chat.completions.create(
                model=settings.openai_chat_model,
                messages=[
                    {"role": "system", "content": EXTRACTION_PROMPT},
                    {"role": "user", "content": f"Extract entities from:\n\n{text}"},
                ],
                temperature=0.0,
                response_format={"type": "json_object"},
                max_tokens=2000,
            )

            result = json.loads(response.choices[0].message.content)
            logger.info(
                "LLM extraction complete (OpenAI)",
                entities=len(result.get("entities", [])),
                relationships=len(result.get("relationships", [])),
            )
            return result

        except Exception as e:
            logger.error("OpenAI extraction failed", error=str(e))
            return {"entities": [], "relationships": []}

    async def _extract_groq(self, text: str) -> dict:
        """Extract using Groq's OpenAI-compatible API."""
        try:
            from openai import AsyncOpenAI
            client = AsyncOpenAI(
                api_key=settings.groq_api_key,
                base_url=settings.groq_base_url,
            )
            response = await client.chat.completions.create(
                model=settings.groq_chat_model,
                messages=[
                    {"role": "system", "content": EXTRACTION_PROMPT},
                    {"role": "user", "content": f"Extract entities from:\n\n{text}"},
                ],
                temperature=0.0,
                response_format={"type": "json_object"},
                max_tokens=2000,
            )

            result = json.loads(response.choices[0].message.content)
            logger.info(
                "LLM extraction complete (Groq)",
                entities=len(result.get("entities", [])),
                relationships=len(result.get("relationships", [])),
            )
            return result

        except Exception as e:
            logger.error("Groq extraction failed", error=str(e))
            return {"entities": [], "relationships": []}
