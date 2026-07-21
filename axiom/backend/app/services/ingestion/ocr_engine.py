"""
OCR Engine for scanned documents and images.
Uses PaddleOCR (primary, offline) with Tesseract as fallback.
"""

from __future__ import annotations
import io
from pathlib import Path
from dataclasses import dataclass
import numpy as np
import structlog

logger = structlog.get_logger()

# Try PaddleOCR first (preferred offline OCR)
try:
    from paddleocr import PaddleOCR
    HAS_PADDLE = True
except ImportError:
    HAS_PADDLE = False

# Tesseract as fallback
try:
    import pytesseract
    from PIL import Image, ImageFilter, ImageEnhance
    HAS_TESSERACT = True
except ImportError:
    HAS_TESSERACT = False

if not HAS_TESSERACT:
    try:
        from PIL import Image, ImageFilter, ImageEnhance
    except ImportError:
        pass

@dataclass
class OCRResult:
    text: str
    confidence: float
    page_number: int
    bounding_boxes: list[dict] | None = None

class OCREngine:
    """
    Performs OCR on images and scanned PDF pages.
    Priority: PaddleOCR (offline, accurate) > Tesseract (fallback)
    """

    def __init__(self, lang: str = "en"):
        self.lang = lang
        self._paddle_ocr = None

    def _get_paddle_ocr(self):
        """Lazy-load PaddleOCR model."""
        if self._paddle_ocr is None and HAS_PADDLE:
            self._paddle_ocr = PaddleOCR(
                use_angle_cls=True,
                lang=self.lang,
                use_gpu=False,
                show_log=False,
            )
            logger.info("PaddleOCR engine loaded")
        return self._paddle_ocr

    def ocr_image_bytes(self, image_bytes: bytes, page_number: int = 1) -> OCRResult:
        """Run OCR on raw image bytes."""
        image = Image.open(io.BytesIO(image_bytes))
        return self._process_image(image, page_number)

    def ocr_image_file(self, file_path: str | Path, page_number: int = 1) -> OCRResult:
        """Run OCR on an image file."""
        image = Image.open(str(file_path))
        return self._process_image(image, page_number)

    def ocr_pdf_page_image(self, page_pixmap_bytes: bytes, page_number: int) -> OCRResult:
        """Run OCR on a rendered PDF page (for scanned PDFs)."""
        image = Image.open(io.BytesIO(page_pixmap_bytes))
        return self._process_image(image, page_number)

    def _process_image(self, image: Image.Image, page_number: int) -> OCRResult:
        """Route to best available OCR engine."""
        if HAS_PADDLE:
            return self._paddle_ocr_process(image, page_number)
        elif HAS_TESSERACT:
            return self._tesseract_process(image, page_number)
        else:
            logger.warning("No OCR engine available")
            return OCRResult(text="", confidence=0.0, page_number=page_number)

    def _paddle_ocr_process(self, image: Image.Image, page_number: int) -> OCRResult:
        """Process image with PaddleOCR."""
        ocr = self._get_paddle_ocr()
        if ocr is None:
            return self._tesseract_process(image, page_number) if HAS_TESSERACT else OCRResult(
                text="", confidence=0.0, page_number=page_number
            )

        # Convert PIL to numpy array for PaddleOCR
        img_array = np.array(image.convert("RGB"))

        result = ocr.ocr(img_array, cls=True)

        text_parts = []
        confidences = []
        bounding_boxes = []

        if result and result[0]:
            for line in result[0]:
                bbox = line[0]
                text_info = line[1]
                text = text_info[0]
                confidence = text_info[1]

                text_parts.append(text)
                confidences.append(confidence)
                bounding_boxes.append({
                    "text": text,
                    "confidence": confidence,
                    "bbox": bbox,
                })

        full_text = " ".join(text_parts)
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0

        logger.info(
            "PaddleOCR completed",
            page=page_number,
            chars=len(full_text),
            confidence=f"{avg_confidence:.2f}",
        )

        return OCRResult(
            text=full_text,
            confidence=avg_confidence,
            page_number=page_number,
            bounding_boxes=bounding_boxes,
        )

    def _tesseract_process(self, image: Image.Image, page_number: int) -> OCRResult:
        """Fallback: Process image with Tesseract."""
        if not HAS_TESSERACT:
            return OCRResult(text="", confidence=0.0, page_number=page_number)

        processed = self._preprocess(image)

        ocr_data = pytesseract.image_to_data(
            processed, lang="eng", output_type=pytesseract.Output.DICT
        )

        text_parts = []
        confidences = []

        for i, word in enumerate(ocr_data["text"]):
            conf = int(ocr_data["conf"][i])
            if conf > 0 and word.strip():
                text_parts.append(word)
                confidences.append(conf)

        text = " ".join(text_parts)
        avg_confidence = (sum(confidences) / len(confidences) / 100.0) if confidences else 0.0

        logger.info(
            "Tesseract OCR completed (fallback)",
            page=page_number,
            chars=len(text),
            confidence=f"{avg_confidence:.2f}",
        )

        return OCRResult(
            text=text,
            confidence=avg_confidence,
            page_number=page_number,
        )

    def _preprocess(self, image: Image.Image) -> Image.Image:
        """Apply preprocessing steps to improve OCR accuracy."""
        if image.mode != "L":
            image = image.convert("L")

        width, height = image.size
        if width < 1000:
            scale = 1500 / width
            image = image.resize(
                (int(width * scale), int(height * scale)), Image.LANCZOS
            )

        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.5)

        image = image.filter(ImageFilter.SHARPEN)

        threshold = 140
        image = image.point(lambda x: 255 if x > threshold else 0, "1")

        return image

    def needs_ocr(self, text: str, page_image_bytes: bytes | None = None) -> bool:
        """Determine if a page needs OCR (too little extractable text)."""
        if len(text.strip()) < 50:
            return True

        printable_ratio = sum(1 for c in text if c.isprintable()) / max(len(text), 1)
        if printable_ratio < 0.8:
            return True

        return False