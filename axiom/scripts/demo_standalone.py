"""
Standalone demo of the AXIOM pipeline core logic.
Runs without ANY external dependencies — pure Python 3.11 stdlib.
Demonstrates: Entity Extraction, Document Classification, Chunking, Relationships.

Usage:
    python scripts/demo_standalone.py
"""

import re
import sys
from dataclasses import dataclass, field
from typing import Optional
from pathlib import Path

# ============================================================================
# ENTITY EXTRACTION (pure regex + pattern-based, no spaCy needed)
# ============================================================================

@dataclass
class Entity:
    entity_type: str
    value: str
    confidence: float
    context: str = ""

@dataclass
class Relation:
    source: str
    relation: str
    target: str
    confidence: float
    context: str = ""

class IndustrialEntityExtractor:
    """Multi-pattern industrial entity extraction — zero dependencies."""

    _MONTHS = {"JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"}
    _NOT_EQUIPMENT = {"SOP", "WO", "MOC", "PTW", "NCR", "IR", "OR", "IS", "OEM"}
    _STANDARDS = {"OISD", "API", "ISO", "ASME", "ASTM"}

    EQUIPMENT_PATTERNS = [
        r"\b([A-Z]{1,4})-(\d{2,5}[A-Z]?)\b",
        r"\b(Pump|Compressor|Valve|Reactor|Vessel|Tank|Heat Exchanger|Motor)\s+([A-Z]?-?\d{2,5}[A-Z]?)\b",
    ]

    PARAMETER_PATTERNS = [
        r"(\d+\.?\d*)\s*(?:mm/s|bar|psi|MPa|kPa|°C|°F|m3/h|GPM|kg/hr|μm)",
    ]

    REGULATION_PATTERNS = [
        r"\b(OISD[-\s]?\d{3})\b",
        r"\b(API[-\s]?\d{3,4}[A-Z]?)\b",
        r"\b(ISO[-\s]?\d{4,5})\b",
        r"\b(ASME[-\s]?[A-Z]+[-\s]?\d+)\b",
    ]

    DATE_PATTERNS = [
        r"\b(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})\b",
        r"\b(\d{1,2}\s*-\s*(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s*-?\s*\d{2,4})\b",
        r"\b(\d{1,2}\s*(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4})\b",
    ]

    DOCUMENT_REF_PATTERNS = [
        r"\b(WO[-\s]?\d{5,10})\b",
        r"\b(MOC[-\s]?\d{4,8})\b",
        r"\b(PTW[-\s]?\d{4,8})\b",
        r"\b(SOP[-\s]?\S{3,15})\b",
        r"\b(INC[-\s]?\d{4,8})\b",
    ]

    PERSONNEL_PATTERN = r"\b([A-Z][a-z]+(?:\s+[A-Z]\.?)?\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\b"

    def extract_all(self, text: str) -> list[Entity]:
        entities = []
        entities.extend(self._extract("equipment", self.EQUIPMENT_PATTERNS, text, 0.9))
        entities.extend(self._extract("parameter", self.PARAMETER_PATTERNS, text, 0.85))
        entities.extend(self._extract("regulation", self.REGULATION_PATTERNS, text, 0.95))
        entities.extend(self._extract("date", self.DATE_PATTERNS, text, 0.85))
        entities.extend(self._extract("document_reference", self.DOCUMENT_REF_PATTERNS, text, 0.9))
        entities.extend(self._extract_personnel(text))
        return self._deduplicate(entities)

    def _extract(self, entity_type: str, patterns: list, text: str, confidence: float) -> list[Entity]:
        entities = []
        for pattern in patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                value = match.group(0).strip()
                if entity_type == "equipment":
                    value = value.upper()
                    prefix = value.split("-")[0] if "-" in value else ""
                    # Filter false positives
                    if prefix in self._MONTHS or prefix in self._NOT_EQUIPMENT or prefix in self._STANDARDS:
                        continue
                context = text[max(0, match.start() - 40):match.end() + 40]
                entities.append(Entity(
                    entity_type=entity_type,
                    value=value,
                    confidence=confidence,
                    context=context,
                ))
        return entities

    def _extract_personnel(self, text: str) -> list[Entity]:
        entities = []
        # Look for names in typical assignment patterns
        patterns = [
            r"(?:Assigned To|Verified By|Reported By|Inspector|Lead|Approved By)[:\s]+([A-Z][a-z]+(?:\s+[A-Z]\.?)?\s+[A-Z][a-z]+)",
            r"([A-Z][a-z]+\s+[A-Z][a-z]+)\s+\((?:Maintenance|Plant|Safety|Operations)",
        ]
        for pattern in patterns:
            for match in re.finditer(pattern, text):
                entities.append(Entity(
                    entity_type="personnel",
                    value=match.group(1).strip(),
                    confidence=0.8,
                    context=text[max(0, match.start() - 20):match.end() + 20],
                ))
        return entities

    def _deduplicate(self, entities: list[Entity]) -> list[Entity]:
        seen = {}
        for e in entities:
            key = (e.entity_type, e.value.lower())
            if key not in seen or e.confidence > seen[key].confidence:
                seen[key] = e
        return list(seen.values())

# ============================================================================
# DOCUMENT CLASSIFICATION
# ============================================================================

class DocumentClassifier:
    SIGNALS = {
        "work_order": [
            (r"work\s+order|WO[-\s]?\d{4,}|maintenance\s+order", 3),
            (r"corrective\s+maintenance|preventive\s+maintenance|breakdown", 2),
            (r"spare\s+parts|man[-\s]?hours|downtime|repair|findings", 1),
        ],
        "sop": [
            (r"standard\s+operating\s+procedure|SOP|operating\s+instruction", 3),
            (r"step\s+\d+|precaution|PPE\s+required", 1),
            (r"procedure\s+no|rev(ision)?|approved\s+by", 2),
        ],
        "inspection_report": [
            (r"inspection\s+report|NDT|thickness\s+survey", 3),
            (r"corrosion|defect|finding|recommendation", 1),
            (r"fitness\s+for\s+service|remaining\s+life", 2),
        ],
        "incident_report": [
            (r"incident\s+report|near[-\s]?miss", 3),
            (r"root\s+cause\s+analysis|RCA|investigation", 2),
            (r"corrective\s+action|CAPA", 2),
        ],
        "regulatory": [
            (r"OISD|PESO|Factory\s+Act|BIS|statutory|compliance", 3),
            (r"regulation|standard|code\s+of\s+practice", 2),
        ],
    }

    def classify(self, text: str, filename: str = "") -> str:
        scores = {cat: 0 for cat in self.SIGNALS}
        sample = text[:5000]
        for category, patterns in self.SIGNALS.items():
            for pattern, weight in patterns:
                matches = len(re.findall(pattern, sample, re.IGNORECASE))
                scores[category] += matches * weight

        best = max(scores, key=scores.get)
        return best if scores[best] >= 2 else "general"

# ============================================================================
# TEXT CHUNKING
# ============================================================================

class TextChunker:
    def __init__(self, chunk_size: int = 400, overlap: int = 50):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk(self, text: str) -> list[str]:
        sentences = re.split(r"(?<=[.!?\n])\s+", text)
        chunks = []
        current = []
        current_len = 0

        for sent in sentences:
            if current_len + len(sent) > self.chunk_size and current:
                chunks.append(" ".join(current))
                # Keep overlap
                overlap_sents = []
                olen = 0
                for s in reversed(current):
                    if olen + len(s) <= self.overlap:
                        overlap_sents.insert(0, s)
                        olen += len(s)
                    else:
                        break
                current = overlap_sents
                current_len = olen

            current.append(sent)
            current_len += len(sent)

        if current:
            chunks.append(" ".join(current))
        return chunks

# ============================================================================
# RELATIONSHIP EXTRACTION
# ============================================================================

class RelationshipExtractor:
    PATTERNS = [
        (r"(\b[A-Z]{1,4}-\d{2,5}[A-Z]?\b).*?(?:failed|tripped).*?(?:due to|because of|caused by)\s+(.+?)(?:\.|$)", "FAILED_DUE_TO"),
        (r"(\b[A-Z]{1,4}-\d{2,5}[A-Z]?\b).*?(?:as per|per|reference)\s+((?:SOP|OISD|API|ISO)\S+)", "GOVERNED_BY"),
        (r"(\b[A-Z]{1,4}-\d{2,5}[A-Z]?\b).*?(?:protecting|on)\s+(?:reactor|vessel|tank)\s+(\b[A-Z]{1,4}-\d{2,5}\b)", "PROTECTS"),
    ]

    def extract(self, text: str, entities: list[Entity]) -> list[Relation]:
        relations = []

        # Pattern-based
        for pattern, rel_type in self.PATTERNS:
            for match in re.finditer(pattern, text, re.IGNORECASE | re.DOTALL):
                groups = match.groups()
                if len(groups) >= 2:
                    relations.append(Relation(
                        source=groups[0].strip().upper(),
                        relation=rel_type,
                        target=groups[1].strip()[:80],
                        confidence=0.8,
                        context=text[max(0, match.start()-20):match.end()+20],
                    ))

        # Co-occurrence: equipment + regulation in same sentence
        sentences = re.split(r"[.!?]\n", text)
        equip = {e.value for e in entities if e.entity_type == "equipment"}
        regs = {e.value for e in entities if e.entity_type == "regulation"}

        for sent in sentences:
            sent_equip = [e for e in equip if e in sent.upper()]
            sent_regs = [r for r in regs if r in sent]
            for eq in sent_equip:
                for reg in sent_regs:
                    relations.append(Relation(
                        source=eq, relation="GOVERNED_BY", target=reg,
                        confidence=0.65, context=sent[:100],
                    ))

        # Deduplicate
        seen = set()
        unique = []
        for r in relations:
            key = (r.source, r.relation, r.target)
            if key not in seen:
                seen.add(key)
                unique.append(r)
        return unique

# ============================================================================
# SAMPLE DOCUMENTS
# ============================================================================

SAMPLE_WORK_ORDER = """
WORK ORDER: WO-100234
Equipment: P-101A (Boiler Feed Water Pump A)
Type: Corrective Maintenance
Priority: High
Date Raised: 15-Mar-2024
Assigned To: Rajesh Kumar

Description:
Pump P-101A tripped on high vibration alarm at 08:45 hrs. Vibration readings showed
12.5 mm/s on drive end bearing (alarm at 11.2 mm/s, trip at 14.0 mm/s as per ISO-10816).
Pump was isolated and decontaminated as per SOP-OPS-050.

Findings:
Drive end bearing (SKF 6310-2RS) found with severe pitting on inner race. Root cause
identified as contaminated lubrication oil. Oil analysis report OR-2024-156 confirms
particulate contamination at 45 μm (limit: 25 μm per OEM manual).

Corrective Actions:
1. Replaced bearing SKF 6310-2RS (both ends as precaution)
2. Flushed lubrication system
3. Replaced lube oil with Shell Omala S4 GX 320
4. Realignment performed - readings within 0.05 mm (spec: 0.1 mm per API-610)
5. Post-maintenance vibration: 2.8 mm/s (acceptable)

Parts Used: Bearing SKF 6310-2RS (qty: 2), Mechanical seal (qty: 1), Lube oil 20L
Man-Hours: 16
Completed: 16-Mar-2024
Verified By: Suresh Patel (Maintenance Supervisor)

Reference: Similar failure occurred on P-101B in Aug-2023 (WO-098876).
Recommend reviewing lubrication PM frequency per OISD-163 guidelines.
"""

SAMPLE_INCIDENT = """
INCIDENT REPORT: INC-2024012
Date: 22-Apr-2024
Severity: High
Area: Unit-2 Hydrocracker

Title: Pressure Safety Valve PSV-3001 Failed to Lift During Routine Testing

Description:
During scheduled PSV testing as per OISD-154 requirements, PSV-3001 protecting
reactor R-601 failed to lift at set pressure of 45 bar. Valve required 52 bar
(115% of set pressure) to actuate. This exceeds the +/- 3% tolerance per API-520.

The valve had been in service for 18 months since last overhaul. Previous test
(Oct-2023) showed normal operation. No actual overpressure event occurred as this
was discovered during planned testing.

Root Cause Analysis:
- Primary cause: Corrosion product buildup on valve seat due to process fluid
  containing trace H2S (measured at 15 ppm, design basis was <5 ppm)
- Contributing factor: Change in feed composition since upstream unit modification
  (MOC-2023-445) not reflected in PSV testing frequency assessment
- Systemic factor: MOC procedure did not trigger downstream equipment review

Corrective Actions:
1. PSV-3001 replaced with upgraded trim material (Stellite 6 seat) - IMMEDIATE
2. All PSVs in H2S service to be tested within 30 days - WITHIN 1 MONTH
3. MOC procedure updated to include downstream impact assessment - WITHIN 2 WEEKS
4. Feed composition monitoring added to daily lab analysis - IMMEDIATE
5. Risk assessment update for reactor R-601 per API-580 - WITHIN 1 MONTH

Lessons Learned:
Process changes upstream can have delayed effects on downstream safety devices.
The MOC system must explicitly address secondary and tertiary impacts. This incident
is similar to the findings in CSB report 2019-003 on the importance of PSV management.

Investigation Lead: D.K. Mehta (Plant Manager)
Status: Open - Actions 2, 3, 5 pending
"""

SAMPLE_SOP = """
STANDARD OPERATING PROCEDURE
Document ID: SOP-OPS-101
Title: Hot Work Near Hydrocarbon Lines
Revision: Rev 3
Effective Date: 01-Jan-2024
Approved By: D.K. Mehta (Plant Manager)
Applicable Regulations: OISD-105, Factory Act Section 38, IS-3016

Scope:
This procedure covers all hot work activities (welding, cutting, grinding)
within 15 meters of equipment containing or previously containing hydrocarbons.

Step 1: Obtain Hot Work Permit (PTW) from Control Room Supervisor
  Responsible: Maintenance Supervisor
  Reference: SOP-SAFE-001

Step 2: Confirm gas test shows <1% LEL in work area. Test valid for 4 hours max.
  Responsible: Safety Officer
  Reference: SOP-SAFE-012

Step 3: Verify equipment isolation (Double Block and Bleed). Check certificate.
  Responsible: Operations Engineer
  Reference: SOP-OPS-050

Step 4: Position fire extinguisher and fire watch. Min 2 DCP extinguishers (10 kg).
  Responsible: Fire & Safety
  Reference: OISD-105 Clause 6.3

Step 5: Commence hot work. Continuous gas monitoring. Stop if LEL exceeds 10%.
  Responsible: Executing Technician
  Reference: OISD-105 Clause 7.1

PPE Required: Fire-retardant coveralls, Welding helmet, Leather gloves,
Safety shoes with metatarsal guard, Portable gas detector (4-gas)
"""

# ============================================================================
# MAIN DEMO
# ============================================================================

def run_demo():
    print("=" * 70)
    print("  AXIOM Industrial Knowledge Intelligence - Pipeline Demo")
    print("  (Standalone - no external dependencies required)")
    print("=" * 70)

    extractor = IndustrialEntityExtractor()
    classifier = DocumentClassifier()
    chunker = TextChunker(chunk_size=300, overlap=50)
    rel_extractor = RelationshipExtractor()

    documents = [
        ("Work Order WO-100234", SAMPLE_WORK_ORDER, "work_order_P101A.pdf"),
        ("Incident Report INC-2024012", SAMPLE_INCIDENT, "incident_PSV3001.pdf"),
        ("SOP Hot Work", SAMPLE_SOP, "sop_hot_work.pdf"),
    ]

    all_entities = {}
    all_relations = {}

    # ─── STEP 1: Process Each Document ───────────────────────────────────
    for doc_name, text, filename in documents:
        print(f"\n\n{'='*70}")
        print(f"  DOCUMENT: {doc_name}")
        print(f"{'='*70}")

        # Classification
        category = classifier.classify(text, filename)
        print(f"\n  [Classification] Category: {category}")

        # Entity Extraction
        entities = extractor.extract_all(text)
        all_entities[doc_name] = entities
        print(f"\n  [Entity Extraction] Found {len(entities)} entities:")

        by_type = {}
        for e in entities:
            by_type.setdefault(e.entity_type, []).append(e)

        for etype, elist in sorted(by_type.items()):
            print(f"    {etype:22s}: {', '.join(e.value for e in elist[:5])}")

        # Chunking
        chunks = chunker.chunk(text)
        print(f"\n  [Chunking] Split into {len(chunks)} chunks (300 chars each)")
        for i, chunk in enumerate(chunks[:2]):
            print(f"    Chunk {i}: \"{chunk[:70]}...\"")

        # Relationship Extraction
        relations = rel_extractor.extract(text, entities)
        all_relations[doc_name] = relations
        print(f"\n  [Relationships] Found {len(relations)} relationships:")
        for r in relations[:5]:
            print(f"    {r.source} -[{r.relation}]-> {r.target}")

    # ─── STEP 2: Cross-Document Intelligence ─────────────────────────────
    print(f"\n\n{'='*70}")
    print("  CROSS-DOCUMENT INTELLIGENCE")
    print(f"{'='*70}")

    # Find shared entities across documents
    doc_equipment = {}
    for doc_name, entities in all_entities.items():
        doc_equipment[doc_name] = {e.value for e in entities if e.entity_type == "equipment"}

    print("\n  Equipment entities per document:")
    for doc_name, equip_set in doc_equipment.items():
        print(f"    {doc_name}: {equip_set}")

    # Cross-document links
    all_equip = set()
    for s in doc_equipment.values():
        all_equip.update(s)

    print(f"\n  Total unique equipment across corpus: {len(all_equip)}")
    print(f"  Equipment tags: {sorted(all_equip)}")

    # Find equipment mentioned in multiple documents
    multi_doc_equip = []
    for tag in all_equip:
        docs_with_tag = [d for d, s in doc_equipment.items() if tag in s]
        if len(docs_with_tag) > 1:
            multi_doc_equip.append((tag, docs_with_tag))

    if multi_doc_equip:
        print(f"\n  Cross-document links found:")
        for tag, docs in multi_doc_equip:
            print(f"    {tag} appears in: {docs}")

    # ─── STEP 3: Knowledge Graph Preview ─────────────────────────────────
    print(f"\n\n{'='*70}")
    print("  KNOWLEDGE GRAPH (would be created in Neo4j)")
    print(f"{'='*70}")

    print("\n  Nodes:")
    node_count = 0
    for doc_name, entities in all_entities.items():
        for e in entities:
            if e.entity_type in ("equipment", "regulation", "personnel"):
                print(f"    (:{e.entity_type.title()} {{value: '{e.value}'}})")
                node_count += 1
                if node_count > 15:
                    print("    ... (truncated)")
                    break
        if node_count > 15:
            break

    print("\n  Relationships:")
    rel_count = 0
    for doc_name, relations in all_relations.items():
        for r in relations:
            print(f"    ({r.source})-[:{r.relation}]->({r.target})")
            rel_count += 1
            if rel_count > 10:
                print("    ... (truncated)")
                break
        if rel_count > 10:
            break

    # ─── STEP 4: Simulated RAG Query ─────────────────────────────────────
    print(f"\n\n{'='*70}")
    print("  SIMULATED RAG QUERY")
    print(f"{'='*70}")

    query = "What caused the failure of pump P-101A and what standards apply?"
    print(f"\n  User Query: \"{query}\"")

    # Simulate retrieval
    print("\n  --- Retrieval Results ---")
    print("  [1] VECTOR SEARCH (semantic match):")
    print("      -> Work Order WO-100234, relevance: 0.94")
    print("         \"Pump P-101A tripped on high vibration...bearing failure...\"")

    print("  [2] GRAPH TRAVERSAL (relationship-aware):")
    print("      -> P-101A -[GOVERNED_BY]-> ISO-10816")
    print("      -> P-101A -[GOVERNED_BY]-> API-610")
    print("      -> P-101A -[GOVERNED_BY]-> OISD-163")
    print("      -> P-101A -[HAS_WORK_ORDER]-> WO-100234")

    print("  [3] KEYWORD SEARCH (BM25 exact match):")
    print("      -> Match on 'P-101A' in Work Order, score: 12.4")
    print("      -> Match on 'P-101A' in Incident Report reference, score: 3.1")

    # Simulate answer generation
    print("\n  --- Generated Answer (with citations) ---")
    print("  " + "-" * 60)
    print("""  Pump P-101A failed due to a drive end bearing (SKF 6310-2RS)
  with severe pitting caused by contaminated lubrication oil
  [Source 1]. Oil analysis confirmed particulate contamination at
  45 microns, exceeding the 25 micron OEM limit [Source 1].

  The vibration reached 12.5 mm/s against an alarm setpoint of
  11.2 mm/s and trip at 14.0 mm/s [Source 1].

  Applicable Standards:
  - ISO-10816: Vibration severity limits [Source 2]
  - API-610: Pump alignment specification (0.1 mm) [Source 2]
  - OISD-163: Maintenance frequency guidelines [Source 2]

  Note: A similar failure occurred on P-101B in Aug-2023
  (WO-098876), suggesting a systemic lubrication issue [Source 1].

  Confidence: HIGH (multiple corroborating sources)

  Suggested follow-ups:
  - What is the lubrication PM schedule for P-101A and P-101B?
  - Has the oil contamination source been identified?
  - Are there other pumps with SKF 6310-2RS bearings to check?""")
    print("  " + "-" * 60)

    # ─── Summary ──────────────────────────────────────────────────────────
    print(f"\n\n{'='*70}")
    print("  PIPELINE SUMMARY")
    print(f"{'='*70}")
    total_entities = sum(len(e) for e in all_entities.values())
    total_relations = sum(len(r) for r in all_relations.values())
    print(f"""
  Documents processed:   3
  Total entities found:  {total_entities}
  Total relationships:   {total_relations}
  Unique equipment tags: {len(all_equip)}
  Cross-doc links:       {len(multi_doc_equip)}

  Pipeline Components:
    [x] Document Ingestion (PDF/DOCX/Image)
    [x] OCR Engine (Tesseract fallback for scanned pages)
    [x] Document Classification (regex pattern scoring)
    [x] Entity Extraction (equipment, parameters, regulations, personnel)
    [x] Relationship Extraction (pattern + co-occurrence)
    [x] Text Chunking (semantic boundary-aware)
    [x] Vector Store Indexing (Qdrant + OpenAI embeddings)
    [x] Knowledge Graph Population (Neo4j)
    [x] Hybrid Retrieval (Vector + Graph + BM25 fusion)
    [x] Answer Generation (LLM with citation enforcement)
    """)
    print("=" * 70)

if __name__ == "__main__":
    run_demo()