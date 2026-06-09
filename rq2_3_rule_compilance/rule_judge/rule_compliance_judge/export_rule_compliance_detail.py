"""
Export per-commit compliance judgment details for one rule to a txt file.

Commits are ordered by relative_delta descending (+5 .. 0 .. -5), i.e. earliest to latest.
relative_delta convention (matches main_branch_commits / git rev-list):
  positive = earlier in history than the rule commit; negative = later.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List, Optional

SCRIPT_DIR = Path(__file__).resolve().parent
RULE_JUDGE_DIR = SCRIPT_DIR.parent
DEFAULT_RESULTS = SCRIPT_DIR / "rule_compliance_outputs" / "rule_compliance_results.json"
DEFAULT_DETECT_RULES = RULE_JUDGE_DIR / "detect_rules.json"
DEFAULT_RULE_ID = "E7_08"

RULE_INFO_FIELDS = [
    "rule_content",
    "change_type",
    "first_level",
    "second_level",
    "detection_targets",
    "detection_logic",
]


def load_json_list(path: Path) -> List[Dict[str, Any]]:
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError(f"JSON must be a list: {path}")
    return [row for row in data if isinstance(row, dict)]


def find_rule_info(detect_rules: List[Dict[str, Any]], rule_id: str) -> Dict[str, Any]:
    for rule in detect_rules:
        if rule.get("rule_id") == rule_id:
            return rule
    raise ValueError(f"rule_id not found in detect_rules.json: {rule_id}")


def build_relative_position_text(delta: int) -> str:
    if delta == 0:
        return "same_as_rule_commit (distance=0)"
    if delta > 0:
        return f"before_rule_commit (distance={delta})"
    return f"after_rule_commit (distance={abs(delta)})"


def describe_time_relation(delta: Optional[int]) -> str:
    if not isinstance(delta, int):
        return "unknown"
    if delta == 0:
        return "rule commit"
    if delta > 0:
        return f"{delta} commit(s) earlier than rule commit"
    return f"{abs(delta)} commit(s) later than rule commit"


def filter_rule_results(
    results: List[Dict[str, Any]], rule_id: str
) -> List[Dict[str, Any]]:
    rows = [row for row in results if row.get("rule_id") == rule_id]
    if not rows:
        raise ValueError(f"rule_id not found in results: {rule_id}")
    return sorted(rows, key=lambda row: row.get("relative_delta", 0), reverse=True)


def format_json_block(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2)


def format_rule_info_section(rule_info: Dict[str, Any], rule_id: str) -> str:
    lines = [
        "=" * 80,
        f"Rule: {rule_id}",
        "=" * 80,
        "",
    ]
    for field in RULE_INFO_FIELDS:
        value = rule_info.get(field, "")
        lines.append(f"{field}:")
        lines.append(str(value))
        lines.append("")
    return "\n".join(lines)


def format_commit_section(row: Dict[str, Any], index: int) -> str:
    relative_delta = row.get("relative_delta")
    delta_label = f"{relative_delta:+d}" if isinstance(relative_delta, int) else str(relative_delta)
    position_text = (
        build_relative_position_text(relative_delta)
        if isinstance(relative_delta, int)
        else str(row.get("relative_position", ""))
    )
    lines = [
        "-" * 80,
        f"[{index}] commit_id: {row.get('commit_id', '')}",
        f"relative_delta: {delta_label}",
        f"relative_position: {position_text}",
        f"time_relation: {describe_time_relation(relative_delta)}",
        f"rule_classification: {row.get('rule_classification', '')}",
        f"is_applicable: {json.dumps(row.get('is_applicable'))}",
        "",
    ]

    if row.get("is_applicable") is False:
        lines.append("inapplicability_reason:")
        lines.append(str(row.get("inapplicability_reason", "")))
    elif row.get("is_applicable") is True:
        classification = row.get("rule_classification")
        if classification == "BOOLEAN":
            lines.append("boolean_result:")
            lines.append(format_json_block(row.get("boolean_result")))
        elif classification == "QUANTIFIABLE":
            lines.append("quantifiable_results:")
            lines.append(format_json_block(row.get("quantifiable_results")))
        else:
            boolean_result = row.get("boolean_result")
            quantifiable_results = row.get("quantifiable_results")
            if boolean_result is not None:
                lines.append("boolean_result:")
                lines.append(format_json_block(boolean_result))
            if quantifiable_results:
                lines.append("quantifiable_results:")
                lines.append(format_json_block(quantifiable_results))
    else:
        lines.append("(is_applicable is not explicitly true/false; no judgment details)")

    lines.append("")
    return "\n".join(lines)


def build_report(
    rule_info: Dict[str, Any],
    rule_id: str,
    commit_rows: List[Dict[str, Any]],
    results_path: Path,
) -> str:
    sections = [
        format_rule_info_section(rule_info, rule_id),
        "=" * 80,
        "Commit Judgments (ordered chronologically: earliest -> latest)",
        f"source: {results_path}",
        f"commits: {len(commit_rows)}",
        "=" * 80,
        "",
    ]
    for index, row in enumerate(commit_rows, start=1):
        sections.append(format_commit_section(row, index))
    return "\n".join(sections)


def default_output_path() -> Path:
    return SCRIPT_DIR / "rule_compliance_detail.txt"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Export per-commit compliance judgment details for one rule."
    )
    parser.add_argument(
        "--rule-id",
        default=DEFAULT_RULE_ID,
        help=f"Rule id to export (default: {DEFAULT_RULE_ID})",
    )
    parser.add_argument(
        "--results",
        type=Path,
        default=DEFAULT_RESULTS,
        help="Path to rule_compliance_results.json",
    )
    parser.add_argument(
        "--detect-rules",
        type=Path,
        default=DEFAULT_DETECT_RULES,
        help="Path to detect_rules.json",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Output txt path (default: rule_compliance_judge/rule_compliance_detail.txt)",
    )
    args = parser.parse_args()

    rule_id = args.rule_id
    output_path = args.output or default_output_path()

    detect_rules = load_json_list(args.detect_rules)
    rule_info = find_rule_info(detect_rules, rule_id)

    results = load_json_list(args.results)
    commit_rows = filter_rule_results(results, rule_id)

    report = build_report(rule_info, rule_id, commit_rows, args.results)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report, encoding="utf-8")

    print(f"Wrote {len(commit_rows)} commit judgments to {output_path}")


if __name__ == "__main__":
    main()
