"""OCR engine with image preprocessing for AXIOM."""

from __future__ import annotations

from io import BytesIO
import logging
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
from pytesseract import Output

from backend.app.config import Settings, get_settings
from backend.app.models.schemas import BoundingBox, ExtractedTextBlock, ExtractionMethod, IngestionIssue, OCRWord, SeverityLevel
from backend.app.services.ingestion.ingestion_types import ParsedDocument


logger = logging.getLogger(__name__)


class OCREngineError(RuntimeError):
    """Raised when OCR processing fails."""


class OCREngine:
    """Tesseract-based OCR with preprocessing and token-level confidence output."""

    def __init__(self, settings: Settings | None = None) -> None:
        """Initialize the OCR engine."""
        self._settings = settings or get_settings()
        self._logger = logger.getChild(self.__class__.__name__)
        pytesseract.pytesseract.tesseract_cmd = str(self._settings.tesseract_cmd)

    def extract_from_file(self, file_path: str | Path, *, page_number: int = 1) -> ParsedDocument:
        """Run OCR on an image file and return normalized text artifacts."""
        image = Image.open(file_path)
        return self.extract_from_image(image, page_number=page_number)

    def extract_from_bytes(self, image_bytes: bytes, *, page_number: int = 1) -> ParsedDocument:
        """Run OCR on image bytes and return normalized text artifacts."""
        image = Image.open(BytesIO(image_bytes))
        return self.extract_from_image(image, page_number=page_number)

    def extract_from_image(self, image: Image.Image, *, page_number: int = 1) -> ParsedDocument:
        """Run OCR on a PIL image with preprocessing and confidence scoring."""
        parsed = ParsedDocument(page_count=1)
        try:
            processed_image = self._preprocess_image(image)
            data = pytesseract.image_to_data(processed_image, output_type=Output.DICT)
        except Exception as exc:  # pragma: no cover - depends on external tesseract binary
            self._logger.exception("OCR extraction failed", extra={"page_number": page_number})
            raise OCREngineError("OCR extraction failed.") from exc

        width, height = processed_image.size
        words: list[OCRWord] = []
        line_fragments: dict[tuple[int, int, int], list[tuple[int, str]]] = {}
        line_boxes: dict[tuple[int, int, int], list[tuple[int, int, int, int]]] = {}

        for index, raw_text in enumerate(data["text"]):
            text = raw_text.strip()
            confidence_raw = data["conf"][index]
            if not text or confidence_raw in {"-1", -1}:
                continue
            confidence = max(0.0, min(1.0, float(confidence_raw) / 100.0))
            x = int(data["left"][index])
            y = int(data["top"][index])
            w = int(data["width"][index])
            h = int(data["height"][index])
            bbox = self._normalize_bbox(x, y, x + w, y + h, width, height)
            words.append(
                OCRWord(
                    text=text,
                    confidence=confidence,
                    page_number=page_number,
                    bounding_box=bbox,
                )
            )
            key = (
                int(data["block_num"][index]),
                int(data["par_num"][index]),
                int(data["line_num"][index]),
            )
            line_fragments.setdefault(key, []).append((x, text))
            line_boxes.setdefault(key, []).append((x, y, x + w, y + h))

        parsed.ocr_words = words
        parsed.text_blocks = self._build_text_blocks(line_fragments, line_boxes, page_number, width, height)

        if not parsed.text_blocks:
            parsed.issues.append(
                IngestionIssue(
                    code="ocr.no_text",
                    message="OCR completed but no text was recognized.",
                    severity=SeverityLevel.WARNING,
                    page_number=page_number,
                )
            )
        return parsed

    def _preprocess_image(self, image: Image.Image) -> Image.Image:
        """Apply deterministic preprocessing before OCR."""
        grayscale = image.convert("L")
        enhanced = ImageEnhance.Contrast(grayscale).enhance(2.0)
        sharpened = enhanced.filter(ImageFilter.SHARPEN)
        image_array = np.array(sharpened)
        denoised = cv2.fastNlMeansDenoising(image_array, h=10)
        _, thresholded = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return Image.fromarray(thresholded)

    def _build_text_blocks(
        self,
        line_fragments: dict[tuple[int, int, int], list[tuple[int, str]]],
        line_boxes: dict[tuple[int, int, int], list[tuple[int, int, int, int]]],
        page_number: int,
        width: int,
        height: int,
    ) -> list[ExtractedTextBlock]:
        """Aggregate OCR words into line-level text blocks."""
        blocks: list[ExtractedTextBlock] = []
        for key, fragments in sorted(line_fragments.items()):
            ordered = [text for _, text in sorted(fragments, key=lambda item: item[0])]
            text = " ".join(ordered).strip()
            if not text:
                continue
            coordinates = line_boxes[key]
            x0 = min(item[0] for item in coordinates)
            y0 = min(item[1] for item in coordinates)
            x1 = max(item[2] for item in coordinates)
            y1 = max(item[3] for item in coordinates)
            blocks.append(
                ExtractedTextBlock(
                    page_number=page_number,
                    text=text,
                    extraction_method=ExtractionMethod.OCR,
                    confidence=0.75,
                    bounding_box=self._normalize_bbox(x0, y0, x1, y1, width, height),
                )
            )
        return blocks

    @staticmethod
    def _normalize_bbox(x0: int, y0: int, x1: int, y1: int, width: int, height: int) -> BoundingBox:
        """Normalize image coordinates into 0..1 bounding boxes."""
        normalized_width = max(width, 1)
        normalized_height = max(height, 1)
        return BoundingBox(
            x_min=max(0.0, min(1.0, x0 / normalized_width)),
            y_min=max(0.0, min(1.0, y0 / normalized_height)),
            x_max=max(0.0, min(1.0, x1 / normalized_width)),
            y_max=max(0.0, min(1.0, y1 / normalized_height)),
        )
