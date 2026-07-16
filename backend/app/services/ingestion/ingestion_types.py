"""Shared internal types for AXIOM ingestion workflows."""

from __future__ import annotations

from dataclasses import dataclass, field

from backend.app.models.schemas import ExtractedImage, ExtractedTable, ExtractedTextBlock, IngestionIssue, OCRWord


@dataclass(slots=True)
class ParsedDocument:
    """Normalized parser output consumed by the ingestion pipeline."""

    text_blocks: list[ExtractedTextBlock] = field(default_factory=list)
    tables: list[ExtractedTable] = field(default_factory=list)
    images: list[ExtractedImage] = field(default_factory=list)
    ocr_words: list[OCRWord] = field(default_factory=list)
    issues: list[IngestionIssue] = field(default_factory=list)
    page_count: int = 1

    @property
    def combined_text(self) -> str:
        """Return all extracted text blocks as a single normalized string."""
        return "\n\n".join(block.text for block in self.text_blocks).strip()

