from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .registry import registry_root


def load_registry(root: Path) -> dict[str, Any]:
    path = registry_root(root) / "knowledge_index.generated.json"
    if not path.exists():
        return {
            "schema_version": "1.0",
            "documents": [],
            "issues": [
                {
                    "level": "error",
                    "path": "docs/_registry/knowledge_index.generated.json",
                    "code": "missing_registry",
                    "message": "Run the build command before validation.",
                }
            ],
        }
    return json.loads(path.read_text(encoding="utf-8"))


def validate_registry(root: Path) -> dict[str, Any]:
    registry = load_registry(root)
    issues = list(registry.get("issues", []))
    documents = registry.get("documents", [])

    ids = [doc.get("id") for doc in documents]
    duplicates = sorted({doc_id for doc_id in ids if ids.count(doc_id) > 1})
    for doc_id in duplicates:
        issues.append(
            {
                "level": "error",
                "path": "docs",
                "code": "duplicate_document_id",
                "message": f"Duplicate document id: {doc_id}",
            }
        )

    if documents and not any(doc.get("bot_usage") == "allowed" for doc in documents):
        issues.append(
            {
                "level": "diagnostic",
                "path": "docs",
                "code": "no_allowed_context",
                "message": "All indexed context is restricted or forbidden; agents must declare limitations.",
            }
        )

    for doc in documents:
        declared = doc.get("declared", {})
        if (
            doc.get("cross_system_impact") == "confirmed"
            and doc.get("authority") != "operational_contract"
            and not declared.get("required_contracts")
        ):
            issues.append(
                {
                    "level": "warning",
                    "path": doc.get("path", ""),
                    "code": "confirmed_impact_without_contracts",
                    "message": "Confirmed cross-system impact should declare required_contracts.",
                }
            )

    levels = {item["level"] for item in issues}
    status = "blocked" if "error" in levels else "approved_with_warning" if "warning" in levels else "approved"
    report = {
        "schema_version": "1.0",
        "status": status,
        "documents": len(documents),
        "issues": issues,
    }
    out = registry_root(root)
    out.mkdir(parents=True, exist_ok=True)
    (out / "validate_report.generated.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report
