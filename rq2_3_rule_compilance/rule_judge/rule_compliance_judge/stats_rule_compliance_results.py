"""
Per-rule statistics for is_applicable distribution in rule_compliance_results.json.

Each row is one rule; 11 columns left-to-right correspond to relative_delta = +5 .. 0 .. -5
(chronological order: leftmost = earliest commit, rightmost = latest commit).
- F: is_applicable is false
- -: no commit at that relative position
- T: is_applicable is true, followed by a compliance summary:
  - BOOLEAN: boolean_result.is_compliant true/false -> T1 / T0
  - QUANTIFIABLE: counts of is_compliant true/false in quantifiable_results -> Tx,y
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Optional

SCRIPT_DIR = Path(__file__).resolve().parent
RULE_JUDGE_DIR = SCRIPT_DIR.parent
DEFAULT_RESULTS = SCRIPT_DIR / "rule_compliance_outputs" / "rule_compliance_results.json"
DEFAULT_DETECT_RULES = RULE_JUDGE_DIR / "detect_rules.json"

# Must match WINDOW_N in run_rule_compliance_judge.py; columns run earliest -> latest
WINDOW_N = 5
# relative_delta: positive = earlier than rule commit; negative = later than rule commit
COLUMN_DELTAS: List[int] = list(range(WINDOW_N, -WINDOW_N - 1, -1))
PREV_DELTAS: List[int] = [delta for delta in COLUMN_DELTAS if delta > 0]
NEXT_DELTAS: List[int] = [delta for delta in COLUMN_DELTAS if delta < 0]
STATS_HEADERS: List[str] = ["Prev5%", "Curr%", "Next5%"]
CSV_MATRIX_FILENAMES = {
    "main": "stats_rule_compliance_matrix.csv",
    "first_level": "stats_category_mean_first_level.csv",
    "second_level": "stats_category_mean_second_level.csv",
}


def load_results(path: Path) -> List[Dict[str, Any]]:
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError(f"results JSON must be a list: {path}")
    return [row for row in data if isinstance(row, dict)]


def build_rule_matrix(rows: List[Dict[str, Any]]) -> Dict[str, Dict[int, Dict[str, Any]]]:
    matrix: Dict[str, Dict[int, Dict[str, Any]]] = {}
    for row in rows:
        rule_id = row.get("rule_id")
        delta = row.get("relative_delta")
        if not isinstance(rule_id, str) or not rule_id:
            continue
        if not isinstance(delta, int):
            continue
        matrix.setdefault(rule_id, {})[delta] = row
    return matrix


def format_boolean_suffix(row: Dict[str, Any]) -> str:
    boolean_result = row.get("boolean_result")
    if not isinstance(boolean_result, dict):
        return ""
    is_compliant = boolean_result.get("is_compliant")
    if is_compliant is True:
        return "1"
    if is_compliant is False:
        return "0"
    return ""


def format_quantifiable_suffix(row: Dict[str, Any]) -> str:
    quantifiable_results = row.get("quantifiable_results")
    if not isinstance(quantifiable_results, list):
        return ""
    true_count = 0
    false_count = 0
    for item in quantifiable_results:
        if not isinstance(item, dict):
            continue
        if item.get("is_compliant") is True:
            true_count += 1
        elif item.get("is_compliant") is False:
            false_count += 1
    return f"{true_count};{false_count}"


def extract_compliance_counts(row: Optional[Dict[str, Any]]) -> Optional[tuple[int, int]]:
    """Extract (true_count, false_count) from a row where is_applicable=true."""
    if row is None or row.get("is_applicable") is not True:
        return None

    classification = row.get("rule_classification")
    if classification == "BOOLEAN":
        boolean_result = row.get("boolean_result")
        if not isinstance(boolean_result, dict):
            return None
        is_compliant = boolean_result.get("is_compliant")
        if is_compliant is True:
            return 1, 0
        if is_compliant is False:
            return 0, 1
        return None

    if classification == "QUANTIFIABLE":
        quantifiable_results = row.get("quantifiable_results")
        if not isinstance(quantifiable_results, list):
            return None
        true_count = 0
        false_count = 0
        for item in quantifiable_results:
            if not isinstance(item, dict):
                continue
            if item.get("is_compliant") is True:
                true_count += 1
            elif item.get("is_compliant") is False:
                false_count += 1
        if true_count + false_count == 0:
            return None
        return true_count, false_count

    return None


def window_has_applicable(rule_rows: Dict[int, Dict[str, Any]], deltas: List[int]) -> bool:
    return any(extract_compliance_counts(rule_rows.get(delta)) is not None for delta in deltas)


def window_ones_ratio(rule_rows: Dict[int, Dict[str, Any]], deltas: List[int]) -> Optional[float]:
    ones = 0
    zeros = 0
    for delta in deltas:
        counts = extract_compliance_counts(rule_rows.get(delta))
        if counts is None:
            continue
        delta_ones, delta_zeros = counts
        ones += delta_ones
        zeros += delta_zeros
    total = ones + zeros
    if total == 0:
        return None
    return ones / total


def format_ratio_percent(ratio: Optional[float]) -> str:
    if ratio is None:
        return "-"
    return f"{ratio * 100:.2f}%"


def format_ratio_decimal(ratio: Optional[float]) -> str:
    if ratio is None:
        return ""
    return f"{ratio:.4f}"


def get_matrix_headers() -> List[str]:
    return [f"{delta:+d}" if delta != 0 else "0" for delta in COLUMN_DELTAS] + STATS_HEADERS


def is_rule_eligible(rule_rows: Dict[int, Dict[str, Any]]) -> bool:
    return window_has_applicable(rule_rows, PREV_DELTAS) and window_has_applicable(
        rule_rows, NEXT_DELTAS
    )


def compute_stats_columns(
    rule_rows: Dict[int, Dict[str, Any]],
) -> tuple[str, str, str, bool, Optional[float], Optional[float], Optional[float]]:
    if not is_rule_eligible(rule_rows):
        return "-", "-", "-", False, None, None, None

    prev_ratio = window_ones_ratio(rule_rows, PREV_DELTAS)
    curr_ratio = window_ones_ratio(rule_rows, [0])
    next_ratio = window_ones_ratio(rule_rows, NEXT_DELTAS)
    return (
        format_ratio_percent(prev_ratio),
        format_ratio_percent(curr_ratio),
        format_ratio_percent(next_ratio),
        True,
        prev_ratio,
        curr_ratio,
        next_ratio,
    )


def format_cell(row: Optional[Dict[str, Any]]) -> str:
    if row is None:
        return "-"

    is_applicable = row.get("is_applicable")
    if is_applicable is False:
        return "F"
    if is_applicable is not True:
        return "-"

    classification = row.get("rule_classification")
    if classification == "BOOLEAN":
        suffix = format_boolean_suffix(row)
        return f"T{suffix}" if suffix else "T"
    if classification == "QUANTIFIABLE":
        suffix = format_quantifiable_suffix(row)
        return f"T{suffix}" if suffix else "T"
    return "T"


def build_table_rows(
    matrix: Dict[str, Dict[int, Dict[str, Any]]],
) -> tuple[List[tuple[str, List[str]]], List[tuple[Optional[float], Optional[float], Optional[float]]]]:
    table_rows: List[tuple[str, List[str]]] = []
    eligible_ratios: List[tuple[Optional[float], Optional[float], Optional[float]]] = []
    for rule_id in sorted(matrix):
        rule_rows = matrix[rule_id]
        cells = [format_cell(rule_rows.get(delta)) for delta in COLUMN_DELTAS]
        prev_pct, curr_pct, next_pct, eligible, prev_ratio, curr_ratio, next_ratio = compute_stats_columns(
            rule_rows
        )
        cells.extend([prev_pct, curr_pct, next_pct])
        table_rows.append((rule_id, cells))
        if eligible:
            eligible_ratios.append((prev_ratio, curr_ratio, next_ratio))
    return table_rows, eligible_ratios


def count_applicable_in_window(rule_rows: Dict[int, Dict[str, Any]], deltas: List[int]) -> int:
    return sum(
        1
        for delta in deltas
        if extract_compliance_counts(rule_rows.get(delta)) is not None
    )


def count_applicable_commits(rule_rows: Dict[int, Dict[str, Any]]) -> int:
    return sum(
        1
        for delta in COLUMN_DELTAS
        if extract_compliance_counts(rule_rows.get(delta)) is not None
    )


def load_detect_rules_map(path: Path) -> Dict[str, Dict[str, str]]:
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError(f"detect_rules JSON must be a list: {path}")

    rule_map: Dict[str, Dict[str, str]] = {}
    for item in data:
        if not isinstance(item, dict):
            continue
        rule_id = item.get("rule_id")
        if not isinstance(rule_id, str) or not rule_id:
            continue
        rule_map[rule_id] = {
            "first_level": str(item.get("first_level", "")),
            "second_level": str(item.get("second_level", "")),
        }
    return rule_map


def counter_to_sorted_dict(counter: Counter[str]) -> Dict[str, int]:
    return dict(sorted(counter.items(), key=lambda item: (-item[1], item[0])))


def build_eligible_category_distribution(
    eligible_rule_ids: List[str],
    detect_rules_map: Dict[str, Dict[str, str]],
) -> Dict[str, Dict[str, int]]:
    first_level_counter: Counter[str] = Counter()
    second_level_counter: Counter[str] = Counter()

    for rule_id in eligible_rule_ids:
        meta = detect_rules_map.get(rule_id)
        if meta is None:
            first_level_counter["(unknown)"] += 1
            second_level_counter["(unknown)"] += 1
            continue
        first_level = meta.get("first_level") or "(unknown)"
        second_level = meta.get("second_level") or "(unknown)"
        first_level_counter[first_level] += 1
        second_level_counter[second_level] += 1

    return {
        "first_level": counter_to_sorted_dict(first_level_counter),
        "second_level": counter_to_sorted_dict(second_level_counter),
    }


def classify_stats_filter_reason(rule_rows: Dict[int, Dict[str, Any]]) -> Optional[str]:
    has_before = window_has_applicable(rule_rows, PREV_DELTAS)
    has_after = window_has_applicable(rule_rows, NEXT_DELTAS)
    if has_before and has_after:
        return None
    if not has_before and not has_after:
        return "both_windows_no_applicable_T"
    if not has_before:
        return "before_window_no_applicable_T"
    return "after_window_no_applicable_T"


def build_postcheck_summary(
    matrix: Dict[str, Dict[int, Dict[str, Any]]],
    total_result_rows: int,
    detect_rules_map: Dict[str, Dict[str, str]],
) -> Dict[str, Any]:
    llm_judged_rules = len(matrix)
    before_after_distribution: Counter[str] = Counter()
    filtered_reason_distribution: Counter[str] = Counter()
    eligible_rule_ids: List[str] = []

    eligible_total_commit_judgments = 0
    eligible_applicable_T_count = 0
    stats_eligible_rules = 0

    for rule_id, rule_rows in matrix.items():
        before_t_count = count_applicable_in_window(rule_rows, PREV_DELTAS)
        after_t_count = count_applicable_in_window(rule_rows, NEXT_DELTAS)
        filter_reason = classify_stats_filter_reason(rule_rows)

        if filter_reason is None:
            stats_eligible_rules += 1
            eligible_rule_ids.append(rule_id)
            eligible_total_commit_judgments += len(rule_rows)
            eligible_applicable_T_count += count_applicable_commits(rule_rows)
            before_after_distribution[f"before={before_t_count},after={after_t_count}"] += 1
        else:
            filtered_reason_distribution[filter_reason] += 1

    stats_filtered_rules = llm_judged_rules - stats_eligible_rules
    category_distribution = build_eligible_category_distribution(
        eligible_rule_ids, detect_rules_map
    )

    return {
        "llm_judged_rules": llm_judged_rules,
        "stats_eligible_rules": stats_eligible_rules,
        "stats_filtered_rules": stats_filtered_rules,
        "total_result_rows": total_result_rows,
        "eligible_rules_summary": {
            "total_commit_judgments": eligible_total_commit_judgments,
            "applicable_T_count": eligible_applicable_T_count,
            "before_after_distribution": dict(
                sorted(before_after_distribution.items(), key=lambda item: item[0])
            ),
            "category_distribution": category_distribution,
        },
        "filtered_reason_distribution": dict(
            sorted(filtered_reason_distribution.items(), key=lambda item: (-item[1], item[0]))
        ),
    }


def write_postcheck_summary(summary_path: Path, summary: Dict[str, Any]) -> None:
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)


def build_mean_row_cells_decimal(
    eligible_rule_rows: List[Dict[int, Dict[str, Any]]],
) -> List[str]:
    eligible_ratios = [
        compute_stats_columns(rule_rows)[4:7] for rule_rows in eligible_rule_rows
    ]

    delta_cells: List[str] = []
    for delta in COLUMN_DELTAS:
        values = [
            ratio
            for rule_rows in eligible_rule_rows
            if (ratio := window_ones_ratio(rule_rows, [delta])) is not None
        ]
        delta_cells.append(format_ratio_decimal(average_ratio(values)))

    stats_cells: List[str] = []
    for column_index in range(3):
        values = [
            ratios[column_index]
            for ratios in eligible_ratios
            if ratios[column_index] is not None
        ]
        stats_cells.append(format_ratio_decimal(average_ratio(values)))

    return delta_cells + stats_cells


def build_mean_row_cells(
    eligible_rule_rows: List[Dict[int, Dict[str, Any]]],
) -> List[str]:
    eligible_ratios = [
        compute_stats_columns(rule_rows)[4:7] for rule_rows in eligible_rule_rows
    ]
    return compute_mean_delta_ratios(eligible_rule_rows) + compute_mean_stats_ratios(eligible_ratios)


def group_eligible_rules_by_category(
    matrix: Dict[str, Dict[int, Dict[str, Any]]],
    detect_rules_map: Dict[str, Dict[str, str]],
    category_field: str,
) -> Dict[str, List[Dict[int, Dict[str, Any]]]]:
    groups: Dict[str, List[Dict[int, Dict[str, Any]]]] = {}
    for rule_id, rule_rows in matrix.items():
        if not is_rule_eligible(rule_rows):
            continue
        meta = detect_rules_map.get(rule_id, {})
        category = meta.get(category_field) or "(unknown)"
        groups.setdefault(category, []).append(rule_rows)
    return groups


def compute_matrix_widths(
    label_header: str,
    rows: List[tuple[str, List[str]]],
    headers: List[str],
) -> tuple[int, List[int]]:
    label_width = len(label_header)
    col_widths = [len(header) for header in headers]
    for label, cells in rows:
        label_width = max(label_width, len(label))
        for index, cell in enumerate(cells):
            col_widths[index] = max(col_widths[index], len(cell))
    return label_width, col_widths


def render_category_mean_matrix(
    matrix: Dict[str, Dict[int, Dict[str, Any]]],
    detect_rules_map: Dict[str, Dict[str, str]],
    category_field: str,
    section_title: str,
) -> List[str]:
    groups = group_eligible_rules_by_category(matrix, detect_rules_map, category_field)
    categories = sorted(groups.keys(), key=lambda category: (-len(groups[category]), category))
    headers = get_matrix_headers()

    table_rows: List[tuple[str, List[str]]] = []
    for category in categories:
        eligible_rule_rows = groups[category]
        label = f"{category} (n={len(eligible_rule_rows)})"
        table_rows.append((label, build_mean_row_cells(eligible_rule_rows)))

    label_header = "category"
    label_width, col_widths = compute_matrix_widths(label_header, table_rows, headers)

    lines = [
        "=" * 80,
        section_title,
        "mean scope: stats_eligible_rules in this category; same computation as the overall mean row",
        "=" * 80,
        render_aligned_row(label_header, headers, label_width, col_widths),
    ]
    for label, cells in table_rows:
        lines.append(render_aligned_row(label, cells, label_width, col_widths))
    return lines


def build_main_matrix_csv_rows(
    matrix: Dict[str, Dict[int, Dict[str, Any]]],
) -> List[List[str]]:
    rows: List[List[str]] = []
    for rule_id in sorted(matrix):
        rule_rows = matrix[rule_id]
        if not is_rule_eligible(rule_rows):
            continue
        commit_cells = [format_cell(rule_rows.get(delta)) for delta in COLUMN_DELTAS]
        _, _, _, _, prev_ratio, curr_ratio, next_ratio = compute_stats_columns(rule_rows)
        stats_cells = [
            format_ratio_decimal(prev_ratio),
            format_ratio_decimal(curr_ratio),
            format_ratio_decimal(next_ratio),
        ]
        rows.append([rule_id, *commit_cells, *stats_cells])
    return rows


def build_category_mean_csv_rows(
    matrix: Dict[str, Dict[int, Dict[str, Any]]],
    detect_rules_map: Dict[str, Dict[str, str]],
    category_field: str,
    include_overall_mean: bool = False,
) -> List[List[str]]:
    rows: List[List[str]] = []
    if include_overall_mean:
        mean_cells = build_mean_row_cells_decimal(collect_eligible_rule_rows(matrix))
        rows.append(["mean", *mean_cells])

    groups = group_eligible_rules_by_category(matrix, detect_rules_map, category_field)
    categories = sorted(groups.keys(), key=lambda category: (-len(groups[category]), category))
    for category in categories:
        eligible_rule_rows = groups[category]
        label = f"{category} (n={len(eligible_rule_rows)})"
        rows.append([label, *build_mean_row_cells_decimal(eligible_rule_rows)])
    return rows


def write_matrix_csv(
    csv_path: Path,
    label_header: str,
    rows: List[List[str]],
) -> None:
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with open(csv_path, "w", encoding="utf-8-sig", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([label_header, *get_matrix_headers()])
        writer.writerows(rows)


def write_matrix_csv_files(
    matrix: Dict[str, Dict[int, Dict[str, Any]]],
    detect_rules_map: Dict[str, Dict[str, str]],
    output_dir: Path,
) -> Dict[str, Path]:
    paths = {
        key: output_dir / filename for key, filename in CSV_MATRIX_FILENAMES.items()
    }
    write_matrix_csv(
        paths["main"],
        "rule_id",
        build_main_matrix_csv_rows(matrix),
    )
    write_matrix_csv(
        paths["first_level"],
        "category",
        build_category_mean_csv_rows(
            matrix,
            detect_rules_map,
            "first_level",
            include_overall_mean=True,
        ),
    )
    write_matrix_csv(
        paths["second_level"],
        "category",
        build_category_mean_csv_rows(
            matrix,
            detect_rules_map,
            "second_level",
            include_overall_mean=False,
        ),
    )
    return paths


def collect_eligible_rule_rows(
    matrix: Dict[str, Dict[int, Dict[str, Any]]],
) -> List[Dict[int, Dict[str, Any]]]:
    return [rule_rows for rule_rows in matrix.values() if is_rule_eligible(rule_rows)]


def compute_column_widths(
    table_rows: List[tuple[str, List[str]]],
    extra_row_cells: Optional[List[str]] = None,
) -> tuple[int, List[int]]:
    headers = [f"{d:+d}" if d != 0 else "0" for d in COLUMN_DELTAS] + STATS_HEADERS
    rule_id_width = max(len("rule_id"), len("mean"))
    col_widths = [len(h) for h in headers]

    rows_for_width = list(table_rows)
    if extra_row_cells is not None:
        rows_for_width.append(("mean", extra_row_cells))

    for rule_id, cells in rows_for_width:
        rule_id_width = max(rule_id_width, len(rule_id))
        for i, cell in enumerate(cells):
            col_widths[i] = max(col_widths[i], len(cell))

    return rule_id_width, col_widths


def average_ratio(values: List[float]) -> Optional[float]:
    if not values:
        return None
    return sum(values) / len(values)


def compute_mean_delta_ratios(
    eligible_rule_rows: List[Dict[int, Dict[str, Any]]],
) -> List[str]:
    """Mean over 11 commit columns: only eligible rules with T in that column."""
    mean_cells: List[str] = []
    for delta in COLUMN_DELTAS:
        values = [
            ratio
            for rule_rows in eligible_rule_rows
            if (ratio := window_ones_ratio(rule_rows, [delta])) is not None
        ]
        mean_cells.append(format_ratio_percent(average_ratio(values)))
    return mean_cells


def compute_mean_stats_ratios(
    eligible_ratios: List[tuple[Optional[float], Optional[float], Optional[float]]],
) -> List[str]:
    """Mean over Prev5%/Curr%/Next5% columns: arithmetic mean of per-rule ratios."""
    if not eligible_ratios:
        return ["-", "-", "-"]

    mean_cells: List[str] = []
    for column_index in range(3):
        values = [
            ratios[column_index]
            for ratios in eligible_ratios
            if ratios[column_index] is not None
        ]
        mean_cells.append(format_ratio_percent(average_ratio(values)))
    return mean_cells


def render_aligned_row(
    label: str,
    cells: List[str],
    rule_id_width: int,
    col_widths: List[int],
) -> str:
    parts = [label.ljust(rule_id_width)]
    parts.extend(cell.rjust(width) for cell, width in zip(cells, col_widths))
    return "  ".join(parts)


def render_table(
    matrix: Dict[str, Dict[int, Dict[str, Any]]],
) -> tuple[List[str], int, int]:
    table_rows, eligible_ratios = build_table_rows(matrix)
    eligible_rule_rows = collect_eligible_rule_rows(matrix)
    mean_row_cells = build_mean_row_cells(eligible_rule_rows)

    rule_id_width, col_widths = compute_column_widths(table_rows, mean_row_cells)
    headers = get_matrix_headers()

    lines = [render_aligned_row("rule_id", headers, rule_id_width, col_widths)]
    for rule_id, cells in table_rows:
        lines.append(render_aligned_row(rule_id, cells, rule_id_width, col_widths))
    lines.append(render_aligned_row("mean", mean_row_cells, rule_id_width, col_widths))
    return lines, len(matrix), len(eligible_ratios)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Print is_applicable matrix per rule from rule_compliance_results.json"
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
        help="Path to detect_rules.json for eligible rule category stats",
    )
    parser.add_argument(
        "--postcheck-output",
        type=Path,
        default=None,
        help="Path to postcheck_summary.json (default: same dir as results)",
    )
    parser.add_argument(
        "--csv-output-dir",
        type=Path,
        default=None,
        help="Directory for matrix CSV outputs (default: same dir as results)",
    )
    parser.add_argument(
        "--skip-table",
        action="store_true",
        help="Only write postcheck_summary.json without printing the matrix table",
    )
    args = parser.parse_args()

    rows = load_results(args.results)
    matrix = build_rule_matrix(rows)
    detect_rules_map = load_detect_rules_map(args.detect_rules)

    postcheck_summary = build_postcheck_summary(matrix, len(rows), detect_rules_map)
    postcheck_path = args.postcheck_output or args.results.parent / "postcheck_summary.json"
    write_postcheck_summary(postcheck_path, postcheck_summary)

    csv_output_dir = args.csv_output_dir or args.results.parent
    csv_paths = write_matrix_csv_files(matrix, detect_rules_map, csv_output_dir)

    if args.skip_table:
        print(f"Postcheck summary written to {postcheck_path}")
        for key, path in csv_paths.items():
            print(f"CSV [{key}]: {path}")
        print(json.dumps(postcheck_summary, ensure_ascii=False, indent=2))
        return

    lines, total_rules, eligible_rules = render_table(matrix)
    for line in lines:
        print(line)

    for section_lines in (
        render_category_mean_matrix(
            matrix,
            detect_rules_map,
            "first_level",
            "Category Mean Matrix by first_level (stats_eligible_rules only)",
        ),
        render_category_mean_matrix(
            matrix,
            detect_rules_map,
            "second_level",
            "Category Mean Matrix by second_level (stats_eligible_rules only)",
        ),
    ):
        print()
        for line in section_lines:
            print(line)

    print("-" * 80)
    print(f"postcheck_summary={postcheck_path}")
    for key, path in csv_paths.items():
        print(f"csv_{key}={path}")
    print(f"rules={total_rules}, result_rows={len(rows)}, source={args.results}")
    print(
        f"stats_eligible_rules={eligible_rules}/{total_rules} "
        f"(Prev5%/Curr%/Next5% require T in both prev and next windows)"
    )
    print(
        "mean computation: average over stats_eligible_rules only; "
        "each rule's compliance rate = true_count / (true_count + false_count); "
        "each column includes only eligible rules with T in that column"
    )
    print(
        "cell legend: F=not applicable; T1/T0=BOOLEAN compliant/non-compliant; "
        "Tx;y=QUANTIFIABLE true/false counts; CSV stats columns use 4-decimal ratios"
    )


if __name__ == "__main__":
    main()
