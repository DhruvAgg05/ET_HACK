"""Entity extraction service for industrial documents."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import logging
import re
from typing import Any
from uuid import UUID, uuid5, NAMESPACE_URL

from backend.app.config import Settings, get_settings
from backend.app.models.schemas import DocumentMetadata, EntityType, ExtractedEntity, ExtractedTextBlock, ExtractionMethod


logger = logging.getLogger(__name__)

try:
    import spacy
except ImportError:  # pragma: no cover - optional runtime dependency
    spacy = None

try:
    from gliner import GLiNER
except ImportError:  # pragma: no cover - optional runtime dependency
    GLiNER = None


@dataclass(slots=True)
class _MatchRecord:
    """Normalized match record before conversion into a Pydantic entity."""

    entity_type: EntityType
    text: str
    canonical_name: str
    normalized_value: str | None
    confidence: float
    page_number: int | None
    source_span_start: int | None
    source_span_end: int | None
    extraction_method: ExtractionMethod
    attributes: dict[str, Any]


class EntityExtractor:
    """Hybrid entity extractor using regex, spaCy, and optional GLiNER."""

    _EQUIPMENT_PATTERN = re.compile(r"\b[A-Z]{1,4}-\d{2,4}[A-Z]?\b")
    _WORK_ORDER_PATTERN = re.compile(r"\bWO[-\s]?\d{3,10}\b", re.IGNORECASE)
    _INCIDENT_PATTERN = re.compile(r"\bINC[-\s]?\d{2,10}\b", re.IGNORECASE)
    _PROCEDURE_PATTERN = re.compile(r"\bSOP[-\s]?\d{2,10}\b", re.IGNORECASE)
    _REGULATION_PATTERN = re.compile(r"\b(?:OISD|API|ASME|ISO)[-\s]?[A-Z0-9.]+\b", re.IGNORECASE)
    _PARAMETER_PATTERN = re.compile(
        r"\b(?P<value>-?\d+(?:\.\d+)?)\s?(?P<unit>bar|psi|kpa|mpa|deg c|°c|c|f|rpm|kw|v|a|m3/h|kg/h|%)\b",
        re.IGNORECASE,
    )
    _DATE_PATTERNS = (
        re.compile(r"\b\d{4}-\d{2}-\d{2}\b"),
        re.compile(r"\b\d{2}/\d{2}/\d{4}\b"),
        re.compile(r"\b\d{1,2}\s+[A-Z][a-z]{2,8}\s+\d{4}\b"),
    )

    def __init__(self, settings: Settings | None = None) -> None:
        """Initialize extractors and optional NLP models."""
        self._settings = settings or get_settings()
        self._logger = logger.getChild(self.__class__.__name__)
        self._spacy_model = self._load_spacy_model()
        self._gliner_model = self._load_gliner_model()

    def extract(self, text_blocks: list[ExtractedTextBlock], metadata: DocumentMetadata) -> list[ExtractedEntity]:
        """Extract entities from layout-aware text blocks."""
        matches: list[_MatchRecord] = []
        for block in text_blocks:
            matches.extend(self._extract_rule_based_entities(block, metadata))
            matches.extend(self._extract_spacy_entities(block))
            matches.extend(self._extract_gliner_entities(block))
        matches.append(
            _MatchRecord(
                entity_type=EntityType.DOCUMENT,
                text=metadata.title,
                canonical_name=metadata.title,
                normalized_value=str(metadata.document_id),
                confidence=1.0,
                page_number=1,
                source_span_start=None,
                source_span_end=None,
                extraction_method=ExtractionMethod.RULE_BASED,
                attributes={
                    "document_type": metadata.document_type.value,
                    "source_system": metadata.source_system.value,
                    "file_name": metadata.file_name,
                },
            )
        )
        return self._deduplicate(matches)

    def _extract_rule_based_entities(self, block: ExtractedTextBlock, metadata: DocumentMetadata) -> list[_MatchRecord]:
        """Extract deterministic industrial entities using regex patterns."""
        text = block.text
        matches: list[_MatchRecord] = []
        matches.extend(
            self._build_matches_from_pattern(
                self._EQUIPMENT_PATTERN,
                text,
                block.page_number,
                EntityType.EQUIPMENT,
                ExtractionMethod.RULE_BASED,
                confidence=0.92,
            )
        )
        matches.extend(
            self._build_matches_from_pattern(
                self._WORK_ORDER_PATTERN,
                text,
                block.page_number,
                EntityType.WORK_ORDER,
                ExtractionMethod.RULE_BASED,
                confidence=0.9,
            )
        )
        matches.extend(
            self._build_matches_from_pattern(
                self._INCIDENT_PATTERN,
                text,
                block.page_number,
                EntityType.INCIDENT,
                ExtractionMethod.RULE_BASED,
                confidence=0.9,
            )
        )
        matches.extend(
            self._build_matches_from_pattern(
                self._PROCEDURE_PATTERN,
                text,
                block.page_number,
                EntityType.PROCEDURE,
                ExtractionMethod.RULE_BASED,
                confidence=0.88,
            )
        )
        matches.extend(
            self._build_matches_from_pattern(
                self._REGULATION_PATTERN,
                text,
                block.page_number,
                EntityType.REGULATION,
                ExtractionMethod.RULE_BASED,
                confidence=0.9,
            )
        )
        for pattern in self._DATE_PATTERNS:
            matches.extend(
                self._build_matches_from_pattern(
                    pattern,
                    text,
                    block.page_number,
                    EntityType.DATE,
                    ExtractionMethod.RULE_BASED,
                    confidence=0.82,
                )
            )
        for match in self._PARAMETER_PATTERN.finditer(text):
            raw = match.group(0)
            value = match.group("value")
            unit = match.group("unit")
            matches.append(
                _MatchRecord(
                    entity_type=EntityType.PARAMETER,
                    text=raw,
                    canonical_name=raw.upper(),
                    normalized_value=value,
                    confidence=0.84,
                    page_number=block.page_number,
                    source_span_start=match.start(),
                    source_span_end=match.end(),
                    extraction_method=ExtractionMethod.RULE_BASED,
                    attributes={"unit": unit},
                )
            )
        if metadata.revision and metadata.revision in text:
            revision_start = text.find(metadata.revision)
            matches.append(
                _MatchRecord(
                    entity_type=EntityType.DOCUMENT,
                    text=metadata.revision,
                    canonical_name=metadata.revision,
                    normalized_value=metadata.revision,
                    confidence=0.8,
                    page_number=block.page_number,
                    source_span_start=revision_start,
                    source_span_end=revision_start + len(metadata.revision),
                    extraction_method=ExtractionMethod.RULE_BASED,
                    attributes={"kind": "revision"},
                )
            )
        return matches

    def _extract_spacy_entities(self, block: ExtractedTextBlock) -> list[_MatchRecord]:
        """Extract PERSON, ORG, and GPE entities from spaCy when available."""
        if self._spacy_model is None:
            return []
        doc = self._spacy_model(block.text)
        matches: list[_MatchRecord] = []
        for ent in doc.ents:
            entity_type = {
                "PERSON": EntityType.PERSONNEL,
                "ORG": EntityType.ORGANIZATION,
                "GPE": EntityType.LOCATION,
                "LOC": EntityType.LOCATION,
                "DATE": EntityType.DATE,
            }.get(ent.label_)
            if entity_type is None:
                continue
            matches.append(
                _MatchRecord(
                    entity_type=entity_type,
                    text=ent.text,
                    canonical_name=ent.text.strip(),
                    normalized_value=None,
                    confidence=0.72,
                    page_number=block.page_number,
                    source_span_start=ent.start_char,
                    source_span_end=ent.end_char,
                    extraction_method=ExtractionMethod.NER,
                    attributes={"provider": "spacy", "label": ent.label_},
                )
            )
        return matches

    def _extract_gliner_entities(self, block: ExtractedTextBlock) -> list[_MatchRecord]:
        """Extract entities from GLiNER when the model is available locally."""
        if self._gliner_model is None:
            return []
        labels = ["equipment", "personnel", "regulation", "location", "work order", "incident"]
        try:
            predictions = self._gliner_model.predict_entities(block.text, labels)
        except Exception:
            self._logger.warning("GLiNER prediction failed", extra={"page_number": block.page_number})
            return []
        matches: list[_MatchRecord] = []
        label_mapping = {
            "equipment": EntityType.EQUIPMENT,
            "personnel": EntityType.PERSONNEL,
            "regulation": EntityType.REGULATION,
            "location": EntityType.LOCATION,
            "work order": EntityType.WORK_ORDER,
            "incident": EntityType.INCIDENT,
        }
        for prediction in predictions:
            label = str(prediction["label"]).lower()
            entity_type = label_mapping.get(label)
            if entity_type is None:
                continue
            text = str(prediction["text"]).strip()
            if not text:
                continue
            matches.append(
                _MatchRecord(
                    entity_type=entity_type,
                    text=text,
                    canonical_name=text,
                    normalized_value=None,
                    confidence=max(0.0, min(1.0, float(prediction.get("score", 0.7)))),
                    page_number=block.page_number,
                    source_span_start=int(prediction.get("start", 0)),
                    source_span_end=int(prediction.get("end", 0)),
                    extraction_method=ExtractionMethod.NER,
                    attributes={"provider": "gliner"},
                )
            )
        return matches

    def _deduplicate(self, matches: list[_MatchRecord]) -> list[ExtractedEntity]:
        """Deduplicate matches while keeping the highest-confidence instance."""
        best_matches: dict[tuple[EntityType, str, int | None], _MatchRecord] = {}
        for match in matches:
            normalized_key = (match.entity_type, match.canonical_name.casefold(), match.page_number)
            current = best_matches.get(normalized_key)
            if current is None or match.confidence > current.confidence:
                best_matches[normalized_key] = match

        return [
            ExtractedEntity(
                entity_id=uuid5(NAMESPACE_URL, f"{item.entity_type.value}:{item.canonical_name}:{item.page_number}:{item.source_span_start}:{item.source_span_end}"),
                entity_type=item.entity_type,
                text=item.text,
                canonical_name=item.canonical_name,
                normalized_value=item.normalized_value,
                confidence=item.confidence,
                page_number=item.page_number,
                source_span_start=item.source_span_start,
                source_span_end=item.source_span_end,
                extraction_method=item.extraction_method,
                attributes=item.attributes,
            )
            for item in best_matches.values()
        ]

    def _build_matches_from_pattern(
        self,
        pattern: re.Pattern[str],
        text: str,
        page_number: int | None,
        entity_type: EntityType,
        extraction_method: ExtractionMethod,
        *,
        confidence: float,
    ) -> list[_MatchRecord]:
        """Build match records from a compiled regex pattern."""
        results: list[_MatchRecord] = []
        for match in pattern.finditer(text):
            matched_text = match.group(0).strip()
            if not matched_text:
                continue
            results.append(
                _MatchRecord(
                    entity_type=entity_type,
                    text=matched_text,
                    canonical_name=matched_text.upper(),
                    normalized_value=matched_text.upper(),
                    confidence=confidence,
                    page_number=page_number,
                    source_span_start=match.start(),
                    source_span_end=match.end(),
                    extraction_method=extraction_method,
                    attributes={},
                )
            )
        return results

    def _load_spacy_model(self) -> Any | None:
        """Load spaCy or a sentence-capable fallback pipeline."""
        if spacy is None:
            self._logger.warning("spaCy is not installed; regex extraction only will be used.")
            return None
        try:
            return spacy.load(self._settings.spacy_model)
        except Exception:
            self._logger.warning("Failed to load spaCy model; falling back to blank English pipeline.")
            fallback = spacy.blank("en")
            if "sentencizer" not in fallback.pipe_names:
                fallback.add_pipe("sentencizer")
            return fallback

    def _load_gliner_model(self) -> Any | None:
        """Load GLiNER when available; otherwise continue without it."""
        if GLiNER is None:
            return None
        try:
            return GLiNER.from_pretrained(self._settings.gliner_model)
        except Exception:
            self._logger.warning("Failed to load GLiNER model; continuing without GLiNER enrichment.")
            return None
