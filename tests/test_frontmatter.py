from context_governance.frontmatter import parse_frontmatter


def test_parse_frontmatter_lists_and_booleans():
    text = """---
id: sample
include_in_registry: true
systems:
  - billing
  - scheduler
---
# Body
"""
    data = parse_frontmatter(text)
    assert data == {"id": "sample", "include_in_registry": True, "systems": ["billing", "scheduler"]}
