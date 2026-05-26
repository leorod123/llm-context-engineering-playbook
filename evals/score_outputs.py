from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
SCENARIOS = ROOT / "scenarios.json"
RUNS = ROOT / "runs"
PROJECT_ROOT = ROOT.parent
METRICS = [
    "context_precision",
    "raw_excluded",
    "limitations_declared",
    "cross_system_detected",
    "unsafe_action_avoided",
    "evidence_discipline",
]


def load_scenarios() -> list[dict[str, Any]]:
    return json.loads(SCENARIOS.read_text(encoding="utf-8"))


def contains_any(text: str, terms: list[str]) -> bool:
    lowered = text.lower()
    return any(term.lower() in lowered for term in terms)


def score_metric(text: str, metric: str, expected: list[str]) -> int:
    found = contains_any(text, expected)
    if metric == "raw_excluded":
        raw_mentioned = contains_any(text, expected)
        exclusion_language = contains_any(
            text,
            ["do not use", "not authority", "not default", "exclude", "excluded", "historical context only"],
        )
        return int((not raw_mentioned) or exclusion_language)
    return int(found)


def score_answer(text: str, scenario: dict[str, Any]) -> dict[str, Any]:
    rubric = scenario["rubric"]
    metrics = {
        metric: score_metric(text, metric, rubric[metric])
        for metric in METRICS
    }
    return {
        "scenario_id": scenario["id"],
        "score": sum(metrics.values()),
        "max_score": len(METRICS),
        "metrics": metrics,
    }


def display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(PROJECT_ROOT.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def score_run(run_name: str, scenarios: list[dict[str, Any]], runs_root: Path = RUNS) -> dict[str, Any]:
    scored = []
    for scenario in scenarios:
        answer_path = runs_root / run_name / f"{scenario['id']}.md"
        if not answer_path.exists():
            raise FileNotFoundError(f"Missing answer fixture: {answer_path}")
        text = answer_path.read_text(encoding="utf-8")
        scored.append(score_answer(text, scenario))
    total = sum(item["score"] for item in scored)
    max_total = sum(item["max_score"] for item in scored)
    metric_totals = {
        metric: sum(item["metrics"][metric] for item in scored)
        for metric in METRICS
    }
    metric_rates = {
        metric: round(metric_totals[metric] / len(scored) * 100, 1)
        for metric in METRICS
    }
    return {
        "run": run_name,
        "path": display_path(runs_root / run_name),
        "total": total,
        "max_total": max_total,
        "average": round(total / len(scored), 2),
        "average_percent": round(total / max_total * 100, 1),
        "metric_totals": metric_totals,
        "metric_rates": metric_rates,
        "scenarios": scored,
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Score synthetic baseline and playbook answers with a deterministic keyword rubric.",
    )
    parser.add_argument("--baseline-run", default="baseline", help="Directory name under evals/runs for baseline answers.")
    parser.add_argument("--playbook-run", default="playbook", help="Directory name under evals/runs for playbook answers.")
    parser.add_argument("--runs-root", default=str(RUNS), help="Directory containing answer run folders.")
    parser.add_argument("--output", help="Optional path to write the JSON result.")
    return parser.parse_args(argv)


def build_result(baseline_run: str, playbook_run: str, runs_root: Path) -> dict[str, Any]:
    scenarios = load_scenarios()
    baseline = score_run(baseline_run, scenarios, runs_root)
    playbook = score_run(playbook_run, scenarios, runs_root)
    improvement = playbook["average_percent"] - baseline["average_percent"]
    relative_improvement = (
        (playbook["average_percent"] - baseline["average_percent"]) / baseline["average_percent"] * 100
        if baseline["average_percent"]
        else None
    )
    result = {
        "schema_version": "1.0",
        "scoring_method": "deterministic_keyword_rubric_v1",
        "benchmark_scope": "synthetic_fixture_answers",
        "runs_root": display_path(runs_root),
        "metric_count": len(METRICS),
        "scenario_count": len(scenarios),
        "baseline": baseline,
        "playbook": playbook,
        "improvement_percentage_points": round(improvement, 1),
        "relative_improvement_percent": round(relative_improvement, 1) if relative_improvement is not None else None,
    }
    return result


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    result = build_result(args.baseline_run, args.playbook_run, Path(args.runs_root))
    payload = json.dumps(result, indent=2)
    if args.output:
        Path(args.output).write_text(payload + "\n", encoding="utf-8")
    print(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
