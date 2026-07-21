"""
Industrial Entity Extraction Engine.
Combines regex patterns (for structured tags) with spaCy NER and LLM-based extraction
for equipment tags, personnel, dates, parameters, and regulatory references.
"""

import re
from dataclasses import dataclass, field
from typing import Optional
import structlog

logger = structlog.get_logger()

@dataclass
class Entity:
    entity_type: str
    value: str
    confidence: float
    start: int = 0
    end: int = 0
    context: str = ""

class IndustrialEntityExtractor:
    """
    Multi-strategy entity extraction for industrial documents.

    Strategy 1: Regex patterns for well-structured tags (equipment IDs, parameters)
    Strategy 2: spaCy NER for people, organizations, dates
    Strategy 3: LLM extraction for complex/ambiguous entities
    """

    # Month abbreviations to exclude from equipment tag matching
    _MONTHS = {"JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"}
    # Common prefixes that are NOT equipment (standards, document refs)
    _NOT_EQUIPMENT = {"SOP", "WO", "MOC", "PTW", "NCR", "IR", "OR", "IS", "OEM"}

    # Industrial equipment tag patterns (ISA standard formats)
    EQUIPMENT_PATTERNS = [
        # Standard tag format: XX-NNNNA (e.g., P-101A, V-201B, C-301)
        r"\b([A-Z]{1,4})-(\d{2,5}[A-Z]?)\b",
        # Extended format: XX-NNNN-NNA (e.g., FV-1001-01A)
        r"\b([A-Z]{1,4})-(\d{3,5})-(\d{2}[A-Z]?)\b",
        # Instrument tags: XXX-NNNN (e.g., TIT-1001, FIC-2001, PSV-3001)
        r"\b([A-Z]{2,4})-(\d{4,5})\b",
        # Named equipment: "Pump 101A", "Compressor C-201"
        r"\b(Pump|Compressor|Valve|Reactor|Vessel|Tank|Heat Exchanger|Boiler|Turbine|Motor|Fan|Blower)\s+([A-Z]?-?\d{2,5}[A-Z]?)\b",
    ]

    # Process parameter patterns
    PARAMETER_PATTERNS = [
        # Temperature: 150°C, 300 deg F
        r"(\d+\.?\d*)\s*(?:°C|°F|deg\s*[CF]|celsius|fahrenheit)",
        # Pressure: 10.5 bar, 150 psi, 1.2 MPa
        r"(\d+\.?\d*)\s*(?:bar|psi|MPa|kPa|kg/cm2|atm)",
        # Flow: 100 m3/h, 500 GPM, 1000 kg/hr
        r"(\d+\.?\d*)\s*(?:m3/h|GPM|kg/hr|l/min|SCFM|Nm3/h)",
        # Vibration: 2.5 mm/s, 0.1 in/s
        r"(\d+\.?\d*)\s*(?:mm/s|in/s|mils|μm)",
    ]

    # Regulatory reference patterns
    REGULATION_PATTERNS = [
        # OISD standards
        r"\b(OISD[-\s]?\d{3})\b",
        # IS/BIS standards
        r"\b(IS[-:\s]?\d{3,5}(?:[-\s]?Part[-\s]?\d+)?)\b",
        # API standards
        r"\b(API[-\s]?\d{3,4}[A-Z]?)\b",
        # ASME codes
        r"\b(ASME[-\s]?[A-Z]+[-\s]?\d+(?:\.\d+)?)\b",
        # Factory Act reference
        r"\b(Factory Act|Factories Act)(?:\s*(?:Section|Sec\.?)\s*(\d+[A-Z]?))?",
        # PESO regulations
        r"\b(PESO|SMPV|Gas Cylinder Rules)\b",
        # ISO standards
        r"\b(ISO[-\s]?\d{4,5}(?:[-:]?\d+)?)\b",
    ]

    # Date patterns common in industrial documents
    DATE_PATTERNS = [
        r"\b(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})\b",
        r"\b(\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{2,4})\b",
        r"\b((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+\d{2,4})\b",
    ]

    # Work order / document reference patterns
    DOCUMENT_REF_PATTERNS = [
        r"\b(WO[-\s]?\d{5,10})\b",  # Work orders
        r"\b(MOC[-\s]?\d{4,8})\b",  # Management of Change
        r"\b(PTW[-\s]?\d{4,8})\b",  # Permit to Work
        r"\b(NCR[-\s]?\d{4,8})\b",  # Non-conformance report
        r"\b(IR[-\s]?\d{4,8})\b",   # Incident report
    ]

    def __init__(self):
        self._nlp = None

    @property
    def nlp(self):
        """Lazy-load spaCy model."""
        if self._nlp is None:
            try:
                import spacy
                try:
                    self._nlp = spacy.load("en_core_web_sm")
                except OSError:
                    self._nlp = spacy.blank("en")
            except ImportError:
                logger.warning("spaCy not installed, NER disabled")
                self._nlp = None
        return self._nlp

    def extract_all(self, text: str, page_number: Optional[int] = None) -> list[Entity]:
        """Run all extraction strategies and merge results."""
        entities = []

        # Strategy 1: Regex-based extraction (high precision for structured tags)
        entities.extend(self._extract_equipment_tags(text, page_number))
        entities.extend(self._extract_parameters(text, page_number))
        entities.extend(self._extract_regulations(text, page_number))
        entities.extend(self._extract_dates(text, page_number))
        entities.extend(self._extract_document_refs(text, page_number))

        # Strategy 2: spaCy NER (people, organizations, locations)
        entities.extend(self._extract_spacy_entities(text, page_number))

        # Deduplicate
        entities = self._deduplicate(entities)

        logger.info(
            "Entity extraction complete",
            total_entities=len(entities),
            page=page_number,
        )
        return entities

    def _extract_equipment_tags(self, text: str, page: Optional[int]) -> list[Entity]:
        """Extract industrial equipment tags, filtering out false positives."""
        entities = []
        for pattern in self.EQUIPMENT_PATTERNS:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                value = match.group(0).strip().upper()
                # Filter out date-like patterns (MAR-2024, OCT-2023)
                prefix = value.split("-")[0] if "-" in value else ""
                if prefix in self._MONTHS:
                    continue
                # Filter out known non-equipment prefixes
                if prefix in self._NOT_EQUIPMENT:
                    continue
                # Filter out regulation-like patterns (OISD-154, API-610, ISO-10816)
                if prefix in {"OISD", "API", "ISO", "ASME", "ASTM"}:
                    continue

                context = text[max(0, match.start() - 50):match.end() + 50]
                entities.append(Entity(
                    entity_type="equipment",
                    value=value,
                    confidence=0.9,
                    start=match.start(),
                    end=match.end(),
                    context=context,
                ))
        return entities

    def _extract_parameters(self, text: str, page: Optional[int]) -> list[Entity]:
        """Extract process parameters with units."""
        entities = []
        for pattern in self.PARAMETER_PATTERNS:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                value = match.group(0).strip()
                context = text[max(0, match.start() - 50):match.end() + 50]
                entities.append(Entity(
                    entity_type="parameter",
                    value=value,
                    confidence=0.85,
                    start=match.start(),
                    end=match.end(),
                    context=context,
                ))
        return entities

    def _extract_regulations(self, text: str, page: Optional[int]) -> list[Entity]:
        """Extract regulatory standard references."""
        entities = []
        for pattern in self.REGULATION_PATTERNS:
            for match in re.finditer(pattern, text):
                value = match.group(0).strip()
                context = text[max(0, match.start() - 50):match.end() + 50]
                entities.append(Entity(
                    entity_type="regulation",
                    value=value,
                    confidence=0.95,
                    start=match.start(),
                    end=match.end(),
                    context=context,
                ))
        return entities

    def _extract_dates(self, text: str, page: Optional[int]) -> list[Entity]:
        """Extract dates from the document."""
        entities = []
        for pattern in self.DATE_PATTERNS:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                value = match.group(1).strip()
                context = text[max(0, match.start() - 40):match.end() + 40]
                entities.append(Entity(
                    entity_type="date",
                    value=value,
                    confidence=0.85,
                    start=match.start(),
                    end=match.end(),
                    context=context,
                ))
        return entities

    def _extract_document_refs(self, text: str, page: Optional[int]) -> list[Entity]:
        """Extract document/work order references."""
        entities = []
        for pattern in self.DOCUMENT_REF_PATTERNS:
            for match in re.finditer(pattern, text):
                value = match.group(0).strip()
                context = text[max(0, match.start() - 40):match.end() + 40]
                entities.append(Entity(
                    entity_type="document_reference",
                    value=value,
                    confidence=0.9,
                    start=match.start(),
                    end=match.end(),
                    context=context,
                ))
        return entities

    def _extract_spacy_entities(self, text: str, page: Optional[int]) -> list[Entity]:
        """Extract named entities using spaCy (people, orgs, locations)."""
        entities = []
        if self.nlp is None:
            return entities
        # Limit text length to avoid spaCy memory issues
        truncated = text[:100000] if len(text) > 100000 else text
        doc = self.nlp(truncated)

        type_map = {
            "PERSON": "personnel",
            "ORG": "organization",
            "GPE": "location",
            "FAC": "facility",
            "DATE": "date",
        }

        for ent in doc.ents:
            if ent.label_ in type_map:
                entities.append(Entity(
                    entity_type=type_map[ent.label_],
                    value=ent.text,
                    confidence=0.75,
                    start=ent.start_char,
                    end=ent.end_char,
                    context=text[max(0, ent.start_char - 30):ent.end_char + 30],
                ))
        return entities

    def _deduplicate(self, entities: list[Entity]) -> list[Entity]:
        """Remove duplicate entities, keeping highest confidence."""
        seen = {}
        for entity in entities:
            key = (entity.entity_type, entity.value.lower())
            if key not in seen or entity.confidence > seen[key].confidence:
                seen[key] = entity
        return list(seen.values())