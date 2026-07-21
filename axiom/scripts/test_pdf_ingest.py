"""Quick test: create a PDF and ingest it via the API."""
import httpx
import json
import fitz

# Create a test PDF
doc = fitz.open()
page = doc.new_page()
text = """WORK ORDER: WO-200001
Equipment: P-101A (Boiler Feed Water Pump A)
Type: Corrective Maintenance
Priority: High
Date Raised: 15-Mar-2024
Assigned To: Rajesh Kumar

Description:
Pump P-101A tripped on high vibration alarm. Vibration readings showed 12.5 mm/s
on drive end bearing (alarm at 11.2 mm/s as per ISO-10816).

Findings:
Drive end bearing found with severe pitting. Root cause identified as contaminated
lubrication oil per OISD-163 guidelines. Replaced bearing and realigned per API-610.

Corrective Actions:
1. Replaced bearing SKF 6310-2RS
2. Flushed lubrication system
3. Realignment performed within 0.05 mm spec

Reference: Similar failure on P-101B (WO-098876). Review per OISD-163.
Verified By: Suresh Patel (Maintenance Supervisor)
"""
page.insert_text((72, 72), text, fontsize=11)
doc.save("data/test_workorder.pdf")
doc.close()
print("Test PDF created: data/test_workorder.pdf")

# Ingest via API
with open("data/test_workorder.pdf", "rb") as f:
    r = httpx.post(
        "<http://localhost:8000/api/v1/ingest/document>",
        files={"file": ("test_workorder.pdf", f, "application/pdf")},
        timeout=30,
    )

d = r.json()
print(f"\nStatus: {d.get('status', d.get('detail', 'unknown'))}")
print(f"Category: {d.get('category')}")
print(f"Pages: {d.get('total_pages')}")
print(f"Entities: {d.get('entities_extracted')}")
print(f"Relationships: {d.get('relationships_found')}")
print(f"Chunks: {d.get('chunks_created')}")

if d.get("entities"):
    print("\nExtracted Entities:")
    for e in d["entities"]:
        print(f"  [{e['type']:20s}] {e['value']:30s} ({e['confidence']:.0%})")

if d.get("relationships"):
    print(f"\nRelationships ({len(d['relationships'])}):")
    for r in d["relationships"][:5]:
        print(f"  {r['source']} -[{r['relation']}]-> {r['target']}")