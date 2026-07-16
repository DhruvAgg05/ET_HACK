"""End-to-end ingestion pipeline orchestration for AXIOM."""

from __future__ import annotations

import asyncio
from hashlib import sha256
import logging
from mimetypes import guess_type
from pathlib import Path
from time import perf_counter

from backend.app.models.schemas import (
    DocumentIngestionRequest,
    DocumentIngestionResult,
    DocumentMetadata,
    DocumentType,
    IngestionIssue,
    ProcessingStatus,
    SeverityLevel,
)
from backend.app.services.ingestion.chunker import Chunker
from backend.app.services.ingestion.document_classifier import DocumentClassifier
from backend.app.services.ingestion.docx_parser import DOCXParser, DOCXParserError
from backend.app.services.ingestion.entity_extractor import EntityExtractor
from backend.app.services.ingestion.ingestion_types import ParsedDocument
from backend.app.services.ingestion.llm_extractor import LLMExtractor
from backend.app.services.ingestion.ocr_engine import OCREngine, OCREngineError
from backend.app.services.ingestion.pdf_parser import PDFParser, PDFParserError
from backend.app.services.ingestion.relationship_extractor import RelationshipExtractor


logger = logging.getLogger(__name__)


class IngestionPipelineError(RuntimeError):
    """Raised when the ingestion pipeline fails irrecoverably."""


class IngestionPipeline:
    """Production ingestion pipeline for industrial documents."""

    def __init__(
        self,
        *,
        pdf_parser: PDFParser | None = None,
        docx_parser: DOCXParser | None = None,
        ocr_engine: OCREngine | None = None,
        document_classifier: DocumentClassifier | None = None,
        chunker: Chunker | None = None,
        entity_extractor: EntityExtractor | None = None,
        relationship_extractor: RelationshipExtractor | None = None,
        llm_extractor: LLMExtractor | None = None,
    ) -> None:
        """Initialize the ingestion pipeline with dependency injection."""
        self._pdf_parser = pdf_parser or PDFParser()
        self._docx_parser = docx_parser or DOCXParser()
        self._ocr_engine = ocr_engine or OCREngine()
        self._document_classifier = document_classifier or DocumentClassifier()
        self._chunker = chunker or Chunker()
        self._entity_extractor = entity_extractor or EntityExtractor()
        self._relationship_extractor = relationship_extractor or RelationshipExtractor()
        self._llm_extractor = llm_extractor or LLMExtractor()
        self._logger = logger.getChild(self.__class__.__name__)

    async def process(self, request: DocumentIngestionRequest) -> DocumentIngestionResult:
        """Process a single document into structured ingestion artifacts."""
        started_at = perf_counter()
        file_path = Path(request.storage_path)
        metadata = self._prepare_metadata(request.metadata, file_path)
        issues: list[IngestionIssue] = []

        if not file_path.exists():
            raise IngestionPipelineError(f"Input file does not exist: {file_path}")

        try:
            parsed = await self._parse_document(file_path, metadata.document_type, request.options.enable_table_extraction)
        except (PDFParserError, DOCXParserError, OCREngineError) as exc:
            self._logger.exception("Ingestion parsing failed", extra={"path": str(file_path)})
            raise IngestionPipelineError(f"Failed to parse document: {file_path}") from exc

        issues.extend(parsed.issues)

        if request.options.enable_ocr and self._should_run_ocr(metadata.document_type, parsed):
            ocr_parsed = await self._perform_ocr_fallback(file_path, metadata.document_type, parsed.page_count)
            parsed.text_blocks.extend(ocr_parsed.text_blocks)
            parsed.ocr_words.extend(ocr_parsed.ocr_words)
            issues.extend(ocr_parsed.issues)

        classified_metadata, classification_issues = self._classify_document(metadata, parsed)
        metadata = classified_metadata
        issues.extend(classification_issues)

        entities = self._entity_extractor.extract(parsed.text_blocks, metadata)
        relationships = self._relationship_extractor.extract(entities, parsed.text_blocks)

        llm_entities = []
        llm_relationships = []
        if request.options.enable_llm_extraction:
            llm_entities, llm_relationships, llm_issues = await self._llm_extractor.extract(
                metadata,
                parsed.combined_text,
                entities,
            )
            issues.extend(llm_issues)
            entities = self._merge_entities(entities, llm_entities)
            relationships = self._merge_relationships(relationships, llm_relationships)

        chunks = self._chunker.chunk_text_blocks(metadata.document_id, parsed.text_blocks)

        status = ProcessingStatus.COMPLETED
        if any(issue.severity == SeverityLevel.CRITICAL for issue in issues):
            status = ProcessingStatus.FAILED
        elif issues:
            status = ProcessingStatus.PARTIAL

        elapsed_ms = int((perf_counter() - started_at) * 1000)
        return DocumentIngestionResult(
            metadata=metadata,
            status=status,
            text_blocks=parsed.text_blocks,
            tables=parsed.tables,
            images=parsed.images,
            ocr_words=parsed.ocr_words,
            entities=entities,
            relationships=relationships,
            chunks=chunks,
            issues=issues,
            processing_time_ms=elapsed_ms,
        )

    async def _parse_document(self, file_path: Path, document_type: DocumentType, enable_tables: bool) -> ParsedDocument:
        """Dispatch to the correct parser based on document type and file extension."""
        effective_type = self._resolve_document_type(document_type, file_path)
        if effective_type == DocumentType.PDF:
            return await asyncio.to_thread(self._pdf_parser.parse, file_path, enable_table_extraction=enable_tables)
        if effective_type == DocumentType.DOCX:
            return await asyncio.to_thread(self._docx_parser.parse, file_path, enable_table_extraction=enable_tables)
        if effective_type in {DocumentType.IMAGE, DocumentType.PID_DRAWING}:
            return await asyncio.to_thread(self._ocr_engine.extract_from_file, file_path, page_number=1)
        if effective_type == DocumentType.TEXT:
            return await asyncio.to_thread(self._parse_plain_text_document, file_path)

        mime_type, _ = guess_type(file_path.name)
        if mime_type == "application/pdf":
            return await asyncio.to_thread(self._pdf_parser.parse, file_path, enable_table_extraction=enable_tables)
        if mime_type in {
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "application/msword",
        }:
            return await asyncio.to_thread(self._docx_parser.parse, file_path, enable_table_extraction=enable_tables)
        return await asyncio.to_thread(self._ocr_engine.extract_from_file, file_path, page_number=1)

    async def _perform_ocr_fallback(self, file_path: Path, document_type: DocumentType, page_count: int) -> ParsedDocument:
        """Perform OCR when direct extraction yields sparse or no text."""
        if document_type == DocumentType.PDF:
            merged = ParsedDocument(page_count=page_count)
            for page_number in range(1, page_count + 1):
                page_bytes = await asyncio.to_thread(self._pdf_parser.render_page_image, file_path, page_number)
                page_result = await asyncio.to_thread(self._ocr_engine.extract_from_bytes, page_bytes, page_number=page_number)
                merged.text_blocks.extend(page_result.text_blocks)
                merged.ocr_words.extend(page_result.ocr_words)
                merged.issues.extend(page_result.issues)
            return merged
        return await asyncio.to_thread(self._ocr_engine.extract_from_file, file_path, page_number=1)

    def _classify_document(
        self,
        metadata: DocumentMetadata,
        parsed: ParsedDocument,
    ) -> tuple[DocumentMetadata, list[IngestionIssue]]:
        """Classify the document and enrich metadata with parser results."""
        issues: list[IngestionIssue] = []
        classification = self._document_classifier.classify(metadata, parsed.combined_text)
        updated_type = metadata.document_type
        if metadata.document_type == DocumentType.UNKNOWN and classification.document_type != DocumentType.UNKNOWN:
            updated_type = classification.document_type
        elif classification.document_type != DocumentType.UNKNOWN and classification.document_type != metadata.document_type:
            issues.append(
                IngestionIssue(
                    code="classification.mismatch",
                    message=(
                        f"Classifier suggested '{classification.document_type.value}' "
                        f"while metadata declared '{metadata.document_type.value}'."
                    ),
                    severity=SeverityLevel.INFO,
                )
            )
        updated_metadata = metadata.model_copy(
            update={
                "document_type": updated_type,
                "page_count": parsed.page_count,
                "external_metadata": {
                    **metadata.external_metadata,
                    "classification_scores": {
                        document_type.value: round(score, 3) for document_type, score in classification.scores.items()
                    },
                    "classification_confidence": round(classification.confidence, 3),
                },
            }
        )
        return updated_metadata, issues

    def _prepare_metadata(self, metadata: DocumentMetadata, file_path: Path) -> DocumentMetadata:
        """Backfill metadata fields derived from the source file."""
        mime_type = metadata.mime_type or (guess_type(file_path.name)[0] or "application/octet-stream")
        checksum = metadata.checksum_sha256 or self._compute_checksum(file_path)
        title = metadata.title or file_path.stem
        return metadata.model_copy(
            update={
                "title": title,
                "mime_type": mime_type,
                "checksum_sha256": checksum,
            }
        )

    def _parse_plain_text_document(self, file_path: Path) -> ParsedDocument:
        """Parse a plain text document into text blocks."""
        text = file_path.read_text(encoding="utf-8", errors="ignore")
        parsed = ParsedDocument(page_count=1)
        blocks = [segment.strip() for segment in text.splitlines() if segment.strip()]
        for block in blocks:
            parsed.text_blocks.append(
                self._ocr_engine._build_text_blocks(  # type: ignore[attr-defined]
                    {(1, 1, len(parsed.text_blocks) + 1): [(0, block)]},
                    {(1, 1, len(parsed.text_blocks) + 1): [(0, 0, max(len(block), 1), 1)]},
                    1,
                    max(len(block), 1),
                    1,
                )[0]
            )
        return parsed

    @staticmethod
    def _resolve_document_type(document_type: DocumentType, file_path: Path) -> DocumentType:
        """Resolve a document type from explicit metadata or file extension."""
        if document_type != DocumentType.UNKNOWN:
            return document_type
        suffix = file_path.suffix.lower()
        if suffix == ".pdf":
            return DocumentType.PDF
        if suffix in {".docx", ".doc"}:
            return DocumentType.DOCX
        if suffix in {".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp"}:
            return DocumentType.IMAGE
        if suffix in {".txt", ".md"}:
            return DocumentType.TEXT
        return DocumentType.UNKNOWN

    @staticmethod
    def _should_run_ocr(document_type: DocumentType, parsed: ParsedDocument) -> bool:
        """Determine whether OCR fallback should be triggered."""
        combined_length = len(parsed.combined_text)
        return document_type in {DocumentType.IMAGE, DocumentType.PID_DRAWING} or combined_length < 120

    @staticmethod
    def _merge_entities(base: list, additions: list) -> list:
        """Merge entities while preferring higher confidence duplicates."""
        merged = {(
            entity.entity_type,
            entity.canonical_name.casefold(),
            entity.page_number,
        ): entity for entity in base}
        for entity in additions:
            key = (entity.entity_type, entity.canonical_name.casefold(), entity.page_number)
            current = merged.get(key)
            if current is None or entity.confidence > current.confidence:
                merged[key] = entity
        return list(merged.values())

    @staticmethod
    def _merge_relationships(base: list, additions: list) -> list:
        """Merge relationships while preferring higher confidence duplicates."""
        merged = {
            (rel.source_entity_id, rel.target_entity_id, rel.relationship_type): rel
            for rel in base
        }
        for relationship in additions:
            key = (relationship.source_entity_id, relationship.target_entity_id, relationship.relationship_type)
            current = merged.get(key)
            if current is None or relationship.confidence > current.confidence:
                merged[key] = relationship
        return list(merged.values())

    @staticmethod
    def _compute_checksum(file_path: Path) -> str:
        """Compute a SHA-256 checksum for the source document."""
        digest = sha256()
        with file_path.open("rb") as file:
            for chunk in iter(lambda: file.read(8192), b""):
                digest.update(chunk)
        return digest.hexdigest()
