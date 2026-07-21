"""
End-to-end demo script for the AXIOM pipeline.
Runs locally without Docker — tests ingestion, entity extraction, and retrieval.

Usage:
    python -m scripts.demo_pipeline
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from app.services.ingestion.entity_extractor import IndustrialEntityExtractor
from app.services.ingestion.chunker import TextChunker
from app.services.ingestion.document_classifier import DocumentClassifier

# Sample industrial text for testing without file upload
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

async def run_demo():
    """Run the full pipeline demo on sample text."""
    print("=" * 70)
    print("  AXIOM Industrial Knowledge Intelligence - Pipeline Demo")
    print("=" * 70)

    # --- 1. Entity Extraction ---
    print("\n\n📋 STEP 1: Entity Extraction")
    print("-" * 50)

    extractor = IndustrialEntityExtractor()

    print("\n→ Processing Work Order WO-100234...")
    wo_entities = extractor.extract_all(SAMPLE_WORK_ORDER)
    print(f"\n  Found {len(wo_entities)} entities:")
    for e in wo_entities:
        print(f"    [{e.entity_type:20s}] {e.value:30s} (confidence: {e.confidence:.2f})")

    print("\n→ Processing Incident Report INC-2024012...")
    inc_entities = extractor.extract_all(SAMPLE_INCIDENT)
    print(f"\n  Found {len(inc_entities)} entities:")
    for e in inc_entities:
        print(f"    [{e.entity_type:20s}] {e.value:30s} (confidence: {e.confidence:.2f})")

    # --- 2. Document Classification ---
    print("\n\n📂 STEP 2: Document Classification")
    print("-" * 50)

    classifier = DocumentClassifier()

    wo_category = classifier.classify(SAMPLE_WORK_ORDER, "work_order_P101A.pdf")
    print(f"  Work Order → Category: {wo_category.value}")

    inc_category = classifier.classify(SAMPLE_INCIDENT, "incident_report_PSV3001.pdf")
    print(f"  Incident Report → Category: {inc_category.value}")

    # --- 3. Text Chunking ---
    print("\n\n✂️  STEP 3: Text Chunking for Vector Storage")
    print("-" * 50)

    chunker = TextChunker(chunk_size=300, chunk_overlap=50)
    chunks = chunker.chunk_text(SAMPLE_WORK_ORDER, document_id="demo-wo-001", page_number=1)
    print(f"  Work Order split into {len(chunks)} chunks:")
    for chunk in chunks:
        print(f"    Chunk {chunk.chunk_index}: {chunk.content[:80]}...")

    # --- 4. Relationship Extraction ---
    print("\n\n🔗 STEP 4: Relationship Extraction")
    print("-" * 50)

    from app.services.ingestion.relationship_extractor import RelationshipExtractor
    rel_extractor = RelationshipExtractor()

    wo_relations = rel_extractor.extract(SAMPLE_WORK_ORDER, wo_entities)
    print(f"\n  Work Order Relationships ({len(wo_relations)}):")
    for r in wo_relations:
        print(f"    {r.source} -[{r.relation}]-> {r.target} (conf: {r.confidence:.2f})")

    inc_relations = rel_extractor.extract(SAMPLE_INCIDENT, inc_entities)
    print(f"\n  Incident Report Relationships ({len(inc_relations)}):")
    for r in inc_relations:
        print(f"    {r.source} -[{r.relation}]-> {r.target} (conf: {r.confidence:.2f})")

    # --- 5. Cross-Document Intelligence ---
    print("\n\n🧠 STEP 5: Cross-Document Intelligence")
    print("-" * 50)

    # Find common entities across documents
    wo_equipment = {e.value for e in wo_entities if e.entity_type == "equipment"}
    inc_equipment = {e.value for e in inc_entities if e.entity_type == "equipment"}
    common = wo_equipment & inc_equipment

    print(f"  Equipment mentioned in Work Order: {wo_equipment}")
    print(f"  Equipment mentioned in Incident: {inc_equipment}")
    print(f"  Common entities (cross-document links): {common}")

    # Demonstrate knowledge that would be in the graph
    print("\n  Knowledge Graph Connections (would be created):")
    print("    P-101A -[HAS_WORK_ORDER]-> WO-100234")
    print("    P-101A -[GOVERNED_BY]-> OISD-163")
    print("    P-101A -[GOVERNED_BY]-> ISO-10816")
    print("    P-101A -[GOVERNED_BY]-> API-610")
    print("    PSV-3001 -[INVOLVED_IN]-> INC-2024012")
    print("    PSV-3001 -[GOVERNED_BY]-> OISD-154")
    print("    PSV-3001 -[GOVERNED_BY]-> API-520")
    print("    R-601 -[PROTECTED_BY]-> PSV-3001")
    print("    MOC-2023-445 -[CAUSED]-> INC-2024012")

    # --- 6. Simulated Query ---
    print("\n\n❓ STEP 6: Simulated Query & Retrieval")
    print("-" * 50)

    query = "What maintenance has been done on pump P-101A and are there any related incidents?"
    print(f"\n  Query: \"{query}\"")
    print("\n  Retrieval would return:")
    print(f"    1. [Vector Match] Work Order WO-100234 (P-101A bearing replacement)")
    print(f"    2. [Graph Traverse] Equipment P-101A → connected to OISD-163, API-610")
    print(f"    3. [Keyword Match] Reference to P-101B similar failure (WO-098876)")
    print(f"    4. [Graph Traverse] Similar equipment P-101B → failure pattern match")

    print("\n  Generated Answer (with citations):")
    print("  " + "─" * 60)
    print("""  Pump P-101A underwent corrective maintenance on 15-Mar-2024 [Source 1].
  The pump tripped due to high vibration (12.5 mm/s) caused by bearing
  failure from contaminated lubrication oil [Source 1]. Both bearings were
  replaced and the lubrication system was flushed.

  A similar failure occurred on sister pump P-101B in August 2023
  (WO-098876), suggesting a systemic lubrication contamination issue
  across this pump type [Source 1, Source 3].

  Applicable standards: ISO-10816 (vibration limits), API-610 (alignment),
  OISD-163 (maintenance frequency) [Source 2].

  Confidence: HIGH

  Suggested follow-ups:
  • What is the lubrication PM schedule for P-101A and P-101B?
  • Are there other pumps with the same bearing type that should be checked?
  • Has the oil contamination source been identified?""")
    print("  " + "─" * 60)

    print("\n\n✅ Pipeline Demo Complete!")
    print("=" * 70)

if __name__ == "__main__":
    asyncio.run(run_demo())