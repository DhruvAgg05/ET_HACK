"""Semantic chunker for AXIOM ingestion text."""

from __future__ import annotations

import logging
import re
from typing import Iterable
from uuid import UUID

from backend.app.config import Settings, get_settings
from backend.app.models.schemas import DocumentChunk, ExtractedTextBlock


logger = logging.getLogger(__name__)


class Chunker:
    """Boundary-aware text chunker that preserves headings and sentence flow."""

    _SENTENCE_BOUNDARY = re.compile(r"(?<=[.!?])\s+")
    _HEADING_PATTERN = re.compile(r"^(?:[A-Z][A-Z0-9 /&()-]{3,}|(?:\d+(?:\.\d+)+)\s+.+)$")

    def __init__(self, settings: Settings | None = None) -> None:
        """Initialize the chunker from application settings."""
        self._settings = settings or get_settings()
        self._logger = logger.getChild(self.__class__.__name__)

    def chunk_text_blocks(self, document_id: UUID, text_blocks: list[ExtractedTextBlock]) -> list[DocumentChunk]:
        """Convert extracted text blocks into semantically coherent chunks."""
        max_chars = self._settings.chunking.max_chars
        min_chars = self._settings.chunking.min_chars
        overlap_chars = self._settings.chunking.overlap_chars

        chunks: list[DocumentChunk] = []
        chunk_index = 0
        current_page_number: int | None = None
        buffer = ""
        buffer_start = 0
        buffer_section: str | None = None

        for block in text_blocks:
            block_text = block.text.strip()
            if not block_text:
                continue
            if self._is_heading(block_text):
                if buffer.strip():
                    chunks.append(
                        self._build_chunk(
                            document_id=document_id,
                            content=buffer.strip(),
                            chunk_index=chunk_index,
                            page_number=current_page_number,
                            char_start=buffer_start,
                            section_title=buffer_section,
                        )
                    )
                    chunk_index += 1
                    buffer = ""
                buffer_section = block_text[:255]
                current_page_number = block.page_number
                buffer_start = 0
                continue

            current_page_number = current_page_number or block.page_number
            segments = self._split_text(block_text)
            for segment in segments:
                candidate = f"{buffer} {segment}".strip() if buffer else segment
                if len(candidate) <= max_chars:
                    if not buffer:
                        buffer_start = 0
                    buffer = candidate
                    continue

                if buffer.strip():
                    chunks.append(
                        self._build_chunk(
                            document_id=document_id,
                            content=buffer.strip(),
                            chunk_index=chunk_index,
                            page_number=current_page_number,
                            char_start=buffer_start,
                            section_title=buffer_section,
                        )
                    )
                    chunk_index += 1
                    overlap = buffer[-overlap_chars:] if overlap_chars else ""
                    buffer = f"{overlap} {segment}".strip() if overlap else segment
                else:
                    for piece in self._hard_wrap(segment, max_chars):
                        if len(piece) < min_chars and chunks:
                            previous = chunks.pop()
                            merged = f"{previous.content} {piece}".strip()
                            chunks.append(
                                previous.model_copy(
                                    update={
                                        "content": merged,
                                        "token_count": self._estimate_token_count(merged),
                                        "char_end": (previous.char_start or 0) + len(merged),
                                    }
                                )
                            )
                        else:
                            chunks.append(
                                self._build_chunk(
                                    document_id=document_id,
                                    content=piece,
                                    chunk_index=chunk_index,
                                    page_number=current_page_number,
                                    char_start=0,
                                    section_title=buffer_section,
                                )
                            )
                            chunk_index += 1
                    buffer = ""

        if buffer.strip():
            chunks.append(
                self._build_chunk(
                    document_id=document_id,
                    content=buffer.strip(),
                    chunk_index=chunk_index,
                    page_number=current_page_number,
                    char_start=buffer_start,
                    section_title=buffer_section,
                )
            )
        return chunks

    def _split_text(self, text: str) -> list[str]:
        """Split text into semantic segments before chunk assembly."""
        sentences = [segment.strip() for segment in self._SENTENCE_BOUNDARY.split(text) if segment.strip()]
        return sentences or [text.strip()]

    def _hard_wrap(self, text: str, max_chars: int) -> Iterable[str]:
        """Hard-wrap a long text segment when semantic boundaries are insufficient."""
        start = 0
        while start < len(text):
            end = min(start + max_chars, len(text))
            if end < len(text):
                split_at = text.rfind(" ", start, end)
                if split_at > start:
                    end = split_at
            yield text[start:end].strip()
            start = end

    def _build_chunk(
        self,
        *,
        document_id: UUID,
        content: str,
        chunk_index: int,
        page_number: int | None,
        char_start: int | None,
        section_title: str | None,
    ) -> DocumentChunk:
        """Build a validated chunk object."""
        start = char_start if char_start is not None else 0
        return DocumentChunk(
            document_id=document_id,
            content=content,
            chunk_index=chunk_index,
            page_number=page_number,
            token_count=self._estimate_token_count(content),
            char_start=start,
            char_end=start + len(content),
            section_title=section_title,
            embedding_model=self._settings.embedding_model,
            metadata={"length_chars": len(content)},
        )

    @staticmethod
    def _estimate_token_count(text: str) -> int:
        """Estimate token count cheaply without a tokenizer dependency."""
        return max(1, int(len(text.split()) * 1.3))

    @classmethod
    def _is_heading(cls, text: str) -> bool:
        """Return whether a text block resembles a section heading."""
        return bool(cls._HEADING_PATTERN.match(text))
