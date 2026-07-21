"""
Text cleaning and normalization for OCR and extracted text.
Removes noise, normalizes unicode, preserves structure.
"""

import re
import unicodedata
import structlog

try:
    import ftfy
    HAS_FTFY = True
except ImportError:
    HAS_FTFY = False

logger = structlog.get_logger()

class TextCleaner:
    """
    Cleans and normalizes text extracted from PDFs and OCR.

    Handles:
    - OCR noise removal
    - Unicode normalization
    - Whitespace cleanup
    - Header/footer removal
    - Table/code/list preservation
    """

    def __init__(self):
        # Patterns for boilerplate detection
        self._header_footer_patterns = [
            re.compile(r"^Page\s+\d+\s*(of\s+\d+)?$", re.IGNORECASE | re.MULTILINE),
            re.compile(r"^\d+\s*$", re.MULTILINE),  # Standalone page numbers
            re.compile(r"^(CONFIDENTIAL|DRAFT|INTERNAL)\s*$", re.IGNORECASE | re.MULTILINE),
            re.compile(r"^(©|Copyright).*$", re.IGNORECASE | re.MULTILINE),
        ]
        # OCR artifact patterns
        self._ocr_noise_patterns = [
            re.compile(r"[|]{3,}"),  # Repeated pipes
            re.compile(r"[_]{5,}"),  # Long underscores (form lines)
            re.compile(r"[~]{3,}"),  # Repeated tildes
            re.compile(r"[.]{5,}"),  # Long dot leaders
        ]

    def clean(self, text: str) -> str:
        """Full cleaning pipeline for extracted text."""
        if not text or not text.strip():
            return ""

        # Step 1: Fix unicode encoding issues
        text = self._fix_unicode(text)

        # Step 2: Normalize unicode characters
        text = self._normalize_unicode(text)

        # Step 3: Remove OCR artifacts
        text = self._remove_ocr_noise(text)

        # Step 4: Fix broken line wraps
        text = self._fix_line_wraps(text)

        # Step 5: Remove duplicate spaces
        text = self._normalize_whitespace(text)

        # Step 6: Remove headers/footers/boilerplate
        text = self._remove_boilerplate(text)

        # Step 7: Normalize bullets and lists
        text = self._normalize_bullets(text)

        # Step 8: Normalize punctuation
        text = self._normalize_punctuation(text)

        return text.strip()

    def _fix_unicode(self, text: str) -> str:
        """Fix mojibake and encoding issues using ftfy."""
        if HAS_FTFY:
            return ftfy.fix_text(text)
        return text

    def _normalize_unicode(self, text: str) -> str:
        """Normalize unicode to NFC form."""
        text = unicodedata.normalize("NFC", text)

        # Replace common unicode variants with ASCII equivalents
        replacements = {
            "\u2018": "'", "\u2019": "'",  # Smart quotes
            "\u201c": '"', "\u201d": '"',
            "\u2013": "-", "\u2014": "-",  # En/em dash
            "\u2026": "...",  # Ellipsis
            "\u00a0": " ",  # Non-breaking space
            "\ufeff": "",  # BOM
            "\u200b": "",  # Zero-width space
        }
        for old, new in replacements.items():
            text = text.replace(old, new)

        return text

    def _remove_ocr_noise(self, text: str) -> str:
        """Remove common OCR artifacts."""
        for pattern in self._ocr_noise_patterns:
            text = pattern.sub("", text)

        # Remove isolated single characters that are likely OCR errors
        # (but preserve single-letter words like "I", "a")
        text = re.sub(r"(?<!\w)([^IaA\s\d])\s(?!\w)", " ", text)

        return text

    def _fix_line_wraps(self, text: str) -> str:
        """Fix broken line wraps from PDF column extraction."""
        # Join lines that were broken mid-sentence (line ends without sentence-ending punctuation)
        lines = text.split("\n")
        fixed_lines = []
        i = 0

        while i < len(lines):
            line = lines[i]

            # Check if line continues on next line
            if (i + 1 < len(lines)
                and line.strip()
                and not line.strip().endswith((".", "!", "?", ":", ";", "|"))
                and not self._is_heading(line)
                and not self._is_list_item(lines[i + 1])
                and lines[i + 1].strip()
                and lines[i + 1][0:1].islower()):
                # Merge with next line
                fixed_lines.append(line.rstrip() + " " + lines[i + 1].lstrip())
                i += 2
            else:
                fixed_lines.append(line)
                i += 1

        return "\n".join(fixed_lines)

    def _normalize_whitespace(self, text: str) -> str:
        """Remove duplicate spaces and normalize whitespace."""
        # Multiple spaces to single
        text = re.sub(r"[ \t]+", " ", text)
        # Multiple blank lines to double newline
        text = re.sub(r"\n{3,}", "\n\n", text)
        # Remove trailing whitespace per line
        text = "\n".join(line.rstrip() for line in text.split("\n"))
        return text

    def _remove_boilerplate(self, text: str) -> str:
        """Remove headers, footers, and repeated boilerplate."""
        for pattern in self._header_footer_patterns:
            text = pattern.sub("", text)
        return text

    def _normalize_bullets(self, text: str) -> str:
        """Normalize various bullet point styles."""
        # Normalize bullet characters
        bullet_chars = ["•", "●", "○", "■", "□", "▪", "►", "▶", "◆", "◇"]
        for char in bullet_chars:
            text = text.replace(char, "- ")

        # Normalize numbered lists variations
        text = re.sub(r"^(\d+)\)\s", r"\1. ", text, flags=re.MULTILINE)

        return text

    def _normalize_punctuation(self, text: str) -> str:
        """Fix common punctuation issues from OCR."""
        # Fix spacing around punctuation
        text = re.sub(r"\s+([.,;:!?])", r"\1", text)
        text = re.sub(r"([.,;:!?])(\w)", r"\1 \2", text)
        return text

    def _is_heading(self, line: str) -> bool:
        """Check if a line appears to be a heading."""
        stripped = line.strip()
        if not stripped:
            return False
        # All caps line
        if stripped.isupper() and len(stripped) < 100:
            return True
        # Numbered heading
        if re.match(r"^\d+(\.\d+)*\s+[A-Z]", stripped):
            return True
        return False

    def _is_list_item(self, line: str) -> bool:
        """Check if a line is a list item."""
        stripped = line.strip()
        if re.match(r"^[-•*]\s", stripped):
            return True
        if re.match(r"^\d+[.)]\s", stripped):
            return True
        return False