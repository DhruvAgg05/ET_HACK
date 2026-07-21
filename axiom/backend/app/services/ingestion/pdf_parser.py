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