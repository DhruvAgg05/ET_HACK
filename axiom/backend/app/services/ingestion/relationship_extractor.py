"""
Relationship extraction - identifies connections between extracted entities
using pattern matching and co-occurrence analysis.
"""

import re
from dataclasses import dataclass
from typing import Optional

import structlog

logger = structlog.get_logger()


@dataclass
class ExtractedRelation:
    source: str
    relation: str
    target: str
    confidence: float
    context: str = ""


class RelationshipExtractor:
    """
    Extracts relationships between entities based on:
    1. Proximity co-occurrence
    2. Syntactic patterns
    3. Structural patterns
    """

    RELATION_PATTERNS = [
        (
            r"(\b[A-Z]{1,4}-\d{2,5}[A-Z]?\b).*?(?:failed|tripped|malfunctioned|broke down).*?(?:due to|because of|caused by)\s+(.+?)(?:\.|$)",
            "FAILED_DUE_TO",
        ),
        (
            r"(\b[A-Z]{1,4}-\d{2,5}[A-Z]?\b).*?(?:repaired|replaced|overhauled|serviced|maintained)",
            "MAINTAINED",
        ),
        (
            r"(\b[A-Z]{1,4}-\d{2,5}[A-Z]?\b).*?(?:inspected|surveyed|examined|tested)",
            "INSPECTED",
        ),
        (
            r"(?:as per|refer|according to|per)\s+(SOP|procedure|WI)[-\s]?(\S+)",
            "GOVERNED_BY",
        ),
        (
            r"(\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+\b).*?(?:performed|executed|carried out|completed).*?(\b[A-Z]{1,4}-\d{2,5}[A-Z]?\b)",
            "PERFORMED_ON",
        ),
        (
            r"(\b[A-Z]{1,4}-\d{2,5}[A-Z]?\b).*?(?:located at|installed in|at)\s+(.+?)(?:\.|,|$)",
            "LOCATED_AT",
        ),
    ]

    def extract(self, text: str, entities: list) -> list[ExtractedRelation]:
        """Extract relationships between entities in the text."""
        relations = []
        relations.extend(self._pattern_based_extraction(text))
        relations.extend(self._cooccurrence_extraction(text, entities))

        seen = set()
        unique_relations = []
        for relation in relations:
            key = (relation.source, relation.relation, relation.target)
            if key not in seen:
                seen.add(key)
                unique_relations.append(relation)

        logger.info("Relationships extracted", count=len(unique_relations))
        return unique_relations

    def _pattern_based_extraction(self, text: str) -> list[ExtractedRelation]:
        """Extract relationships using regex patterns."""
        relations = []

        for pattern, rel_type in self.RELATION_PATTERNS:
            for match in re.finditer(pattern, text, re.IGNORECASE | re.DOTALL):
                groups = match.groups()
                if len(groups) >= 2:
                    source = groups[0].strip()
                    target = groups[-1].strip()[:100]
                    context = text[max(0, match.start() - 30):match.end() + 30]

                    relations.append(
                        ExtractedRelation(
                            source=source,
                            relation=rel_type,
                            target=target,
                            confidence=0.8,
                            context=context,
                        )
                    )

        return relations

    def _cooccurrence_extraction(self, text: str, entities: list) -> list[ExtractedRelation]:
        """Find relationships based on entity co-occurrence in sentences."""
        relations = []
        sentences = re.split(r"[.!?]\s+", text)

        equipment_entities = [e for e in entities if e.entity_type == "equipment"]
        other_entities = [e for e in entities if e.entity_type != "equipment"]

        for sentence in sentences:
            equip_in_sentence = [
                e for e in equipment_entities if e.value.lower() in sentence.lower()
            ]
            others_in_sentence = [
                e for e in other_entities if e.value.lower() in sentence.lower()
            ]

            for equip in equip_in_sentence:
                for other in others_in_sentence:
                    rel_type = self._infer_relation_type(equip.entity_type, other.entity_type)
                    if rel_type:
                        relations.append(
                            ExtractedRelation(
                                source=equip.value,
                                relation=rel_type,
                                target=other.value,
                                confidence=0.6,
                                context=sentence[:150],
                            )
                        )

            if len(equip_in_sentence) > 1:
                for i, eq1 in enumerate(equip_in_sentence):
                    for eq2 in equip_in_sentence[i + 1:]:
                        relations.append(
                            ExtractedRelation(
                                source=eq1.value,
                                relation="CONNECTED_TO",
                                target=eq2.value,
                                confidence=0.5,
                                context=sentence[:150],
                            )
                        )

        return relations

    def _infer_relation_type(self, source_type: str, target_type: str) -> Optional[str]:
        """Infer relationship type from entity types."""
        type_map = {
            ("equipment", "personnel"): "ASSIGNED_TO",
            ("equipment", "regulation"): "GOVERNED_BY",
            ("equipment", "parameter"): "HAS_PARAMETER",
            ("equipment", "date"): "EVENT_DATE",
            ("equipment", "document_reference"): "REFERENCED_IN",
            ("equipment", "location"): "LOCATED_AT",
            ("equipment", "organization"): "OWNED_BY",
        }
        return type_map.get((source_type, target_type))
