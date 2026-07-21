"""
Generate synthetic industrial documents for demo/testing.
Creates realistic work orders, inspection reports, SOPs, and incident reports.
"""

import json
import os
from pathlib import Path
from datetime import datetime, timedelta
import random

OUTPUT_DIR = Path("data/sample_documents")

def generate_work_orders(count: int = 20):
    """Generate synthetic maintenance work orders."""
    equipment_tags = [
        "P-101A", "P-101B", "P-201A", "C-301", "C-301B",
        "V-401", "V-402", "HX-501", "HX-502", "R-601",
        "FV-1001", "XV-1002", "PSV-3001", "TIT-4001", "FIC-2001",
    ]

    work_types = ["Corrective Maintenance", "Preventive Maintenance", "Predictive Maintenance"]
    priorities = ["Critical", "High", "Medium", "Low"]
    statuses = ["Completed", "In Progress", "Planned", "Overdue"]

    technicians = [
        "Rajesh Kumar", "Amit Sharma", "Suresh Patel", "Vikram Singh",
        "Anil Reddy", "Pradeep Joshi", "Manoj Verma", "Sanjay Gupta",
    ]

    failure_modes = [
        "Bearing failure due to inadequate lubrication",
        "Seal leakage - mechanical seal worn",
        "High vibration - misalignment detected",
        "Impeller erosion causing reduced flow",
        "Coupling damage - fatigue crack",
        "Motor overheating - winding insulation degradation",
        "Control valve sticking - stem packing worn",
        "Corrosion under insulation (CUI)",
        "Gasket failure at flange joint",
        "Instrument drift - requires recalibration",
    ]

    work_orders = []
    base_date = datetime(2022, 1, 1)

    for i in range(count):
        wo_date = base_date + timedelta(days=random.randint(0, 900))
        equipment = random.choice(equipment_tags)

        wo = {
            "work_order_id": f"WO-{100000 + i}",
            "equipment_tag": equipment,
            "work_type": random.choice(work_types),
            "priority": random.choice(priorities),
            "status": random.choice(statuses),
            "date_raised": wo_date.strftime("%d-%b-%Y"),
            "date_completed": (wo_date + timedelta(days=random.randint(1, 14))).strftime("%d-%b-%Y"),
            "assigned_to": random.choice(technicians),
            "description": random.choice(failure_modes),
            "findings": f"Inspection of {equipment} revealed {random.choice(failure_modes).lower()}. "
                       f"Equipment was isolated as per PTW-{random.randint(1000, 9999)}. "
                       f"Maintenance carried out as per SOP-MAINT-{random.randint(100, 999)}.",
            "parts_used": random.choice([
                "Bearing SKF 6205-2RS (qty: 2)",
                "Mechanical seal Type A (qty: 1)",
                "Gasket set DN150 PN40 (qty: 1)",
                "Coupling element (qty: 1)",
                "Packing rings (qty: 4)",
            ]),
            "man_hours": random.randint(2, 48),
            "applicable_standard": random.choice(["OISD-163", "API-610", "ISO-10816", "ASME B31.3"]),
        }
        work_orders.append(wo)

    return work_orders

def generate_inspection_reports(count: int = 10):
    """Generate synthetic inspection reports."""
    reports = []

    equipment_tags = ["V-401", "V-402", "P-101A", "HX-501", "R-601", "C-301"]
    inspection_types = [
        "Thickness Survey", "NDT Inspection", "Internal Inspection",
        "External Visual Inspection", "Pressure Test",
    ]
    inspectors = ["M. Krishnan", "S. Banerjee", "R. Iyer", "P. Nair"]

    for i in range(count):
        tag = random.choice(equipment_tags)
        insp_date = datetime(2023, 1, 1) + timedelta(days=random.randint(0, 500))

        report = {
            "report_id": f"IR-{2023000 + i}",
            "equipment_tag": tag,
            "inspection_type": random.choice(inspection_types),
            "date": insp_date.strftime("%d-%b-%Y"),
            "inspector": random.choice(inspectors),
            "next_inspection_due": (insp_date + timedelta(days=random.randint(180, 730))).strftime("%d-%b-%Y"),
            "findings": f"Thickness measurement at location TML-{random.randint(1,12)}: "
                       f"{random.uniform(4.0, 12.0):.1f} mm (minimum required: 6.0 mm per API-510). "
                       f"Corrosion rate: {random.uniform(0.05, 0.5):.2f} mm/year. "
                       f"{'No defects found. Fit for continued service.' if random.random() > 0.3 else 'Localized thinning detected. Recommend repair or monitoring at reduced interval.'}",
            "recommendation": random.choice([
                "Continue normal service. Next inspection as scheduled.",
                "Reduce inspection interval to 12 months.",
                "Weld repair required at location TML-5 before next turnaround.",
                "Install corrosion monitoring probe.",
                "Apply protective coating during next shutdown.",
            ]),
            "applicable_standards": ["API-510", "API-570", "OISD-128", "ASME PCC-2"],
            "compliance_status": random.choice(["Compliant", "Compliant with conditions", "Non-compliant - action required"]),
        }
        reports.append(report)

    return reports

def generate_incident_reports(count: int = 8):
    """Generate synthetic incident/near-miss reports."""
    reports = []

    for i in range(count):
        date = datetime(2022, 6, 1) + timedelta(days=random.randint(0, 700))

        scenarios = [
            {
                "title": "Pump Seal Failure - Hydrocarbon Release",
                "equipment": "P-101A",
                "severity": "High",
                "description": "Mechanical seal failure on pump P-101A resulted in minor hydrocarbon release. "
                             "Area gas detectors activated. Emergency isolation carried out within 3 minutes. "
                             "No injuries. Approximately 50 liters released to containment area.",
                "root_cause": "Seal operated beyond recommended life (18 months vs 12 months recommended). "
                            "PM schedule not updated after OEM bulletin OEM-2022-045.",
                "corrective_actions": [
                    "Replace seal with upgraded Type B seal as per OEM recommendation",
                    "Update PM schedule to 12-month seal replacement",
                    "Review all similar pumps for seal life compliance",
                    "Issue safety alert to all operating teams",
                ],
            },
            {
                "title": "Near Miss - Pressure Safety Valve Failure to Operate",
                "equipment": "PSV-3001",
                "severity": "Critical",
                "description": "During routine PSV testing, PSV-3001 on reactor R-601 failed to lift at set pressure. "
                             "Valve found stuck due to corrosion on seat. Discovered during planned test - no actual overpressure event.",
                "root_cause": "Process fluid causing accelerated corrosion on valve internals. "
                            "Testing interval of 24 months inadequate for this service.",
                "corrective_actions": [
                    "Replace PSV-3001 with corrosion-resistant trim material",
                    "Reduce testing interval to 12 months for all PSVs in similar service",
                    "Conduct immediate testing of all PSVs in corrosive service",
                    "Update risk assessment per OISD-154 requirements",
                ],
            },
            {
                "title": "Compressor Trip - High Discharge Temperature",
                "equipment": "C-301",
                "severity": "Medium",
                "description": "Compressor C-301 tripped on high discharge temperature alarm. "
                             "Temperature reached 185°C (alarm at 180°C, design limit 200°C). "
                             "Automatic shutdown functioned correctly. No equipment damage.",
                "root_cause": "Intercooler HX-301 fouled, reducing cooling capacity by 30%. "
                            "Fouling inspection was 4 months overdue.",
                "corrective_actions": [
                    "Clean intercooler HX-301",
                    "Establish fouling monitoring via pressure drop trending",
                    "Add cooling efficiency KPI to daily operator rounds",
                    "Review inspection scheduling compliance for all heat exchangers",
                ],
            },
        ]

        scenario = random.choice(scenarios)

        report = {
            "incident_id": f"INC-{2022000 + i}",
            "date": date.strftime("%d-%b-%Y"),
            "title": scenario["title"],
            "equipment_tag": scenario["equipment"],
            "severity": scenario["severity"],
            "area": f"Unit-{random.randint(1,5)}",
            "reported_by": random.choice(["Control Room Operator", "Field Technician", "Shift Supervisor"]),
            "description": scenario["description"],
            "root_cause_analysis": scenario["root_cause"],
            "corrective_actions": scenario["corrective_actions"],
            "lessons_learned": f"This incident highlights the importance of adhering to OEM maintenance recommendations "
                             f"and timely execution of inspection schedules. Reference: {random.choice(['OISD-154', 'OISD-163', 'API-580'])}.",
            "investigation_status": "Closed" if random.random() > 0.2 else "Open",
        }
        reports.append(report)

    return reports

def generate_sop():
    """Generate a sample SOP document."""
    return {
        "document_id": "SOP-OPS-101",
        "title": "Standard Operating Procedure: Hot Work Near Hydrocarbon Lines",
        "revision": "Rev 3",
        "effective_date": "01-Jan-2024",
        "approved_by": "Plant Manager - D.K. Mehta",
        "applicable_regulations": ["OISD-105", "Factory Act Section 38", "IS-3016"],
        "scope": "This procedure covers all hot work activities (welding, cutting, grinding) "
                "within 15 meters of equipment containing or previously containing hydrocarbons.",
        "steps": [
            {
                "step": 1,
                "action": "Obtain Hot Work Permit (PTW) from Control Room Supervisor",
                "responsible": "Maintenance Supervisor",
                "reference": "PTW Procedure SOP-SAFE-001",
            },
            {
                "step": 2,
                "action": "Confirm gas test shows <1% LEL in work area. Gas test valid for 4 hours maximum.",
                "responsible": "Safety Officer",
                "reference": "Gas Testing Procedure SOP-SAFE-012",
            },
            {
                "step": 3,
                "action": "Verify equipment isolation (Double Block and Bleed). Check isolation certificate.",
                "responsible": "Operations Engineer",
                "reference": "Isolation Procedure SOP-OPS-050",
            },
            {
                "step": 4,
                "action": "Position fire extinguisher and fire watch personnel. Minimum 2 DCP extinguishers (10 kg).",
                "responsible": "Fire & Safety",
                "reference": "OISD-105 Clause 6.3",
            },
            {
                "step": 5,
                "action": "Commence hot work. Continuous gas monitoring required. Stop work if LEL exceeds 10%.",
                "responsible": "Executing Technician",
                "reference": "OISD-105 Clause 7.1",
            },
        ],
        "ppe_required": [
            "Fire-retardant coveralls",
            "Welding helmet with appropriate shade",
            "Leather gloves",
            "Safety shoes with metatarsal guard",
            "Portable gas detector (4-gas)",
        ],
        "emergency_procedure": "In case of fire/gas leak: Stop work immediately -> Activate area alarm -> "
                              "Evacuate to Assembly Point B -> Call Emergency: Ext 999",
    }

def save_documents():
    """Generate and save all sample documents."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Work Orders
    work_orders = generate_work_orders(20)
    with open(OUTPUT_DIR / "work_orders.json", "w") as f:
        json.dump(work_orders, f, indent=2)
    print(f"Generated {len(work_orders)} work orders")

    # Inspection Reports
    inspections = generate_inspection_reports(10)
    with open(OUTPUT_DIR / "inspection_reports.json", "w") as f:
        json.dump(inspections, f, indent=2)
    print(f"Generated {len(inspections)} inspection reports")

    # Incident Reports
    incidents = generate_incident_reports(8)
    with open(OUTPUT_DIR / "incident_reports.json", "w") as f:
        json.dump(incidents, f, indent=2)
    print(f"Generated {len(incidents)} incident reports")

    # SOP
    sop = generate_sop()
    with open(OUTPUT_DIR / "sop_hot_work.json", "w") as f:
        json.dump(sop, f, indent=2)
    print("Generated SOP document")

    # Also create text versions for ingestion testing
    _create_text_versions(work_orders, inspections, incidents, sop)

    print(f"\nAll documents saved to {OUTPUT_DIR}")

def _create_text_versions(work_orders, inspections, incidents, sop):
    """Create plain text versions of documents for testing the ingestion pipeline."""

    # Work order as text
    with open(OUTPUT_DIR / "work_order_sample.txt", "w") as f:
        for wo in work_orders[:5]:
            f.write(f"WORK ORDER: {wo['work_order_id']}\n")
            f.write(f"Equipment: {wo['equipment_tag']}\n")
            f.write(f"Type: {wo['work_type']}\n")
            f.write(f"Priority: {wo['priority']}\n")
            f.write(f"Date: {wo['date_raised']}\n")
            f.write(f"Assigned To: {wo['assigned_to']}\n")
            f.write(f"Description: {wo['description']}\n")
            f.write(f"Findings: {wo['findings']}\n")
            f.write(f"Parts Used: {wo['parts_used']}\n")
            f.write(f"Man-Hours: {wo['man_hours']}\n")
            f.write(f"Standard: {wo['applicable_standard']}\n")
            f.write("\n" + "="*60 + "\n\n")

    # Incident report as text
    with open(OUTPUT_DIR / "incident_report_sample.txt", "w") as f:
        for inc in incidents[:3]:
            f.write(f"INCIDENT REPORT: {inc['incident_id']}\n")
            f.write(f"Date: {inc['date']}\n")
            f.write(f"Title: {inc['title']}\n")
            f.write(f"Equipment: {inc['equipment_tag']}\n")
            f.write(f"Severity: {inc['severity']}\n")
            f.write(f"\nDescription:\n{inc['description']}\n")
            f.write(f"\nRoot Cause Analysis:\n{inc['root_cause_analysis']}\n")
            f.write(f"\nCorrective Actions:\n")
            for action in inc['corrective_actions']:
                f.write(f"  - {action}\n")
            f.write(f"\nLessons Learned:\n{inc['lessons_learned']}\n")
            f.write("\n" + "="*60 + "\n\n")

    # SOP as text
    with open(OUTPUT_DIR / "sop_hot_work.txt", "w") as f:
        f.write(f"STANDARD OPERATING PROCEDURE\n")
        f.write(f"Document ID: {sop['document_id']}\n")
        f.write(f"Title: {sop['title']}\n")
        f.write(f"Revision: {sop['revision']}\n")
        f.write(f"Effective Date: {sop['effective_date']}\n")
        f.write(f"Approved By: {sop['approved_by']}\n")
        f.write(f"\nApplicable Regulations: {', '.join(sop['applicable_regulations'])}\n")
        f.write(f"\nScope:\n{sop['scope']}\n")
        f.write(f"\nPROCEDURE STEPS:\n")
        for step in sop['steps']:
            f.write(f"\n  Step {step['step']}: {step['action']}\n")
            f.write(f"    Responsible: {step['responsible']}\n")
            f.write(f"    Reference: {step['reference']}\n")
        f.write(f"\nPPE Required:\n")
        for ppe in sop['ppe_required']:
            f.write(f"  - {ppe}\n")
        f.write(f"\nEmergency Procedure:\n{sop['emergency_procedure']}\n")

if __name__ == "__main__":
    save_documents()