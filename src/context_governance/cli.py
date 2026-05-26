from __future__ import annotations

import argparse
import json
from pathlib import Path

from .discover import discover_context
from .registry import write_registry
from .validate import validate_registry


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build, validate, and query LLM context governance docs.")
    sub = parser.add_subparsers(dest="command", required=True)

    build = sub.add_parser("build", help="Build docs/_registry/knowledge_index.generated.json")
    build.add_argument("--root", default=".", help="Repository or example root.")

    validate = sub.add_parser("validate", help="Validate the generated registry.")
    validate.add_argument("--root", default=".", help="Repository or example root.")

    discover = sub.add_parser("discover", help="Return small, explainable context from the registry.")
    discover.add_argument("--root", default=".", help="Repository or example root.")
    discover.add_argument("--system")
    discover.add_argument("--project-id")
    discover.add_argument("--component")
    discover.add_argument("--tag")
    discover.add_argument("--limit", type=int, default=5)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = Path(args.root)

    if args.command == "build":
        payload = write_registry(root)
        print(json.dumps({"status": "built", "docs": len(payload["documents"]), "issues": len(payload["issues"])}, indent=2))
        return 0

    if args.command == "validate":
        report = validate_registry(root)
        print(json.dumps(report, indent=2))
        return 0 if report["status"] != "blocked" else 1

    if args.command == "discover":
        payload = discover_context(
            root,
            system=args.system,
            project_id=args.project_id,
            component=args.component,
            tag=args.tag,
            limit=args.limit,
        )
        print(json.dumps(payload, indent=2))
        return 0

    return 2
