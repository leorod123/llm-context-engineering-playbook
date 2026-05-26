from __future__ import annotations

from typing import Any


def parse_scalar(raw: str) -> Any:
    value = raw.strip()
    lower = value.lower()
    if lower == "true":
        return True
    if lower == "false":
        return False
    if lower == "null":
        return None
    if value in {"[]", "[ ]"}:
        return []
    return value.strip('"').strip("'")


def parse_frontmatter(text: str) -> dict[str, Any] | None:
    normalized = text.lstrip("\ufeff").replace("\r\n", "\n")
    if not normalized.startswith("---\n"):
        return None
    end = normalized.find("\n---\n", 4)
    if end == -1:
        return None

    block = normalized[4:end]
    result: dict[str, Any] = {}
    current_list: list[Any] | None = None

    for line in block.splitlines():
        if not line.strip() or line.strip().startswith("#"):
            continue
        if line.startswith("  - "):
            if current_list is not None:
                current_list.append(parse_scalar(line[4:]))
            continue
        if ":" not in line:
            current_list = None
            continue
        key, raw_value = line.split(":", 1)
        key = key.strip()
        value = raw_value.strip()
        if value == "":
            current_list = []
            result[key] = current_list
        else:
            result[key] = parse_scalar(value)
            current_list = None
    return result
