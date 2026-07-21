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