# AI for Industrial Knowledge Intelligence: Unified Asset & Operations Brain

## Executive Summary

**Product Name:** AXIOM — Asset & eXpert Intelligence for Operations & Maintenance

A unified AI platform that ingests heterogeneous industrial documents (P&IDs, work orders, inspection reports, SOPs, regulatory filings), constructs a living knowledge graph, and surfaces actionable intelligence through a conversational copilot — enabling field technicians, maintenance engineers, and compliance teams to find answers in seconds instead of hours.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        AXIOM PLATFORM ARCHITECTURE                       │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │                    PRESENTATION LAYER                              │  │
│  │  ┌──────────┐  ┌──────────────┐  ┌────────────┐  ┌───────────┐  │  │
│  │  │ Mobile   │  │ Web Dashboard│  │ Chat/Copilot│  │ API       │  │  │
│  │  │ (PWA)    │  │ (React)      │  │ Interface   │  │ Gateway   │  │  │
│  │  └──────────┘  └──────────────┘  └────────────┘  └───────────┘  │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│                                    │                                     │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │                    INTELLIGENCE LAYER                              │  │
│  │  ┌──────────────┐  ┌───────────────┐  ┌────────────────────────┐ │  │
│  │  │ RAG Engine   │  │ Agentic       │  │ Compliance & Quality   │ │  │
│  │  │ (Query +     │  │ Workflows     │  │ Monitor                │ │  │
│  │  │  Retrieval)  │  │ (LangGraph)   │  │                        │ │  │
│  │  └──────────────┘  └───────────────┘  └────────────────────────┘ │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│                                    │                                     │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │                    KNOWLEDGE LAYER                                 │  │
│  │  ┌──────────────┐  ┌───────────────┐  ┌────────────────────────┐ │  │
│  │  │ Knowledge    │  │ Vector Store  │  │ Temporal Event         │ │  │
│  │  │ Graph        │  │ (Embeddings)  │  │ Store                  │ │  │
│  │  │ (Neo4j)      │  │ (Qdrant)      │  │ (TimescaleDB)          │ │  │
│  │  └──────────────┘  └───────────────┘  └────────────────────────┘ │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│                                    │                                     │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │                    INGESTION LAYER                                 │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌─────────────────┐  │  │
│  │  │ PDF/Doc  │  │ P&ID/    │  │ OCR +    │  │ Email/          │  │  │
│  │  │ Parser   │  │ Drawing  │  │ Table    │  │ Attachment      │  │  │
│  │  │          │  │ Vision   │  │ Extract  │  │ Processor       │  │  │
│  │  └──────────┘  └──────────┘  └──────────┘  └─────────────────┘  │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Core Modules & Implementation Plan

### Module 1: Universal Document Ingestion Pipeline

**Goal:** Ingest any industrial document format and extract structured entities + relationships.

| Component | Technology | Purpose |
|-----------|-----------|---------|
| PDF/DOCX Parser | PyMuPDF + Unstructured.io | Text extraction with layout awareness |
| P&ID/Drawing Parser | YOLOv8 fine-tuned + GPT-4o Vision | Symbol detection, tag extraction, flow parsing |
| OCR Engine | Azure Document Intelligence / Tesseract + LayoutLM | Scanned documents, handwritten notes |
| Table Extractor | Camelot + LLM post-processing | Extract structured data from embedded tables |
| Entity Extractor | Fine-tuned NER (spaCy/GLiNER) + LLM | Equipment tags, process params, personnel, dates |
| Email Processor | Microsoft Graph API + attachment handler | Pull regulatory correspondence & attachments |

**Ingestion Flow:**
```
Document Upload → Format Detection → Preprocessing (deskew, denoise)
  → Layout Analysis → Text/Table/Image Extraction
  → Entity Recognition → Relationship Extraction
  → Knowledge Graph Insertion → Vector Embedding Generation
  → Indexing & Notification
```

**Key Innovation:** Multi-pass extraction — first pass uses traditional NLP for high-confidence entities, second pass uses LLM for ambiguous/contextual relationships, third pass uses cross-document co-reference resolution to link entities across documents.

---

### Module 2: Industrial Knowledge Graph

**Goal:** Build a living, queryable graph that connects equipment, procedures, people, events, and regulations.

**Ontology Design (Core Node Types):**
```
Equipment         → tag, type, location, criticality, OEM
Procedure         → type (SOP/WI/JSA), revision, status, approver
WorkOrder         → id, type (CM/PM/PdM), status, findings
Inspection        → type, date, findings, inspector, next_due
Incident          → id, severity, root_cause, corrective_actions
Regulation        → standard, clause, requirement, applicability
Personnel         → name, role, certifications, experience_domain
Parameter         → tag, unit, normal_range, alarm_limits
Document          → id, type, revision, source_system, upload_date
```

**Core Relationships:**
```
Equipment -[HAS_PROCEDURE]→ Procedure
Equipment -[HAS_WORK_ORDER]→ WorkOrder
Equipment -[INSPECTED_BY]→ Inspection
Equipment -[INVOLVED_IN]→ Incident
Equipment -[GOVERNED_BY]→ Regulation
Equipment -[MONITORS]→ Parameter
WorkOrder -[REFERENCES]→ Document
Incident -[CAUSED_BY]→ Equipment
Incident -[LED_TO]→ Procedure (new/revised)
Personnel -[PERFORMED]→ WorkOrder
Personnel -[AUTHORED]→ Document
```

**Technology:** Neo4j (graph store) + Qdrant (vector embeddings per chunk) + TimescaleDB (temporal events/parameters)

**Auto-Update Mechanism:** File watchers + webhook integrations trigger re-ingestion on new/modified documents. Delta processing updates only affected graph nodes/edges.

---

### Module 3: Expert Knowledge Copilot (RAG)

**Goal:** Conversational AI that answers operational questions with source citations and confidence.

**RAG Architecture:**
```
User Query → Intent Classification → Query Decomposition (if complex)
  → Hybrid Retrieval:
      ├─ Vector Search (semantic similarity via Qdrant)
      ├─ Graph Traversal (structured relationships via Neo4j)
      └─ Keyword Search (BM25 via Elasticsearch)
  → Re-ranking (cross-encoder)
  → Context Assembly (with source metadata)
  → LLM Generation (with citation enforcement)
  → Confidence Scoring + Source Links
  → Response Delivery (text + visual knowledge card)
```

**Key Features:**
- **Hybrid Retrieval:** Combines vector similarity, graph traversal, and keyword matching — industrial queries often need exact tag matches (keyword) + contextual understanding (vector) + relationship traversal (graph)
- **Citation Enforcement:** Every claim linked to source document, page, and paragraph
- **Confidence Scoring:** 3-tier confidence (High/Medium/Low) based on retrieval scores and source freshness
- **Follow-up Suggestions:** Proactively suggests related queries based on graph neighborhood
- **Multi-modal Responses:** Returns relevant drawings/diagrams alongside text answers
- **Mobile-First:** PWA with offline caching for field use, voice input support

**Example Queries the Copilot Should Handle:**
1. "What is the maintenance history of pump P-101A in the last 2 years?"
2. "Show me the SOP for hot work near hydrogen lines"
3. "Which equipment has overdue inspections under OISD-154?"
4. "What were the root causes of similar compressor trips across all our plants?"
5. "Generate a pre-shutdown checklist for Reactor R-201 based on past turnaround records"

---

### Module 4: Multi-Agent Operations Intelligence System

**Goal:** A coordinated team of specialized AI agents that monitor, diagnose, predict, and report on equipment health — working together through a shared knowledge graph.

**Agent Orchestration Architecture (LangGraph):**
```
                    ┌─────────────────────────────────┐
                    │      ORCHESTRATOR AGENT          │
                    │  (Routes tasks, manages state)   │
                    └──────────────┬──────────────────┘
                                   │
          ┌────────────────────────┼────────────────────────┐
          │                        │                        │
          ▼                        ▼                        ▼
┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│  SENSOR HEALTH   │  │ FAULT DIAGNOSIS  │  │   PREDICTIVE     │
│  MONITOR AGENT   │  │  & SUGGESTION    │  │  MAINTENANCE     │
│                  │  │     AGENT        │  │     AGENT        │
│ • Ingest logs    │  │ • Root cause     │  │ • Failure predict │
│ • Anomaly detect │  │ • Fix suggestion │  │ • RUL estimation │
│ • Threshold check│  │ • Parts needed   │  │ • Schedule optim │
│ • Pattern drift  │  │ • SOP reference  │  │ • Risk scoring   │
└────────┬─────────┘  └────────┬─────────┘  └────────┬─────────┘
         │                     │                      │
         └─────────────────────┼──────────────────────┘
                               │
                               ▼
                  ┌──────────────────────┐
                  │  SHIFT HANDOVER      │
                  │      AGENT           │
                  │                      │
                  │ • Summarize events   │
                  │ • Flag pending items │
                  │ • Generate report    │
                  │ • Recommend focus    │
                  └──────────────────────┘
```

---

#### Agent 1: Sensor Health Monitor Agent

**Purpose:** Continuously ingests machine sensor logs (vibration, temperature, pressure, flow, current) and determines if equipment is operating within acceptable limits.

**Input:** Real-time or batch sensor log data (CSV/JSON/MQTT)
**Output:** Health status classification + anomaly alerts

**Logic Flow:**
```
Sensor Data Stream (vibration, temp, pressure, current, flow)
  → Preprocessing (normalize, handle missing values, resample)
  → Multi-Strategy Anomaly Detection:
      ├─ Threshold Check: Compare against OEM limits from Knowledge Graph
      ├─ Statistical: Z-score / IQR on rolling windows
      ├─ Pattern: Compare against known "pre-failure signatures"
      └─ Trend: Detect drift/degradation over time
  → Health Classification:
      ├─ NORMAL: All parameters within limits
      ├─ WARNING: Parameters drifting toward limits
      ├─ CRITICAL: Parameters breached, immediate action needed
      └─ ANOMALY: Unusual pattern detected, needs investigation
  → Output: Alert + context + hand off to Fault Diagnosis Agent
```

**Key Capabilities:**
- Ingests sensor logs in CSV, JSON, or streaming format
- Pulls equipment-specific thresholds from Knowledge Graph (OEM specs, historical baselines)
- Detects both point anomalies (sudden spike) and contextual anomalies (gradual drift)
- Maintains rolling health score per equipment tag
- Triggers downstream agents when status changes

---

#### Agent 2: Fault Diagnosis & Suggestion Agent

**Purpose:** When the Sensor Monitor flags an anomaly, this agent determines the probable cause and recommends corrective actions — by reasoning across the knowledge graph.

**Input:** Anomaly alert from Monitor Agent + sensor context
**Output:** Root cause hypothesis + ranked corrective actions + SOP references

**Logic Flow:**
```
Anomaly Alert (equipment_tag, parameter, severity, context)
  → Knowledge Graph Query:
      ├─ Pull equipment failure history (same tag)
      ├─ Pull similar equipment failures (same type across fleet)
      ├─ Pull OEM troubleshooting guide references
      ├─ Pull relevant maintenance procedures (SOPs)
      └─ Pull current operating conditions (other related sensors)
  → LLM Reasoning (Ishikawa / 5-Why structured thinking):
      ├─ Correlate current symptoms with historical failure patterns
      ├─ Identify most probable root causes (ranked by confidence)
      ├─ Cross-reference with recent maintenance actions (could recent
      │   work have introduced the issue?)
      └─ Check environmental/seasonal factors
  → Recommendation Generation:
      ├─ Immediate actions (safe operating adjustments)
      ├─ Short-term fix (specific maintenance task)
      ├─ Long-term resolution (design change, PM frequency update)
      ├─ Parts & resources needed
      └─ Referenced SOPs + safety precautions
  → Output: Diagnosis Report with citations + confidence level
```

**Key Capabilities:**
- Doesn't just pattern-match — reasons across the full knowledge graph
- Provides confidence-scored hypotheses (not single answers)
- Always cites source documents (work orders, OEM manuals, past incidents)
- Considers "what changed recently" (recent maintenance, MOC, process changes)
- Suggests multiple resolution paths ranked by risk/effort

---

#### Agent 3: Predictive Maintenance Agent

**Purpose:** Uses historical failure patterns combined with current sensor trends to predict WHEN equipment will likely fail, enabling proactive scheduling.

**Input:** Current sensor health data + historical failure/maintenance records from KG
**Output:** Remaining Useful Life (RUL) estimate + optimized maintenance schedule

**Logic Flow:**
```
Equipment Health Profile (from Sensor Monitor Agent)
  → Historical Analysis:
      ├─ Pull all past failures of this equipment
      ├─ Pull failures of similar equipment type across fleet
      ├─ Map sensor degradation curves before past failures
      └─ Pull OEM recommended maintenance intervals
  → Predictive Modeling:
      ├─ Compare current degradation trend vs historical pre-failure curves
      ├─ Estimate Remaining Useful Life (RUL) using:
      │   ├─ Statistical: Weibull distribution from failure history
      │   ├─ Trend-based: Linear/exponential extrapolation of parameter drift
      │   └─ Pattern-based: Similarity to known "failure signature" profiles
      ├─ Confidence interval on prediction
      └─ Risk score: probability of failure before next scheduled PM
  → Schedule Optimization:
      ├─ Compare predicted failure date vs next scheduled maintenance
      ├─ Suggest advancement/deferral of maintenance
      ├─ Consider production schedule (best maintenance windows)
      └─ Estimate cost of early intervention vs unplanned failure
  → Output: RUL estimate + risk score + recommended action date
```

**Key Capabilities:**
- Combines statistical reliability models with real-time sensor data
- Learns from fleet-wide failure data (not just single equipment)
- Provides confidence intervals, not just point predictions
- Integrates with production schedule to find optimal windows
- Quantifies the cost/risk tradeoff of intervention timing

---

#### Agent 4: Shift Handover Agent

**Purpose:** Automatically generates comprehensive shift handover reports by summarizing all events, alarms, actions, and pending items from a shift period.

**Input:** Time range (shift start/end) + all events from that period
**Output:** Structured handover report with priorities for incoming team

**Logic Flow:**
```
Shift Time Window (e.g., 06:00 - 18:00)
  → Data Collection:
      ├─ All sensor alarms triggered during shift
      ├─ All anomalies detected by Monitor Agent
      ├─ Maintenance activities completed (from work orders)
      ├─ Maintenance activities started but not completed
      ├─ Process parameter deviations
      ├─ Safety events or near-misses
      └─ Operator actions / manual overrides logged
  → Summarization & Prioritization:
      ├─ Critical items requiring immediate attention
      ├─ Equipment health changes (what got better/worse)
      ├─ Work in progress (partially completed tasks)
      ├─ Upcoming scheduled activities (next 12 hours)
      ├─ Pending decisions requiring incoming team's input
      └─ Anomalies under investigation (context for continuity)
  → Report Generation:
      ├─ Executive summary (3-5 bullet points)
      ├─ Detailed section per area/unit
      ├─ Equipment health dashboard snapshot
      ├─ Action items with ownership and deadlines
      └─ "Watch items" — things to monitor closely
  → Output: Formatted report (PDF/display) + verbal summary for voice briefing
```

**Key Capabilities:**
- Eliminates manual handover note-taking (saves 30+ min per shift)
- Never misses an event — captures everything from all systems
- Prioritizes by severity so incoming team knows what to focus on first
- Maintains continuity for multi-day issues (tracks ongoing investigations)
- Can generate voice summary for hands-free briefing

---

#### Agent Coordination & Communication

**How agents work together:**
```
Example Flow: Bearing Degradation Detection -> Resolution

1. SENSOR MONITOR AGENT detects vibration trending upward on Pump P-101A
   -> Status: WARNING (7.5 mm/s, limit 11.2 mm/s, trending up at 0.3 mm/s per week)

2. FAULT DIAGNOSIS AGENT activated:
   -> Queries KG: "P-101A had bearing failure in Mar-2024 with similar signature"
   -> Hypothesis: "Lubrication degradation (80% confidence)"
   -> Suggestion: "Check oil condition, schedule bearing inspection within 2 weeks"
   -> References: WO-100234, SOP-MAINT-045, OEM Manual Section 4.3

3. PREDICTIVE MAINTENANCE AGENT calculates:
   -> At current degradation rate: estimated failure in 18-25 days
   -> Next scheduled PM: 45 days away
   -> Recommendation: "Advance PM by 3 weeks. Optimal window: this weekend shutdown"
   -> Cost analysis: Early PM = $2,400 vs unplanned failure = $45,000 + 72h downtime

4. SHIFT HANDOVER AGENT captures all of the above:
   -> "P-101A vibration WARNING -- diagnosis suggests lubrication issue,
      PM advancement recommended for this weekend. See Diagnosis Report DR-2024-089."
```

---

#### Agent Technical Implementation Details

**Agent 1 -- Sensor Monitor: Detection Algorithms**

| Algorithm | What it Catches | Formula / Logic |
|-----------|----------------|-----------------|
| Threshold Check | Value exceeding OEM limits | Compare against 3-band limits (normal/warning/critical) from Knowledge Graph. Severity = proximity to critical as fraction. |
| Z-Score | Sudden spikes or drops | `z = abs(value - mean) / stdev` over rolling 50-reading window. z > 2.5 = warning, z > 3.5 = anomaly. |
| Trend Detection | Slow degradation over time | Split rolling window into older/recent halves, compare means. Change > 20% = trending. Direction computed via linear regression slope. |

Default industrial thresholds built in (overridden by KG):
```
vibration:   normal < 7.1 mm/s   warning < 11.2 mm/s   critical < 18.0 mm/s  (ISO-10816)
temperature: normal < 80 C       warning < 95 C         critical < 120 C
pressure:    normal < 45 bar      warning < 50 bar       critical < 55 bar
current:     normal < 85% rated   warning < 95%          critical < 105%
```

**Agent 2 -- Fault Diagnosis: Knowledge Sources**

| Source | How It's Used |
|--------|-------------|
| Failure Pattern Library | 15+ pre-built failure mode hypotheses mapped by parameter type (vibration->bearing/misalignment/imbalance, temperature->cooling/overload, pressure->blockage/leak) |
| Knowledge Graph Query | `neo4j.get_equipment_context(tag)` returns past work orders, incidents, inspections, applicable regulations -- confidence boosted +15% when history matches a hypothesis |
| LLM Reasoning (Ollama) | Sends alert + existing hypotheses to local LLM for additional root causes, interaction effects, and "what changed recently" analysis |
| Standard Action Library | Category-mapped corrective actions (mechanical/process/instrumentation) with priority, effort, parts, SOP references, and safety precautions |

**Agent 3 -- Predictive Maintenance: Two Prediction Methods**

| Method | Algorithm | Output |
|--------|----------|--------|
| Trend Extrapolation | Linear regression on reading history. `days_to_failure = (critical_limit - current) / slope / 24`. CI widened by `(1 - R^2) * 2`. | RUL in days + confidence interval |
| Weibull Reliability | `reliability = e^(-(hours/MTBF)^beta)` with beta=2 (wear-out). `remaining = MTBF * Gamma(1.5) - hours`. | Statistical RUL independent of sensors |

Cost/benefit lookup per equipment type:
```
pump:       planned=$2,500    unplanned=$45,000
compressor: planned=$8,000    unplanned=$150,000
motor:      planned=$3,000    unplanned=$35,000
valve:      planned=$1,500    unplanned=$25,000
```

**Agent 4 -- Shift Handover: Report Sections**

| Section | Content | Source |
|---------|---------|--------|
| Executive Summary | 3-5 bullet points (LLM-generated if Ollama available) | All events aggregated |
| Critical Items | Unresolved critical/high severity items | Events with status=pending + severity=critical/high |
| Alarm Summary | Total / Critical / Resolved / Pending counts | Filtered from event log |
| Work in Progress | Partially completed maintenance tasks | Events with status=in_progress |
| Watch Items | Equipment with 2+ alarms (recurring issue) + unresolved high items | Alarm frequency analysis |
| Upcoming Activities | Next 12 hours scheduled maintenance | PM schedule integration |

---

#### Agent API Endpoints

| Endpoint | Method | Description | Request Body |
|----------|--------|-------------|-------------|
| `/api/v1/agents/analyze-sensors` | POST | Full pipeline: Monitor -> Diagnose -> Log. Auto-saves reports. | `{"readings": [{"equipment_tag","parameter","value","unit","timestamp"}]}` |
| `/api/v1/agents/predict-maintenance` | POST | RUL estimation for specific equipment. Auto-saves report. | `{"equipment_tag","parameter_history","critical_limits","equipment_type","hours_in_service"}` |
| `/api/v1/agents/shift-handover` | POST | Generate shift report for time window. Auto-saves report. | `{"shift_start","shift_end"}` |
| `/api/v1/agents/reports` | GET | List/filter saved reports by category, equipment, or status | Query params: `?category=&equipment=&status=` |
| `/api/v1/agents/reports/{category}/{filename}` | GET | Retrieve a specific saved report by path | Path params: category + filename |

**Agent Data Flow:**
```
POST /analyze-sensors (batch of readings)
  |
  v
Orchestrator.process_sensor_batch()
  |
  |--> SensorHealthMonitorAgent.analyze_batch()
  |      Returns: list[AnomalyAlert]
  |
  |--> For each WARNING/CRITICAL alert:
  |      FaultDiagnosisAgent.diagnose(alert)
  |        |--> _get_pattern_hypotheses()     -- built-in failure library
  |        |--> _query_knowledge_graph()       -- Neo4j equipment context
  |        |--> _llm_reasoning()               -- Ollama for deeper analysis
  |        |--> _generate_actions()            -- category-mapped actions
  |      Returns: DiagnosisReport
  |
  |--> ShiftHandoverAgent.log_alarm()          -- stores for handover
  |
  |--> ReportSaver.save_sensor_analysis()      -- saves to data/reports/sensor_analysis/
  |--> ReportSaver.save_fault_diagnosis()      -- saves per-equipment diagnosis report
  |
  v
Response: {alerts, diagnoses, health_summary, actions_generated, report_saved_to}

POST /predict-maintenance
  |
  |--> PredictiveMaintenanceAgent.predict()
  |--> ReportSaver.save_predictive_report()    -- saves to data/reports/predictive/
  v
Response: {rul_estimates, recommendations, risk_summary, report_saved_to}

POST /shift-handover
  |
  |--> ShiftHandoverAgent.generate_report()
  |--> ReportSaver.save_shift_handover()       -- saves to data/reports/shift_handover/
  v
Response: {summary, critical_items, watch_items, formatted_report, report_saved_to}

GET /reports?equipment=P-101A&status=CRITICAL
  |
  |--> Scans data/reports/ subdirectories
  |--> Filters filenames by equipment tag and status label
  v
Response: {total_reports, reports: [{filename, category, equipment, shift, status, path}]}
```

---

### Module 5: Quality & Regulatory Compliance Intelligence

**Goal:** Continuously map regulatory requirements against actual plant state, flagging gaps proactively.

**Compliance Mapping Engine:**
```
Regulation Database (BIS, OISD, PESO, Factory Act, ISO, API)
  → Requirement Decomposition (clause → checklist items)
  → Auto-mapping to:
      ├─ Relevant Equipment/Systems
      ├─ Applicable Procedures (current revision)
      ├─ Required Inspection Records
      ├─ Training/Competency Requirements
      └─ Documentation Evidence Requirements
  → Gap Analysis:
      ├─ Missing/expired documents
      ├─ Overdue inspections
      ├─ Procedure-regulation misalignment
      ├─ Training gaps
      └─ Equipment non-compliance indicators
  → Output: Compliance Dashboard + Audit Package Generator + Alert System
```

---

### Module 6: Lessons Learned & Failure Intelligence Engine

**Goal:** Pattern recognition across historical incidents and near-misses to prevent recurrence.

**Approach:**
- Cluster similar incidents using embedding similarity
- Extract causal factors and map to equipment/process taxonomy
- Build "failure signature" profiles for equipment types
- Proactive alerting when current conditions match historical pre-failure patterns
- Cross-plant and cross-industry learning (anonymized)

---

## Technology Stack (100% FREE -- Zero API Costs)

### Core Infrastructure
| Layer | Technology | Cost | Purpose |
|-------|-----------|------|---------|
| **LLM** | Ollama + Llama 3.1 8B / Mistral 7B | FREE | Answer generation, entity extraction, shift summaries |
| **Embeddings** | sentence-transformers (all-MiniLM-L6-v2) | FREE | 384-dim local embeddings, no network needed |
| **Vector DB** | Qdrant (Docker, open source) | FREE | Semantic search over document chunks |
| **Graph DB** | Neo4j Community Edition (Docker) | FREE | Knowledge graph: equipment, events, regulations |
| **Cache/Queue** | Redis (Docker) | FREE | Async task queue for ingestion pipeline |
| **Backend** | FastAPI (Python 3.11) | FREE | Async REST API, WebSocket support |
| **Deployment** | Docker Compose (5 containers) | FREE | One-command startup of full stack |

### Document Ingestion Pipeline
| Component | Technology | What It Does |
|-----------|-----------|-------------|
| PDF Parser | PyMuPDF (fitz) | Text extraction with layout, table finder, image extraction |
| DOCX Parser | python-docx | Paragraph + table extraction from Word documents |
| OCR Engine | Tesseract + Pillow | Grayscale -> contrast enhance -> sharpen -> binarize -> OCR. Confidence scoring per word. |
| Entity Extractor | Regex patterns (ISA format) + spaCy NER | 6 entity types: equipment (`XX-NNNN`), parameters (value+unit), regulations (`OISD-NNN`), dates, personnel, document references. False-positive filtering for months/standards. |
| Relationship Extractor | Regex triggers + co-occurrence | Pattern-based: "X failed due to Y". Co-occurrence: equipment + regulation in same sentence = GOVERNED_BY. |
| Document Classifier | Keyword pattern scoring | Weighted regex patterns per category (work_order/SOP/incident/inspection/regulatory). Filename bonus. |
| Text Chunker | Semantic boundary splitting | Respects section headers and sentence boundaries. 512-char chunks with 64-char overlap. |
| LLM Extractor | Ollama (JSON mode) | Second-pass extraction for complex/ambiguous entities. Structured JSON output. |

### RAG / Retrieval
| Component | Technology | Algorithm |
|-----------|-----------|-----------|
| Vector Search | Qdrant + sentence-transformers | Cosine similarity over 384-dim embeddings |
| Graph Search | Neo4j Cypher | Entity extraction from query -> `get_equipment_context()` -> relationship traversal |
| Keyword Search | BM25Okapi (rank-bm25) | TF-IDF-based scoring over tokenized corpus |
| Result Fusion | Reciprocal Rank Fusion | `RRF_score = sum(1/(k + rank_i))` across all retrieval methods, k=60 |
| Answer Generation | Ollama (Llama 3.1) | System prompt enforces citations, 0.1 temperature, 1500 token limit |

### Multi-Agent System
| Agent | Tech Used | Key Algorithm |
|-------|----------|---------------|
| Sensor Monitor | Python stdlib (statistics) | 3-strategy detection: threshold bands + Z-score (rolling 50) + trend split-half comparison |
| Fault Diagnosis | Pattern library + Neo4j + Ollama | 15+ failure mode hypotheses, KG-boosted confidence, LLM-powered 5-Why reasoning |
| Predictive Maintenance | Linear regression + Weibull (math lib) | Trend extrapolation to critical limit + Weibull RUL with beta=2 wear-out mode |
| Shift Handover | Event aggregation + Ollama | Frequency analysis for watch items, LLM summarization, structured report formatting |
| Orchestrator | Sequential pipeline | Monitor -> Diagnosis (if anomaly) -> log to Handover. Shared state via function calls. |

---

## Implementation Status & Timeline

### Phase 1: Foundation -- COMPLETE
- [x] Project structure with Docker Compose (Neo4j + Qdrant + Redis + Ollama)
- [x] Document ingestion pipeline (PDF, DOCX, image with OCR fallback)
- [x] Neo4j schema with constraints + indexes for all node types
- [x] Entity extraction (equipment tags, parameters, regulations, personnel, dates, doc refs)
- [x] Relationship extraction (pattern-based + co-occurrence)
- [x] Document classification (7 categories: WO/SOP/incident/inspection/OEM/regulatory/P&ID)
- [x] Knowledge graph population from extracted entities
- [x] Text chunking with semantic boundary awareness
- [x] Sample data generation (20 work orders, 10 inspections, 8 incidents, 1 SOP)

### Phase 2: Intelligence Layer -- COMPLETE
- [x] Hybrid RAG retrieval (vector + graph traversal + BM25 keyword)
- [x] Reciprocal Rank Fusion for result merging
- [x] Conversational copilot with citation enforcement
- [x] Confidence scoring (high/medium/low)
- [x] Follow-up question suggestions
- [x] Sensor Health Monitor Agent (3 detection strategies)
- [x] Fault Diagnosis Agent (pattern library + KG + LLM reasoning)
- [x] Predictive Maintenance Agent (trend extrapolation + Weibull)
- [x] Shift Handover Agent (event aggregation + LLM summary)
- [x] Agent Orchestrator (coordinates all 4 agents)
- [x] Report Persistence System (auto-save all reports with naming convention)
- [x] Report browsing API (list/filter/retrieve saved reports)
- [x] FREE local stack (Ollama + sentence-transformers, no API keys needed)

### Phase 3: UX & Integration -- TODO
- [ ] Build web dashboard (document explorer + graph visualization)
- [ ] Build chat interface (desktop + mobile-responsive)
- [ ] Implement interactive knowledge graph visualization (D3.js or vis.js)
- [ ] Build compliance dashboard with gap indicators
- [ ] Add voice input support for field use (Web Speech API)

### Phase 4: Polish & Deliverables -- TODO
- [ ] End-to-end testing with real industrial document samples
- [ ] Performance optimization (caching, batch processing)
- [ ] Record demo video (5-7 min narrated walkthrough)
- [ ] Create architecture diagram (publication-quality)
- [ ] Prepare presentation deck (10-12 slides)
- [ ] Write evaluation metrics & benchmark results

### Files Implemented: 44 files
```
Backend source:  22 files (config, models, 4 routers, 15 services including 6 agents)
Backend infra:    2 files (Dockerfile, requirements.txt)
Init modules:     9 files (__init__.py across all packages)
Project config:   5 files (docker-compose, .env.example, README)
Scripts:          3 files (demo_standalone, demo_agents, generate_synthetic_docs)
Sample data:      3 files (generated JSON + TXT documents)
```

---

## Data Strategy for Demo

**Synthetic + Public Industrial Documents:**
1. **P&IDs:** Generate sample P&IDs using standard ISA symbology (or use open-source examples from engineering education resources)
2. **Maintenance Records:** Synthesize realistic work order history using LLM (based on public equipment failure mode databases like OREDA)
3. **SOPs/Procedures:** Create sample operating procedures following typical industrial structure
4. **Inspection Reports:** Generate sample inspection findings aligned with OISD/API standards
5. **Incident Reports:** Synthesize based on publicly available investigation reports (CSB, OISD bulletins)
6. **Regulatory Documents:** Use publicly available BIS/OISD standards clauses

**Target Corpus Size:** 200-500 documents across 6+ types to demonstrate heterogeneous ingestion.

---

## Differentiation & Innovation Points

1. **Multi-modal Knowledge Graph:** Not just text — includes parsed P&ID topology, making it possible to answer "what is upstream of valve XV-101?" by traversing the graph
2. **Temporal Knowledge:** The graph tracks state over time — "what was the bearing vibration trend before the last 3 failures of this pump type?"
3. **Cross-document Co-reference Resolution:** Equipment tag "P-101A" in a work order is linked to the same node as "Pump 101A" in an incident report and "BFW Pump A" in an SOP
4. **Proactive Intelligence:** System doesn't just answer questions — it pushes alerts when it detects patterns (e.g., "3 plants experienced similar valve failures after this maintenance interval change")
5. **Explainable AI:** Every recommendation traces back through the reasoning chain to source documents — critical for safety-critical industries
6. **Offline-First Mobile:** Field technicians need answers at the equipment, not at their desk

---

## Evaluation Metrics (Self-Assessment Framework)

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| Entity Extraction Accuracy | >85% F1 | Annotated test set of 50 documents |
| Query Answer Quality | >80% relevance (human-rated) | 30 domain-expert benchmark questions |
| Knowledge Graph Completeness | >70% of entities linked | Random sample audit |
| Time-to-Answer vs. Manual Search | 10x faster | Comparative timing study |
| Compliance Gap Detection | >75% precision | Known-gap test scenarios |
| Cross-document Discovery | Demonstrate 5+ non-obvious connections | Qualitative showcase |

---

## Risk Mitigation

| Risk | Mitigation |
|------|-----------|
| P&ID parsing accuracy | Fallback to GPT-4o Vision for complex drawings; human-in-the-loop for low-confidence extractions |
| LLM hallucination in safety-critical answers | Strict citation enforcement; confidence thresholds; "I don't know" responses when retrieval confidence is low |
| Data sensitivity | Local LLM option (Llama 3.1); all processing can run air-gapped |
| Scalability of graph for large orgs | Partitioning strategy by plant/unit; lazy loading; graph summarization |
| Demo impact | Pre-seed with compelling scenarios that showcase cross-document intelligence |

---

## Deliverables Checklist

- [ ] **Working Prototype:** Deployed (Docker Compose) with ingestion pipeline, knowledge graph, RAG copilot, and at least one agentic workflow (maintenance RCA or compliance)
- [ ] **Architecture Diagram:** Publication-quality diagram showing all layers, data flows, and technology choices
- [ ] **Presentation Deck:** 10-12 slides covering problem, solution, architecture, demo highlights, business impact, and roadmap
- [ ] **Demo Video:** 5-7 minute narrated walkthrough showing end-to-end flow from document ingestion to actionable intelligence

---

## Project Structure (Implemented)

```
axiom/
├── docker-compose.yml              # Neo4j + Qdrant + Redis + Ollama + Backend
├── .env.example                    # Config (LLM_PROVIDER=ollama, all free)
├── README.md                       # Setup guide with $0 cost breakdown
│
├── backend/
│   ├── Dockerfile                  # Python 3.11 + Tesseract OCR
│   ├── requirements.txt            # All free/open-source dependencies
│   ├── app/
│   │   ├── main.py                 # FastAPI app with lifespan (Neo4j + Qdrant init)
│   │   ├── config.py               # Settings: Ollama/OpenAI, Neo4j, Qdrant, Redis
│   │   │
│   │   ├── models/
│   │   │   └── schemas.py          # Pydantic: DocumentChunk, QueryRequest/Response, etc.
│   │   │
│   │   ├── routers/
│   │   │   ├── ingest.py           # POST /ingest/document, /ingest/batch
│   │   │   ├── query.py            # POST /query/ask, /query/search
│   │   │   ├── graph.py            # GET /graph/equipment/{tag}, /graph/stats
│   │   │   └── agents.py           # POST /agents/analyze-sensors, /predict, /handover
│   │   │
│   │   └── services/
│   │       ├── ingestion/
│   │       │   ├── pdf_parser.py           # PyMuPDF: text + table + image extraction
│   │       │   ├── ocr_engine.py           # Tesseract: preprocessing + OCR with confidence
│   │       │   ├── entity_extractor.py     # Regex + spaCy NER: equipment/params/regulations
│   │       │   ├── relationship_extractor.py # Pattern + co-occurrence relationship extraction
│   │       │   ├── document_classifier.py  # Keyword scoring: WO/SOP/incident/inspection/etc.
│   │       │   ├── chunker.py              # Semantic boundary-aware text chunking
│   │       │   ├── llm_extractor.py        # Ollama/OpenAI for complex entity extraction
│   │       │   └── pipeline.py             # Orchestrates: parse->OCR->classify->extract->chunk
│   │       │
│   │       ├── knowledge_graph/
│   │       │   ├── neo4j_client.py         # Async Neo4j: schema, CRUD, traversal, search
│   │       │   └── graph_builder.py        # Maps entities/relationships to Neo4j nodes/edges
│   │       │
│   │       ├── vectorstore/
│   │       │   └── qdrant_service.py       # Embedding engine (sentence-transformers/Ollama)
│   │       │                                 + Qdrant indexing/search
│   │       │
│   │       ├── rag/
│   │       │   ├── retriever.py            # Hybrid: Vector + Graph + BM25, RRF fusion
│   │       │   └── generator.py            # Ollama/OpenAI answer gen with citation enforcement
│   │       │
│   │       └── agents/
│   │           ├── sensor_monitor_agent.py      # Threshold + Z-score + trend detection
│   │           ├── fault_diagnosis_agent.py     # Pattern library + KG + LLM reasoning
│   │           ├── predictive_maintenance_agent.py  # Trend extrapolation + Weibull RUL
│   │           ├── shift_handover_agent.py      # Event collection + LLM summarization
│   │           ├── report_saver.py              # Auto-saves all reports with naming convention
│   │           └── orchestrator.py              # Coordinates all 4 agents in pipeline
│
├── scripts/
│   ├── demo_standalone.py          # Full ingestion pipeline demo (zero deps)
│   ├── demo_agents.py              # Full 4-agent demo (zero deps)
│   └── generate_synthetic_docs.py  # Creates sample WOs, incidents, SOPs, inspections
│
├── data/
│   ├── sample_documents/           # Generated: JSON + TXT work orders, incidents, SOPs
│   └── reports/                    # Auto-generated agent reports (naming convention)
│       ├── sensor_analysis/        # {equipment}_{shift}_{status}_{timestamp}.json
│       ├── fault_diagnosis/        # {equipment}_{shift}_DIAGNOSIS-{conf}_{timestamp}.json
│       ├── predictive/             # {equipment}_{shift}_PREDICTION-{risk}_{timestamp}.json
│       └── shift_handover/         # {equipment}_{shift}_HANDOVER-{status}_{timestamp}.json
│
└── frontend/                       # (Phase 3: React + Next.js PWA)
    └── ...
```

---

## Complete API Reference (17 endpoints)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| **Ingestion** | | |
| `/api/v1/ingest/document` | POST | Upload & process single document (PDF/DOCX/image) |
| `/api/v1/ingest/batch` | POST | Upload & process multiple documents |
| **Query (RAG)** | | |
| `/api/v1/query/ask` | POST | Ask question, get AI answer with source citations |
| `/api/v1/query/search` | POST | Search documents, return ranked chunks (no LLM) |
| **Knowledge Graph** | | |
| `/api/v1/graph/search` | POST | Search graph nodes by term |
| `/api/v1/graph/equipment/{tag}` | GET | Full equipment context (WOs, incidents, regulations) |
| `/api/v1/graph/neighbors/{type}/{key}/{value}` | GET | Graph neighborhood traversal |
| `/api/v1/graph/stats` | GET | Node/relationship counts by type |
| **Multi-Agent Intelligence** | | |
| `/api/v1/agents/analyze-sensors` | POST | Sensor batch -> anomaly detection -> diagnosis. Auto-saves report. |
| `/api/v1/agents/predict-maintenance` | POST | RUL estimation + maintenance scheduling. Auto-saves report. |
| `/api/v1/agents/shift-handover` | POST | Automated shift report generation. Auto-saves report. |
| **Report Management** | | |
| `/api/v1/agents/reports` | GET | List all saved reports. Filter: `?category=&equipment=&status=` |
| `/api/v1/agents/reports/{category}/{filename}` | GET | Retrieve specific saved report JSON |

---

## Report Persistence System

All agent-generated reports are automatically saved to `data/reports/` with structured naming and browsable via API.

**Naming Convention:** `{equipment}_{shift}_{status}_{YYYYMMDD_HHMMSS}.json`

| Component | Rule |
|-----------|------|
| **Equipment** | Tag from the reading (e.g. `P-101A`). Multiple equipment = `P-101A_C-301` (up to 3) or `MULTI-5eq`. Fleet-wide = `FLEET`. |
| **Shift** | Auto-detected from timestamp: `day` (06-14), `evening` (14-22), `night` (22-06) |
| **Status** | Derived from alert severity: `NORMAL`, `WARNING`, `CRITICAL`. Diagnosis adds confidence: `DIAGNOSIS-HIGH`. Prediction adds risk: `PREDICTION-HIGH-RISK`. Handover adds: `HANDOVER-NORMAL` / `HANDOVER-CRITICAL`. |
| **Timestamp** | UTC `YYYYMMDD_HHMMSS` |

**Directory Structure:**
```
data/reports/
  sensor_analysis/
    P-101A_day_CRITICAL_20240701_143022.json
    C-301_P-101A_evening_WARNING_20240701_180500.json
    MULTI-5eq_night_NORMAL_20240702_020000.json
  fault_diagnosis/
    P-101A_day_DIAGNOSIS-HIGH_20240701_143025.json
    C-301_evening_DIAGNOSIS-MEDIUM_20240701_180510.json
  predictive/
    P-101A_day_PREDICTION-HIGH-RISK_20240703_091500.json
    HX-501_evening_PREDICTION-LOW-RISK_20240703_150000.json
  shift_handover/
    FLEET_day_HANDOVER-CRITICAL_20240701_060000.json
    P-101A_night_HANDOVER-NORMAL_20240701_220000.json
```

**API Usage:**
```bash
# List all reports
curl http://localhost:8000/api/v1/agents/reports

# Filter by equipment
curl "http://localhost:8000/api/v1/agents/reports?equipment=P-101A"

# Filter by status (only problematic)
curl "http://localhost:8000/api/v1/agents/reports?status=CRITICAL"

# Filter by category
curl "http://localhost:8000/api/v1/agents/reports?category=fault_diagnosis"

# Get specific report
curl http://localhost:8000/api/v1/agents/reports/sensor_analysis/P-101A_day_CRITICAL_20240701_143022.json
```

---

## Key Demo Scenarios (Wow Factor)

### Scenario 1: "The Missing Connection"
Upload 5 seemingly unrelated documents (a work order from 2022, an incident report from 2023, an OEM bulletin, an inspection finding, and a procedure). Show how AXIOM automatically connects them through the knowledge graph and surfaces a pattern: "These 3 equipment failures share a common root cause that spans across departments."

### Scenario 2: "Field Technician at 2 AM"
A maintenance technician encounters an unfamiliar alarm on a critical piece of equipment. Using voice query on mobile: "What should I do when compressor C-201 shows high discharge temperature with low oil pressure?" The copilot returns the relevant SOP section, similar past incidents, and immediate actions — with confidence score and source links.

### Scenario 3: "Audit in 48 Hours"
Regulatory audit announced. The compliance agent scans all equipment against OISD-154 requirements, identifies 12 documentation gaps, and auto-generates an evidence package for the 85% that IS compliant — turning weeks of preparation into hours.

### Scenario 4: "The Retirement Knowledge Transfer"
A senior engineer is retiring. AXIOM identifies all documents they authored, procedures they developed, and tacit knowledge captured in their work order comments over 20 years — creating a structured knowledge handover package.

---

## Budget Estimate — $0 Total (Fully Local Stack)

| Service | Cost | Notes |
|---------|------|-------|
| Ollama + Llama 3.1 / Mistral (local LLM) | $0 | Runs on any machine with 8GB+ RAM |
| sentence-transformers (local embeddings) | $0 | No API calls, runs on CPU |
| Neo4j Community Edition (Docker) | $0 | Self-hosted, full graph features |
| Qdrant (Docker) | $0 | Self-hosted vector DB |
| Tesseract OCR | $0 | Open source, bundled in Docker image |
| Redis (Docker) | $0 | Open source message broker |
| spaCy + PyMuPDF | $0 | Open source NLP/PDF libraries |
| Docker (local or any Linux server) | $0 | Free for development and deployment |
| **Total** | **$0** | **Entire platform runs offline with no paid APIs** |

> **Optional upgrade**: If higher quality LLM responses are desired, swap `LLM_PROVIDER=openai` in `.env` and add an API key (~$50). The platform works identically with or without it.

---

## Team Role Allocation (4-5 members suggested)

| Role | Responsibility |
|------|---------------|
| **Backend/AI Lead** | Ingestion pipeline, entity extraction, RAG engine, agent workflows |
| **Knowledge Engineer** | Ontology design, Neo4j schema, graph population, relationship extraction |
| **Frontend/UX** | Dashboard, chat UI, mobile PWA, graph visualization |
| **Data/Demo Lead** | Synthetic data generation, demo scenarios, benchmarking, evaluation metrics |
| **Integration/DevOps** | Docker setup, API gateway, deployment, monitoring, presentation |

---

## Winning Strategy

1. **Start with the demo backwards** -- Design the 3-4 "wow moment" demo scenarios FIRST, then build just enough to make them work flawlessly
2. **Real documents > synthetic** -- Even 20 real industrial documents (publicly available OEM manuals, OISD standards, sample P&IDs) are more convincing than 200 synthetic ones
3. **Knowledge graph visualization is your secret weapon** -- Judges can SEE the connections. An interactive graph explorer is worth more than 1000 words
4. **Mobile demo** -- Show the copilot working on a phone. Nobody else will do this. It directly addresses the "field technician" use case
5. **Quantify everything** -- Show retrieval latency, entity extraction F1 scores, time savings vs. manual search. Numbers win over narratives
6. **Business impact framing** -- Lead with "18-22% of unplanned downtime is caused by knowledge fragmentation. Our platform reduces this by X%"

---

## Quick Start -- Run the Demos Now (No Setup Required)

```bash
# 1. Generate sample industrial documents
python scripts/generate_synthetic_docs.py

# 2. Run ingestion pipeline demo (entity extraction, classification, chunking)
python scripts/demo_standalone.py

# 3. Run multi-agent demo (sensor monitoring, fault diagnosis, RUL prediction, shift handover)
python scripts/demo_agents.py

# 4. Full stack with Docker (requires Docker installed)
docker-compose up -d                              # Start Neo4j + Qdrant + Redis + Ollama
docker exec axiom-ollama-1 ollama pull llama3.1:8b # Pull free LLM (~4.7GB, one-time)
cd backend && pip install -r requirements.txt      # Install Python deps
uvicorn app.main:app --reload --port 8000          # Start API server
```
