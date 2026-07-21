"""
Knowledge Graph Builder — populates Neo4j from extracted entities and relationships.
Maps extracted data to the industrial ontology.

Neo4j Schema (per GraphRAG pipeline):
    Document -[HAS_PAGE]-> Page
    Page -[HAS_SECTION]-> Section
    Section -[HAS_CHUNK]-> Chunk
    Chunk -[MENTIONS]-> Entity
    Entity -[RELATED_TO]-> Entity
    Table -[HAS_COLUMN]-> Column
"""

import structlog

from app.models.schemas import IngestedDocument, DocumentCategory
from app.services.knowledge_graph.neo4j_client import Neo4jClient

logger = structlog.get_logger()

class GraphBuilder:
    """Builds and updates the knowledge graph from ingested documents."""

    def __init__(self, neo4j_client: Neo4jClient):
        self.neo4j = neo4j_client

    async def populate_from_document(self, document: IngestedDocument):
        """
        Populate the knowledge graph from an ingested document.

        Creates the full hierarchy:
        Document → Page → Section → Chunk → Entity (with relationships)
        """
        logger.info(
            "Populating knowledge graph",
            document_id=document.document_id,
            entities=len(document.entities),
            relationships=len(document.relationships),
        )

        # 1. Create the Document node
        await self._create_document_node(document)

        # 2. Create Page and Chunk nodes with hierarchy
        await self._create_chunk_hierarchy(document)

        # 3. Create entity nodes and link to chunks
        await self._create_entity_nodes(document)

        # 4. Create relationships between entities
        await self._create_relationships(document)

        logger.info("Knowledge graph updated", document_id=document.document_id)

    async def _create_document_node(self, document: IngestedDocument):
        """Create a Document node in the graph."""
        await self.neo4j.create_node("Document", {
            "document_id": document.document_id,
            "filename": document.filename,
            "file_type": document.file_type.value,
            "category": document.category.value,
            "total_pages": document.total_pages,
            "ingested_at": document.ingested_at.isoformat(),
        })

    async def _create_chunk_hierarchy(self, document: IngestedDocument):
        """Create Page → Section → Chunk hierarchy linked to Document."""
        pages_created = set()
        sections_created = set()

        for chunk in document.chunks:
            page_num = chunk.page_number or 1
            page_id = f"{document.document_id}_page_{page_num}"

            # Create Page node if not exists
            if page_id not in pages_created:
                await self.neo4j.create_node("Page", {
                    "page_id": page_id,
                    "page_number": page_num,
                    "document_id": document.document_id,
                })
                # Document -[HAS_PAGE]-> Page
                await self.neo4j.create_relationship(
                    source_label="Document",
                    source_key="document_id",
                    source_value=document.document_id,
                    target_label="Page",
                    target_key="page_id",
                    target_value=page_id,
                    relationship="HAS_PAGE",
                    properties={"page_number": page_num},
                )
                pages_created.add(page_id)

            # Create Section node if section metadata available
            section_heading = chunk.metadata.get("section", "") or chunk.metadata.get("heading", "")
            section_id = f"{page_id}_section_{section_heading or 'default'}"

            if section_id not in sections_created:
                await self.neo4j.create_node("Section", {
                    "section_id": section_id,
                    "heading": section_heading,
                    "page_id": page_id,
                })
                # Page -[HAS_SECTION]-> Section
                await self.neo4j.create_relationship(
                    source_label="Page",
                    source_key="page_id",
                    source_value=page_id,
                    target_label="Section",
                    target_key="section_id",
                    target_value=section_id,
                    relationship="HAS_SECTION",
                    properties={},
                )
                sections_created.add(section_id)

            # Create Chunk node
            await self.neo4j.create_node("Chunk", {
                "chunk_id": chunk.chunk_id,
                "content": chunk.content[:500],  # Store abbreviated content
                "chunk_index": chunk.chunk_index,
                "document_id": document.document_id,
                "page_number": page_num,
            })
            # Section -[HAS_CHUNK]-> Chunk
            await self.neo4j.create_relationship(
                source_label="Section",
                source_key="section_id",
                source_value=section_id,
                target_label="Chunk",
                target_key="chunk_id",
                target_value=chunk.chunk_id,
                relationship="HAS_CHUNK",
                properties={"chunk_index": chunk.chunk_index},
            )

    async def _create_entity_nodes(self, document: IngestedDocument):
        """Create nodes for each extracted entity and link to chunks via MENTIONS."""
        for entity in document.entities:
            node_label = self._entity_type_to_label(entity.entity_type)
            if not node_label:
                continue

            # Create the entity node
            properties = self._build_entity_properties(entity)
            await self.neo4j.create_node(node_label, properties)

            # Link entity to document
            key_field = self._get_key_field(node_label)
            if key_field:
                await self.neo4j.create_relationship(
                    source_label=node_label,
                    source_key=key_field,
                    source_value=properties[key_field],
                    target_label="Document",
                    target_key="document_id",
                    target_value=document.document_id,
                    relationship="REFERENCED_IN",
                    properties={"confidence": entity.confidence},
                )

            # Link entity to relevant chunks via MENTIONS
            entity_value_lower = entity.value.lower()
            for chunk in document.chunks:
                if entity_value_lower in chunk.content.lower():
                    if key_field:
                        await self.neo4j.create_relationship(
                            source_label="Chunk",
                            source_key="chunk_id",
                            source_value=chunk.chunk_id,
                            target_label=node_label,
                            target_key=key_field,
                            target_value=properties[key_field],
                            relationship="MENTIONS",
                            properties={"confidence": entity.confidence},
                        )

    async def _create_relationships(self, document: IngestedDocument):
        """Create relationship edges between entity nodes."""
        for rel in document.relationships:
            source_label = self._guess_label_from_value(rel.source_entity)
            target_label = self._guess_label_from_value(rel.target_entity)

            if not source_label or not target_label:
                continue

            source_key = self._get_key_field(source_label)
            target_key = self._get_key_field(target_label)

            if source_key and target_key:
                try:
                    await self.neo4j.create_relationship(
                        source_label=source_label,
                        source_key=source_key,
                        source_value=rel.source_entity,
                        target_label=target_label,
                        target_key=target_key,
                        target_value=rel.target_entity,
                        relationship=rel.relationship_type,
                        properties={
                            "confidence": rel.confidence,
                            "source_document": document.document_id,
                        },
                    )
                except Exception as e:
                    logger.debug(
                        "Relationship creation skipped",
                        source=rel.source_entity,
                        target=rel.target_entity,
                        error=str(e),
                    )

    def _entity_type_to_label(self, entity_type: str) -> str | None:
        """Map entity type to Neo4j node label."""
        mapping = {
            "equipment": "Equipment",
            "personnel": "Personnel",
            "regulation": "Regulation",
            "parameter": "Parameter",
            "document_reference": "Document",
            "location": "Location",
            "organization": "Organization",
            "facility": "Location",
        }
        return mapping.get(entity_type)

    def _build_entity_properties(self, entity) -> dict:
        """Build node properties from an entity."""
        type_to_props = {
            "equipment": {"tag": entity.value, "context": entity.context[:200]},
            "personnel": {"name": entity.value},
            "regulation": {"standard_id": entity.value, "context": entity.context[:200]},
            "parameter": {"value": entity.value, "context": entity.context[:200]},
            "document_reference": {"document_id": entity.value},
            "location": {"name": entity.value},
            "organization": {"name": entity.value},
        }
        return type_to_props.get(entity.entity_type, {"value": entity.value})

    def _get_key_field(self, label: str) -> str | None:
        """Get the primary key field for a node label."""
        key_map = {
            "Equipment": "tag",
            "Personnel": "name",
            "Regulation": "standard_id",
            "Parameter": "value",
            "Document": "document_id",
            "Location": "name",
            "Organization": "name",
            "WorkOrder": "wo_id",
            "Incident": "incident_id",
            "Procedure": "procedure_id",
            "Inspection": "inspection_id",
        }
        return key_map.get(label)

    def _guess_label_from_value(self, value: str) -> str | None:
        """Guess the node label from the entity value format."""
        import re

        # Equipment tag pattern
        if re.match(r"^[A-Z]{1,4}-\d{2,5}[A-Z]?$", value):
            return "Equipment"
        # Work order
        if re.match(r"^WO[-\s]?\d{4,}$", value, re.IGNORECASE):
            return "WorkOrder"
        # Regulation
        if re.match(r"^(OISD|API|ISO|ASME|IS)[-\s]?\d+", value):
            return "Regulation"
        # If it looks like a person name
        if re.match(r"^[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+$", value):
            return "Personnel"

        return None