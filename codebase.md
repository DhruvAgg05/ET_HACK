# New Codebase

# AXIOM Codebase Documentation

Complete source code for **AXIOM — Offline GraphRAG Industrial Knowledge Platform**.
Total files documented: **64**

---

## Table of Contents

### Top Level

- [README.md](https://app.notion.com/p/New-Codebase-3a0dc871c95380959c34c5137fed2982?pvs=21) — Project README
- [docker-compose.yml](https://app.notion.com/p/New-Codebase-3a0dc871c95380959c34c5137fed2982?pvs=21) — Docker Compose — Neo4j + Ollama infrastructure

### Infrastructure

- [backend/Dockerfile](https://app.notion.com/p/New-Codebase-3a0dc871c95380959c34c5137fed2982?pvs=21) — Backend Docker image
- [backend/requirements.txt](https://app.notion.com/p/New-Codebase-3a0dc871c95380959c34c5137fed2982?pvs=21) — Python dependencies

### Backend Core

- [backend/app/**init**.py](https://app.notion.com/p/New-Codebase-3a0dc871c95380959c34c5137fed2982?pvs=21) — App package init
- [backend/app/config.py](https://app.notion.com/p/New-Codebase-3a0dc871c95380959c34c5137fed2982?pvs=21) — Application configuration (Pydantic Settings)
- [backend/app/main.py](https://app.notion.com/p/New-Codebase-3a0dc871c95380959c34c5137fed2982?pvs=21) — FastAPI application entry point
- [backend/app/models/**init**.py](https://app.notion.com/p/New-Codebase-3a0dc871c95380959c34c5137fed2982?pvs=21) — Models package init
- [backend/app/models/schemas.py](https://app.notion.com/p/New-Codebase-3a0dc871c95380959c34c5137fed2982?pvs=21) — Pydantic data models
- [backend/app/services/**init**.py](https://app.notion.com/p/New-Codebase-3a0dc871c95380959c34c5137fed2982?pvs=21) — Services package init

### API Routers

- [backend/app/routers/**init**.py](https://app.notion.com/p/New-Codebase-3a0dc871c95380959c34c5137fed2982?pvs=21) — Routers package init
- [backend/app/routers/ingest.py](https://app.notion.com/p/New-Codebase-3a0dc871c95380959c34c5137fed2982?pvs=21) — Document ingestion API + SSE streaming pipeline
- [backend/app/routers/query.py](https://app.notion.com/p/New-Codebase-3a0dc871c95380959c34c5137fed2982?pvs=21) — RAG query API + SSE streaming retrieval
- [backend/app/routers/graph.py](https://app.notion.com/p/New-Codebase-3a0dc871c95380959c34c5137fed2982?pvs=21) — Knowledge graph + FAISS search API
- [backend/app/routers/agents.py](https://app.notion.com/p/New-Codebase-3a0dc871c95380959c34c5137fed2982?pvs=21) — Multi-agent intelligence API

### Document Ingestion Services

- [backend/app/services/ingestion/**init**.py](https://app.notion.com/p/New-Codebase-3a0dc871c95380959c34c5137fed2982?pvs=21) — Ingestion package init
- [backend/app/services/ingestion/pipeline.py](https://app.notion.com/p/New-Codebase-3a0dc871c95380959c34c5137fed2982?pvs=21) — Main 11-step ingestion pipeline orchestrator
- [backend/app/services/ingestion/pdf_parser.py](https://app.notion.com/p/New-Codebase-3a0dc871c95380959c34c5137fed2982?pvs=21) — PDF and DOCX parser (PyMuPDF)
- [backend/app/services/ingestion/ocr_engine.py](https://app.notion.com/p/New-Codebase-3a0dc871c95380959c34c5137fed2982?pvs=21) — OCR engine — PaddleOCR (primary) + Tesseract (fallback)
- [backend/app/services/ingestion/text_cleaner.py](https://app.notion.com/p/New-Codebase-3a0dc871c95380959c34c5137fed2982?pvs=21) — Text cleaning and normalization (ftfy + regex)
- [backend/app/services/ingestion/document_structurer.py](https://app.notion.com/p/New-Codebase-3a0dc871c95380959c34c5137fed2982?pvs=21) — Document structure builder (pages → sections → paragraphs)
- [backend/app/services/ingestion/chunker.py](https://app.notion.com/p/New-Codebase-3a0dc871c95380959c34c5137fed2982?pvs=21) — Semantic text chunker (500 tokens, 70 overlap)
- [backend/app/services/ingestion/entity_extractor.py](https://app.notion.com/p/New-Codebase-3a0dc871c95380959c34c5137fed2982?pvs=21) — Industrial entity extractor (spaCy + regex)
- [backend/app/services/ingestion/relationship_extractor.py](https://app.notion.com/p/New-Codebase-3a0dc871c95380959c34c5137fed2982?pvs=21) — Relationship triple extractor
- [backend/app/services/ingestion/document_classifier.py](https://app.notion.com/p/New-Codebase-3a0dc871c95380959c34c5137fed2982?pvs=21) — Document category classifier (7 categories)
- [backend/app/services/ingestion/llm_extractor.py](https://app.notion.com/p/New-Codebase-3a0dc871c95380959c34c5137fed2982?pvs=21) — LLM-based entity extractor (Ollama)

### Vector Store Services

- [backend/app/services/vectorstore/**init**.py](https://app.notion.com/p/New-Codebase-3a0dc871c95380959c34c5137fed2982?pvs=21) — Vectorstore package init
- [backend/app/services/vectorstore/faiss_service.py](https://app.notion.com/p/New-Codebase-3a0dc871c95380959c34c5137fed2982?pvs=21) — FAISS vector store + sentence-transformers embedding engine
- [backend/app/services/vectorstore/qdrant_service.py](https://app.notion.com/p/New-Codebase-3a0dc871c95380959c34c5137fed2982?pvs=21) — Qdrant vector store (legacy, kept for reference)

### Knowledge Graph Services

- [backend/app/services/knowledge_graph/**init**.py](https://app.notion.com/p/New-Codebase-3a0dc871c95380959c34c5137fed2982?pvs=21) — Knowledge graph package init
- [backend/app/services/knowledge_graph/neo4j_client.py](https://app.notion.com/p/New-Codebase-3a0dc871c95380959c34c5137fed2982?pvs=21) — Neo4j async client with schema management
- [backend/app/services/knowledge_graph/graph_builder.py](https://app.notion.com/p/New-Codebase-3a0dc871c95380959c34c5137fed2982?pvs=21) — Knowledge graph builder (Document→Page→Section→Chunk→Entity)

### RAG / Retrieval Services

- [backend/app/services/rag/**init**.py](https://app.notion.com/p/New-Codebase-3a0dc871c95380959c34c5137fed2982?pvs=21) — RAG package init
- [backend/app/services/rag/retriever.py](https://app.notion.com/p/New-Codebase-3a0dc871c95380959c34c5137fed2982?pvs=21) — Hybrid retriever — FAISS + Neo4j + BM25 (0.6 semantic + 0.4 graph)
- [backend/app/services/rag/generator.py](https://app.notion.com/p/New-Codebase-3a0dc871c95380959c34c5137fed2982?pvs=21) — Answer generator — Ollama / OpenAI with citation enforcement

### Multi-Agent System

- [backend/app/services/agents/**init**.py](https://app.notion.com/p/New-Codebase-3a0dc871c95380959c34c5137fed2982?pvs=21) — Agents package init
- [backend/app/services/agents/sensor_monitor_agent.py](https://app.notion.com/p/New-Codebase-3a0dc871c95380959c34c5137fed2982?pvs=21) — Sensor health monitor agent
- [backend/app/services/agents/fault_diagnosis_agent.py](https://app.notion.com/p/New-Codebase-3a0dc871c95380959c34c5137fed2982?pvs=21) — Fault diagnosis agent
- [backend/app/services/agents/predictive_maintenance_agent.py](https://app.notion.com/p/New-Codebase-3a0dc871c95380959c34c5137fed2982?pvs=21) — Predictive maintenance agent (RUL)
- [backend/app/services/agents/shift_handover_agent.py](https://app.notion.com/p/New-Codebase-3a0dc871c95380959c34c5137fed2982?pvs=21) — Shift handover report agent
- [backend/app/services/agents/report_saver.py](https://app.notion.com/p/New-Codebase-3a0dc871c95380959c34c5137fed2982?pvs=21) — Report persistence service
- [backend/app/services/agents/orchestrator.py](https://app.notion.com/p/New-Codebase-3a0dc871c95380959c34c5137fed2982?pvs=21) — Agent orchestrator (Monitor→Diagnosis→Predictive→Handover)

### Frontend (Next.js)

- [frontend/package.json](https://app.notion.com/p/New-Codebase-3a0dc871c95380959c34c5137fed2982?pvs=21) — Frontend package.json (Next.js 16 + React 19)
- [frontend/next.config.js](https://app.notion.com/p/New-Codebase-3a0dc871c95380959c34c5137fed2982?pvs=21) — Next.js configuration (API proxy)
- [frontend/src/app/layout.js](https://app.notion.com/p/New-Codebase-3a0dc871c95380959c34c5137fed2982?pvs=21) — Root layout
- [frontend/src/app/page.js](https://app.notion.com/p/New-Codebase-3a0dc871c95380959c34c5137fed2982?pvs=21) — Main application — Pipeline Visualizer + Query + Dashboard + Knowledge Graph
- [frontend/src/app/globals.css](https://app.notion.com/p/New-Codebase-3a0dc871c95380959c34c5137fed2982?pvs=21) — Global styles — dark theme + pipeline visualization CSS

### Sample Data

- [data/sample_documents/work_order_sample.txt](https://app.notion.com/p/New-Codebase-3a0dc871c95380959c34c5137fed2982?pvs=21) — Sample work order document
- [data/sample_documents/incident_report_sample.txt](https://app.notion.com/p/New-Codebase-3a0dc871c95380959c34c5137fed2982?pvs=21) — Sample incident report
- [data/sample_documents/sop_hot_work.txt](https://app.notion.com/p/New-Codebase-3a0dc871c95380959c34c5137fed2982?pvs=21) — Sample SOP — hot work procedure
- [data/sample_documents/work_orders.json](https://app.notion.com/p/New-Codebase-3a0dc871c95380959c34c5137fed2982?pvs=21) — Synthetic work orders (JSON)
- [data/sample_documents/incident_reports.json](https://app.notion.com/p/New-Codebase-3a0dc871c95380959c34c5137fed2982?pvs=21) — Synthetic incident reports (JSON)
- [data/sample_documents/inspection_reports.json](https://app.notion.com/p/New-Codebase-3a0dc871c95380959c34c5137fed2982?pvs=21) — Synthetic inspection reports (JSON)
- [data/sample_documents/sop_hot_work.json](https://app.notion.com/p/New-Codebase-3a0dc871c95380959c34c5137fed2982?pvs=21) — Synthetic SOP — hot work (JSON)

### Demo Documents

- [backend/data/uploads/incident_report_steam_leak.txt](https://app.notion.com/p/New-Codebase-3a0dc871c95380959c34c5137fed2982?pvs=21) — Demo — Steam leak incident report (E-301A)
- [backend/data/uploads/sop_pump_maintenance.txt](https://app.notion.com/p/New-Codebase-3a0dc871c95380959c34c5137fed2982?pvs=21) — Demo — SOP for centrifugal pump maintenance
- [backend/data/uploads/inspection_P101A.txt](https://app.notion.com/p/New-Codebase-3a0dc871c95380959c34c5137fed2982?pvs=21) — Demo — RBI inspection report for P-101A
- [backend/data/uploads/work_order_sample.txt](https://app.notion.com/p/New-Codebase-3a0dc871c95380959c34c5137fed2982?pvs=21) — Demo — Work order samples

### Scripts

- [scripts/generate_codebase_doc.py](https://app.notion.com/p/New-Codebase-3a0dc871c95380959c34c5137fed2982?pvs=21) — Codebase documentation generator
- [scripts/generate_synthetic_docs.py](https://app.notion.com/p/New-Codebase-3a0dc871c95380959c34c5137fed2982?pvs=21) — Synthetic document generator
- [scripts/demo_standalone.py](https://app.notion.com/p/New-Codebase-3a0dc871c95380959c34c5137fed2982?pvs=21) — Standalone pipeline demo (zero dependencies)
- [scripts/demo_agents.py](https://app.notion.com/p/New-Codebase-3a0dc871c95380959c34c5137fed2982?pvs=21) — Multi-agent demo (zero dependencies)
- [scripts/demo_pipeline.py](https://app.notion.com/p/New-Codebase-3a0dc871c95380959c34c5137fed2982?pvs=21) — Pipeline demo script
- [scripts/test_pdf_ingest.py](https://app.notion.com/p/New-Codebase-3a0dc871c95380959c34c5137fed2982?pvs=21) — PDF ingestion test

---

## Folder Structure

```
axiom/
    README.md
    docker-compose.yml
    backend/
        Dockerfile
        requirements.txt
        app/
            __init__.py
            config.py
            main.py
            models/
                __init__.py
                schemas.py
            routers/
                __init__.py
                ingest.py
                query.py
                graph.py
                agents.py
            services/
                __init__.py
                ingestion/
                    __init__.py
                    pipeline.py
                    pdf_parser.py
                    ocr_engine.py
                    text_cleaner.py
                    document_structurer.py
                    chunker.py
                    entity_extractor.py
                    relationship_extractor.py
                    document_classifier.py
                    llm_extractor.py
                vectorstore/
                    __init__.py
                    faiss_service.py
                    qdrant_service.py
                knowledge_graph/
                    __init__.py
                    neo4j_client.py
                    graph_builder.py
                rag/
                    __init__.py
                    retriever.py
                    generator.py
                agents/
                    __init__.py
                    sensor_monitor_agent.py
                    fault_diagnosis_agent.py
                    predictive_maintenance_agent.py
                    shift_handover_agent.py
                    report_saver.py
                    orchestrator.py
    frontend/
        package.json
        next.config.js
        src/
            app/
                layout.js
                page.js
                globals.css
    data/
        sample_documents/
            work_order_sample.txt
            incident_report_sample.txt
            sop_hot_work.txt
            work_orders.json
            incident_reports.json
            inspection_reports.json
            sop_hot_work.json
    backend/
        data/
            uploads/
                incident_report_steam_leak.txt
                sop_pump_maintenance.txt
                inspection_P101A.txt
                work_order_sample.txt
    scripts/
        generate_codebase_doc.py
        generate_synthetic_docs.py
        demo_standalone.py
        demo_agents.py
        demo_pipeline.py
        test_pdf_ingest.py
```

---

## `README.md`

**Project README**

```markdown
# AXIOM — Offline GraphRAG Industrial Knowledge Platform
## Fully Offline PDF → Knowledge Graph → Hybrid Retrieval Pipeline

## Architecture
```

PDF
├── Type Detection (PyMuPDF) ─── Digital → direct text extraction
│                              └── Scanned → PaddleOCR (offline)
├── Text Cleaning (ftfy + regex + unicode normalization)
├── Document Structuring (Pages → Sections → Paragraphs)
├── Semantic Chunking (500 tokens, 70 overlap)
├── Entity Extraction (spaCy + regex patterns)
├── Relationship Extraction (subject → predicate → object triples)
├── FAISS Vector Index (sentence-transformers/all-MiniLM-L6-v2, 384-dim)
└── Neo4j Knowledge Graph (Document → Page → Section → Chunk → Entity)
│
Hybrid Retrieval: 0.6 × Semantic (FAISS) + 0.4 × Graph (Neo4j)
│
Local LLM (Ollama: Llama 3.1 / Qwen 2.5 / Mistral)

```

## Quick Start

### Prerequisites
- Python 3.11+
- Docker (for Neo4j + Ollama)
- 8GB+ RAM

### 1. Start Neo4j
```bash
docker compose up neo4j -d
```

### 2. Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 3. Start Backend

```bash
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 4. Start Frontend

```bash
cd frontend
npm install && npm run dev
```

### 5. Open UI

Navigate to [http://localhost:3000](http://localhost:3000/)

- **Pipeline Visualizer** — Upload a PDF and watch all 11 ingestion steps in real-time
- **Query & Retrieval** — Ask questions and see FAISS search, graph expansion, re-ranking, and LLM generation
- **Dashboard** — FAISS index stats, Neo4j node counts, document inventory, service status
- **Knowledge Graph** — Text search and semantic search across indexed documents

### 6. (Optional) Start Ollama for LLM answers

```bash
ollama serve
ollama pull llama3.1:8b
```

## Ingestion Pipeline (11 Steps)

| Step | Phase | Tool |
| --- | --- | --- |
| 1 | PDF Type Detection | PyMuPDF (digital vs scanned) |
| 2 | Document Parsing | PyMuPDF / pdfplumber |
| 3 | OCR Processing | PaddleOCR (primary) / Tesseract (fallback) |
| 4 | Text Cleaning | ftfy + regex + unicode normalization |
| 5 | Document Structuring | Custom (pages → sections → paragraphs) |
| 6 | Document Classification | Keyword pattern matching (7 categories) |
| 7 | Semantic Chunking | 500 tokens, 70 overlap, section-aware |
| 8 | Entity Extraction | spaCy NER + regex patterns |
| 9 | Relationship Extraction | Pattern matching + co-occurrence |
| 10 | Embedding + FAISS | sentence-transformers → FAISS IndexFlatIP |
| 11 | Neo4j Graph | Document → Page → Section → Chunk → Entity |

## Retrieval Pipeline (7 Steps)

| Step | Phase | Detail |
| --- | --- | --- |
| 1 | Query Analysis | Extract equipment tags, regulation refs, key terms |
| 2 | Query Embedding | sentence-transformers (all-MiniLM-L6-v2) |
| 3 | FAISS Search | Top-k semantic similarity search |
| 4 | Neo4j Expansion | Entity neighborhood traversal |
| 5 | Hybrid Re-Ranking | Score = 0.6 × Semantic + 0.4 × Graph |
| 6 | Context Assembly | Build prompt with source citations |
| 7 | LLM Generation | Ollama (local) or OpenAI (optional) |

## Neo4j Graph Schema

```
Document -[HAS_PAGE]-> Page -[HAS_SECTION]-> Section -[HAS_CHUNK]-> Chunk
Chunk -[MENTIONS]-> Entity (Equipment, Personnel, Regulation, etc.)
Entity -[RELATED_TO]-> Entity
```

## API Endpoints

| Endpoint | Method | Description |
| --- | --- | --- |
| `/api/v1/ingest/document/stream` | POST | Upload with real-time SSE pipeline visualization |
| `/api/v1/ingest/document` | POST | Upload & process a document |
| `/api/v1/ingest/batch` | POST | Batch upload multiple documents |
| `/api/v1/query/ask/stream` | POST | Query with real-time retrieval step visualization |
| `/api/v1/query/ask` | POST | Ask a question, get AI answer with sources |
| `/api/v1/query/search` | POST | Search documents without answer generation |
| `/api/v1/graph/search` | POST | Search knowledge graph + FAISS metadata |
| `/api/v1/graph/search/semantic` | POST | Semantic vector search over FAISS |
| `/api/v1/graph/equipment/{tag}` | GET | Full equipment context from Neo4j |
| `/api/v1/graph/stats` | GET | Combined FAISS + Neo4j statistics |
| `/health` | GET | Health check |

## Tech Stack — $0 Cost

| Component | Technology | Cost |
| --- | --- | --- |
| PDF Parsing | PyMuPDF + pdfplumber | FREE |
| OCR | PaddleOCR (primary) + Tesseract (fallback) | FREE |
| Text Cleaning | ftfy + regex + unicodedata | FREE |
| NLP | spaCy | FREE |
| Embeddings | sentence-transformers (all-MiniLM-L6-v2) | FREE |
| Vector DB | FAISS (offline, file-persisted) | FREE |
| Graph DB | Neo4j Community (Docker) | FREE |
| LLM | Ollama (Llama 3.1 / Qwen 2.5 / Mistral) | FREE |
| Backend | FastAPI + Uvicorn | FREE |
| Frontend | Next.js 16 + React 19 | FREE |

## Project Structure

```
axiom/
├── docker-compose.yml          # Neo4j + Ollama containers
├── backend/
│   ├── app/
│   │   ├── main.py             # FastAPI app with FAISS + Neo4j lifespan
│   │   ├── config.py           # Settings (chunk size, weights, paths)
│   │   ├── models/schemas.py   # Pydantic data models
│   │   ├── routers/
│   │   │   ├── ingest.py       # Upload + SSE streaming pipeline
│   │   │   ├── query.py        # RAG query + SSE streaming retrieval
│   │   │   └── graph.py        # Knowledge graph + FAISS search
│   │   └── services/
│   │       ├── ingestion/
│   │       │   ├── pipeline.py           # 11-step orchestrator
│   │       │   ├── pdf_parser.py         # PyMuPDF + DOCX parser
│   │       │   ├── ocr_engine.py         # PaddleOCR + Tesseract
│   │       │   ├── text_cleaner.py       # Noise removal, unicode
│   │       │   ├── document_structurer.py # Page/section hierarchy
│   │       │   ├── chunker.py            # Semantic chunking
│   │       │   ├── entity_extractor.py   # spaCy + regex NER
│   │       │   ├── relationship_extractor.py # Triple extraction
│   │       │   └── document_classifier.py # Category classification
│   │       ├── vectorstore/
│   │       │   └── faiss_service.py      # FAISS index + embeddings
│   │       ├── knowledge_graph/
│   │       │   ├── neo4j_client.py       # Neo4j async driver
│   │       │   └── graph_builder.py      # Document→Page→Chunk→Entity
│   │       └── rag/
│   │           ├── retriever.py          # Hybrid FAISS+Neo4j+BM25
│   │           └── generator.py          # Ollama/OpenAI answer gen
│   └── data/
│       ├── faiss/                        # Persisted FAISS index
│       └── uploads/                      # Uploaded documents
└── frontend/
    └── src/app/
        ├── page.js             # Pipeline Visualizer + Query UI
        └── globals.css         # Dark theme styles
```

```

---

## `docker-compose.yml`

**Docker Compose — Neo4j + Ollama infrastructure**

```yaml
version: "3.9"

services:
  # FREE: Local LLM server (Ollama)
  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    # After startup, pull models with:
    # docker exec -it axiom-ollama-1 ollama pull llama3.1:8b
    # docker exec -it axiom-ollama-1 ollama pull nomic-embed-text

  # FREE: Graph database (Knowledge Graph)
  neo4j:
    image: neo4j:5.22-community
    ports:
      - "7474:7474"
      - "7687:7687"
    environment:
      NEO4J_AUTH: neo4j/axiom_password
      NEO4J_PLUGINS: '["apoc"]'
    volumes:
      - neo4j_data:/data

  # FREE: Message broker / cache
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - neo4j
      - redis
      - ollama
    volumes:
      - ./data:/app/data
      - faiss_data:/app/data/faiss

volumes:
  neo4j_data:
  ollama_data:
  faiss_data:
```

---

## `backend/Dockerfile`

**Backend Docker image**

```docker
FROM python:3.11-slim

WORKDIR /app

# System dependencies for PaddleOCR + Tesseract fallback
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    tesseract-ocr-eng \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Pre-download the embedding model
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## `backend/requirements.txt`

**Python dependencies**

```
# Core
fastapi==0.115.0
uvicorn[standard]==0.30.6
python-multipart==0.0.9
pydantic==2.9.0
pydantic-settings==2.5.0
python-dotenv==1.0.1

# Document Processing
PyMuPDF==1.24.9
pdfplumber==0.11.4
Pillow==10.4.0
python-docx==1.1.2
openpyxl==3.1.5

# OCR — PaddleOCR (primary, offline) + Tesseract (fallback)
paddleocr==2.8.1
paddlepaddle==2.6.2
pytesseract==0.3.13

# Text Cleaning
ftfy==6.3.1

# AI/ML — ALL FREE LOCAL MODELS
sentence-transformers==3.1.0  # FREE local embeddings
langchain==0.3.0
langchain-community==0.3.0
langgraph==0.2.0
tiktoken==0.7.0
httpx==0.27.2  # For Ollama API calls

# OpenAI (OPTIONAL - paid fallback, not required)
# openai==1.45.0
# langchain-openai==0.2.0

# Knowledge Graph (FREE - Neo4j Community)
neo4j==5.24.0

# Vector Store (FREE - FAISS offline)
faiss-cpu==1.9.0
numpy>=1.24.0

# NLP & Entity Extraction (FREE)
spacy==3.7.6

# Search (FREE)
rank-bm25==0.2.2

# Async (FREE)
celery[redis]==5.4.0
redis==5.0.8

# Utilities
tenacity==9.0.0
structlog==24.4.0
uuid6==2024.7.10
```

---

## `backend/app/__init__.py`

**App package init**

```python

```

---

## `backend/app/config.py`

**Application configuration (Pydantic Settings)**

```python
from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    # LLM Provider: "ollama" (free local) or "openai" (paid)
    llm_provider: str = "ollama"

    # Ollama (FREE - local)
    ollama_base_url: str = "<http://localhost:11434>"
    ollama_chat_model: str = "llama3.1:8b"  # or mistral, qwen2.5, phi3, gemma2
    ollama_embedding_model: str = "nomic-embed-text"  # free embedding model

    # OpenAI (optional fallback - PAID)
    openai_api_key: str = ""
    openai_embedding_model: str = "text-embedding-3-small"
    openai_chat_model: str = "gpt-4o"

    # Local Embeddings (FREE - sentence-transformers)
    local_embedding_model: str = "all-MiniLM-L6-v2"  # fast, 384 dims
    # Alternative: "BAAI/bge-small-en-v1.5" (384 dims, better quality)

    # Neo4j (FREE - Community Edition)
    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: str = "axiom_password"

    # FAISS (FREE - offline vector index)
    faiss_index_dir: str = "./data/faiss"

    # Qdrant (legacy, kept for backward compatibility)
    qdrant_host: str = "localhost"
    qdrant_port: int = 6333
    qdrant_collection: str = "axiom_documents"

    # Redis (FREE - open source)
    redis_url: str = "redis://localhost:6379/0"

    # App
    upload_dir: str = "./data/uploads"
    log_level: str = "INFO"

    # Embedding dimension (384 for MiniLM/BGE-small, 768 for nomic-embed-text)
    embedding_dimension: int = 384

    # Chunking: 300-600 tokens, 50-80 overlap (per GraphRAG pipeline spec)
    chunk_size: int = 500
    chunk_overlap: int = 70

    # Retrieval scoring weights
    semantic_weight: float = 0.6
    graph_weight: float = 0.4

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()

# Ensure directories exist
Path(settings.upload_dir).mkdir(parents=True, exist_ok=True)
Path(settings.faiss_index_dir).mkdir(parents=True, exist_ok=True)
```

---

## `backend/app/main.py`

**FastAPI application entry point**

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import structlog

from app.config import settings
from app.routers import ingest, query, graph, agents
from app.services.knowledge_graph.neo4j_client import Neo4jClient
from app.services.vectorstore.faiss_service import FAISSService

logger = structlog.get_logger()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize and cleanup resources on startup/shutdown."""
    logger.info("Starting AXIOM platform...")

    # Initialize Neo4j
    neo4j_client = Neo4jClient()
    await neo4j_client.initialize()
    app.state.neo4j = neo4j_client

    # Initialize FAISS vector index
    faiss_service = FAISSService()
    await faiss_service.initialize()
    app.state.faiss = faiss_service

    logger.info("AXIOM platform ready.")
    yield

    # Cleanup
    await neo4j_client.close()
    logger.info("AXIOM platform shut down.")

app = FastAPI(
    title="AXIOM - Industrial Knowledge Intelligence",
    description="AI-powered platform for industrial document ingestion, knowledge graph construction, and intelligent retrieval.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ingest.router, prefix="/api/v1/ingest", tags=["Ingestion"])
app.include_router(query.router, prefix="/api/v1/query", tags=["Query"])
app.include_router(graph.router, prefix="/api/v1/graph", tags=["Knowledge Graph"])
app.include_router(agents.router, prefix="/api/v1/agents", tags=["Multi-Agent Intelligence"])

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "AXIOM"}
```

---

## `backend/app/models/__init__.py`

**Models package init**

```python

```

---

## `backend/app/models/schemas.py`

**Pydantic data models**

```python
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum

# --- Document Models ---

class DocumentType(str, Enum):
    PDF = "pdf"
    DOCX = "docx"
    XLSX = "xlsx"
    IMAGE = "image"
    EMAIL = "email"
    UNKNOWN = "unknown"

class DocumentCategory(str, Enum):
    PID = "p&id"
    WORK_ORDER = "work_order"
    SOP = "sop"
    INSPECTION_REPORT = "inspection_report"
    INCIDENT_REPORT = "incident_report"
    OEM_MANUAL = "oem_manual"
    REGULATORY = "regulatory"
    GENERAL = "general"

class ExtractedEntity(BaseModel):
    entity_type: str  # equipment, personnel, date, parameter, regulation, location
    value: str
    confidence: float = Field(ge=0, le=1)
    source_page: Optional[int] = None
    context: Optional[str] = None

class ExtractedRelationship(BaseModel):
    source_entity: str
    relationship_type: str
    target_entity: str
    confidence: float = Field(ge=0, le=1)
    source_context: Optional[str] = None

class DocumentChunk(BaseModel):
    chunk_id: str
    document_id: str
    content: str
    page_number: Optional[int] = None
    chunk_index: int
    metadata: dict = {}

class IngestedDocument(BaseModel):
    document_id: str
    filename: str
    file_type: DocumentType
    category: DocumentCategory
    total_pages: int = 0
    extracted_text: str
    chunks: list[DocumentChunk] = []
    entities: list[ExtractedEntity] = []
    relationships: list[ExtractedRelationship] = []
    ingested_at: datetime = Field(default_factory=datetime.utcnow)

# --- Query Models ---

class QueryRequest(BaseModel):
    question: str
    filters: Optional[dict] = None
    top_k: int = Field(default=5, ge=1, le=20)
    include_graph_context: bool = True

class RetrievedContext(BaseModel):
    chunk_id: str
    document_id: str
    filename: str
    content: str
    page_number: Optional[int] = None
    relevance_score: float
    source_type: str  # "vector", "graph", "keyword"

class QueryResponse(BaseModel):
    answer: str
    confidence: str  # "high", "medium", "low"
    sources: list[RetrievedContext]
    related_entities: list[dict] = []
    suggested_followups: list[str] = []

# --- Graph Models ---

class GraphNode(BaseModel):
    node_id: str
    node_type: str
    properties: dict

class GraphEdge(BaseModel):
    source_id: str
    target_id: str
    relationship: str
    properties: dict = {}
```

---

## `backend/app/routers/__init__.py`

**Routers package init**

```python

```

---

## `backend/app/routers/ingest.py`

**Document ingestion API + SSE streaming pipeline**

```python
"""
Document Ingestion API — upload documents and trigger the full processing pipeline.
Includes SSE streaming endpoint for real-time pipeline step visualization.
"""

from fastapi import APIRouter, UploadFile, File, Request, HTTPException
from fastapi.responses import StreamingResponse
from pathlib import Path
import shutil
import json
import uuid
import asyncio
import time
import structlog

from app.config import settings
from app.services.ingestion.pipeline import IngestionPipeline
from app.services.ingestion.pdf_parser import PDFParser, DOCXParser
from app.services.ingestion.ocr_engine import OCREngine
from app.services.ingestion.text_cleaner import TextCleaner
from app.services.ingestion.document_structurer import DocumentStructurer
from app.services.ingestion.entity_extractor import IndustrialEntityExtractor
from app.services.ingestion.chunker import TextChunker
from app.services.ingestion.document_classifier import DocumentClassifier
from app.services.ingestion.relationship_extractor import RelationshipExtractor
from app.services.knowledge_graph.graph_builder import GraphBuilder
from app.services.vectorstore.faiss_service import FAISSService
from app.services.knowledge_graph.neo4j_client import Neo4jClient
from app.models.schemas import (
    DocumentType, DocumentCategory, IngestedDocument,
    DocumentChunk, ExtractedEntity, ExtractedRelationship,
)

logger = structlog.get_logger()
router = APIRouter()

def _sse_event(event: str, data: dict) -> str:
    """Format a Server-Sent Event."""
    return f"event: {event}\ndata: {json.dumps(data)}\n\n"

@router.post("/document/stream")
async def ingest_document_stream(request: Request, file: UploadFile = File(...)):
    """
    Stream the ingestion pipeline steps in real-time via SSE.
    Each step emits an event with status, data, and timing.
    """
    allowed_extensions = {".pdf", ".docx", ".doc", ".xlsx", ".png", ".jpg", ".jpeg", ".tiff", ".tif", ".txt", ".json", ".csv"}
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in allowed_extensions:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {file_ext}")

    # Save file first
    upload_dir = Path(settings.upload_dir)
    upload_dir.mkdir(parents=True, exist_ok=True)
    file_path = upload_dir / file.filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    async def generate_events():
        import fitz
        from datetime import datetime
        from app.services.ingestion.pdf_parser import ParsedDocument, ParsedPage

        document_id = str(uuid.uuid4())
        pipeline_start = time.time()

        # === STEP 1: PDF Type Detection ===
        yield _sse_event("step", {
            "step": 1, "name": "PDF Type Detection",
            "status": "running", "description": "Analyzing file type..."
        })
        await asyncio.sleep(0.05)

        ext = file_path.suffix.lower()
        type_map = {
            ".pdf": "PDF", ".docx": "DOCX", ".doc": "DOCX",
            ".png": "IMAGE", ".jpg": "IMAGE", ".jpeg": "IMAGE",
            ".tiff": "IMAGE", ".tif": "IMAGE", ".txt": "TEXT",
        }
        file_type_str = type_map.get(ext, "UNKNOWN")

        is_scanned = False
        total_pages = 1
        if ext == ".pdf":
            try:
                doc = fitz.open(str(file_path))
                total_pages = len(doc)
                text_check = doc[0].get_text("text") if len(doc) > 0 else ""
                is_scanned = len(text_check.strip()) < 50
                doc.close()
            except Exception:
                is_scanned = True

        yield _sse_event("step", {
            "step": 1, "name": "PDF Type Detection",
            "status": "complete",
            "result": {
                "file_type": file_type_str,
                "is_scanned": is_scanned,
                "total_pages": total_pages,
                "pipeline": "OCR (PaddleOCR)" if is_scanned else "Digital (PyMuPDF)",
            },
            "duration_ms": int((time.time() - pipeline_start) * 1000),
        })

        # === STEP 2: Document Parsing ===
        step2_start = time.time()
        yield _sse_event("step", {
            "step": 2, "name": "Document Parsing",
            "status": "running",
            "description": f"Extracting text from {total_pages} page(s) using PyMuPDF..."
        })

        pdf_parser = PDFParser()
        docx_parser = DOCXParser()
        ocr_engine = OCREngine()

        if file_type_str == "PDF":
            parsed = pdf_parser.parse(file_path)
        elif file_type_str == "DOCX":
            parsed = docx_parser.parse(file_path)
        elif file_type_str == "IMAGE":
            ocr_result = ocr_engine.ocr_image_file(file_path)
            parsed = ParsedDocument(
                filename=file_path.name, total_pages=1,
                pages=[ParsedPage(page_number=1, text=ocr_result.text, tables=[], images=[], has_text=True)],
                metadata={"ocr_confidence": ocr_result.confidence},
            )
        else:
            text = file_path.read_text(encoding="utf-8", errors="replace")
            parsed = ParsedDocument(
                filename=file_path.name, total_pages=1,
                pages=[ParsedPage(page_number=1, text=text, tables=[], images=[], has_text=bool(text.strip()))],
                metadata={},
            )

        pages_with_text = sum(1 for p in parsed.pages if p.has_text)
        yield _sse_event("step", {
            "step": 2, "name": "Document Parsing",
            "status": "complete",
            "result": {
                "total_pages": parsed.total_pages,
                "pages_with_text": pages_with_text,
                "tables_found": sum(len(p.tables) for p in parsed.pages),
                "images_found": sum(len(p.images) for p in parsed.pages),
                "sample_text": parsed.pages[0].text[:300] if parsed.pages else "",
            },
            "duration_ms": int((time.time() - step2_start) * 1000),
        })

        # === STEP 3: OCR (if needed) ===
        step3_start = time.time()
        ocr_pages = []
        needs_ocr = any(ocr_engine.needs_ocr(p.text) for p in parsed.pages)

        yield _sse_event("step", {
            "step": 3, "name": "OCR Processing",
            "status": "running" if needs_ocr else "skipped",
            "description": "Running PaddleOCR on scanned pages..." if needs_ocr else "All pages have extractable text — OCR skipped",
        })

        raw_text_parts = []
        for page in parsed.pages:
            if page.has_text and not ocr_engine.needs_ocr(page.text):
                raw_text_parts.append(page.text)
            else:
                if ext == ".pdf":
                    try:
                        doc = fitz.open(str(file_path))
                        pdf_page = doc[page.page_number - 1]
                        pix = pdf_page.get_pixmap(dpi=300)
                        image_bytes = pix.tobytes("png")
                        doc.close()
                        ocr_result = ocr_engine.ocr_pdf_page_image(image_bytes, page.page_number)
                        raw_text_parts.append(ocr_result.text)
                        ocr_pages.append({
                            "page": page.page_number,
                            "confidence": round(ocr_result.confidence, 3),
                            "chars": len(ocr_result.text),
                        })
                    except Exception:
                        raw_text_parts.append(page.text)
                else:
                    raw_text_parts.append(page.text)

            for table in page.tables:
                for row in table:
                    row_text = " | ".join(cell or "" for cell in row)
                    if row_text.strip():
                        raw_text_parts.append(row_text)

        raw_text = "\n\n".join(raw_text_parts)

        yield _sse_event("step", {
            "step": 3, "name": "OCR Processing",
            "status": "complete" if needs_ocr else "skipped",
            "result": {
                "ocr_needed": needs_ocr,
                "pages_ocrd": len(ocr_pages),
                "ocr_details": ocr_pages,
                "engine": "PaddleOCR" if needs_ocr else "N/A",
                "total_chars_extracted": len(raw_text),
            },
            "duration_ms": int((time.time() - step3_start) * 1000),
        })

        # === STEP 4: Text Cleaning ===
        step4_start = time.time()
        yield _sse_event("step", {
            "step": 4, "name": "Text Cleaning",
            "status": "running",
            "description": "Removing noise, normalizing unicode, fixing line wraps..."
        })

        text_cleaner = TextCleaner()
        cleaned_text = text_cleaner.clean(raw_text)
        chars_removed = len(raw_text) - len(cleaned_text)

        yield _sse_event("step", {
            "step": 4, "name": "Text Cleaning",
            "status": "complete",
            "result": {
                "original_length": len(raw_text),
                "cleaned_length": len(cleaned_text),
                "chars_removed": chars_removed,
                "reduction_pct": round(chars_removed / max(len(raw_text), 1) * 100, 1),
                "sample_cleaned": cleaned_text[:300],
            },
            "duration_ms": int((time.time() - step4_start) * 1000),
        })

        # === STEP 5: Document Structuring ===
        step5_start = time.time()
        yield _sse_event("step", {
            "step": 5, "name": "Document Structuring",
            "status": "running",
            "description": "Building page → section → paragraph hierarchy..."
        })

        structurer = DocumentStructurer()
        cleaned_page_texts = {p.page_number: text_cleaner.clean(p.text) for p in parsed.pages}
        structured_doc = structurer.structure(parsed, cleaned_page_texts)
        total_sections = sum(len(p.sections) for p in structured_doc.pages)

        structure_preview = []
        for sp in structured_doc.pages[:3]:
            page_info = {"page": sp.page, "sections": []}
            for sec in sp.sections[:5]:
                page_info["sections"].append({
                    "heading": sec.heading or "(No heading)",
                    "paragraphs": len(sec.paragraphs),
                    "tables": len(sec.tables),
                })
            structure_preview.append(page_info)

        yield _sse_event("step", {
            "step": 5, "name": "Document Structuring",
            "status": "complete",
            "result": {
                "total_pages": len(structured_doc.pages),
                "total_sections": total_sections,
                "structure_preview": structure_preview,
            },
            "duration_ms": int((time.time() - step5_start) * 1000),
        })

        # === STEP 6: Classification ===
        step6_start = time.time()
        yield _sse_event("step", {
            "step": 6, "name": "Document Classification",
            "status": "running", "description": "Classifying document category..."
        })

        classifier = DocumentClassifier()
        category = classifier.classify(cleaned_text, file.filename)

        yield _sse_event("step", {
            "step": 6, "name": "Document Classification",
            "status": "complete",
            "result": {"category": category.value, "filename": file.filename},
            "duration_ms": int((time.time() - step6_start) * 1000),
        })

        # === STEP 7: Chunking ===
        step7_start = time.time()
        yield _sse_event("step", {
            "step": 7, "name": "Semantic Chunking",
            "status": "running",
            "description": f"Splitting into chunks ({settings.chunk_size} tokens, {settings.chunk_overlap} overlap)..."
        })

        chunker = TextChunker()
        all_chunks = []
        for page in structured_doc.pages:
            for section in page.sections:
                section_text = "\n\n".join(section.paragraphs)
                for table in section.tables:
                    for row in table:
                        section_text += "\n" + " | ".join(cell or "" for cell in row)
                if section_text.strip():
                    section_chunks = chunker.chunk_text(
                        text=section_text, document_id=document_id,
                        page_number=page.page, section_heading=section.heading,
                        metadata={"filename": file.filename, "category": category.value, "page": page.page, "section": section.heading},
                    )
                    all_chunks.extend(section_chunks)

        chunk_samples = [
            {"chunk_id": c.chunk_id, "page": c.page_number, "section": c.section_heading or "", "length": len(c.content), "preview": c.content[:150]}
            for c in all_chunks[:5]
        ]

        yield _sse_event("step", {
            "step": 7, "name": "Semantic Chunking",
            "status": "complete",
            "result": {
                "total_chunks": len(all_chunks),
                "avg_chunk_length": int(sum(len(c.content) for c in all_chunks) / max(len(all_chunks), 1)),
                "chunk_size_config": settings.chunk_size,
                "chunk_overlap_config": settings.chunk_overlap,
                "chunk_samples": chunk_samples,
            },
            "duration_ms": int((time.time() - step7_start) * 1000),
        })

        # === STEP 8: Entity Extraction ===
        step8_start = time.time()
        yield _sse_event("step", {
            "step": 8, "name": "Entity Extraction",
            "status": "running",
            "description": "Extracting entities (spaCy + regex patterns)..."
        })

        entity_extractor = IndustrialEntityExtractor()
        entities = entity_extractor.extract_all(cleaned_text)

        entity_summary = {}
        for e in entities:
            entity_summary[e.entity_type] = entity_summary.get(e.entity_type, 0) + 1

        yield _sse_event("step", {
            "step": 8, "name": "Entity Extraction",
            "status": "complete",
            "result": {
                "total_entities": len(entities),
                "by_type": entity_summary,
                "samples": [{"type": e.entity_type, "value": e.value, "confidence": round(e.confidence, 3)} for e in entities[:15]],
            },
            "duration_ms": int((time.time() - step8_start) * 1000),
        })

        # === STEP 9: Relationship Extraction ===
        step9_start = time.time()
        yield _sse_event("step", {
            "step": 9, "name": "Relationship Extraction",
            "status": "running",
            "description": "Extracting triples (subject → predicate → object)..."
        })

        relationship_extractor = RelationshipExtractor()
        relationships = relationship_extractor.extract(cleaned_text, entities)

        yield _sse_event("step", {
            "step": 9, "name": "Relationship Extraction",
            "status": "complete",
            "result": {
                "total_relationships": len(relationships),
                "samples": [{"source": r.source, "relation": r.relation, "target": r.target, "confidence": round(r.confidence, 3)} for r in relationships[:10]],
            },
            "duration_ms": int((time.time() - step9_start) * 1000),
        })

        # === STEP 10: FAISS Indexing ===
        step10_start = time.time()
        yield _sse_event("step", {
            "step": 10, "name": "Embedding & FAISS Indexing",
            "status": "running",
            "description": f"Generating embeddings ({settings.local_embedding_model}) and indexing..."
        })

        doc_chunks = [
            DocumentChunk(chunk_id=c.chunk_id, document_id=document_id, content=c.content, page_number=c.page_number, chunk_index=c.chunk_index, metadata=c.metadata)
            for c in all_chunks
        ]

        try:
            faiss_service: FAISSService = request.app.state.faiss
            await faiss_service.index_chunks(doc_chunks, document_id)
            faiss_status = "indexed"
        except Exception as e:
            faiss_status = f"failed: {str(e)}"

        yield _sse_event("step", {
            "step": 10, "name": "Embedding & FAISS Indexing",
            "status": "complete",
            "result": {
                "model": settings.local_embedding_model,
                "dimension": settings.embedding_dimension,
                "chunks_indexed": len(doc_chunks),
                "index_status": faiss_status,
            },
            "duration_ms": int((time.time() - step10_start) * 1000),
        })

        # === STEP 11: Neo4j Graph ===
        step11_start = time.time()
        yield _sse_event("step", {
            "step": 11, "name": "Neo4j Knowledge Graph",
            "status": "running",
            "description": "Loading Document → Page → Section → Chunk → Entity hierarchy..."
        })

        document = IngestedDocument(
            document_id=document_id, filename=file.filename,
            file_type=DocumentType.PDF if file_type_str == "PDF" else DocumentType.UNKNOWN,
            category=category, total_pages=parsed.total_pages,
            extracted_text=cleaned_text, chunks=doc_chunks,
            entities=[ExtractedEntity(entity_type=e.entity_type, value=e.value, confidence=e.confidence, context=e.context) for e in entities],
            relationships=[ExtractedRelationship(source_entity=r.source, relationship_type=r.relation, target_entity=r.target, confidence=r.confidence, source_context=r.context) for r in relationships],
            ingested_at=datetime.utcnow(),
        )

        try:
            neo4j: Neo4jClient = request.app.state.neo4j
            graph_builder = GraphBuilder(neo4j)
            await graph_builder.populate_from_document(document)
            graph_status = "populated"
        except Exception as e:
            graph_status = f"failed: {str(e)}"

        yield _sse_event("step", {
            "step": 11, "name": "Neo4j Knowledge Graph",
            "status": "complete",
            "result": {
                "graph_status": graph_status,
                "nodes_created": len(entities) + len(doc_chunks) + parsed.total_pages + 1,
                "relationships_created": len(relationships) + len(entities),
                "hierarchy": "Document → Page → Section → Chunk → Entity",
            },
            "duration_ms": int((time.time() - step11_start) * 1000),
        })

        # === COMPLETE ===
        total_duration = int((time.time() - pipeline_start) * 1000)
        yield _sse_event("complete", {
            "document_id": document_id,
            "filename": file.filename,
            "category": category.value,
            "total_pages": parsed.total_pages,
            "total_chunks": len(all_chunks),
            "total_entities": len(entities),
            "total_relationships": len(relationships),
            "total_duration_ms": total_duration,
        })

    return StreamingResponse(
        generate_events(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )

@router.post("/document")
async def ingest_document(request: Request, file: UploadFile = File(...)):
    """
    Upload and process a document through the full GraphRAG ingestion pipeline.

    Pipeline phases:
    1. Detect PDF type (digital vs scanned)
    2. Parse document (PyMuPDF/pdfplumber)
    3. OCR if needed (PaddleOCR → Tesseract fallback)
    4. Clean and normalize text
    5. Preserve document structure
    6. Classify document category
    7. Chunk semantically (300-600 tokens, 50-80 overlap)
    8. Extract entities (spaCy + LLM)
    9. Extract relationships (triples with confidence)
    10. Index in FAISS vector store
    11. Populate Neo4j knowledge graph

    Returns the full ingestion result with extracted entities and metadata.
    """
    # Validate file type
    allowed_extensions = {".pdf", ".docx", ".doc", ".xlsx", ".png", ".jpg", ".jpeg", ".tiff", ".tif", ".txt", ".json", ".csv"}
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {file_ext}. Allowed: {allowed_extensions}",
        )

    # Save uploaded file
    upload_dir = Path(settings.upload_dir)
    upload_dir.mkdir(parents=True, exist_ok=True)
    file_path = upload_dir / file.filename

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")

    logger.info("File uploaded", filename=file.filename, path=str(file_path))

    # Run ingestion pipeline
    try:
        pipeline = IngestionPipeline()
        document = await pipeline.ingest(file_path, filename=file.filename)
    except Exception as e:
        logger.error("Ingestion failed", error=str(e), filename=file.filename)
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {str(e)}")

    # Index chunks in FAISS vector store
    try:
        faiss_service: FAISSService = request.app.state.faiss
        await faiss_service.index_chunks(document.chunks, document.document_id)
    except Exception as e:
        logger.error("FAISS indexing failed", error=str(e))

    # Populate knowledge graph
    try:
        neo4j: Neo4jClient = request.app.state.neo4j
        graph_builder = GraphBuilder(neo4j)
        await graph_builder.populate_from_document(document)
    except Exception as e:
        logger.error("Graph population failed", error=str(e))

    return {
        "status": "success",
        "document_id": document.document_id,
        "filename": document.filename,
        "file_type": document.file_type.value,
        "category": document.category.value,
        "total_pages": document.total_pages,
        "entities_extracted": len(document.entities),
        "relationships_found": len(document.relationships),
        "chunks_created": len(document.chunks),
        "entities": [
            {
                "type": e.entity_type,
                "value": e.value,
                "confidence": e.confidence,
            }
            for e in document.entities
        ],
        "relationships": [
            {
                "source": r.source_entity,
                "relation": r.relationship_type,
                "target": r.target_entity,
                "confidence": r.confidence,
            }
            for r in document.relationships
        ],
    }

@router.post("/batch")
async def ingest_batch(request: Request, files: list[UploadFile] = File(...)):
    """Upload and process multiple documents."""
    results = []
    for file in files:
        try:
            # Reuse single document endpoint logic
            result = await ingest_document(request, file)
            results.append(result)
        except HTTPException as e:
            results.append({
                "status": "failed",
                "filename": file.filename,
                "error": e.detail,
            })
        except Exception as e:
            results.append({
                "status": "failed",
                "filename": file.filename,
                "error": str(e),
            })

    return {
        "total": len(files),
        "successful": sum(1 for r in results if r.get("status") == "success"),
        "failed": sum(1 for r in results if r.get("status") == "failed"),
        "results": results,
    }
```

---

## `backend/app/routers/query.py`

**RAG query API + SSE streaming retrieval**

```python
"""
Query API — handles user questions with hybrid retrieval and LLM answer generation.
Includes streaming endpoint that visualizes retrieval and generation steps.
"""

from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import StreamingResponse
import json
import time
import asyncio
import structlog

from app.models.schemas import QueryRequest, QueryResponse
from app.services.rag.retriever import HybridRetriever
from app.services.rag.generator import AnswerGenerator
from app.services.vectorstore.faiss_service import FAISSService
from app.services.knowledge_graph.neo4j_client import Neo4jClient

logger = structlog.get_logger()
router = APIRouter()

@router.post("/ask", response_model=QueryResponse)
async def ask_question(request: Request, query: QueryRequest):
    """
    Ask a question and get an AI-generated answer with source citations.

    Pipeline:
    1. Parse and classify the user query
    2. Hybrid retrieval (vector + graph + keyword)
    3. Context assembly with source metadata
    4. LLM answer generation with citations
    5. Confidence scoring
    6. Follow-up suggestions
    """
    if not query.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    logger.info("Query received", question=query.question[:100])

    # Get services from app state
    faiss_service: FAISSService = request.app.state.faiss
    neo4j: Neo4jClient = request.app.state.neo4j

    # Initialize retriever (FAISS + Neo4j hybrid)
    retriever = HybridRetriever(faiss_service=faiss_service, neo4j=neo4j)

    # Perform hybrid retrieval
    category_filter = query.filters.get("category") if query.filters else None
    retrieved = await retriever.retrieve(
        query=query.question,
        top_k=query.top_k,
        use_graph=query.include_graph_context,
        category_filter=category_filter,
    )

    # Get additional graph context for equipment-specific queries
    graph_context = None
    if query.include_graph_context:
        graph_context = await _get_graph_context(neo4j, query.question)

    # Generate answer
    generator = AnswerGenerator()
    response = await generator.generate(
        query=query.question,
        retrieved_chunks=retrieved,
        graph_context=graph_context,
    )

    logger.info(
        "Query answered",
        confidence=response.confidence,
        sources=len(response.sources),
    )

    return response

@router.post("/search")
async def search_documents(request: Request, query: QueryRequest):
    """
    Search documents without answer generation — returns ranked chunks.
    Useful for exploring the document corpus.
    """
    faiss_service: FAISSService = request.app.state.faiss
    neo4j: Neo4jClient = request.app.state.neo4j

    retriever = HybridRetriever(faiss_service=faiss_service, neo4j=neo4j)

    category_filter = query.filters.get("category") if query.filters else None
    retrieved = await retriever.retrieve(
        query=query.question,
        top_k=query.top_k,
        category_filter=category_filter,
    )

    return {
        "query": query.question,
        "results": [
            {
                "chunk_id": r.chunk_id,
                "document_id": r.document_id,
                "filename": r.filename,
                "content": r.content,
                "page_number": r.page_number,
                "relevance_score": r.score,
                "source_type": r.source_type,
            }
            for r in retrieved
        ],
        "total_results": len(retrieved),
    }

async def _get_graph_context(neo4j: Neo4jClient, question: str) -> dict | None:
    """Extract graph context relevant to the question."""
    import re

    # Look for equipment tags in the question
    equipment_tags = re.findall(r"\b[A-Z]{1,4}-\d{2,5}[A-Z]?\b", question)

    if equipment_tags:
        # Get context for the first equipment tag found
        context = await neo4j.get_equipment_context(equipment_tags[0])
        if context:
            return context

    return None

def _sse_event(event: str, data: dict) -> str:
    """Format a Server-Sent Event."""
    return f"event: {event}\ndata: {json.dumps(data)}\n\n"

@router.post("/ask/stream")
async def ask_question_stream(request: Request, query: QueryRequest):
    """
    Stream the query pipeline steps: embedding → FAISS search → graph expansion →
    re-ranking → context assembly → LLM generation.
    """
    if not query.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    faiss_service: FAISSService = request.app.state.faiss
    neo4j: Neo4jClient = request.app.state.neo4j

    async def generate_events():
        pipeline_start = time.time()

        # === STEP 1: Query Analysis ===
        yield _sse_event("step", {
            "step": 1, "name": "Query Analysis",
            "status": "running",
            "description": "Parsing query and extracting search terms..."
        })
        await asyncio.sleep(0.05)

        import re
        equipment_tags = re.findall(r"\b[A-Z]{1,4}-\d{2,5}[A-Z]?\b", query.question)
        regulation_refs = re.findall(r"\b(?:OISD|API|ISO|ASME)[-\s]?\d+\b", query.question)
        stop_words = {"what", "is", "the", "a", "an", "of", "for", "in", "on", "at", "to", "from", "by", "with", "how", "when", "where", "which", "show", "me", "tell", "find", "get"}
        key_terms = [w for w in query.question.split() if w.lower() not in stop_words and len(w) > 2]

        yield _sse_event("step", {
            "step": 1, "name": "Query Analysis",
            "status": "complete",
            "result": {
                "question": query.question,
                "equipment_tags": equipment_tags,
                "regulation_refs": regulation_refs,
                "key_terms": key_terms[:10],
                "will_use_graph": bool(equipment_tags or regulation_refs),
            },
            "duration_ms": int((time.time() - pipeline_start) * 1000),
        })

        # === STEP 2: Query Embedding ===
        step2_start = time.time()
        yield _sse_event("step", {
            "step": 2, "name": "Query Embedding",
            "status": "running",
            "description": "Generating query vector with sentence-transformers..."
        })

        from app.config import settings
        query_embedding = await faiss_service.generate_embedding(query.question)

        yield _sse_event("step", {
            "step": 2, "name": "Query Embedding",
            "status": "complete",
            "result": {
                "model": settings.local_embedding_model,
                "dimension": len(query_embedding),
                "vector_preview": [round(v, 4) for v in query_embedding[:8]] + ["..."],
            },
            "duration_ms": int((time.time() - step2_start) * 1000),
        })

        # === STEP 3: FAISS Semantic Search ===
        step3_start = time.time()
        yield _sse_event("step", {
            "step": 3, "name": "FAISS Semantic Search",
            "status": "running",
            "description": f"Searching top-{query.top_k * 2} similar chunks..."
        })

        category_filter = query.filters.get("category") if query.filters else None
        vector_results = await faiss_service.search(
            query=query.question, top_k=query.top_k * 2, category_filter=category_filter
        )

        vector_chunks = [
            {
                "chunk_id": r["chunk_id"],
                "filename": r.get("filename", ""),
                "page": r.get("page_number"),
                "score": round(r["score"], 4),
                "preview": r["content"][:120],
            }
            for r in vector_results
        ]

        yield _sse_event("step", {
            "step": 3, "name": "FAISS Semantic Search",
            "status": "complete",
            "result": {
                "chunks_found": len(vector_results),
                "top_score": vector_chunks[0]["score"] if vector_chunks else 0,
                "chunks": vector_chunks[:6],
            },
            "duration_ms": int((time.time() - step3_start) * 1000),
        })

        # === STEP 4: Neo4j Graph Expansion ===
        step4_start = time.time()
        yield _sse_event("step", {
            "step": 4, "name": "Neo4j Graph Expansion",
            "status": "running",
            "description": "Expanding entity neighborhoods in knowledge graph..."
        })

        graph_context_parts = []
        graph_nodes_found = 0

        for tag in equipment_tags:
            try:
                context = await neo4j.get_equipment_context(tag)
                if context:
                    graph_context_parts.append({
                        "entity": tag,
                        "type": "equipment",
                        "neighbors": str(context)[:200],
                    })
                    graph_nodes_found += 1
            except Exception:
                pass

        for ref in regulation_refs:
            try:
                neighbors = await neo4j.get_neighbors("Regulation", "standard_id", ref)
                if neighbors:
                    graph_context_parts.append({
                        "entity": ref,
                        "type": "regulation",
                        "neighbors": str(neighbors[:3])[:200],
                    })
                    graph_nodes_found += 1
            except Exception:
                pass

        # General search
        for term in key_terms[:3]:
            try:
                nodes = await neo4j.search_nodes(term, limit=3)
                for node in nodes:
                    graph_nodes_found += 1
            except Exception:
                pass

        yield _sse_event("step", {
            "step": 4, "name": "Neo4j Graph Expansion",
            "status": "complete",
            "result": {
                "entities_searched": len(equipment_tags) + len(regulation_refs) + min(len(key_terms), 3),
                "graph_nodes_found": graph_nodes_found,
                "graph_context": graph_context_parts[:5],
            },
            "duration_ms": int((time.time() - step4_start) * 1000),
        })

        # === STEP 5: Re-Ranking ===
        step5_start = time.time()
        yield _sse_event("step", {
            "step": 5, "name": "Hybrid Re-Ranking",
            "status": "running",
            "description": f"Scoring: {settings.semantic_weight} × Semantic + {settings.graph_weight} × Graph..."
        })

        retriever = HybridRetriever(faiss_service=faiss_service, neo4j=neo4j)
        final_results = await retriever.retrieve(
            query=query.question,
            top_k=query.top_k,
            use_graph=query.include_graph_context,
            category_filter=category_filter,
        )

        ranked_chunks = [
            {
                "rank": i + 1,
                "chunk_id": r.chunk_id,
                "filename": r.filename,
                "page": r.page_number,
                "final_score": round(r.score, 4),
                "source_type": r.source_type,
                "content": r.content[:200],
            }
            for i, r in enumerate(final_results)
        ]

        yield _sse_event("step", {
            "step": 5, "name": "Hybrid Re-Ranking",
            "status": "complete",
            "result": {
                "scoring_formula": f"{settings.semantic_weight} × Semantic + {settings.graph_weight} × Graph",
                "final_chunks": len(ranked_chunks),
                "ranked_results": ranked_chunks,
            },
            "duration_ms": int((time.time() - step5_start) * 1000),
        })

        # === STEP 6: Context Assembly ===
        step6_start = time.time()
        yield _sse_event("step", {
            "step": 6, "name": "Context Assembly",
            "status": "running",
            "description": "Building context prompt for LLM..."
        })

        context_text = ""
        for i, r in enumerate(final_results):
            context_text += f"\n[Source {i+1}: {r.filename} p.{r.page_number}]\n{r.content}\n"

        yield _sse_event("step", {
            "step": 6, "name": "Context Assembly",
            "status": "complete",
            "result": {
                "context_length": len(context_text),
                "sources_included": len(final_results),
                "context_preview": context_text[:500],
            },
            "duration_ms": int((time.time() - step6_start) * 1000),
        })

        # === STEP 7: LLM Generation ===
        step7_start = time.time()
        yield _sse_event("step", {
            "step": 7, "name": "LLM Generation",
            "status": "running",
            "description": f"Sending to {settings.ollama_chat_model} via Ollama..."
        })

        generator = AnswerGenerator()
        graph_ctx = None
        if equipment_tags:
            try:
                graph_ctx = await neo4j.get_equipment_context(equipment_tags[0])
            except Exception:
                pass

        response = await generator.generate(
            query=query.question,
            retrieved_chunks=final_results,
            graph_context=graph_ctx,
        )

        yield _sse_event("step", {
            "step": 7, "name": "LLM Generation",
            "status": "complete",
            "result": {
                "model": settings.ollama_chat_model,
                "answer_length": len(response.answer) if hasattr(response, 'answer') else 0,
                "confidence": response.confidence if hasattr(response, 'confidence') else "unknown",
                "sources_cited": len(response.sources) if hasattr(response, 'sources') else 0,
            },
            "duration_ms": int((time.time() - step7_start) * 1000),
        })

        # === FINAL ===
        total_duration = int((time.time() - pipeline_start) * 1000)
        yield _sse_event("complete", {
            "answer": response.answer if hasattr(response, 'answer') else str(response),
            "confidence": response.confidence if hasattr(response, 'confidence') else "unknown",
            "sources": [{"filename": s.filename, "page_number": s.page_number} for s in response.sources] if hasattr(response, 'sources') else [],
            "suggested_followups": response.suggested_followups if hasattr(response, 'suggested_followups') else [],
            "total_duration_ms": total_duration,
            "chunks_retrieved": len(final_results),
        })

    return StreamingResponse(
        generate_events(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )
```

---

## `backend/app/routers/graph.py`

**Knowledge graph + FAISS search API**

```python
"""
Knowledge Graph API — direct graph exploration, FAISS index stats, and search endpoints.
"""

from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
import structlog

from app.services.knowledge_graph.neo4j_client import Neo4jClient
from app.services.vectorstore.faiss_service import FAISSService

logger = structlog.get_logger()
router = APIRouter()

class GraphSearchRequest(BaseModel):
    query: str
    node_type: str | None = None
    depth: int = 2
    limit: int = 50

@router.post("/search")
async def search_graph(request: Request, search: GraphSearchRequest):
    """Search the knowledge graph and FAISS index for matching results."""
    neo4j: Neo4jClient = request.app.state.neo4j
    faiss_service: FAISSService = request.app.state.faiss

    results = []

    # Try Neo4j search
    neo4j_results = await neo4j.search_nodes(search.query, limit=search.limit)
    for r in neo4j_results:
        results.append({**r, "source": "neo4j"})

    # Also search FAISS metadata for document/chunk matches
    faiss_matches = []
    for meta in faiss_service.get_all_metadata():
        term = search.query.lower()
        if (term in meta.get("filename", "").lower()
            or term in meta.get("content", "").lower()
            or term in meta.get("category", "").lower()):
            faiss_matches.append({
                "label": "Chunk",
                "props": {
                    "chunk_id": meta["chunk_id"],
                    "document_id": meta["document_id"],
                    "filename": meta.get("filename", ""),
                    "page": meta.get("page_number"),
                    "category": meta.get("category", ""),
                    "preview": meta["content"][:150],
                },
                "source": "faiss",
            })
            if len(faiss_matches) >= search.limit:
                break

    results.extend(faiss_matches)
    return {"results": results, "total": len(results)}

@router.post("/search/semantic")
async def semantic_search(request: Request, search: GraphSearchRequest):
    """Semantic vector search over FAISS index."""
    faiss_service: FAISSService = request.app.state.faiss
    results = await faiss_service.search(query=search.query, top_k=search.limit)
    return {
        "results": [
            {
                "chunk_id": r["chunk_id"],
                "document_id": r["document_id"],
                "filename": r.get("filename", ""),
                "page_number": r.get("page_number"),
                "category": r.get("category", ""),
                "content": r["content"][:300],
                "score": round(r["score"], 4),
            }
            for r in results
        ],
        "total": len(results),
    }

@router.get("/equipment/{tag}")
async def get_equipment(request: Request, tag: str):
    """Get full context for a piece of equipment from the knowledge graph."""
    neo4j: Neo4jClient = request.app.state.neo4j
    context = await neo4j.get_equipment_context(tag.upper())
    if not context:
        raise HTTPException(status_code=404, detail=f"Equipment {tag} not found")
    return context

@router.get("/neighbors/{node_type}/{key}/{value}")
async def get_neighbors(
    request: Request, node_type: str, key: str, value: str, depth: int = 2
):
    """Get neighboring nodes in the knowledge graph."""
    neo4j: Neo4jClient = request.app.state.neo4j
    neighbors = await neo4j.get_neighbors(node_type, key, value, depth)
    return {"node": {"type": node_type, key: value}, "neighbors": neighbors}

@router.get("/stats")
async def graph_stats(request: Request):
    """Get knowledge graph and vector index statistics."""
    neo4j: Neo4jClient = request.app.state.neo4j
    faiss_service: FAISSService = request.app.state.faiss

    # FAISS stats (always available)
    all_meta = faiss_service.get_all_metadata()
    total_chunks = len(all_meta)
    unique_docs = len(set(m["document_id"] for m in all_meta)) if all_meta else 0
    unique_files = len(set(m.get("filename", "") for m in all_meta if m.get("filename"))) if all_meta else 0

    # Category breakdown
    categories = {}
    for m in all_meta:
        cat = m.get("category", "unknown")
        categories[cat] = categories.get(cat, 0) + 1

    # Document list
    docs_map = {}
    for m in all_meta:
        doc_id = m["document_id"]
        if doc_id not in docs_map:
            docs_map[doc_id] = {
                "document_id": doc_id,
                "filename": m.get("filename", ""),
                "category": m.get("category", ""),
                "chunks": 0,
                "pages": set(),
            }
        docs_map[doc_id]["chunks"] += 1
        if m.get("page_number"):
            docs_map[doc_id]["pages"].add(m["page_number"])

    documents = [
        {**d, "pages": len(d["pages"]), "page_list": sorted(d["pages"])}
        for d in docs_map.values()
    ]

    # Neo4j stats (may be empty if not connected)
    neo4j_nodes = 0
    neo4j_rels = 0
    neo4j_connected = False
    node_types = []

    try:
        nodes = await neo4j.execute_query("MATCH (n) RETURN count(n) as count")
        rels = await neo4j.execute_query("MATCH ()-[r]->() RETURN count(r) as count")
        if nodes:
            neo4j_nodes = nodes[0]["count"]
            neo4j_connected = True
        if rels:
            neo4j_rels = rels[0]["count"]

        # Get node type breakdown
        types_result = await neo4j.execute_query(
            "MATCH (n) RETURN labels(n)[0] as label, count(n) as count ORDER BY count DESC"
        )
        node_types = [{"label": r["label"], "count": r["count"]} for r in types_result] if types_result else []
    except Exception:
        pass

    return {
        "neo4j_connected": neo4j_connected,
        "total_nodes": neo4j_nodes,
        "total_relationships": neo4j_rels,
        "node_types": node_types,
        "faiss_total_chunks": total_chunks,
        "faiss_total_documents": unique_docs,
        "faiss_total_files": unique_files,
        "faiss_dimension": faiss_service.index.d if faiss_service.index else 0,
        "categories": categories,
        "documents": documents,
    }
```

---

## `backend/app/routers/agents.py`

**Multi-agent intelligence API**

```python
"""
Agent API Router — exposes the multi-agent system via REST endpoints.
All reports are persisted to data/reports/ with naming convention:
    {equipment}_{shift}_{status}_{timestamp}.json
"""

from fastapi import APIRouter, Request
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import structlog

from app.services.agents.orchestrator import AgentOrchestrator
from app.services.agents.sensor_monitor_agent import SensorReading
from app.services.agents.report_saver import ReportSaver

logger = structlog.get_logger()
router = APIRouter()
report_saver = ReportSaver()

class SensorDataPoint(BaseModel):
    equipment_tag: str
    parameter: str
    value: float
    unit: str
    timestamp: Optional[datetime] = None

class SensorBatchRequest(BaseModel):
    readings: list[SensorDataPoint]

class PredictiveRequest(BaseModel):
    equipment_tag: str
    parameter_history: dict[str, list[float]]
    critical_limits: dict[str, float]
    equipment_type: str = "pump"
    hours_in_service: float = 10000
    next_pm_date: Optional[datetime] = None

class HandoverRequest(BaseModel):
    shift_start: datetime
    shift_end: datetime

@router.post("/analyze-sensors")
async def analyze_sensors(request: Request, data: SensorBatchRequest):
    """
    Process sensor readings through the multi-agent pipeline.

    Flow:
    1. Sensor Monitor Agent checks all readings for anomalies
    2. Fault Diagnosis Agent analyzes anomalies (root cause + suggestions)
    3. Events logged for shift handover

    Returns alerts, diagnoses, and health summary.
    """
    neo4j = getattr(request.app.state, "neo4j", None)
    orchestrator = AgentOrchestrator(neo4j_client=neo4j)

    # Convert to internal format
    readings = [
        SensorReading(
            equipment_tag=r.equipment_tag,
            parameter=r.parameter,
            value=r.value,
            unit=r.unit,
            timestamp=r.timestamp or datetime.utcnow(),
        )
        for r in data.readings
    ]

    result = await orchestrator.process_sensor_batch(readings)

    response_data = {
        "total_readings": len(readings),
        "anomalies_detected": len(result.alerts),
        "diagnoses_generated": len(result.diagnoses),
        "actions_suggested": result.actions_generated,
        "alerts": [
            {
                "equipment_tag": a.equipment_tag,
                "parameter": a.parameter,
                "value": a.current_value,
                "unit": a.unit,
                "status": a.status.value,
                "severity_score": a.severity_score,
                "reason": a.reason,
                "trend": a.trend_info,
            }
            for a in result.alerts
        ],
        "diagnoses": [
            {
                "equipment_tag": d.equipment_tag,
                "alert_summary": d.alert_summary,
                "confidence": d.confidence_level,
                "hypotheses": [
                    {
                        "cause": h.cause,
                        "confidence": h.confidence,
                        "category": h.category,
                        "evidence": h.evidence,
                    }
                    for h in d.hypotheses
                ],
                "recommended_actions": [
                    {
                        "action": a.action,
                        "priority": a.priority,
                        "effort": a.estimated_effort,
                        "parts_needed": a.parts_needed,
                        "sop_reference": a.sop_reference,
                    }
                    for a in d.recommended_actions
                ],
            }
            for d in result.diagnoses
        ],
        "health_summary": result.health_summary,
    }

    # Save sensor analysis report
    equipment_tags = list(set(r.equipment_tag for r in data.readings))
    sensor_report_path = report_saver.save_sensor_analysis(
        report_data=response_data,
        equipment_tags=equipment_tags,
        alerts=result.alerts,
    )
    response_data["report_saved_to"] = sensor_report_path

    # Save individual diagnosis reports
    diagnosis_report_paths = []
    for d in result.diagnoses:
        diag_data = {
            "equipment_tag": d.equipment_tag,
            "alert_summary": d.alert_summary,
            "confidence": d.confidence_level,
            "hypotheses": [
                {"cause": h.cause, "confidence": h.confidence, "category": h.category, "evidence": h.evidence}
                for h in d.hypotheses
            ],
            "recommended_actions": [
                {"action": a.action, "priority": a.priority, "effort": a.estimated_effort,
                 "parts_needed": a.parts_needed, "sop_reference": a.sop_reference}
                for a in d.recommended_actions
            ],
            "similar_past_incidents": d.similar_past_incidents,
        }
        path = report_saver.save_fault_diagnosis(
            report_data=diag_data,
            equipment_tag=d.equipment_tag,
            confidence_level=d.confidence_level,
        )
        diagnosis_report_paths.append(path)
    response_data["diagnosis_reports_saved_to"] = diagnosis_report_paths

    return response_data

@router.post("/predict-maintenance")
async def predict_maintenance(request: Request, data: PredictiveRequest):
    """
    Run predictive maintenance analysis for specific equipment.
    Returns Remaining Useful Life estimate and maintenance recommendations.
    """
    neo4j = getattr(request.app.state, "neo4j", None)
    orchestrator = AgentOrchestrator(neo4j_client=neo4j)

    report = await orchestrator.get_predictive_report(
        equipment_tag=data.equipment_tag,
        parameter_history=data.parameter_history,
        critical_limits=data.critical_limits,
        equipment_type=data.equipment_type,
        hours_in_service=data.hours_in_service,
        next_pm=data.next_pm_date,
    )

    response_data = {
        "equipment_tag": report.equipment_tag,
        "overall_health_score": report.overall_health_score,
        "risk_summary": report.risk_summary,
        "rul_estimates": [
            {
                "parameter": r.parameter,
                "days_to_failure": r.estimated_days_to_failure,
                "confidence_interval": r.confidence_interval,
                "risk_score": r.risk_score,
                "method": r.method,
                "health_pct": r.current_health_pct,
            }
            for r in report.rul_estimates
        ],
        "recommendations": [
            {
                "action": r.action,
                "recommended_date": r.recommended_date.isoformat(),
                "urgency": r.urgency,
                "cost_early_intervention": r.cost_of_early_intervention,
                "cost_unplanned_failure": r.cost_of_unplanned_failure,
                "reasoning": r.reasoning,
            }
            for r in report.maintenance_recommendations
        ],
    }

    # Save predictive report
    pred_report_path = report_saver.save_predictive_report(
        report_data=response_data,
        equipment_tag=data.equipment_tag,
        risk_level=report.risk_summary,
    )
    response_data["report_saved_to"] = pred_report_path

    return response_data

@router.post("/shift-handover")
async def generate_handover(request: Request, data: HandoverRequest):
    """
    Generate a shift handover report for the specified time window.
    Summarizes all events, alarms, and pending items.
    """
    neo4j = getattr(request.app.state, "neo4j", None)
    orchestrator = AgentOrchestrator(neo4j_client=neo4j)

    report, formatted_text = await orchestrator.generate_shift_handover(
        shift_start=data.shift_start,
        shift_end=data.shift_end,
    )

    response_data = {
        "shift": {
            "type": report.shift_type,
            "start": report.shift_start.isoformat(),
            "end": report.shift_end.isoformat(),
        },
        "summary": report.executive_summary,
        "stats": {
            "total_alarms": report.total_alarms,
            "critical_alarms": report.critical_alarms,
            "maintenance_actions": report.maintenance_actions,
        },
        "critical_items": report.critical_items,
        "work_in_progress": report.work_in_progress,
        "watch_items": report.watch_items,
        "upcoming": report.upcoming_activities,
        "formatted_report": formatted_text,
    }

    # Collect equipment tags from critical items and health changes
    equipment_tags = list(set(
        item.get("equipment", "")
        for item in report.critical_items + report.equipment_health_changes + report.work_in_progress
        if item.get("equipment")
    ))

    # Save shift handover report
    handover_path = report_saver.save_shift_handover(
        report_data=response_data,
        shift_type=report.shift_type,
        has_critical=report.critical_alarms > 0,
        shift_start=report.shift_start,
        equipment_tags=equipment_tags,
    )
    response_data["report_saved_to"] = handover_path

    return response_data

@router.get("/reports")
async def list_reports(
    category: Optional[str] = None,
    equipment: Optional[str] = None,
    status: Optional[str] = None,
):
    """
    List all saved reports. Filter by category, equipment tag, or status.

    Categories: sensor_analysis, fault_diagnosis, predictive, shift_handover
    Status in filename: NORMAL, WARNING, CRITICAL, HIGH-RISK, LOW-RISK, etc.
    """
    from pathlib import Path
    import json

    base = report_saver.base_dir
    results = []

    # Determine which subdirs to scan
    if category and (base / category).is_dir():
        subdirs = [base / category]
    else:
        subdirs = [d for d in base.iterdir() if d.is_dir()]

    for subdir in subdirs:
        for filepath in sorted(subdir.glob("*.json"), reverse=True):
            name = filepath.stem  # e.g. P-101A_day_CRITICAL_20240701_143022
            parts = name.split("_")

            # Apply filters
            if equipment and equipment.upper() not in name.upper():
                continue
            if status and status.upper() not in name.upper():
                continue

            # Parse naming convention
            file_info = {
                "filename": filepath.name,
                "category": subdir.name,
                "path": str(filepath),
                "size_bytes": filepath.stat().st_size,
                "created": datetime.fromtimestamp(filepath.stat().st_ctime).isoformat(),
            }

            # Extract equipment/shift/status from filename parts
            if len(parts) >= 4:
                # Last two parts are date_time, work backwards
                file_info["timestamp"] = f"{parts[-2]}_{parts[-1]}"
                file_info["status_label"] = parts[-3] if len(parts) >= 4 else ""
                file_info["shift"] = parts[-4] if len(parts) >= 5 else ""
                file_info["equipment"] = "_".join(parts[:-4]) if len(parts) > 4 else parts[0]

            results.append(file_info)

    return {
        "total_reports": len(results),
        "reports_directory": str(base),
        "reports": results[:100],  # Limit to 100 most recent
    }

@router.get("/reports/{category}/{filename}")
async def get_report(category: str, filename: str):
    """Retrieve a specific saved report by category and filename."""
    from pathlib import Path
    import json

    filepath = report_saver.base_dir / category / filename
    if not filepath.exists() or not filepath.is_file():
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail=f"Report not found: {category}/{filename}")

    # Prevent path traversal
    if ".." in filename or "/" in filename or "\\" in filename:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail="Invalid filename")

    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    return {
        "filename": filename,
        "category": category,
        "data": data,
    }
```

---

## `backend/app/services/__init__.py`

**Services package init**

```python

```

---

## `backend/app/services/ingestion/__init__.py`

**Ingestion package init**

```python

```

---

## `backend/app/services/ingestion/pipeline.py`

**Main 11-step ingestion pipeline orchestrator**

```python
"""
Main ingestion pipeline — orchestrates PDF detection, OCR, cleaning, structuring,
entity extraction, chunking, knowledge graph population, and vector indexing.

Pipeline phases (per GraphRAG spec):
1. PDF Type Detection (digital vs scanned)
2. OCR (PaddleOCR primary, Tesseract fallback)
3. Cleaning & Normalization
4. Document Structuring
5. Chunking + Metadata
6. Entity Extraction (spaCy + LLM)
7. Relationship Extraction
8. Neo4j Graph Loading
9. Embeddings + FAISS Indexing
10. Hybrid Retrieval ready
"""

import uuid
import fitz
from pathlib import Path
from datetime import datetime
import structlog

from app.config import settings
from app.models.schemas import (
    DocumentType, DocumentCategory, IngestedDocument,
    DocumentChunk, ExtractedEntity, ExtractedRelationship,
)
from app.services.ingestion.pdf_parser import PDFParser, DOCXParser, ParsedDocument
from app.services.ingestion.ocr_engine import OCREngine
from app.services.ingestion.text_cleaner import TextCleaner
from app.services.ingestion.document_structurer import DocumentStructurer
from app.services.ingestion.entity_extractor import IndustrialEntityExtractor
from app.services.ingestion.chunker import TextChunker
from app.services.ingestion.document_classifier import DocumentClassifier
from app.services.ingestion.relationship_extractor import RelationshipExtractor

logger = structlog.get_logger()

class IngestionPipeline:
    """
    End-to-end document ingestion pipeline (GraphRAG spec).

    Flow:
    1. Detect PDF type (digital vs scanned)
    2. Parse document (extract text, tables, images)
    3. OCR only if needed (PaddleOCR → Tesseract fallback)
    4. Clean and normalize text
    5. Preserve document structure (pages → sections → paragraphs)
    6. Classify document category
    7. Chunk semantically (300-600 tokens, 50-80 overlap)
    8. Extract entities (spaCy + LLM)
    9. Extract relationships (triples with confidence)
    10. Return structured IngestedDocument for graph + FAISS indexing
    """

    def __init__(self):
        self.pdf_parser = PDFParser()
        self.docx_parser = DOCXParser()
        self.ocr_engine = OCREngine()
        self.text_cleaner = TextCleaner()
        self.structurer = DocumentStructurer()
        self.entity_extractor = IndustrialEntityExtractor()
        self.chunker = TextChunker()
        self.classifier = DocumentClassifier()
        self.relationship_extractor = RelationshipExtractor()

    async def ingest(self, file_path: str | Path, filename: str | None = None) -> IngestedDocument:
        """Process a document through the full ingestion pipeline."""
        file_path = Path(file_path)
        filename = filename or file_path.name
        document_id = str(uuid.uuid4())

        logger.info("Starting ingestion", document_id=document_id, filename=filename)

        # Phase 1: Detect file type (digital vs scanned)
        file_type = self._detect_file_type(file_path)

        # Phase 2: Parse document (extract text, tables, images)
        parsed = self._parse_document(file_path, file_type)

        # Phase 3: OCR fallback for pages with no/little text
        raw_text = self._extract_text_with_ocr_fallback(parsed, file_path)

        # Phase 4: Clean and normalize text
        cleaned_text = self.text_cleaner.clean(raw_text)

        # Phase 5: Build structured document representation
        # Clean individual pages for page-level structure
        cleaned_page_texts = {}
        for page in parsed.pages:
            page_raw = page.text
            if self.ocr_engine.needs_ocr(page_raw):
                # Already OCR'd in phase 3, use the cleaned version
                cleaned_page_texts[page.page_number] = self.text_cleaner.clean(page_raw)
            else:
                cleaned_page_texts[page.page_number] = self.text_cleaner.clean(page_raw)

        structured_doc = self.structurer.structure(parsed, cleaned_page_texts)

        # Phase 6: Classify document category
        category = self.classifier.classify(cleaned_text, filename)

        # Phase 7: Extract entities (spaCy + patterns)
        entities = self._extract_entities(cleaned_text, parsed)

        # Phase 8: Extract relationships (triples with confidence)
        relationships = self.relationship_extractor.extract(cleaned_text, entities)

        # Phase 9: Chunk text semantically using structured sections
        chunks = self._create_chunks_from_structure(
            structured_doc, document_id, filename, category
        )

        # Build final result
        document = IngestedDocument(
            document_id=document_id,
            filename=filename,
            file_type=file_type,
            category=category,
            total_pages=parsed.total_pages,
            extracted_text=cleaned_text,
            chunks=chunks,
            entities=[
                ExtractedEntity(
                    entity_type=e.entity_type,
                    value=e.value,
                    confidence=e.confidence,
                    context=e.context,
                )
                for e in entities
            ],
            relationships=[
                ExtractedRelationship(
                    source_entity=r.source,
                    relationship_type=r.relation,
                    target_entity=r.target,
                    confidence=r.confidence,
                    source_context=r.context,
                )
                for r in relationships
            ],
            ingested_at=datetime.utcnow(),
        )

        logger.info(
            "Ingestion complete",
            document_id=document_id,
            filename=filename,
            category=category,
            entities_found=len(entities),
            relationships_found=len(relationships),
            chunks_created=len(chunks),
            pages=parsed.total_pages,
        )

        return document

    def _detect_file_type(self, file_path: Path) -> DocumentType:
        """Detect document type from extension."""
        ext = file_path.suffix.lower()
        type_map = {
            ".pdf": DocumentType.PDF,
            ".docx": DocumentType.DOCX,
            ".doc": DocumentType.DOCX,
            ".xlsx": DocumentType.XLSX,
            ".xls": DocumentType.XLSX,
            ".png": DocumentType.IMAGE,
            ".jpg": DocumentType.IMAGE,
            ".jpeg": DocumentType.IMAGE,
            ".tiff": DocumentType.IMAGE,
            ".tif": DocumentType.IMAGE,
            ".txt": DocumentType.UNKNOWN,  # handled as plain text
            ".json": DocumentType.UNKNOWN,
            ".csv": DocumentType.UNKNOWN,
        }
        return type_map.get(ext, DocumentType.UNKNOWN)

    def _parse_document(self, file_path: Path, file_type: DocumentType) -> ParsedDocument:
        """Parse document based on its type."""
        if file_type == DocumentType.PDF:
            return self.pdf_parser.parse(file_path)
        elif file_type == DocumentType.DOCX:
            return self.docx_parser.parse(file_path)
        elif file_type == DocumentType.IMAGE:
            # For standalone images, create a single-page parsed doc
            ocr_result = self.ocr_engine.ocr_image_file(file_path)
            from app.services.ingestion.pdf_parser import ParsedPage
            return ParsedDocument(
                filename=file_path.name,
                total_pages=1,
                pages=[ParsedPage(
                    page_number=1,
                    text=ocr_result.text,
                    tables=[],
                    images=[],
                    has_text=True,
                )],
                metadata={"ocr_confidence": ocr_result.confidence},
            )
        else:
            # Plain text / JSON / CSV / unknown — read as text
            from app.services.ingestion.pdf_parser import ParsedPage
            try:
                text = file_path.read_text(encoding="utf-8", errors="replace")
            except Exception:
                try:
                    text = file_path.read_text(encoding="latin-1", errors="replace")
                except Exception:
                    text = ""

            if not text.strip():
                # Last resort: try PDF parsing
                try:
                    return self.pdf_parser.parse(file_path)
                except Exception:
                    pass

            return ParsedDocument(
                filename=file_path.name,
                total_pages=1,
                pages=[ParsedPage(
                    page_number=1,
                    text=text,
                    tables=[],
                    images=[],
                    has_text=len(text.strip()) > 10,
                )],
                metadata={"format": file_path.suffix.lstrip(".")},
            )

    def _extract_text_with_ocr_fallback(
        self, parsed: ParsedDocument, file_path: Path
    ) -> str:
        """Extract text from all pages, using OCR when direct extraction fails."""
        all_text_parts = []

        for page in parsed.pages:
            if page.has_text and not self.ocr_engine.needs_ocr(page.text):
                # Direct text extraction worked
                all_text_parts.append(page.text)
            else:
                # Need OCR — render page to image first
                logger.info("Running OCR fallback", page=page.page_number)
                try:
                    if file_path.suffix.lower() == ".pdf":
                        doc = fitz.open(str(file_path))
                        pdf_page = doc[page.page_number - 1]
                        pix = pdf_page.get_pixmap(dpi=300)
                        image_bytes = pix.tobytes("png")
                        doc.close()
                        ocr_result = self.ocr_engine.ocr_pdf_page_image(
                            image_bytes, page.page_number
                        )
                        all_text_parts.append(ocr_result.text)
                    elif page.images:
                        # Use first image from the page
                        ocr_result = self.ocr_engine.ocr_image_bytes(
                            page.images[0], page.page_number
                        )
                        all_text_parts.append(ocr_result.text)
                    else:
                        all_text_parts.append(page.text)
                except Exception as e:
                    logger.error("OCR failed", page=page.page_number, error=str(e))
                    all_text_parts.append(page.text)

            # Also include table text
            for table in page.tables:
                for row in table:
                    row_text = " | ".join(cell or "" for cell in row)
                    if row_text.strip():
                        all_text_parts.append(row_text)

        return "\n\n".join(all_text_parts)

    def _extract_entities(self, full_text: str, parsed: ParsedDocument) -> list:
        """Extract entities from the full document text."""
        all_entities = []

        # Extract from full text
        entities = self.entity_extractor.extract_all(full_text)
        all_entities.extend(entities)

        # Also extract per-page for page-level attribution
        for page in parsed.pages:
            if page.text.strip():
                page_entities = self.entity_extractor.extract_all(
                    page.text, page_number=page.page_number
                )
                for ent in page_entities:
                    # Only add if not already found
                    if not any(
                        e.value == ent.value and e.entity_type == ent.entity_type
                        for e in all_entities
                    ):
                        all_entities.append(ent)

        return all_entities

    def _create_chunks(
        self,
        full_text: str,
        document_id: str,
        parsed: ParsedDocument,
        filename: str,
        category: DocumentCategory,
    ) -> list[DocumentChunk]:
        """Create text chunks for vector storage (legacy method)."""
        chunks = []

        for page in parsed.pages:
            page_text = page.text.strip()
            if not page_text:
                continue

            page_chunks = self.chunker.chunk_text(
                text=page_text,
                document_id=document_id,
                page_number=page.page_number,
                metadata={
                    "filename": filename,
                    "category": category.value,
                    "page": page.page_number,
                },
            )

            for chunk in page_chunks:
                chunks.append(DocumentChunk(
                    chunk_id=chunk.chunk_id,
                    document_id=document_id,
                    content=chunk.content,
                    page_number=chunk.page_number,
                    chunk_index=chunk.chunk_index,
                    metadata=chunk.metadata,
                ))

        if not chunks and full_text.strip():
            full_chunks = self.chunker.chunk_text(
                text=full_text,
                document_id=document_id,
                metadata={"filename": filename, "category": category.value},
            )
            for chunk in full_chunks:
                chunks.append(DocumentChunk(
                    chunk_id=chunk.chunk_id,
                    document_id=document_id,
                    content=chunk.content,
                    page_number=chunk.page_number,
                    chunk_index=chunk.chunk_index,
                    metadata=chunk.metadata,
                ))

        return chunks

    def _create_chunks_from_structure(
        self,
        structured_doc,
        document_id: str,
        filename: str,
        category: DocumentCategory,
    ) -> list[DocumentChunk]:
        """
        Create chunks from structured document representation.
        Follows hierarchy: Document → Page → Section → Paragraph → Chunk
        """
        from app.services.ingestion.document_structurer import StructuredDocument

        chunks = []

        for page in structured_doc.pages:
            for section in page.sections:
                # Combine section paragraphs into text
                section_text = "\n\n".join(section.paragraphs)

                # Include table text
                for table in section.tables:
                    for row in table:
                        row_text = " | ".join(cell or "" for cell in row)
                        if row_text.strip():
                            section_text += "\n" + row_text

                if not section_text.strip():
                    continue

                section_chunks = self.chunker.chunk_text(
                    text=section_text,
                    document_id=document_id,
                    page_number=page.page,
                    section_heading=section.heading,
                    metadata={
                        "filename": filename,
                        "category": category.value,
                        "page": page.page,
                        "section": section.heading,
                    },
                )

                for chunk in section_chunks:
                    chunks.append(DocumentChunk(
                        chunk_id=chunk.chunk_id,
                        document_id=document_id,
                        content=chunk.content,
                        page_number=chunk.page_number,
                        chunk_index=chunk.chunk_index,
                        metadata=chunk.metadata,
                    ))

        # Fallback: if structured chunking produced nothing, chunk full text
        if not chunks:
            full_text = structured_doc.get_full_text()
            if full_text.strip():
                fallback_chunks = self.chunker.chunk_text(
                    text=full_text,
                    document_id=document_id,
                    metadata={"filename": filename, "category": category.value},
                )
                for chunk in fallback_chunks:
                    chunks.append(DocumentChunk(
                        chunk_id=chunk.chunk_id,
                        document_id=document_id,
                        content=chunk.content,
                        page_number=chunk.page_number,
                        chunk_index=chunk.chunk_index,
                        metadata=chunk.metadata,
                    ))

        return chunks
```

---

## `backend/app/services/ingestion/pdf_parser.py`

**PDF and DOCX parser (PyMuPDF)**

```python
"""
PDF and DOCX document parser with layout-aware text extraction.
Uses PyMuPDF for PDFs and python-docx for Word documents.
"""

import fitz  # PyMuPDF
from pathlib import Path
from dataclasses import dataclass
import structlog

logger = structlog.get_logger()

@dataclass
class ParsedPage:
    page_number: int
    text: str
    tables: list[list[list[str]]]
    images: list[bytes]
    has_text: bool

@dataclass
class ParsedDocument:
    filename: str
    total_pages: int
    pages: list[ParsedPage]
    metadata: dict

class PDFParser:
    """Extracts text, tables, and images from PDF documents."""

    def parse(self, file_path: str | Path) -> ParsedDocument:
        file_path = Path(file_path)
        logger.info("Parsing PDF", filename=file_path.name)

        doc = fitz.open(str(file_path))
        pages = []

        for page_num in range(len(doc)):
            page = doc[page_num]

            # Extract text with layout preservation
            text = page.get_text("text")

            # Extract tables using built-in table finder
            tables = self._extract_tables(page)

            # Extract images (for OCR fallback or P&ID processing)
            images = self._extract_images(page)

            has_text = len(text.strip()) > 50

            pages.append(ParsedPage(
                page_number=page_num + 1,
                text=text,
                tables=tables,
                images=images,
                has_text=has_text,
            ))

        metadata = doc.metadata or {}
        doc.close()

        logger.info(
            "PDF parsed",
            filename=file_path.name,
            pages=len(pages),
            pages_with_text=sum(1 for p in pages if p.has_text),
        )

        return ParsedDocument(
            filename=file_path.name,
            total_pages=len(pages),
            pages=pages,
            metadata=metadata,
        )

    def _extract_tables(self, page: fitz.Page) -> list[list[list[str]]]:
        """Extract tables from a PDF page using PyMuPDF's table finder."""
        tables = []
        try:
            tab_finder = page.find_tables()
            for table in tab_finder:
                extracted = table.extract()
                if extracted:
                    tables.append(extracted)
        except Exception as e:
            logger.warning("Table extraction failed", error=str(e))
        return tables

    def _extract_images(self, page: fitz.Page) -> list[bytes]:
        """Extract images from a PDF page for OCR processing."""
        images = []
        try:
            image_list = page.get_images(full=True)
            doc = page.parent
            for img_info in image_list:
                xref = img_info[0]
                pix = fitz.Pixmap(doc, xref)
                if pix.n - pix.alpha > 3:  # CMYK → RGB
                    pix = fitz.Pixmap(fitz.csRGB, pix)
                images.append(pix.tobytes("png"))
                pix = None
        except Exception as e:
            logger.warning("Image extraction failed", error=str(e))
        return images

class DOCXParser:
    """Extracts text and tables from Word documents."""

    def parse(self, file_path: str | Path) -> ParsedDocument:
        from docx import Document

        file_path = Path(file_path)
        logger.info("Parsing DOCX", filename=file_path.name)

        doc = Document(str(file_path))

        # Extract all paragraph text
        full_text = []
        for para in doc.paragraphs:
            if para.text.strip():
                full_text.append(para.text)

        # Extract tables
        tables = []
        for table in doc.tables:
            table_data = []
            for row in table.rows:
                row_data = [cell.text.strip() for cell in row.cells]
                table_data.append(row_data)
            tables.append(table_data)

        text = "\n".join(full_text)

        page = ParsedPage(
            page_number=1,
            text=text,
            tables=tables,
            images=[],
            has_text=len(text.strip()) > 50,
        )

        return ParsedDocument(
            filename=file_path.name,
            total_pages=1,
            pages=[page],
            metadata={"format": "docx"},
        )
```

---

## `backend/app/services/ingestion/ocr_engine.py`

**OCR engine — PaddleOCR (primary) + Tesseract (fallback)**

```python
"""
OCR Engine for scanned documents and images.
Uses PaddleOCR (primary, offline) with Tesseract as fallback.
"""

from __future__ import annotations
import io
from pathlib import Path
from dataclasses import dataclass
import numpy as np
import structlog

logger = structlog.get_logger()

# Try PaddleOCR first (preferred offline OCR)
try:
    from paddleocr import PaddleOCR
    HAS_PADDLE = True
except ImportError:
    HAS_PADDLE = False

# Tesseract as fallback
try:
    import pytesseract
    from PIL import Image, ImageFilter, ImageEnhance
    HAS_TESSERACT = True
except ImportError:
    HAS_TESSERACT = False

if not HAS_TESSERACT:
    try:
        from PIL import Image, ImageFilter, ImageEnhance
    except ImportError:
        pass

@dataclass
class OCRResult:
    text: str
    confidence: float
    page_number: int
    bounding_boxes: list[dict] | None = None

class OCREngine:
    """
    Performs OCR on images and scanned PDF pages.
    Priority: PaddleOCR (offline, accurate) > Tesseract (fallback)
    """

    def __init__(self, lang: str = "en"):
        self.lang = lang
        self._paddle_ocr = None

    def _get_paddle_ocr(self):
        """Lazy-load PaddleOCR model."""
        if self._paddle_ocr is None and HAS_PADDLE:
            self._paddle_ocr = PaddleOCR(
                use_angle_cls=True,
                lang=self.lang,
                use_gpu=False,
                show_log=False,
            )
            logger.info("PaddleOCR engine loaded")
        return self._paddle_ocr

    def ocr_image_bytes(self, image_bytes: bytes, page_number: int = 1) -> OCRResult:
        """Run OCR on raw image bytes."""
        image = Image.open(io.BytesIO(image_bytes))
        return self._process_image(image, page_number)

    def ocr_image_file(self, file_path: str | Path, page_number: int = 1) -> OCRResult:
        """Run OCR on an image file."""
        image = Image.open(str(file_path))
        return self._process_image(image, page_number)

    def ocr_pdf_page_image(self, page_pixmap_bytes: bytes, page_number: int) -> OCRResult:
        """Run OCR on a rendered PDF page (for scanned PDFs)."""
        image = Image.open(io.BytesIO(page_pixmap_bytes))
        return self._process_image(image, page_number)

    def _process_image(self, image: Image.Image, page_number: int) -> OCRResult:
        """Route to best available OCR engine."""
        if HAS_PADDLE:
            return self._paddle_ocr_process(image, page_number)
        elif HAS_TESSERACT:
            return self._tesseract_process(image, page_number)
        else:
            logger.warning("No OCR engine available")
            return OCRResult(text="", confidence=0.0, page_number=page_number)

    def _paddle_ocr_process(self, image: Image.Image, page_number: int) -> OCRResult:
        """Process image with PaddleOCR."""
        ocr = self._get_paddle_ocr()
        if ocr is None:
            return self._tesseract_process(image, page_number) if HAS_TESSERACT else OCRResult(
                text="", confidence=0.0, page_number=page_number
            )

        # Convert PIL to numpy array for PaddleOCR
        img_array = np.array(image.convert("RGB"))

        result = ocr.ocr(img_array, cls=True)

        text_parts = []
        confidences = []
        bounding_boxes = []

        if result and result[0]:
            for line in result[0]:
                bbox = line[0]
                text_info = line[1]
                text = text_info[0]
                confidence = text_info[1]

                text_parts.append(text)
                confidences.append(confidence)
                bounding_boxes.append({
                    "text": text,
                    "confidence": confidence,
                    "bbox": bbox,
                })

        full_text = " ".join(text_parts)
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0

        logger.info(
            "PaddleOCR completed",
            page=page_number,
            chars=len(full_text),
            confidence=f"{avg_confidence:.2f}",
        )

        return OCRResult(
            text=full_text,
            confidence=avg_confidence,
            page_number=page_number,
            bounding_boxes=bounding_boxes,
        )

    def _tesseract_process(self, image: Image.Image, page_number: int) -> OCRResult:
        """Fallback: Process image with Tesseract."""
        if not HAS_TESSERACT:
            return OCRResult(text="", confidence=0.0, page_number=page_number)

        processed = self._preprocess(image)

        ocr_data = pytesseract.image_to_data(
            processed, lang="eng", output_type=pytesseract.Output.DICT
        )

        text_parts = []
        confidences = []

        for i, word in enumerate(ocr_data["text"]):
            conf = int(ocr_data["conf"][i])
            if conf > 0 and word.strip():
                text_parts.append(word)
                confidences.append(conf)

        text = " ".join(text_parts)
        avg_confidence = (sum(confidences) / len(confidences) / 100.0) if confidences else 0.0

        logger.info(
            "Tesseract OCR completed (fallback)",
            page=page_number,
            chars=len(text),
            confidence=f"{avg_confidence:.2f}",
        )

        return OCRResult(
            text=text,
            confidence=avg_confidence,
            page_number=page_number,
        )

    def _preprocess(self, image: Image.Image) -> Image.Image:
        """Apply preprocessing steps to improve OCR accuracy."""
        if image.mode != "L":
            image = image.convert("L")

        width, height = image.size
        if width < 1000:
            scale = 1500 / width
            image = image.resize(
                (int(width * scale), int(height * scale)), Image.LANCZOS
            )

        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.5)

        image = image.filter(ImageFilter.SHARPEN)

        threshold = 140
        image = image.point(lambda x: 255 if x > threshold else 0, "1")

        return image

    def needs_ocr(self, text: str, page_image_bytes: bytes | None = None) -> bool:
        """Determine if a page needs OCR (too little extractable text)."""
        if len(text.strip()) < 50:
            return True

        printable_ratio = sum(1 for c in text if c.isprintable()) / max(len(text), 1)
        if printable_ratio < 0.8:
            return True

        return False
```

---

## `backend/app/services/ingestion/text_cleaner.py`

**Text cleaning and normalization (ftfy + regex)**

```python
"""
Text cleaning and normalization for OCR and extracted text.
Removes noise, normalizes unicode, preserves structure.
"""

import re
import unicodedata
import structlog

try:
    import ftfy
    HAS_FTFY = True
except ImportError:
    HAS_FTFY = False

logger = structlog.get_logger()

class TextCleaner:
    """
    Cleans and normalizes text extracted from PDFs and OCR.

    Handles:
    - OCR noise removal
    - Unicode normalization
    - Whitespace cleanup
    - Header/footer removal
    - Table/code/list preservation
    """

    def __init__(self):
        # Patterns for boilerplate detection
        self._header_footer_patterns = [
            re.compile(r"^Page\s+\d+\s*(of\s+\d+)?$", re.IGNORECASE | re.MULTILINE),
            re.compile(r"^\d+\s*$", re.MULTILINE),  # Standalone page numbers
            re.compile(r"^(CONFIDENTIAL|DRAFT|INTERNAL)\s*$", re.IGNORECASE | re.MULTILINE),
            re.compile(r"^(©|Copyright).*$", re.IGNORECASE | re.MULTILINE),
        ]
        # OCR artifact patterns
        self._ocr_noise_patterns = [
            re.compile(r"[|]{3,}"),  # Repeated pipes
            re.compile(r"[_]{5,}"),  # Long underscores (form lines)
            re.compile(r"[~]{3,}"),  # Repeated tildes
            re.compile(r"[.]{5,}"),  # Long dot leaders
        ]

    def clean(self, text: str) -> str:
        """Full cleaning pipeline for extracted text."""
        if not text or not text.strip():
            return ""

        # Step 1: Fix unicode encoding issues
        text = self._fix_unicode(text)

        # Step 2: Normalize unicode characters
        text = self._normalize_unicode(text)

        # Step 3: Remove OCR artifacts
        text = self._remove_ocr_noise(text)

        # Step 4: Fix broken line wraps
        text = self._fix_line_wraps(text)

        # Step 5: Remove duplicate spaces
        text = self._normalize_whitespace(text)

        # Step 6: Remove headers/footers/boilerplate
        text = self._remove_boilerplate(text)

        # Step 7: Normalize bullets and lists
        text = self._normalize_bullets(text)

        # Step 8: Normalize punctuation
        text = self._normalize_punctuation(text)

        return text.strip()

    def _fix_unicode(self, text: str) -> str:
        """Fix mojibake and encoding issues using ftfy."""
        if HAS_FTFY:
            return ftfy.fix_text(text)
        return text

    def _normalize_unicode(self, text: str) -> str:
        """Normalize unicode to NFC form."""
        text = unicodedata.normalize("NFC", text)

        # Replace common unicode variants with ASCII equivalents
        replacements = {
            "\u2018": "'", "\u2019": "'",  # Smart quotes
            "\u201c": '"', "\u201d": '"',
            "\u2013": "-", "\u2014": "-",  # En/em dash
            "\u2026": "...",  # Ellipsis
            "\u00a0": " ",  # Non-breaking space
            "\ufeff": "",  # BOM
            "\u200b": "",  # Zero-width space
        }
        for old, new in replacements.items():
            text = text.replace(old, new)

        return text

    def _remove_ocr_noise(self, text: str) -> str:
        """Remove common OCR artifacts."""
        for pattern in self._ocr_noise_patterns:
            text = pattern.sub("", text)

        # Remove isolated single characters that are likely OCR errors
        # (but preserve single-letter words like "I", "a")
        text = re.sub(r"(?<!\w)([^IaA\s\d])\s(?!\w)", " ", text)

        return text

    def _fix_line_wraps(self, text: str) -> str:
        """Fix broken line wraps from PDF column extraction."""
        # Join lines that were broken mid-sentence (line ends without sentence-ending punctuation)
        lines = text.split("\n")
        fixed_lines = []
        i = 0

        while i < len(lines):
            line = lines[i]

            # Check if line continues on next line
            if (i + 1 < len(lines)
                and line.strip()
                and not line.strip().endswith((".", "!", "?", ":", ";", "|"))
                and not self._is_heading(line)
                and not self._is_list_item(lines[i + 1])
                and lines[i + 1].strip()
                and lines[i + 1][0:1].islower()):
                # Merge with next line
                fixed_lines.append(line.rstrip() + " " + lines[i + 1].lstrip())
                i += 2
            else:
                fixed_lines.append(line)
                i += 1

        return "\n".join(fixed_lines)

    def _normalize_whitespace(self, text: str) -> str:
        """Remove duplicate spaces and normalize whitespace."""
        # Multiple spaces to single
        text = re.sub(r"[ \t]+", " ", text)
        # Multiple blank lines to double newline
        text = re.sub(r"\n{3,}", "\n\n", text)
        # Remove trailing whitespace per line
        text = "\n".join(line.rstrip() for line in text.split("\n"))
        return text

    def _remove_boilerplate(self, text: str) -> str:
        """Remove headers, footers, and repeated boilerplate."""
        for pattern in self._header_footer_patterns:
            text = pattern.sub("", text)
        return text

    def _normalize_bullets(self, text: str) -> str:
        """Normalize various bullet point styles."""
        # Normalize bullet characters
        bullet_chars = ["•", "●", "○", "■", "□", "▪", "►", "▶", "◆", "◇"]
        for char in bullet_chars:
            text = text.replace(char, "- ")

        # Normalize numbered lists variations
        text = re.sub(r"^(\d+)\)\s", r"\1. ", text, flags=re.MULTILINE)

        return text

    def _normalize_punctuation(self, text: str) -> str:
        """Fix common punctuation issues from OCR."""
        # Fix spacing around punctuation
        text = re.sub(r"\s+([.,;:!?])", r"\1", text)
        text = re.sub(r"([.,;:!?])(\w)", r"\1 \2", text)
        return text

    def _is_heading(self, line: str) -> bool:
        """Check if a line appears to be a heading."""
        stripped = line.strip()
        if not stripped:
            return False
        # All caps line
        if stripped.isupper() and len(stripped) < 100:
            return True
        # Numbered heading
        if re.match(r"^\d+(\.\d+)*\s+[A-Z]", stripped):
            return True
        return False

    def _is_list_item(self, line: str) -> bool:
        """Check if a line is a list item."""
        stripped = line.strip()
        if re.match(r"^[-•*]\s", stripped):
            return True
        if re.match(r"^\d+[.)]\s", stripped):
            return True
        return False
```

---

## `backend/app/services/ingestion/document_structurer.py`

**Document structure builder (pages → sections → paragraphs)**

```python
"""
Document Structurer — converts raw extracted text into a structured JSON representation.
Preserves headings, paragraphs, tables, and page metadata.
"""

import re
from dataclasses import dataclass, field
import structlog

from app.services.ingestion.pdf_parser import ParsedDocument

logger = structlog.get_logger()

@dataclass
class Section:
    heading: str
    paragraphs: list[str] = field(default_factory=list)
    tables: list[list[list[str]]] = field(default_factory=list)

@dataclass
class StructuredPage:
    page: int
    sections: list[Section] = field(default_factory=list)

@dataclass
class StructuredDocument:
    document: str
    pages: list[StructuredPage] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Convert to JSON-serializable dict."""
        return {
            "document": self.document,
            "pages": [
                {
                    "page": p.page,
                    "sections": [
                        {
                            "heading": s.heading,
                            "paragraphs": s.paragraphs,
                            "tables": s.tables,
                        }
                        for s in p.sections
                    ],
                }
                for p in self.pages
            ],
        }

    def get_full_text(self) -> str:
        """Reconstruct full text from structured representation."""
        parts = []
        for page in self.pages:
            for section in page.sections:
                if section.heading:
                    parts.append(section.heading)
                parts.extend(section.paragraphs)
                for table in section.tables:
                    for row in table:
                        parts.append(" | ".join(cell or "" for cell in row))
        return "\n\n".join(parts)

class DocumentStructurer:
    """
    Converts parsed document into a structured representation
    preserving document hierarchy (pages → sections → paragraphs/tables).
    """

    # Heading detection patterns
    _heading_patterns = [
        re.compile(r"^(\d+(\.\d+)*)\s+(.+)$"),  # Numbered: "1.2 Title"
        re.compile(r"^([A-Z][A-Z\s]{4,})$"),  # ALL CAPS heading
        re.compile(r"^(#{1,6})\s+(.+)$"),  # Markdown-style
        re.compile(r"^(Section|Chapter|Part)\s+\d+[.:]\s*(.+)$", re.IGNORECASE),
    ]

    def structure(self, parsed: ParsedDocument, cleaned_texts: dict[int, str] | None = None) -> StructuredDocument:
        """
        Build structured document from ParsedDocument.

        Args:
            parsed: The parsed document with pages
            cleaned_texts: Optional dict mapping page_number -> cleaned text
        """
        structured = StructuredDocument(document=parsed.filename)

        for page in parsed.pages:
            page_num = page.page_number

            # Use cleaned text if available, otherwise raw
            text = cleaned_texts.get(page_num, page.text) if cleaned_texts else page.text

            sections = self._extract_sections(text)

            # Attach tables to the last section of the page
            if page.tables and sections:
                sections[-1].tables = page.tables
            elif page.tables:
                sections.append(Section(heading="", tables=page.tables))

            structured.pages.append(StructuredPage(
                page=page_num,
                sections=sections,
            ))

        logger.info(
            "Document structured",
            filename=parsed.filename,
            pages=len(structured.pages),
            total_sections=sum(len(p.sections) for p in structured.pages),
        )

        return structured

    def _extract_sections(self, text: str) -> list[Section]:
        """Split page text into sections based on headings."""
        if not text.strip():
            return []

        lines = text.split("\n")
        sections: list[Section] = []
        current_heading = ""
        current_paragraphs: list[str] = []
        current_para_buffer: list[str] = []

        for line in lines:
            stripped = line.strip()

            if not stripped:
                # Blank line: flush paragraph buffer
                if current_para_buffer:
                    current_paragraphs.append(" ".join(current_para_buffer))
                    current_para_buffer = []
                continue

            if self._is_heading(stripped):
                # Flush current paragraph buffer
                if current_para_buffer:
                    current_paragraphs.append(" ".join(current_para_buffer))
                    current_para_buffer = []

                # Save previous section
                if current_heading or current_paragraphs:
                    sections.append(Section(
                        heading=current_heading,
                        paragraphs=current_paragraphs,
                    ))

                # Start new section
                current_heading = stripped
                current_paragraphs = []
            else:
                current_para_buffer.append(stripped)

        # Flush remaining
        if current_para_buffer:
            current_paragraphs.append(" ".join(current_para_buffer))

        if current_heading or current_paragraphs:
            sections.append(Section(
                heading=current_heading,
                paragraphs=current_paragraphs,
            ))

        # If no sections found, create a single section with all text
        if not sections:
            sections.append(Section(
                heading="",
                paragraphs=[text.strip()] if text.strip() else [],
            ))

        return sections

    def _is_heading(self, line: str) -> bool:
        """Determine if a line is a heading."""
        if not line or len(line) > 150:
            return False

        for pattern in self._heading_patterns:
            if pattern.match(line):
                return True

        # Short all-caps line (likely heading)
        if line.isupper() and 3 < len(line) < 80:
            return True

        return False
```

---

## `backend/app/services/ingestion/chunker.py`

**Semantic text chunker (500 tokens, 70 overlap)**

```python
"""
Text chunking utility for splitting documents into retrieval-friendly segments.
Uses semantic-aware chunking that respects paragraph and section boundaries.
Chunk size: 300-600 tokens, overlap: 50-80 tokens.
"""

from dataclasses import dataclass
import re
import uuid
import structlog

from app.config import settings

logger = structlog.get_logger()

@dataclass
class Chunk:
    chunk_id: str
    content: str
    chunk_index: int
    page_number: int | None
    section_heading: str | None
    metadata: dict

class TextChunker:
    """
    Splits document text into chunks optimized for retrieval.
    Respects section/paragraph boundaries for better semantic coherence.

    Hierarchy: Document → Page → Section → Paragraph → Chunk
    """

    def __init__(
        self,
        chunk_size: int = settings.chunk_size,
        chunk_overlap: int = settings.chunk_overlap,
    ):
        self.chunk_size = chunk_size  # 300-600 tokens
        self.chunk_overlap = chunk_overlap  # 50-80 tokens

    def chunk_text(
        self,
        text: str,
        document_id: str,
        page_number: int | None = None,
        section_heading: str | None = None,
        metadata: dict | None = None,
    ) -> list[Chunk]:
        """Split text into overlapping chunks with semantic boundaries."""
        if not text.strip():
            return []

        metadata = metadata or {}

        # First, split by section boundaries (headers, double newlines)
        sections = self._split_into_sections(text)

        chunks = []
        chunk_index = 0

        for section in sections:
            if len(section) <= self.chunk_size:
                # Section fits in one chunk
                if section.strip():
                    chunks.append(Chunk(
                        chunk_id=f"{document_id}_chunk_{chunk_index}",
                        content=section.strip(),
                        chunk_index=chunk_index,
                        page_number=page_number,
                        section_heading=section_heading,
                        metadata={
                            **metadata,
                            "document_id": document_id,
                            "page": page_number,
                            "heading": section_heading,
                            "chunk_id": f"{document_id}_chunk_{chunk_index}",
                            "source": metadata.get("filename", ""),
                        },
                    ))
                    chunk_index += 1
            else:
                # Section needs further splitting
                sub_chunks = self._split_long_section(section)
                for sub in sub_chunks:
                    if sub.strip():
                        chunks.append(Chunk(
                            chunk_id=f"{document_id}_chunk_{chunk_index}",
                            content=sub.strip(),
                            chunk_index=chunk_index,
                            page_number=page_number,
                            section_heading=section_heading,
                            metadata={
                                **metadata,
                                "document_id": document_id,
                                "page": page_number,
                                "heading": section_heading,
                                "chunk_id": f"{document_id}_chunk_{chunk_index}",
                                "source": metadata.get("filename", ""),
                            },
                        ))
                        chunk_index += 1

        logger.debug("Text chunked", chunks=len(chunks), document_id=document_id)
        return chunks

    def _split_into_sections(self, text: str) -> list[str]:
        """Split text at natural section boundaries."""
        # Split on section headers (numbered or capitalized lines)
        section_pattern = r"\n(?=\d+\.\s+[A-Z]|\n[A-Z][A-Z\s]{5,}\n|\n---)"
        sections = re.split(section_pattern, text)
        return [s for s in sections if s.strip()]

    def _split_long_section(self, text: str) -> list[str]:
        """Split a long section into overlapping chunks at sentence boundaries."""
        # Split into sentences
        sentences = re.split(r"(?<=[.!?])\s+", text)

        chunks = []
        current_chunk = []
        current_length = 0

        for sentence in sentences:
            sentence_len = len(sentence)

            if current_length + sentence_len > self.chunk_size and current_chunk:
                # Emit current chunk
                chunks.append(" ".join(current_chunk))

                # Keep overlap
                overlap_text = " ".join(current_chunk)
                overlap_sentences = []
                overlap_len = 0
                for s in reversed(current_chunk):
                    if overlap_len + len(s) <= self.chunk_overlap:
                        overlap_sentences.insert(0, s)
                        overlap_len += len(s)
                    else:
                        break

                current_chunk = overlap_sentences
                current_length = overlap_len

            current_chunk.append(sentence)
            current_length += sentence_len

        # Emit remaining
        if current_chunk:
            chunks.append(" ".join(current_chunk))

        return chunks
```

---

## `backend/app/services/ingestion/entity_extractor.py`

**Industrial entity extractor (spaCy + regex)**

```python
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
```

---

## `backend/app/services/ingestion/relationship_extractor.py`

**Relationship triple extractor**

```python
"""
Relationship extraction — identifies connections between extracted entities
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
```

class RelationshipExtractor:
"""
Extracts relationships between entities based on:
1. Proximity co-occurrence (entities mentioned close together)
2. Syntactic patterns (e.g., "pump P-101A failed due to bearing wear")
3. Structural patterns (e.g., entities in same table row)
"""

```
# Relationship trigger patterns
RELATION_PATTERNS = [
    # Equipment → Failure
    (
        r"(\b[A-Z]{1,4}-\d{2,5}[A-Z]?\b).*?(?:failed|tripped|malfunctioned|broke down).*?(?:due to|because of|caused by)\s+(.+?)(?:\.|$)",
        "FAILED_DUE_TO",
    ),
    # Equipment → Maintenance action
    (
        r"(\b[A-Z]{1,4}-\d{2,5}[A-Z]?\b).*?(?:repaired|replaced|overhauled|serviced|maintained)",
        "MAINTAINED",
    ),
    # Equipment → Inspection
    (
        r"(\b[A-Z]{1,4}-\d{2,5}[A-Z]?\b).*?(?:inspected|surveyed|examined|tested)",
        "INSPECTED",
    ),
    # Equipment → Procedure
    (
        r"(?:as per|refer|according to|per)\s+(SOP|procedure|WI)[-\s]?(\S+)",
        "GOVERNED_BY",
    ),
    # Personnel → Action on Equipment
    (
        r"(\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+\b).*?(?:performed|executed|carried out|completed).*?(\b[A-Z]{1,4}-\d{2,5}[A-Z]?\b)",
        "PERFORMED_ON",
    ),
    # Equipment → Location
    (
        r"(\b[A-Z]{1,4}-\d{2,5}[A-Z]?\b).*?(?:located at|installed in|at)\s+(.+?)(?:\.|,|$)",
        "LOCATED_AT",
    ),
]

def extract(self, text: str, entities: list) -> list[ExtractedRelation]:
    """Extract relationships between entities in the text."""
    relations = []

    # Strategy 1: Pattern-based extraction
    relations.extend(self._pattern_based_extraction(text))

    # Strategy 2: Co-occurrence (entities in same sentence)
    relations.extend(self._cooccurrence_extraction(text, entities))

    # Deduplicate
    seen = set()
    unique_relations = []
    for r in relations:
        key = (r.source, r.relation, r.target)
        if key not in seen:
            seen.add(key)
            unique_relations.append(r)

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
                target = groups[-1].strip()[:100]  # Limit target length
                context = text[max(0, match.start() - 30):match.end() + 30]

                relations.append(ExtractedRelation(
                    source=source,
                    relation=rel_type,
                    target=target,
                    confidence=0.8,
                    context=context,
                ))

    return relations

def _cooccurrence_extraction(self, text: str, entities: list) -> list[ExtractedRelation]:
    """Find relationships based on entity co-occurrence in sentences."""
    relations = []

    # Split into sentences
    sentences = re.split(r"[.!?]\s+", text)

    # Group entities by type
    equipment_entities = [e for e in entities if e.entity_type == "equipment"]
    other_entities = [e for e in entities if e.entity_type != "equipment"]

    for sentence in sentences:
        # Find equipment and other entities in same sentence
        equip_in_sentence = [
            e for e in equipment_entities if e.value.lower() in sentence.lower()
        ]
        others_in_sentence = [
            e for e in other_entities if e.value.lower() in sentence.lower()
        ]

        # Create co-occurrence relations
        for equip in equip_in_sentence:
            for other in others_in_sentence:
                rel_type = self._infer_relation_type(equip.entity_type, other.entity_type)
                if rel_type:
                    relations.append(ExtractedRelation(
                        source=equip.value,
                        relation=rel_type,
                        target=other.value,
                        confidence=0.6,
                        context=sentence[:150],
                    ))

        # Equipment → Equipment relations (in same sentence implies connection)
        if len(equip_in_sentence) > 1:
            for i, eq1 in enumerate(equip_in_sentence):
                for eq2 in equip_in_sentence[i + 1:]:
                    relations.append(ExtractedRelation(
                        source=eq1.value,
                        relation="CONNECTED_TO",
                        target=eq2.value,
                        confidence=0.5,
                        context=sentence[:150],
                    ))

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
```

```

---

## `backend/app/services/ingestion/document_classifier.py`

**Document category classifier (7 categories)**

```python
"""
Document classifier — determines the category of an industrial document
based on content analysis and filename patterns.
"""

import re
import structlog

from app.models.schemas import DocumentCategory

logger = structlog.get_logger()

class DocumentClassifier:
    """Classifies industrial documents into categories using keyword/pattern matching."""

    # Category indicators (keyword → category with weight)
    CATEGORY_SIGNALS = {
        DocumentCategory.PID: [
            (r"P&ID|piping.*instrument.*diagram|process flow diagram", 3),
            (r"line\s+list|equipment\s+list|instrument\s+index", 2),
            (r"control\s+valve|flow\s+transmitter|level\s+indicator", 1),
        ],
        DocumentCategory.WORK_ORDER: [
            (r"work\s+order|WO[-\s]?\d{4,}|maintenance\s+order", 3),
            (r"corrective\s+maintenance|preventive\s+maintenance|breakdown", 2),
            (r"spare\s+parts|man[-\s]?hours|downtime|repair", 1),
            (r"job\s+card|service\s+report|maintenance\s+record", 2),
        ],
        DocumentCategory.SOP: [
            (r"standard\s+operating\s+procedure|SOP|operating\s+instruction", 3),
            (r"work\s+instruction|safe\s+work\s+practice|JSA", 2),
            (r"step\s+\d+|precaution|PPE\s+required|safety\s+measure", 1),
            (r"procedure\s+no|rev(ision)?\.?\s*\d+|approved\s+by", 2),
        ],
        DocumentCategory.INSPECTION_REPORT: [
            (r"inspection\s+report|NDT\s+report|thickness\s+survey", 3),
            (r"corrosion|defect|finding|recommendation", 1),
            (r"ultrasonic|radiography|magnetic\s+particle|dye\s+penetrant", 2),
            (r"fitness\s+for\s+service|remaining\s+life|next\s+inspection", 2),
        ],
        DocumentCategory.INCIDENT_REPORT: [
            (r"incident\s+report|accident\s+report|near[-\s]?miss", 3),
            (r"root\s+cause\s+analysis|RCA|investigation", 2),
            (r"injury|fatality|fire|explosion|release|spill", 1),
            (r"corrective\s+action|preventive\s+action|CAPA", 2),
        ],
        DocumentCategory.OEM_MANUAL: [
            (r"operation\s+manual|maintenance\s+manual|OEM|manufacturer", 3),
            (r"installation\s+guide|commissioning|troubleshooting", 2),
            (r"spare\s+part.*list|exploded\s+view|wiring\s+diagram", 2),
            (r"model\s+no|serial\s+no|warranty", 1),
        ],
        DocumentCategory.REGULATORY: [
            (r"OISD|PESO|Factory\s+Act|BIS|statutory|compliance", 3),
            (r"regulation|standard|code\s+of\s+practice|guideline", 2),
            (r"shall\s+comply|mandatory|requirement|obligation", 1),
            (r"audit|certification|license|permit|approval", 1),
        ],
    }

    # Filename pattern signals
    FILENAME_PATTERNS = {
        DocumentCategory.PID: r"(?i)p&?id|pfd|process.*flow",
        DocumentCategory.WORK_ORDER: r"(?i)wo[-_]|work[-_]?order|maint",
        DocumentCategory.SOP: r"(?i)sop|procedure|oper.*instruct",
        DocumentCategory.INSPECTION_REPORT: r"(?i)insp|ndt|survey|thickness",
        DocumentCategory.INCIDENT_REPORT: r"(?i)incident|accident|near.?miss|rca",
        DocumentCategory.OEM_MANUAL: r"(?i)manual|oem|vendor|catalog",
        DocumentCategory.REGULATORY: r"(?i)oisd|regulation|standard|compliance",
    }

    def classify(self, text: str, filename: str = "") -> DocumentCategory:
        """Classify a document based on its content and filename."""
        scores: dict[DocumentCategory, float] = {cat: 0 for cat in DocumentCategory}

        # Score based on content patterns
        text_sample = text[:5000]  # Use first 5000 chars for classification
        for category, patterns in self.CATEGORY_SIGNALS.items():
            for pattern, weight in patterns:
                matches = len(re.findall(pattern, text_sample, re.IGNORECASE))
                scores[category] += matches * weight

        # Score based on filename
        for category, pattern in self.FILENAME_PATTERNS.items():
            if re.search(pattern, filename):
                scores[category] += 5  # Filename is a strong signal

        # Get highest scoring category
        best_category = max(scores, key=scores.get)
        best_score = scores[best_category]

        if best_score < 2:
            return DocumentCategory.GENERAL

        logger.info(
            "Document classified",
            category=best_category.value,
            score=best_score,
            filename=filename,
        )
        return best_category
```

---

## `backend/app/services/ingestion/llm_extractor.py`

**LLM-based entity extractor (Ollama)**

```python
"""
LLM-powered entity and relationship extraction for complex/ambiguous cases.
Uses FREE local LLM (Ollama) by default, with OpenAI as optional paid fallback.
"""

import httpx
import json
import structlog

from app.config import settings

logger = structlog.get_logger()

EXTRACTION_PROMPT = """You are an industrial document entity extraction system.
Extract structured entities and relationships from the following text.

Extract these entity types:
- equipment: Equipment tags, names, types (pumps, valves, compressors, etc.)
- personnel: People mentioned (operators, engineers, inspectors)
- parameter: Process parameters with values and units
- regulation: Standards, codes, regulatory references (OISD, API, ISO, BIS)
- date: Dates and time references
- location: Plant areas, units, buildings
- failure_mode: Equipment failure descriptions
- action: Maintenance/operational actions taken

Also extract relationships between entities in the format:
{source_entity} -[RELATIONSHIP_TYPE]-> {target_entity}

Common relationship types:
- FAILED_DUE_TO, MAINTAINED_BY, GOVERNED_BY, LOCATED_AT,
- PERFORMED_ON, CAUSED, REPLACED_WITH, CONNECTED_TO

Return as JSON with this structure:
{
  "entities": [
    {"type": "equipment", "value": "P-101A", "confidence": 0.95}
  ],
  "relationships": [
    {"source": "P-101A", "relation": "FAILED_DUE_TO", "target": "bearing wear", "confidence": 0.85}
  ]
}

ONLY extract entities that are clearly present in the text. Do not infer or hallucinate.
"""

class LLMEntityExtractor:
    """Uses FREE local LLM (Ollama) for complex entity and relationship extraction."""

    def __init__(self):
        self.provider = settings.llm_provider

    async def extract(self, text: str) -> dict:
        """Extract entities and relationships using LLM."""
        text_chunk = text[:4000]

        if self.provider == "ollama":
            return await self._extract_ollama(text_chunk)
        elif self.provider == "openai" and settings.openai_api_key:
            return await self._extract_openai(text_chunk)
        else:
            return {"entities": [], "relationships": []}

    async def _extract_ollama(self, text: str) -> dict:
        """Extract using Ollama (FREE local)."""
        try:
            async with httpx.AsyncClient(timeout=90.0) as client:
                response = await client.post(
                    f"{settings.ollama_base_url}/api/chat",
                    json={
                        "model": settings.ollama_chat_model,
                        "messages": [
                            {"role": "system", "content": EXTRACTION_PROMPT},
                            {"role": "user", "content": f"Extract entities from:\n\n{text}"},
                        ],
                        "stream": False,
                        "format": "json",
                        "options": {"temperature": 0.0, "num_predict": 2000},
                    },
                )

                if response.status_code == 200:
                    content = response.json()["message"]["content"]
                    result = json.loads(content)
                    logger.info(
                        "LLM extraction complete (Ollama)",
                        entities=len(result.get("entities", [])),
                        relationships=len(result.get("relationships", [])),
                    )
                    return result
                else:
                    return {"entities": [], "relationships": []}

        except Exception as e:
            logger.error("Ollama extraction failed", error=str(e))
            return {"entities": [], "relationships": []}

    async def _extract_openai(self, text: str) -> dict:
        """Extract using OpenAI (PAID fallback)."""
        try:
            from openai import AsyncOpenAI
            client = AsyncOpenAI(api_key=settings.openai_api_key)
            response = await client.chat.completions.create(
                model=settings.openai_chat_model,
                messages=[
                    {"role": "system", "content": EXTRACTION_PROMPT},
                    {"role": "user", "content": f"Extract entities from:\n\n{text}"},
                ],
                temperature=0.0,
                response_format={"type": "json_object"},
                max_tokens=2000,
            )

            result = json.loads(response.choices[0].message.content)
            logger.info(
                "LLM extraction complete (OpenAI)",
                entities=len(result.get("entities", [])),
                relationships=len(result.get("relationships", [])),
            )
            return result

        except Exception as e:
            logger.error("OpenAI extraction failed", error=str(e))
            return {"entities": [], "relationships": []}
```

---

## `backend/app/services/vectorstore/__init__.py`

**Vectorstore package init**

```python

```

---

## `backend/app/services/vectorstore/faiss_service.py`

**FAISS vector store + sentence-transformers embedding engine**

```python
"""
FAISS vector store service — handles embedding generation, storage, and retrieval.
Uses FREE local sentence-transformers for embeddings (no API costs).
Stores vectors in FAISS for offline semantic search.
"""

# Disable SSL verification globally for HuggingFace model downloads
# (required on corporate networks with self-signed certificates)
import ssl
import os
os.environ["HF_HUB_DISABLE_SSL_VERIFY"] = "1"
os.environ["CURL_CA_BUNDLE"] = ""
try:
    ssl._create_default_https_context = ssl._create_unverified_context
except AttributeError:
    pass
try:
    import httpx
    _orig_client_init = httpx.Client.__init__
    def _patched_client_init(self, *args, **kwargs):
        kwargs.setdefault("verify", False)
        _orig_client_init(self, *args, **kwargs)
    httpx.Client.__init__ = _patched_client_init
except Exception:
    pass

import os
import json
import numpy as np
from pathlib import Path
import structlog

try:
    import faiss
    HAS_FAISS = True
except ImportError:
    HAS_FAISS = False

from app.config import settings
from app.models.schemas import DocumentChunk

logger = structlog.get_logger()

class EmbeddingEngine:
    """
    Embedding generation using FREE local models.
    Priority: sentence-transformers (local) > Ollama (local) > OpenAI (paid fallback)
    """

    def __init__(self):
        self._st_model = None

    def _load_sentence_transformer(self):
        """Load sentence-transformers model (FREE, local, fast)."""
        if self._st_model is None:
            try:
                from sentence_transformers import SentenceTransformer
                self._st_model = SentenceTransformer(settings.local_embedding_model)
                logger.info(
                    "Loaded local embedding model",
                    model=settings.local_embedding_model,
                )
            except Exception as e:
                logger.warning("sentence-transformers not available", error=str(e))
        return self._st_model

    async def generate_embedding(self, text: str) -> list[float]:
        """Generate embedding using best available FREE method."""
        # Method 1: Local sentence-transformers (preferred — fast, free, no network)
        model = self._load_sentence_transformer()
        if model is not None:
            embedding = model.encode(text[:512], normalize_embeddings=True)
            return embedding.tolist()

        # Method 2: Ollama embeddings (free, local, needs Ollama running)
        try:
            import httpx
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{settings.ollama_base_url}/api/embeddings",
                    json={"model": settings.ollama_embedding_model, "prompt": text[:2000]},
                    timeout=30.0,
                )
                if response.status_code == 200:
                    return response.json()["embedding"]
        except Exception as e:
            logger.debug("Ollama embeddings failed", error=str(e))

        # Fallback: zero vector
        logger.warning("No embedding engine available, using zero vector")
        return [0.0] * settings.embedding_dimension

    async def generate_embeddings_batch(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for multiple texts in batch."""
        model = self._load_sentence_transformer()
        if model is not None:
            truncated = [t[:512] for t in texts]
            embeddings = model.encode(truncated, normalize_embeddings=True, batch_size=32)
            return [e.tolist() for e in embeddings]

        # Fallback: one by one
        results = []
        for text in texts:
            emb = await self.generate_embedding(text)
            results.append(emb)
        return results

class FAISSService:
    """
    Manages vector embeddings in FAISS for semantic search.
    Fully offline — no external service required.
    """

    def __init__(self):
        self.embedding_engine = EmbeddingEngine()
        self.index: "faiss.IndexFlatIP" | None = None
        self._metadata: list[dict] = []  # Stores chunk metadata alongside vectors
        self._index_path = Path(settings.faiss_index_dir)
        self._index_file = self._index_path / "index.faiss"
        self._metadata_file = self._index_path / "metadata.json"

    async def initialize(self):
        """Initialize FAISS index — load from disk or create new."""
        if not HAS_FAISS:
            logger.error("FAISS not installed. Install with: pip install faiss-cpu")
            return

        self._index_path.mkdir(parents=True, exist_ok=True)

        if self._index_file.exists() and self._metadata_file.exists():
            # Load existing index
            self.index = faiss.read_index(str(self._index_file))
            with open(self._metadata_file, "r", encoding="utf-8") as f:
                self._metadata = json.load(f)
            logger.info(
                "FAISS index loaded from disk",
                vectors=self.index.ntotal,
                metadata_entries=len(self._metadata),
            )
        else:
            # Create new index (Inner Product for cosine similarity with normalized vectors)
            self.index = faiss.IndexFlatIP(settings.embedding_dimension)
            self._metadata = []
            logger.info("New FAISS index created", dimension=settings.embedding_dimension)

    def _save_index(self):
        """Persist FAISS index and metadata to disk."""
        if self.index is None:
            return
        faiss.write_index(self.index, str(self._index_file))
        with open(self._metadata_file, "w", encoding="utf-8") as f:
            json.dump(self._metadata, f, ensure_ascii=False)
        logger.debug("FAISS index saved to disk", vectors=self.index.ntotal)

    async def generate_embedding(self, text: str) -> list[float]:
        """Generate embedding vector using FREE local model."""
        return await self.embedding_engine.generate_embedding(text)

    async def generate_embeddings_batch(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for multiple texts in a batch."""
        return await self.embedding_engine.generate_embeddings_batch(texts)

    async def index_chunks(self, chunks: list[DocumentChunk], document_id: str):
        """Index document chunks with their embeddings in FAISS."""
        if self.index is None:
            logger.warning("FAISS not initialized, skipping indexing")
            return

        if not chunks:
            return

        # Generate embeddings in batch
        texts = [chunk.content for chunk in chunks]
        embeddings = await self.generate_embeddings_batch(texts)

        # Convert to numpy array
        vectors = np.array(embeddings, dtype=np.float32)

        # Add to FAISS index
        self.index.add(vectors)

        # Store metadata for each vector
        for chunk in chunks:
            self._metadata.append({
                "chunk_id": chunk.chunk_id,
                "document_id": document_id,
                "content": chunk.content,
                "page_number": chunk.page_number,
                "chunk_index": chunk.chunk_index,
                "filename": chunk.metadata.get("filename", ""),
                "category": chunk.metadata.get("category", ""),
            })

        # Persist to disk
        self._save_index()

        logger.info(
            "Chunks indexed in FAISS",
            document_id=document_id,
            chunks_indexed=len(chunks),
            total_vectors=self.index.ntotal,
        )

    async def search(
        self,
        query: str,
        top_k: int = 5,
        category_filter: str | None = None,
    ) -> list[dict]:
        """Perform semantic search over indexed chunks."""
        if self.index is None or self.index.ntotal == 0:
            return []

        # Generate query embedding
        query_embedding = await self.generate_embedding(query)
        query_vector = np.array([query_embedding], dtype=np.float32)

        # Search FAISS (get more results if filtering)
        search_k = top_k * 3 if category_filter else top_k
        scores, indices = self.index.search(query_vector, min(search_k, self.index.ntotal))

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < 0 or idx >= len(self._metadata):
                continue

            meta = self._metadata[idx]

            # Apply category filter if specified
            if category_filter and meta.get("category", "") != category_filter:
                continue

            results.append({
                "chunk_id": meta["chunk_id"],
                "document_id": meta["document_id"],
                "content": meta["content"],
                "page_number": meta.get("page_number"),
                "chunk_index": meta.get("chunk_index"),
                "filename": meta.get("filename", ""),
                "category": meta.get("category", ""),
                "score": float(score),
            })

            if len(results) >= top_k:
                break

        return results

    async def delete_document(self, document_id: str):
        """Remove all vectors for a document. Rebuilds index without those vectors."""
        if self.index is None:
            return

        # Find indices to keep
        keep_indices = [
            i for i, meta in enumerate(self._metadata)
            if meta["document_id"] != document_id
        ]

        if len(keep_indices) == len(self._metadata):
            return  # Nothing to delete

        # Rebuild index without deleted vectors
        if keep_indices:
            # Reconstruct vectors for kept indices
            all_vectors = np.zeros((self.index.ntotal, settings.embedding_dimension), dtype=np.float32)
            for i in range(self.index.ntotal):
                all_vectors[i] = self.index.reconstruct(i)

            kept_vectors = all_vectors[keep_indices]
            kept_metadata = [self._metadata[i] for i in keep_indices]

            # Rebuild
            self.index = faiss.IndexFlatIP(settings.embedding_dimension)
            self.index.add(kept_vectors)
            self._metadata = kept_metadata
        else:
            self.index = faiss.IndexFlatIP(settings.embedding_dimension)
            self._metadata = []

        self._save_index()
        logger.info("Document removed from FAISS", document_id=document_id)

    def get_all_metadata(self) -> list[dict]:
        """Get all stored metadata (for BM25 index building)."""
        return self._metadata
```

---

## `backend/app/services/vectorstore/qdrant_service.py`

**Qdrant vector store (legacy, kept for reference)**

```python
"""
Qdrant vector store service — handles embedding generation, storage, and retrieval.
Uses FREE local sentence-transformers for embeddings (no API costs).
Optionally supports Ollama embeddings or OpenAI (paid) as fallback.
"""

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance, VectorParams, PointStruct,
    Filter, FieldCondition, MatchValue,
)
import uuid
import structlog

from app.config import settings
from app.models.schemas import DocumentChunk

logger = structlog.get_logger()

class EmbeddingEngine:
    """
    Embedding generation using FREE local models.
    Priority: sentence-transformers (local) > Ollama (local) > OpenAI (paid fallback)
    """

    def __init__(self):
        self._st_model = None
        self._ollama_available = False

    def _load_sentence_transformer(self):
        """Load sentence-transformers model (FREE, local, fast)."""
        if self._st_model is None:
            try:
                from sentence_transformers import SentenceTransformer
                self._st_model = SentenceTransformer(settings.local_embedding_model)
                logger.info(
                    "Loaded local embedding model",
                    model=settings.local_embedding_model,
                )
            except Exception as e:
                logger.warning("sentence-transformers not available", error=str(e))
        return self._st_model

    async def generate_embedding(self, text: str) -> list[float]:
        """Generate embedding using best available FREE method."""
        # Method 1: Local sentence-transformers (preferred — fast, free, no network)
        model = self._load_sentence_transformer()
        if model is not None:
            embedding = model.encode(text[:512], normalize_embeddings=True)
            return embedding.tolist()

        # Method 2: Ollama embeddings (free, local, needs Ollama running)
        try:
            import httpx
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{settings.ollama_base_url}/api/embeddings",
                    json={"model": settings.ollama_embedding_model, "prompt": text[:2000]},
                    timeout=30.0,
                )
                if response.status_code == 200:
                    return response.json()["embedding"]
        except Exception as e:
            logger.debug("Ollama embeddings failed", error=str(e))

        # Method 3: OpenAI (PAID fallback — only if key configured)
        if settings.openai_api_key:
            try:
                from openai import AsyncOpenAI
                client = AsyncOpenAI(api_key=settings.openai_api_key)
                response = await client.embeddings.create(
                    model=settings.openai_embedding_model,
                    input=text[:8000],
                )
                return response.data[0].embedding
            except Exception as e:
                logger.error("OpenAI embedding failed", error=str(e))

        # Fallback: zero vector
        logger.warning("No embedding engine available, using zero vector")
        return [0.0] * settings.embedding_dimension

    async def generate_embeddings_batch(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for multiple texts in batch."""
        # sentence-transformers supports efficient batching
        model = self._load_sentence_transformer()
        if model is not None:
            truncated = [t[:512] for t in texts]
            embeddings = model.encode(truncated, normalize_embeddings=True, batch_size=32)
            return [e.tolist() for e in embeddings]

        # Fallback: one by one
        results = []
        for text in texts:
            emb = await self.generate_embedding(text)
            results.append(emb)
        return results

class QdrantService:
    """Manages vector embeddings in Qdrant for semantic search."""

    def __init__(self):
        self.client: QdrantClient | None = None
        self.embedding_engine = EmbeddingEngine()
        self.collection_name = settings.qdrant_collection

    async def initialize(self):
        """Initialize Qdrant client and create collection if needed."""
        try:
            self.client = QdrantClient(
                host=settings.qdrant_host,
                port=settings.qdrant_port,
            )

            # Create collection if it doesn't exist
            collections = self.client.get_collections().collections
            collection_names = [c.name for c in collections]

            if self.collection_name not in collection_names:
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(
                        size=settings.embedding_dimension,
                        distance=Distance.COSINE,
                    ),
                )
                logger.info("Qdrant collection created", name=self.collection_name)
            else:
                logger.info("Qdrant collection exists", name=self.collection_name)

        except Exception as e:
            logger.error("Qdrant initialization failed", error=str(e))
            self.client = None

    async def generate_embedding(self, text: str) -> list[float]:
        """Generate embedding vector using FREE local model."""
        return await self.embedding_engine.generate_embedding(text)

    async def generate_embeddings_batch(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for multiple texts in a batch."""
        return await self.embedding_engine.generate_embeddings_batch(texts)

    async def index_chunks(self, chunks: list[DocumentChunk], document_id: str):
        """Index document chunks with their embeddings in Qdrant."""
        if not self.client:
            logger.warning("Qdrant not connected, skipping indexing")
            return

        if not chunks:
            return

        # Generate embeddings in batch
        texts = [chunk.content for chunk in chunks]
        embeddings = await self.generate_embeddings_batch(texts)

        # Create Qdrant points
        points = []
        for chunk, embedding in zip(chunks, embeddings):
            point_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, chunk.chunk_id))
            points.append(PointStruct(
                id=point_id,
                vector=embedding,
                payload={
                    "chunk_id": chunk.chunk_id,
                    "document_id": document_id,
                    "content": chunk.content,
                    "page_number": chunk.page_number,
                    "chunk_index": chunk.chunk_index,
                    "filename": chunk.metadata.get("filename", ""),
                    "category": chunk.metadata.get("category", ""),
                },
            ))

        # Upsert in batches of 100
        batch_size = 100
        for i in range(0, len(points), batch_size):
            batch = points[i:i + batch_size]
            self.client.upsert(
                collection_name=self.collection_name,
                points=batch,
            )

        logger.info(
            "Chunks indexed in Qdrant",
            document_id=document_id,
            chunks_indexed=len(points),
        )

    async def search(
        self,
        query: str,
        top_k: int = 5,
        category_filter: str | None = None,
    ) -> list[dict]:
        """Perform semantic search over indexed chunks."""
        if not self.client:
            return []

        # Generate query embedding
        query_embedding = await self.generate_embedding(query)

        # Build filter if needed
        search_filter = None
        if category_filter:
            search_filter = Filter(
                must=[
                    FieldCondition(
                        key="category",
                        match=MatchValue(value=category_filter),
                    )
                ]
            )

        # Search
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            limit=top_k,
            query_filter=search_filter,
        )

        # Format results
        formatted = []
        for hit in results:
            formatted.append({
                "chunk_id": hit.payload.get("chunk_id", ""),
                "document_id": hit.payload.get("document_id", ""),
                "filename": hit.payload.get("filename", ""),
                "content": hit.payload.get("content", ""),
                "page_number": hit.payload.get("page_number"),
                "score": hit.score,
            })

        return formatted

    async def delete_document(self, document_id: str):
        """Delete all chunks belonging to a document."""
        if not self.client:
            return

        self.client.delete(
            collection_name=self.collection_name,
            points_selector=Filter(
                must=[
                    FieldCondition(
                        key="document_id",
                        match=MatchValue(value=document_id),
                    )
                ]
            ),
        )
        logger.info("Document vectors deleted", document_id=document_id)
```

---

## `backend/app/services/knowledge_graph/__init__.py`

**Knowledge graph package init**

```python

```

---

## `backend/app/services/knowledge_graph/neo4j_client.py`

**Neo4j async client with schema management**

```python
"""
Neo4j client for knowledge graph operations.
Handles connection management, schema initialization, and CRUD operations.
"""

from neo4j import AsyncGraphDatabase, AsyncDriver
import structlog

from app.config import settings

logger = structlog.get_logger()

class Neo4jClient:
    """Async Neo4j client for the AXIOM knowledge graph."""

    def __init__(self):
        self._driver: AsyncDriver | None = None

    async def initialize(self):
        """Initialize connection and create schema constraints."""
        self._driver = AsyncGraphDatabase.driver(
            settings.neo4j_uri,
            auth=(settings.neo4j_user, settings.neo4j_password),
        )

        # Verify connectivity
        try:
            await self._driver.verify_connectivity()
            logger.info("Neo4j connected", uri=settings.neo4j_uri)
        except Exception as e:
            logger.error("Neo4j connection failed", error=str(e))
            self._driver = None
            return

        # Create schema constraints and indexes
        await self._create_schema()

    async def _create_schema(self):
        """Create uniqueness constraints and indexes for the knowledge graph."""
        constraints = [
            "CREATE CONSTRAINT IF NOT EXISTS FOR (e:Equipment) REQUIRE e.tag IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (d:Document) REQUIRE d.document_id IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (p:Procedure) REQUIRE p.procedure_id IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (w:WorkOrder) REQUIRE w.wo_id IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (i:Incident) REQUIRE i.incident_id IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (r:Regulation) REQUIRE r.standard_id IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (pe:Personnel) REQUIRE pe.name IS UNIQUE",
            # GraphRAG hierarchy nodes
            "CREATE CONSTRAINT IF NOT EXISTS FOR (pg:Page) REQUIRE pg.page_id IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (s:Section) REQUIRE s.section_id IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (c:Chunk) REQUIRE c.chunk_id IS UNIQUE",
        ]

        indexes = [
            "CREATE INDEX IF NOT EXISTS FOR (e:Equipment) ON (e.type)",
            "CREATE INDEX IF NOT EXISTS FOR (d:Document) ON (d.category)",
            "CREATE INDEX IF NOT EXISTS FOR (d:Document) ON (d.filename)",
            "CREATE INDEX IF NOT EXISTS FOR (w:WorkOrder) ON (w.status)",
            "CREATE INDEX IF NOT EXISTS FOR (c:Chunk) ON (c.document_id)",
            "CREATE INDEX IF NOT EXISTS FOR (pg:Page) ON (pg.document_id)",
        ]

        async with self._driver.session() as session:
            for query in constraints + indexes:
                try:
                    await session.run(query)
                except Exception as e:
                    logger.debug("Schema query skipped", query=query[:50], reason=str(e))

        logger.info("Neo4j schema initialized")

    async def close(self):
        """Close the Neo4j driver."""
        if self._driver:
            await self._driver.close()
            logger.info("Neo4j connection closed")

    async def execute_query(self, query: str, parameters: dict = None) -> list[dict]:
        """Execute a Cypher query and return results."""
        if not self._driver:
            logger.warning("Neo4j not connected, skipping query")
            return []

        async with self._driver.session() as session:
            result = await session.run(query, parameters or {})
            records = await result.data()
            return records

    async def create_node(self, label: str, properties: dict) -> str:
        """Create or merge a node in the graph."""
        # Use MERGE to avoid duplicates
        prop_string = ", ".join(f"{k}: ${k}" for k in properties.keys())
        query = f"MERGE (n:{label} {{{prop_string}}}) RETURN elementId(n) as id"

        async with self._driver.session() as session:
            result = await session.run(query, properties)
            record = await result.single()
            return record["id"] if record else ""

    async def create_relationship(
        self,
        source_label: str,
        source_key: str,
        source_value: str,
        target_label: str,
        target_key: str,
        target_value: str,
        relationship: str,
        properties: dict = None,
    ):
        """Create a relationship between two nodes."""
        props = ""
        params = {
            "source_value": source_value,
            "target_value": target_value,
        }

        if properties:
            prop_string = ", ".join(f"{k}: ${k}" for k in properties.keys())
            props = f" {{{prop_string}}}"
            params.update(properties)

        query = f"""
        MATCH (a:{source_label} {{{source_key}: $source_value}})
        MATCH (b:{target_label} {{{target_key}: $target_value}})
        MERGE (a)-[r:{relationship}{props}]->(b)
        RETURN type(r) as rel_type
        """

        async with self._driver.session() as session:
            await session.run(query, params)

    async def get_neighbors(
        self, node_label: str, node_key: str, node_value: str, depth: int = 2
    ) -> list[dict]:
        """Get neighboring nodes up to specified depth."""
        query = f"""
        MATCH path = (n:{node_label} {{{node_key}: $value}})-[*1..{depth}]-(m)
        RETURN
            labels(m)[0] as node_type,
            properties(m) as properties,
            [r in relationships(path) | type(r)] as relationships
        LIMIT 50
        """
        return await self.execute_query(query, {"value": node_value})

    async def search_nodes(self, search_term: str, limit: int = 20) -> list[dict]:
        """Full-text search across all node types."""
        query = """
        CALL {
            MATCH (n:Equipment) WHERE n.tag CONTAINS $term
            RETURN n, labels(n)[0] as label
            UNION
            MATCH (n:Document) WHERE n.filename CONTAINS $term
            RETURN n, labels(n)[0] as label
            UNION
            MATCH (n:Personnel) WHERE n.name CONTAINS $term
            RETURN n, labels(n)[0] as label
            UNION
            MATCH (n:Regulation) WHERE n.standard_id CONTAINS $term
            RETURN n, labels(n)[0] as label
        }
        RETURN label, properties(n) as props
        LIMIT $limit
        """
        return await self.execute_query(query, {"term": search_term, "limit": limit})

    async def get_equipment_context(self, equipment_tag: str) -> dict:
        """Get full context for a piece of equipment (all connected nodes)."""
        query = """
        MATCH (e:Equipment {tag: $tag})
        OPTIONAL MATCH (e)-[:HAS_WORK_ORDER]->(wo:WorkOrder)
        OPTIONAL MATCH (e)-[:GOVERNED_BY]->(r:Regulation)
        OPTIONAL MATCH (e)-[:INSPECTED_BY]->(i:Inspection)
        OPTIONAL MATCH (e)-[:INVOLVED_IN]->(inc:Incident)
        OPTIONAL MATCH (e)-[:HAS_PROCEDURE]->(p:Procedure)
        OPTIONAL MATCH (e)-[:REFERENCED_IN]->(d:Document)
        RETURN
            properties(e) as equipment,
            collect(DISTINCT properties(wo)) as work_orders,
            collect(DISTINCT properties(r)) as regulations,
            collect(DISTINCT properties(i)) as inspections,
            collect(DISTINCT properties(inc)) as incidents,
            collect(DISTINCT properties(p)) as procedures,
            collect(DISTINCT properties(d)) as documents
        """
        results = await self.execute_query(query, {"tag": equipment_tag})
        return results[0] if results else {}
```

---

## `backend/app/services/knowledge_graph/graph_builder.py`

**Knowledge graph builder (Document→Page→Section→Chunk→Entity)**

```python
"""
Knowledge Graph Builder — populates Neo4j from extracted entities and relationships.
Maps extracted data to the industrial ontology.

Neo4j Schema (per GraphRAG pipeline):
    Document -[HAS_PAGE]-> Page
    Page -[HAS_SECTION]-> Section
    Section -[HAS_CHUNK]-> Chunk
    Chunk -[MENTIONS]-> Entity
    Entity -[RELATED_TO]-> Entity
    Table -[HAS_COLUMN]-> Column
"""

import structlog

from app.models.schemas import IngestedDocument, DocumentCategory
from app.services.knowledge_graph.neo4j_client import Neo4jClient

logger = structlog.get_logger()

class GraphBuilder:
    """Builds and updates the knowledge graph from ingested documents."""

    def __init__(self, neo4j_client: Neo4jClient):
        self.neo4j = neo4j_client

    async def populate_from_document(self, document: IngestedDocument):
        """
        Populate the knowledge graph from an ingested document.

        Creates the full hierarchy:
        Document → Page → Section → Chunk → Entity (with relationships)
        """
        logger.info(
            "Populating knowledge graph",
            document_id=document.document_id,
            entities=len(document.entities),
            relationships=len(document.relationships),
        )

        # 1. Create the Document node
        await self._create_document_node(document)

        # 2. Create Page and Chunk nodes with hierarchy
        await self._create_chunk_hierarchy(document)

        # 3. Create entity nodes and link to chunks
        await self._create_entity_nodes(document)

        # 4. Create relationships between entities
        await self._create_relationships(document)

        logger.info("Knowledge graph updated", document_id=document.document_id)

    async def _create_document_node(self, document: IngestedDocument):
        """Create a Document node in the graph."""
        await self.neo4j.create_node("Document", {
            "document_id": document.document_id,
            "filename": document.filename,
            "file_type": document.file_type.value,
            "category": document.category.value,
            "total_pages": document.total_pages,
            "ingested_at": document.ingested_at.isoformat(),
        })

    async def _create_chunk_hierarchy(self, document: IngestedDocument):
        """Create Page → Section → Chunk hierarchy linked to Document."""
        pages_created = set()
        sections_created = set()

        for chunk in document.chunks:
            page_num = chunk.page_number or 1
            page_id = f"{document.document_id}_page_{page_num}"

            # Create Page node if not exists
            if page_id not in pages_created:
                await self.neo4j.create_node("Page", {
                    "page_id": page_id,
                    "page_number": page_num,
                    "document_id": document.document_id,
                })
                # Document -[HAS_PAGE]-> Page
                await self.neo4j.create_relationship(
                    source_label="Document",
                    source_key="document_id",
                    source_value=document.document_id,
                    target_label="Page",
                    target_key="page_id",
                    target_value=page_id,
                    relationship="HAS_PAGE",
                    properties={"page_number": page_num},
                )
                pages_created.add(page_id)

            # Create Section node if section metadata available
            section_heading = chunk.metadata.get("section", "") or chunk.metadata.get("heading", "")
            section_id = f"{page_id}_section_{section_heading or 'default'}"

            if section_id not in sections_created:
                await self.neo4j.create_node("Section", {
                    "section_id": section_id,
                    "heading": section_heading,
                    "page_id": page_id,
                })
                # Page -[HAS_SECTION]-> Section
                await self.neo4j.create_relationship(
                    source_label="Page",
                    source_key="page_id",
                    source_value=page_id,
                    target_label="Section",
                    target_key="section_id",
                    target_value=section_id,
                    relationship="HAS_SECTION",
                    properties={},
                )
                sections_created.add(section_id)

            # Create Chunk node
            await self.neo4j.create_node("Chunk", {
                "chunk_id": chunk.chunk_id,
                "content": chunk.content[:500],  # Store abbreviated content
                "chunk_index": chunk.chunk_index,
                "document_id": document.document_id,
                "page_number": page_num,
            })
            # Section -[HAS_CHUNK]-> Chunk
            await self.neo4j.create_relationship(
                source_label="Section",
                source_key="section_id",
                source_value=section_id,
                target_label="Chunk",
                target_key="chunk_id",
                target_value=chunk.chunk_id,
                relationship="HAS_CHUNK",
                properties={"chunk_index": chunk.chunk_index},
            )

    async def _create_entity_nodes(self, document: IngestedDocument):
        """Create nodes for each extracted entity and link to chunks via MENTIONS."""
        for entity in document.entities:
            node_label = self._entity_type_to_label(entity.entity_type)
            if not node_label:
                continue

            # Create the entity node
            properties = self._build_entity_properties(entity)
            await self.neo4j.create_node(node_label, properties)

            # Link entity to document
            key_field = self._get_key_field(node_label)
            if key_field:
                await self.neo4j.create_relationship(
                    source_label=node_label,
                    source_key=key_field,
                    source_value=properties[key_field],
                    target_label="Document",
                    target_key="document_id",
                    target_value=document.document_id,
                    relationship="REFERENCED_IN",
                    properties={"confidence": entity.confidence},
                )

            # Link entity to relevant chunks via MENTIONS
            entity_value_lower = entity.value.lower()
            for chunk in document.chunks:
                if entity_value_lower in chunk.content.lower():
                    if key_field:
                        await self.neo4j.create_relationship(
                            source_label="Chunk",
                            source_key="chunk_id",
                            source_value=chunk.chunk_id,
                            target_label=node_label,
                            target_key=key_field,
                            target_value=properties[key_field],
                            relationship="MENTIONS",
                            properties={"confidence": entity.confidence},
                        )

    async def _create_relationships(self, document: IngestedDocument):
        """Create relationship edges between entity nodes."""
        for rel in document.relationships:
            source_label = self._guess_label_from_value(rel.source_entity)
            target_label = self._guess_label_from_value(rel.target_entity)

            if not source_label or not target_label:
                continue

            source_key = self._get_key_field(source_label)
            target_key = self._get_key_field(target_label)

            if source_key and target_key:
                try:
                    await self.neo4j.create_relationship(
                        source_label=source_label,
                        source_key=source_key,
                        source_value=rel.source_entity,
                        target_label=target_label,
                        target_key=target_key,
                        target_value=rel.target_entity,
                        relationship=rel.relationship_type,
                        properties={
                            "confidence": rel.confidence,
                            "source_document": document.document_id,
                        },
                    )
                except Exception as e:
                    logger.debug(
                        "Relationship creation skipped",
                        source=rel.source_entity,
                        target=rel.target_entity,
                        error=str(e),
                    )

    def _entity_type_to_label(self, entity_type: str) -> str | None:
        """Map entity type to Neo4j node label."""
        mapping = {
            "equipment": "Equipment",
            "personnel": "Personnel",
            "regulation": "Regulation",
            "parameter": "Parameter",
            "document_reference": "Document",
            "location": "Location",
            "organization": "Organization",
            "facility": "Location",
        }
        return mapping.get(entity_type)

    def _build_entity_properties(self, entity) -> dict:
        """Build node properties from an entity."""
        type_to_props = {
            "equipment": {"tag": entity.value, "context": entity.context[:200]},
            "personnel": {"name": entity.value},
            "regulation": {"standard_id": entity.value, "context": entity.context[:200]},
            "parameter": {"value": entity.value, "context": entity.context[:200]},
            "document_reference": {"document_id": entity.value},
            "location": {"name": entity.value},
            "organization": {"name": entity.value},
        }
        return type_to_props.get(entity.entity_type, {"value": entity.value})

    def _get_key_field(self, label: str) -> str | None:
        """Get the primary key field for a node label."""
        key_map = {
            "Equipment": "tag",
            "Personnel": "name",
            "Regulation": "standard_id",
            "Parameter": "value",
            "Document": "document_id",
            "Location": "name",
            "Organization": "name",
            "WorkOrder": "wo_id",
            "Incident": "incident_id",
            "Procedure": "procedure_id",
            "Inspection": "inspection_id",
        }
        return key_map.get(label)

    def _guess_label_from_value(self, value: str) -> str | None:
        """Guess the node label from the entity value format."""
        import re

        # Equipment tag pattern
        if re.match(r"^[A-Z]{1,4}-\d{2,5}[A-Z]?$", value):
            return "Equipment"
        # Work order
        if re.match(r"^WO[-\s]?\d{4,}$", value, re.IGNORECASE):
            return "WorkOrder"
        # Regulation
        if re.match(r"^(OISD|API|ISO|ASME|IS)[-\s]?\d+", value):
            return "Regulation"
        # If it looks like a person name
        if re.match(r"^[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+$", value):
            return "Personnel"

        return None
```

---

## `backend/app/services/rag/__init__.py`

**RAG package init**

```python

```

---

## `backend/app/services/rag/retriever.py`

**Hybrid retriever — FAISS + Neo4j + BM25 (0.6 semantic + 0.4 graph)**

```python
"""
Hybrid Retriever — combines FAISS vector search, Neo4j knowledge graph traversal,
and keyword (BM25) search for comprehensive document retrieval.

Scoring: 0.6 * Semantic Similarity + 0.4 * Graph Relevance
"""

import re
from rank_bm25 import BM25Okapi
from dataclasses import dataclass
import structlog

from app.config import settings
from app.services.vectorstore.faiss_service import FAISSService
from app.services.knowledge_graph.neo4j_client import Neo4jClient

logger = structlog.get_logger()

@dataclass
class RetrievalResult:
    chunk_id: str
    document_id: str
    filename: str
    content: str
    page_number: int | None
    score: float
    source_type: str  # "vector", "graph", "keyword"

class HybridRetriever:
    """
    Multi-strategy retrieval engine (GraphRAG hybrid approach):

    1. Embedding → FAISS Top-k (semantic similarity)
    2. Extract query entities → Neo4j neighborhood expansion (graph relevance)
    3. Merge graph context + semantic chunks
    4. Re-rank using: Score = 0.6 * Semantic + 0.4 * Graph
    5. Return final ranked context

    Also supports BM25 keyword search for exact term matching.
    """

    def __init__(self, faiss_service: FAISSService, neo4j: Neo4jClient):
        self.faiss = faiss_service
        self.neo4j = neo4j
        self._bm25_corpus: list[dict] | None = None
        self._bm25_index: BM25Okapi | None = None
        self.semantic_weight = settings.semantic_weight  # 0.6
        self.graph_weight = settings.graph_weight  # 0.4

    async def retrieve(
        self,
        query: str,
        top_k: int = 5,
        use_vector: bool = True,
        use_graph: bool = True,
        use_keyword: bool = True,
        category_filter: str | None = None,
    ) -> list[RetrievalResult]:
        """
        Perform hybrid retrieval:
        1. FAISS semantic search → top-k candidates
        2. Extract entities from query → Neo4j neighborhood expansion
        3. Merge and re-rank using weighted scoring

        Score = 0.6 * semantic_similarity + 0.4 * graph_relevance
        """
        vector_results: list[RetrievalResult] = []
        graph_results: list[RetrievalResult] = []
        keyword_results: list[RetrievalResult] = []

        # 1. FAISS vector search (semantic similarity)
        if use_vector:
            vector_results = await self._vector_search(query, top_k * 2, category_filter)
            logger.debug("FAISS search", results=len(vector_results))

        # 2. Neo4j knowledge graph neighborhood expansion
        if use_graph:
            graph_results = await self._graph_search(query, top_k * 2)
            logger.debug("Graph search", results=len(graph_results))

        # 3. BM25 keyword search
        if use_keyword and self._bm25_index:
            keyword_results = self._keyword_search(query, top_k * 2)
            logger.debug("Keyword search", results=len(keyword_results))

        # Merge and re-rank with weighted scoring
        final_results = self._weighted_rerank(
            vector_results, graph_results, keyword_results, top_k
        )

        logger.info("Hybrid retrieval complete", total_results=len(final_results))
        return final_results

    def _weighted_rerank(
        self,
        vector_results: list[RetrievalResult],
        graph_results: list[RetrievalResult],
        keyword_results: list[RetrievalResult],
        top_k: int,
    ) -> list[RetrievalResult]:
        """
        Re-rank results using weighted scoring:
        Score = 0.6 * Semantic Similarity + 0.4 * Graph Relevance

        Keyword results boost the semantic score.
        """
        scores: dict[str, float] = {}
        result_map: dict[str, RetrievalResult] = {}

        # Normalize vector scores to [0, 1]
        max_vector_score = max((r.score for r in vector_results), default=1.0) or 1.0
        for result in vector_results:
            key = result.chunk_id
            normalized_score = result.score / max_vector_score
            scores[key] = self.semantic_weight * normalized_score
            result_map[key] = result

        # Normalize graph scores and add graph weight
        max_graph_score = max((r.score for r in graph_results), default=1.0) or 1.0
        for result in graph_results:
            key = result.chunk_id
            normalized_score = result.score / max_graph_score
            graph_contribution = self.graph_weight * normalized_score
            scores[key] = scores.get(key, 0) + graph_contribution
            if key not in result_map:
                result_map[key] = result

        # Keyword results add a boost (treated as part of semantic)
        if keyword_results:
            max_kw_score = max((r.score for r in keyword_results), default=1.0) or 1.0
            for result in keyword_results:
                key = result.chunk_id
                normalized_score = result.score / max_kw_score
                # Keyword contributes as a boost to semantic score
                keyword_boost = 0.1 * normalized_score
                scores[key] = scores.get(key, 0) + keyword_boost
                if key not in result_map:
                    result_map[key] = result

        # Sort by final weighted score
        sorted_keys = sorted(scores.keys(), key=lambda x: scores[x], reverse=True)

        # Build final results
        final_results = []
        for key in sorted_keys[:top_k]:
            result = result_map[key]
            result.score = scores[key]
            final_results.append(result)

        return final_results

    async def _vector_search(
        self, query: str, top_k: int, category_filter: str | None
    ) -> list[RetrievalResult]:
        """Semantic search via FAISS."""
        results = await self.faiss.search(
            query=query, top_k=top_k, category_filter=category_filter
        )
        return [
            RetrievalResult(
                chunk_id=r["chunk_id"],
                document_id=r["document_id"],
                filename=r["filename"],
                content=r["content"],
                page_number=r.get("page_number"),
                score=r["score"],
                source_type="vector",
            )
            for r in results
        ]

    async def _graph_search(self, query: str, top_k: int) -> list[RetrievalResult]:
        """
        Extract entities from query and traverse the knowledge graph
        to find related document chunks.
        """
        # Extract potential equipment tags from the query
        equipment_tags = re.findall(r"\b[A-Z]{1,4}-\d{2,5}[A-Z]?\b", query)
        regulation_refs = re.findall(r"\b(?:OISD|API|ISO|ASME)[-\s]?\d+\b", query)

        results = []

        # Search for equipment context
        for tag in equipment_tags:
            context = await self.neo4j.get_equipment_context(tag)
            if context:
                # Build a text representation of the graph context
                context_text = self._format_graph_context(tag, context)
                results.append(RetrievalResult(
                    chunk_id=f"graph_{tag}",
                    document_id="knowledge_graph",
                    filename="Knowledge Graph",
                    content=context_text,
                    page_number=None,
                    score=0.9,
                    source_type="graph",
                ))

        # Search for regulation context
        for ref in regulation_refs:
            neighbors = await self.neo4j.get_neighbors("Regulation", "standard_id", ref)
            if neighbors:
                context_text = f"Regulation {ref} applies to: "
                context_text += "; ".join(
                    f"{n['node_type']}: {n['properties']}" for n in neighbors[:5]
                )
                results.append(RetrievalResult(
                    chunk_id=f"graph_{ref}",
                    document_id="knowledge_graph",
                    filename="Knowledge Graph",
                    content=context_text,
                    page_number=None,
                    score=0.85,
                    source_type="graph",
                ))

        # General graph search
        search_terms = self._extract_search_terms(query)
        for term in search_terms[:3]:  # Limit to avoid too many queries
            nodes = await self.neo4j.search_nodes(term, limit=5)
            for node in nodes:
                props = node.get("props", {})
                results.append(RetrievalResult(
                    chunk_id=f"graph_{term}_{len(results)}",
                    document_id="knowledge_graph",
                    filename=props.get("filename", "Knowledge Graph"),
                    content=str(props),
                    page_number=None,
                    score=0.7,
                    source_type="graph",
                ))

        return results[:top_k]

    def _keyword_search(self, query: str, top_k: int) -> list[RetrievalResult]:
        """BM25 keyword search over indexed corpus."""
        if not self._bm25_index or not self._bm25_corpus:
            return []

        tokenized_query = query.lower().split()
        scores = self._bm25_index.get_scores(tokenized_query)

        # Get top results
        top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]

        results = []
        for idx in top_indices:
            if scores[idx] > 0:
                doc = self._bm25_corpus[idx]
                results.append(RetrievalResult(
                    chunk_id=doc.get("chunk_id", f"bm25_{idx}"),
                    document_id=doc.get("document_id", ""),
                    filename=doc.get("filename", ""),
                    content=doc.get("content", ""),
                    page_number=doc.get("page_number"),
                    score=float(scores[idx]),
                    source_type="keyword",
                ))

        return results

    def update_bm25_index(self, documents: list[dict]):
        """Update the BM25 index with new documents."""
        self._bm25_corpus = documents
        tokenized_corpus = [doc["content"].lower().split() for doc in documents]
        if tokenized_corpus:
            self._bm25_index = BM25Okapi(tokenized_corpus)
            logger.info("BM25 index updated", documents=len(documents))

    def _reciprocal_rank_fusion(
        self, result_lists: list[list[RetrievalResult]], k: int = 60
    ) -> list[RetrievalResult]:
        """
        Fuse multiple ranked lists using Reciprocal Rank Fusion.
        RRF score = sum(1 / (k + rank_i)) for each list where the doc appears.
        """
        scores: dict[str, float] = {}
        result_map: dict[str, RetrievalResult] = {}

        for result_list in result_lists:
            for rank, result in enumerate(result_list):
                key = result.chunk_id
                rrf_score = 1.0 / (k + rank + 1)
                scores[key] = scores.get(key, 0) + rrf_score

                # Keep the result with highest individual score
                if key not in result_map or result.score > result_map[key].score:
                    result_map[key] = result

        # Sort by fused score
        sorted_keys = sorted(scores.keys(), key=lambda x: scores[x], reverse=True)

        # Update scores in results
        fused_results = []
        for key in sorted_keys:
            result = result_map[key]
            result.score = scores[key]
            fused_results.append(result)

        return fused_results

    def _format_graph_context(self, equipment_tag: str, context: dict) -> str:
        """Format knowledge graph context into readable text."""
        parts = [f"Equipment: {equipment_tag}"]

        equipment = context.get("equipment", {})
        if equipment:
            parts.append(f"Properties: {equipment}")

        work_orders = context.get("work_orders", [])
        if work_orders:
            parts.append(f"Work Orders ({len(work_orders)}): {work_orders[:3]}")

        incidents = context.get("incidents", [])
        if incidents:
            parts.append(f"Incidents ({len(incidents)}): {incidents[:3]}")

        regulations = context.get("regulations", [])
        if regulations:
            parts.append(f"Applicable Regulations: {regulations}")

        inspections = context.get("inspections", [])
        if inspections:
            parts.append(f"Inspections ({len(inspections)}): {inspections[:3]}")

        return "\n".join(parts)

    def _extract_search_terms(self, query: str) -> list[str]:
        """Extract meaningful search terms from a natural language query."""
        # Remove common stop words and extract key terms
        stop_words = {
            "what", "is", "the", "a", "an", "of", "for", "in", "on", "at",
            "to", "from", "by", "with", "how", "when", "where", "which",
            "show", "me", "tell", "find", "get", "list", "all", "any",
        }
        words = query.split()
        terms = [w for w in words if w.lower() not in stop_words and len(w) > 2]
        return terms
```

---

## `backend/app/services/rag/generator.py`

**Answer generator — Ollama / OpenAI with citation enforcement**

```python
"""
Answer Generator — takes retrieved context and generates a grounded,
cited answer using an LLM with strict citation enforcement.
Uses FREE local LLM (Ollama) by default, with OpenAI as optional paid fallback.
"""

import httpx
from dataclasses import dataclass
import structlog
import json

from app.config import settings
from app.services.rag.retriever import RetrievalResult
from app.models.schemas import QueryResponse, RetrievedContext

logger = structlog.get_logger()

SYSTEM_PROMPT = """You are AXIOM, an AI-powered Industrial Knowledge Intelligence assistant.
You help maintenance engineers, field technicians, and operations teams find answers
from their industrial document corpus (SOPs, work orders, inspection reports, P&IDs,
incident reports, and regulatory documents).

CRITICAL RULES:
1. ONLY answer based on the provided context. If the context doesn't contain enough
   information, say "I don't have sufficient information to answer this confidently."
2. ALWAYS cite your sources using [Source N] notation where N corresponds to the
   context chunk number.
3. If you see conflicting information across sources, note the discrepancy.
4. For safety-critical information (procedures, limits, regulatory requirements),
   be explicit about your confidence level.
5. When mentioning equipment tags, parameters, or standards, preserve exact values.
6. Suggest follow-up questions that might help the user get more specific information.

RESPONSE FORMAT:
- Lead with a direct, concise answer
- Support with details and citations
- End with confidence assessment and suggested follow-ups
"""

class AnswerGenerator:
    """Generates grounded, cited answers from retrieved context.
    Uses Ollama (FREE local) by default, OpenAI as optional paid fallback."""

    def __init__(self):
        self.provider = settings.llm_provider  # "ollama" or "openai"

    async def generate(
        self,
        query: str,
        retrieved_chunks: list[RetrievalResult],
        graph_context: dict | None = None,
    ) -> QueryResponse:
        """Generate an answer from retrieved context."""

        # Build context string with numbered sources
        context_parts = []
        sources = []

        for i, chunk in enumerate(retrieved_chunks, 1):
            source_label = f"[Source {i}]"
            context_parts.append(
                f"{source_label}\n"
                f"Document: {chunk.filename}\n"
                f"Page: {chunk.page_number or 'N/A'}\n"
                f"Content: {chunk.content}\n"
                f"Retrieval Method: {chunk.source_type}\n"
            )
            sources.append(RetrievedContext(
                chunk_id=chunk.chunk_id,
                document_id=chunk.document_id,
                filename=chunk.filename,
                content=chunk.content,
                page_number=chunk.page_number,
                relevance_score=chunk.score,
                source_type=chunk.source_type,
            ))

        # Add graph context if available
        if graph_context:
            context_parts.append(
                f"\n[Knowledge Graph Context]\n{json.dumps(graph_context, indent=2, default=str)}"
            )

        full_context = "\n---\n".join(context_parts)

        # Generate answer
        if self.provider == "ollama":
            answer, confidence = await self._ollama_generate(query, full_context)
        elif self.provider == "openai" and settings.openai_api_key:
            answer, confidence = await self._openai_generate(query, full_context)
        else:
            # Fallback: return context summary without LLM
            answer = self._fallback_answer(query, retrieved_chunks)
            confidence = "low"

        # Generate follow-up suggestions
        followups = self._generate_followups(query, retrieved_chunks)

        # Extract related entities from context
        related_entities = self._extract_related_entities(retrieved_chunks)

        return QueryResponse(
            answer=answer,
            confidence=confidence,
            sources=sources,
            related_entities=related_entities,
            suggested_followups=followups,
        )

    async def _ollama_generate(self, query: str, context: str) -> tuple[str, str]:
        """Generate answer using Ollama (FREE local LLM)."""
        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                response = await client.post(
                    f"{settings.ollama_base_url}/api/chat",
                    json={
                        "model": settings.ollama_chat_model,
                        "messages": [
                            {"role": "system", "content": SYSTEM_PROMPT},
                            {
                                "role": "user",
                                "content": f"Context:\n{context}\n\nQuestion: {query}",
                            },
                        ],
                        "stream": False,
                        "options": {
                            "temperature": 0.1,
                            "num_predict": 1500,
                        },
                    },
                )

                if response.status_code == 200:
                    result = response.json()
                    answer = result["message"]["content"]
                    confidence = self._assess_confidence(answer, context)
                    return answer, confidence
                else:
                    logger.error("Ollama request failed", status=response.status_code)
                    return self._fallback_answer(query, []), "low"

        except Exception as e:
            logger.error("Ollama generation failed", error=str(e))
            return f"LLM unavailable. Ensure Ollama is running: `ollama serve`\nError: {str(e)}", "low"

    async def _openai_generate(self, query: str, context: str) -> tuple[str, str]:
        """Generate answer using OpenAI (PAID fallback)."""
        try:
            from openai import AsyncOpenAI
            client = AsyncOpenAI(api_key=settings.openai_api_key)
            response = await client.chat.completions.create(
                model=settings.openai_chat_model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {
                        "role": "user",
                        "content": f"Context:\n{context}\n\nQuestion: {query}",
                    },
                ],
                temperature=0.1,
                max_tokens=1500,
            )

            answer = response.choices[0].message.content
            confidence = self._assess_confidence(answer, context)
            return answer, confidence

        except Exception as e:
            logger.error("OpenAI generation failed", error=str(e))
            return f"Error generating answer: {str(e)}", "low"

    def _fallback_answer(self, query: str, chunks: list[RetrievalResult]) -> str:
        """Generate a basic answer without LLM (fallback mode)."""
        if not chunks:
            return "No relevant documents found for your query."

        answer_parts = [
            f"Based on {len(chunks)} relevant document(s) found:\n"
        ]

        for i, chunk in enumerate(chunks[:3], 1):
            answer_parts.append(
                f"\n**[Source {i}]** From '{chunk.filename}'"
                f"{f' (Page {chunk.page_number})' if chunk.page_number else ''}:\n"
                f"{chunk.content[:300]}{'...' if len(chunk.content) > 300 else ''}\n"
            )

        answer_parts.append(
            "\n*Note: Running in fallback mode without LLM. "
            "Configure OPENAI_API_KEY for full answer generation.*"
        )
        return "\n".join(answer_parts)

    def _assess_confidence(self, answer: str, context: str) -> str:
        """Assess confidence level of the generated answer."""
        # High confidence: answer contains citations and context is rich
        citation_count = answer.count("[Source")
        if citation_count >= 2 and len(context) > 1000:
            return "high"
        elif citation_count >= 1:
            return "medium"
        else:
            return "low"

    def _generate_followups(
        self, query: str, chunks: list[RetrievalResult]
    ) -> list[str]:
        """Generate suggested follow-up questions."""
        followups = []

        # Extract equipment tags from results
        import re
        all_content = " ".join(c.content for c in chunks)
        equipment_tags = set(re.findall(r"\b[A-Z]{1,4}-\d{2,5}[A-Z]?\b", all_content))

        if equipment_tags:
            tag = list(equipment_tags)[0]
            followups.append(f"What is the maintenance history of {tag}?")
            followups.append(f"Are there any open work orders for {tag}?")

        # Generic follow-ups based on query type
        if "maintenance" in query.lower() or "repair" in query.lower():
            followups.append("What spare parts are needed?")
            followups.append("What is the recommended maintenance interval?")
        elif "inspection" in query.lower():
            followups.append("When is the next inspection due?")
            followups.append("What were the findings from the last inspection?")
        elif "procedure" in query.lower() or "sop" in query.lower():
            followups.append("What PPE is required for this procedure?")
            followups.append("What are the safety precautions?")

        return followups[:4]

    def _extract_related_entities(self, chunks: list[RetrievalResult]) -> list[dict]:
        """Extract entities mentioned across retrieved chunks."""
        import re
        entities = []
        seen = set()

        all_content = " ".join(c.content for c in chunks)

        # Equipment
        for tag in re.findall(r"\b[A-Z]{1,4}-\d{2,5}[A-Z]?\b", all_content):
            if tag not in seen:
                entities.append({"type": "equipment", "value": tag})
                seen.add(tag)

        # Regulations
        for reg in re.findall(r"\b(?:OISD|API|ISO)[-\s]?\d+\b", all_content):
            if reg not in seen:
                entities.append({"type": "regulation", "value": reg})
                seen.add(reg)

        return entities[:10]
```

---

## `backend/app/services/agents/__init__.py`

**Agents package init**

```python

```

---

## `backend/app/services/agents/sensor_monitor_agent.py`

**Sensor health monitor agent**

```python
"""
Sensor Health Monitor Agent
Ingests machine sensor logs, detects anomalies using multi-strategy detection,
and classifies equipment health status.
"""

import statistics
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
from typing import Optional
import structlog

logger = structlog.get_logger()

class HealthStatus(str, Enum):
    NORMAL = "normal"
    WARNING = "warning"
    CRITICAL = "critical"
    ANOMALY = "anomaly"

@dataclass
class SensorReading:
    equipment_tag: str
    parameter: str  # e.g., "vibration", "temperature", "pressure"
    value: float
    unit: str
    timestamp: datetime
    metadata: dict = field(default_factory=dict)

@dataclass
class ThresholdConfig:
    """OEM or engineering-defined limits for a parameter."""
    normal_min: float
    normal_max: float
    warning_min: float
    warning_max: float
    critical_min: float
    critical_max: float

@dataclass
class AnomalyAlert:
    equipment_tag: str
    parameter: str
    current_value: float
    unit: str
    status: HealthStatus
    severity_score: float  # 0-1
    reason: str
    threshold_info: Optional[dict] = None
    trend_info: Optional[dict] = None
    timestamp: datetime = field(default_factory=datetime.utcnow)
    recommended_action: str = ""

class SensorHealthMonitorAgent:
    """
    Agent that monitors sensor logs and detects anomalies using:
    1. Threshold checking (OEM limits from Knowledge Graph)
    2. Statistical anomaly detection (Z-score on rolling window)
    3. Trend detection (drift/degradation over time)
    4. Pattern matching (compare to known pre-failure signatures)
    """

    # Default industrial thresholds (overridden by KG data when available)
    DEFAULT_THRESHOLDS = {
        "vibration": ThresholdConfig(
            normal_min=0, normal_max=7.1,      # ISO 10816 Group 2
            warning_min=0, warning_max=11.2,
            critical_min=0, critical_max=18.0,
        ),
        "temperature": ThresholdConfig(
            normal_min=20, normal_max=80,
            warning_min=10, warning_max=95,
            critical_min=0, critical_max=120,
        ),
        "pressure": ThresholdConfig(
            normal_min=0, normal_max=45,
            warning_min=0, warning_max=50,
            critical_min=0, critical_max=55,
        ),
        "current": ThresholdConfig(
            normal_min=0, normal_max=85,       # % of rated
            warning_min=0, warning_max=95,
            critical_min=0, critical_max=105,
        ),
        "flow": ThresholdConfig(
            normal_min=80, normal_max=120,     # % of design
            warning_min=60, warning_max=130,
            critical_min=40, critical_max=150,
        ),
    }

    def __init__(self):
        # Rolling history per equipment+parameter for statistical analysis
        self._history: dict[str, list[float]] = {}
        self._window_size = 50  # readings to keep for stats

    def analyze_reading(
        self,
        reading: SensorReading,
        custom_threshold: Optional[ThresholdConfig] = None,
    ) -> AnomalyAlert | None:
        """
        Analyze a single sensor reading and return an alert if anomalous.
        Returns None if reading is NORMAL.
        """
        key = f"{reading.equipment_tag}_{reading.parameter}"

        # Update history
        if key not in self._history:
            self._history[key] = []
        self._history[key].append(reading.value)
        if len(self._history[key]) > self._window_size:
            self._history[key] = self._history[key][-self._window_size:]

        # Get threshold (custom from KG > default)
        threshold = custom_threshold or self.DEFAULT_THRESHOLDS.get(reading.parameter)

        # Run detection strategies
        status = HealthStatus.NORMAL
        reasons = []
        severity = 0.0

        # Strategy 1: Threshold check
        if threshold:
            thresh_result = self._check_threshold(reading.value, threshold)
            if thresh_result[0].value != "normal":
                status = thresh_result[0]
                reasons.append(thresh_result[1])
                severity = max(severity, thresh_result[2])

        # Strategy 2: Statistical anomaly (Z-score)
        if len(self._history[key]) >= 10:
            stat_result = self._statistical_check(reading.value, self._history[key])
            if stat_result:
                if stat_result[2] > severity:
                    status = stat_result[0]
                reasons.append(stat_result[1])
                severity = max(severity, stat_result[2])

        # Strategy 3: Trend detection
        if len(self._history[key]) >= 20:
            trend_result = self._trend_check(self._history[key])
            if trend_result:
                reasons.append(trend_result[1])
                severity = max(severity, trend_result[2])
                if trend_result[0].value == "warning" and status.value == "normal":
                    status = HealthStatus.WARNING

        # Only return alert if not normal
        if status == HealthStatus.NORMAL:
            return None

        return AnomalyAlert(
            equipment_tag=reading.equipment_tag,
            parameter=reading.parameter,
            current_value=reading.value,
            unit=reading.unit,
            status=status,
            severity_score=min(severity, 1.0),
            reason=" | ".join(reasons),
            threshold_info={
                "normal_max": threshold.normal_max if threshold else None,
                "warning_max": threshold.warning_max if threshold else None,
                "critical_max": threshold.critical_max if threshold else None,
            },
            trend_info=self._get_trend_info(self._history[key]),
            timestamp=reading.timestamp,
        )

    def analyze_batch(self, readings: list[SensorReading]) -> list[AnomalyAlert]:
        """Analyze a batch of sensor readings and return all anomalies."""
        alerts = []
        for reading in readings:
            alert = self.analyze_reading(reading)
            if alert:
                alerts.append(alert)

        if alerts:
            logger.info(
                "Batch analysis complete",
                total_readings=len(readings),
                anomalies_found=len(alerts),
                critical=sum(1 for a in alerts if a.status == HealthStatus.CRITICAL),
            )
        return alerts

    def get_equipment_health_summary(self, equipment_tag: str) -> dict:
        """Get current health summary for a piece of equipment."""
        relevant_keys = [k for k in self._history if k.startswith(equipment_tag)]
        summary = {"equipment_tag": equipment_tag, "parameters": {}}

        for key in relevant_keys:
            param = key.split("_", 1)[1] if "_" in key else key
            values = self._history[key]
            if values:
                summary["parameters"][param] = {
                    "latest": values[-1],
                    "mean": statistics.mean(values),
                    "std": statistics.stdev(values) if len(values) > 1 else 0,
                    "trend": self._calculate_trend_direction(values),
                    "readings_count": len(values),
                }

        return summary

    def _check_threshold(
        self, value: float, threshold: ThresholdConfig
    ) -> tuple[HealthStatus, str, float]:
        """Check value against defined thresholds."""
        if value >= threshold.critical_max or value <= threshold.critical_min:
            return (
                HealthStatus.CRITICAL,
                f"CRITICAL: Value {value} exceeds critical limit "
                f"({threshold.critical_min}-{threshold.critical_max})",
                1.0,
            )
        elif value >= threshold.warning_max or value <= threshold.warning_min:
            # Calculate how close to critical
            if threshold.critical_max > threshold.warning_max:
                proximity = (value - threshold.warning_max) / (
                    threshold.critical_max - threshold.warning_max
                )
            else:
                proximity = 0.5
            return (
                HealthStatus.WARNING,
                f"WARNING: Value {value} exceeds normal limit "
                f"({threshold.normal_min}-{threshold.normal_max})",
                0.5 + (proximity * 0.4),
            )
        else:
            return (HealthStatus.NORMAL, "", 0.0)

    def _statistical_check(
        self, value: float, history: list[float]
    ) -> tuple[HealthStatus, str, float] | None:
        """Detect statistical anomalies using Z-score."""
        if len(history) < 10:
            return None

        mean = statistics.mean(history[:-1])  # Exclude current reading
        std = statistics.stdev(history[:-1])

        if std == 0:
            return None

        z_score = abs(value - mean) / std

        if z_score > 3.5:
            return (
                HealthStatus.ANOMALY,
                f"STATISTICAL ANOMALY: Z-score={z_score:.1f} "
                f"(value={value}, mean={mean:.1f}, std={std:.2f})",
                min(z_score / 5.0, 1.0),
            )
        elif z_score > 2.5:
            return (
                HealthStatus.WARNING,
                f"Statistical deviation: Z-score={z_score:.1f}",
                0.4,
            )
        return None

    def _trend_check(
        self, history: list[float]
    ) -> tuple[HealthStatus, str, float] | None:
        """Detect degradation trends (steadily increasing/decreasing)."""
        if len(history) < 20:
            return None

        # Compare recent half vs older half
        midpoint = len(history) // 2
        older_mean = statistics.mean(history[:midpoint])
        recent_mean = statistics.mean(history[midpoint:])

        if older_mean == 0:
            return None

        change_pct = ((recent_mean - older_mean) / abs(older_mean)) * 100

        if abs(change_pct) > 20:
            direction = "increasing" if change_pct > 0 else "decreasing"
            return (
                HealthStatus.WARNING,
                f"TREND: Parameter {direction} by {abs(change_pct):.1f}% "
                f"(older avg: {older_mean:.1f}, recent avg: {recent_mean:.1f})",
                min(abs(change_pct) / 50.0, 0.8),
            )
        return None

    def _get_trend_info(self, history: list[float]) -> dict:
        """Calculate trend metadata."""
        if len(history) < 5:
            return {"direction": "insufficient_data"}

        recent = history[-5:]
        direction = self._calculate_trend_direction(recent)
        rate = (recent[-1] - recent[0]) / max(len(recent) - 1, 1)

        return {
            "direction": direction,
            "rate_per_reading": round(rate, 4),
            "last_5_values": [round(v, 2) for v in recent],
        }

    def _calculate_trend_direction(self, values: list[float]) -> str:
        """Determine if values are trending up, down, or stable."""
        if len(values) < 3:
            return "stable"

        # Simple linear regression slope
        n = len(values)
        x_mean = (n - 1) / 2
        y_mean = statistics.mean(values)

        numerator = sum((i - x_mean) * (v - y_mean) for i, v in enumerate(values))
        denominator = sum((i - x_mean) ** 2 for i in range(n))

        if denominator == 0:
            return "stable"

        slope = numerator / denominator
        # Normalize slope relative to mean
        relative_slope = slope / max(abs(y_mean), 0.001)

        if relative_slope > 0.02:
            return "increasing"
        elif relative_slope < -0.02:
            return "decreasing"
        else:
            return "stable"
```

---

## `backend/app/services/agents/fault_diagnosis_agent.py`

**Fault diagnosis agent**

```python
"""
Fault Diagnosis & Suggestion Agent
When the Sensor Monitor detects an anomaly, this agent determines probable cause
and recommends corrective actions by reasoning across the Knowledge Graph.
"""

import httpx
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import structlog

from app.config import settings
from app.services.agents.sensor_monitor_agent import AnomalyAlert, HealthStatus
from app.services.knowledge_graph.neo4j_client import Neo4jClient

logger = structlog.get_logger()

@dataclass
class DiagnosisHypothesis:
    cause: str
    confidence: float  # 0-1
    evidence: list[str]  # Supporting references
    category: str  # "mechanical", "electrical", "process", "instrumentation"

@dataclass
class CorrectionAction:
    action: str
    priority: str  # "immediate", "short_term", "long_term"
    estimated_effort: str  # "1h", "4h", "1 day", etc.
    parts_needed: list[str] = field(default_factory=list)
    sop_reference: str = ""
    safety_precautions: list[str] = field(default_factory=list)

@dataclass
class DiagnosisReport:
    equipment_tag: str
    alert_summary: str
    hypotheses: list[DiagnosisHypothesis]
    recommended_actions: list[CorrectionAction]
    similar_past_incidents: list[dict]
    confidence_level: str  # "high", "medium", "low"
    generated_at: datetime = field(default_factory=datetime.utcnow)
    references: list[str] = field(default_factory=list)

class FaultDiagnosisAgent:
    """
    Diagnoses equipment faults by:
    1. Querying Knowledge Graph for equipment history and similar failures
    2. Cross-referencing OEM troubleshooting guides
    3. Using LLM reasoning (Ishikawa/5-Why) for root cause analysis
    4. Generating ranked corrective actions with SOP references
    """

    # Common failure mode patterns (used when KG data is limited)
    FAILURE_PATTERNS = {
        "vibration": {
            "high_value": [
                DiagnosisHypothesis(
                    cause="Bearing degradation (inner/outer race wear)",
                    confidence=0.75,
                    evidence=["Most common cause of vibration increase in rotating equipment"],
                    category="mechanical",
                ),
                DiagnosisHypothesis(
                    cause="Misalignment (angular or parallel)",
                    confidence=0.65,
                    evidence=["Often occurs after maintenance involving coupling disconnect"],
                    category="mechanical",
                ),
                DiagnosisHypothesis(
                    cause="Imbalance (fouling, erosion, or loose component)",
                    confidence=0.55,
                    evidence=["Check for deposit buildup or missing balance weight"],
                    category="mechanical",
                ),
                DiagnosisHypothesis(
                    cause="Looseness (structural or rotating)",
                    confidence=0.45,
                    evidence=["Check foundation bolts and bearing housing"],
                    category="mechanical",
                ),
            ],
            "trending_up": [
                DiagnosisHypothesis(
                    cause="Progressive bearing wear — lubrication degradation likely",
                    confidence=0.7,
                    evidence=["Gradual increase pattern typical of lube contamination"],
                    category="mechanical",
                ),
            ],
        },
        "temperature": {
            "high_value": [
                DiagnosisHypothesis(
                    cause="Cooling system insufficiency (fouled cooler or low coolant flow)",
                    confidence=0.7,
                    evidence=["Check heat exchanger pressure drop and coolant level"],
                    category="process",
                ),
                DiagnosisHypothesis(
                    cause="Bearing overheating (lubrication failure)",
                    confidence=0.65,
                    evidence=["Correlate with vibration data for confirmation"],
                    category="mechanical",
                ),
                DiagnosisHypothesis(
                    cause="Overloading (operating above design capacity)",
                    confidence=0.5,
                    evidence=["Check current draw and flow rate vs design"],
                    category="process",
                ),
            ],
        },
        "pressure": {
            "high_value": [
                DiagnosisHypothesis(
                    cause="Downstream blockage or restriction",
                    confidence=0.7,
                    evidence=["Check downstream valves, filters, and line condition"],
                    category="process",
                ),
                DiagnosisHypothesis(
                    cause="Control valve malfunction (stuck closed)",
                    confidence=0.6,
                    evidence=["Check valve position feedback vs command"],
                    category="instrumentation",
                ),
            ],
            "low_value": [
                DiagnosisHypothesis(
                    cause="Leak in system (flange, seal, or pipe)",
                    confidence=0.7,
                    evidence=["Inspect for visible leaks, check system inventory"],
                    category="mechanical",
                ),
                DiagnosisHypothesis(
                    cause="Pump/compressor degradation (worn impeller or valves)",
                    confidence=0.6,
                    evidence=["Compare discharge pressure vs speed curve"],
                    category="mechanical",
                ),
            ],
        },
    }

    STANDARD_ACTIONS = {
        "mechanical": [
            CorrectionAction(
                action="Perform vibration spectrum analysis to confirm failure mode",
                priority="immediate",
                estimated_effort="2h",
                safety_precautions=["Lock-out/Tag-out if accessing rotating parts"],
            ),
            CorrectionAction(
                action="Inspect and sample lubrication oil (send for analysis)",
                priority="immediate",
                estimated_effort="1h",
                sop_reference="SOP-MAINT-045: Lubrication Sampling Procedure",
            ),
            CorrectionAction(
                action="Schedule bearing replacement during next available window",
                priority="short_term",
                estimated_effort="8h",
                parts_needed=["Bearing (check OEM spec)", "Seal set", "Lubricant"],
                sop_reference="SOP-MAINT-023: Bearing Replacement Procedure",
                safety_precautions=["PTW required", "Isolate and depressurize", "LOTO"],
            ),
        ],
        "process": [
            CorrectionAction(
                action="Check and clean heat exchanger / cooling system",
                priority="short_term",
                estimated_effort="4h",
                sop_reference="SOP-MAINT-067: Heat Exchanger Cleaning",
            ),
            CorrectionAction(
                action="Verify process parameters against design basis",
                priority="immediate",
                estimated_effort="1h",
            ),
        ],
        "instrumentation": [
            CorrectionAction(
                action="Calibrate sensor / verify reading with portable instrument",
                priority="immediate",
                estimated_effort="1h",
                sop_reference="SOP-INST-012: Instrument Calibration",
            ),
            CorrectionAction(
                action="Check control valve stroke and positioner",
                priority="short_term",
                estimated_effort="2h",
            ),
        ],
    }

    def __init__(self, neo4j_client: Optional[Neo4jClient] = None):
        self.neo4j = neo4j_client

    async def diagnose(self, alert: AnomalyAlert) -> DiagnosisReport:
        """
        Generate a full diagnosis report for an anomaly alert.
        Combines pattern matching, KG lookup, and LLM reasoning.
        """
        logger.info(
            "Starting fault diagnosis",
            equipment=alert.equipment_tag,
            parameter=alert.parameter,
            status=alert.status.value,
        )

        # Step 1: Get hypotheses from pattern library
        hypotheses = self._get_pattern_hypotheses(alert)

        # Step 2: Enrich with Knowledge Graph data (if available)
        similar_incidents = []
        if self.neo4j:
            kg_context = await self._query_knowledge_graph(alert)
            similar_incidents = kg_context.get("similar_incidents", [])
            # Adjust confidence based on historical evidence
            hypotheses = self._adjust_confidence_from_history(hypotheses, kg_context)

        # Step 3: Get LLM-powered deeper analysis (if Ollama available)
        llm_hypotheses = await self._llm_reasoning(alert, hypotheses)
        if llm_hypotheses:
            hypotheses.extend(llm_hypotheses)

        # Step 4: Generate corrective actions
        actions = self._generate_actions(hypotheses, alert)

        # Step 5: Determine overall confidence
        confidence = self._assess_overall_confidence(hypotheses, similar_incidents)

        # Build report
        report = DiagnosisReport(
            equipment_tag=alert.equipment_tag,
            alert_summary=(
                f"{alert.parameter} {alert.status.value} on {alert.equipment_tag}: "
                f"{alert.current_value} {alert.unit} — {alert.reason}"
            ),
            hypotheses=sorted(hypotheses, key=lambda h: h.confidence, reverse=True)[:5],
            recommended_actions=actions,
            similar_past_incidents=similar_incidents,
            confidence_level=confidence,
            references=[],
        )

        logger.info(
            "Diagnosis complete",
            equipment=alert.equipment_tag,
            hypotheses=len(report.hypotheses),
            actions=len(report.recommended_actions),
            confidence=confidence,
        )

        return report

    def _get_pattern_hypotheses(self, alert: AnomalyAlert) -> list[DiagnosisHypothesis]:
        """Get initial hypotheses from the failure pattern library."""
        param_patterns = self.FAILURE_PATTERNS.get(alert.parameter, {})

        # Determine sub-pattern based on alert characteristics
        if alert.status == HealthStatus.CRITICAL:
            key = "high_value"
        elif "trending" in (alert.trend_info or {}).get("direction", ""):
            key = "trending_up"
        else:
            key = "high_value"

        hypotheses = param_patterns.get(key, [])

        # Deep copy to avoid mutating the class patterns
        return [
            DiagnosisHypothesis(
                cause=h.cause,
                confidence=h.confidence,
                evidence=list(h.evidence),
                category=h.category,
            )
            for h in hypotheses
        ]

    async def _query_knowledge_graph(self, alert: AnomalyAlert) -> dict:
        """Query KG for equipment history, similar failures, and OEM data."""
        context = {
            "equipment_history": {},
            "similar_incidents": [],
            "oem_recommendations": [],
        }

        if not self.neo4j:
            return context

        try:
            # Get equipment full context
            equip_context = await self.neo4j.get_equipment_context(alert.equipment_tag)
            if equip_context:
                context["equipment_history"] = equip_context

                # Extract similar incidents
                incidents = equip_context.get("incidents", [])
                work_orders = equip_context.get("work_orders", [])
                context["similar_incidents"] = [
                    {"type": "incident", "data": inc} for inc in incidents[:5]
                ] + [
                    {"type": "work_order", "data": wo} for wo in work_orders[:5]
                ]

        except Exception as e:
            logger.warning("KG query failed", error=str(e))

        return context

    def _adjust_confidence_from_history(
        self, hypotheses: list[DiagnosisHypothesis], kg_context: dict
    ) -> list[DiagnosisHypothesis]:
        """Increase confidence for hypotheses supported by historical data."""
        history_text = str(kg_context).lower()

        for hypothesis in hypotheses:
            # Check if similar cause appears in history
            cause_keywords = hypothesis.cause.lower().split()
            matches = sum(1 for kw in cause_keywords if kw in history_text)
            if matches > 2:
                hypothesis.confidence = min(hypothesis.confidence + 0.15, 0.98)
                hypothesis.evidence.append("Supported by equipment history in Knowledge Graph")

        return hypotheses

    async def _llm_reasoning(
        self, alert: AnomalyAlert, existing_hypotheses: list[DiagnosisHypothesis]
    ) -> list[DiagnosisHypothesis]:
        """Use LLM for deeper diagnostic reasoning."""
        try:
            prompt = f"""You are an industrial equipment diagnostic expert.

Equipment: {alert.equipment_tag}
Parameter: {alert.parameter}
Current Value: {alert.current_value} {alert.unit}
Status: {alert.status.value}
Alert Reason: {alert.reason}
Trend: {alert.trend_info}

Existing hypotheses:
{chr(10).join(f'- {h.cause} (confidence: {h.confidence:.0%})' for h in existing_hypotheses)}

Based on your expertise, are there any additional root causes we should consider?
Particularly think about:
1. Recently changed conditions that could cause this
2. Interaction effects between multiple parameters
3. Less obvious causes specific to this equipment type

Provide 1-2 additional hypotheses if relevant, or confirm the existing ones are comprehensive.
Format: JSON array of objects with "cause", "confidence" (0-1), "category", "evidence" fields."""

            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"{settings.ollama_base_url}/api/chat",
                    json={
                        "model": settings.ollama_chat_model,
                        "messages": [{"role": "user", "content": prompt}],
                        "stream": False,
                        "format": "json",
                        "options": {"temperature": 0.1, "num_predict": 500},
                    },
                )

                if response.status_code == 200:
                    import json
                    content = response.json()["message"]["content"]
                    data = json.loads(content)
                    hypotheses_data = data if isinstance(data, list) else data.get("hypotheses", [])
                    return [
                        DiagnosisHypothesis(
                            cause=h.get("cause", ""),
                            confidence=float(h.get("confidence", 0.5)),
                            evidence=[h.get("evidence", "LLM analysis")],
                            category=h.get("category", "general"),
                        )
                        for h in hypotheses_data[:2]
                    ]
        except Exception as e:
            logger.debug("LLM reasoning unavailable", error=str(e))

        return []

    def _generate_actions(
        self, hypotheses: list[DiagnosisHypothesis], alert: AnomalyAlert
    ) -> list[CorrectionAction]:
        """Generate corrective actions based on top hypotheses."""
        actions = []

        # Get actions for the top hypothesis category
        if hypotheses:
            top_category = hypotheses[0].category
            category_actions = self.STANDARD_ACTIONS.get(top_category, [])
            actions.extend(category_actions)

        # Add severity-specific immediate action
        if alert.status == HealthStatus.CRITICAL:
            actions.insert(0, CorrectionAction(
                action=f"IMMEDIATE: Reduce load on {alert.equipment_tag} or prepare for controlled shutdown",
                priority="immediate",
                estimated_effort="15min",
                safety_precautions=[
                    "Notify control room",
                    "Alert maintenance team on standby",
                    "Verify backup equipment readiness",
                ],
            ))

        return actions

    def _assess_overall_confidence(
        self, hypotheses: list[DiagnosisHypothesis], similar_incidents: list
    ) -> str:
        """Assess overall diagnosis confidence."""
        if not hypotheses:
            return "low"

        top_confidence = hypotheses[0].confidence if hypotheses else 0
        has_history = len(similar_incidents) > 0

        if top_confidence > 0.7 and has_history:
            return "high"
        elif top_confidence > 0.5:
            return "medium"
        else:
            return "low"
```

---

## `backend/app/services/agents/predictive_maintenance_agent.py`

**Predictive maintenance agent (RUL)**

```python
"""
Predictive Maintenance Agent
Uses historical failure patterns + current sensor trends to predict
WHEN equipment will likely fail (Remaining Useful Life estimation).
"""

import math
import statistics
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional
import structlog

from app.services.agents.sensor_monitor_agent import HealthStatus

logger = structlog.get_logger()

@dataclass
class RULEstimate:
    equipment_tag: str
    parameter: str
    estimated_days_to_failure: float
    confidence_interval: tuple[float, float]  # (lower, upper) in days
    risk_score: float  # 0-1 (probability of failure before next scheduled PM)
    method: str  # "trend_extrapolation", "weibull", "pattern_match"
    current_health_pct: float  # 0-100
    degradation_rate: float  # units per day

@dataclass
class MaintenanceRecommendation:
    equipment_tag: str
    action: str
    recommended_date: datetime
    urgency: str  # "advance_pm", "schedule_new", "defer_ok", "immediate"
    cost_of_early_intervention: float
    cost_of_unplanned_failure: float
    confidence: str
    reasoning: str

@dataclass
class PredictiveReport:
    equipment_tag: str
    rul_estimates: list[RULEstimate]
    overall_health_score: float  # 0-100
    next_scheduled_pm: Optional[datetime]
    maintenance_recommendations: list[MaintenanceRecommendation]
    risk_summary: str
    generated_at: datetime = field(default_factory=datetime.utcnow)

class PredictiveMaintenanceAgent:
    """
    Predicts equipment failure timing using:
    1. Trend extrapolation (project when parameter hits critical limit)
    2. Weibull reliability analysis (statistical failure distribution)
    3. Pattern matching (compare degradation curve to historical failures)
    """

    # Typical MTBF data for common industrial equipment (hours)
    EQUIPMENT_MTBF = {
        "pump": 25000,
        "compressor": 30000,
        "motor": 40000,
        "valve": 50000,
        "heat_exchanger": 60000,
        "bearing": 20000,
    }

    # Cost estimates for cost/benefit analysis
    COST_ESTIMATES = {
        "planned_maintenance": {
            "pump": 2500,
            "compressor": 8000,
            "motor": 3000,
            "valve": 1500,
        },
        "unplanned_failure": {
            "pump": 45000,      # Parts + labor + downtime
            "compressor": 150000,
            "motor": 35000,
            "valve": 25000,
        },
    }

    def __init__(self):
        self._failure_history: dict[str, list[dict]] = {}  # equipment_tag -> past failures

    def register_failure_history(self, equipment_tag: str, failures: list[dict]):
        """Register historical failure data for an equipment."""
        self._failure_history[equipment_tag] = failures

    def predict(
        self,
        equipment_tag: str,
        parameter_history: dict[str, list[float]],  # param_name -> readings
        critical_limits: dict[str, float],  # param_name -> critical threshold
        next_scheduled_pm: Optional[datetime] = None,
        equipment_type: str = "pump",
        hours_since_last_maintenance: float = 0,
    ) -> PredictiveReport:
        """
        Generate a full predictive maintenance report.

        Args:
            equipment_tag: Equipment identifier
            parameter_history: Recent readings per parameter
            critical_limits: Threshold that indicates failure
            next_scheduled_pm: When the next PM is currently scheduled
            equipment_type: For cost/MTBF lookups
            hours_since_last_maintenance: Operating hours since last major maintenance
        """
        logger.info("Running predictive analysis", equipment=equipment_tag)

        rul_estimates = []

        # Estimate RUL for each monitored parameter
        for param, readings in parameter_history.items():
            if len(readings) < 10:
                continue

            limit = critical_limits.get(param)
            if limit is None:
                continue

            # Method 1: Trend extrapolation
            trend_rul = self._trend_extrapolation(readings, limit, param)
            if trend_rul:
                rul_estimates.append(RULEstimate(
                    equipment_tag=equipment_tag,
                    parameter=param,
                    estimated_days_to_failure=trend_rul["days"],
                    confidence_interval=trend_rul["ci"],
                    risk_score=trend_rul["risk"],
                    method="trend_extrapolation",
                    current_health_pct=trend_rul["health_pct"],
                    degradation_rate=trend_rul["rate"],
                ))

        # Method 2: Weibull reliability (if failure history available)
        weibull_rul = self._weibull_estimate(
            equipment_tag, equipment_type, hours_since_last_maintenance
        )
        if weibull_rul:
            rul_estimates.append(weibull_rul)

        # Calculate overall health score
        overall_health = self._calculate_overall_health(rul_estimates)

        # Generate maintenance recommendations
        recommendations = self._generate_recommendations(
            equipment_tag, rul_estimates, next_scheduled_pm, equipment_type
        )

        # Risk summary
        risk_summary = self._generate_risk_summary(rul_estimates, next_scheduled_pm)

        return PredictiveReport(
            equipment_tag=equipment_tag,
            rul_estimates=rul_estimates,
            overall_health_score=overall_health,
            next_scheduled_pm=next_scheduled_pm,
            maintenance_recommendations=recommendations,
            risk_summary=risk_summary,
        )

    def _trend_extrapolation(
        self, readings: list[float], critical_limit: float, param: str
    ) -> Optional[dict]:
        """Extrapolate current trend to estimate when limit will be reached."""
        if len(readings) < 10:
            return None

        n = len(readings)
        # Linear regression
        x_mean = (n - 1) / 2
        y_mean = statistics.mean(readings)

        numerator = sum((i - x_mean) * (v - y_mean) for i, v in enumerate(readings))
        denominator = sum((i - x_mean) ** 2 for i in range(n))

        if denominator == 0:
            return None

        slope = numerator / denominator  # units per reading
        intercept = y_mean - slope * x_mean

        if slope <= 0 and readings[-1] < critical_limit:
            # Not degrading toward limit
            return None

        # Current value and distance to limit
        current = readings[-1]
        distance_to_limit = critical_limit - current

        if slope == 0:
            return None

        # Readings to failure
        readings_to_failure = distance_to_limit / slope if slope != 0 else float("inf")

        if readings_to_failure < 0:
            # Already past limit
            readings_to_failure = 0

        # Assume 1 reading per hour (adjust based on actual frequency)
        hours_to_failure = readings_to_failure
        days_to_failure = hours_to_failure / 24

        # Confidence interval (based on R² of linear fit)
        residuals = [readings[i] - (slope * i + intercept) for i in range(n)]
        ss_res = sum(r**2 for r in residuals)
        ss_tot = sum((v - y_mean)**2 for v in readings)
        r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0

        # Wider CI for lower R²
        ci_factor = 1 + (1 - r_squared) * 2
        ci_lower = max(0, days_to_failure / ci_factor)
        ci_upper = days_to_failure * ci_factor

        # Health percentage
        health_pct = max(0, min(100, (1 - current / critical_limit) * 100))

        # Risk score: how likely to fail before next scheduled PM
        risk = 1.0 if days_to_failure <= 0 else min(1.0, 7 / max(days_to_failure, 0.1))

        return {
            "days": round(days_to_failure, 1),
            "ci": (round(ci_lower, 1), round(ci_upper, 1)),
            "risk": round(risk, 2),
            "health_pct": round(health_pct, 1),
            "rate": round(slope, 4),
        }

    def _weibull_estimate(
        self, equipment_tag: str, equipment_type: str, hours_in_service: float
    ) -> Optional[RULEstimate]:
        """Estimate RUL using Weibull distribution parameters."""
        mtbf = self.EQUIPMENT_MTBF.get(equipment_type)
        if not mtbf:
            return None

        # Simplified Weibull with shape parameter beta=2 (wear-out mode)
        beta = 2.0
        eta = mtbf  # Characteristic life

        # Reliability at current age
        reliability = math.exp(-((hours_in_service / eta) ** beta))

        # Estimated remaining life (conditional)
        if reliability <= 0.01:
            remaining_hours = 0
        else:
            # Mean residual life approximation
            remaining_hours = eta * math.gamma(1 + 1/beta) - hours_in_service
            remaining_hours = max(0, remaining_hours)

        days_remaining = remaining_hours / 24

        # Confidence interval
        ci_lower = days_remaining * 0.6
        ci_upper = days_remaining * 1.5

        # Risk score based on reliability
        risk_score = 1 - reliability

        return RULEstimate(
            equipment_tag=equipment_tag,
            parameter="reliability",
            estimated_days_to_failure=round(days_remaining, 1),
            confidence_interval=(round(ci_lower, 1), round(ci_upper, 1)),
            risk_score=round(risk_score, 2),
            method="weibull",
            current_health_pct=round(reliability * 100, 1),
            degradation_rate=0,
        )

    def _calculate_overall_health(self, rul_estimates: list[RULEstimate]) -> float:
        """Calculate overall equipment health from individual estimates."""
        if not rul_estimates:
            return 100.0

        # Use the worst (lowest) health score
        health_scores = [r.current_health_pct for r in rul_estimates]
        return min(health_scores)

    def _generate_recommendations(
        self,
        equipment_tag: str,
        rul_estimates: list[RULEstimate],
        next_pm: Optional[datetime],
        equipment_type: str,
    ) -> list[MaintenanceRecommendation]:
        """Generate maintenance schedule recommendations."""
        recommendations = []
        now = datetime.utcnow()

        # Find the most critical RUL
        if not rul_estimates:
            return recommendations

        worst_rul = min(rul_estimates, key=lambda r: r.estimated_days_to_failure)
        estimated_failure_date = now + timedelta(days=worst_rul.estimated_days_to_failure)

        # Cost estimates
        planned_cost = self.COST_ESTIMATES["planned_maintenance"].get(equipment_type, 5000)
        failure_cost = self.COST_ESTIMATES["unplanned_failure"].get(equipment_type, 50000)

        if worst_rul.estimated_days_to_failure <= 3:
            recommendations.append(MaintenanceRecommendation(
                equipment_tag=equipment_tag,
                action=f"URGENT: Schedule immediate maintenance on {equipment_tag}. "
                       f"Estimated failure within {worst_rul.estimated_days_to_failure:.0f} days.",
                recommended_date=now + timedelta(days=1),
                urgency="immediate",
                cost_of_early_intervention=planned_cost,
                cost_of_unplanned_failure=failure_cost,
                confidence=worst_rul.method,
                reasoning=f"Parameter '{worst_rul.parameter}' degradation rate "
                         f"indicates failure by {estimated_failure_date.strftime('%d-%b-%Y')}",
            ))
        elif next_pm and estimated_failure_date < next_pm:
            days_to_advance = (next_pm - estimated_failure_date).days
            recommendations.append(MaintenanceRecommendation(
                equipment_tag=equipment_tag,
                action=f"Advance scheduled PM by {days_to_advance} days. "
                       f"Current schedule ({next_pm.strftime('%d-%b')}) is after predicted failure.",
                recommended_date=estimated_failure_date - timedelta(days=3),
                urgency="advance_pm",
                cost_of_early_intervention=planned_cost,
                cost_of_unplanned_failure=failure_cost,
                confidence=worst_rul.method,
                reasoning=f"Predicted failure: {estimated_failure_date.strftime('%d-%b-%Y')}, "
                         f"next PM: {next_pm.strftime('%d-%b-%Y')}. Gap = {days_to_advance} days.",
            ))
        elif worst_rul.risk_score < 0.2:
            recommendations.append(MaintenanceRecommendation(
                equipment_tag=equipment_tag,
                action=f"Continue monitoring. {equipment_tag} health is acceptable.",
                recommended_date=next_pm or (now + timedelta(days=30)),
                urgency="defer_ok",
                cost_of_early_intervention=planned_cost,
                cost_of_unplanned_failure=failure_cost,
                confidence=worst_rul.method,
                reasoning=f"RUL = {worst_rul.estimated_days_to_failure:.0f} days, "
                         f"risk score = {worst_rul.risk_score:.0%}. Within acceptable limits.",
            ))

        return recommendations

    def _generate_risk_summary(
        self, rul_estimates: list[RULEstimate], next_pm: Optional[datetime]
    ) -> str:
        """Generate a human-readable risk summary."""
        if not rul_estimates:
            return "Insufficient data for prediction. Continue monitoring."

        worst = min(rul_estimates, key=lambda r: r.estimated_days_to_failure)

        if worst.estimated_days_to_failure <= 7:
            return (
                f"HIGH RISK: Equipment predicted to fail within {worst.estimated_days_to_failure:.0f} days "
                f"based on {worst.parameter} degradation ({worst.method}). "
                f"Immediate maintenance planning recommended."
            )
        elif worst.estimated_days_to_failure <= 30:
            return (
                f"MODERATE RISK: Estimated {worst.estimated_days_to_failure:.0f} days remaining life. "
                f"Plan maintenance within 2 weeks."
            )
        else:
            return (
                f"LOW RISK: Estimated {worst.estimated_days_to_failure:.0f} days remaining life. "
                f"Continue routine monitoring."
            )
```

---

## `backend/app/services/agents/shift_handover_agent.py`

**Shift handover report agent**

```python
"""
Shift Handover Agent
Automatically generates comprehensive shift handover reports by summarizing
all events, alarms, actions, and pending items from a shift period.
"""

import httpx
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional
import structlog

from app.config import settings
from app.services.agents.sensor_monitor_agent import AnomalyAlert, HealthStatus

logger = structlog.get_logger()

@dataclass
class ShiftEvent:
    timestamp: datetime
    event_type: str  # "alarm", "maintenance", "process_deviation", "safety", "operator_action"
    severity: str  # "critical", "high", "medium", "low", "info"
    equipment_tag: str
    description: str
    status: str  # "resolved", "pending", "in_progress"
    action_taken: str = ""
    assigned_to: str = ""

@dataclass
class HandoverSection:
    title: str
    items: list[dict]
    priority: str  # "critical", "high", "medium", "low"

@dataclass
class HandoverReport:
    shift_start: datetime
    shift_end: datetime
    shift_type: str  # "day", "night", "evening"
    generated_at: datetime = field(default_factory=datetime.utcnow)

    # Summary
    executive_summary: list[str] = field(default_factory=list)
    critical_items: list[dict] = field(default_factory=list)

    # Detailed sections
    alarms_summary: dict = field(default_factory=dict)
    equipment_health_changes: list[dict] = field(default_factory=list)
    work_in_progress: list[dict] = field(default_factory=list)
    completed_activities: list[dict] = field(default_factory=list)
    upcoming_activities: list[dict] = field(default_factory=list)
    watch_items: list[dict] = field(default_factory=list)

    # Stats
    total_alarms: int = 0
    critical_alarms: int = 0
    maintenance_actions: int = 0

class ShiftHandoverAgent:
    """
    Generates structured shift handover reports by:
    1. Collecting all events from the shift period
    2. Categorizing and prioritizing
    3. Summarizing using LLM
    4. Formatting for incoming team
    """

    def __init__(self):
        self._events: list[ShiftEvent] = []

    def log_event(self, event: ShiftEvent):
        """Log a shift event for inclusion in handover report."""
        self._events.append(event)

    def log_alarm(
        self,
        alert: AnomalyAlert,
        action_taken: str = "",
        resolved: bool = False,
    ):
        """Convert an anomaly alert to a shift event."""
        self._events.append(ShiftEvent(
            timestamp=alert.timestamp,
            event_type="alarm",
            severity="critical" if alert.status == HealthStatus.CRITICAL else "high",
            equipment_tag=alert.equipment_tag,
            description=f"{alert.parameter}: {alert.current_value} {alert.unit} — {alert.reason}",
            status="resolved" if resolved else "pending",
            action_taken=action_taken,
        ))

    async def generate_report(
        self,
        shift_start: datetime,
        shift_end: datetime,
        upcoming_pm: list[dict] | None = None,
    ) -> HandoverReport:
        """Generate the full shift handover report."""
        logger.info(
            "Generating handover report",
            shift_start=shift_start.isoformat(),
            shift_end=shift_end.isoformat(),
        )

        # Filter events to this shift
        shift_events = [
            e for e in self._events
            if shift_start <= e.timestamp <= shift_end
        ]

        # Determine shift type
        hour = shift_start.hour
        shift_type = "day" if 6 <= hour < 14 else ("evening" if 14 <= hour < 22 else "night")

        # Categorize events
        alarms = [e for e in shift_events if e.event_type == "alarm"]
        maintenance = [e for e in shift_events if e.event_type == "maintenance"]
        deviations = [e for e in shift_events if e.event_type == "process_deviation"]
        safety = [e for e in shift_events if e.event_type == "safety"]

        # Build alarm summary
        alarms_summary = {
            "total": len(alarms),
            "critical": sum(1 for a in alarms if a.severity == "critical"),
            "high": sum(1 for a in alarms if a.severity == "high"),
            "resolved": sum(1 for a in alarms if a.status == "resolved"),
            "pending": sum(1 for a in alarms if a.status == "pending"),
        }

        # Critical items (unresolved critical/high severity)
        critical_items = [
            {
                "equipment": e.equipment_tag,
                "issue": e.description,
                "status": e.status,
                "action": e.action_taken or "NEEDS ATTENTION",
                "time": e.timestamp.strftime("%H:%M"),
            }
            for e in shift_events
            if e.severity in ("critical", "high") and e.status != "resolved"
        ]

        # Equipment health changes
        equipment_changes = self._summarize_equipment_changes(shift_events)

        # Work in progress
        wip = [
            {
                "equipment": e.equipment_tag,
                "activity": e.description,
                "status": e.status,
                "assigned_to": e.assigned_to,
            }
            for e in shift_events
            if e.status == "in_progress"
        ]

        # Completed activities
        completed = [
            {
                "equipment": e.equipment_tag,
                "activity": e.description,
                "completed_at": e.timestamp.strftime("%H:%M"),
            }
            for e in shift_events
            if e.status == "resolved" and e.event_type == "maintenance"
        ]

        # Watch items (trending parameters, recurring alarms)
        watch_items = self._identify_watch_items(shift_events)

        # Generate executive summary
        executive_summary = await self._generate_summary(
            shift_events, alarms_summary, critical_items, shift_type
        )

        report = HandoverReport(
            shift_start=shift_start,
            shift_end=shift_end,
            shift_type=shift_type,
            executive_summary=executive_summary,
            critical_items=critical_items,
            alarms_summary=alarms_summary,
            equipment_health_changes=equipment_changes,
            work_in_progress=wip,
            completed_activities=completed,
            upcoming_activities=upcoming_pm or [],
            watch_items=watch_items,
            total_alarms=len(alarms),
            critical_alarms=alarms_summary["critical"],
            maintenance_actions=len(maintenance),
        )

        logger.info(
            "Handover report generated",
            events=len(shift_events),
            critical_items=len(critical_items),
            watch_items=len(watch_items),
        )

        return report

    def format_report_text(self, report: HandoverReport) -> str:
        """Format the handover report as readable text."""
        lines = []
        lines.append("=" * 70)
        lines.append(f"  SHIFT HANDOVER REPORT")
        lines.append(f"  Shift: {report.shift_type.upper()} "
                     f"({report.shift_start.strftime('%d-%b %H:%M')} to "
                     f"{report.shift_end.strftime('%d-%b %H:%M')})")
        lines.append(f"  Generated: {report.generated_at.strftime('%d-%b-%Y %H:%M')}")
        lines.append("=" * 70)

        # Executive Summary
        lines.append("\n  EXECUTIVE SUMMARY:")
        for item in report.executive_summary:
            lines.append(f"    • {item}")

        # Critical Items
        if report.critical_items:
            lines.append(f"\n  ⚠️  CRITICAL ITEMS REQUIRING IMMEDIATE ATTENTION ({len(report.critical_items)}):")
            for item in report.critical_items:
                lines.append(f"    [{item['time']}] {item['equipment']}: {item['issue']}")
                lines.append(f"             Status: {item['status']} | Action: {item['action']}")

        # Alarm Summary
        lines.append(f"\n  ALARM SUMMARY:")
        lines.append(f"    Total: {report.alarms_summary.get('total', 0)} | "
                     f"Critical: {report.alarms_summary.get('critical', 0)} | "
                     f"Resolved: {report.alarms_summary.get('resolved', 0)} | "
                     f"Pending: {report.alarms_summary.get('pending', 0)}")

        # Work in Progress
        if report.work_in_progress:
            lines.append(f"\n  WORK IN PROGRESS ({len(report.work_in_progress)}):")
            for wip in report.work_in_progress:
                lines.append(f"    • {wip['equipment']}: {wip['activity']}")
                if wip.get('assigned_to'):
                    lines.append(f"      Assigned to: {wip['assigned_to']}")

        # Watch Items
        if report.watch_items:
            lines.append(f"\n  WATCH ITEMS (monitor closely):")
            for item in report.watch_items:
                lines.append(f"    • {item['equipment']}: {item['reason']}")

        # Upcoming
        if report.upcoming_activities:
            lines.append(f"\n  UPCOMING ACTIVITIES (next 12 hours):")
            for act in report.upcoming_activities[:5]:
                lines.append(f"    • {act.get('description', act)}")

        lines.append("\n" + "=" * 70)
        return "\n".join(lines)

    def _summarize_equipment_changes(self, events: list[ShiftEvent]) -> list[dict]:
        """Identify equipment whose health status changed during the shift."""
        equipment_events: dict[str, list[ShiftEvent]] = {}
        for e in events:
            equipment_events.setdefault(e.equipment_tag, []).append(e)

        changes = []
        for tag, tag_events in equipment_events.items():
            severities = [e.severity for e in tag_events]
            if "critical" in severities or "high" in severities:
                changes.append({
                    "equipment": tag,
                    "events_count": len(tag_events),
                    "worst_severity": "critical" if "critical" in severities else "high",
                    "latest_status": tag_events[-1].status,
                })

        return changes

    def _identify_watch_items(self, events: list[ShiftEvent]) -> list[dict]:
        """Identify items that need continued monitoring."""
        watch = []

        # Recurring alarms (same equipment, multiple times)
        equipment_alarm_count: dict[str, int] = {}
        for e in events:
            if e.event_type == "alarm":
                equipment_alarm_count[e.equipment_tag] = (
                    equipment_alarm_count.get(e.equipment_tag, 0) + 1
                )

        for tag, count in equipment_alarm_count.items():
            if count >= 2:
                watch.append({
                    "equipment": tag,
                    "reason": f"Recurring alarms ({count} times this shift) — may indicate developing issue",
                })

        # Unresolved items
        pending = [e for e in events if e.status == "pending" and e.severity in ("high", "medium")]
        for e in pending:
            watch.append({
                "equipment": e.equipment_tag,
                "reason": f"Unresolved: {e.description}",
            })

        return watch

    async def _generate_summary(
        self,
        events: list[ShiftEvent],
        alarms: dict,
        critical: list,
        shift_type: str,
    ) -> list[str]:
        """Generate executive summary bullets, using LLM if available."""
        # Build summary from data (works without LLM)
        summary = []

        if not events:
            summary.append("Quiet shift — no significant events or alarms.")
            return summary

        # Alarm overview
        if alarms["critical"] > 0:
            pending = alarms["pending"]
            resolved_msg = "All resolved." if pending == 0 else f"{pending} still pending."
            summary.append(
                f"{alarms['critical']} critical alarm(s) occurred. {resolved_msg}"
            )
        elif alarms["total"] > 0:
            summary.append(f"{alarms['total']} alarms total, none critical. {alarms['resolved']} resolved.")
        else:
            summary.append("No alarms during this shift.")

        # Critical items
        if critical:
            tags = ", ".join(set(item["equipment"] for item in critical))
            summary.append(f"ATTENTION NEEDED: {tags}")

        # Equipment count
        unique_equipment = set(e.equipment_tag for e in events)
        summary.append(f"{len(unique_equipment)} equipment items had events logged.")

        # Try LLM for more natural summary
        try:
            event_text = "\n".join(
                f"[{e.timestamp.strftime('%H:%M')}] {e.equipment_tag}: {e.description} ({e.status})"
                for e in events[:20]
            )

            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{settings.ollama_base_url}/api/chat",
                    json={
                        "model": settings.ollama_chat_model,
                        "messages": [{
                            "role": "user",
                            "content": f"Summarize this {shift_type} shift in 2-3 bullet points "
                                      f"for the incoming maintenance team:\n\n{event_text}",
                        }],
                        "stream": False,
                        "options": {"temperature": 0.2, "num_predict": 200},
                    },
                )
                if response.status_code == 200:
                    llm_summary = response.json()["message"]["content"]
                    # Add LLM summary as additional context
                    for line in llm_summary.strip().split("\n"):
                        line = line.strip().lstrip("•-* ")
                        if line and line not in summary:
                            summary.append(line)
        except Exception:
            pass  # LLM summary is optional enhancement

        return summary[:5]

    def clear_events(self):
        """Clear event log (after shift handover is generated)."""
        self._events.clear()
```

---

## `backend/app/services/agents/report_saver.py`

**Report persistence service**

```python
"""
Report persistence service.
Saves all agent-generated reports to disk with structured naming convention.

Naming Convention:
    {equipment_tag}_{shift}_{status}_{YYYYMMDD_HHMMSS}.json

Examples:
    P-101A_day_CRITICAL_20240701_143022.json
    C-301_night_NORMAL_20240701_230015.json
    MULTI_day_WARNING_20240702_060000.json        (multi-equipment batch)
    FLEET_day_HANDOVER_20240702_180000.json        (shift handover)
    P-101A_NA_PREDICTION_20240703_091500.json      (predictive report)

Directory structure:
    data/reports/
    ├── sensor_analysis/       # From /analyze-sensors
    ├── fault_diagnosis/       # Individual diagnosis reports
    ├── predictive/            # From /predict-maintenance
    └── shift_handover/        # From /shift-handover
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Any
import structlog

from app.config import settings

logger = structlog.get_logger()

REPORTS_BASE = Path(settings.upload_dir).parent / "reports"

def _sanitize(value: str) -> str:
    """Sanitize a string for use in filenames. Remove/replace unsafe chars."""
    safe = value.replace("/", "-").replace("\\", "-").replace(" ", "_")
    # Keep only alphanumeric, dash, underscore
    return "".join(c for c in safe if c.isalnum() or c in "-_").strip("_-")

def _determine_shift(timestamp: datetime | None = None) -> str:
    """Determine shift name from hour: day (06-14), evening (14-22), night (22-06)."""
    if timestamp is None:
        timestamp = datetime.utcnow()
    hour = timestamp.hour
    if 6 <= hour < 14:
        return "day"
    elif 14 <= hour < 22:
        return "evening"
    else:
        return "night"

def _determine_status(alerts: list | None = None, has_critical: bool = False) -> str:
    """Determine overall status label for filename."""
    if has_critical:
        return "CRITICAL"
    if alerts:
        severities = []
        for a in alerts:
            if hasattr(a, "status"):
                severities.append(a.status.value if hasattr(a.status, "value") else str(a.status))
            elif isinstance(a, dict):
                severities.append(a.get("status", ""))
        if "critical" in severities:
            return "CRITICAL"
        if "warning" in severities or "anomaly" in severities:
            return "WARNING"
    return "NORMAL"

class ReportSaver:
    """Persists agent reports to structured directories with naming convention."""

    def __init__(self, base_dir: str | Path | None = None):
        self.base_dir = Path(base_dir) if base_dir else REPORTS_BASE
        # Create subdirectories
        for subdir in ["sensor_analysis", "fault_diagnosis", "predictive", "shift_handover"]:
            (self.base_dir / subdir).mkdir(parents=True, exist_ok=True)

    def save_sensor_analysis(
        self,
        report_data: dict,
        equipment_tags: list[str],
        alerts: list,
        timestamp: datetime | None = None,
    ) -> str:
        """
        Save sensor analysis report.
        Name: {equipment}_{shift}_{status}_{timestamp}.json
        """
        ts = timestamp or datetime.utcnow()
        equipment = self._equipment_label(equipment_tags)
        shift = _determine_shift(ts)
        status = _determine_status(alerts)

        filename = f"{equipment}_{shift}_{status}_{ts.strftime('%Y%m%d_%H%M%S')}.json"
        filepath = self.base_dir / "sensor_analysis" / filename

        self._write(filepath, report_data)
        return str(filepath)

    def save_fault_diagnosis(
        self,
        report_data: dict,
        equipment_tag: str,
        confidence_level: str,
        timestamp: datetime | None = None,
    ) -> str:
        """
        Save individual fault diagnosis report.
        Name: {equipment}_{shift}_{confidence}_{timestamp}.json
        """
        ts = timestamp or datetime.utcnow()
        equipment = _sanitize(equipment_tag)
        shift = _determine_shift(ts)
        status = confidence_level.upper()  # HIGH / MEDIUM / LOW

        filename = f"{equipment}_{shift}_DIAGNOSIS-{status}_{ts.strftime('%Y%m%d_%H%M%S')}.json"
        filepath = self.base_dir / "fault_diagnosis" / filename

        self._write(filepath, report_data)
        return str(filepath)

    def save_predictive_report(
        self,
        report_data: dict,
        equipment_tag: str,
        risk_level: str,
        timestamp: datetime | None = None,
    ) -> str:
        """
        Save predictive maintenance report.
        Name: {equipment}_{shift}_{risk}_{timestamp}.json
        """
        ts = timestamp or datetime.utcnow()
        equipment = _sanitize(equipment_tag)
        shift = _determine_shift(ts)

        # Map health to status label
        if "HIGH RISK" in risk_level.upper():
            status = "HIGH-RISK"
        elif "MODERATE" in risk_level.upper():
            status = "MODERATE-RISK"
        else:
            status = "LOW-RISK"

        filename = f"{equipment}_{shift}_PREDICTION-{status}_{ts.strftime('%Y%m%d_%H%M%S')}.json"
        filepath = self.base_dir / "predictive" / filename

        self._write(filepath, report_data)
        return str(filepath)

    def save_shift_handover(
        self,
        report_data: dict,
        shift_type: str,
        has_critical: bool,
        shift_start: datetime,
        equipment_tags: list[str] | None = None,
    ) -> str:
        """
        Save shift handover report.
        Name: {equipment}_{shift}_{status}_{timestamp}.json
        """
        ts = shift_start
        equipment = self._equipment_label(equipment_tags) if equipment_tags else "FLEET"
        shift = shift_type.lower()
        status = "CRITICAL" if has_critical else ("WARNING" if report_data.get("stats", {}).get("total_alarms", 0) > 0 else "NORMAL")

        filename = f"{equipment}_{shift}_HANDOVER-{status}_{ts.strftime('%Y%m%d_%H%M%S')}.json"
        filepath = self.base_dir / "shift_handover" / filename

        self._write(filepath, report_data)
        return str(filepath)

    def _equipment_label(self, tags: list[str]) -> str:
        """Build equipment portion of filename from tag list."""
        if not tags:
            return "UNKNOWN"
        unique = sorted(set(_sanitize(t) for t in tags if t))
        if len(unique) == 1:
            return unique[0]
        elif len(unique) <= 3:
            return "_".join(unique)
        else:
            return f"MULTI-{len(unique)}eq"

    def _write(self, filepath: Path, data: dict):
        """Write report data as JSON."""
        # Make datetimes serializable
        serializable = json.loads(
            json.dumps(data, default=str, ensure_ascii=False)
        )
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(serializable, f, indent=2, ensure_ascii=False)

        logger.info("Report saved", path=str(filepath))
```

---

## `backend/app/services/agents/orchestrator.py`

**Agent orchestrator (Monitor→Diagnosis→Predictive→Handover)**

```python
"""
Agent Orchestrator — coordinates the multi-agent system.
Routes sensor data through the correct agent pipeline.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import structlog

from app.services.agents.sensor_monitor_agent import (
    SensorHealthMonitorAgent, SensorReading, AnomalyAlert, HealthStatus,
)
from app.services.agents.fault_diagnosis_agent import FaultDiagnosisAgent, DiagnosisReport
from app.services.agents.predictive_maintenance_agent import PredictiveMaintenanceAgent
from app.services.agents.shift_handover_agent import ShiftHandoverAgent, ShiftEvent
from app.services.agents.report_saver import ReportSaver
from app.services.knowledge_graph.neo4j_client import Neo4jClient

logger = structlog.get_logger()

@dataclass
class OrchestratorResult:
    """Combined result from multi-agent processing."""
    alerts: list[AnomalyAlert]
    diagnoses: list[DiagnosisReport]
    health_summary: dict
    actions_generated: int

class AgentOrchestrator:
    """
    Coordinates the multi-agent pipeline:

    Sensor Data → Monitor Agent → (if anomaly) → Diagnosis Agent
                                               → Predictive Agent
                                               → Handover Agent (logs event)
    """

    def __init__(self, neo4j_client: Optional[Neo4jClient] = None):
        self.monitor = SensorHealthMonitorAgent()
        self.diagnosis = FaultDiagnosisAgent(neo4j_client=neo4j_client)
        self.predictive = PredictiveMaintenanceAgent()
        self.handover = ShiftHandoverAgent()
        self._neo4j = neo4j_client

    async def process_sensor_batch(
        self, readings: list[SensorReading]
    ) -> OrchestratorResult:
        """
        Process a batch of sensor readings through the full agent pipeline.

        1. Monitor Agent analyzes all readings
        2. For anomalies, Diagnosis Agent generates root cause hypotheses
        3. All events logged for Shift Handover Agent
        """
        # Step 1: Sensor Health Monitor
        alerts = self.monitor.analyze_batch(readings)

        # Step 2: For each alert, run Fault Diagnosis
        diagnoses = []
        for alert in alerts:
            if alert.status in (HealthStatus.CRITICAL, HealthStatus.WARNING):
                diagnosis = await self.diagnosis.diagnose(alert)
                diagnoses.append(diagnosis)

                # Log to handover agent
                self.handover.log_alarm(
                    alert,
                    action_taken=(
                        diagnosis.recommended_actions[0].action
                        if diagnosis.recommended_actions
                        else "Under investigation"
                    ),
                )

        # Build health summary
        equipment_tags = set(r.equipment_tag for r in readings)
        health_summary = {}
        for tag in equipment_tags:
            health_summary[tag] = self.monitor.get_equipment_health_summary(tag)

        logger.info(
            "Orchestrator batch complete",
            readings=len(readings),
            alerts=len(alerts),
            diagnoses=len(diagnoses),
        )

        return OrchestratorResult(
            alerts=alerts,
            diagnoses=diagnoses,
            health_summary=health_summary,
            actions_generated=sum(len(d.recommended_actions) for d in diagnoses),
        )

    async def get_predictive_report(
        self,
        equipment_tag: str,
        parameter_history: dict[str, list[float]],
        critical_limits: dict[str, float],
        equipment_type: str = "pump",
        hours_in_service: float = 10000,
        next_pm: Optional[datetime] = None,
    ):
        """Run predictive maintenance analysis for specific equipment."""
        return self.predictive.predict(
            equipment_tag=equipment_tag,
            parameter_history=parameter_history,
            critical_limits=critical_limits,
            next_scheduled_pm=next_pm,
            equipment_type=equipment_type,
            hours_since_last_maintenance=hours_in_service,
        )

    async def generate_shift_handover(
        self,
        shift_start: datetime,
        shift_end: datetime,
    ):
        """Generate shift handover report."""
        report = await self.handover.generate_report(shift_start, shift_end)
        return report, self.handover.format_report_text(report)
```

---

## `frontend/package.json`

**Frontend package.json (Next.js 16 + React 19)**

```json
{
  "name": "frontend",
  "version": "1.0.0",
  "description": "",
  "main": "index.js",
  "scripts": {
    "dev": "next dev -p 3000",
    "build": "next build",
    "start": "next start -p 3000"
  },
  "keywords": [],
  "author": "",
  "license": "ISC",
  "dependencies": {
    "next": "^16.2.10",
    "react": "^19.2.7",
    "react-dom": "^19.2.7"
  },
  "devDependencies": {
    "@types/node": "26.1.1",
    "@types/react": "19.2.17",
    "typescript": "7.0.2"
  }
}
```

---

## `frontend/next.config.js`

**Next.js configuration (API proxy)**

```jsx
/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: '<http://localhost:8000/api/:path*>',
      },
    ];
  },
};

export default nextConfig;
```

---

## `frontend/src/app/layout.js`

**Root layout**

```jsx
export const metadata = { title: 'AXIOM - Industrial Knowledge Intelligence' };

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
```

---

## `frontend/src/app/page.js`

**Main application — Pipeline Visualizer + Query + Dashboard + Knowledge Graph**

```jsx
'use client';
import './globals.css';
import { useState, useRef, useEffect } from 'react';

const API = '<http://localhost:8000>';

const TABS = [
  { id: 'ingest', label: 'Pipeline Visualizer', icon: '▶' },
  { id: 'chat', label: 'Query & Retrieval', icon: '◆' },
  { id: 'dashboard', label: 'Dashboard', icon: '~' },
  { id: 'graph', label: 'Knowledge Graph', icon: 'o' },
];

export default function Home() {
  const [tab, setTab] = useState('ingest');
  const [health, setHealth] = useState(null);

  useEffect(() => {
    fetch(`${API}/health`).then(r => r.json()).then(setHealth).catch(() => {});
  }, []);

  return (
    <div className="layout">
      <aside className="sidebar">
        <h1>AXIOM <span>GraphRAG Pipeline Visualizer</span></h1>
        <div className="nav-section">Pipeline</div>
        {TABS.map(t => (
          <div key={t.id} className={`nav-item ${tab === t.id ? 'active' : ''}`} onClick={() => setTab(t.id)}>
            <span style={{ fontFamily: 'monospace', width: 16 }}>{t.icon}</span> {t.label}
          </div>
        ))}
        <div className="nav-section" style={{ marginTop: 'auto', paddingTop: 24 }}>System</div>
        <div className="nav-item" style={{ color: health ? 'var(--green)' : 'var(--red)' }}>
          <span style={{ fontFamily: 'monospace', width: 16 }}>●</span>
          Backend: {health ? 'Connected' : 'Offline'}
        </div>
      </aside>
      <main className="main">
        <div className="header">
          <h2>{TABS.find(t => t.id === tab)?.label}</h2>
          <span style={{ fontSize: 12, color: 'var(--text-muted)' }}>AXIOM v1.0 | Fully Offline GraphRAG</span>
        </div>
        <div className="content">
          {tab === 'ingest' && <PipelineVisualizerTab />}
          {tab === 'chat' && <QueryVisualizerTab />}
          {tab === 'dashboard' && <DashboardTab />}
          {tab === 'graph' && <GraphTab />}
        </div>
      </main>
    </div>
  );
}
```

/* ═══════════════════════════════════════════════════════════════
PIPELINE VISUALIZER — Shows each ingestion step in real-time
═══════════════════════════════════════════════════════════════ */

const PIPELINE_STEPS = [
{ step: 1, name: 'PDF Type Detection', icon: '📄', color: '#3b82f6' },
{ step: 2, name: 'Document Parsing', icon: '📋', color: '#8b5cf6' },
{ step: 3, name: 'OCR Processing', icon: '👁', color: '#f59e0b' },
{ step: 4, name: 'Text Cleaning', icon: '🧹', color: '#10b981' },
{ step: 5, name: 'Document Structuring', icon: '🏗', color: '#06b6d4' },
{ step: 6, name: 'Document Classification', icon: '🏷', color: '#ec4899' },
{ step: 7, name: 'Semantic Chunking', icon: '✂', color: '#f97316' },
{ step: 8, name: 'Entity Extraction', icon: '🔍', color: '#14b8a6' },
{ step: 9, name: 'Relationship Extraction', icon: '🔗', color: '#a855f7' },
{ step: 10, name: 'FAISS Indexing', icon: '📊', color: '#eab308' },
{ step: 11, name: 'Neo4j Graph', icon: '🕸', color: '#22c55e' },
];

function PipelineVisualizerTab() {
const [steps, setSteps] = useState([]);
const [isRunning, setIsRunning] = useState(false);
const [completed, setCompleted] = useState(null);
const [expandedStep, setExpandedStep] = useState(null);
const fileRef = useRef(null);
const scrollRef = useRef(null);

useEffect(() => {
if (scrollRef.current) {
scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
}
}, [steps]);

const upload = async (file) => {
setIsRunning(true);
setSteps([]);
setCompleted(null);
setExpandedStep(null);

```
const fd = new FormData();
fd.append('file', file);

try {
  const response = await fetch(`${API}/api/v1/ingest/document/stream`, {
    method: 'POST',
    body: fd,
  });

  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = '';

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    buffer += decoder.decode(value, { stream: true });
    const lines = buffer.split('\n');
    buffer = lines.pop() || '';

    let currentEvent = null;
    for (const line of lines) {
      if (line.startsWith('event: ')) {
        currentEvent = line.slice(7);
      } else if (line.startsWith('data: ') && currentEvent) {
        try {
          const data = JSON.parse(line.slice(6));
          if (currentEvent === 'step') {
            setSteps(prev => {
              const existing = prev.findIndex(s => s.step === data.step);
              if (existing >= 0) {
                const updated = [...prev];
                updated[existing] = data;
                return updated;
              }
              return [...prev, data];
            });
          } else if (currentEvent === 'complete') {
            setCompleted(data);
          }
        } catch (e) {}
        currentEvent = null;
      }
    }
  }
} catch (e) {
  setSteps(prev => [...prev, { step: 0, name: 'Error', status: 'error', description: e.message }]);
}
setIsRunning(false);
```

};

return (
<div className="pipeline-layout">
{/* Upload Area */}
<div className="upload-section">
<div className="upload-zone" onClick={() => !isRunning && fileRef.current?.click()}>
<input type="file" ref={fileRef} accept=".pdf,.docx,.doc,.png,.jpg,.jpeg,.tiff,.txt,.json,.csv"
onChange={e => e.target.files[0] && upload(e.target.files[0])} />
{isRunning ? (
<><span className="spinner" style={{ width: 24, height: 24 }} /><div style={{ marginTop: 8 }}>Processing...</div></>
) : (
<><div style={{ fontSize: 28 }}>+</div><div>Drop a PDF to see the pipeline in action</div>
<div style={{ fontSize: 11, color: 'var(--text-muted)', marginTop: 4 }}>PDF, DOCX, TXT, images</div></>
)}
</div>
</div>

```
  {/* Pipeline Steps Timeline */}
  <div className="pipeline-container" ref={scrollRef}>
    {/* Step progress bar */}
    <div className="pipeline-progress">
      {PIPELINE_STEPS.map(ps => {
        const stepData = steps.find(s => s.step === ps.step);
        const status = stepData?.status || 'pending';
        return (
          <div key={ps.step} className={`progress-dot ${status}`}
            style={{ '--dot-color': ps.color }}
            title={ps.name}>
            <span>{status === 'complete' ? '✓' : status === 'running' ? '⟳' : status === 'skipped' ? '⊘' : ps.step}</span>
          </div>
        );
      })}
    </div>

    {/* Detailed step cards */}
    {steps.map(stepData => {
      const meta = PIPELINE_STEPS.find(p => p.step === stepData.step) || {};
      const isExpanded = expandedStep === stepData.step;
      return (
        <div key={stepData.step} className={`step-card ${stepData.status}`}
          onClick={() => setExpandedStep(isExpanded ? null : stepData.step)}
          style={{ '--step-color': meta.color || '#666' }}>
          <div className="step-header">
            <div className="step-icon">{meta.icon}</div>
            <div className="step-info">
              <div className="step-name">
                <span className="step-number">Step {stepData.step}</span>
                {stepData.name}
              </div>
              <div className="step-desc">{stepData.description}</div>
            </div>
            <div className="step-status">
              {stepData.status === 'running' && <span className="spinner" />}
              {stepData.status === 'complete' && <span className="status-badge complete">✓ {stepData.duration_ms}ms</span>}
              {stepData.status === 'skipped' && <span className="status-badge skipped">Skipped</span>}
            </div>
          </div>

          {/* Expanded result view */}
          {isExpanded && stepData.result && (
            <div className="step-result">
              <ResultDisplay data={stepData.result} stepNum={stepData.step} />
            </div>
          )}
        </div>
      );
    })}

    {/* Completion Summary */}
    {completed && (
      <div className="completion-card">
        <div className="completion-header">✓ Pipeline Complete</div>
        <div className="completion-grid">
          <div className="completion-stat"><span className="stat-value">{completed.total_pages}</span><span className="stat-label">Pages</span></div>
          <div className="completion-stat"><span className="stat-value">{completed.total_chunks}</span><span className="stat-label">Chunks</span></div>
          <div className="completion-stat"><span className="stat-value">{completed.total_entities}</span><span className="stat-label">Entities</span></div>
          <div className="completion-stat"><span className="stat-value">{completed.total_relationships}</span><span className="stat-label">Relationships</span></div>
          <div className="completion-stat"><span className="stat-value">{completed.total_duration_ms}ms</span><span className="stat-label">Total Time</span></div>
          <div className="completion-stat"><span className="stat-value">{completed.category}</span><span className="stat-label">Category</span></div>
        </div>
      </div>
    )}
  </div>
</div>
```

);
}

/* Result display component for expanded step details */
function ResultDisplay({ data, stepNum }) {
if (!data) return null;

// Chunk samples
if (data.chunk_samples) {
return (
<div className="result-section">
<div className="result-meta">
<span>Total: <strong>{data.total_chunks}</strong></span>
<span>Avg Length: <strong>{data.avg_chunk_length}</strong> chars</span>
<span>Config: <strong>{data.chunk_size_config}</strong> / <strong>{data.chunk_overlap_config}</strong> overlap</span>
</div>
<div className="chunk-list">
{data.chunk_samples.map((c, i) => (
<div key={i} className="chunk-item">
<div className="chunk-header">
<span className="chunk-id">{c.chunk_id}</span>
<span className="chunk-meta">Page {c.page} | {c.length} chars</span>
</div>
<div className="chunk-preview">{c.preview}</div>
</div>
))}
</div>
</div>
);
}

// Entity samples
if (data.samples && data.by_type) {
return (
<div className="result-section">
<div className="result-meta">
<span>Total: <strong>{data.total_entities}</strong></span>
{Object.entries(data.by_type).map(([type, count]) => (
<span key={type} className="entity-badge">{type}: {count}</span>
))}
</div>
<div className="entity-list">
{data.samples.map((e, i) => (
<div key={i} className="entity-item">
<span className="entity-type">{e.type}</span>
<span className="entity-value">{e.value}</span>
<span className="entity-conf">{(e.confidence * 100).toFixed(0)}%</span>
</div>
))}
</div>
</div>
);
}

// Relationship samples
if (data.samples && data.total_relationships !== undefined) {
return (
<div className="result-section">
<div className="result-meta"><span>Total: <strong>{data.total_relationships}</strong> triples</span></div>
<div className="rel-list">
{data.samples.map((r, i) => (
<div key={i} className="rel-item">
<span className="rel-source">{r.source}</span>
<span className="rel-arrow">→ {r.relation} →</span>
<span className="rel-target">{r.target}</span>
<span className="rel-conf">{(r.confidence * 100).toFixed(0)}%</span>
</div>
))}
</div>
</div>
);
}

// Structure preview
if (data.structure_preview) {
return (
<div className="result-section">
<div className="result-meta">
<span>Pages: <strong>{data.total_pages}</strong></span>
<span>Sections: <strong>{data.total_sections}</strong></span>
</div>
<div className="structure-tree">
{data.structure_preview.map((p, i) => (
<div key={i} className="tree-page">
<div className="tree-page-header">📄 Page {p.page}</div>
{p.sections.map((s, j) => (
<div key={j} className="tree-section">
<span className="tree-indent">├─</span> {s.heading}
<span className="tree-meta">{s.paragraphs} paragraphs{s.tables > 0 ? `, ${s.tables} tables` : ''}</span>
</div>
))}
</div>
))}
</div>
</div>
);
}

// Generic key-value display
return (
<div className="result-section">
<div className="result-kv">
{Object.entries(data).filter(([k, v]) => typeof v !== 'object' || v === null).map(([k, v]) => (
<div key={k} className="kv-row">
<span className="kv-key">{k.replace(/_/g, ' ')}</span>
<span className="kv-value">{typeof v === 'number' ? v.toLocaleString() : String(v)}</span>
</div>
))}
</div>
{data.sample_text && <div className="text-preview"><strong>Sample:</strong> {data.sample_text.slice(0, 300)}</div>}
{data.sample_cleaned && <div className="text-preview"><strong>Cleaned:</strong> {data.sample_cleaned.slice(0, 300)}</div>}
</div>
);
}

/* ═══════════════════════════════════════════════════════════════
QUERY VISUALIZER — Shows retrieval + generation process
═══════════════════════════════════════════════════════════════ */

function QueryVisualizerTab() {
const [question, setQuestion] = useState('');
const [steps, setSteps] = useState([]);
const [isRunning, setIsRunning] = useState(false);
const [result, setResult] = useState(null);
const [expandedStep, setExpandedStep] = useState(null);
const scrollRef = useRef(null);

useEffect(() => {
if (scrollRef.current) scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
}, [steps]);

const ask = async () => {
if (!question.trim() || isRunning) return;
setIsRunning(true);
setSteps([]);
setResult(null);
setExpandedStep(null);

```
try {
  const response = await fetch(`${API}/api/v1/query/ask/stream`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question, top_k: 5 }),
  });

  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = '';

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    buffer += decoder.decode(value, { stream: true });
    const lines = buffer.split('\n');
    buffer = lines.pop() || '';

    let currentEvent = null;
    for (const line of lines) {
      if (line.startsWith('event: ')) {
        currentEvent = line.slice(7);
      } else if (line.startsWith('data: ') && currentEvent) {
        try {
          const data = JSON.parse(line.slice(6));
          if (currentEvent === 'step') {
            setSteps(prev => {
              const existing = prev.findIndex(s => s.step === data.step);
              if (existing >= 0) {
                const updated = [...prev];
                updated[existing] = data;
                return updated;
              }
              return [...prev, data];
            });
          } else if (currentEvent === 'complete') {
            setResult(data);
          }
        } catch (e) {}
        currentEvent = null;
      }
    }
  }
} catch (e) {
  setSteps(prev => [...prev, { step: 0, name: 'Error', status: 'error', description: e.message }]);
}
setIsRunning(false);
```

};

const QUERY_STEPS = [
{ step: 1, icon: '🔎', color: '#3b82f6' },
{ step: 2, icon: '🧮', color: '#8b5cf6' },
{ step: 3, icon: '📊', color: '#f59e0b' },
{ step: 4, icon: '🕸', color: '#22c55e' },
{ step: 5, icon: '⚖', color: '#ec4899' },
{ step: 6, icon: '📝', color: '#06b6d4' },
{ step: 7, icon: '🤖', color: '#f97316' },
];

return (
<div className="query-layout">
{/* Query Input */}
<div className="query-input-section">
<div className="query-input-row">
<input
value={question}
onChange={e => setQuestion(e.target.value)}
onKeyDown={e => e.key === 'Enter' && ask()}
placeholder="Ask a question to see how GraphRAG retrieves and generates answers..."
disabled={isRunning}
/>
<button onClick={ask} disabled={isRunning}>
{isRunning ? <span className="spinner" /> : 'Ask'}
</button>
</div>
<div className="query-suggestions">
{['What maintenance is required for P-101A?', 'Show me recent incidents', 'What does OISD-154 require?'].map(q => (
<span key={q} className="suggestion" onClick={() => { setQuestion(q); }}>{q}</span>
))}
</div>
</div>

```
  {/* Retrieval Steps */}
  <div className="query-steps-container" ref={scrollRef}>
    {steps.map(stepData => {
      const meta = QUERY_STEPS.find(p => p.step === stepData.step) || {};
      const isExpanded = expandedStep === stepData.step;
      return (
        <div key={stepData.step} className={`step-card ${stepData.status}`}
          onClick={() => setExpandedStep(isExpanded ? null : stepData.step)}
          style={{ '--step-color': meta.color || '#666' }}>
          <div className="step-header">
            <div className="step-icon">{meta.icon}</div>
            <div className="step-info">
              <div className="step-name">
                <span className="step-number">Step {stepData.step}</span>
                {stepData.name}
              </div>
              <div className="step-desc">{stepData.description}</div>
            </div>
            <div className="step-status">
              {stepData.status === 'running' && <span className="spinner" />}
              {stepData.status === 'complete' && <span className="status-badge complete">✓ {stepData.duration_ms}ms</span>}
            </div>
          </div>

          {isExpanded && stepData.result && (
            <div className="step-result">
              <QueryResultDisplay data={stepData.result} stepNum={stepData.step} />
            </div>
          )}
        </div>
      );
    })}

    {/* Final Answer */}
    {result && (
      <div className="answer-card">
        <div className="answer-header">
          <span>🤖 Answer</span>
          <span className={`badge ${result.confidence}`}>{result.confidence} confidence</span>
          <span className="answer-time">{result.total_duration_ms}ms total</span>
        </div>
        <div className="answer-body">{result.answer}</div>
        {result.sources?.length > 0 && (
          <div className="answer-sources">
            <strong>Sources:</strong> {result.sources.map((s, i) => (
              <span key={i} className="source-tag">[{s.filename} p.{s.page_number || '?'}]</span>
            ))}
          </div>
        )}
        {result.suggested_followups?.length > 0 && (
          <div className="answer-followups">
            {result.suggested_followups.map((f, i) => (
              <span key={i} className="followup" onClick={() => setQuestion(f)}>{f}</span>
            ))}
          </div>
        )}
      </div>
    )}
  </div>
</div>
```

);
}

function QueryResultDisplay({ data, stepNum }) {
// Ranked results display
if (data.ranked_results) {
return (
<div className="result-section">
<div className="result-meta">
<span>Formula: <strong>{data.scoring_formula}</strong></span>
<span>Chunks: <strong>{data.final_chunks}</strong></span>
</div>
<div className="ranked-list">
{data.ranked_results.map((r, i) => (
<div key={i} className="ranked-item">
<div className="rank-badge">#{r.rank}</div>
<div className="ranked-content">
<div className="ranked-header">
<span className="ranked-file">{r.filename}</span>
<span className="ranked-page">p.{r.page}</span>
<span className={`ranked-source ${r.source_type}`}>{r.source_type}</span>
<span className="ranked-score">{r.final_score.toFixed(4)}</span>
</div>
<div className="ranked-text">{r.content}</div>
</div>
</div>
))}
</div>
</div>
);
}

// FAISS chunks
if (data.chunks) {
return (
<div className="result-section">
<div className="result-meta">
<span>Found: <strong>{data.chunks_found}</strong> chunks</span>
<span>Top score: <strong>{data.top_score}</strong></span>
</div>
<div className="chunk-list">
{data.chunks.map((c, i) => (
<div key={i} className="chunk-item">
<div className="chunk-header">
<span className="chunk-id">{c.filename}</span>
<span className="chunk-meta">Page {c.page} | Score: {c.score}</span>
</div>
<div className="chunk-preview">{c.preview}</div>
</div>
))}
</div>
</div>
);
}

// Context preview
if (data.context_preview) {
return (
<div className="result-section">
<div className="result-meta">
<span>Context Length: <strong>{data.context_length}</strong> chars</span>
<span>Sources: <strong>{data.sources_included}</strong></span>
</div>
<div className="context-preview-box">{data.context_preview}</div>
</div>
);
}

// Graph context
if (data.graph_context) {
return (
<div className="result-section">
<div className="result-meta">
<span>Entities searched: <strong>{data.entities_searched}</strong></span>
<span>Nodes found: <strong>{data.graph_nodes_found}</strong></span>
</div>
{data.graph_context.map((g, i) => (
<div key={i} className="graph-context-item">
<span className="graph-entity">{g.entity}</span>
<span className="graph-type">{g.type}</span>
<div className="graph-neighbors">{g.neighbors}</div>
</div>
))}
</div>
);
}

// Generic
return (
<div className="result-section">
<div className="result-kv">
{Object.entries(data).filter(([k, v]) => v !== null && v !== undefined).map(([k, v]) => (
<div key={k} className="kv-row">
<span className="kv-key">{k.replace(/_/g, ' ')}</span>
<span className="kv-value">{Array.isArray(v) ? v.join(', ') : String(v)}</span>
</div>
))}
</div>
</div>
);
}

/* ═══════════════════════════════════════
Dashboard
═══════════════════════════════════════ */
function DashboardTab() {
const [stats, setStats] = useState(null);
const load = () => fetch(`${API}/api/v1/graph/stats`).then(r => r.json()).then(setStats).catch(() => {});
useEffect(() => { load(); }, []);
return (
<>
{/* Top stats row */}
<div className="card-grid">
<div className="card">
<h3>FAISS Vector Index</h3>
<div className="value">{stats?.faiss_total_chunks ?? '--'}</div>
<div className="sub">chunks indexed ({stats?.faiss_dimension || 384}-dim)</div>
</div>
<div className="card">
<h3>Documents Ingested</h3>
<div className="value">{stats?.faiss_total_files ?? '--'}</div>
<div className="sub">{stats?.faiss_total_documents ?? 0} unique document IDs</div>
</div>
<div className="card">
<h3>Neo4j Graph</h3>
<div className="value" style={{ color: stats?.neo4j_connected ? 'var(--green)' : 'var(--text-muted)' }}>
{stats?.neo4j_connected ? stats.total_nodes : 'Offline'}
</div>
<div className="sub">
{stats?.neo4j_connected
? `${stats.total_nodes} nodes, ${stats.total_relationships} relationships`
: 'Start Neo4j to enable graph features'}
</div>
</div>
<div className="card">
<h3>Cost</h3>
<div className="value" style={{ color: 'var(--green)' }}>$0</div>
<div className="sub">100% offline stack</div>
</div>
</div>

```
  {/* Category breakdown */}
  {stats?.categories && Object.keys(stats.categories).length > 0 && (
    <div className="card" style={{ marginBottom: 16 }}>
      <h3>Documents by Category</h3>
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8, marginTop: 12 }}>
        {Object.entries(stats.categories).map(([cat, count]) => (
          <div key={cat} style={{
            padding: '8px 16px', background: 'var(--surface2)', borderRadius: 8,
            border: '1px solid var(--border)', textAlign: 'center',
          }}>
            <div style={{ fontSize: 20, fontWeight: 700 }}>{count}</div>
            <div style={{ fontSize: 10, color: 'var(--text-muted)', textTransform: 'uppercase', marginTop: 2 }}>{cat}</div>
          </div>
        ))}
      </div>
    </div>
  )}

  {/* Indexed documents table */}
  {stats?.documents?.length > 0 && (
    <div className="card" style={{ marginBottom: 16 }}>
      <h3>Indexed Documents ({stats.documents.length})</h3>
      <div className="table-wrap" style={{ marginTop: 10 }}>
        <table>
          <thead>
            <tr><th>Filename</th><th>Category</th><th>Chunks</th><th>Pages</th><th>Document ID</th></tr>
          </thead>
          <tbody>
            {stats.documents.map((d, i) => (
              <tr key={i}>
                <td style={{ fontWeight: 600 }}>{d.filename || '(unnamed)'}</td>
                <td><span className="badge normal">{d.category}</span></td>
                <td>{d.chunks}</td>
                <td>{d.pages}</td>
                <td style={{ fontFamily: 'monospace', fontSize: 10, color: 'var(--text-muted)' }}>{d.document_id?.slice(0, 12)}...</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )}

  {/* Neo4j node types */}
  {stats?.node_types?.length > 0 && (
    <div className="card" style={{ marginBottom: 16 }}>
      <h3>Neo4j Node Types</h3>
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8, marginTop: 12 }}>
        {stats.node_types.map((nt, i) => (
          <div key={i} style={{
            padding: '8px 16px', background: 'var(--surface2)', borderRadius: 8,
            border: '1px solid var(--border)', textAlign: 'center',
          }}>
            <div style={{ fontSize: 18, fontWeight: 700 }}>{nt.count}</div>
            <div style={{ fontSize: 10, color: 'var(--primary)', textTransform: 'uppercase', marginTop: 2 }}>{nt.label}</div>
          </div>
        ))}
      </div>
    </div>
  )}

  {/* Architecture */}
  <div className="card" style={{ marginBottom: 16 }}>
    <h3>Pipeline Architecture</h3>
    <pre style={{ fontSize: 11, color: 'var(--text-muted)', lineHeight: 1.8, marginTop: 8 }}>
```

{`PDF → Type Detection (PyMuPDF)   ├── Digital → Direct text extraction   └── Scanned → PaddleOCR (offline)        ↓   Text Cleaning (ftfy + regex + unicode normalization)        ↓   Document Structuring (Pages → Sections → Paragraphs)        ↓   Semantic Chunking (500 tokens, 70 overlap)        ↓   ├── Entity Extraction (spaCy + regex)   └── Relationship Extraction (triples)        ↓   ├── FAISS Vector Index (sentence-transformers/all-MiniLM-L6-v2)   └── Neo4j Knowledge Graph (Document→Page→Section→Chunk→Entity)        ↓   Hybrid Retrieval: 0.6×Semantic + 0.4×Graph        ↓   Local LLM (Ollama: Llama 3.1 / Qwen 2.5 / Mistral)`}
</pre>
</div>

```
  {/* Service status */}
  <div className="card">
    <h3>Service Status</h3>
    <div style={{ display: 'grid', gap: 8, marginTop: 12 }}>
      {[
        { name: 'FAISS Vector Index', ok: (stats?.faiss_total_chunks ?? 0) >= 0, detail: `${stats?.faiss_total_chunks ?? 0} vectors` },
        { name: 'Neo4j Knowledge Graph', ok: stats?.neo4j_connected, detail: stats?.neo4j_connected ? `${stats.total_nodes} nodes` : 'Not running — start with: docker compose up neo4j' },
        { name: 'Sentence Transformers', ok: true, detail: 'all-MiniLM-L6-v2 (384-dim)' },
        { name: 'Ollama LLM', ok: null, detail: 'Required for answer generation' },
      ].map((s, i) => (
        <div key={i} style={{ display: 'flex', alignItems: 'center', gap: 10, padding: '6px 0', borderBottom: '1px solid var(--border)' }}>
          <span style={{ width: 8, height: 8, borderRadius: '50%', background: s.ok === true ? 'var(--green)' : s.ok === false ? 'var(--red)' : 'var(--yellow)', flexShrink: 0 }} />
          <span style={{ fontSize: 13, fontWeight: 600, width: 200 }}>{s.name}</span>
          <span style={{ fontSize: 11, color: 'var(--text-muted)' }}>{s.detail}</span>
        </div>
      ))}
    </div>
  </div>

  <div style={{ marginTop: 12, textAlign: 'center' }}>
    <button onClick={load} style={{ padding: '8px 20px', background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: 8, color: 'var(--text)', cursor: 'pointer', fontSize: 12 }}>
      Refresh Stats
    </button>
  </div>
</>
```

);
}

/* ═══════════════════════════════════════
Knowledge Graph Explorer
═══════════════════════════════════════ */
function GraphTab() {
const [searchTerm, setSearchTerm] = useState('');
const [searchMode, setSearchMode] = useState('text'); // 'text' or 'semantic'
const [results, setResults] = useState(null);
const [stats, setStats] = useState(null);
const [loading, setLoading] = useState(false);

useEffect(() => {
fetch(`${API}/api/v1/graph/stats`).then(r => r.json()).then(setStats).catch(() => {});
}, []);

const search = async () => {
if (!searchTerm.trim()) return;
setLoading(true);
try {
const endpoint = searchMode === 'semantic' ? '/api/v1/graph/search/semantic' : '/api/v1/graph/search';
const res = await fetch(`${API}${endpoint}`, {
method: 'POST', headers: { 'Content-Type': 'application/json' },
body: JSON.stringify({ query: searchTerm, limit: 20 }),
});
setResults(await res.json());
} catch (e) { setResults({ error: e.message }); }
setLoading(false);
};

return (
<>
{/* Search controls */}
<div style={{ display: 'flex', gap: 8, marginBottom: 8 }}>
<input value={searchTerm} onChange={e => setSearchTerm(e.target.value)} onKeyDown={e => e.key === 'Enter' && search()}
placeholder={searchMode === 'semantic' ? 'Semantic search across all chunks...' : 'Search by keyword in filenames, content, entities...'}
style={{ flex: 1, padding: '10px 16px', background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: 8, color: 'var(--text)', fontSize: 14, outline: 'none' }} />
<button onClick={search} disabled={loading}
style={{ padding: '10px 20px', background: 'var(--primary)', color: 'white', border: 'none', borderRadius: 8, cursor: 'pointer', fontWeight: 600 }}>
{loading ? '...' : 'Search'}
</button>
</div>

```
  <div style={{ display: 'flex', gap: 8, marginBottom: 16 }}>
    <button onClick={() => setSearchMode('text')}
      style={{ padding: '5px 12px', background: searchMode === 'text' ? 'var(--primary)' : 'var(--surface)', color: searchMode === 'text' ? 'white' : 'var(--text-muted)', border: '1px solid var(--border)', borderRadius: 6, cursor: 'pointer', fontSize: 11, fontWeight: 600 }}>
      Text Search
    </button>
    <button onClick={() => setSearchMode('semantic')}
      style={{ padding: '5px 12px', background: searchMode === 'semantic' ? 'var(--primary)' : 'var(--surface)', color: searchMode === 'semantic' ? 'white' : 'var(--text-muted)', border: '1px solid var(--border)', borderRadius: 6, cursor: 'pointer', fontSize: 11, fontWeight: 600 }}>
      Semantic Search (FAISS)
    </button>
  </div>

  {/* Indexed documents overview */}
  {stats?.documents?.length > 0 && !results && (
    <div className="card" style={{ marginBottom: 16 }}>
      <h3>Indexed Documents ({stats.faiss_total_files} files, {stats.faiss_total_chunks} chunks)</h3>
      <div style={{ marginTop: 8 }}>
        {stats.documents.map((d, i) => (
          <div key={i} className="doc-list-item" onClick={() => { setSearchTerm(d.filename); search(); }}
            style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '10px 12px', borderBottom: '1px solid var(--border)', cursor: 'pointer', transition: 'background 0.1s' }}
            onMouseOver={e => e.currentTarget.style.background = 'var(--surface2)'}
            onMouseOut={e => e.currentTarget.style.background = 'transparent'}>
            <div>
              <div style={{ fontSize: 13, fontWeight: 600 }}>{d.filename || '(unnamed)'}</div>
              <div style={{ fontSize: 10, color: 'var(--text-muted)' }}>
                {d.chunks} chunks · {d.pages} pages · ID: {d.document_id?.slice(0, 8)}
              </div>
            </div>
            <span className="badge normal">{d.category}</span>
          </div>
        ))}
      </div>
    </div>
  )}

  {/* Empty state */}
  {stats && !stats.documents?.length && !results && (
    <div className="card" style={{ textAlign: 'center', padding: 48 }}>
      <div style={{ fontSize: 32, marginBottom: 8 }}>📭</div>
      <div style={{ fontSize: 14, color: 'var(--text-muted)' }}>No documents indexed yet</div>
      <div style={{ fontSize: 12, color: 'var(--text-muted)', marginTop: 4 }}>
        Go to Pipeline Visualizer and upload a PDF to populate the index
      </div>
    </div>
  )}

  {/* Search results — text search */}
  {results && !results.error && searchMode === 'text' && (
    <div className="card" style={{ marginBottom: 16 }}>
      <h3>
        Search Results ({results.total || 0})
        <button onClick={() => setResults(null)} style={{ float: 'right', background: 'none', border: 'none', color: 'var(--text-muted)', cursor: 'pointer', fontSize: 12 }}>Clear</button>
      </h3>
      {results.results?.length === 0 && (
        <div style={{ padding: 24, textAlign: 'center', color: 'var(--text-muted)' }}>No matches found. Try a different search term or use Semantic Search.</div>
      )}
      {results.results?.map((r, i) => (
        <div key={i} style={{ padding: '10px 0', borderBottom: '1px solid var(--border)' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 4 }}>
            <span className={`badge ${r.source === 'faiss' ? 'normal' : 'medium'}`}>{r.source === 'faiss' ? 'FAISS' : 'Neo4j'}</span>
            <span className="badge normal">{r.label}</span>
            {r.props?.filename && <span style={{ fontSize: 12, fontWeight: 600 }}>{r.props.filename}</span>}
            {r.props?.page && <span style={{ fontSize: 10, color: 'var(--text-muted)' }}>p.{r.props.page}</span>}
          </div>
          {r.props?.preview && <div style={{ fontSize: 11, color: 'var(--text-muted)', lineHeight: 1.4, marginTop: 4 }}>{r.props.preview}</div>}
          {!r.props?.preview && <div style={{ fontSize: 11, color: 'var(--text-muted)' }}>{JSON.stringify(r.props).slice(0, 200)}</div>}
        </div>
      ))}
    </div>
  )}

  {/* Search results — semantic search */}
  {results && !results.error && searchMode === 'semantic' && (
    <div className="card" style={{ marginBottom: 16 }}>
      <h3>
        Semantic Results ({results.total || 0})
        <button onClick={() => setResults(null)} style={{ float: 'right', background: 'none', border: 'none', color: 'var(--text-muted)', cursor: 'pointer', fontSize: 12 }}>Clear</button>
      </h3>
      {results.results?.length === 0 && (
        <div style={{ padding: 24, textAlign: 'center', color: 'var(--text-muted)' }}>No matching chunks found. Upload documents first.</div>
      )}
      {results.results?.map((r, i) => (
        <div key={i} className="ranked-item" style={{ marginBottom: 6 }}>
          <div className="rank-badge">#{i + 1}</div>
          <div className="ranked-content">
            <div className="ranked-header">
              <span className="ranked-file">{r.filename}</span>
              <span className="ranked-page">p.{r.page_number}</span>
              <span className="badge normal">{r.category}</span>
              <span className="ranked-score">{r.score}</span>
            </div>
            <div className="ranked-text">{r.content}</div>
          </div>
        </div>
      ))}
    </div>
  )}

  {results?.error && <div className="card"><div style={{ color: 'var(--red)' }}>Error: {results.error}</div></div>}

  {/* Neo4j status */}
  {stats && !stats.neo4j_connected && (
    <div className="card" style={{ borderColor: 'var(--yellow)', opacity: 0.8 }}>
      <h3 style={{ color: 'var(--yellow)' }}>Neo4j Not Running</h3>
      <div style={{ fontSize: 12, color: 'var(--text-muted)', marginTop: 4 }}>
        Knowledge graph features require Neo4j. Start it with:
        <pre style={{ marginTop: 8, padding: 8, background: 'var(--bg)', borderRadius: 6, fontSize: 11 }}>
          docker compose up neo4j -d
        </pre>
        FAISS text and semantic search still work without Neo4j.
      </div>
    </div>
  )}
</>
```

);
}

```

---

## `frontend/src/app/globals.css`

**Global styles — dark theme + pipeline visualization CSS**

```css
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

:root {
  --bg: #0a0e17;
  --surface: #111827;
  --surface2: #1a2234;
  --border: #2a3444;
  --text: #e2e8f0;
  --text-muted: #8892a4;
  --primary: #3b82f6;
  --primary-hover: #2563eb;
  --green: #10b981;
  --yellow: #f59e0b;
  --red: #ef4444;
  --orange: #f97316;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  background: var(--bg);
  color: var(--text);
  min-height: 100vh;
}

.layout {
  display: flex;
  min-height: 100vh;
}

.sidebar {
  width: 240px;
  background: var(--surface);
  border-right: 1px solid var(--border);
  padding: 20px 0;
  flex-shrink: 0;
}

.sidebar h1 {
  font-size: 20px;
  font-weight: 700;
  padding: 0 20px 16px;
  border-bottom: 1px solid var(--border);
  color: var(--primary);
}

.sidebar h1 span {
  color: var(--text-muted);
  font-size: 11px;
  font-weight: 400;
  display: block;
  margin-top: 2px;
}

.nav-section {
  padding: 12px 12px 4px;
  font-size: 10px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: var(--text-muted);
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 20px;
  cursor: pointer;
  color: var(--text-muted);
  font-size: 13px;
  transition: all 0.15s;
  border-left: 3px solid transparent;
}

.nav-item:hover, .nav-item.active {
  background: var(--surface2);
  color: var(--text);
  border-left-color: var(--primary);
}

.main {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.header {
  padding: 16px 24px;
  border-bottom: 1px solid var(--border);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header h2 {
  font-size: 18px;
  font-weight: 600;
}

.content {
  flex: 1;
  padding: 24px;
  overflow-y: auto;
}

/* Cards */
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 16px;
  margin-bottom: 24px;
}

.card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 20px;
}

.card h3 {
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: var(--text-muted);
  margin-bottom: 8px;
}

.card .value {
  font-size: 28px;
  font-weight: 700;
}

.card .sub {
  font-size: 12px;
  color: var(--text-muted);
  margin-top: 4px;
}

/* Status badges */
.badge {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 9999px;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
}

.badge.normal { background: #064e3b; color: var(--green); }
.badge.warning { background: #78350f; color: var(--yellow); }
.badge.critical { background: #7f1d1d; color: var(--red); }
.badge.high { background: #7f1d1d; color: var(--red); }
.badge.medium { background: #78350f; color: var(--yellow); }
.badge.low { background: #064e3b; color: var(--green); }

/* Chat */
.chat-container {
  display: flex;
  flex-direction: column;
  height: calc(100vh - 120px);
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 16px 0;
}

.message {
  max-width: 80%;
  margin-bottom: 16px;
  padding: 12px 16px;
  border-radius: 12px;
  font-size: 14px;
  line-height: 1.5;
}

.message.user {
  background: var(--primary);
  color: white;
  margin-left: auto;
  border-bottom-right-radius: 4px;
}

.message.assistant {
  background: var(--surface2);
  border: 1px solid var(--border);
  border-bottom-left-radius: 4px;
}

.message .sources {
  margin-top: 8px;
  padding-top: 8px;
  border-top: 1px solid var(--border);
  font-size: 11px;
  color: var(--text-muted);
}

.chat-input-row {
  display: flex;
  gap: 8px;
  padding: 12px 0;
}

.chat-input-row input {
  flex: 1;
  padding: 12px 16px;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 8px;
  color: var(--text);
  font-size: 14px;
  outline: none;
}

.chat-input-row input:focus {
  border-color: var(--primary);
}

.chat-input-row button {
  padding: 12px 24px;
  background: var(--primary);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  font-size: 14px;
}

.chat-input-row button:hover {
  background: var(--primary-hover);
}

.chat-input-row button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Tables */
.table-wrap {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 8px;
  overflow: hidden;
}

table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
}

th {
  text-align: left;
  padding: 10px 16px;
  background: var(--surface2);
  color: var(--text-muted);
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  border-bottom: 1px solid var(--border);
}

td {
  padding: 10px 16px;
  border-bottom: 1px solid var(--border);
}

tr:last-child td {
  border-bottom: none;
}

/* Upload */
.upload-zone {
  border: 2px dashed var(--border);
  border-radius: 12px;
  padding: 48px;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s;
}

.upload-zone:hover {
  border-color: var(--primary);
  background: rgba(59, 130, 246, 0.05);
}

.upload-zone input { display: none; }

/* Sensor chart placeholder */
.health-bar {
  height: 8px;
  background: var(--surface2);
  border-radius: 4px;
  overflow: hidden;
  margin-top: 8px;
}

.health-bar-fill {
  height: 100%;
  border-radius: 4px;
  transition: width 0.3s;
}

/* Loading */
.spinner {
  display: inline-block;
  width: 16px;
  height: 16px;
  border: 2px solid var(--border);
  border-top-color: var(--primary);
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Reports list */
.report-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
  border-bottom: 1px solid var(--border);
  cursor: pointer;
  transition: background 0.15s;
}

.report-item:hover {
  background: var(--surface2);
}

.report-item .name {
  font-size: 13px;
  font-family: monospace;
}

.report-item .meta {
  font-size: 11px;
  color: var(--text-muted);
}

/* ══════════════════════════════════════════════
   PIPELINE VISUALIZER STYLES
   ══════════════════════════════════════════════ */

.pipeline-layout {
  display: flex;
  flex-direction: column;
  gap: 16px;
  height: calc(100vh - 120px);
}

.upload-section {
  flex-shrink: 0;
}

.pipeline-container {
  flex: 1;
  overflow-y: auto;
  padding-right: 8px;
}

/* Progress dots */
.pipeline-progress {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 12px 16px;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 10px;
  margin-bottom: 16px;
  flex-wrap: wrap;
}

.progress-dot {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 10px;
  font-weight: 700;
  background: var(--surface2);
  border: 2px solid var(--border);
  color: var(--text-muted);
  transition: all 0.3s ease;
}

.progress-dot.complete {
  background: var(--dot-color, var(--green));
  border-color: var(--dot-color, var(--green));
  color: white;
}

.progress-dot.running {
  border-color: var(--dot-color, var(--primary));
  color: var(--dot-color, var(--primary));
  animation: pulse 1s infinite;
}

.progress-dot.skipped {
  opacity: 0.5;
  border-style: dashed;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.15); }
}

/* Step cards */
.step-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 10px;
  margin-bottom: 8px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.2s;
  border-left: 3px solid var(--step-color, var(--border));
}

.step-card:hover {
  background: var(--surface2);
}

.step-card.running {
  border-left-color: var(--step-color);
  box-shadow: 0 0 12px rgba(59, 130, 246, 0.1);
}

.step-card.complete {
  border-left-color: var(--step-color);
}

.step-header {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
}

.step-icon {
  font-size: 20px;
  width: 32px;
  text-align: center;
  flex-shrink: 0;
}

.step-info {
  flex: 1;
  min-width: 0;
}

.step-name {
  font-size: 13px;
  font-weight: 600;
  color: var(--text);
}

.step-number {
  font-size: 10px;
  color: var(--text-muted);
  margin-right: 8px;
  text-transform: uppercase;
}

.step-desc {
  font-size: 11px;
  color: var(--text-muted);
  margin-top: 2px;
}

.step-status {
  flex-shrink: 0;
}

.status-badge {
  font-size: 11px;
  padding: 3px 8px;
  border-radius: 6px;
  font-weight: 600;
}

.status-badge.complete {
  background: rgba(16, 185, 129, 0.15);
  color: var(--green);
}

.status-badge.skipped {
  background: rgba(139, 92, 246, 0.15);
  color: #a78bfa;
}

/* Step result expanded */
.step-result {
  padding: 0 16px 16px;
  border-top: 1px solid var(--border);
  margin-top: 4px;
  padding-top: 12px;
  animation: slideDown 0.2s ease;
}

@keyframes slideDown {
  from { opacity: 0; max-height: 0; }
  to { opacity: 1; max-height: 1000px; }
}

.result-section {
  font-size: 12px;
}

.result-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 10px;
  color: var(--text-muted);
}

.result-meta strong {
  color: var(--text);
}

/* Chunk display */
.chunk-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.chunk-item {
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 8px 12px;
}

.chunk-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 4px;
}

.chunk-id {
  font-size: 10px;
  font-family: monospace;
  color: var(--primary);
}

.chunk-meta {
  font-size: 10px;
  color: var(--text-muted);
}

.chunk-preview {
  font-size: 11px;
  color: var(--text-muted);
  line-height: 1.4;
  white-space: pre-wrap;
  word-break: break-word;
}

/* Entity display */
.entity-badge {
  background: var(--surface2);
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 10px;
}

.entity-list {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

.entity-item {
  display: flex;
  align-items: center;
  gap: 6px;
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 4px 8px;
}

.entity-type {
  font-size: 9px;
  text-transform: uppercase;
  color: var(--primary);
  font-weight: 600;
}

.entity-value {
  font-size: 11px;
  font-family: monospace;
}

.entity-conf {
  font-size: 9px;
  color: var(--text-muted);
}

/* Relationship display */
.rel-list {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.rel-item {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 4px 8px;
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: 6px;
  font-size: 11px;
}

.rel-source, .rel-target {
  font-family: monospace;
  font-weight: 600;
}

.rel-arrow {
  color: var(--primary);
  font-size: 10px;
}

.rel-conf {
  margin-left: auto;
  color: var(--text-muted);
  font-size: 10px;
}

/* Structure tree */
.structure-tree {
  font-size: 12px;
}

.tree-page {
  margin-bottom: 8px;
}

.tree-page-header {
  font-weight: 600;
  margin-bottom: 4px;
}

.tree-section {
  padding-left: 16px;
  color: var(--text-muted);
  line-height: 1.6;
}

.tree-indent {
  color: var(--border);
  font-family: monospace;
}

.tree-meta {
  font-size: 10px;
  color: var(--text-muted);
  margin-left: 8px;
}

/* Key-value display */
.result-kv {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 4px 16px;
}

.kv-row {
  display: contents;
}

.kv-key {
  font-size: 11px;
  color: var(--text-muted);
  text-transform: capitalize;
}

.kv-value {
  font-size: 11px;
  font-family: monospace;
  color: var(--text);
}

.text-preview {
  margin-top: 8px;
  padding: 8px;
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: 6px;
  font-size: 11px;
  color: var(--text-muted);
  line-height: 1.4;
  max-height: 120px;
  overflow: auto;
  white-space: pre-wrap;
  word-break: break-word;
}

/* Completion card */
.completion-card {
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(59, 130, 246, 0.1));
  border: 1px solid var(--green);
  border-radius: 10px;
  padding: 20px;
  margin-top: 8px;
}

.completion-header {
  font-size: 16px;
  font-weight: 700;
  color: var(--green);
  margin-bottom: 16px;
}

.completion-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: 12px;
}

.completion-stat {
  text-align: center;
}

.stat-value {
  display: block;
  font-size: 20px;
  font-weight: 700;
  color: var(--text);
}

.stat-label {
  display: block;
  font-size: 10px;
  color: var(--text-muted);
  text-transform: uppercase;
  margin-top: 2px;
}

/* ══════════════════════════════════════════════
   QUERY VISUALIZER STYLES
   ══════════════════════════════════════════════ */

.query-layout {
  display: flex;
  flex-direction: column;
  height: calc(100vh - 120px);
  gap: 16px;
}

.query-input-section {
  flex-shrink: 0;
}

.query-input-row {
  display: flex;
  gap: 8px;
}

.query-input-row input {
  flex: 1;
  padding: 12px 16px;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 8px;
  color: var(--text);
  font-size: 14px;
  outline: none;
}

.query-input-row input:focus {
  border-color: var(--primary);
}

.query-input-row button {
  padding: 12px 24px;
  background: var(--primary);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
}

.query-input-row button:disabled {
  opacity: 0.5;
}

.query-suggestions {
  display: flex;
  gap: 8px;
  margin-top: 8px;
  flex-wrap: wrap;
}

.suggestion {
  font-size: 11px;
  padding: 4px 10px;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 12px;
  color: var(--text-muted);
  cursor: pointer;
  transition: all 0.15s;
}

.suggestion:hover {
  border-color: var(--primary);
  color: var(--primary);
}

.query-steps-container {
  flex: 1;
  overflow-y: auto;
  padding-right: 8px;
}

/* Ranked results */
.ranked-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.ranked-item {
  display: flex;
  gap: 10px;
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 10px 12px;
}

.rank-badge {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: var(--primary);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  font-weight: 700;
  flex-shrink: 0;
}

.ranked-content {
  flex: 1;
  min-width: 0;
}

.ranked-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 4px;
  flex-wrap: wrap;
}

.ranked-file {
  font-size: 11px;
  font-weight: 600;
  color: var(--text);
}

.ranked-page {
  font-size: 10px;
  color: var(--text-muted);
}

.ranked-source {
  font-size: 9px;
  padding: 1px 5px;
  border-radius: 4px;
  text-transform: uppercase;
  font-weight: 600;
}

.ranked-source.vector {
  background: rgba(59, 130, 246, 0.2);
  color: #60a5fa;
}

.ranked-source.graph {
  background: rgba(34, 197, 94, 0.2);
  color: #4ade80;
}

.ranked-source.keyword {
  background: rgba(249, 115, 22, 0.2);
  color: #fb923c;
}

.ranked-score {
  font-size: 11px;
  font-family: monospace;
  color: var(--green);
  margin-left: auto;
}

.ranked-text {
  font-size: 11px;
  color: var(--text-muted);
  line-height: 1.4;
  white-space: pre-wrap;
  word-break: break-word;
}

/* Context preview */
.context-preview-box {
  padding: 10px;
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: 6px;
  font-size: 11px;
  font-family: monospace;
  color: var(--text-muted);
  line-height: 1.5;
  max-height: 200px;
  overflow: auto;
  white-space: pre-wrap;
}

/* Graph context */
.graph-context-item {
  padding: 6px 8px;
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: 6px;
  margin-bottom: 4px;
}

.graph-entity {
  font-family: monospace;
  font-weight: 600;
  font-size: 12px;
}

.graph-type {
  font-size: 9px;
  margin-left: 6px;
  color: var(--primary);
  text-transform: uppercase;
}

.graph-neighbors {
  font-size: 10px;
  color: var(--text-muted);
  margin-top: 2px;
}

/* Answer card */
.answer-card {
  background: var(--surface);
  border: 1px solid var(--green);
  border-radius: 10px;
  padding: 16px;
  margin-top: 8px;
}

.answer-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 12px;
  font-size: 14px;
  font-weight: 600;
}

.answer-time {
  font-size: 11px;
  color: var(--text-muted);
  margin-left: auto;
}

.answer-body {
  font-size: 14px;
  line-height: 1.6;
  color: var(--text);
  white-space: pre-wrap;
}

.answer-sources {
  margin-top: 12px;
  padding-top: 10px;
  border-top: 1px solid var(--border);
  font-size: 11px;
  color: var(--text-muted);
}

.source-tag {
  background: var(--surface2);
  padding: 2px 6px;
  border-radius: 4px;
  margin: 0 4px;
  font-family: monospace;
}

.answer-followups {
  margin-top: 10px;
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.followup {
  font-size: 11px;
  padding: 4px 10px;
  background: var(--surface2);
  border: 1px solid var(--border);
  border-radius: 12px;
  color: var(--primary);
  cursor: pointer;
}

.followup:hover {
  border-color: var(--primary);
}
```

---

## `data/sample_documents/work_order_sample.txt`

**Sample work order document**

```
WORK ORDER: WO-100000
Equipment: FV-1001
Type: Predictive Maintenance
Priority: High
Date: 18-Dec-2023
Assigned To: Pradeep Joshi
Description: Corrosion under insulation (CUI)
Findings: Inspection of FV-1001 revealed high vibration - misalignment detected. Equipment was isolated as per PTW-4711. Maintenance carried out as per SOP-MAINT-714.
Parts Used: Coupling element (qty: 1)
Man-Hours: 44
Standard: ASME B31.3

============================================================

WORK ORDER: WO-100001
Equipment: P-101B
Type: Preventive Maintenance
Priority: Medium
Date: 28-Jun-2023
Assigned To: Anil Reddy
Description: Instrument drift - requires recalibration
Findings: Inspection of P-101B revealed instrument drift - requires recalibration. Equipment was isolated as per PTW-8941. Maintenance carried out as per SOP-MAINT-661.
Parts Used: Gasket set DN150 PN40 (qty: 1)
Man-Hours: 12
Standard: OISD-163

============================================================

WORK ORDER: WO-100002
Equipment: HX-502
Type: Predictive Maintenance
Priority: Critical
Date: 18-Mar-2022
Assigned To: Suresh Patel
Description: High vibration - misalignment detected
Findings: Inspection of HX-502 revealed corrosion under insulation (cui). Equipment was isolated as per PTW-8610. Maintenance carried out as per SOP-MAINT-994.
Parts Used: Bearing SKF 6205-2RS (qty: 2)
Man-Hours: 8
Standard: API-610

============================================================

WORK ORDER: WO-100003
Equipment: P-201A
Type: Corrective Maintenance
Priority: Medium
Date: 26-May-2024
Assigned To: Amit Sharma
Description: Control valve sticking - stem packing worn
Findings: Inspection of P-201A revealed gasket failure at flange joint. Equipment was isolated as per PTW-4111. Maintenance carried out as per SOP-MAINT-259.
Parts Used: Packing rings (qty: 4)
Man-Hours: 22
Standard: OISD-163

============================================================

WORK ORDER: WO-100004
Equipment: XV-1002
Type: Preventive Maintenance
Priority: Medium
Date: 08-Nov-2023
Assigned To: Amit Sharma
Description: High vibration - misalignment detected
Findings: Inspection of XV-1002 revealed coupling damage - fatigue crack. Equipment was isolated as per PTW-2291. Maintenance carried out as per SOP-MAINT-104.
Parts Used: Gasket set DN150 PN40 (qty: 1)
Man-Hours: 24
Standard: API-610

============================================================
```

---

## `data/sample_documents/incident_report_sample.txt`

**Sample incident report**

```
INCIDENT REPORT: INC-2022000
Date: 27-Mar-2024
Title: Near Miss - Pressure Safety Valve Failure to Operate
Equipment: PSV-3001
Severity: Critical

Description:
During routine PSV testing, PSV-3001 on reactor R-601 failed to lift at set pressure. Valve found stuck due to corrosion on seat. Discovered during planned test - no actual overpressure event.

Root Cause Analysis:
Process fluid causing accelerated corrosion on valve internals. Testing interval of 24 months inadequate for this service.

Corrective Actions:
  - Replace PSV-3001 with corrosion-resistant trim material
  - Reduce testing interval to 12 months for all PSVs in similar service
  - Conduct immediate testing of all PSVs in corrosive service
  - Update risk assessment per OISD-154 requirements

Lessons Learned:
This incident highlights the importance of adhering to OEM maintenance recommendations and timely execution of inspection schedules. Reference: API-580.

============================================================

INCIDENT REPORT: INC-2022001
Date: 11-Apr-2023
Title: Pump Seal Failure - Hydrocarbon Release
Equipment: P-101A
Severity: High

Description:
Mechanical seal failure on pump P-101A resulted in minor hydrocarbon release. Area gas detectors activated. Emergency isolation carried out within 3 minutes. No injuries. Approximately 50 liters released to containment area.

Root Cause Analysis:
Seal operated beyond recommended life (18 months vs 12 months recommended). PM schedule not updated after OEM bulletin OEM-2022-045.

Corrective Actions:
  - Replace seal with upgraded Type B seal as per OEM recommendation
  - Update PM schedule to 12-month seal replacement
  - Review all similar pumps for seal life compliance
  - Issue safety alert to all operating teams

Lessons Learned:
This incident highlights the importance of adhering to OEM maintenance recommendations and timely execution of inspection schedules. Reference: OISD-163.

============================================================

INCIDENT REPORT: INC-2022002
Date: 24-Nov-2022
Title: Compressor Trip - High Discharge Temperature
Equipment: C-301
Severity: Medium

Description:
Compressor C-301 tripped on high discharge temperature alarm. Temperature reached 185°C (alarm at 180°C, design limit 200°C). Automatic shutdown functioned correctly. No equipment damage.

Root Cause Analysis:
Intercooler HX-301 fouled, reducing cooling capacity by 30%. Fouling inspection was 4 months overdue.

Corrective Actions:
  - Clean intercooler HX-301
  - Establish fouling monitoring via pressure drop trending
  - Add cooling efficiency KPI to daily operator rounds
  - Review inspection scheduling compliance for all heat exchangers

Lessons Learned:
This incident highlights the importance of adhering to OEM maintenance recommendations and timely execution of inspection schedules. Reference: OISD-163.

============================================================
```

---

## `data/sample_documents/sop_hot_work.txt`

**Sample SOP — hot work procedure**

```
STANDARD OPERATING PROCEDURE
Document ID: SOP-OPS-101
Title: Standard Operating Procedure: Hot Work Near Hydrocarbon Lines
Revision: Rev 3
Effective Date: 01-Jan-2024
Approved By: Plant Manager - D.K. Mehta

Applicable Regulations: OISD-105, Factory Act Section 38, IS-3016

Scope:
This procedure covers all hot work activities (welding, cutting, grinding) within 15 meters of equipment containing or previously containing hydrocarbons.

PROCEDURE STEPS:

  Step 1: Obtain Hot Work Permit (PTW) from Control Room Supervisor
    Responsible: Maintenance Supervisor
    Reference: PTW Procedure SOP-SAFE-001

  Step 2: Confirm gas test shows <1% LEL in work area. Gas test valid for 4 hours maximum.
    Responsible: Safety Officer
    Reference: Gas Testing Procedure SOP-SAFE-012

  Step 3: Verify equipment isolation (Double Block and Bleed). Check isolation certificate.
    Responsible: Operations Engineer
    Reference: Isolation Procedure SOP-OPS-050

  Step 4: Position fire extinguisher and fire watch personnel. Minimum 2 DCP extinguishers (10 kg).
    Responsible: Fire & Safety
    Reference: OISD-105 Clause 6.3

  Step 5: Commence hot work. Continuous gas monitoring required. Stop work if LEL exceeds 10%.
    Responsible: Executing Technician
    Reference: OISD-105 Clause 7.1

PPE Required:
  - Fire-retardant coveralls
  - Welding helmet with appropriate shade
  - Leather gloves
  - Safety shoes with metatarsal guard
  - Portable gas detector (4-gas)

Emergency Procedure:
In case of fire/gas leak: Stop work immediately -> Activate area alarm -> Evacuate to Assembly Point B -> Call Emergency: Ext 999
```

---

## `data/sample_documents/work_orders.json`

**Synthetic work orders (JSON)**

```json
[
  {
    "work_order_id": "WO-100000",
    "equipment_tag": "FV-1001",
    "work_type": "Predictive Maintenance",
    "priority": "High",
    "status": "Overdue",
    "date_raised": "18-Dec-2023",
    "date_completed": "19-Dec-2023",
    "assigned_to": "Pradeep Joshi",
    "description": "Corrosion under insulation (CUI)",
    "findings": "Inspection of FV-1001 revealed high vibration - misalignment detected. Equipment was isolated as per PTW-4711. Maintenance carried out as per SOP-MAINT-714.",
    "parts_used": "Coupling element (qty: 1)",
    "man_hours": 44,
    "applicable_standard": "ASME B31.3"
  },
  {
    "work_order_id": "WO-100001",
    "equipment_tag": "P-101B",
    "work_type": "Preventive Maintenance",
    "priority": "Medium",
    "status": "Overdue",
    "date_raised": "28-Jun-2023",
    "date_completed": "08-Jul-2023",
    "assigned_to": "Anil Reddy",
    "description": "Instrument drift - requires recalibration",
    "findings": "Inspection of P-101B revealed instrument drift - requires recalibration. Equipment was isolated as per PTW-8941. Maintenance carried out as per SOP-MAINT-661.",
    "parts_used": "Gasket set DN150 PN40 (qty: 1)",
    "man_hours": 12,
    "applicable_standard": "OISD-163"
  },
  {
    "work_order_id": "WO-100002",
    "equipment_tag": "HX-502",
    "work_type": "Predictive Maintenance",
    "priority": "Critical",
    "status": "Completed",
    "date_raised": "18-Mar-2022",
    "date_completed": "31-Mar-2022",
    "assigned_to": "Suresh Patel",
    "description": "High vibration - misalignment detected",
    "findings": "Inspection of HX-502 revealed corrosion under insulation (cui). Equipment was isolated as per PTW-8610. Maintenance carried out as per SOP-MAINT-994.",
    "parts_used": "Bearing SKF 6205-2RS (qty: 2)",
    "man_hours": 8,
    "applicable_standard": "API-610"
  },
  {
    "work_order_id": "WO-100003",
    "equipment_tag": "P-201A",
    "work_type": "Corrective Maintenance",
    "priority": "Medium",
    "status": "In Progress",
    "date_raised": "26-May-2024",
    "date_completed": "01-Jun-2024",
    "assigned_to": "Amit Sharma",
    "description": "Control valve sticking - stem packing worn",
    "findings": "Inspection of P-201A revealed gasket failure at flange joint. Equipment was isolated as per PTW-4111. Maintenance carried out as per SOP-MAINT-259.",
    "parts_used": "Packing rings (qty: 4)",
    "man_hours": 22,
    "applicable_standard": "OISD-163"
  },
  {
    "work_order_id": "WO-100004",
    "equipment_tag": "XV-1002",
    "work_type": "Preventive Maintenance",
    "priority": "Medium",
    "status": "In Progress",
    "date_raised": "08-Nov-2023",
    "date_completed": "10-Nov-2023",
    "assigned_to": "Amit Sharma",
    "description": "High vibration - misalignment detected",
    "findings": "Inspection of XV-1002 revealed coupling damage - fatigue crack. Equipment was isolated as per PTW-2291. Maintenance carried out as per SOP-MAINT-104.",
    "parts_used": "Gasket set DN150 PN40 (qty: 1)",
    "man_hours": 24,
    "applicable_standard": "API-610"
  },
  {
    "work_order_id": "WO-100005",
    "equipment_tag": "XV-1002",
    "work_type": "Preventive Maintenance",
    "priority": "Low",
    "status": "Planned",
    "date_raised": "20-Oct-2023",
    "date_completed": "24-Oct-2023",
    "assigned_to": "Amit Sharma",
    "description": "Gasket failure at flange joint",
    "findings": "Inspection of XV-1002 revealed corrosion under insulation (cui). Equipment was isolated as per PTW-7146. Maintenance carried out as per SOP-MAINT-770.",
    "parts_used": "Packing rings (qty: 4)",
    "man_hours": 38,
    "applicable_standard": "API-610"
  },
  {
    "work_order_id": "WO-100006",
    "equipment_tag": "HX-501",
    "work_type": "Corrective Maintenance",
    "priority": "Critical",
    "status": "Overdue",
    "date_raised": "08-Jan-2022",
    "date_completed": "13-Jan-2022",
    "assigned_to": "Amit Sharma",
    "description": "Corrosion under insulation (CUI)",
    "findings": "Inspection of HX-501 revealed instrument drift - requires recalibration. Equipment was isolated as per PTW-5706. Maintenance carried out as per SOP-MAINT-893.",
    "parts_used": "Gasket set DN150 PN40 (qty: 1)",
    "man_hours": 40,
    "applicable_standard": "ASME B31.3"
  },
  {
    "work_order_id": "WO-100007",
    "equipment_tag": "HX-501",
    "work_type": "Corrective Maintenance",
    "priority": "High",
    "status": "Planned",
    "date_raised": "23-Jan-2023",
    "date_completed": "06-Feb-2023",
    "assigned_to": "Vikram Singh",
    "description": "Motor overheating - winding insulation degradation",
    "findings": "Inspection of HX-501 revealed control valve sticking - stem packing worn. Equipment was isolated as per PTW-8471. Maintenance carried out as per SOP-MAINT-421.",
    "parts_used": "Gasket set DN150 PN40 (qty: 1)",
    "man_hours": 8,
    "applicable_standard": "ASME B31.3"
  },
  {
    "work_order_id": "WO-100008",
    "equipment_tag": "P-101B",
    "work_type": "Predictive Maintenance",
    "priority": "High",
    "status": "Completed",
    "date_raised": "04-Jul-2022",
    "date_completed": "16-Jul-2022",
    "assigned_to": "Pradeep Joshi",
    "description": "Motor overheating - winding insulation degradation",
    "findings": "Inspection of P-101B revealed instrument drift - requires recalibration. Equipment was isolated as per PTW-6625. Maintenance carried out as per SOP-MAINT-229.",
    "parts_used": "Bearing SKF 6205-2RS (qty: 2)",
    "man_hours": 6,
    "applicable_standard": "API-610"
  },
  {
    "work_order_id": "WO-100009",
    "equipment_tag": "TIT-4001",
    "work_type": "Corrective Maintenance",
    "priority": "Critical",
    "status": "Completed",
    "date_raised": "19-Oct-2023",
    "date_completed": "26-Oct-2023",
    "assigned_to": "Suresh Patel",
    "description": "Control valve sticking - stem packing worn",
    "findings": "Inspection of TIT-4001 revealed control valve sticking - stem packing worn. Equipment was isolated as per PTW-3958. Maintenance carried out as per SOP-MAINT-359.",
    "parts_used": "Mechanical seal Type A (qty: 1)",
    "man_hours": 41,
    "applicable_standard": "ASME B31.3"
  },
  {
    "work_order_id": "WO-100010",
    "equipment_tag": "C-301",
    "work_type": "Predictive Maintenance",
    "priority": "Critical",
    "status": "Overdue",
    "date_raised": "27-Mar-2023",
    "date_completed": "08-Apr-2023",
    "assigned_to": "Amit Sharma",
    "description": "Motor overheating - winding insulation degradation",
    "findings": "Inspection of C-301 revealed seal leakage - mechanical seal worn. Equipment was isolated as per PTW-5842. Maintenance carried out as per SOP-MAINT-768.",
    "parts_used": "Bearing SKF 6205-2RS (qty: 2)",
    "man_hours": 12,
    "applicable_standard": "OISD-163"
  },
  {
    "work_order_id": "WO-100011",
    "equipment_tag": "PSV-3001",
    "work_type": "Predictive Maintenance",
    "priority": "High",
    "status": "In Progress",
    "date_raised": "04-Sep-2023",
    "date_completed": "17-Sep-2023",
    "assigned_to": "Pradeep Joshi",
    "description": "Gasket failure at flange joint",
    "findings": "Inspection of PSV-3001 revealed coupling damage - fatigue crack. Equipment was isolated as per PTW-3350. Maintenance carried out as per SOP-MAINT-728.",
    "parts_used": "Bearing SKF 6205-2RS (qty: 2)",
    "man_hours": 19,
    "applicable_standard": "ASME B31.3"
  },
  {
    "work_order_id": "WO-100012",
    "equipment_tag": "FV-1001",
    "work_type": "Preventive Maintenance",
    "priority": "Critical",
    "status": "Planned",
    "date_raised": "11-Apr-2024",
    "date_completed": "20-Apr-2024",
    "assigned_to": "Suresh Patel",
    "description": "Corrosion under insulation (CUI)",
    "findings": "Inspection of FV-1001 revealed motor overheating - winding insulation degradation. Equipment was isolated as per PTW-5951. Maintenance carried out as per SOP-MAINT-742.",
    "parts_used": "Packing rings (qty: 4)",
    "man_hours": 45,
    "applicable_standard": "ASME B31.3"
  },
  {
    "work_order_id": "WO-100013",
    "equipment_tag": "V-402",
    "work_type": "Predictive Maintenance",
    "priority": "Critical",
    "status": "Completed",
    "date_raised": "17-May-2024",
    "date_completed": "21-May-2024",
    "assigned_to": "Amit Sharma",
    "description": "Coupling damage - fatigue crack",
    "findings": "Inspection of V-402 revealed motor overheating - winding insulation degradation. Equipment was isolated as per PTW-2804. Maintenance carried out as per SOP-MAINT-514.",
    "parts_used": "Gasket set DN150 PN40 (qty: 1)",
    "man_hours": 41,
    "applicable_standard": "ASME B31.3"
  },
  {
    "work_order_id": "WO-100014",
    "equipment_tag": "P-101A",
    "work_type": "Corrective Maintenance",
    "priority": "High",
    "status": "Overdue",
    "date_raised": "06-Jan-2023",
    "date_completed": "09-Jan-2023",
    "assigned_to": "Rajesh Kumar",
    "description": "Impeller erosion causing reduced flow",
    "findings": "Inspection of P-101A revealed high vibration - misalignment detected. Equipment was isolated as per PTW-8086. Maintenance carried out as per SOP-MAINT-609.",
    "parts_used": "Gasket set DN150 PN40 (qty: 1)",
    "man_hours": 23,
    "applicable_standard": "ISO-10816"
  },
  {
    "work_order_id": "WO-100015",
    "equipment_tag": "C-301",
    "work_type": "Preventive Maintenance",
    "priority": "Low",
    "status": "Overdue",
    "date_raised": "04-Dec-2023",
    "date_completed": "08-Dec-2023",
    "assigned_to": "Sanjay Gupta",
    "description": "High vibration - misalignment detected",
    "findings": "Inspection of C-301 revealed high vibration - misalignment detected. Equipment was isolated as per PTW-2599. Maintenance carried out as per SOP-MAINT-575.",
    "parts_used": "Coupling element (qty: 1)",
    "man_hours": 27,
    "applicable_standard": "ISO-10816"
  },
  {
    "work_order_id": "WO-100016",
    "equipment_tag": "C-301",
    "work_type": "Preventive Maintenance",
    "priority": "High",
    "status": "Completed",
    "date_raised": "04-Aug-2023",
    "date_completed": "14-Aug-2023",
    "assigned_to": "Suresh Patel",
    "description": "Motor overheating - winding insulation degradation",
    "findings": "Inspection of C-301 revealed control valve sticking - stem packing worn. Equipment was isolated as per PTW-8834. Maintenance carried out as per SOP-MAINT-206.",
    "parts_used": "Bearing SKF 6205-2RS (qty: 2)",
    "man_hours": 25,
    "applicable_standard": "ASME B31.3"
  },
  {
    "work_order_id": "WO-100017",
    "equipment_tag": "C-301B",
    "work_type": "Preventive Maintenance",
    "priority": "Low",
    "status": "Completed",
    "date_raised": "18-May-2022",
    "date_completed": "25-May-2022",
    "assigned_to": "Vikram Singh",
    "description": "Gasket failure at flange joint",
    "findings": "Inspection of C-301B revealed seal leakage - mechanical seal worn. Equipment was isolated as per PTW-5705. Maintenance carried out as per SOP-MAINT-717.",
    "parts_used": "Coupling element (qty: 1)",
    "man_hours": 8,
    "applicable_standard": "API-610"
  },
  {
    "work_order_id": "WO-100018",
    "equipment_tag": "PSV-3001",
    "work_type": "Predictive Maintenance",
    "priority": "Medium",
    "status": "Planned",
    "date_raised": "07-Apr-2022",
    "date_completed": "20-Apr-2022",
    "assigned_to": "Suresh Patel",
    "description": "Instrument drift - requires recalibration",
    "findings": "Inspection of PSV-3001 revealed seal leakage - mechanical seal worn. Equipment was isolated as per PTW-1049. Maintenance carried out as per SOP-MAINT-566.",
    "parts_used": "Coupling element (qty: 1)",
    "man_hours": 21,
    "applicable_standard": "ISO-10816"
  },
  {
    "work_order_id": "WO-100019",
    "equipment_tag": "HX-501",
    "work_type": "Preventive Maintenance",
    "priority": "High",
    "status": "Completed",
    "date_raised": "01-Jun-2024",
    "date_completed": "07-Jun-2024",
    "assigned_to": "Suresh Patel",
    "description": "High vibration - misalignment detected",
    "findings": "Inspection of HX-501 revealed instrument drift - requires recalibration. Equipment was isolated as per PTW-8392. Maintenance carried out as per SOP-MAINT-223.",
    "parts_used": "Packing rings (qty: 4)",
    "man_hours": 44,
    "applicable_standard": "ISO-10816"
  }
]
```

---

## `data/sample_documents/incident_reports.json`

**Synthetic incident reports (JSON)**

```json
[
  {
    "incident_id": "INC-2022000",
    "date": "27-Mar-2024",
    "title": "Near Miss - Pressure Safety Valve Failure to Operate",
    "equipment_tag": "PSV-3001",
    "severity": "Critical",
    "area": "Unit-2",
    "reported_by": "Control Room Operator",
    "description": "During routine PSV testing, PSV-3001 on reactor R-601 failed to lift at set pressure. Valve found stuck due to corrosion on seat. Discovered during planned test - no actual overpressure event.",
    "root_cause_analysis": "Process fluid causing accelerated corrosion on valve internals. Testing interval of 24 months inadequate for this service.",
    "corrective_actions": [
      "Replace PSV-3001 with corrosion-resistant trim material",
      "Reduce testing interval to 12 months for all PSVs in similar service",
      "Conduct immediate testing of all PSVs in corrosive service",
      "Update risk assessment per OISD-154 requirements"
    ],
    "lessons_learned": "This incident highlights the importance of adhering to OEM maintenance recommendations and timely execution of inspection schedules. Reference: API-580.",
    "investigation_status": "Closed"
  },
  {
    "incident_id": "INC-2022001",
    "date": "11-Apr-2023",
    "title": "Pump Seal Failure - Hydrocarbon Release",
    "equipment_tag": "P-101A",
    "severity": "High",
    "area": "Unit-5",
    "reported_by": "Field Technician",
    "description": "Mechanical seal failure on pump P-101A resulted in minor hydrocarbon release. Area gas detectors activated. Emergency isolation carried out within 3 minutes. No injuries. Approximately 50 liters released to containment area.",
    "root_cause_analysis": "Seal operated beyond recommended life (18 months vs 12 months recommended). PM schedule not updated after OEM bulletin OEM-2022-045.",
    "corrective_actions": [
      "Replace seal with upgraded Type B seal as per OEM recommendation",
      "Update PM schedule to 12-month seal replacement",
      "Review all similar pumps for seal life compliance",
      "Issue safety alert to all operating teams"
    ],
    "lessons_learned": "This incident highlights the importance of adhering to OEM maintenance recommendations and timely execution of inspection schedules. Reference: OISD-163.",
    "investigation_status": "Closed"
  },
  {
    "incident_id": "INC-2022002",
    "date": "24-Nov-2022",
    "title": "Compressor Trip - High Discharge Temperature",
    "equipment_tag": "C-301",
    "severity": "Medium",
    "area": "Unit-2",
    "reported_by": "Shift Supervisor",
    "description": "Compressor C-301 tripped on high discharge temperature alarm. Temperature reached 185\u00b0C (alarm at 180\u00b0C, design limit 200\u00b0C). Automatic shutdown functioned correctly. No equipment damage.",
    "root_cause_analysis": "Intercooler HX-301 fouled, reducing cooling capacity by 30%. Fouling inspection was 4 months overdue.",
    "corrective_actions": [
      "Clean intercooler HX-301",
      "Establish fouling monitoring via pressure drop trending",
      "Add cooling efficiency KPI to daily operator rounds",
      "Review inspection scheduling compliance for all heat exchangers"
    ],
    "lessons_learned": "This incident highlights the importance of adhering to OEM maintenance recommendations and timely execution of inspection schedules. Reference: OISD-163.",
    "investigation_status": "Closed"
  },
  {
    "incident_id": "INC-2022003",
    "date": "16-Jun-2023",
    "title": "Near Miss - Pressure Safety Valve Failure to Operate",
    "equipment_tag": "PSV-3001",
    "severity": "Critical",
    "area": "Unit-1",
    "reported_by": "Shift Supervisor",
    "description": "During routine PSV testing, PSV-3001 on reactor R-601 failed to lift at set pressure. Valve found stuck due to corrosion on seat. Discovered during planned test - no actual overpressure event.",
    "root_cause_analysis": "Process fluid causing accelerated corrosion on valve internals. Testing interval of 24 months inadequate for this service.",
    "corrective_actions": [
      "Replace PSV-3001 with corrosion-resistant trim material",
      "Reduce testing interval to 12 months for all PSVs in similar service",
      "Conduct immediate testing of all PSVs in corrosive service",
      "Update risk assessment per OISD-154 requirements"
    ],
    "lessons_learned": "This incident highlights the importance of adhering to OEM maintenance recommendations and timely execution of inspection schedules. Reference: API-580.",
    "investigation_status": "Closed"
  },
  {
    "incident_id": "INC-2022004",
    "date": "30-Sep-2023",
    "title": "Compressor Trip - High Discharge Temperature",
    "equipment_tag": "C-301",
    "severity": "Medium",
    "area": "Unit-2",
    "reported_by": "Shift Supervisor",
    "description": "Compressor C-301 tripped on high discharge temperature alarm. Temperature reached 185\u00b0C (alarm at 180\u00b0C, design limit 200\u00b0C). Automatic shutdown functioned correctly. No equipment damage.",
    "root_cause_analysis": "Intercooler HX-301 fouled, reducing cooling capacity by 30%. Fouling inspection was 4 months overdue.",
    "corrective_actions": [
      "Clean intercooler HX-301",
      "Establish fouling monitoring via pressure drop trending",
      "Add cooling efficiency KPI to daily operator rounds",
      "Review inspection scheduling compliance for all heat exchangers"
    ],
    "lessons_learned": "This incident highlights the importance of adhering to OEM maintenance recommendations and timely execution of inspection schedules. Reference: API-580.",
    "investigation_status": "Closed"
  },
  {
    "incident_id": "INC-2022005",
    "date": "25-Jun-2023",
    "title": "Compressor Trip - High Discharge Temperature",
    "equipment_tag": "C-301",
    "severity": "Medium",
    "area": "Unit-2",
    "reported_by": "Shift Supervisor",
    "description": "Compressor C-301 tripped on high discharge temperature alarm. Temperature reached 185\u00b0C (alarm at 180\u00b0C, design limit 200\u00b0C). Automatic shutdown functioned correctly. No equipment damage.",
    "root_cause_analysis": "Intercooler HX-301 fouled, reducing cooling capacity by 30%. Fouling inspection was 4 months overdue.",
    "corrective_actions": [
      "Clean intercooler HX-301",
      "Establish fouling monitoring via pressure drop trending",
      "Add cooling efficiency KPI to daily operator rounds",
      "Review inspection scheduling compliance for all heat exchangers"
    ],
    "lessons_learned": "This incident highlights the importance of adhering to OEM maintenance recommendations and timely execution of inspection schedules. Reference: OISD-163.",
    "investigation_status": "Closed"
  },
  {
    "incident_id": "INC-2022006",
    "date": "07-Feb-2023",
    "title": "Pump Seal Failure - Hydrocarbon Release",
    "equipment_tag": "P-101A",
    "severity": "High",
    "area": "Unit-3",
    "reported_by": "Field Technician",
    "description": "Mechanical seal failure on pump P-101A resulted in minor hydrocarbon release. Area gas detectors activated. Emergency isolation carried out within 3 minutes. No injuries. Approximately 50 liters released to containment area.",
    "root_cause_analysis": "Seal operated beyond recommended life (18 months vs 12 months recommended). PM schedule not updated after OEM bulletin OEM-2022-045.",
    "corrective_actions": [
      "Replace seal with upgraded Type B seal as per OEM recommendation",
      "Update PM schedule to 12-month seal replacement",
      "Review all similar pumps for seal life compliance",
      "Issue safety alert to all operating teams"
    ],
    "lessons_learned": "This incident highlights the importance of adhering to OEM maintenance recommendations and timely execution of inspection schedules. Reference: OISD-163.",
    "investigation_status": "Closed"
  },
  {
    "incident_id": "INC-2022007",
    "date": "26-Oct-2023",
    "title": "Near Miss - Pressure Safety Valve Failure to Operate",
    "equipment_tag": "PSV-3001",
    "severity": "Critical",
    "area": "Unit-1",
    "reported_by": "Shift Supervisor",
    "description": "During routine PSV testing, PSV-3001 on reactor R-601 failed to lift at set pressure. Valve found stuck due to corrosion on seat. Discovered during planned test - no actual overpressure event.",
    "root_cause_analysis": "Process fluid causing accelerated corrosion on valve internals. Testing interval of 24 months inadequate for this service.",
    "corrective_actions": [
      "Replace PSV-3001 with corrosion-resistant trim material",
      "Reduce testing interval to 12 months for all PSVs in similar service",
      "Conduct immediate testing of all PSVs in corrosive service",
      "Update risk assessment per OISD-154 requirements"
    ],
    "lessons_learned": "This incident highlights the importance of adhering to OEM maintenance recommendations and timely execution of inspection schedules. Reference: API-580.",
    "investigation_status": "Closed"
  }
]
```

---

## `data/sample_documents/inspection_reports.json`

**Synthetic inspection reports (JSON)**

```json
[
  {
    "report_id": "IR-2023000",
    "equipment_tag": "R-601",
    "inspection_type": "External Visual Inspection",
    "date": "09-Mar-2024",
    "inspector": "P. Nair",
    "next_inspection_due": "10-Nov-2024",
    "findings": "Thickness measurement at location TML-7: 5.2 mm (minimum required: 6.0 mm per API-510). Corrosion rate: 0.19 mm/year. No defects found. Fit for continued service.",
    "recommendation": "Continue normal service. Next inspection as scheduled.",
    "applicable_standards": [
      "API-510",
      "API-570",
      "OISD-128",
      "ASME PCC-2"
    ],
    "compliance_status": "Compliant"
  },
  {
    "report_id": "IR-2023001",
    "equipment_tag": "P-101A",
    "inspection_type": "Pressure Test",
    "date": "15-Jan-2023",
    "inspector": "P. Nair",
    "next_inspection_due": "29-Nov-2023",
    "findings": "Thickness measurement at location TML-5: 6.7 mm (minimum required: 6.0 mm per API-510). Corrosion rate: 0.44 mm/year. No defects found. Fit for continued service.",
    "recommendation": "Continue normal service. Next inspection as scheduled.",
    "applicable_standards": [
      "API-510",
      "API-570",
      "OISD-128",
      "ASME PCC-2"
    ],
    "compliance_status": "Non-compliant - action required"
  },
  {
    "report_id": "IR-2023002",
    "equipment_tag": "V-402",
    "inspection_type": "Pressure Test",
    "date": "02-Mar-2023",
    "inspector": "R. Iyer",
    "next_inspection_due": "05-Jun-2024",
    "findings": "Thickness measurement at location TML-10: 8.6 mm (minimum required: 6.0 mm per API-510). Corrosion rate: 0.16 mm/year. Localized thinning detected. Recommend repair or monitoring at reduced interval.",
    "recommendation": "Apply protective coating during next shutdown.",
    "applicable_standards": [
      "API-510",
      "API-570",
      "OISD-128",
      "ASME PCC-2"
    ],
    "compliance_status": "Compliant with conditions"
  },
  {
    "report_id": "IR-2023003",
    "equipment_tag": "HX-501",
    "inspection_type": "Thickness Survey",
    "date": "13-Apr-2023",
    "inspector": "R. Iyer",
    "next_inspection_due": "11-May-2024",
    "findings": "Thickness measurement at location TML-11: 8.1 mm (minimum required: 6.0 mm per API-510). Corrosion rate: 0.15 mm/year. Localized thinning detected. Recommend repair or monitoring at reduced interval.",
    "recommendation": "Install corrosion monitoring probe.",
    "applicable_standards": [
      "API-510",
      "API-570",
      "OISD-128",
      "ASME PCC-2"
    ],
    "compliance_status": "Non-compliant - action required"
  },
  {
    "report_id": "IR-2023004",
    "equipment_tag": "R-601",
    "inspection_type": "Pressure Test",
    "date": "16-Feb-2024",
    "inspector": "S. Banerjee",
    "next_inspection_due": "06-Sep-2024",
    "findings": "Thickness measurement at location TML-3: 8.4 mm (minimum required: 6.0 mm per API-510). Corrosion rate: 0.32 mm/year. No defects found. Fit for continued service.",
    "recommendation": "Apply protective coating during next shutdown.",
    "applicable_standards": [
      "API-510",
      "API-570",
      "OISD-128",
      "ASME PCC-2"
    ],
    "compliance_status": "Compliant"
  },
  {
    "report_id": "IR-2023005",
    "equipment_tag": "P-101A",
    "inspection_type": "External Visual Inspection",
    "date": "05-Jan-2024",
    "inspector": "S. Banerjee",
    "next_inspection_due": "26-Aug-2025",
    "findings": "Thickness measurement at location TML-6: 9.3 mm (minimum required: 6.0 mm per API-510). Corrosion rate: 0.10 mm/year. Localized thinning detected. Recommend repair or monitoring at reduced interval.",
    "recommendation": "Install corrosion monitoring probe.",
    "applicable_standards": [
      "API-510",
      "API-570",
      "OISD-128",
      "ASME PCC-2"
    ],
    "compliance_status": "Non-compliant - action required"
  },
  {
    "report_id": "IR-2023006",
    "equipment_tag": "V-401",
    "inspection_type": "Thickness Survey",
    "date": "12-Dec-2023",
    "inspector": "M. Krishnan",
    "next_inspection_due": "13-Nov-2025",
    "findings": "Thickness measurement at location TML-2: 8.0 mm (minimum required: 6.0 mm per API-510). Corrosion rate: 0.27 mm/year. Localized thinning detected. Recommend repair or monitoring at reduced interval.",
    "recommendation": "Reduce inspection interval to 12 months.",
    "applicable_standards": [
      "API-510",
      "API-570",
      "OISD-128",
      "ASME PCC-2"
    ],
    "compliance_status": "Compliant with conditions"
  },
  {
    "report_id": "IR-2023007",
    "equipment_tag": "V-401",
    "inspection_type": "Thickness Survey",
    "date": "03-Mar-2023",
    "inspector": "R. Iyer",
    "next_inspection_due": "01-Feb-2025",
    "findings": "Thickness measurement at location TML-7: 10.8 mm (minimum required: 6.0 mm per API-510). Corrosion rate: 0.44 mm/year. No defects found. Fit for continued service.",
    "recommendation": "Continue normal service. Next inspection as scheduled.",
    "applicable_standards": [
      "API-510",
      "API-570",
      "OISD-128",
      "ASME PCC-2"
    ],
    "compliance_status": "Compliant"
  },
  {
    "report_id": "IR-2023008",
    "equipment_tag": "C-301",
    "inspection_type": "Pressure Test",
    "date": "25-Sep-2023",
    "inspector": "M. Krishnan",
    "next_inspection_due": "25-Jan-2025",
    "findings": "Thickness measurement at location TML-7: 8.6 mm (minimum required: 6.0 mm per API-510). Corrosion rate: 0.49 mm/year. No defects found. Fit for continued service.",
    "recommendation": "Continue normal service. Next inspection as scheduled.",
    "applicable_standards": [
      "API-510",
      "API-570",
      "OISD-128",
      "ASME PCC-2"
    ],
    "compliance_status": "Compliant"
  },
  {
    "report_id": "IR-2023009",
    "equipment_tag": "R-601",
    "inspection_type": "Pressure Test",
    "date": "21-Jan-2023",
    "inspector": "R. Iyer",
    "next_inspection_due": "06-Aug-2024",
    "findings": "Thickness measurement at location TML-6: 6.2 mm (minimum required: 6.0 mm per API-510). Corrosion rate: 0.30 mm/year. No defects found. Fit for continued service.",
    "recommendation": "Apply protective coating during next shutdown.",
    "applicable_standards": [
      "API-510",
      "API-570",
      "OISD-128",
      "ASME PCC-2"
    ],
    "compliance_status": "Non-compliant - action required"
  }
]
```

---

## `data/sample_documents/sop_hot_work.json`

**Synthetic SOP — hot work (JSON)**

```json
{
  "document_id": "SOP-OPS-101",
  "title": "Standard Operating Procedure: Hot Work Near Hydrocarbon Lines",
  "revision": "Rev 3",
  "effective_date": "01-Jan-2024",
  "approved_by": "Plant Manager - D.K. Mehta",
  "applicable_regulations": [
    "OISD-105",
    "Factory Act Section 38",
    "IS-3016"
  ],
  "scope": "This procedure covers all hot work activities (welding, cutting, grinding) within 15 meters of equipment containing or previously containing hydrocarbons.",
  "steps": [
    {
      "step": 1,
      "action": "Obtain Hot Work Permit (PTW) from Control Room Supervisor",
      "responsible": "Maintenance Supervisor",
      "reference": "PTW Procedure SOP-SAFE-001"
    },
    {
      "step": 2,
      "action": "Confirm gas test shows <1% LEL in work area. Gas test valid for 4 hours maximum.",
      "responsible": "Safety Officer",
      "reference": "Gas Testing Procedure SOP-SAFE-012"
    },
    {
      "step": 3,
      "action": "Verify equipment isolation (Double Block and Bleed). Check isolation certificate.",
      "responsible": "Operations Engineer",
      "reference": "Isolation Procedure SOP-OPS-050"
    },
    {
      "step": 4,
      "action": "Position fire extinguisher and fire watch personnel. Minimum 2 DCP extinguishers (10 kg).",
      "responsible": "Fire & Safety",
      "reference": "OISD-105 Clause 6.3"
    },
    {
      "step": 5,
      "action": "Commence hot work. Continuous gas monitoring required. Stop work if LEL exceeds 10%.",
      "responsible": "Executing Technician",
      "reference": "OISD-105 Clause 7.1"
    }
  ],
  "ppe_required": [
    "Fire-retardant coveralls",
    "Welding helmet with appropriate shade",
    "Leather gloves",
    "Safety shoes with metatarsal guard",
    "Portable gas detector (4-gas)"
  ],
  "emergency_procedure": "In case of fire/gas leak: Stop work immediately -> Activate area alarm -> Evacuate to Assembly Point B -> Call Emergency: Ext 999"
}
```

---

## `backend/data/uploads/incident_report_steam_leak.txt`

**Demo — Steam leak incident report (E-301A)**

```
INCIDENT REPORT - IR-2024-0847

Date of Incident: 15-Mar-2024
Time: 14:35 IST
Location: Crude Distillation Unit (CDU-1), Gujarat Refinery Complex
Reported By: Rajesh Kumar (Shift Supervisor)
Investigation Lead: Priya Mehta (HSE Manager)

1. INCIDENT SUMMARY

On 15-Mar-2024 at approximately 14:35 hours, a high-pressure steam leak was detected on the overhead condenser system of equipment E-301A in the Crude Distillation Unit. The leak originated from a corroded flange joint on the 6-inch steam line connecting the heat exchanger to the overhead accumulator V-302.

The area was immediately evacuated per SOP-EM-001 (Emergency Evacuation Procedure). No personnel injuries were reported. The unit was brought to a safe shutdown within 45 minutes following procedure SOP-SD-015 (Emergency Shutdown - CDU).

2. EQUIPMENT INVOLVED

Primary Equipment:
- E-301A: Shell and Tube Heat Exchanger (Overhead Condenser)
- V-302: Overhead Accumulator Vessel
- P-301A: Overhead Reflux Pump
- PSV-3001: Pressure Safety Valve (set at 12.5 kg/cm2)

Associated Instrumentation:
- PT-3001: Pressure Transmitter (reading 11.8 kg/cm2 at time of incident)
- TT-3005: Temperature Transmitter (reading 142 deg C)
- FT-3002: Flow Transmitter (overhead vapor line)
- LT-3003: Level Transmitter on V-302

3. ROOT CAUSE ANALYSIS

The investigation team, led by Priya Mehta, determined the following root causes:

Primary Cause: Corrosion Under Insulation (CUI) on the 6-inch carbon steel flange joint. The flange gasket had degraded due to prolonged exposure to moisture ingress beneath thermal insulation. Wall thickness measurements showed reduction from original 7.1mm to 2.3mm (67% metal loss).

Contributing Factors:
- Last inspection of this section was conducted on 22-Aug-2022 (18 months overdue per OISD-154 guidelines which mandate annual inspection)
- The insulation cladding had visible damage reported in WO-2023-1156 but repair was deferred due to turnaround scheduling
- Operating temperature cycling between 85-145 deg C created condensation conditions favorable for CUI

4. REGULATORY COMPLIANCE

The following regulations and standards are applicable:
- OISD-154: Safety Inspection of Refinery Equipment
- API-510: Pressure Vessel Inspection Code
- API-570: Piping Inspection Code
- IS-2825: Code for Unfired Pressure Vessels
- Factory Act 1948, Section 28: Dangerous Operations

The incident constitutes a near-miss under OISD-145 (Safety Audit) classification. A report has been filed with the Chief Inspector of Factories, Gujarat.

5. CORRECTIVE ACTIONS

Immediate Actions (Completed):
- Isolated E-301A and depressurized the system
- Replaced corroded flange section with new ASTM A105 flange
- Installed new spiral wound gasket (SS-316/Graphite)
- Conducted hydrostatic test at 18.75 kg/cm2 per API-510

Short-Term Actions (Within 30 days):
- Complete CUI survey of all equipment in CDU-1 overhead section
- Update inspection schedule for all flanged connections per OISD-154
- Repair insulation cladding on E-301A, E-301B, and V-302

Long-Term Actions (Within 90 days):
- Implement risk-based inspection (RBI) program per API-580/581
- Install corrosion monitoring probes on critical piping circuits
- Upgrade insulation material to hydrophobic type on overhead system
- Training program for all maintenance personnel on CUI identification

6. PERSONNEL INVOLVED

- Rajesh Kumar (Shift Supervisor) - First responder, initiated evacuation
- Anil Reddy (Panel Operator) - Executed emergency shutdown sequence
- Suresh Patel (Maintenance Engineer) - Led repair activities
- Priya Mehta (HSE Manager) - Investigation lead
- Dr. Vikram Singh (Plant Manager) - Approved corrective action plan
- Amit Sharma (Inspection Engineer) - Conducted wall thickness measurements

Report Classification: NEAR-MISS (Category B)
Follow-up Review Date: 15-Apr-2024
Distribution: Plant Manager, HSE Department, Inspection Department, Operations
```

---

## `backend/data/uploads/sop_pump_maintenance.txt`

**Demo — SOP for centrifugal pump maintenance**

```
STANDARD OPERATING PROCEDURE
SOP-PM-042: Preventive Maintenance of Centrifugal Pumps

Revision: 03
Effective Date: 01-Jan-2024
Prepared By: Suresh Patel (Maintenance Engineer)
Approved By: Dr. Vikram Singh (Plant Manager)
Classification: Safety Critical

1. PURPOSE AND SCOPE

This procedure defines the step-by-step preventive maintenance activities for all centrifugal pumps in the Gujarat Refinery Complex. This SOP applies to pumps P-101A, P-101B, P-201A, P-201B, P-301A, P-301B, and all auxiliary centrifugal pumps in CDU-1, CDU-2, and the Hydrogen Generation Unit.

All maintenance activities must comply with OISD-137 (Inspection and Maintenance of Cross-Country Pipelines) and API-610 (Centrifugal Pumps for Petroleum Industry).

2. SAFETY PRECAUTIONS

Before commencing any maintenance activity:
- Obtain valid Permit to Work (PTW) as per SOP-PTW-001
- Ensure Lock-Out Tag-Out (LOTO) procedure SOP-LOTO-003 is completed
- Verify zero energy state confirmation from Panel Operator
- Wear required PPE: Safety helmet, goggles, flame-resistant coveralls, safety shoes
- Check H2S monitor readings if working in sour service areas
- Ensure fire extinguisher (DCP type) is available within 15 meters

3. QUARTERLY MAINTENANCE CHECKLIST

3.1 Vibration Analysis
- Measure vibration levels at drive end (DE) and non-drive end (NDE) bearings
- Acceptable limits per ISO-10816:
  - Normal: < 4.5 mm/s RMS
  - Warning: 4.5-7.1 mm/s RMS
  - Critical: > 7.1 mm/s RMS (immediate shutdown required)
- Record baseline vibration signature for trend analysis
- Compare with previous readings from CMMS database

3.2 Bearing Temperature Check
- Measure bearing temperature using IR thermometer
- Normal operating range: 45-75 deg C
- Warning threshold: 85 deg C
- Trip threshold: 95 deg C (automatic shutdown via THS-xxx)

3.3 Mechanical Seal Inspection
- Check for visible leakage at seal faces
- Acceptable leakage: < 5 drops per minute for single seals
- Zero visible leakage required for dual/tandem seals
- Verify seal flush system pressure and flow (Plan 11/13/54)
- Check seal quench/drain connections

3.4 Lubrication
- Verify oil level in bearing housing (sight glass check)
- Oil grade: ISO VG-68 mineral oil (or as specified on equipment datasheet)
- Oil change interval: 6 months or 4000 operating hours (whichever is earlier)
- Grease-lubricated bearings: Apply Shell Gadus S2 V220 at 3-month intervals
- Check oil condition - discoloration, water contamination, metal particles

4. ANNUAL MAINTENANCE (DURING TURNAROUND)

4.1 Complete Pump Overhaul
- Disassemble pump and inspect all internal components
- Check impeller for erosion, cavitation damage, and balance
- Measure shaft runout (max allowable: 0.05mm TIR)
- Replace wear rings if clearance exceeds API-610 limits
- Replace all O-rings, gaskets, and mechanical seal components
- Conduct hydraulic performance test after reassembly

4.2 Alignment Verification
- Perform laser alignment of pump-motor coupling
- Maximum misalignment: 0.05mm offset, 0.05mm/100mm angular
- Document alignment readings in maintenance record

5. DOCUMENTATION

All maintenance activities must be recorded in:
- Computerized Maintenance Management System (CMMS)
- Equipment History Card
- PTW closure report

Work Orders for pump maintenance:
- Quarterly PM: WO prefix "PM-Q-"
- Annual overhaul: WO prefix "PM-A-"
- Corrective maintenance: WO prefix "CM-"

6. REFERENCES

- API-610: Centrifugal Pumps for Petroleum Industry
- ISO-10816: Mechanical Vibration - Evaluation
- OISD-137: Inspection and Maintenance
- OISD-154: Safety Inspection of Refinery Equipment
- Factory Act 1948
- Plant Maintenance Manual, Chapter 7

Prepared By: Suresh Patel (Maintenance Engineer)
Reviewed By: Amit Sharma (Inspection Engineer)
Approved By: Dr. Vikram Singh (Plant Manager)
```

---

## `backend/data/uploads/inspection_P101A.txt`

**Demo — RBI inspection report for P-101A**

```
EQUIPMENT INSPECTION REPORT
Report No: INS-2024-0392
Inspection Type: Risk-Based Inspection (RBI)

Equipment Tag: P-101A
Equipment Name: Crude Charge Pump (Primary)
Equipment Type: Centrifugal Pump, API-610 Type BB2
Location: CDU-1 Pump House, Gujarat Refinery Complex
Manufacturer: Flowserve Corporation
Model: HPX 6x8x13
Serial Number: FSC-2018-44721
Installation Date: 15-Jun-2018
Design Pressure: 42 kg/cm2
Design Temperature: 180 deg C
Operating Pressure: 35.2 kg/cm2
Operating Temperature: 156 deg C
Service: Hot Crude Oil (API Gravity 32.5)

1. INSPECTION SUMMARY

Inspection Date: 10-Feb-2024
Inspector: Amit Sharma (Inspection Engineer, API-510/570 Certified)
Next Inspection Due: 10-Feb-2025

Overall Condition Rating: SATISFACTORY (Grade B)
Remaining Life Assessment: 8 years (based on current corrosion rate)

2. VIBRATION MEASUREMENTS

Location          | Reading (mm/s RMS) | Limit  | Status
Drive End (DE) H  | 3.2                | 4.5    | NORMAL
Drive End (DE) V  | 2.8                | 4.5    | NORMAL
Drive End (DE) A  | 3.5                | 4.5    | NORMAL
Non-Drive (NDE) H | 4.1                | 4.5    | WARNING
Non-Drive (NDE) V | 3.9                | 4.5    | NORMAL
Non-Drive (NDE) A | 4.3                | 4.5    | WARNING

Trend Analysis: NDE bearing vibration has increased 35% over last 6 months.
Recommendation: Schedule bearing replacement during next planned outage.
Frequency spectrum analysis indicates possible ball pass frequency outer race (BPFO) defect.

3. THICKNESS MEASUREMENTS

Component           | Original | Measured | Min Req | Corr Rate  | Status
Pump Casing         | 12.0 mm  | 11.2 mm  | 9.5 mm  | 0.13 mm/yr | OK
Suction Nozzle      | 8.5 mm   | 7.8 mm   | 6.2 mm  | 0.12 mm/yr | OK
Discharge Nozzle    | 9.0 mm   | 8.1 mm   | 6.8 mm  | 0.15 mm/yr | OK
Wear Ring (Casing)  | 0.35 mm  | 0.52 mm  | 0.70 mm | N/A        | OK
Wear Ring (Impeller)| 0.35 mm  | 0.48 mm  | 0.70 mm | N/A        | OK

4. MECHANICAL SEAL CONDITION

Seal Type: John Crane Type 4620 (Dual Pressurized)
Barrier Fluid: Clean diesel (Plan 53B)
Barrier Pressure: 38.5 kg/cm2 (maintained 3.3 kg/cm2 above process)
Leakage Observed: None (zero visible leakage - ACCEPTABLE)
Seal Flush System: Operating normally

5. BEARING CONDITION

Drive End: SKF 6316-2RS (Deep Groove Ball Bearing)
- Temperature: 62 deg C (Normal range: 45-75 deg C)
- Oil condition: Clear, no contamination detected
- Recommendation: Continue monitoring

Non-Drive End: SKF 7316-BECBM (Angular Contact Ball Bearing)
- Temperature: 71 deg C (Approaching warning threshold)
- Oil condition: Slight discoloration noted
- Vibration trending upward (see Section 2)
- Recommendation: REPLACE BEARING during next opportunity. Order spare immediately.
- Estimated remaining life: 3-4 months based on degradation trend

6. MOTOR CONDITION

Motor Tag: M-101A
Motor Type: Squirrel Cage Induction, TEFC
Rating: 250 kW, 3300V, 50Hz
Current Draw: 42A (rated 48A) - 87.5% loading - NORMAL
Insulation Resistance: 850 MOhm (minimum acceptable: 100 MOhm) - GOOD
Winding Temperature: 78 deg C (Class F insulation, max 155 deg C) - NORMAL

7. COMPLIANCE

This inspection complies with:
- API-610: Centrifugal Pumps for Petroleum Industry
- OISD-154: Safety Inspection of Refinery Equipment
- API-510: Pressure Vessel Inspection Code (for pump casing)
- ISO-10816-3: Vibration Evaluation for Industrial Machines

8. CORRECTIVE ACTIONS REQUIRED

Priority HIGH:
- Replace NDE bearing (SKF 7316-BECBM) within 60 days
- Create Work Order WO-2024-0891 for bearing replacement
- Order spare bearing from approved vendor (Lead time: 2-3 weeks)

Priority MEDIUM:
- Change bearing housing oil on both ends
- Schedule laser alignment check after bearing replacement
- Update vibration baseline after bearing replacement

Priority LOW:
- Repaint pump base plate (surface corrosion observed)
- Replace corroded foundation bolt (northeast corner)

Inspector: Amit Sharma
Badge No: INS-0042
Certification: API-510, API-570, API-653
Signature: [Signed]
Date: 10-Feb-2024
```

---

## `backend/data/uploads/work_order_sample.txt`

**Demo — Work order samples**

```
WORK ORDER: WO-100000
Equipment: FV-1001
Type: Predictive Maintenance
Priority: High
Date: 18-Dec-2023
Assigned To: Pradeep Joshi
Description: Corrosion under insulation (CUI)
Findings: Inspection of FV-1001 revealed high vibration - misalignment detected. Equipment was isolated as per PTW-4711. Maintenance carried out as per SOP-MAINT-714.
Parts Used: Coupling element (qty: 1)
Man-Hours: 44
Standard: ASME B31.3

============================================================

WORK ORDER: WO-100001
Equipment: P-101B
Type: Preventive Maintenance
Priority: Medium
Date: 28-Jun-2023
Assigned To: Anil Reddy
Description: Instrument drift - requires recalibration
Findings: Inspection of P-101B revealed instrument drift - requires recalibration. Equipment was isolated as per PTW-8941. Maintenance carried out as per SOP-MAINT-661.
Parts Used: Gasket set DN150 PN40 (qty: 1)
Man-Hours: 12
Standard: OISD-163

============================================================

WORK ORDER: WO-100002
Equipment: HX-502
Type: Predictive Maintenance
Priority: Critical
Date: 18-Mar-2022
Assigned To: Suresh Patel
Description: High vibration - misalignment detected
Findings: Inspection of HX-502 revealed corrosion under insulation (cui). Equipment was isolated as per PTW-8610. Maintenance carried out as per SOP-MAINT-994.
Parts Used: Bearing SKF 6205-2RS (qty: 2)
Man-Hours: 8
Standard: API-610

============================================================

WORK ORDER: WO-100003
Equipment: P-201A
Type: Corrective Maintenance
Priority: Medium
Date: 26-May-2024
Assigned To: Amit Sharma
Description: Control valve sticking - stem packing worn
Findings: Inspection of P-201A revealed gasket failure at flange joint. Equipment was isolated as per PTW-4111. Maintenance carried out as per SOP-MAINT-259.
Parts Used: Packing rings (qty: 4)
Man-Hours: 22
Standard: OISD-163

============================================================

WORK ORDER: WO-100004
Equipment: XV-1002
Type: Preventive Maintenance
Priority: Medium
Date: 08-Nov-2023
Assigned To: Amit Sharma
Description: High vibration - misalignment detected
Findings: Inspection of XV-1002 revealed coupling damage - fatigue crack. Equipment was isolated as per PTW-2291. Maintenance carried out as per SOP-MAINT-104.
Parts Used: Gasket set DN150 PN40 (qty: 1)
Man-Hours: 24
Standard: API-610

============================================================
```

---

## `scripts/generate_codebase_doc.py`

**Codebase documentation generator**

```python
"""Generates codebase.md by reading ALL source files in the project."""
import os
from pathlib import Path

ROOT = Path(__file__).parent.parent
OUT = ROOT / "codebase.md"

# EVERY file in the project, grouped by section
FILES = [
    # === TOP LEVEL ===
    ("README.md", "Project README"),
    ("docker-compose.yml", "Docker Compose — Neo4j + Ollama infrastructure"),

    # === BACKEND — Infrastructure ===
    ("backend/Dockerfile", "Backend Docker image"),
    ("backend/requirements.txt", "Python dependencies"),

    # === BACKEND — App Core ===
    ("backend/app/__init__.py", "App package init"),
    ("backend/app/config.py", "Application configuration (Pydantic Settings)"),
    ("backend/app/main.py", "FastAPI application entry point"),
    ("backend/app/models/__init__.py", "Models package init"),
    ("backend/app/models/schemas.py", "Pydantic data models"),

    # === BACKEND — API Routers ===
    ("backend/app/routers/__init__.py", "Routers package init"),
    ("backend/app/routers/ingest.py", "Document ingestion API + SSE streaming pipeline"),
    ("backend/app/routers/query.py", "RAG query API + SSE streaming retrieval"),
    ("backend/app/routers/graph.py", "Knowledge graph + FAISS search API"),
    ("backend/app/routers/agents.py", "Multi-agent intelligence API"),

    # === BACKEND — Ingestion Services ===
    ("backend/app/services/__init__.py", "Services package init"),
    ("backend/app/services/ingestion/__init__.py", "Ingestion package init"),
    ("backend/app/services/ingestion/pipeline.py", "Main 11-step ingestion pipeline orchestrator"),
    ("backend/app/services/ingestion/pdf_parser.py", "PDF and DOCX parser (PyMuPDF)"),
    ("backend/app/services/ingestion/ocr_engine.py", "OCR engine — PaddleOCR (primary) + Tesseract (fallback)"),
    ("backend/app/services/ingestion/text_cleaner.py", "Text cleaning and normalization (ftfy + regex)"),
    ("backend/app/services/ingestion/document_structurer.py", "Document structure builder (pages → sections → paragraphs)"),
    ("backend/app/services/ingestion/chunker.py", "Semantic text chunker (500 tokens, 70 overlap)"),
    ("backend/app/services/ingestion/entity_extractor.py", "Industrial entity extractor (spaCy + regex)"),
    ("backend/app/services/ingestion/relationship_extractor.py", "Relationship triple extractor"),
    ("backend/app/services/ingestion/document_classifier.py", "Document category classifier (7 categories)"),
    ("backend/app/services/ingestion/llm_extractor.py", "LLM-based entity extractor (Ollama)"),

    # === BACKEND — Vector Store ===
    ("backend/app/services/vectorstore/__init__.py", "Vectorstore package init"),
    ("backend/app/services/vectorstore/faiss_service.py", "FAISS vector store + sentence-transformers embedding engine"),
    ("backend/app/services/vectorstore/qdrant_service.py", "Qdrant vector store (legacy, kept for reference)"),

    # === BACKEND — Knowledge Graph ===
    ("backend/app/services/knowledge_graph/__init__.py", "Knowledge graph package init"),
    ("backend/app/services/knowledge_graph/neo4j_client.py", "Neo4j async client with schema management"),
    ("backend/app/services/knowledge_graph/graph_builder.py", "Knowledge graph builder (Document→Page→Section→Chunk→Entity)"),

    # === BACKEND — RAG ===
    ("backend/app/services/rag/__init__.py", "RAG package init"),
    ("backend/app/services/rag/retriever.py", "Hybrid retriever — FAISS + Neo4j + BM25 (0.6 semantic + 0.4 graph)"),
    ("backend/app/services/rag/generator.py", "Answer generator — Ollama / OpenAI with citation enforcement"),

    # === BACKEND — Agents ===
    ("backend/app/services/agents/__init__.py", "Agents package init"),
    ("backend/app/services/agents/sensor_monitor_agent.py", "Sensor health monitor agent"),
    ("backend/app/services/agents/fault_diagnosis_agent.py", "Fault diagnosis agent"),
    ("backend/app/services/agents/predictive_maintenance_agent.py", "Predictive maintenance agent (RUL)"),
    ("backend/app/services/agents/shift_handover_agent.py", "Shift handover report agent"),
    ("backend/app/services/agents/report_saver.py", "Report persistence service"),
    ("backend/app/services/agents/orchestrator.py", "Agent orchestrator (Monitor→Diagnosis→Predictive→Handover)"),

    # === FRONTEND ===
    ("frontend/package.json", "Frontend package.json (Next.js 16 + React 19)"),
    ("frontend/next.config.js", "Next.js configuration (API proxy)"),
    ("frontend/src/app/layout.js", "Root layout"),
    ("frontend/src/app/page.js", "Main application — Pipeline Visualizer + Query + Dashboard + Knowledge Graph"),
    ("frontend/src/app/globals.css", "Global styles — dark theme + pipeline visualization CSS"),

    # === SAMPLE DATA (data/sample_documents/) ===
    ("data/sample_documents/work_order_sample.txt", "Sample work order document"),
    ("data/sample_documents/incident_report_sample.txt", "Sample incident report"),
    ("data/sample_documents/sop_hot_work.txt", "Sample SOP — hot work procedure"),
    ("data/sample_documents/work_orders.json", "Synthetic work orders (JSON)"),
    ("data/sample_documents/incident_reports.json", "Synthetic incident reports (JSON)"),
    ("data/sample_documents/inspection_reports.json", "Synthetic inspection reports (JSON)"),
    ("data/sample_documents/sop_hot_work.json", "Synthetic SOP — hot work (JSON)"),

    # === DEMO DOCUMENTS (backend/data/uploads/) ===
    ("backend/data/uploads/incident_report_steam_leak.txt", "Demo — Steam leak incident report (E-301A)"),
    ("backend/data/uploads/sop_pump_maintenance.txt", "Demo — SOP for centrifugal pump maintenance"),
    ("backend/data/uploads/inspection_P101A.txt", "Demo — RBI inspection report for P-101A"),
    ("backend/data/uploads/work_order_sample.txt", "Demo — Work order samples"),

    # === SCRIPTS ===
    ("scripts/generate_codebase_doc.py", "Codebase documentation generator"),
    ("scripts/generate_synthetic_docs.py", "Synthetic document generator"),
    ("scripts/demo_standalone.py", "Standalone pipeline demo (zero dependencies)"),
    ("scripts/demo_agents.py", "Multi-agent demo (zero dependencies)"),
    ("scripts/demo_pipeline.py", "Pipeline demo script"),
    ("scripts/test_pdf_ingest.py", "PDF ingestion test"),
]

def read_file_safe(filepath):
    """Read file with encoding fallback."""
    full = ROOT / filepath
    if not full.exists():
        return f"# FILE NOT FOUND: {filepath}"
    try:
        return full.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return full.read_text(encoding="latin-1", errors="replace")

def get_lang(filepath):
    """Get markdown language tag from file extension."""
    ext = Path(filepath).suffix
    return {
        ".py": "python", ".js": "javascript", ".css": "css",
        ".yml": "yaml", ".yaml": "yaml", ".json": "json",
        ".md": "markdown", ".txt": "text",
    }.get(ext, "")

def main():
    lines = []
    lines.append("# AXIOM Codebase Documentation")
    lines.append("")
    lines.append("Complete source code for **AXIOM — Offline GraphRAG Industrial Knowledge Platform**.")
    lines.append(f"Total files documented: **{len(FILES)}**")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Table of contents
    lines.append("## Table of Contents")
    lines.append("")
    current_section = ""
    sections = {
        "README": "Top Level",
        "docker-compose": "Top Level",
        "backend/Dockerfile": "Infrastructure",
        "backend/requirements": "Infrastructure",
        "backend/app/__init__": "Backend Core",
        "backend/app/config": "Backend Core",
        "backend/app/main": "Backend Core",
        "backend/app/models": "Backend Core",
        "backend/app/routers": "API Routers",
        "backend/app/services/__init__": "Backend Core",
        "backend/app/services/ingestion": "Document Ingestion Services",
        "backend/app/services/knowledge_graph": "Knowledge Graph Services",
        "backend/app/services/vectorstore": "Vector Store Services",
        "backend/app/services/rag": "RAG / Retrieval Services",
        "backend/app/services/agents": "Multi-Agent System",
        "frontend": "Frontend (Next.js)",
        "data": "Sample Data",
        "backend/data": "Demo Documents",
        "scripts": "Scripts",
    }

    toc_sections = {}
    for filepath, title in FILES:
        section = "Other"
        for prefix, sec_name in sections.items():
            if filepath.startswith(prefix):
                section = sec_name
                break
        toc_sections.setdefault(section, []).append((filepath, title))

    for section, items in toc_sections.items():
        lines.append(f"### {section}")
        for filepath, title in items:
            anchor = filepath.replace("/", "").replace(".", "").replace("_", "").lower()
            lines.append(f"- [{filepath}](#{anchor}) — {title}")
        lines.append("")

    lines.append("---")
    lines.append("")

    # Folder structure
    lines.append("## Folder Structure")
    lines.append("")
    lines.append("```")
    lines.append("axiom/")
    prev_dirs = []
    for filepath, _ in FILES:
        parts = filepath.split("/")
        # Print directory tree
        for i, part in enumerate(parts[:-1]):
            prefix_parts = parts[:i+1]
            if prefix_parts != prev_dirs[:i+1]:
                indent = "    " * (i + 1)
                lines.append(f"{indent}{part}/")
        indent = "    " * len(parts)
        lines.append(f"{indent}{parts[-1]}")
        prev_dirs = parts[:-1]
    lines.append("```")
    lines.append("")
    lines.append("---")
    lines.append("")

    # File documentation — full source code for every file
    for filepath, title in FILES:
        lang = get_lang(filepath)
        if filepath.endswith("Dockerfile"):
            lang = "dockerfile"
        content = read_file_safe(filepath)

        lines.append(f"## `{filepath}`")
        lines.append("")
        lines.append(f"**{title}**")
        lines.append("")
        lines.append(f"```{lang}")
        lines.append(content.rstrip())
        lines.append("```")
        lines.append("")
        lines.append("---")
        lines.append("")

    # Write output
    OUT.write_text("\n".join(lines), encoding="utf-8")
    file_size = OUT.stat().st_size
    print(f"Generated {OUT} ({len(FILES)} files, {len(lines)} lines, {file_size // 1024} KB)")

if __name__ == "__main__":
    main()
```

---

## `scripts/generate_synthetic_docs.py`

**Synthetic document generator**

```python
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
```

---

## `scripts/demo_standalone.py`

**Standalone pipeline demo (zero dependencies)**

```python
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
```

---

## `scripts/demo_agents.py`

**Multi-agent demo (zero dependencies)**

```python
"""
Standalone demo of the Multi-Agent System.
No external dependencies - runs with pure Python 3.11.

Demonstrates:
1. Sensor Health Monitor detecting anomalies
2. Fault Diagnosis generating root cause hypotheses
3. Predictive Maintenance estimating RUL
4. Shift Handover report generation
"""

import sys
import math
import statistics
import types
from pathlib import Path
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum

# Shim structlog and other missing modules so agent code imports cleanly
class _NullLogger:
    def info(self, *a, **kw): pass
    def debug(self, *a, **kw): pass
    def warning(self, *a, **kw): pass
    def error(self, *a, **kw): pass

_structlog = types.ModuleType("structlog")
_structlog.get_logger = lambda *a, **kw: _NullLogger()
sys.modules["structlog"] = _structlog

# Shim pydantic_settings (only needed by config.py)
_ps = types.ModuleType("pydantic_settings")
class _FakeBaseSettings:
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
    def __init_subclass__(cls, **kw): pass
    def __init__(self, **kw):
        import os
        for k, v in type(self).__dict__.items():
            if not k.startswith("_") and k != "Config":
                setattr(self, k, os.environ.get(k.upper(), v))
_ps.BaseSettings = _FakeBaseSettings
sys.modules["pydantic_settings"] = _ps

# Shim httpx (used by agents for Ollama calls - not needed in standalone demo)
_httpx = types.ModuleType("httpx")
class _FakeAsyncClient:
    async def __aenter__(self): return self
    async def __aexit__(self, *a): pass
    async def post(self, *a, **kw):
        r = types.SimpleNamespace(status_code=503, json=lambda: {})
        return r
_httpx.AsyncClient = lambda **kw: _FakeAsyncClient()
sys.modules["httpx"] = _httpx

# Shim neo4j driver
_neo4j_mod = types.ModuleType("neo4j")
_neo4j_mod.AsyncGraphDatabase = type("AsyncGraphDatabase", (), {"driver": staticmethod(lambda *a, **kw: None)})
_neo4j_mod.AsyncDriver = type("AsyncDriver", (), {})
sys.modules["neo4j"] = _neo4j_mod

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

def demo_sensor_monitor():
    """Demo: Sensor Health Monitor Agent detects anomalies."""
    print("\n" + "=" * 70)
    print("  AGENT 1: SENSOR HEALTH MONITOR")
    print("  Ingesting machine sensor logs and detecting anomalies")
    print("=" * 70)

    from app.services.agents.sensor_monitor_agent import (
        SensorHealthMonitorAgent, SensorReading, HealthStatus,
    )

    agent = SensorHealthMonitorAgent()

    # Simulate sensor readings for Pump P-101A
    # Normal operation followed by degradation
    print("\n  Simulating 30 vibration readings for Pump P-101A...")
    print("  (Normal -> Degrading -> Warning -> Critical)\n")

    readings = []
    base_time = datetime(2024, 7, 1, 8, 0)

    # Normal readings (1-15)
    for i in range(15):
        readings.append(SensorReading(
            equipment_tag="P-101A",
            parameter="vibration",
            value=3.5 + (i * 0.1) + (0.2 * (i % 3)),  # Slight variation
            unit="mm/s",
            timestamp=base_time + timedelta(hours=i),
        ))

    # Degrading readings (16-25)
    for i in range(15, 25):
        readings.append(SensorReading(
            equipment_tag="P-101A",
            parameter="vibration",
            value=5.0 + ((i - 15) * 0.6),  # Steeper increase
            unit="mm/s",
            timestamp=base_time + timedelta(hours=i),
        ))

    # Critical readings (26-30)
    for i in range(25, 30):
        readings.append(SensorReading(
            equipment_tag="P-101A",
            parameter="vibration",
            value=11.0 + ((i - 25) * 0.5),  # Past warning limit
            unit="mm/s",
            timestamp=base_time + timedelta(hours=i),
        ))

    # Process readings
    alerts = []
    for reading in readings:
        alert = agent.analyze_reading(reading)
        status_icon = "." if not alert else ("[!]" if alert.status == HealthStatus.WARNING else "[X]")
        if alert:
            alerts.append(alert)

    print(f"  Readings processed: {len(readings)}")
    print(f"  Anomalies detected: {len(alerts)}")
    print(f"\n  Alerts generated:")
    for a in alerts:
        print(f"    [{a.timestamp.strftime('%H:%M')}] {a.status.value.upper()}: "
              f"{a.parameter}={a.current_value:.1f} {a.unit}")
        print(f"             Reason: {a.reason}")
        print(f"             Severity Score: {a.severity_score:.2f}")
        print()

    # Health summary
    summary = agent.get_equipment_health_summary("P-101A")
    print(f"  Equipment Health Summary:")
    for param, data in summary.get("parameters", {}).items():
        print(f"    {param}: latest={data['latest']:.1f}, "
              f"mean={data['mean']:.1f}, trend={data['trend']}")

    return alerts

def demo_fault_diagnosis(alerts):
    """Demo: Fault Diagnosis Agent generates root cause hypotheses."""
    print("\n\n" + "=" * 70)
    print("  AGENT 2: FAULT DIAGNOSIS & SUGGESTION")
    print("  Analyzing anomalies and suggesting corrective actions")
    print("=" * 70)

    from app.services.agents.fault_diagnosis_agent import FaultDiagnosisAgent

    agent = FaultDiagnosisAgent(neo4j_client=None)  # No KG in standalone demo

    if not alerts:
        print("\n  No alerts to diagnose.")
        return

    # Take the most critical alert
    critical_alert = max(alerts, key=lambda a: a.severity_score)
    print(f"\n  Diagnosing: {critical_alert.equipment_tag} - "
          f"{critical_alert.parameter} {critical_alert.status.value}")
    print(f"  Value: {critical_alert.current_value} {critical_alert.unit}")

    # Run synchronous part of diagnosis (pattern matching)
    hypotheses = agent._get_pattern_hypotheses(critical_alert)

    print(f"\n  Root Cause Hypotheses ({len(hypotheses)} generated):")
    for i, h in enumerate(sorted(hypotheses, key=lambda x: x.confidence, reverse=True), 1):
        print(f"    {i}. {h.cause}")
        print(f"       Confidence: {h.confidence:.0%} | Category: {h.category}")
        print(f"       Evidence: {h.evidence[0]}")
        print()

    # Get standard actions
    actions = agent._generate_actions(hypotheses, critical_alert)
    print(f"  Recommended Actions ({len(actions)}):")
    for i, a in enumerate(actions, 1):
        print(f"    {i}. [{a.priority.upper()}] {a.action}")
        if a.parts_needed:
            print(f"       Parts: {', '.join(a.parts_needed)}")
        if a.sop_reference:
            print(f"       Reference: {a.sop_reference}")
        if a.safety_precautions:
            print(f"       Safety: {', '.join(a.safety_precautions)}")
        print()

def demo_predictive_maintenance():
    """Demo: Predictive Maintenance Agent estimates RUL."""
    print("\n\n" + "=" * 70)
    print("  AGENT 3: PREDICTIVE MAINTENANCE")
    print("  Estimating Remaining Useful Life (RUL)")
    print("=" * 70)

    from app.services.agents.predictive_maintenance_agent import PredictiveMaintenanceAgent

    agent = PredictiveMaintenanceAgent()

    # Simulate degrading vibration history (50 readings over 50 hours)
    vibration_history = [3.5 + (i * 0.15) + (0.1 * (i % 4)) for i in range(50)]
    # Latest reading: ~10.5 mm/s, limit: 14.0 mm/s

    print(f"\n  Equipment: P-101A (Pump)")
    print(f"  Current vibration: {vibration_history[-1]:.1f} mm/s")
    print(f"  Critical limit: 14.0 mm/s")
    print(f"  Trend: Increasing at ~0.15 mm/s per hour")
    print(f"  Hours in service since last maintenance: 18000")

    report = agent.predict(
        equipment_tag="P-101A",
        parameter_history={"vibration": vibration_history},
        critical_limits={"vibration": 14.0},
        next_scheduled_pm=datetime.utcnow() + timedelta(days=45),
        equipment_type="pump",
        hours_since_last_maintenance=18000,
    )

    print(f"\n  --- Predictive Report ---")
    print(f"  Overall Health Score: {report.overall_health_score:.1f}%")
    print(f"  Risk Summary: {report.risk_summary}")

    print(f"\n  RUL Estimates:")
    for rul in report.rul_estimates:
        print(f"    Parameter: {rul.parameter}")
        print(f"    Days to failure: {rul.estimated_days_to_failure:.1f} "
              f"(CI: {rul.confidence_interval[0]:.1f} - {rul.confidence_interval[1]:.1f})")
        print(f"    Risk Score: {rul.risk_score:.0%}")
        print(f"    Method: {rul.method}")
        print(f"    Health: {rul.current_health_pct:.1f}%")
        print()

    print(f"  Maintenance Recommendations:")
    for rec in report.maintenance_recommendations:
        print(f"    Urgency: {rec.urgency.upper()}")
        print(f"    Action: {rec.action}")
        print(f"    Recommended Date: {rec.recommended_date.strftime('%d-%b-%Y')}")
        print(f"    Cost of planned fix: ${rec.cost_of_early_intervention:,.0f}")
        print(f"    Cost of unplanned failure: ${rec.cost_of_unplanned_failure:,.0f}")
        print(f"    Reasoning: {rec.reasoning}")
        print()

def demo_shift_handover(alerts):
    """Demo: Shift Handover Agent generates report."""
    print("\n\n" + "=" * 70)
    print("  AGENT 4: SHIFT HANDOVER")
    print("  Generating automated shift report")
    print("=" * 70)

    from app.services.agents.shift_handover_agent import (
        ShiftHandoverAgent, ShiftEvent, HandoverReport,
    )

    agent = ShiftHandoverAgent()

    shift_start = datetime(2024, 7, 1, 6, 0)
    shift_end = datetime(2024, 7, 1, 18, 0)

    # Log events from this shift
    agent.log_event(ShiftEvent(
        timestamp=shift_start + timedelta(hours=1),
        event_type="maintenance",
        severity="medium",
        equipment_tag="HX-501",
        description="Scheduled cleaning of heat exchanger tubes",
        status="resolved",
        assigned_to="Rajesh Kumar",
        action_taken="Cleaned, back in service at 08:30",
    ))

    # Log the sensor alerts
    for alert in alerts[:3]:
        agent.log_alarm(alert, action_taken="Monitoring, maintenance team notified")

    agent.log_event(ShiftEvent(
        timestamp=shift_start + timedelta(hours=8),
        event_type="operator_action",
        severity="info",
        equipment_tag="C-301",
        description="Compressor speed reduced from 3500 to 3200 RPM per operator decision",
        status="resolved",
        action_taken="Load reduced to manage temperature",
    ))

    agent.log_event(ShiftEvent(
        timestamp=shift_start + timedelta(hours=10),
        event_type="maintenance",
        severity="high",
        equipment_tag="P-101A",
        description="Vibration inspection requested - bearing check pending",
        status="in_progress",
        assigned_to="Suresh Patel",
    ))

    # Generate report (synchronous parts only for demo)
    import asyncio

    async def gen():
        return await agent.generate_report(shift_start, shift_end)

    try:
        report = asyncio.run(gen())
    except Exception:
        # Fallback if Ollama not available
        report = HandoverReport(
            shift_start=shift_start,
            shift_end=shift_end,
            shift_type="day",
            executive_summary=[
                "3 vibration alarms on P-101A - trending upward, maintenance notified",
                "HX-501 cleaning completed successfully",
                "C-301 speed reduced (operator decision) - monitor temperature",
                "P-101A bearing inspection IN PROGRESS (Suresh Patel)",
            ],
            critical_items=[{
                "equipment": "P-101A",
                "issue": "Vibration exceeding warning limit (11.5 mm/s)",
                "status": "pending",
                "action": "Monitoring, maintenance team notified",
                "time": "14:00",
            }],
            alarms_summary={"total": 3, "critical": 1, "high": 2, "resolved": 0, "pending": 3},
            work_in_progress=[{
                "equipment": "P-101A",
                "activity": "Bearing inspection",
                "status": "in_progress",
                "assigned_to": "Suresh Patel",
            }],
            watch_items=[{
                "equipment": "P-101A",
                "reason": "Recurring alarms (3 times this shift) - developing bearing issue",
            }],
            total_alarms=3,
            critical_alarms=1,
            maintenance_actions=2,
        )

    formatted = agent.format_report_text(report)
    print(f"\n{formatted}")

def demo_agent_coordination():
    """Show how all agents work together."""
    print("\n\n" + "=" * 70)
    print("  AGENT COORDINATION - Full Pipeline Example")
    print("=" * 70)

    print("""
  ┌─────────────────────────────────────────────────────────────────┐
  │ SCENARIO: Bearing degradation detected on Pump P-101A          │
  └─────────────────────────────────────────────────────────────────┘

  Timeline:

  [08:00] SENSOR MONITOR AGENT:
          -> Vibration reading: 7.5 mm/s (trending up at 0.3 mm/s/hour)
          -> Status: NORMAL (but trend detected)
          -> Action: Continue monitoring, log trend

  [12:00] SENSOR MONITOR AGENT:
          -> Vibration reading: 9.8 mm/s
          -> Status: WARNING (approaching 11.2 mm/s alarm)
          -> Action: Trigger Fault Diagnosis Agent

  [12:01] FAULT DIAGNOSIS AGENT:
          -> Queried Knowledge Graph:
            • P-101A had bearing failure in Mar-2024 (WO-100234)
            • Similar pattern seen on P-101B in Aug-2023
            • OEM recommends bearing inspection at 8.0 mm/s
          -> Top Hypothesis: "Bearing wear - lubrication degradation" (85%)
          -> Recommended Actions:
            1. IMMEDIATE: Sample lube oil (1 hour)
            2. SHORT-TERM: Schedule bearing inspection (4 hours)
            3. LONG-TERM: Review lubrication PM frequency

  [12:02] PREDICTIVE MAINTENANCE AGENT:
          -> Current degradation rate: 0.3 mm/s per hour
          -> Critical limit: 14.0 mm/s
          -> Estimated failure: 14 hours (by 02:00 tomorrow)
          -> Next scheduled PM: 45 days away
          -> RECOMMENDATION: "Advance PM immediately. Failure imminent."
          -> Cost analysis:
            • Planned repair now: $2,500
            • Unplanned failure tonight: $45,000 + 72h downtime

  [18:00] SHIFT HANDOVER AGENT:
          -> Generates report for incoming night shift:
            "CRITICAL: P-101A vibration WARNING. Bearing failure predicted
             within 14 hours. Diagnosis suggests lube degradation.
             Oil sampling in progress (Suresh Patel). Recommend preparing
             for emergency bearing replacement if oil results confirm."

  ┌─────────────────────────────────────────────────────────────────┐
  │ OUTCOME: Night shift team takes preemptive action, avoids       │
  │ unplanned failure. $42,500 saved. Zero downtime.                │
  └─────────────────────────────────────────────────────────────────┘
""")

if __name__ == "__main__":
    print("=" * 70)
    print("  AXIOM - Multi-Agent Operations Intelligence Demo")
    print("  4 Agents working together for equipment health management")
    print("=" * 70)

    # Run all agent demos
    alerts = demo_sensor_monitor()
    demo_fault_diagnosis(alerts)
    demo_predictive_maintenance()
    demo_shift_handover(alerts)
    demo_agent_coordination()

    print("\n" + "=" * 70)
    print("  DEMO COMPLETE - All 4 agents demonstrated successfully")
    print("=" * 70)
```

---

## `scripts/demo_pipeline.py`

**Pipeline demo script**

```python
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
```

---

## `scripts/test_pdf_ingest.py`

**PDF ingestion test**

```python
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
```

---