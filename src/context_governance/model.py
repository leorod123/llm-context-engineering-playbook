from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any


REQUIRED_FIELDS = [
    "id",
    "title",
    "doc_type",
    "status",
    "created_at",
    "updated_at",
    "systems",
    "authority",
    "include_in_registry",
    "validation_state",
    "semantic_status",
    "bot_usage",
    "evidence_status",
]

DOC_TYPES = {
    "project",
    "audit",
    "architecture",
    "runbook",
    "decision",
    "validation",
    "maintenance",
    "incident",
    "contract",
    "reference",
}

STATUSES = {"draft", "active", "implemented", "validated", "superseded", "archived", "rejected"}
AUTHORITIES = {
    "primary_architecture",
    "operational_contract",
    "project_memory",
    "audit_summary",
    "validation_evidence",
    "historical_context",
    "secondary_semantic_context",
    "exploratory",
}
VALIDATION_STATES = {
    "unvalidated",
    "structurally_validated",
    "implementation_validated",
    "semantically_validated",
    "runtime_validated",
}
SEMANTIC_STATUSES = {"validated", "partially_validated", "unvalidated", "invalid"}
BOT_USAGE = {"allowed", "restricted", "forbidden"}
EVIDENCE_STATUSES = {"none", "hypothesis", "partial", "validated"}
CROSS_SYSTEM_IMPACT = {"none", "possible", "confirmed"}


@dataclass(frozen=True)
class Issue:
    level: str
    path: str
    code: str
    message: str

    def to_dict(self) -> dict[str, str]:
        return {
            "level": self.level,
            "path": self.path,
            "code": self.code,
            "message": self.message,
        }


def issue(level: str, root: Path, path: Path, code: str, message: str) -> Issue:
    try:
        rel = path.relative_to(root).as_posix()
    except ValueError:
        rel = path.as_posix()
    return Issue(level=level, path=rel, code=code, message=message)


def declared_fields(data: dict[str, Any]) -> dict[str, Any]:
    return {
        "components": data.get("components", []),
        "tags": data.get("tags", []),
        "related_contracts": data.get("related_contracts", []),
        "upstream_systems": data.get("upstream_systems", []),
        "downstream_systems": data.get("downstream_systems", []),
        "downstream_projects": data.get("downstream_projects", []),
        "required_contracts": data.get("required_contracts", []),
        "known_boundaries": data.get("known_boundaries", []),
    }
