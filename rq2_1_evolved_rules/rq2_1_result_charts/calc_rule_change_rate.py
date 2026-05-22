import csv
import json
import os
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


SCRIPT_DIR = Path(__file__).resolve().parent
EVOLVED_DIR = SCRIPT_DIR.parent / "file_diffs"
ANALYZED_DIR = SCRIPT_DIR.parent.parent / "rq1_rules" / "rules"
OUTPUT_CSV = SCRIPT_DIR / "rq2_1_change_rate_stats.csv"

CHANGE_TYPES = ("added", "modified", "deleted")

ORDERED_SECOND_LEVELS = [
    "Technology Stack Selections",
    "Design Principles & Patterns",
    "System Architecture",
    "Design References & Constraints",
    "Framework Usage",
    "Code Style Conventions",
    "Performance Optimization",
    "Language Features",
    "Error & Exception Handling",
    "Business Logic",
    "Workflow Conventions",
    "Project Documentation",
    "Directory Structure",
    "Environment Configuration",
    "Version Control",
    "Dependency Management",
    "Testing Strategy",
    "Security Practices",
    "Code Quality Standards",
    "Logging Standards",
    "Code Review",
    "AI Behavior & Decision Strategies",
    "AI Output Content Guidelines",
    "AI Context Management",
    "AI Tool Usage",
]

ORDERED_ROWS = [
    "Architecture & Design",
    "Technology Stack Selections",
    "Design Principles & Patterns",
    "System Architecture",
    "Design References & Constraints",
    "Code Implementation",
    "Framework Usage",
    "Code Style Conventions",
    "Performance Optimization",
    "Language Features",
    "Error & Exception Handling",
    "Business Logic",
    "Development Workflow & Project Management",
    "Workflow Conventions",
    "Project Documentation",
    "Directory Structure",
    "Environment Configuration",
    "Version Control",
    "Dependency Management",
    "Quality Assurance",
    "Testing Strategy",
    "Security Practices",
    "Code Quality Standards",
    "Logging Standards",
    "Code Review",
    "AI Collaboration Specifications",
    "AI Behavior & Decision Strategies",
    "AI Output Content Guidelines",
    "AI Context Management",
    "AI Tool Usage",
]

FIRST_TO_SECONDS = {
    "Architecture & Design": [
        "Technology Stack Selections",
        "Design Principles & Patterns",
        "System Architecture",
        "Design References & Constraints",
    ],
    "Code Implementation": [
        "Framework Usage",
        "Code Style Conventions",
        "Performance Optimization",
        "Language Features",
        "Error & Exception Handling",
        "Business Logic",
    ],
    "Development Workflow & Project Management": [
        "Workflow Conventions",
        "Project Documentation",
        "Directory Structure",
        "Environment Configuration",
        "Version Control",
        "Dependency Management",
    ],
    "Quality Assurance": [
        "Testing Strategy",
        "Security Practices",
        "Code Quality Standards",
        "Logging Standards",
        "Code Review",
    ],
    "AI Collaboration Specifications": [
        "AI Behavior & Decision Strategies",
        "AI Output Content Guidelines",
        "AI Context Management",
        "AI Tool Usage",
    ],
}

# 历史标注中存在少量命名差异，统一映射到当前统计口径。
SECOND_LEVEL_ALIASES = {
    "Design Principles": "Design Principles & Patterns",
    "Architecture Patterns": "System Architecture",
}


def find_json_files(directory: Path) -> List[str]:
    json_files: List[str] = []
    for root, _dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".json"):
                json_files.append(os.path.join(root, file))
    return json_files


def normalize_label(label: str) -> str:
    if not isinstance(label, str):
        return "Unknown"
    return label.strip()


def normalize_second_level(second_level: str) -> str:
    normalized = normalize_label(second_level)
    return SECOND_LEVEL_ALIASES.get(normalized, normalized)


def is_chore(first_level: str) -> bool:
    return normalize_label(first_level).lower() == "chore"


def read_json_list(path: str) -> Iterable[dict]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                yield item


def collect_counts_analyzed() -> Tuple[int, Counter, Counter]:
    total = 0
    first_counter: Counter = Counter()
    second_counter: Counter = Counter()

    for json_file in find_json_files(ANALYZED_DIR):
        for obj in read_json_list(json_file):
            first = normalize_label(obj.get("first_level", "Unknown"))
            second = normalize_second_level(obj.get("second_level", "Unknown"))
            if is_chore(first):
                continue
            total += 1
            first_counter[first] += 1
            second_counter[second] += 1

    return total, first_counter, second_counter


def collect_counts_evolved() -> Tuple[int, Counter, Counter, Dict[str, Counter], Dict[str, Counter]]:
    total = 0
    first_counter: Counter = Counter()
    second_counter: Counter = Counter()
    first_change_type_counter: Dict[str, Counter] = defaultdict(Counter)
    second_change_type_counter: Dict[str, Counter] = defaultdict(Counter)

    for json_file in find_json_files(EVOLVED_DIR):
        for obj in read_json_list(json_file):
            first = normalize_label(obj.get("first_level", "Unknown"))
            second = normalize_second_level(obj.get("second_level", "Unknown"))
            if is_chore(first):
                continue

            change_type = normalize_label(obj.get("change_type", "Unknown")).lower()
            total += 1
            first_counter[first] += 1
            second_counter[second] += 1
            first_change_type_counter[first][change_type] += 1
            second_change_type_counter[second][change_type] += 1

    return total, first_counter, second_counter, first_change_type_counter, second_change_type_counter


def pct(value: int, denominator: int) -> float:
    if denominator == 0:
        return 0.0
    return value / denominator


def build_rows(
    analyzed_first: Counter,
    analyzed_second: Counter,
    evolved_first: Counter,
    evolved_second: Counter,
    evolved_first_change_types: Dict[str, Counter],
    evolved_second_change_types: Dict[str, Counter],
) -> List[dict]:
    rows: List[dict] = []

    for category in ORDERED_ROWS:
        is_first_level = category in FIRST_TO_SECONDS
        level = "first_level" if is_first_level else "second_level"

        if is_first_level:
            analyzed_count = analyzed_first.get(category, 0)
            evolved_count = evolved_first.get(category, 0)
            change_counter = evolved_first_change_types.get(category, Counter())
        else:
            analyzed_count = analyzed_second.get(category, 0)
            evolved_count = evolved_second.get(category, 0)
            change_counter = evolved_second_change_types.get(category, Counter())

        row = {
            "category_level": level,
            "category_name": category,
            "analyzed_count": analyzed_count,
            "evolved_count": evolved_count,
            "change_rate": f"{pct(evolved_count, analyzed_count):.6f}",
            "added_count": 0,
            "added_ratio_in_category": "0.000000",
            "modified_count": 0,
            "modified_ratio_in_category": "0.000000",
            "deleted_count": 0,
            "deleted_ratio_in_category": "0.000000",
        }

        for change_type in CHANGE_TYPES:
            count = change_counter.get(change_type, 0)
            row[f"{change_type}_count"] = count
            row[f"{change_type}_ratio_in_category"] = f"{pct(count, evolved_count):.6f}"

        rows.append(row)

    return rows


def write_csv(rows: List[dict]) -> None:
    fieldnames = [
        "category_level",
        "category_name",
        "analyzed_count",
        "evolved_count",
        "change_rate",
        "added_count",
        "added_ratio_in_category",
        "modified_count",
        "modified_ratio_in_category",
        "deleted_count",
        "deleted_ratio_in_category",
    ]
    with open(OUTPUT_CSV, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    analyzed_total, analyzed_first, analyzed_second = collect_counts_analyzed()
    (
        evolved_total,
        evolved_first,
        evolved_second,
        evolved_first_change_types,
        evolved_second_change_types,
    ) = collect_counts_evolved()

    print(f"analyzed_total_without_chore={analyzed_total}")
    print(f"evolved_total_without_chore={evolved_total}")

    expected_evolved = 1540
    expected_analyzed = 7310
    if evolved_total != expected_evolved or analyzed_total != expected_analyzed:
        raise ValueError(
            "Count check failed: "
            f"expected evolved={expected_evolved}, analyzed={expected_analyzed}; "
            f"got evolved={evolved_total}, analyzed={analyzed_total}"
        )

    rows = build_rows(
        analyzed_first=analyzed_first,
        analyzed_second=analyzed_second,
        evolved_first=evolved_first,
        evolved_second=evolved_second,
        evolved_first_change_types=evolved_first_change_types,
        evolved_second_change_types=evolved_second_change_types,
    )
    write_csv(rows)
    print(f"CSV written: {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
