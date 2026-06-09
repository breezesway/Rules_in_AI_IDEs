"""
Read commit_windows_info meta.txt and print binned distribution statistics (text only).

Metrics:
- Per commit: modified file count; total changed lines (add+del).
- Per file: changed lines; after_lines (full file lines after commit).

Bucket rules (designed for typical skew: many small, few huge):
- File count per commit: small linear bands + tail.
- Line-based metrics: decade bands on a log10 scale + zero bucket.
"""

from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path
from statistics import mean
from typing import Callable, Dict, List, Optional, Tuple

RULE_JUDGE_DIR = Path(__file__).resolve().parent
INFO_ROOT = RULE_JUDGE_DIR / "commit_windows_info"

MODIFIED_LINE_RE = re.compile(
    r"^(?P<path>.+)\t\+(?P<ins>-|\d+)\t-(?P<del>-|\d+)\tafter_lines=(?P<after>SKIPPED|\d+)(?:\tskipped_reason=(?P<reason>.+))?$"
)


def safe_int(v: str) -> Optional[int]:
    try:
        return int(v)
    except (TypeError, ValueError):
        return None


def parse_meta(meta_path: Path) -> dict:
    lines = meta_path.read_text(encoding="utf-8", errors="replace").splitlines()
    modified_rows = []
    in_modified = False
    skipped_count_declared = 0

    for line in lines:
        if line == "modified files:":
            in_modified = True
            continue
        if line == "project_tree_after_this_commit:":
            in_modified = False
            continue
        if in_modified:
            if not line.strip():
                in_modified = False
                continue
            m = MODIFIED_LINE_RE.match(line)
            if m:
                modified_rows.append(
                    {
                        "path": m.group("path"),
                        "ins_raw": m.group("ins"),
                        "del_raw": m.group("del"),
                        "after_raw": m.group("after"),
                        "reason": m.group("reason") or "",
                    }
                )

    for line in lines:
        if line.startswith("skipped_files_count:"):
            try:
                skipped_count_declared = int(line.split(":", 1)[1].strip())
            except ValueError:
                skipped_count_declared = 0
            break

    return {"modified_rows": modified_rows, "skipped_count_declared": skipped_count_declared}


def collect_series() -> Tuple[List[int], List[int], List[int], List[int], Dict[str, Counter], int]:
    commit_file_counts: List[int] = []
    commit_changed_lines: List[int] = []
    file_changed_lines: List[int] = []
    file_after_lines: List[int] = []
    commits_with_skipped = 0
    skipped_reason_counter: Counter = Counter()
    skipped_ext_counter: Counter = Counter()
    skipped_path_counter: Counter = Counter()

    for meta in sorted(INFO_ROOT.glob("*/*/meta.txt")):
        data = parse_meta(meta)
        rows = data["modified_rows"]
        commit_file_counts.append(len(rows))
        total_changed = 0
        commit_has_skipped = False
        for row in rows:
            ins_i = safe_int(row["ins_raw"])
            del_i = safe_int(row["del_raw"])
            after_i = safe_int(row["after_raw"])
            if ins_i is not None and del_i is not None:
                ch = ins_i + del_i
                total_changed += ch
                file_changed_lines.append(ch)
            if after_i is not None:
                file_after_lines.append(after_i)
            reason = row["reason"]
            path = row["path"]
            if reason:
                commit_has_skipped = True
                skipped_reason_counter[reason] += 1
                skipped_path_counter[path] += 1
                ext = Path(path).suffix.lower() or "[no_ext]"
                skipped_ext_counter[ext] += 1
        commit_changed_lines.append(total_changed)
        if commit_has_skipped or data.get("skipped_count_declared", 0) > 0:
            commits_with_skipped += 1

    skipped_stats = {
        "reason_counter": skipped_reason_counter,
        "ext_counter": skipped_ext_counter,
        "path_counter": skipped_path_counter,
    }
    return (
        commit_file_counts,
        commit_changed_lines,
        file_changed_lines,
        file_after_lines,
        skipped_stats,
        commits_with_skipped,
    )


def bucket_files_per_commit(n: int) -> str:
    """Buckets for 'how many files in one commit' (integer >= 1)."""
    if n <= 0:
        return "0"
    if n == 1:
        return "1"
    if n <= 5:
        return "2–5"
    if n <= 10:
        return "6–10"
    if n <= 20:
        return "11–20"
    if n <= 50:
        return "21–50"
    if n <= 100:
        return "51–100"
    if n <= 200:
        return "101–200"
    return "201+"


def bucket_lines(v: int) -> str:
    """
    Buckets for line counts (changed lines or file line count).
    0 separate; low end by powers of 10; **1k–10k** as 1k–2k, 2k–4k, 4k–6k, 6k–9,999.
    """
    if v == 0:
        return "0"
    if v < 10:
        return "1–9"
    if v < 100:
        return "10–99"
    if v < 1000:
        return "100–999"
    # [1k, 10k) split: 1k–2k, 2k–4k, 4k–6k, 6k–9,999
    if v < 2000:
        return "1k–2k"
    if v < 4000:
        return "2k–4k"
    if v < 6000:
        return "4k–6k"
    if v < 10_000:
        return "6k–9,999"
    if v < 100_000:
        return "10k–99,999"
    if v < 1_000_000:
        return "100k–999,999"
    return "1,000,000+"


def count_buckets(values: List[int], label_fn: Callable[[int], str]) -> List[Tuple[str, int]]:
    """Stable order: first occurrence order of labels as we define buckets."""
    order: List[str] = []
    counts: Dict[str, int] = {}

    def add_label(lab: str) -> None:
        if lab not in counts:
            order.append(lab)
            counts[lab] = 0

    # Pre-register known order for consistent output
    if label_fn == bucket_files_per_commit:
        for lab in ("0", "1", "2–5", "6–10", "11–20", "21–50", "51–100", "101–200", "201+"):
            add_label(lab)
    else:
        for lab in (
            "0",
            "1–9",
            "10–99",
            "100–999",
            "1k–2k",
            "2k–4k",
            "4k–6k",
            "6k–9,999",
            "10k–99,999",
            "100k–999,999",
            "1,000,000+",
        ):
            add_label(lab)

    for v in values:
        lab = label_fn(v)
        if lab not in counts:
            order.append(lab)
            counts[lab] = 0
        counts[lab] += 1

    return [(lab, counts[lab]) for lab in order if counts.get(lab, 0) > 0]


def summary_lines(name: str, values: List[int]) -> List[str]:
    if not values:
        return [f"{name}: (no data)", ""]
    s = sorted(values)
    n = len(s)

    def pct(p: float) -> int:
        i = int(round((n - 1) * p))
        return s[max(0, min(i, n - 1))]

    return [
        f"{name}",
        f"  n={n}  min={s[0]}  max={s[-1]}  mean={mean(values):.2f}",
        f"  p50={pct(0.5)}  p90={pct(0.9)}  p99={pct(0.99)}",
    ]


def print_bucket_table(title: str, lines_out: List[str], buckets: List[Tuple[str, int]], total_n: int) -> None:
    lines_out.append(title)
    lines_out.append("-" * min(72, len(title) + 20))
    if total_n == 0:
        lines_out.append("  (no data)")
        lines_out.append("")
        return
    w = max(len(b[0]) for b in buckets) if buckets else 1
    for lab, c in buckets:
        pct = 100.0 * c / total_n
        lines_out.append(f"  {lab:<{w}}  {c:>6}  ({pct:5.1f}%)")
    lines_out.append(f"  {'TOTAL':<{w}}  {total_n:>6}  (100.0%)")
    lines_out.append("")


def main() -> None:
    if not INFO_ROOT.is_dir():
        print(f"Folder not found: {INFO_ROOT}", file=sys.stderr)
        sys.exit(1)

    (
        commit_file_counts,
        commit_changed_lines,
        file_changed_lines,
        file_after_lines,
        skipped_stats,
        commits_with_skipped,
    ) = collect_series()

    out: List[str] = []
    out.append("commit_windows_info — binned distributions")
    out.append("(generated by stats_commit_windows_binned.py)")
    out.append("")
    out.append("Bucket rules:")
    out.append("  • Files per commit: 1, 2–5, 6–10, … 201+")
    out.append("  • Line counts: 0, 1–9, … 100–999, then 1k–2k, 2k–4k, 4k–6k, 6k–9,999, then 10k+ …")
    out.append("")

    out.extend(summary_lines("1) Commits — modified file count", commit_file_counts))
    out.append("")
    print_bucket_table(
        "1) Distribution (files per commit)",
        out,
        count_buckets(commit_file_counts, bucket_files_per_commit),
        len(commit_file_counts),
    )

    out.extend(summary_lines("2) Commits — total changed lines (add+del)", commit_changed_lines))
    out.append("")
    print_bucket_table(
        "2) Distribution (total changed lines per commit)",
        out,
        count_buckets(commit_changed_lines, bucket_lines),
        len(commit_changed_lines),
    )

    out.extend(summary_lines("3) Files — changed lines per file (add+del)", file_changed_lines))
    out.append("")
    print_bucket_table(
        "3) Distribution (changed lines per file)",
        out,
        count_buckets(file_changed_lines, bucket_lines),
        len(file_changed_lines),
    )

    out.extend(summary_lines("4) Files — lines after commit (after_lines)", file_after_lines))
    out.append("")
    print_bucket_table(
        "4) Distribution (after_lines per file)",
        out,
        count_buckets(file_after_lines, bucket_lines),
        len(file_after_lines),
    )

    reason_counter: Counter = skipped_stats["reason_counter"]
    ext_counter: Counter = skipped_stats["ext_counter"]
    path_counter: Counter = skipped_stats["path_counter"]
    commit_total = len(commit_file_counts)

    out.append("[Skipped files]")
    out.append(f"  commits with skipped files: {commits_with_skipped}")
    out.append(f"  commits without skipped files: {commit_total - commits_with_skipped}")
    out.append(f"  skipped file entries total: {sum(reason_counter.values())}")
    out.append("")
    out.append("  top skipped reasons:")
    if reason_counter:
        for reason, cnt in reason_counter.most_common(20):
            out.append(f"    - {reason}: {cnt}")
    else:
        out.append("    - none")
    out.append("")
    out.append("  top skipped file extensions:")
    if ext_counter:
        for ext, cnt in ext_counter.most_common(20):
            out.append(f"    - {ext}: {cnt}")
    else:
        out.append("    - none")
    out.append("")
    out.append("  top skipped file paths:")
    if path_counter:
        for path, cnt in path_counter.most_common(20):
            out.append(f"    - {path}: {cnt}")
    else:
        out.append("    - none")
    out.append("")
    out.append("  all skipped file paths:")
    if path_counter:
        for path in sorted(path_counter.keys()):
            out.append(f"    - {path}")
    else:
        out.append("    - none")

    text = "\n".join(out) + "\n"
    print(text)


if __name__ == "__main__":
    main()
