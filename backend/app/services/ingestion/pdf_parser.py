"""PDF parser for AXIOM ingestion workflows."""

from __future__ import annotations

from io import BytesIO
import logging
from pathlib import Path
from typing import Any

import fitz

from backend.app.models.schemas import BoundingBox, ExtractedImage, ExtractedTable, ExtractedTextBlock, ExtractionMethod, IngestionIssue, SeverityLevel
from backend.app.services.ingestion.ingestion_types import ParsedDocument


logger = logging.getLogger(__name__)


class PDFParserError(RuntimeError):
    """Raised when a PDF cannot be parsed safely."""


class PDFParser:
    """Extract text, tables, and embedded image metadata from PDF files."""

    def __init__(self) -> None:
        """Initialize the parser."""
        self._logger = logger.getChild(self.__class__.__name__)

    def parse(self, file_path: str | Path, *, enable_table_extraction: bool = True) -> ParsedDocument:
        """Parse a PDF file into normalized ingestion artifacts."""
        path = Path(file_path)
        if not path.exists():
            raise PDFParserError(f"PDF file not found: {path}")

        parsed = ParsedDocument()
        try:
            with fitz.open(path) as document:
                parsed.page_count = document.page_count or 1
                for page_index in range(document.page_count):
                    page_number = page_index + 1
                    page = document.load_page(page_index)
                    parsed.text_blocks.extend(self._extract_text_blocks(page, page_number))
                    if enable_table_extraction:
                        parsed.tables.extend(self._extract_tables(page, page_number))
                    parsed.images.extend(self._extract_images(page, page_number))
        except Exception as exc:  # pragma: no cover - depends on native parser internals
            self._logger.exception("Failed to parse PDF", extra={"path": str(path)})
            raise PDFParserError(f"Failed to parse PDF file: {path}") from exc

        if not parsed.text_blocks:
            parsed.issues.append(
                IngestionIssue(
                    code="pdf.no_text",
                    message="No text blocks were extracted from the PDF; OCR fallback may be required.",
                    severity=SeverityLevel.WARNING,
                )
            )
        return parsed

    def _extract_text_blocks(self, page: fitz.Page, page_number: int) -> list[ExtractedTextBlock]:
        """Extract layout-aware text blocks from a PDF page."""
        page_rect = page.rect
        blocks: list[ExtractedTextBlock] = []
        for block in page.get_text("blocks"):
            x0, y0, x1, y1, text, *_ = block
            normalized_text = " ".join(text.split())
            if not normalized_text:
                continue
            blocks.append(
                ExtractedTextBlock(
                    page_number=page_number,
                    text=normalized_text,
                    extraction_method=ExtractionMethod.DIRECT_TEXT,
                    confidence=1.0,
                    bounding_box=self._normalize_bbox(x0, y0, x1, y1, page_rect.width, page_rect.height),
                )
            )
        return blocks

    def _extract_tables(self, page: fitz.Page, page_number: int) -> list[ExtractedTable]:
        """Extract tables using PyMuPDF's table detector when available."""
        tables: list[ExtractedTable] = []
        try:
            finder = page.find_tables()
        except Exception:
            return tables

        for table in finder.tables:
            extracted = table.extract()
            if not extracted:
                continue
            headers = [str(cell or "").strip() for cell in extracted[0] if str(cell or "").strip()]
            data_rows = [[str(cell or "").strip() for cell in row] for row in extracted[1:]]
            if not headers:
                continue
            try:
                tables.append(
                    ExtractedTable(
                        page_number=page_number,
                        headers=headers,
                        rows=[row[: len(headers)] + [""] * max(0, len(headers) - len(row)) for row in data_rows],
                        extraction_method=ExtractionMethod.TABLE,
                        confidence=0.85,
                    )
                )
            except Exception:
                self._logger.warning("Skipping malformed table", extra={"page_number": page_number})
        return tables

    def _extract_images(self, page: fitz.Page, page_number: int) -> list[ExtractedImage]:
        """Extract embedded image metadata from a PDF page."""
        images: list[ExtractedImage] = []
        for image_info in page.get_image_info(xrefs=True):
            width = int(image_info.get("width", 0))
            height = int(image_info.get("height", 0))
            if width <= 0 or height <= 0:
                continue
            bbox = image_info.get("bbox")
            normalized_bbox = None
            if bbox:
                x0, y0, x1, y1 = bbox
                normalized_bbox = self._normalize_bbox(x0, y0, x1, y1, page.rect.width, page.rect.height)
            images.append(
                ExtractedImage(
                    page_number=page_number,
                    content_type="image/png",
                    width=width,
                    height=height,
                    bounding_box=normalized_bbox,
                    caption=f"Embedded image {len(images) + 1} on page {page_number}",
                )
            )
        return images

    @staticmethod
    def render_page_image(file_path: str | Path, page_number: int, *, dpi: int = 200) -> bytes:
        """Render a PDF page to PNG bytes for OCR fallback."""
        path = Path(file_path)
        with fitz.open(path) as document:
            page = document.load_page(page_number - 1)
            matrix = fitz.Matrix(dpi / 72.0, dpi / 72.0)
            pixmap = page.get_pixmap(matrix=matrix, alpha=False)
            return pixmap.tobytes("png")

    @staticmethod
    def _normalize_bbox(x0: float, y0: float, x1: float, y1: float, page_width: float, page_height: float) -> BoundingBox:
        """Normalize page coordinates into 0..1 bounding boxes."""
        width = max(page_width, 1.0)
        height = max(page_height, 1.0)
        return BoundingBox(
            x_min=max(0.0, min(1.0, x0 / width)),
            y_min=max(0.0, min(1.0, y0 / height)),
            x_max=max(0.0, min(1.0, x1 / width)),
            y_max=max(0.0, min(1.0, y1 / height)),
        )
