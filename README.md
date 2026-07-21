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