"""
Neo4j client for knowledge graph operations.
Handles connection management, schema initialization, and CRUD operations.
"""

from neo4j import AsyncGraphDatabase, AsyncDriver
import structlog

from app.config import settings

logger = structlog.get_logger()

class Neo4jClient:
    """Async Neo4j client for the AXIOM knowledge graph."""

    def __init__(self):
        self._driver: AsyncDriver | None = None

    async def initialize(self):
        """Initialize connection and create schema constraints."""
        self._driver = AsyncGraphDatabase.driver(
            settings.neo4j_uri,
            auth=(settings.neo4j_user, settings.neo4j_password),
        )

        # Verify connectivity
        try:
            await self._driver.verify_connectivity()
            logger.info("Neo4j connected", uri=settings.neo4j_uri)
        except Exception as e:
            logger.error("Neo4j connection failed", error=str(e))
            self._driver = None
            return

        # Create schema constraints and indexes
        await self._create_schema()

    async def _create_schema(self):
        """Create uniqueness constraints and indexes for the knowledge graph."""
        constraints = [
            "CREATE CONSTRAINT IF NOT EXISTS FOR (e:Equipment) REQUIRE e.tag IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (d:Document) REQUIRE d.document_id IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (p:Procedure) REQUIRE p.procedure_id IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (w:WorkOrder) REQUIRE w.wo_id IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (i:Incident) REQUIRE i.incident_id IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (r:Regulation) REQUIRE r.standard_id IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (pe:Personnel) REQUIRE pe.name IS UNIQUE",
            # GraphRAG hierarchy nodes
            "CREATE CONSTRAINT IF NOT EXISTS FOR (pg:Page) REQUIRE pg.page_id IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (s:Section) REQUIRE s.section_id IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (c:Chunk) REQUIRE c.chunk_id IS UNIQUE",
        ]

        indexes = [
            "CREATE INDEX IF NOT EXISTS FOR (e:Equipment) ON (e.type)",
            "CREATE INDEX IF NOT EXISTS FOR (d:Document) ON (d.category)",
            "CREATE INDEX IF NOT EXISTS FOR (d:Document) ON (d.filename)",
            "CREATE INDEX IF NOT EXISTS FOR (w:WorkOrder) ON (w.status)",
            "CREATE INDEX IF NOT EXISTS FOR (c:Chunk) ON (c.document_id)",
            "CREATE INDEX IF NOT EXISTS FOR (pg:Page) ON (pg.document_id)",
        ]

        async with self._driver.session() as session:
            for query in constraints + indexes:
                try:
                    await session.run(query)
                except Exception as e:
                    logger.debug("Schema query skipped", query=query[:50], reason=str(e))

        logger.info("Neo4j schema initialized")

    async def close(self):
        """Close the Neo4j driver."""
        if self._driver:
            await self._driver.close()
            logger.info("Neo4j connection closed")

    async def execute_query(self, query: str, parameters: dict = None) -> list[dict]:
        """Execute a Cypher query and return results."""
        if not self._driver:
            logger.warning("Neo4j not connected, skipping query")
            return []

        async with self._driver.session() as session:
            result = await session.run(query, parameters or {})
            records = await result.data()
            return records

    async def create_node(self, label: str, properties: dict) -> str:
        """Create or merge a node in the graph."""
        # Use MERGE to avoid duplicates
        prop_string = ", ".join(f"{k}: ${k}" for k in properties.keys())
        query = f"MERGE (n:{label} {{{prop_string}}}) RETURN elementId(n) as id"

        async with self._driver.session() as session:
            result = await session.run(query, properties)
            record = await result.single()
            return record["id"] if record else ""

    async def create_relationship(
        self,
        source_label: str,
        source_key: str,
        source_value: str,
        target_label: str,
        target_key: str,
        target_value: str,
        relationship: str,
        properties: dict = None,
    ):
        """Create a relationship between two nodes."""
        props = ""
        params = {
            "source_value": source_value,
            "target_value": target_value,
        }

        if properties:
            prop_string = ", ".join(f"{k}: ${k}" for k in properties.keys())
            props = f" {{{prop_string}}}"
            params.update(properties)

        query = f"""
        MATCH (a:{source_label} {{{source_key}: $source_value}})
        MATCH (b:{target_label} {{{target_key}: $target_value}})
        MERGE (a)-[r:{relationship}{props}]->(b)
        RETURN type(r) as rel_type
        """

        async with self._driver.session() as session:
            await session.run(query, params)

    async def get_neighbors(
        self, node_label: str, node_key: str, node_value: str, depth: int = 2
    ) -> list[dict]:
        """Get neighboring nodes up to specified depth."""
        query = f"""
        MATCH path = (n:{node_label} {{{node_key}: $value}})-[*1..{depth}]-(m)
        RETURN
            labels(m)[0] as node_type,
            properties(m) as properties,
            [r in relationships(path) | type(r)] as relationships
        LIMIT 50
        """
        return await self.execute_query(query, {"value": node_value})

    async def search_nodes(self, search_term: str, limit: int = 20) -> list[dict]:
        """Full-text search across all node types."""
        query = """
        CALL {
            MATCH (n:Equipment) WHERE n.tag CONTAINS $term
            RETURN n, labels(n)[0] as label
            UNION
            MATCH (n:Document) WHERE n.filename CONTAINS $term
            RETURN n, labels(n)[0] as label
            UNION
            MATCH (n:Personnel) WHERE n.name CONTAINS $term
            RETURN n, labels(n)[0] as label
            UNION
            MATCH (n:Regulation) WHERE n.standard_id CONTAINS $term
            RETURN n, labels(n)[0] as label
        }
        RETURN label, properties(n) as props
        LIMIT $limit
        """
        return await self.execute_query(query, {"term": search_term, "limit": limit})

    async def get_equipment_context(self, equipment_tag: str) -> dict:
        """Get full context for a piece of equipment (all connected nodes)."""
        query = """
        MATCH (e:Equipment {tag: $tag})
        OPTIONAL MATCH (e)-[:HAS_WORK_ORDER]->(wo:WorkOrder)
        OPTIONAL MATCH (e)-[:GOVERNED_BY]->(r:Regulation)
        OPTIONAL MATCH (e)-[:INSPECTED_BY]->(i:Inspection)
        OPTIONAL MATCH (e)-[:INVOLVED_IN]->(inc:Incident)
        OPTIONAL MATCH (e)-[:HAS_PROCEDURE]->(p:Procedure)
        OPTIONAL MATCH (e)-[:REFERENCED_IN]->(d:Document)
        RETURN
            properties(e) as equipment,
            collect(DISTINCT properties(wo)) as work_orders,
            collect(DISTINCT properties(r)) as regulations,
            collect(DISTINCT properties(i)) as inspections,
            collect(DISTINCT properties(inc)) as incidents,
            collect(DISTINCT properties(p)) as procedures,
            collect(DISTINCT properties(d)) as documents
        """
        results = await self.execute_query(query, {"tag": equipment_tag})
        return results[0] if results else {}