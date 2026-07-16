"""Rule-based document classifier for AXIOM."""

from __future__ import annotations

import logging
import re
from typing import NamedTuple

from backend.app.models.schemas import DocumentMetadata, DocumentType


logger = logging.getLogger(__name__)


class ClassificationResult(NamedTuple):
    """Structured document classification result."""

    document_type: DocumentType
    confidence: float
    scores: dict[DocumentType, float]


class DocumentClassifier:
    """Weighted keyword classifier for industrial document types."""

    _RULES: dict[DocumentType, tuple[tuple[re.Pattern[str], float], ...]] = {
        DocumentType.WORK_ORDER: (
            (re.compile(r"\bwork\s*order\b|\bwo[-\s]?\d+\b", re.IGNORECASE), 3.0),
            (re.compile(r"\bcorrective maintenance\b|\bpm\b|\bcm\b", re.IGNORECASE), 1.5),
        ),
        DocumentType.SOP: (
            (re.compile(r"\bstandard operating procedure\b|\bsop\b", re.IGNORECASE), 3.0),
            (re.compile(r"\bprocedure\b|\bprecaution\b|\bpermit\b", re.IGNORECASE), 1.0),
        ),
        DocumentType.INSPECTION_REPORT: (
            (re.compile(r"\binspection\b|\binspector\b|\bnext due\b", re.IGNORECASE), 2.5),
            (re.compile(r"\bthickness\b|\bcorrosion\b|\bultrasonic\b", re.IGNORECASE), 1.5),
        ),
        DocumentType.INCIDENT_REPORT: (
            (re.compile(r"\bincident\b|\bnear miss\b|\broot cause\b", re.IGNORECASE), 2.5),
            (re.compile(r"\bcorrective action\b|\bimmediate cause\b", re.IGNORECASE), 1.5),
        ),
        DocumentType.REGULATORY_FILING: (
            (re.compile(r"\boisd\b|\bapi\b|\basme\b|\biso\b|\bregulation\b", re.IGNORECASE), 2.5),
            (re.compile(r"\bshall\b|\bmust\b|\brequirement\b|\bclause\b", re.IGNORECASE), 1.5),
        ),
        DocumentType.OEM_MANUAL: (
            (re.compile(r"\boem\b|\bmanufacturer\b|\bmanual\b", re.IGNORECASE), 2.5),
            (re.compile(r"\btroubleshooting\b|\bspecification\b|\bmaintenance interval\b", re.IGNORECASE), 1.5),
        ),
        DocumentType.PID_DRAWING: (
            (re.compile(r"\bp&?id\b|\bpiping and instrumentation\b", re.IGNORECASE), 3.0),
            (re.compile(r"\binstrument\b|\bline number\b|\bvalve\b", re.IGNORECASE), 1.0),
        ),
    }

    def __init__(self) -> None:
        """Initialize the classifier."""
        self._logger = logger.getChild(self.__class__.__name__)

    def classify(self, metadata: DocumentMetadata, text: str) -> ClassificationResult:
        """Classify a document based on file metadata and extracted text."""
        normalized_text = text or ""
        scores = {document_type: 0.0 for document_type in self._RULES}
        for document_type, rules in self._RULES.items():
            for pattern, weight in rules:
                matches = len(pattern.findall(normalized_text))
                if matches:
                    scores[document_type] += weight * min(matches, 5)

        file_name = metadata.file_name.lower()
        title = metadata.title.lower()
        for document_type in scores:
            token = document_type.value.replace("_", " ")
            if token in file_name or token in title:
                scores[document_type] += 1.25

        predicted_type = max(scores, key=scores.get, default=DocumentType.UNKNOWN)
        highest_score = scores.get(predicted_type, 0.0)
        confidence = min(1.0, highest_score / 6.0) if highest_score > 0 else 0.0

        if highest_score == 0.0:
            return ClassificationResult(DocumentType.UNKNOWN, 0.0, scores)
        return ClassificationResult(predicted_type, confidence, scores)
