"""LLM-assisted extraction for ambiguous entities and relationships."""

from __future__ import annotations

import json
import logging
from typing import Any
from uuid import UUID, uuid5, NAMESPACE_URL

import httpx

from backend.app.config import LLMProvider, Settings, get_settings
from backend.app.models.schemas import (
    DocumentMetadata,
    EntityType,
    ExtractedEntity,
    ExtractedRelationship,
    ExtractionMethod,
    IngestionIssue,
    RelationshipType,
    SeverityLevel,
)


logger = logging.getLogger(__name__)


class LLMExtractor:
    """Provider-backed second-pass extractor for ambiguous content."""

    def __init__(self, settings: Settings | None = None) -> None:
        """Initialize the extractor with application settings."""
        self._settings = settings or get_settings()
        self._logger = logger.getChild(self.__class__.__name__)

    async def extract(
        self,
        metadata: DocumentMetadata,
        text: str,
        existing_entities: list[ExtractedEntity],
    ) -> tuple[list[ExtractedEntity], list[ExtractedRelationship], list[IngestionIssue]]:
        """Extract additional entities and relationships using the configured LLM."""
        if not text.strip():
            return [], [], []

        prompt = self._build_prompt(metadata, text, existing_entities)
        try:
            response_payload = await self._request_structured_extraction(prompt)
        except Exception as exc:
            self._logger.warning("LLM extraction failed", extra={"error": str(exc)})
            return [], [], [
                IngestionIssue(
                    code="llm.extraction_failed",
                    message=f"LLM-assisted extraction failed: {exc}",
                    severity=SeverityLevel.WARNING,
                )
            ]

        entities = self._parse_entities(response_payload.get("entities", []))
        relationships = self._parse_relationships(response_payload.get("relationships", []), entities, existing_entities)
        return entities, relationships, []

    async def _request_structured_extraction(self, prompt: str) -> dict[str, Any]:
        """Request JSON extraction output from the active LLM provider."""
        timeout = self._settings.active_llm_timeout_seconds
        async with httpx.AsyncClient(timeout=timeout) as client:
            if self._settings.llm_provider == LLMProvider.OLLAMA:
                response = await client.post(
                    f"{self._settings.ollama.base_url}/api/generate",
                    json={
                        "model": self._settings.ollama.model,
                        "prompt": prompt,
                        "format": "json",
                        "stream": False,
                        "options": {"temperature": 0.0},
                    },
                )
                response.raise_for_status()
                payload = response.json()
                return json.loads(payload["response"])

            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self._settings.openai.api_key.get_secret_value()}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": self._settings.openai.model,
                    "temperature": 0.0,
                    "response_format": {"type": "json_object"},
                    "messages": [
                        {"role": "system", "content": "Return valid JSON only."},
                        {"role": "user", "content": prompt},
                    ],
                },
            )
            response.raise_for_status()
            payload = response.json()
            content = payload["choices"][0]["message"]["content"]
            return json.loads(content)

    def _build_prompt(
        self,
        metadata: DocumentMetadata,
        text: str,
        existing_entities: list[ExtractedEntity],
    ) -> str:
        """Build a deterministic extraction prompt."""
        entity_hints = [
            {
                "text": entity.text,
                "entity_type": entity.entity_type.value,
                "canonical_name": entity.canonical_name,
            }
            for entity in existing_entities[:50]
        ]
        return (
            "You are extracting industrial knowledge graph entities and relationships.\n"
            "Return JSON with keys 'entities' and 'relationships'.\n"
            "Each entity must contain: text, entity_type, canonical_name, normalized_value, confidence, page_number, attributes.\n"
            "Each relationship must contain: source_text, target_text, relationship_type, confidence, evidence.\n"
            f"Document title: {metadata.title}\n"
            f"Document type: {metadata.document_type.value}\n"
            f"Known entities: {json.dumps(entity_hints, ensure_ascii=False)}\n"
            f"Document excerpt:\n{text[:12_000]}"
        )

    def _parse_entities(self, raw_entities: list[dict[str, Any]]) -> list[ExtractedEntity]:
        """Parse LLM entity output into validated schemas."""
        entities: list[ExtractedEntity] = []
        for raw in raw_entities:
            try:
                entity_type = EntityType(str(raw["entity_type"]))
                text = str(raw["text"]).strip()
                if not text:
                    continue
                entities.append(
                    ExtractedEntity(
                        entity_id=uuid5(NAMESPACE_URL, f"llm:{entity_type.value}:{text}:{raw.get('page_number')}"),
                        entity_type=entity_type,
                        text=text,
                        canonical_name=str(raw.get("canonical_name", text)).strip()[:255],
                        normalized_value=self._maybe_string(raw.get("normalized_value")),
                        confidence=max(0.0, min(1.0, float(raw.get("confidence", 0.65)))),
                        page_number=self._maybe_int(raw.get("page_number")),
                        source_span_start=None,
                        source_span_end=None,
                        extraction_method=ExtractionMethod.LLM,
                        attributes=raw.get("attributes", {}) if isinstance(raw.get("attributes", {}), dict) else {},
                    )
                )
            except Exception:
                self._logger.debug("Skipping invalid LLM entity payload", extra={"payload": raw})
        return entities

    def _parse_relationships(
        self,
        raw_relationships: list[dict[str, Any]],
        llm_entities: list[ExtractedEntity],
        existing_entities: list[ExtractedEntity],
    ) -> list[ExtractedRelationship]:
        """Parse LLM relationship output into validated schemas."""
        entity_lookup = {entity.text.casefold(): entity for entity in [*existing_entities, *llm_entities]}
        relationships: list[ExtractedRelationship] = []
        for raw in raw_relationships:
            try:
                source_text = str(raw["source_text"]).strip().casefold()
                target_text = str(raw["target_text"]).strip().casefold()
                source_entity = entity_lookup.get(source_text)
                target_entity = entity_lookup.get(target_text)
                if source_entity is None or target_entity is None or source_entity.entity_id == target_entity.entity_id:
                    continue
                relationship_type = RelationshipType(str(raw["relationship_type"]))
                evidence = str(raw["evidence"]).strip()[:2_000]
                if not evidence:
                    continue
                relationships.append(
                    ExtractedRelationship(
                        relationship_id=uuid5(
                            NAMESPACE_URL,
                            f"llm:{source_entity.entity_id}:{relationship_type.value}:{target_entity.entity_id}:{evidence[:100]}",
                        ),
                        relationship_type=relationship_type,
                        source_entity_id=source_entity.entity_id,
                        target_entity_id=target_entity.entity_id,
                        confidence=max(0.0, min(1.0, float(raw.get("confidence", 0.6)))),
                        evidence=evidence,
                        extraction_method=ExtractionMethod.LLM,
                    )
                )
            except Exception:
                self._logger.debug("Skipping invalid LLM relationship payload", extra={"payload": raw})
        return relationships

    @staticmethod
    def _maybe_int(value: Any) -> int | None:
        """Coerce an optional integer value."""
        if value in {None, ""}:
            return None
        return int(value)

    @staticmethod
    def _maybe_string(value: Any) -> str | None:
        """Coerce an optional string value."""
        if value in {None, ""}:
            return None
        return str(value)[:255]
