"""
Text chunking utility for splitting documents into retrieval-friendly segments.
Uses semantic-aware chunking that respects paragraph and section boundaries.
Chunk size: 300-600 tokens, overlap: 50-80 tokens.
"""

from dataclasses import dataclass
import re
import uuid
import structlog

from app.config import settings

logger = structlog.get_logger()

@dataclass
class Chunk:
    chunk_id: str
    content: str
    chunk_index: int
    page_number: int | None
    section_heading: str | None
    metadata: dict

class TextChunker:
    """
    Splits document text into chunks optimized for retrieval.
    Respects section/paragraph boundaries for better semantic coherence.

    Hierarchy: Document → Page → Section → Paragraph → Chunk
    """

    def __init__(
        self,
        chunk_size: int = settings.chunk_size,
        chunk_overlap: int = settings.chunk_overlap,
    ):
        self.chunk_size = chunk_size  # 300-600 tokens
        self.chunk_overlap = chunk_overlap  # 50-80 tokens

    def chunk_text(
        self,
        text: str,
        document_id: str,
        page_number: int | None = None,
        section_heading: str | None = None,
        metadata: dict | None = None,
    ) -> list[Chunk]:
        """Split text into overlapping chunks with semantic boundaries."""
        if not text.strip():
            return []

        metadata = metadata or {}

        # First, split by section boundaries (headers, double newlines)
        sections = self._split_into_sections(text)

        chunks = []
        chunk_index = 0

        for section in sections:
            if len(section) <= self.chunk_size:
                # Section fits in one chunk
                if section.strip():
                    chunks.append(Chunk(
                        chunk_id=f"{document_id}_chunk_{chunk_index}",
                        content=section.strip(),
                        chunk_index=chunk_index,
                        page_number=page_number,
                        section_heading=section_heading,
                        metadata={
                            **metadata,
                            "document_id": document_id,
                            "page": page_number,
                            "heading": section_heading,
                            "chunk_id": f"{document_id}_chunk_{chunk_index}",
                            "source": metadata.get("filename", ""),
                        },
                    ))
                    chunk_index += 1
            else:
                # Section needs further splitting
                sub_chunks = self._split_long_section(section)
                for sub in sub_chunks:
                    if sub.strip():
                        chunks.append(Chunk(
                            chunk_id=f"{document_id}_chunk_{chunk_index}",
                            content=sub.strip(),
                            chunk_index=chunk_index,
                            page_number=page_number,
                            section_heading=section_heading,
                            metadata={
                                **metadata,
                                "document_id": document_id,
                                "page": page_number,
                                "heading": section_heading,
                                "chunk_id": f"{document_id}_chunk_{chunk_index}",
                                "source": metadata.get("filename", ""),
                            },
                        ))
                        chunk_index += 1

        logger.debug("Text chunked", chunks=len(chunks), document_id=document_id)
        return chunks

    def _split_into_sections(self, text: str) -> list[str]:
        """Split text at natural section boundaries."""
        # Split on section headers (numbered or capitalized lines)
        section_pattern = r"\n(?=\d+\.\s+[A-Z]|\n[A-Z][A-Z\s]{5,}\n|\n---)"
        sections = re.split(section_pattern, text)
        return [s for s in sections if s.strip()]

    def _split_long_section(self, text: str) -> list[str]:
        """Split a long section into overlapping chunks at sentence boundaries."""
        # Split into sentences
        sentences = re.split(r"(?<=[.!?])\s+", text)

        chunks = []
        current_chunk = []
        current_length = 0

        for sentence in sentences:
            sentence_len = len(sentence)

            if current_length + sentence_len > self.chunk_size and current_chunk:
                # Emit current chunk
                chunks.append(" ".join(current_chunk))

                # Keep overlap
                overlap_text = " ".join(current_chunk)
                overlap_sentences = []
                overlap_len = 0
                for s in reversed(current_chunk):
                    if overlap_len + len(s) <= self.chunk_overlap:
                        overlap_sentences.insert(0, s)
                        overlap_len += len(s)
                    else:
                        break

                current_chunk = overlap_sentences
                current_length = overlap_len

            current_chunk.append(sentence)
            current_length += sentence_len

        # Emit remaining
        if current_chunk:
            chunks.append(" ".join(current_chunk))

        return chunks