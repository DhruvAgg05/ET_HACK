"""Async Neo4j client for AXIOM knowledge graph operations."""

from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable, Sequence
import logging
import re
from typing import Any, Literal

from neo4j import AsyncDriver, AsyncGraphDatabase, AsyncManagedTransaction
from neo4j.exceptions import DriverError, Neo4jError, ServiceUnavailable, SessionExpired, TransientError

from backend.app.config import Settings, get_settings


logger = logging.getLogger(__name__)

SAFE_CYPHER_NAME_PATTERN = re.compile(r"^[A-Za-z][A-Za-z0-9_]{0,63}$")
CypherAccessMode = Literal["READ", "WRITE"]


class Neo4jClientError(RuntimeError):
    """Raised when the Neo4j client cannot complete an operation."""


class Neo4jClient:
    """High-level async Neo4j client with pooling, retries, and typed helpers."""

    def __init__(self, settings: Settings | None = None) -> None:
        """Initialize the client with validated application settings."""
        self._settings = settings or get_settings()
        self._driver: AsyncDriver | None = None
        self._lock = asyncio.Lock()
        self._logger = logger.getChild(self.__class__.__name__)

    async def __aenter__(self) -> Neo4jClient:
        """Open the Neo4j connection when entering an async context."""
        await self.connect()
        return self

    async def __aexit__(self, exc_type: type[BaseException] | None, exc: BaseException | None, tb: Any) -> None:
        """Close the Neo4j driver on async context exit."""
        await self.close()

    async def connect(self) -> None:
        """Create the Neo4j driver and verify connectivity."""
        if self._driver is not None:
            return

        async with self._lock:
            if self._driver is not None:
                return

            config = self._settings.neo4j
            self._logger.info("Connecting to Neo4j", extra={"uri": config.uri, "database": config.database})
            driver = AsyncGraphDatabase.driver(
                config.uri,
                auth=(config.username, config.password.get_secret_value()),
                max_connection_pool_size=config.max_connection_pool_size,
                connection_timeout=config.connection_timeout_seconds,
                max_transaction_retry_time=config.max_transaction_retry_time_seconds,
            )
            try:
                await driver.verify_connectivity()
            except (Neo4jError, DriverError, OSError) as exc:
                await driver.close()
                self._logger.exception("Neo4j connectivity verification failed")
                raise Neo4jClientError("Failed to connect to Neo4j.") from exc

            self._driver = driver
            self._logger.info("Neo4j connection established")

    async def close(self) -> None:
        """Close the underlying Neo4j driver."""
        if self._driver is None:
            return

        async with self._lock:
            if self._driver is None:
                return
            await self._driver.close()
            self._driver = None
            self._logger.info("Neo4j connection closed")

    async def health_check(self) -> dict[str, Any]:
        """Return a health summary for the Neo4j connection."""
        await self.connect()
        await self.run_query("RETURN 1 AS ok", access_mode="READ")
        return {"status": "ok", "database": self._settings.neo4j.database}

    async def create_schema(self) -> None:
        """Create the core AXIOM graph constraints and indexes."""
        schema_statements = (
            "CREATE CONSTRAINT equipment_tag_unique IF NOT EXISTS FOR (n:Equipment) REQUIRE n.tag IS UNIQUE",
            "CREATE CONSTRAINT procedure_id_unique IF NOT EXISTS FOR (n:Procedure) REQUIRE n.id IS UNIQUE",
            "CREATE CONSTRAINT work_order_id_unique IF NOT EXISTS FOR (n:WorkOrder) REQUIRE n.id IS UNIQUE",
            "CREATE CONSTRAINT inspection_id_unique IF NOT EXISTS FOR (n:Inspection) REQUIRE n.id IS UNIQUE",
            "CREATE CONSTRAINT incident_id_unique IF NOT EXISTS FOR (n:Incident) REQUIRE n.id IS UNIQUE",
            "CREATE CONSTRAINT regulation_id_unique IF NOT EXISTS FOR (n:Regulation) REQUIRE n.id IS UNIQUE",
            "CREATE CONSTRAINT personnel_name_unique IF NOT EXISTS FOR (n:Personnel) REQUIRE n.name IS UNIQUE",
            "CREATE CONSTRAINT parameter_tag_unique IF NOT EXISTS FOR (n:Parameter) REQUIRE n.tag IS UNIQUE",
            "CREATE CONSTRAINT document_id_unique IF NOT EXISTS FOR (n:Document) REQUIRE n.id IS UNIQUE",
            "CREATE INDEX document_type_idx IF NOT EXISTS FOR (n:Document) ON (n.document_type)",
            "CREATE INDEX equipment_type_idx IF NOT EXISTS FOR (n:Equipment) ON (n.type)",
            "CREATE INDEX regulation_standard_idx IF NOT EXISTS FOR (n:Regulation) ON (n.standard)",
        )
        for statement in schema_statements:
            await self.run_query(statement, access_mode="WRITE")

    async def run_query(
        self,
        query: str,
        parameters: dict[str, Any] | None = None,
        *,
        access_mode: CypherAccessMode = "WRITE",
        timeout_seconds: float | None = None,
    ) -> list[dict[str, Any]]:
        """Execute an arbitrary Cypher query and return record data dictionaries."""
        parameters = parameters or {}

        async def operation() -> list[dict[str, Any]]:
            driver = await self._get_driver()
            async with driver.session(
                database=self._settings.neo4j.database,
                default_access_mode=access_mode,
            ) as session:
                result = await session.run(query, parameters=parameters, timeout=timeout_seconds)
                records = [record.data() async for record in result]
                await result.consume()
                return records

        try:
            return await self._with_retry(operation, "run_query")
        except (Neo4jError, DriverError, OSError) as exc:
            self._logger.exception("Neo4j query failed", extra={"query": query})
            raise Neo4jClientError("Neo4j query execution failed.") from exc

    async def upsert_node(
        self,
        label: str,
        identifier_key: str,
        identifier_value: Any,
        properties: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Merge a node by a unique identifier and update its properties."""
        safe_label = self._validate_cypher_name(label)
        safe_identifier_key = self._validate_cypher_name(identifier_key)
        query = (
            f"MERGE (n:`{safe_label}` {{{safe_identifier_key}: $identifier_value}}) "
            "SET n += $properties "
            "RETURN properties(n) AS node"
        )
        records = await self.run_query(
            query,
            parameters={"identifier_value": identifier_value, "properties": properties or {}},
            access_mode="WRITE",
        )
        return records[0]["node"] if records else {}

    async def bulk_upsert_nodes(
        self,
        label: str,
        identifier_key: str,
        items: Sequence[dict[str, Any]],
    ) -> int:
        """Bulk upsert nodes of the same label using UNWIND for efficiency."""
        if not items:
            return 0
        safe_label = self._validate_cypher_name(label)
        safe_identifier_key = self._validate_cypher_name(identifier_key)
        query = (
            "UNWIND $items AS item "
            f"MERGE (n:`{safe_label}` {{{safe_identifier_key}: item.identifier_value}}) "
            "SET n += item.properties "
            "RETURN count(n) AS processed_count"
        )
        payload = [
            {"identifier_value": item["identifier_value"], "properties": item.get("properties", {})}
            for item in items
        ]
        records = await self.run_query(query, {"items": payload}, access_mode="WRITE")
        return int(records[0]["processed_count"]) if records else 0

    async def upsert_relationship(
        self,
        source_label: str,
        source_key: str,
        source_value: Any,
        relationship_type: str,
        target_label: str,
        target_key: str,
        target_value: Any,
        properties: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Merge a relationship between two existing or newly created nodes."""
        safe_source_label = self._validate_cypher_name(source_label)
        safe_source_key = self._validate_cypher_name(source_key)
        safe_relationship_type = self._validate_cypher_name(relationship_type)
        safe_target_label = self._validate_cypher_name(target_label)
        safe_target_key = self._validate_cypher_name(target_key)
        query = (
            f"MERGE (source:`{safe_source_label}` {{{safe_source_key}: $source_value}}) "
            f"MERGE (target:`{safe_target_label}` {{{safe_target_key}: $target_value}}) "
            f"MERGE (source)-[rel:`{safe_relationship_type}`]->(target) "
            "SET rel += $properties "
            "RETURN properties(rel) AS relationship"
        )
        records = await self.run_query(
            query,
            {
                "source_value": source_value,
                "target_value": target_value,
                "properties": properties or {},
            },
            access_mode="WRITE",
        )
        return records[0]["relationship"] if records else {}

    async def get_node_by_property(self, label: str, key: str, value: Any) -> dict[str, Any] | None:
        """Fetch a single node by label and property value."""
        safe_label = self._validate_cypher_name(label)
        safe_key = self._validate_cypher_name(key)
        query = f"MATCH (n:`{safe_label}`) WHERE n.{safe_key} = $value RETURN properties(n) AS node LIMIT 1"
        records = await self.run_query(query, {"value": value}, access_mode="READ")
        return records[0]["node"] if records else None

    async def search_nodes(
        self,
        term: str,
        *,
        node_labels: Sequence[str] | None = None,
        limit: int = 20,
    ) -> list[dict[str, Any]]:
        """Search graph nodes by a free-text term across common identifier fields."""
        if limit < 1:
            raise ValueError("limit must be greater than zero.")

        labels = [self._validate_cypher_name(label) for label in node_labels] if node_labels else []
        label_filter = "labels(n)" if not labels else "[label IN labels(n) WHERE label IN $labels]"
        query = (
            "MATCH (n) "
            f"WHERE ({'size(' + label_filter + ') > 0' if labels else 'true'}) "
            "AND any(key IN keys(n) WHERE toLower(toString(n[key])) CONTAINS toLower($term)) "
            "RETURN elementId(n) AS node_id, labels(n) AS labels, properties(n) AS properties "
            "LIMIT $limit"
        )
        return await self.run_query(query, {"term": term, "labels": labels, "limit": limit}, access_mode="READ")

    async def get_equipment_context(self, equipment_tag: str) -> dict[str, Any] | None:
        """Return graph-backed context for a specific equipment tag."""
        query = """
        MATCH (equipment:Equipment {tag: $equipment_tag})
        OPTIONAL MATCH (equipment)-[:HAS_WORK_ORDER]->(wo:WorkOrder)
        OPTIONAL MATCH (equipment)-[:INVOLVED_IN]->(incident:Incident)
        OPTIONAL MATCH (equipment)-[:GOVERNED_BY]->(regulation:Regulation)
        OPTIONAL MATCH (equipment)-[:INSPECTED_BY]->(inspection:Inspection)
        OPTIONAL MATCH (wo)-[:REFERENCES]->(document:Document)
        RETURN
            properties(equipment) AS equipment,
            collect(DISTINCT properties(wo)) AS work_orders,
            collect(DISTINCT properties(incident)) AS incidents,
            collect(DISTINCT properties(regulation)) AS regulations,
            collect(DISTINCT properties(inspection)) AS inspections,
            collect(DISTINCT properties(document)) AS documents
        LIMIT 1
        """
        records = await self.run_query(query, {"equipment_tag": equipment_tag}, access_mode="READ")
        if not records:
            return None
        record = records[0]
        return {
            "equipment": record["equipment"],
            "work_orders": self._compact_graph_results(record["work_orders"]),
            "incidents": self._compact_graph_results(record["incidents"]),
            "regulations": self._compact_graph_results(record["regulations"]),
            "inspections": self._compact_graph_results(record["inspections"]),
            "documents": self._compact_graph_results(record["documents"]),
        }

    async def get_neighbors(self, node_label: str, key: str, value: Any, *, depth: int = 1, limit: int = 100) -> dict[str, Any]:
        """Traverse a node neighborhood up to a bounded depth."""
        if depth < 1 or depth > 5:
            raise ValueError("depth must be between 1 and 5.")
        if limit < 1 or limit > 10_000:
            raise ValueError("limit must be between 1 and 10000.")

        safe_label = self._validate_cypher_name(node_label)
        safe_key = self._validate_cypher_name(key)
        query = (
            f"MATCH (root:`{safe_label}`) WHERE root.{safe_key} = $value "
            f"MATCH path = (root)-[*1..{depth}]-(neighbor) "
            "WITH root, collect(DISTINCT neighbor)[0..$limit] AS nodes, collect(DISTINCT relationships(path)) AS rel_groups "
            "RETURN properties(root) AS root_node, "
            "[n IN nodes | {id: elementId(n), labels: labels(n), properties: properties(n)}] AS nodes, "
            "[rel_group IN rel_groups | [rel IN rel_group | {"
            "id: elementId(rel), type: type(rel), source: elementId(startNode(rel)), target: elementId(endNode(rel)), properties: properties(rel)"
            "}]] AS rel_groups"
        )
        records = await self.run_query(query, {"value": value, "limit": limit}, access_mode="READ")
        if not records:
            return {"root_node": None, "nodes": [], "edges": []}

        record = records[0]
        edges: list[dict[str, Any]] = []
        seen_edge_ids: set[str] = set()
        for group in record["rel_groups"]:
            for edge in group:
                edge_id = edge["id"]
                if edge_id not in seen_edge_ids:
                    seen_edge_ids.add(edge_id)
                    edges.append(edge)
        return {"root_node": record["root_node"], "nodes": record["nodes"], "edges": edges}

    async def get_graph_stats(self) -> dict[str, list[dict[str, Any]]]:
        """Return graph node and relationship counts grouped by type."""
        node_query = "MATCH (n) UNWIND labels(n) AS label RETURN label AS name, count(*) AS count ORDER BY count DESC"
        rel_query = "MATCH ()-[r]->() RETURN type(r) AS name, count(*) AS count ORDER BY count DESC"
        node_counts, relationship_counts = await asyncio.gather(
            self.run_query(node_query, access_mode="READ"),
            self.run_query(rel_query, access_mode="READ"),
        )
        return {"node_counts": node_counts, "relationship_counts": relationship_counts}

    async def delete_nodes_by_property(self, label: str, key: str, value: Any) -> int:
        """Delete nodes matching a label/property filter and detach relationships."""
        safe_label = self._validate_cypher_name(label)
        safe_key = self._validate_cypher_name(key)
        query = (
            f"MATCH (n:`{safe_label}`) WHERE n.{safe_key} = $value "
            "WITH collect(n) AS nodes, count(n) AS delete_count "
            "FOREACH (node IN nodes | DETACH DELETE node) "
            "RETURN delete_count"
        )
        records = await self.run_query(query, {"value": value}, access_mode="WRITE")
        return int(records[0]["delete_count"]) if records else 0

    async def _get_driver(self) -> AsyncDriver:
        """Return an initialized driver instance."""
        await self.connect()
        if self._driver is None:
            raise Neo4jClientError("Neo4j driver is not initialized.")
        return self._driver

    async def _with_retry(
        self,
        operation: Callable[[], Awaitable[Any]],
        operation_name: str,
    ) -> Any:
        """Retry transient Neo4j operations with bounded exponential backoff."""
        max_attempts = self._settings.neo4j.max_retry_attempts
        delay_seconds = 0.5
        for attempt in range(1, max_attempts + 1):
            try:
                return await operation()
            except (ServiceUnavailable, SessionExpired, TransientError, OSError) as exc:
                if attempt >= max_attempts:
                    self._logger.exception(
                        "Neo4j operation exhausted retries",
                        extra={"operation": operation_name, "attempt": attempt},
                    )
                    raise
                self._logger.warning(
                    "Retrying Neo4j operation after transient failure",
                    extra={"operation": operation_name, "attempt": attempt, "error": str(exc)},
                )
                await asyncio.sleep(delay_seconds)
                delay_seconds *= 2

    @staticmethod
    def _validate_cypher_name(value: str) -> str:
        """Validate a Cypher label, relationship type, or property name."""
        if not SAFE_CYPHER_NAME_PATTERN.fullmatch(value):
            raise ValueError(f"Invalid Cypher identifier: {value!r}")
        return value

    @staticmethod
    def _compact_graph_results(items: Sequence[dict[str, Any] | None]) -> list[dict[str, Any]]:
        """Remove null or empty graph projection results."""
        return [item for item in items if item]
