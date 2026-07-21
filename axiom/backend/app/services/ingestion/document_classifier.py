"""
Document classifier — determines the category of an industrial document
based on content analysis and filename patterns.
"""

import re
import structlog

from app.models.schemas import DocumentCategory

logger = structlog.get_logger()

class DocumentClassifier:
    """Classifies industrial documents into categories using keyword/pattern matching."""

    # Category indicators (keyword → category with weight)
    CATEGORY_SIGNALS = {
        DocumentCategory.PID: [
            (r"P&ID|piping.*instrument.*diagram|process flow diagram", 3),
            (r"line\s+list|equipment\s+list|instrument\s+index", 2),
            (r"control\s+valve|flow\s+transmitter|level\s+indicator", 1),
        ],
        DocumentCategory.WORK_ORDER: [
            (r"work\s+order|WO[-\s]?\d{4,}|maintenance\s+order", 3),
            (r"corrective\s+maintenance|preventive\s+maintenance|breakdown", 2),
            (r"spare\s+parts|man[-\s]?hours|downtime|repair", 1),
            (r"job\s+card|service\s+report|maintenance\s+record", 2),
        ],
        DocumentCategory.SOP: [
            (r"standard\s+operating\s+procedure|SOP|operating\s+instruction", 3),
            (r"work\s+instruction|safe\s+work\s+practice|JSA", 2),
            (r"step\s+\d+|precaution|PPE\s+required|safety\s+measure", 1),
            (r"procedure\s+no|rev(ision)?\.?\s*\d+|approved\s+by", 2),
        ],
        DocumentCategory.INSPECTION_REPORT: [
            (r"inspection\s+report|NDT\s+report|thickness\s+survey", 3),
            (r"corrosion|defect|finding|recommendation", 1),
            (r"ultrasonic|radiography|magnetic\s+particle|dye\s+penetrant", 2),
            (r"fitness\s+for\s+service|remaining\s+life|next\s+inspection", 2),
        ],
        DocumentCategory.INCIDENT_REPORT: [
            (r"incident\s+report|accident\s+report|near[-\s]?miss", 3),
            (r"root\s+cause\s+analysis|RCA|investigation", 2),
            (r"injury|fatality|fire|explosion|release|spill", 1),
            (r"corrective\s+action|preventive\s+action|CAPA", 2),
        ],
        DocumentCategory.OEM_MANUAL: [
            (r"operation\s+manual|maintenance\s+manual|OEM|manufacturer", 3),
            (r"installation\s+guide|commissioning|troubleshooting", 2),
            (r"spare\s+part.*list|exploded\s+view|wiring\s+diagram", 2),
            (r"model\s+no|serial\s+no|warranty", 1),
        ],
        DocumentCategory.REGULATORY: [
            (r"OISD|PESO|Factory\s+Act|BIS|statutory|compliance", 3),
            (r"regulation|standard|code\s+of\s+practice|guideline", 2),
            (r"shall\s+comply|mandatory|requirement|obligation", 1),
            (r"audit|certification|license|permit|approval", 1),
        ],
    }

    # Filename pattern signals
    FILENAME_PATTERNS = {
        DocumentCategory.PID: r"(?i)p&?id|pfd|process.*flow",
        DocumentCategory.WORK_ORDER: r"(?i)wo[-_]|work[-_]?order|maint",
        DocumentCategory.SOP: r"(?i)sop|procedure|oper.*instruct",
        DocumentCategory.INSPECTION_REPORT: r"(?i)insp|ndt|survey|thickness",
        DocumentCategory.INCIDENT_REPORT: r"(?i)incident|accident|near.?miss|rca",
        DocumentCategory.OEM_MANUAL: r"(?i)manual|oem|vendor|catalog",
        DocumentCategory.REGULATORY: r"(?i)oisd|regulation|standard|compliance",
    }

    def classify(self, text: str, filename: str = "") -> DocumentCategory:
        """Classify a document based on its content and filename."""
        scores: dict[DocumentCategory, float] = {cat: 0 for cat in DocumentCategory}

        # Score based on content patterns
        text_sample = text[:5000]  # Use first 5000 chars for classification
        for category, patterns in self.CATEGORY_SIGNALS.items():
            for pattern, weight in patterns:
                matches = len(re.findall(pattern, text_sample, re.IGNORECASE))
                scores[category] += matches * weight

        # Score based on filename
        for category, pattern in self.FILENAME_PATTERNS.items():
            if re.search(pattern, filename):
                scores[category] += 5  # Filename is a strong signal

        # Get highest scoring category
        best_category = max(scores, key=scores.get)
        best_score = scores[best_category]

        if best_score < 2:
            return DocumentCategory.GENERAL

        logger.info(
            "Document classified",
            category=best_category.value,
            score=best_score,
            filename=filename,
        )
        return best_category