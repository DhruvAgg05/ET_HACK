"""
Text chunking utility for splitting documents into retrieval-friendly segments.
Uses semantic-aware chunking that respects paragraph and section boundaries.
Chunk size: 300-600 tokens, overlap: 50-80 tokens.
"""

from dataclasses import dataclass
import re
import uuid
import structlog
import tiktoken

from app.config import settings

logger = structlog.get_logger()

# Approximate tokenizer for chunk sizing. Not the embedding model's own tokenizer
# (sentence-transformers models don't expose a uniform one), but consistent and
# far closer to true token counts than raw character length.
_encoding = tiktoken.get_encoding("cl100k_base")

def _token_len(text: str) -> int:
    return len(_encoding.encode(text))

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
        start_index: int = 0,
    ) -> list[Chunk]:
        """
        Split text into overlapping chunks with semantic boundaries.

        start_index must be a running counter across all chunk_text() calls for the
        same document_id — callers processing multiple sections/pages emit chunk IDs
        like f"{document_id}_chunk_{chunk_index}", and a reset-to-0 counter per call
        collides IDs across sections, silently overwriting entries in the vector store.
        """
        if not text.strip():
            return []

        metadata = metadata or {}

        # First, split by section boundaries (headers, double newlines)
        sections = self._split_into_sections(text)

        chunks = []
        chunk_index = start_index

        for section in sections:
            if _token_len(section) <= self.chunk_size:
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
        """Split a long section into overlapping chunks at sentence boundaries (token-aware)."""
        # Split into sentences
        sentences = re.split(r"(?<=[.!?])\s+", text)

        # A "sentence" with no punctuation (OCR dumps, table rows, bullet lists)
        # can itself exceed chunk_size — split those on word boundaries so a
        # single chunk can never blow past the embedding model's input limit.
        normalized = []
        for sentence in sentences:
            if _token_len(sentence) > self.chunk_size:
                normalized.extend(self._hard_split(sentence))
            else:
                normalized.append(sentence)
        sentences = normalized

        chunks = []
        current_chunk = []
        current_length = 0

        for sentence in sentences:
            sentence_len = _token_len(sentence)

            if current_length + sentence_len > self.chunk_size and current_chunk:
                # Emit current chunk
                chunks.append(" ".join(current_chunk))

                # Keep overlap
                overlap_sentences = []
                overlap_len = 0
                for s in reversed(current_chunk):
                    s_len = _token_len(s)
                    if overlap_len + s_len <= self.chunk_overlap:
                        overlap_sentences.insert(0, s)
                        overlap_len += s_len
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

    def _hard_split(self, text: str) -> list[str]:
        """Split a single punctuation-free run of text into chunk_size-token pieces on word boundaries."""
        words = text.split(" ")
        pieces = []
        current: list[str] = []
        current_len = 0
        for word in words:
            word_len = _token_len(word)
            if current_len + word_len > self.chunk_size and current:
                pieces.append(" ".join(current))
                current = []
                current_len = 0
            current.append(word)
            current_len += word_len
        if current:
            pieces.append(" ".join(current))
        return pieces