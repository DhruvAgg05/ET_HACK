"""Relationship extraction service for AXIOM."""

from __future__ import annotations

import logging
import re
from typing import Iterable
from uuid import UUID, uuid5, NAMESPACE_URL

from backend.app.models.schemas import EntityType, ExtractedEntity, ExtractedRelationship, ExtractedTextBlock, ExtractionMethod, RelationshipType


logger = logging.getLogger(__name__)


class RelationshipExtractor:
    """Pattern- and co-occurrence-based relationship extraction."""

    _SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+")
    _CAUSATION_PATTERN = re.compile(r"\b(failed due to|caused by|resulted from|triggered by)\b", re.IGNORECASE)

    def __init__(self) -> None:
        """Initialize the extractor."""
        self._logger = logger.getChild(self.__class__.__name__)

    def extract(
        self,
        entities: list[ExtractedEntity],
        text_blocks: list[ExtractedTextBlock],
    ) -> list[ExtractedRelationship]:
        """Extract relationships from entities co-occurring in the same sentence."""
        by_page: dict[int, list[ExtractedEntity]] = {}
        for entity in entities:
            if entity.page_number is None:
                continue
            by_page.setdefault(entity.page_number, []).append(entity)

        relationships: dict[tuple[UUID, UUID, RelationshipType], ExtractedRelationship] = {}
        for block in text_blocks:
            page_entities = by_page.get(block.page_number, [])
            if not page_entities:
                continue
            for sentence in self._sentence_segments(block.text):
                overlapping = [
                    entity
                    for entity in page_entities
                    if entity.text.lower() in sentence.lower()
                ]
                for relationship in self._relationships_for_sentence(sentence, overlapping):
                    key = (relationship.source_entity_id, relationship.target_entity_id, relationship.relationship_type)
                    existing = relationships.get(key)
                    if existing is None or relationship.confidence > existing.confidence:
                        relationships[key] = relationship
        return list(relationships.values())

    def _relationships_for_sentence(
        self,
        sentence: str,
        entities: list[ExtractedEntity],
    ) -> Iterable[ExtractedRelationship]:
        """Infer relationships for entities contained in a sentence."""
        equipment_entities = [item for item in entities if item.entity_type == EntityType.EQUIPMENT]
        regulation_entities = [item for item in entities if item.entity_type == EntityType.REGULATION]
        procedure_entities = [item for item in entities if item.entity_type == EntityType.PROCEDURE]
        work_order_entities = [item for item in entities if item.entity_type == EntityType.WORK_ORDER]
        incident_entities = [item for item in entities if item.entity_type == EntityType.INCIDENT]
        parameter_entities = [item for item in entities if item.entity_type == EntityType.PARAMETER]

        for equipment in equipment_entities:
            for regulation in regulation_entities:
                yield self._build_relationship(
                    equipment,
                    regulation,
                    RelationshipType.GOVERNED_BY,
                    sentence,
                    confidence=0.76,
                )
            for procedure in procedure_entities:
                yield self._build_relationship(
                    equipment,
                    procedure,
                    RelationshipType.HAS_PROCEDURE,
                    sentence,
                    confidence=0.78,
                )
            for work_order in work_order_entities:
                yield self._build_relationship(
                    equipment,
                    work_order,
                    RelationshipType.HAS_WORK_ORDER,
                    sentence,
                    confidence=0.82,
                )
            for incident in incident_entities:
                yield self._build_relationship(
                    equipment,
                    incident,
                    RelationshipType.INVOLVED_IN,
                    sentence,
                    confidence=0.8,
                )
            if self._CAUSATION_PATTERN.search(sentence):
                for parameter in parameter_entities:
                    yield self._build_relationship(
                        parameter,
                        equipment,
                        RelationshipType.CAUSED_BY,
                        sentence,
                        confidence=0.7,
                    )

        for work_order in work_order_entities:
            for document in (entity for entity in entities if entity.entity_type == EntityType.DOCUMENT):
                yield self._build_relationship(
                    work_order,
                    document,
                    RelationshipType.REFERENCES,
                    sentence,
                    confidence=0.75,
                )

    def _build_relationship(
        self,
        source: ExtractedEntity,
        target: ExtractedEntity,
        relationship_type: RelationshipType,
        evidence: str,
        *,
        confidence: float,
    ) -> ExtractedRelationship:
        """Construct a validated relationship object."""
        relationship_id = uuid5(
            NAMESPACE_URL,
            f"{source.entity_id}:{relationship_type.value}:{target.entity_id}:{evidence[:100]}",
        )
        return ExtractedRelationship(
            relationship_id=relationship_id,
            relationship_type=relationship_type,
            source_entity_id=source.entity_id,
            target_entity_id=target.entity_id,
            confidence=confidence,
            evidence=evidence[:2_000],
            extraction_method=ExtractionMethod.RULE_BASED,
        )

    def _sentence_segments(self, text: str) -> list[str]:
        """Split text into sentence-like segments."""
        return [segment.strip() for segment in self._SENTENCE_SPLIT.split(text) if segment.strip()]
