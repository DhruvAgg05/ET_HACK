"""Pydantic schemas for the AXIOM platform.

This module centralizes the API and service-contract data models used across
document ingestion, retrieval, knowledge graph operations, and multi-agent
operations intelligence workflows.
"""

from __future__ import annotations

from datetime import UTC, datetime
from enum import Enum
import re
from typing import Annotated, Any
from uuid import UUID, uuid4

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    HttpUrl,
    field_validator,
    model_validator,
)


EQUIPMENT_TAG_PATTERN = re.compile(r"^[A-Z0-9][A-Z0-9\-_/.]{1,63}$")
REVISION_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,31}$")
CLAUSE_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9()./_ -]{0,63}$")
HEX_64_PATTERN = re.compile(r"^[a-fA-F0-9]{64}$")
SAFE_FILENAME_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,254}$")
GRAPH_KEY_PATTERN = re.compile(r"^[A-Za-z][A-Za-z0-9_]{0,63}$")

NonEmptyStr = Annotated[str, Field(min_length=1, strip_whitespace=True)]
ShortText = Annotated[str, Field(min_length=1, max_length=255, strip_whitespace=True)]
MediumText = Annotated[str, Field(min_length=1, max_length=2_000, strip_whitespace=True)]
LongText = Annotated[str, Field(min_length=1, max_length=20_000, strip_whitespace=True)]
EquipmentTagStr = Annotated[str, Field(min_length=2, max_length=64, strip_whitespace=True)]
UnitStr = Annotated[str, Field(min_length=1, max_length=32, strip_whitespace=True)]
PathStr = Annotated[str, Field(min_length=1, max_length=1_024, strip_whitespace=True)]
IdentifierStr = Annotated[str, Field(min_length=1, max_length=128, strip_whitespace=True)]


class AxiomBaseModel(BaseModel):
    """Base schema configuration shared across all AXIOM models."""

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
        str_strip_whitespace=True,
        validate_assignment=True,
        use_enum_values=False,
    )


class DocumentType(str, Enum):
    """Supported industrial document types."""

    PDF = "pdf"
    DOCX = "docx"
    IMAGE = "image"
    EMAIL = "email"
    WORK_ORDER = "work_order"
    SOP = "sop"
    INSPECTION_REPORT = "inspection_report"
    INCIDENT_REPORT = "incident_report"
    REGULATORY_FILING = "regulatory_filing"
    OEM_MANUAL = "oem_manual"
    PID_DRAWING = "pid_drawing"
    SPREADSHEET = "spreadsheet"
    TEXT = "text"
    UNKNOWN = "unknown"


class SourceSystem(str, Enum):
    """Origin system for ingested records and generated outputs."""

    MANUAL_UPLOAD = "manual_upload"
    EMAIL = "email"
    SHAREPOINT = "sharepoint"
    DMS = "dms"
    SCADA = "scada"
    ERP = "erp"
    CMMS = "cmms"
    GENERATED = "generated"
    API = "api"


class ProcessingStatus(str, Enum):
    """Lifecycle state for ingestion and downstream processing operations."""

    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    PARTIAL = "partial"


class ExtractionMethod(str, Enum):
    """Extraction strategy used to obtain structured information."""

    DIRECT_TEXT = "direct_text"
    OCR = "ocr"
    TABLE = "table"
    RULE_BASED = "rule_based"
    NER = "ner"
    LLM = "llm"
    VISION = "vision"
    HYBRID = "hybrid"


class EntityType(str, Enum):
    """Recognized entity categories in industrial content."""

    EQUIPMENT = "equipment"
    PROCEDURE = "procedure"
    WORK_ORDER = "work_order"
    INSPECTION = "inspection"
    INCIDENT = "incident"
    REGULATION = "regulation"
    PERSONNEL = "personnel"
    PARAMETER = "parameter"
    DOCUMENT = "document"
    LOCATION = "location"
    DATE = "date"
    PART = "part"
    ORGANIZATION = "organization"


class RelationshipType(str, Enum):
    """Supported knowledge-graph relationship types."""

    HAS_PROCEDURE = "HAS_PROCEDURE"
    HAS_WORK_ORDER = "HAS_WORK_ORDER"
    INSPECTED_BY = "INSPECTED_BY"
    INVOLVED_IN = "INVOLVED_IN"
    GOVERNED_BY = "GOVERNED_BY"
    MONITORS = "MONITORS"
    REFERENCES = "REFERENCES"
    CAUSED_BY = "CAUSED_BY"
    LED_TO = "LED_TO"
    PERFORMED = "PERFORMED"
    AUTHORED = "AUTHORED"
    LOCATED_AT = "LOCATED_AT"
    RELATED_TO = "RELATED_TO"


class QueryIntent(str, Enum):
    """Classified user-query intents for the copilot."""

    GENERAL_QA = "general_qa"
    SEARCH = "search"
    ROOT_CAUSE = "root_cause"
    MAINTENANCE_HISTORY = "maintenance_history"
    COMPLIANCE = "compliance"
    PREDICTIVE_MAINTENANCE = "predictive_maintenance"
    PROCEDURE_LOOKUP = "procedure_lookup"
    GRAPH_EXPLORATION = "graph_exploration"


class ConfidenceLevel(str, Enum):
    """Human-readable confidence tier."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class SeverityLevel(str, Enum):
    """Severity classification for alarms, incidents, and events."""

    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


class HealthStatus(str, Enum):
    """Equipment health state returned by the monitoring pipeline."""

    NORMAL = "normal"
    WARNING = "warning"
    CRITICAL = "critical"
    ANOMALY = "anomaly"


class ShiftType(str, Enum):
    """Operational shift buckets used in report naming and summaries."""

    DAY = "day"
    EVENING = "evening"
    NIGHT = "night"


class ReportCategory(str, Enum):
    """Persisted report categories exposed by the report API."""

    SENSOR_ANALYSIS = "sensor_analysis"
    FAULT_DIAGNOSIS = "fault_diagnosis"
    PREDICTIVE = "predictive"
    SHIFT_HANDOVER = "shift_handover"


class RiskLevel(str, Enum):
    """Risk classification for predictive maintenance outputs."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class ActionPriority(str, Enum):
    """Priority band for operational recommendations."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    IMMEDIATE = "immediate"


class NodeType(str, Enum):
    """Graph node labels used by the knowledge layer."""

    EQUIPMENT = "Equipment"
    PROCEDURE = "Procedure"
    WORK_ORDER = "WorkOrder"
    INSPECTION = "Inspection"
    INCIDENT = "Incident"
    REGULATION = "Regulation"
    PERSONNEL = "Personnel"
    PARAMETER = "Parameter"
    DOCUMENT = "Document"


class BoundingBox(AxiomBaseModel):
    """Normalized rectangular region within a page or image."""

    x_min: Annotated[float, Field(ge=0.0, le=1.0)]
    y_min: Annotated[float, Field(ge=0.0, le=1.0)]
    x_max: Annotated[float, Field(ge=0.0, le=1.0)]
    y_max: Annotated[float, Field(ge=0.0, le=1.0)]

    @model_validator(mode="after")
    def validate_bounds(self) -> BoundingBox:
        """Ensure the bounding box is well-formed."""
        if self.x_max <= self.x_min:
            raise ValueError("x_max must be greater than x_min.")
        if self.y_max <= self.y_min:
            raise ValueError("y_max must be greater than y_min.")
        return self


class DocumentMetadata(AxiomBaseModel):
    """Metadata describing an ingested or generated document."""

    document_id: UUID = Field(default_factory=uuid4)
    title: ShortText
    document_type: DocumentType
    source_system: SourceSystem
    revision: Annotated[str | None, Field(default=None, max_length=32)]
    source_reference: Annotated[str | None, Field(default=None, max_length=255)]
    file_name: Annotated[str, Field(min_length=1, max_length=255)]
    mime_type: Annotated[str, Field(min_length=3, max_length=127)]
    checksum_sha256: Annotated[str | None, Field(default=None, min_length=64, max_length=64)]
    language: Annotated[str, Field(default="en", min_length=2, max_length=16)]
    page_count: Annotated[int | None, Field(default=None, ge=1, le=100_000)]
    uploaded_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    effective_date: datetime | None = None
    tags: list[ShortText] = Field(default_factory=list, max_length=50)
    external_metadata: dict[str, Any] = Field(default_factory=dict)

    @field_validator("revision")
    @classmethod
    def validate_revision(cls, value: str | None) -> str | None:
        """Validate revision values against a safe revision pattern."""
        if value is None:
            return value
        if not REVISION_PATTERN.fullmatch(value):
            raise ValueError("revision must contain only letters, numbers, dots, underscores, or hyphens.")
        return value

    @field_validator("checksum_sha256")
    @classmethod
    def validate_checksum(cls, value: str | None) -> str | None:
        """Validate a SHA-256 checksum when provided."""
        if value is None:
            return value
        if not HEX_64_PATTERN.fullmatch(value):
            raise ValueError("checksum_sha256 must be a 64-character hexadecimal SHA-256 value.")
        return value.lower()

    @field_validator("file_name")
    @classmethod
    def validate_file_name(cls, value: str) -> str:
        """Reject unsafe file names."""
        if "/" in value or "\\" in value:
            raise ValueError("file_name must not contain directory separators.")
        return value

    @field_validator("tags")
    @classmethod
    def deduplicate_tags(cls, value: list[str]) -> list[str]:
        """Deduplicate tags while preserving order."""
        seen: set[str] = set()
        deduplicated: list[str] = []
        for item in value:
            normalized = item.casefold()
            if normalized not in seen:
                seen.add(normalized)
                deduplicated.append(item)
        return deduplicated


class OCRWord(AxiomBaseModel):
    """Single OCR token with geometry and confidence metadata."""

    text: NonEmptyStr
    confidence: Annotated[float, Field(ge=0.0, le=1.0)]
    page_number: Annotated[int, Field(ge=1, le=100_000)]
    bounding_box: BoundingBox


class ExtractedTextBlock(AxiomBaseModel):
    """A layout-aware text block extracted from a document page."""

    block_id: UUID = Field(default_factory=uuid4)
    page_number: Annotated[int, Field(ge=1, le=100_000)]
    text: LongText
    extraction_method: ExtractionMethod
    confidence: Annotated[float, Field(ge=0.0, le=1.0)]
    bounding_box: BoundingBox | None = None
    language: Annotated[str, Field(default="en", min_length=2, max_length=16)]


class ExtractedTable(AxiomBaseModel):
    """Structured table extracted from a source document."""

    table_id: UUID = Field(default_factory=uuid4)
    page_number: Annotated[int, Field(ge=1, le=100_000)]
    headers: list[ShortText] = Field(min_length=1, max_length=128)
    rows: list[list[str]] = Field(default_factory=list, max_length=10_000)
    extraction_method: ExtractionMethod
    confidence: Annotated[float, Field(ge=0.0, le=1.0)]
    bounding_box: BoundingBox | None = None

    @model_validator(mode="after")
    def validate_rows(self) -> ExtractedTable:
        """Ensure all table rows match the header width."""
        width = len(self.headers)
        if any(len(row) != width for row in self.rows):
            raise ValueError("All table rows must contain the same number of cells as headers.")
        return self


class ExtractedImage(AxiomBaseModel):
    """Metadata for an extracted image or rendered drawing snippet."""

    image_id: UUID = Field(default_factory=uuid4)
    page_number: Annotated[int, Field(ge=1, le=100_000)]
    content_type: Annotated[str, Field(min_length=3, max_length=127)]
    width: Annotated[int, Field(ge=1, le=20_000)]
    height: Annotated[int, Field(ge=1, le=20_000)]
    bounding_box: BoundingBox | None = None
    caption: Annotated[str | None, Field(default=None, max_length=500)]


class ExtractedEntity(AxiomBaseModel):
    """Structured entity recognized within industrial content."""

    entity_id: UUID = Field(default_factory=uuid4)
    entity_type: EntityType
    text: ShortText
    canonical_name: ShortText
    normalized_value: Annotated[str | None, Field(default=None, max_length=255)]
    confidence: Annotated[float, Field(ge=0.0, le=1.0)]
    page_number: Annotated[int | None, Field(default=None, ge=1, le=100_000)]
    source_span_start: Annotated[int | None, Field(default=None, ge=0)]
    source_span_end: Annotated[int | None, Field(default=None, ge=0)]
    extraction_method: ExtractionMethod
    attributes: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_offsets(self) -> ExtractedEntity:
        """Validate character span offsets when both are provided."""
        if self.source_span_start is not None and self.source_span_end is not None:
            if self.source_span_end <= self.source_span_start:
                raise ValueError("source_span_end must be greater than source_span_start.")
        return self


class ExtractedRelationship(AxiomBaseModel):
    """Relationship extracted between two recognized entities."""

    relationship_id: UUID = Field(default_factory=uuid4)
    relationship_type: RelationshipType
    source_entity_id: UUID
    target_entity_id: UUID
    confidence: Annotated[float, Field(ge=0.0, le=1.0)]
    evidence: MediumText
    extraction_method: ExtractionMethod

    @model_validator(mode="after")
    def validate_distinct_entities(self) -> ExtractedRelationship:
        """Ensure relationships do not point back to the same entity."""
        if self.source_entity_id == self.target_entity_id:
            raise ValueError("source_entity_id and target_entity_id must be different.")
        return self


class DocumentChunk(AxiomBaseModel):
    """Semantically meaningful text chunk used for indexing and retrieval."""

    chunk_id: UUID = Field(default_factory=uuid4)
    document_id: UUID
    content: LongText
    chunk_index: Annotated[int, Field(ge=0, le=1_000_000)]
    page_number: Annotated[int | None, Field(default=None, ge=1, le=100_000)]
    token_count: Annotated[int, Field(ge=1, le=100_000)]
    char_start: Annotated[int | None, Field(default=None, ge=0)]
    char_end: Annotated[int | None, Field(default=None, ge=0)]
    section_title: Annotated[str | None, Field(default=None, max_length=255)]
    embedding_model: Annotated[str | None, Field(default=None, max_length=255)]
    metadata: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_char_range(self) -> DocumentChunk:
        """Ensure chunk character offsets are well-formed."""
        if self.char_start is not None and self.char_end is not None:
            if self.char_end <= self.char_start:
                raise ValueError("char_end must be greater than char_start.")
        return self


class DocumentIngestionOptions(AxiomBaseModel):
    """Tunable options for the document ingestion pipeline."""

    enable_ocr: bool = True
    enable_table_extraction: bool = True
    enable_llm_extraction: bool = True
    generate_embeddings: bool = True
    persist_to_graph: bool = True
    max_chunk_tokens: Annotated[int, Field(default=512, ge=64, le=8_192)]
    overlap_tokens: Annotated[int, Field(default=64, ge=0, le=1_024)]

    @model_validator(mode="after")
    def validate_chunking(self) -> DocumentIngestionOptions:
        """Ensure chunk overlap remains smaller than chunk size."""
        if self.overlap_tokens >= self.max_chunk_tokens:
            raise ValueError("overlap_tokens must be smaller than max_chunk_tokens.")
        return self


class DocumentIngestionRequest(AxiomBaseModel):
    """Metadata-driven ingestion request for a single document."""

    metadata: DocumentMetadata
    storage_path: PathStr
    options: DocumentIngestionOptions = Field(default_factory=DocumentIngestionOptions)


class IngestionIssue(AxiomBaseModel):
    """Warning or error produced during ingestion."""

    code: IdentifierStr
    message: MediumText
    severity: SeverityLevel
    page_number: Annotated[int | None, Field(default=None, ge=1, le=100_000)]


class DocumentIngestionResult(AxiomBaseModel):
    """Outcome of processing a single document through the ingestion pipeline."""

    metadata: DocumentMetadata
    status: ProcessingStatus
    text_blocks: list[ExtractedTextBlock] = Field(default_factory=list)
    tables: list[ExtractedTable] = Field(default_factory=list)
    images: list[ExtractedImage] = Field(default_factory=list)
    ocr_words: list[OCRWord] = Field(default_factory=list)
    entities: list[ExtractedEntity] = Field(default_factory=list)
    relationships: list[ExtractedRelationship] = Field(default_factory=list)
    chunks: list[DocumentChunk] = Field(default_factory=list)
    issues: list[IngestionIssue] = Field(default_factory=list)
    processing_time_ms: Annotated[int, Field(ge=0, le=86_400_000)]


class BatchIngestionResponse(AxiomBaseModel):
    """Aggregated response for batch ingestion workflows."""

    job_id: UUID = Field(default_factory=uuid4)
    status: ProcessingStatus
    documents: list[DocumentIngestionResult] = Field(min_length=1, max_length=10_000)
    processed_count: Annotated[int, Field(ge=0)]
    failed_count: Annotated[int, Field(ge=0)]

    @model_validator(mode="after")
    def validate_counts(self) -> BatchIngestionResponse:
        """Ensure aggregated counters align with document results."""
        total = len(self.documents)
        if self.processed_count + self.failed_count != total:
            raise ValueError("processed_count + failed_count must equal the number of documents.")
        return self


class Citation(AxiomBaseModel):
    """Source citation attached to an answer or diagnosis."""

    document_id: UUID | None = None
    document_title: ShortText
    file_name: Annotated[str, Field(min_length=1, max_length=255)]
    page_number: Annotated[int | None, Field(default=None, ge=1, le=100_000)]
    paragraph_reference: Annotated[str | None, Field(default=None, max_length=64)]
    excerpt: Annotated[str | None, Field(default=None, max_length=1_000)]
    source_url: HttpUrl | None = None
    relevance_score: Annotated[float, Field(ge=0.0, le=1.0)]


class FollowUpSuggestion(AxiomBaseModel):
    """Suggested next-step question derived from graph context."""

    text: MediumText
    rationale: Annotated[str | None, Field(default=None, max_length=500)]


class KnowledgeCard(AxiomBaseModel):
    """Compact structured card surfaced alongside a conversational answer."""

    title: ShortText
    summary: MediumText
    equipment_tags: list[EquipmentTagStr] = Field(default_factory=list, max_length=10)
    key_facts: list[ShortText] = Field(default_factory=list, max_length=20)

    @field_validator("equipment_tags")
    @classmethod
    def normalize_equipment_tags(cls, value: list[str]) -> list[str]:
        """Normalize and validate equipment tags."""
        return [_normalize_equipment_tag(item) for item in value]


class QueryRequest(AxiomBaseModel):
    """Request model for natural-language copilot questions."""

    question: MediumText
    intent: QueryIntent = QueryIntent.GENERAL_QA
    top_k: Annotated[int, Field(default=8, ge=1, le=50)]
    include_graph_context: bool = True
    include_keyword_search: bool = True
    include_follow_ups: bool = True
    equipment_tags: list[EquipmentTagStr] = Field(default_factory=list, max_length=20)
    document_ids: list[UUID] = Field(default_factory=list, max_length=100)
    conversation_id: UUID | None = None

    @field_validator("equipment_tags")
    @classmethod
    def normalize_query_equipment_tags(cls, value: list[str]) -> list[str]:
        """Normalize equipment tags in a query request."""
        return [_normalize_equipment_tag(item) for item in value]


class SearchResult(AxiomBaseModel):
    """Ranked retrieval result returned by hybrid search."""

    chunk_id: UUID
    document_id: UUID
    document_title: ShortText
    page_number: Annotated[int | None, Field(default=None, ge=1, le=100_000)]
    content: MediumText
    score: Annotated[float, Field(ge=0.0, le=1.0)]
    retrieval_method: ExtractionMethod | QueryIntent | str
    metadata: dict[str, Any] = Field(default_factory=dict)


class QueryResponse(AxiomBaseModel):
    """Answer payload returned by the RAG copilot."""

    answer: LongText
    confidence: ConfidenceLevel
    confidence_score: Annotated[float, Field(ge=0.0, le=1.0)]
    citations: list[Citation] = Field(default_factory=list, max_length=100)
    supporting_results: list[SearchResult] = Field(default_factory=list, max_length=100)
    knowledge_cards: list[KnowledgeCard] = Field(default_factory=list, max_length=10)
    follow_up_suggestions: list[FollowUpSuggestion] = Field(default_factory=list, max_length=10)
    generated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    @model_validator(mode="after")
    def validate_confidence_and_sources(self) -> QueryResponse:
        """Require evidence for medium and high-confidence answers."""
        if self.confidence in {ConfidenceLevel.MEDIUM, ConfidenceLevel.HIGH} and not self.citations:
            raise ValueError("Medium and high-confidence responses must include at least one citation.")
        return self


class QuerySearchRequest(AxiomBaseModel):
    """Request model for retrieval-only search without generation."""

    query: MediumText
    top_k: Annotated[int, Field(default=10, ge=1, le=100)]
    document_ids: list[UUID] = Field(default_factory=list, max_length=100)
    equipment_tags: list[EquipmentTagStr] = Field(default_factory=list, max_length=20)

    @field_validator("equipment_tags")
    @classmethod
    def normalize_search_equipment_tags(cls, value: list[str]) -> list[str]:
        """Normalize search equipment tags."""
        return [_normalize_equipment_tag(item) for item in value]


class QuerySearchResponse(AxiomBaseModel):
    """Response model for retrieval-only search endpoints."""

    query: MediumText
    total_results: Annotated[int, Field(ge=0)]
    results: list[SearchResult] = Field(default_factory=list, max_length=100)

    @model_validator(mode="after")
    def validate_total_results(self) -> QuerySearchResponse:
        """Ensure total_results is not smaller than the page payload."""
        if self.total_results < len(self.results):
            raise ValueError("total_results cannot be smaller than len(results).")
        return self


class GraphNode(AxiomBaseModel):
    """Serialized graph node with typed label and properties."""

    node_id: IdentifierStr
    node_type: NodeType
    primary_name: ShortText
    properties: dict[str, Any] = Field(default_factory=dict)


class GraphEdge(AxiomBaseModel):
    """Serialized graph relationship between two nodes."""

    edge_id: IdentifierStr
    relationship_type: RelationshipType
    source_node_id: IdentifierStr
    target_node_id: IdentifierStr
    properties: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_edge_nodes(self) -> GraphEdge:
        """Prevent self-referential graph edges in API payloads."""
        if self.source_node_id == self.target_node_id:
            raise ValueError("source_node_id and target_node_id must be different.")
        return self


class GraphSearchRequest(AxiomBaseModel):
    """Request model for searching graph entities by a text term."""

    term: MediumText
    node_types: list[NodeType] = Field(default_factory=list, max_length=10)
    limit: Annotated[int, Field(default=20, ge=1, le=100)]


class GraphSearchResponse(AxiomBaseModel):
    """Response for graph entity search operations."""

    term: MediumText
    nodes: list[GraphNode] = Field(default_factory=list, max_length=100)
    total_matches: Annotated[int, Field(ge=0)]

    @model_validator(mode="after")
    def validate_total_matches(self) -> GraphSearchResponse:
        """Ensure total matches is consistent with the returned node set."""
        if self.total_matches < len(self.nodes):
            raise ValueError("total_matches cannot be smaller than len(nodes).")
        return self


class WorkOrderSummary(AxiomBaseModel):
    """Compact work-order summary for equipment context responses."""

    work_order_id: IdentifierStr
    title: ShortText
    status: ShortText
    finding_summary: Annotated[str | None, Field(default=None, max_length=1_000)]
    completed_at: datetime | None = None


class InspectionSummary(AxiomBaseModel):
    """Compact inspection summary for equipment context responses."""

    inspection_id: IdentifierStr
    inspection_type: ShortText
    inspection_date: datetime
    findings_summary: Annotated[str | None, Field(default=None, max_length=1_000)]
    next_due: datetime | None = None


class IncidentSummary(AxiomBaseModel):
    """Compact incident summary for equipment context responses."""

    incident_id: IdentifierStr
    severity: SeverityLevel
    root_cause_summary: Annotated[str | None, Field(default=None, max_length=1_000)]
    occurred_at: datetime


class RegulationSummary(AxiomBaseModel):
    """Compact regulation summary for compliance responses."""

    regulation_id: IdentifierStr
    standard: ShortText
    clause: Annotated[str, Field(min_length=1, max_length=64)]
    requirement_summary: MediumText

    @field_validator("clause")
    @classmethod
    def validate_clause(cls, value: str) -> str:
        """Validate regulation clause strings."""
        if not CLAUSE_PATTERN.fullmatch(value):
            raise ValueError("clause contains unsupported characters.")
        return value


class EquipmentContextResponse(AxiomBaseModel):
    """Detailed graph-backed context view for a specific equipment tag."""

    equipment_tag: EquipmentTagStr
    equipment_type: Annotated[str | None, Field(default=None, max_length=128)]
    location: Annotated[str | None, Field(default=None, max_length=255)]
    criticality: Annotated[str | None, Field(default=None, max_length=64)]
    work_orders: list[WorkOrderSummary] = Field(default_factory=list, max_length=1_000)
    inspections: list[InspectionSummary] = Field(default_factory=list, max_length=1_000)
    incidents: list[IncidentSummary] = Field(default_factory=list, max_length=1_000)
    regulations: list[RegulationSummary] = Field(default_factory=list, max_length=1_000)
    related_documents: list[DocumentMetadata] = Field(default_factory=list, max_length=1_000)

    @field_validator("equipment_tag")
    @classmethod
    def normalize_equipment_tag(cls, value: str) -> str:
        """Normalize equipment tag values."""
        return _normalize_equipment_tag(value)


class GraphNeighborsResponse(AxiomBaseModel):
    """Graph neighborhood traversal response."""

    root_node: GraphNode
    nodes: list[GraphNode] = Field(default_factory=list, max_length=5_000)
    edges: list[GraphEdge] = Field(default_factory=list, max_length=10_000)
    depth: Annotated[int, Field(ge=1, le=5)]


class GraphStatsBucket(AxiomBaseModel):
    """Count bucket keyed by graph label or relationship type."""

    name: IdentifierStr
    count: Annotated[int, Field(ge=0)]


class GraphStatsResponse(AxiomBaseModel):
    """Aggregate graph statistics for observability endpoints."""

    node_counts: list[GraphStatsBucket] = Field(default_factory=list, max_length=100)
    relationship_counts: list[GraphStatsBucket] = Field(default_factory=list, max_length=100)
    generated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class SensorReading(AxiomBaseModel):
    """Single sensor observation used by monitoring workflows."""

    equipment_tag: EquipmentTagStr
    parameter: ShortText
    value: float
    unit: UnitStr
    timestamp: datetime
    source_system: SourceSystem = SourceSystem.SCADA

    @field_validator("equipment_tag")
    @classmethod
    def normalize_sensor_equipment_tag(cls, value: str) -> str:
        """Normalize the equipment tag."""
        return _normalize_equipment_tag(value)


class SensorAnalysisRequest(AxiomBaseModel):
    """Request payload for anomaly detection and diagnosis workflows."""

    readings: list[SensorReading] = Field(min_length=1, max_length=100_000)


class AnomalyAlert(AxiomBaseModel):
    """Detected anomaly or threshold breach for a sensor signal."""

    equipment_tag: EquipmentTagStr
    parameter: ShortText
    status: HealthStatus
    severity: SeverityLevel
    observed_value: float
    unit: UnitStr
    threshold_value: float | None = None
    z_score: Annotated[float | None, Field(default=None, ge=0.0)]
    message: MediumText
    detected_at: datetime

    @field_validator("equipment_tag")
    @classmethod
    def normalize_alert_equipment_tag(cls, value: str) -> str:
        """Normalize equipment tag values."""
        return _normalize_equipment_tag(value)


class CorrectiveAction(AxiomBaseModel):
    """Action recommendation produced by a diagnosis or predictive workflow."""

    description: MediumText
    priority: ActionPriority
    recommended_by: ShortText
    sop_reference: Annotated[str | None, Field(default=None, max_length=128)]
    required_parts: list[ShortText] = Field(default_factory=list, max_length=100)


class RootCauseHypothesis(AxiomBaseModel):
    """Confidence-scored root-cause hypothesis for an anomaly."""

    cause: MediumText
    confidence: ConfidenceLevel
    confidence_score: Annotated[float, Field(ge=0.0, le=1.0)]
    evidence: list[Citation] = Field(default_factory=list, max_length=50)

    @model_validator(mode="after")
    def validate_evidence_requirement(self) -> RootCauseHypothesis:
        """Require evidence for medium and high-confidence hypotheses."""
        if self.confidence in {ConfidenceLevel.MEDIUM, ConfidenceLevel.HIGH} and not self.evidence:
            raise ValueError("Medium and high-confidence hypotheses must include evidence.")
        return self


class DiagnosisReport(AxiomBaseModel):
    """Per-equipment diagnostic assessment produced by the fault agent."""

    report_id: UUID = Field(default_factory=uuid4)
    equipment_tag: EquipmentTagStr
    status: HealthStatus
    alert: AnomalyAlert
    hypotheses: list[RootCauseHypothesis] = Field(min_length=1, max_length=20)
    recommended_actions: list[CorrectiveAction] = Field(default_factory=list, max_length=50)
    generated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    @field_validator("equipment_tag")
    @classmethod
    def normalize_diagnosis_equipment_tag(cls, value: str) -> str:
        """Normalize equipment tags in diagnosis reports."""
        return _normalize_equipment_tag(value)


class SensorHealthSummary(AxiomBaseModel):
    """Aggregate monitoring summary across a batch of sensor readings."""

    total_readings: Annotated[int, Field(ge=0)]
    affected_equipment: Annotated[int, Field(ge=0)]
    normal_count: Annotated[int, Field(ge=0)]
    warning_count: Annotated[int, Field(ge=0)]
    critical_count: Annotated[int, Field(ge=0)]
    anomaly_count: Annotated[int, Field(ge=0)]

    @model_validator(mode="after")
    def validate_summary_counts(self) -> SensorHealthSummary:
        """Ensure summary buckets do not exceed the total reading count."""
        total_classified = self.normal_count + self.warning_count + self.critical_count + self.anomaly_count
        if total_classified > self.total_readings:
            raise ValueError("Classified readings cannot exceed total_readings.")
        return self


class SensorAnalysisResponse(AxiomBaseModel):
    """Response payload for the sensor analysis pipeline."""

    alerts: list[AnomalyAlert] = Field(default_factory=list, max_length=10_000)
    diagnoses: list[DiagnosisReport] = Field(default_factory=list, max_length=10_000)
    health_summary: SensorHealthSummary
    actions_generated: Annotated[int, Field(ge=0)]
    report_saved_to: PathStr | None = None


class ParameterHistoryPoint(AxiomBaseModel):
    """Historical point for predictive maintenance trend analysis."""

    timestamp: datetime
    value: float


class CriticalLimit(AxiomBaseModel):
    """Critical threshold configuration for a monitored parameter."""

    parameter: ShortText
    limit_value: float
    unit: UnitStr
    direction: Annotated[str, Field(pattern="^(above|below)$")]


class PredictiveMaintenanceRequest(AxiomBaseModel):
    """Request payload for remaining useful life estimation."""

    equipment_tag: EquipmentTagStr
    parameter_history: dict[str, list[ParameterHistoryPoint]] = Field(min_length=1, max_length=100)
    critical_limits: list[CriticalLimit] = Field(min_length=1, max_length=100)
    equipment_type: ShortText
    hours_in_service: Annotated[float, Field(ge=0.0, le=10_000_000.0)]

    @field_validator("equipment_tag")
    @classmethod
    def normalize_pm_equipment_tag(cls, value: str) -> str:
        """Normalize equipment tags."""
        return _normalize_equipment_tag(value)

    @field_validator("parameter_history")
    @classmethod
    def validate_parameter_history(cls, value: dict[str, list[ParameterHistoryPoint]]) -> dict[str, list[ParameterHistoryPoint]]:
        """Require at least two time-ordered samples per parameter."""
        for parameter, points in value.items():
            if len(points) < 2:
                raise ValueError(f"parameter_history for '{parameter}' must contain at least two points.")
            timestamps = [point.timestamp for point in points]
            if timestamps != sorted(timestamps):
                raise ValueError(f"parameter_history for '{parameter}' must be sorted by timestamp.")
        return value


class RemainingUsefulLifeEstimate(AxiomBaseModel):
    """Remaining useful life output for a specific equipment asset."""

    equipment_tag: EquipmentTagStr
    estimated_days_to_failure: Annotated[float, Field(ge=0.0, le=100_000.0)]
    confidence: ConfidenceLevel
    confidence_interval_days: tuple[Annotated[float, Field(ge=0.0)], Annotated[float, Field(ge=0.0)]]
    risk_level: RiskLevel

    @field_validator("equipment_tag")
    @classmethod
    def normalize_rul_equipment_tag(cls, value: str) -> str:
        """Normalize equipment tags."""
        return _normalize_equipment_tag(value)

    @field_validator("confidence_interval_days")
    @classmethod
    def validate_confidence_interval(cls, value: tuple[float, float]) -> tuple[float, float]:
        """Ensure RUL confidence intervals are ordered."""
        lower, upper = value
        if upper < lower:
            raise ValueError("confidence_interval_days upper bound must be greater than or equal to lower bound.")
        return value


class MaintenanceRecommendation(AxiomBaseModel):
    """Optimized maintenance recommendation for a predicted failure mode."""

    action: MediumText
    recommended_date: datetime
    risk_level: RiskLevel
    rationale: MediumText
    estimated_cost_impact: Annotated[float | None, Field(default=None, ge=0.0)]


class PredictiveMaintenanceResponse(AxiomBaseModel):
    """Response payload for predictive maintenance endpoint workflows."""

    rul_estimates: list[RemainingUsefulLifeEstimate] = Field(min_length=1, max_length=100)
    recommendations: list[MaintenanceRecommendation] = Field(default_factory=list, max_length=100)
    risk_summary: MediumText
    report_saved_to: PathStr | None = None


class ShiftHandoverRequest(AxiomBaseModel):
    """Request payload for shift handover generation."""

    shift_start: datetime
    shift_end: datetime
    equipment_tags: list[EquipmentTagStr] = Field(default_factory=list, max_length=100)

    @field_validator("equipment_tags")
    @classmethod
    def normalize_handover_equipment_tags(cls, value: list[str]) -> list[str]:
        """Normalize equipment tags."""
        return [_normalize_equipment_tag(item) for item in value]

    @model_validator(mode="after")
    def validate_time_window(self) -> ShiftHandoverRequest:
        """Ensure the handover time window is valid and bounded."""
        if self.shift_end <= self.shift_start:
            raise ValueError("shift_end must be later than shift_start.")
        if (self.shift_end - self.shift_start).total_seconds() > 86_400:
            raise ValueError("Shift handover windows must not exceed 24 hours.")
        return self


class ShiftEvent(AxiomBaseModel):
    """Operational event included in handover synthesis."""

    event_id: UUID = Field(default_factory=uuid4)
    timestamp: datetime
    equipment_tag: EquipmentTagStr | None = None
    severity: SeverityLevel
    summary: MediumText
    action_taken: Annotated[str | None, Field(default=None, max_length=1_000)]
    source_system: SourceSystem

    @field_validator("equipment_tag")
    @classmethod
    def normalize_shift_event_equipment_tag(cls, value: str | None) -> str | None:
        """Normalize equipment tags when present."""
        if value is None:
            return value
        return _normalize_equipment_tag(value)


class HandoverItem(AxiomBaseModel):
    """Prioritized item for the incoming operations team."""

    priority: ActionPriority
    title: ShortText
    detail: MediumText
    equipment_tag: EquipmentTagStr | None = None

    @field_validator("equipment_tag")
    @classmethod
    def normalize_handover_item_equipment_tag(cls, value: str | None) -> str | None:
        """Normalize equipment tags when present."""
        if value is None:
            return value
        return _normalize_equipment_tag(value)


class ShiftHandoverReport(AxiomBaseModel):
    """Structured shift handover output for operational continuity."""

    report_id: UUID = Field(default_factory=uuid4)
    shift_type: ShiftType
    shift_start: datetime
    shift_end: datetime
    summary: MediumText
    critical_items: list[HandoverItem] = Field(default_factory=list, max_length=100)
    watch_items: list[HandoverItem] = Field(default_factory=list, max_length=100)
    events: list[ShiftEvent] = Field(default_factory=list, max_length=10_000)
    generated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    @model_validator(mode="after")
    def validate_report_window(self) -> ShiftHandoverReport:
        """Ensure the report window is chronological."""
        if self.shift_end <= self.shift_start:
            raise ValueError("shift_end must be later than shift_start.")
        return self


class ShiftHandoverResponse(AxiomBaseModel):
    """API response wrapper for shift handover generation."""

    summary: MediumText
    critical_items: list[HandoverItem] = Field(default_factory=list, max_length=100)
    watch_items: list[HandoverItem] = Field(default_factory=list, max_length=100)
    formatted_report: ShiftHandoverReport
    report_saved_to: PathStr | None = None


class ReportRecord(AxiomBaseModel):
    """Metadata entry describing a persisted agent report."""

    filename: Annotated[str, Field(min_length=1, max_length=255)]
    category: ReportCategory
    equipment: Annotated[str, Field(min_length=1, max_length=128)]
    shift: ShiftType
    status: ShortText
    path: PathStr
    created_at: datetime | None = None

    @field_validator("filename")
    @classmethod
    def validate_filename(cls, value: str) -> str:
        """Validate a report file name."""
        if not SAFE_FILENAME_PATTERN.fullmatch(value):
            raise ValueError("filename contains unsupported characters.")
        if not value.endswith(".json"):
            raise ValueError("filename must end with .json.")
        return value


class ReportListResponse(AxiomBaseModel):
    """Response model for report listing endpoints."""

    total_reports: Annotated[int, Field(ge=0)]
    reports: list[ReportRecord] = Field(default_factory=list, max_length=10_000)

    @model_validator(mode="after")
    def validate_report_total(self) -> ReportListResponse:
        """Ensure the report total is consistent with the returned collection."""
        if self.total_reports < len(self.reports):
            raise ValueError("total_reports cannot be smaller than len(reports).")
        return self


class ReportFilterParams(AxiomBaseModel):
    """Validated filter parameters for browsing persisted reports."""

    category: ReportCategory | None = None
    equipment: EquipmentTagStr | None = None
    status: Annotated[str | None, Field(default=None, min_length=1, max_length=64)]

    @field_validator("equipment")
    @classmethod
    def normalize_filter_equipment(cls, value: str | None) -> str | None:
        """Normalize equipment filter values."""
        if value is None:
            return value
        return _normalize_equipment_tag(value)


class ReportPathParams(AxiomBaseModel):
    """Validated path parameters for retrieving a persisted report."""

    category: ReportCategory
    filename: Annotated[str, Field(min_length=1, max_length=255)]

    @field_validator("filename")
    @classmethod
    def validate_report_path_filename(cls, value: str) -> str:
        """Validate a safe report retrieval file name."""
        if not SAFE_FILENAME_PATTERN.fullmatch(value):
            raise ValueError("filename contains unsupported characters.")
        if not value.endswith(".json"):
            raise ValueError("filename must end with .json.")
        return value


class HealthCheckResponse(AxiomBaseModel):
    """Simple service health response."""

    service: ShortText
    status: ShortText
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    version: Annotated[str | None, Field(default=None, max_length=32)]


def _normalize_equipment_tag(value: str) -> str:
    """Normalize and validate industrial equipment tags."""
    normalized = value.strip().upper()
    if not EQUIPMENT_TAG_PATTERN.fullmatch(normalized):
        raise ValueError(
            "equipment_tag must be 2-64 characters and contain only letters, numbers, hyphens, underscores, slashes, or periods."
        )
    return normalized
