"""
Document Ingestion API — upload documents and trigger the full processing pipeline.
Includes SSE streaming endpoint for real-time pipeline step visualization.
"""

from fastapi import APIRouter, UploadFile, File, Request, HTTPException
from fastapi.responses import StreamingResponse
from pathlib import Path
import json
import uuid
import asyncio
import time
import hashlib
import re
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

def _content_hash(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def _hash_index_path() -> Path:
    return Path(settings.upload_dir) / "_content_hashes.json"

def _load_hash_index() -> dict:
    """Maps content sha256 -> {document_id, filename}, used to detect re-uploads
    of a document already ingested (same bytes) so we don't duplicate vectors/graph nodes."""
    path = _hash_index_path()
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}

def _save_hash_index(index: dict):
    _hash_index_path().write_text(json.dumps(index), encoding="utf-8")

def _safe_stored_filename(original: str, content_hash: str) -> str:
    """
    Derive a filesystem-safe stored filename from a client-supplied name.
    Path(original).name strips directory components (defeats ../ traversal and
    absolute paths); the hash suffix prevents two different uploads with the
    same display name from silently overwriting each other on disk.
    """
    name = Path(original).name or "file"
    stem = Path(name).stem
    ext = Path(name).suffix.lower()
    safe_stem = re.sub(r"[^A-Za-z0-9._-]", "_", stem)[:100] or "file"
    return f"{safe_stem}_{content_hash[:10]}{ext}"

@router.post("/document/stream")
async def ingest_document_stream(request: Request, file: UploadFile = File(...)):
    """
    Stream the ingestion pipeline steps in real-time via SSE.
    Each step emits an event with status, data, and timing.
    """
    display_filename = Path(file.filename).name or "file"
    allowed_extensions = {".pdf", ".docx", ".doc", ".xlsx", ".png", ".jpg", ".jpeg", ".tiff", ".tif", ".txt", ".json", ".csv"}
    file_ext = Path(display_filename).suffix.lower()
    if file_ext not in allowed_extensions:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {file_ext}")

    file_bytes = await file.read()
    content_hash = _content_hash(file_bytes)

    hash_index = _load_hash_index()
    existing = hash_index.get(content_hash)
    if existing:
        async def already_ingested():
            yield _sse_event("duplicate", {
                "message": "This exact file was already ingested — skipping re-processing.",
                "document_id": existing["document_id"],
                "filename": existing["filename"],
            })
        return StreamingResponse(already_ingested(), media_type="text/event-stream")

    # Save file first
    upload_dir = Path(settings.upload_dir)
    upload_dir.mkdir(parents=True, exist_ok=True)
    stored_name = _safe_stored_filename(display_filename, content_hash)
    file_path = upload_dir / stored_name
    file_path.write_bytes(file_bytes)

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
        ocr_page_texts: dict[int, str] = {}
        for page in parsed.pages:
            page_text = page.text
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
                        page_text = ocr_result.text
                        raw_text_parts.append(page_text)
                        ocr_pages.append({
                            "page": page.page_number,
                            "confidence": round(ocr_result.confidence, 3),
                            "chars": len(ocr_result.text),
                        })
                    except Exception:
                        raw_text_parts.append(page.text)
                else:
                    raw_text_parts.append(page.text)

            ocr_page_texts[page.page_number] = page_text

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
        cleaned_page_texts = {
            page_number: text_cleaner.clean(text)
            for page_number, text in ocr_page_texts.items()
        }
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
        category = classifier.classify(cleaned_text, display_filename)

        yield _sse_event("step", {
            "step": 6, "name": "Document Classification",
            "status": "complete",
            "result": {"category": category.value, "filename": display_filename},
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
        next_chunk_index = 0
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
                        metadata={"filename": display_filename, "category": category.value, "page": page.page, "section": section.heading},
                        start_index=next_chunk_index,
                    )
                    next_chunk_index += len(section_chunks)
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
            request.app.state.retriever.update_bm25_index(faiss_service.get_all_metadata())
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
            document_id=document_id, filename=display_filename,
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

        # Record content hash so a re-upload of these exact bytes is recognized next time
        hash_index[content_hash] = {"document_id": document_id, "filename": display_filename}
        _save_hash_index(hash_index)

        # === COMPLETE ===
        total_duration = int((time.time() - pipeline_start) * 1000)
        yield _sse_event("complete", {
            "document_id": document_id,
            "filename": display_filename,
            "category": category.value,
            "total_pages": parsed.total_pages,
            "total_chunks": len(all_chunks),
            "total_entities": len(entities),
            "total_relationships": len(relationships),
            "faiss_status": faiss_status,
            "graph_status": graph_status,
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
    display_filename = Path(file.filename).name or "file"
    allowed_extensions = {".pdf", ".docx", ".doc", ".xlsx", ".png", ".jpg", ".jpeg", ".tiff", ".tif", ".txt", ".json", ".csv"}
    file_ext = Path(display_filename).suffix.lower()
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {file_ext}. Allowed: {allowed_extensions}",
        )

    file_bytes = await file.read()
    content_hash = _content_hash(file_bytes)

    hash_index = _load_hash_index()
    existing = hash_index.get(content_hash)
    if existing:
        return {
            "status": "duplicate",
            "message": "This exact file was already ingested — skipping re-processing.",
            "document_id": existing["document_id"],
            "filename": existing["filename"],
        }

    # Save uploaded file under a sanitized, collision-proof name
    upload_dir = Path(settings.upload_dir)
    upload_dir.mkdir(parents=True, exist_ok=True)
    stored_name = _safe_stored_filename(display_filename, content_hash)
    file_path = upload_dir / stored_name

    try:
        file_path.write_bytes(file_bytes)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")

    logger.info("File uploaded", filename=display_filename, path=str(file_path))

    # Run ingestion pipeline
    try:
        pipeline = IngestionPipeline()
        document = await pipeline.ingest(file_path, filename=display_filename)
    except Exception as e:
        logger.error("Ingestion failed", error=str(e), filename=display_filename)
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {str(e)}")

    # Index chunks in FAISS vector store
    faiss_indexed = False
    faiss_error = None
    try:
        faiss_service: FAISSService = request.app.state.faiss
        await faiss_service.index_chunks(document.chunks, document.document_id)
        request.app.state.retriever.update_bm25_index(faiss_service.get_all_metadata())
        faiss_indexed = True
    except Exception as e:
        faiss_error = str(e)
        logger.error("FAISS indexing failed", error=faiss_error)

    # Populate knowledge graph
    graph_populated = False
    graph_error = None
    try:
        neo4j: Neo4jClient = request.app.state.neo4j
        graph_builder = GraphBuilder(neo4j)
        await graph_builder.populate_from_document(document)
        graph_populated = True
    except Exception as e:
        graph_error = str(e)
        logger.error("Graph population failed", error=graph_error)

    # Only remember this hash if the document actually made it into at least
    # one retrievable store — otherwise a re-upload after a transient failure
    # would be silently skipped as a "duplicate" of a document that isn't there.
    if faiss_indexed or graph_populated:
        hash_index[content_hash] = {"document_id": document.document_id, "filename": display_filename}
        _save_hash_index(hash_index)

    warnings = []
    if not faiss_indexed:
        warnings.append(f"Vector indexing failed — document is not searchable: {faiss_error}")
    if not graph_populated:
        warnings.append(f"Knowledge graph population failed: {graph_error}")

    return {
        "status": "success" if (faiss_indexed and graph_populated) else "partial_success" if (faiss_indexed or graph_populated) else "failed",
        "warnings": warnings,
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
        "successful": sum(1 for r in results if r.get("status") in ("success", "duplicate")),
        "partial": sum(1 for r in results if r.get("status") == "partial_success"),
        "failed": sum(1 for r in results if r.get("status") == "failed"),
        "results": results,
    }