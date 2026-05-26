from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .registry import registry_root


STATUS_SCORE = {"validated": 5, "implemented": 4, "active": 3, "draft": 1, "superseded": -10, "archived": -10, "rejected": -20}
AUTHORITY_SCORE = {"operational_contract": 5, "primary_architecture": 5, "validation_evidence": 4, "project_memory": 3, "audit_summary": 2, "secondary_semantic_context": 1, "historical_context": -4, "exploratory": -4}
VALIDATION_SCORE = {"runtime_validated": 5, "semantically_validated": 4, "implementation_validated": 3, "structurally_validated": 2, "unvalidated": 0}
SEMANTIC_SCORE = {"validated": 4, "partially_validated": 2, "unvalidated": 0, "invalid": -20}
BOT_SCORE = {"allowed": 10, "restricted": 1, "forbidden": -100}
EVIDENCE_SCORE = {"validated": 4, "partial": 2, "hypothesis": 0, "none": 0}


def load_registry(root: Path) -> dict[str, Any]:
    path = registry_root(root) / "knowledge_index.generated.json"
    if not path.exists():
        return {"documents": [], "generated_at": None}
    return json.loads(path.read_text(encoding="utf-8"))


def score_doc(doc: dict[str, Any], *, system: str | None, project_id: str | None, component: str | None, tag: str | None) -> tuple[int, list[str]]:
    score = 0
    matched: list[str] = []
    declared = doc.get("declared", {})

    if system and system in doc.get("systems", []):
        score += 40
        matched.append("system")
    if project_id and project_id == doc.get("project_id"):
        score += 50
        matched.append("project_id")
    if component and component in declared.get("components", []):
        score += 25
        matched.append("component")
    if tag and tag in declared.get("tags", []):
        score += 15
        matched.append("tag")

    score += STATUS_SCORE.get(doc.get("status"), 0)
    score += AUTHORITY_SCORE.get(doc.get("authority"), 0)
    score += VALIDATION_SCORE.get(doc.get("validation_state"), 0)
    score += SEMANTIC_SCORE.get(doc.get("semantic_status"), 0)
    score += BOT_SCORE.get(doc.get("bot_usage"), 0)
    score += EVIDENCE_SCORE.get(doc.get("evidence_status"), 0)
    return score, matched


def discover_context(root: Path, *, system: str | None = None, project_id: str | None = None, component: str | None = None, tag: str | None = None, limit: int = 5) -> dict[str, Any]:
    registry = load_registry(root)
    query_present = any([system, project_id, component, tag])
    ranked: list[tuple[int, dict[str, Any], list[str]]] = []

    for doc in registry.get("documents", []):
        if doc.get("bot_usage") == "forbidden":
            continue
        score, matched = score_doc(doc, system=system, project_id=project_id, component=component, tag=tag)
        if query_present and not matched:
            continue
        if score > 0:
            ranked.append((score, doc, matched))

    ranked.sort(key=lambda item: item[0], reverse=True)
    top = ranked[:limit]

    top_docs = [
        {
            "id": doc["id"],
            "title": doc["title"],
            "path": doc["path"],
            "score": score,
            "matched_on": matched,
            "authority": doc["authority"],
            "validation_state": doc["validation_state"],
            "semantic_status": doc["semantic_status"],
            "bot_usage": doc["bot_usage"],
            "evidence_status": doc["evidence_status"],
        }
        for score, doc, matched in top
    ]

    limitations: list[str] = []
    if not top_docs:
        limitations.append("no matching registry context found")
    if top_docs and not any(doc["bot_usage"] == "allowed" for doc in top_docs):
        limitations.append("selected context is restricted; use it with explicit limitations")
    if top_docs and not any(doc["semantic_status"] == "validated" for doc in top_docs):
        limitations.append("selected context is not fully semantically validated")

    return {
        "schema_version": "1.0",
        "query": {"system": system, "project_id": project_id, "component": component, "tag": tag},
        "registry_generated_at": registry.get("generated_at"),
        "top_docs": top_docs,
        "why_selected": [{"id": item["id"], "matched_on": item["matched_on"], "score": item["score"]} for item in top_docs],
        "context_required": query_present,
        "confidence": 0.8 if top_docs and not limitations else 0.45 if top_docs else 0.2,
        "limitations": limitations,
    }
