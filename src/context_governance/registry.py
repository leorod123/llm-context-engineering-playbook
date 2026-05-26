from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .frontmatter import parse_frontmatter
from .model import (
    AUTHORITIES,
    BOT_USAGE,
    CROSS_SYSTEM_IMPACT,
    DOC_TYPES,
    EVIDENCE_STATUSES,
    REQUIRED_FIELDS,
    SEMANTIC_STATUSES,
    STATUSES,
    VALIDATION_STATES,
    declared_fields,
    issue,
)


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def docs_root(root: Path) -> Path:
    return root / "docs"


def registry_root(root: Path) -> Path:
    return docs_root(root) / "_registry"


def markdown_paths(root: Path) -> list[Path]:
    docs = docs_root(root)
    if not docs.exists():
        return []
    paths: list[Path] = []
    for path in sorted(docs.rglob("*.md")):
        if path.name == "README.md":
            continue
        parts = {part.lower() for part in path.relative_to(docs).parts}
        if "raw" in parts or "_registry" in parts:
            continue
        paths.append(path)
    return paths


def source_hash(paths: list[Path], root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(paths):
        digest.update(path.relative_to(root).as_posix().encode("utf-8"))
        digest.update(path.read_bytes())
    return digest.hexdigest()


def validate_frontmatter(root: Path, path: Path, data: dict[str, Any]) -> list[dict[str, str]]:
    issues = []
    for field in REQUIRED_FIELDS:
        if field not in data:
            issues.append(issue("error", root, path, "missing_required_field", f"Missing required field: {field}").to_dict())

    if data.get("include_in_registry") is not True:
        issues.append(issue("diagnostic", root, path, "not_indexed", "Document does not opt into the registry.").to_dict())

    checks = [
        ("doc_type", DOC_TYPES),
        ("status", STATUSES),
        ("authority", AUTHORITIES),
        ("validation_state", VALIDATION_STATES),
        ("semantic_status", SEMANTIC_STATUSES),
        ("bot_usage", BOT_USAGE),
        ("evidence_status", EVIDENCE_STATUSES),
    ]
    for field, allowed in checks:
        value = data.get(field)
        if value is not None and value not in allowed:
            issues.append(issue("error", root, path, f"invalid_{field}", f"Unsupported {field}: {value}").to_dict())

    systems = data.get("systems")
    if systems is not None and not isinstance(systems, list):
        issues.append(issue("error", root, path, "systems_not_list", "systems must be a list.").to_dict())

    impact = data.get("cross_system_impact", "none")
    if impact not in CROSS_SYSTEM_IMPACT:
        issues.append(issue("error", root, path, "invalid_cross_system_impact", f"Unsupported cross_system_impact: {impact}").to_dict())

    if data.get("bot_usage") == "allowed":
        if data.get("semantic_status") != "validated":
            issues.append(issue("error", root, path, "allowed_without_validated_semantics", "bot_usage allowed requires semantic_status validated.").to_dict())
        if data.get("validation_state") not in {"semantically_validated", "runtime_validated"}:
            issues.append(issue("error", root, path, "allowed_without_strong_validation", "bot_usage allowed requires semantic or runtime validation.").to_dict())
        if data.get("evidence_status") != "validated":
            issues.append(issue("error", root, path, "allowed_without_validated_evidence", "bot_usage allowed requires validated evidence.").to_dict())

    if impact == "confirmed" and not data.get("known_boundaries"):
        issues.append(issue("warning", root, path, "confirmed_impact_without_boundaries", "Confirmed cross-system impact should declare known_boundaries.").to_dict())

    return issues


def document_record(root: Path, path: Path, data: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": data["id"],
        "title": data["title"],
        "path": path.relative_to(root).as_posix(),
        "project_id": data.get("project_id"),
        "doc_type": data["doc_type"],
        "status": data["status"],
        "authority": data["authority"],
        "systems": data["systems"],
        "validation_state": data["validation_state"],
        "semantic_status": data["semantic_status"],
        "bot_usage": data["bot_usage"],
        "evidence_status": data["evidence_status"],
        "cross_system_impact": data.get("cross_system_impact", "none"),
        "declared": declared_fields(data),
        "created_at": data["created_at"],
        "updated_at": data["updated_at"],
    }


def build_registry(root: Path) -> dict[str, Any]:
    root = root.resolve()
    paths = markdown_paths(root)
    documents: list[dict[str, Any]] = []
    issues: list[dict[str, str]] = []

    for path in paths:
        data = parse_frontmatter(path.read_text(encoding="utf-8"))
        if data is None:
            issues.append(issue("warning", root, path, "missing_frontmatter", "Markdown file has no frontmatter.").to_dict())
            continue
        issues.extend(validate_frontmatter(root, path, data))
        if data.get("include_in_registry") is True and not any(item["level"] == "error" and item["path"] == path.relative_to(root).as_posix() for item in issues):
            documents.append(document_record(root, path, data))

    by_system: dict[str, list[str]] = {}
    by_project: dict[str, list[str]] = {}
    for doc in documents:
        for system in doc["systems"]:
            by_system.setdefault(system, []).append(doc["id"])
        if doc.get("project_id"):
            by_project.setdefault(doc["project_id"], []).append(doc["id"])

    return {
        "schema_version": "1.0",
        "generated_at": now_iso(),
        "source_hash": source_hash(paths, root) if paths else None,
        "docs_scanned": len(paths),
        "documents": documents,
        "system_index": by_system,
        "project_index": by_project,
        "issues": issues,
    }


def write_registry(root: Path) -> dict[str, Any]:
    payload = build_registry(root)
    out = registry_root(root)
    out.mkdir(parents=True, exist_ok=True)
    (out / "knowledge_index.generated.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return payload
