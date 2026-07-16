# AXIOM Platform

AXIOM is an industrial knowledge intelligence platform designed around document ingestion, knowledge graph construction, vector retrieval, agentic workflows, and operational copilot experiences.

This step contains only the production-grade project setup and architecture scaffold. No application logic has been implemented yet.

## Stack Baseline

- Python `3.11`
- FastAPI for the async API layer
- Neo4j for the knowledge graph
- Qdrant for vector search
- Redis for caching and Celery transport
- TimescaleDB for temporal event storage
- LangChain and LangGraph for orchestration
- Sentence Transformers for embeddings
- PyMuPDF, Camelot, Tesseract OCR, Pillow, and OpenCV for ingestion
- spaCy and GLiNER for entity extraction

## Repository Layout

```text
.
├── backend
│   ├── Dockerfile
│   └── app
├── data
├── frontend
├── scripts
├── tests
├── .env.example
├── .gitignore
├── .pre-commit-config.yaml
├── docker-compose.yml
├── pyproject.toml
├── requirements-dev.txt
└── requirements.txt
```

## Local Installation

1. Ensure Python `3.11` is installed.
2. Create the environment:

```bash
py -3.11 -m venv .venv
```

3. Activate it:

```bash
.venv\Scripts\activate
```

4. Upgrade packaging tools:

```bash
python -m pip install --upgrade pip setuptools wheel
```

5. Install runtime dependencies:

```bash
pip install -r requirements.txt
```

6. Install development tooling:

```bash
pip install -r requirements-dev.txt
```

7. Copy the environment file:

```bash
Copy-Item .env.example .env
```

8. Install git hooks:

```bash
pre-commit install
```

## System Dependencies

The following native tools are required outside of Python:

- Docker Desktop
- Tesseract OCR
- Ghostscript
- Poppler utilities

The provided backend Docker image installs the Linux-native dependencies required for Tesseract, Camelot, and OpenCV.

## Docker Workflow

1. Create the runtime environment file:

```bash
Copy-Item .env.example .env
```

2. Build and start the stack:

```bash
docker-compose up --build -d
```

3. Pull the Ollama model after the container is running:

```bash
docker exec axiom-ollama ollama pull llama3.1:8b
```

## Quality Tooling

- `black` for code formatting
- `ruff` for linting and import sorting
- `mypy` in strict mode
- `pytest` with async support
- `pre-commit` for local enforcement

## Notes

- The scaffold uses Python `3.11` as the required interpreter baseline.
- Source modules are intentionally created without implementation in this step so the architecture can be built incrementally in the next phase.
