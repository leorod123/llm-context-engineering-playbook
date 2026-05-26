from pathlib import Path

from context_governance.discover import discover_context
from context_governance.registry import write_registry
from context_governance.validate import validate_registry


ROOT = Path(__file__).resolve().parents[1] / "examples" / "synthetic_saas"


def test_example_build_validate_discover():
    registry = write_registry(ROOT)
    assert registry["documents"]
    assert all("/raw/" not in doc["path"] for doc in registry["documents"])

    report = validate_registry(ROOT)
    assert report["status"] in {"approved", "approved_with_warning"}

    discovery = discover_context(ROOT, system="billing")
    assert discovery["top_docs"]
    assert "restricted" in " ".join(discovery["limitations"])
