from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum

# --- Document Models ---

class DocumentType(str, Enum):
    PDF = "pdf"
    DOCX = "docx"
    XLSX = "xlsx"
    IMAGE = "image"
    EMAIL = "email"
    UNKNOWN = "unknown"

class DocumentCategory(str, Enum):
    PID = "p&id"
    WORK_ORDER = "work_order"
    SOP = "sop"
    INSPECTION_REPORT = "inspection_report"
    INCIDENT_REPORT = "incident_report"
    OEM_MANUAL = "oem_manual"
    REGULATORY = "regulatory"
    GENERAL = "general"

class ExtractedEntity(BaseModel):
    entity_type: str  # equipment, personnel, date, parameter, regulation, location
    value: str
    confidence: float = Field(ge=0, le=1)
    source_page: Optional[int] = None
    context: Optional[str] = None

class ExtractedRelationship(BaseModel):
    source_entity: str
    relationship_type: str
    target_entity: str
    confidence: float = Field(ge=0, le=1)
    source_context: Optional[str] = None

class DocumentChunk(BaseModel):
    chunk_id: str
    document_id: str
    content: str
    page_number: Optional[int] = None
    chunk_index: int
    metadata: dict = {}

class IngestedDocument(BaseModel):
    document_id: str
    filename: str
    file_type: DocumentType
    category: DocumentCategory
    total_pages: int = 0
    extracted_text: str
    chunks: list[DocumentChunk] = []
    entities: list[ExtractedEntity] = []
    relationships: list[ExtractedRelationship] = []
    ingested_at: datetime = Field(default_factory=datetime.utcnow)

# --- Query Models ---

class QueryRequest(BaseModel):
    question: str
    filters: Optional[dict] = None
    top_k: int = Field(default=5, ge=1, le=20)
    include_graph_context: bool = True

class RetrievedContext(BaseModel):
    chunk_id: str
    document_id: str
    filename: str
    content: str
    page_number: Optional[int] = None
    relevance_score: float
    source_type: str  # "vector", "graph", "keyword"

class QueryResponse(BaseModel):
    answer: str
    confidence: str  # "high", "medium", "low"
    sources: list[RetrievedContext]
    related_entities: list[dict] = []
    suggested_followups: list[str] = []

# --- Graph Models ---

class GraphNode(BaseModel):
    node_id: str
    node_type: str
    properties: dict

class GraphEdge(BaseModel):
    source_id: str
    target_id: str
    relationship: str
    properties: dict = {}