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