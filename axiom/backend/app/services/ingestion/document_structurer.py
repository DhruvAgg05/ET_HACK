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