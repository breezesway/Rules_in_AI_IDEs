"""Compare token complexity: 160 retained rules versus their 917-rule complement.

Run with /opt/anaconda3/bin/python. Reuses the sibling compliance script's
post-change content selection, tokenizer settings and persistent cache logic.
"""

from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from importlib.metadata import version
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent.parent
INFLUENCE = PROJECT / "rule_influence"
COMPLIANCE = HERE.parent / "rule_complexity_compliance"


def load_helpers():
    path = COMPLIANCE / "analyze_complexity_compliance.py"
    spec = importlib.util.spec_from_file_location("complexity_compliance_helpers", path)
    if spec is None or spec.loader is None:
        raise ValueError(f"Cannot load tokenizer helpers: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_groups(source, selected_csv, diffs_dir):
    data = json.loads(source.read_text(encoding="utf-8"))
    if not isinstance(data, list) or len(data) != 1077:
        raise ValueError("Source must contain exactly 1077 rules")
    rules = {}
    for rule in data:
        rid, content = rule.get("rule_id"), rule.get("rule_content")
        if not isinstance(rid, str) or not rid.strip() or rid in rules:
            raise ValueError(f"Invalid or duplicate rule ID: {rid}")
        if not isinstance(content, str) or not content.strip():
            raise ValueError(f"Empty rule content: {rid}")
        rules[rid] = rule
    with selected_csv.open(encoding="utf-8-sig", newline="") as handle:
        selected = [row["rule_id"] for row in csv.DictReader(handle)]
    if len(selected) != 160 or len(set(selected)) != 160:
        raise ValueError("Selected CSV must contain 160 unique rule IDs")
    selected = set(selected)
    if not selected.issubset(rules):
        raise ValueError(f"Selected IDs missing from source: {sorted(selected - rules.keys())}")
    if len(rules.keys() - selected) != 917:
        raise ValueError("Expected exactly 917 rules outside the selected set")

    # Metadata identifies modified rules; content is taken from the supplied JSON.
    metadata = {}
    for path in sorted(diffs_dir.rglob("*.json")):
        records = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(records, list):
            continue
        for rule in records:
            rid = rule.get("id")
            if rid not in rules:
                continue
            if rid in metadata and metadata[rid] != rule:
                raise ValueError(f"Conflicting original metadata: {rid}")
            metadata[rid] = rule
    if rules.keys() - metadata.keys():
        raise ValueError("Missing change-type metadata for some source rules")
    rows = []
    for rid in sorted(rules):
        meta = metadata[rid]
        if meta.get("content") != rules[rid]["rule_content"]:
            raise ValueError(f"Source content differs from original metadata: {rid}")
        if meta.get("change_type") not in ("added", "modified"):
            raise ValueError(f"Unsupported change type: {rid}")
        rows.append({"rule_id": rid, "group": "retained_160" if rid in selected else "filtered_917",
                     "original_content": rules[rid]["rule_content"],
                     "change_type": meta["change_type"]})
    return rows


def compare(rows, alpha, helpers):
    from scipy.stats import mannwhitneyu

    retained = [row for row in rows if row["group"] == "retained_160"]
    filtered = [row for row in rows if row["group"] == "filtered_917"]
    x = [r["token_count"] for r in retained]
    y = [r["token_count"] for r in filtered]
    test = mannwhitneyu(x, y, alternative="two-sided", method="asymptotic",
                        use_continuity=True, nan_policy="raise")
    u, p = float(test.statistic), float(test.pvalue)
    # U awards half a win to ties; this identity equals P(X>Y)-P(X<Y).
    delta = 2 * u / (len(x) * len(y)) - 1
    return {
        "test": "Mann-Whitney U, two-sided, asymptotic, tie and continuity corrected",
        "x": "retained_160", "y": "filtered_917", "U_x": u,
        "U_y": len(x) * len(y) - u, "p_value": p,
        "alpha": alpha, "significant": p < alpha,
        "cliffs_delta": delta, "rank_biserial_correlation": delta,
        "effect_formula": "2 * U_x / (n_x * n_y) - 1",
        "effect_direction": "Positive: retained rules tend to have more tokens than filtered rules",
        "descriptive_statistics": {
            "retained_160": helpers.describe_tokens(retained),
            "filtered_917": helpers.describe_tokens(filtered)},
        "content_extraction": {group: dict(Counter(r["content_source"] for r in group_rows))
                               for group, group_rows in (("retained_160", retained),
                                                         ("filtered_917", filtered))},
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--diffs-dir", type=Path, default=INFLUENCE / "file_diffs")
    parser.add_argument("--cache", type=Path, default=HERE / "rule_token_cache.json")
    parser.add_argument("--output-dir", type=Path, default=HERE / "results")
    parser.add_argument("--alpha", type=float, default=0.05)
    args = parser.parse_args()
    if not 0 < args.alpha < 1:
        parser.error("Require 0 < alpha < 1")
    helpers = load_helpers()
    rows = load_groups(args.source, args.selected_csv, args.diffs_dir)
    # Seed from the previously computed 160 rules; the helper checks settings and hashes.
    seed = COMPLIANCE / "rule_token_cache.json"
    if not args.cache.exists() and seed.is_file():
        helpers.write_json(args.cache, json.loads(seed.read_text(encoding="utf-8")))
    hits, computed = helpers.add_token_counts(rows, args.cache, "cl100k_base", "after")
    result = compare(rows, args.alpha, helpers)
    result.update({"source": str(args.source.resolve()),
                   "selected_csv": str(args.selected_csv.resolve()),
                   "metadata_source": str(args.diffs_dir.resolve()),
                   "encoding": "cl100k_base", "content_mode": "after",
                   "cache": {"hits": hits, "computed": computed},
                   "scipy_version": version("scipy"), "tiktoken_version": version("tiktoken"),
                   "created_at_utc": datetime.now(timezone.utc).isoformat()})
    args.output_dir.mkdir(parents=True, exist_ok=True)
    helpers.write_json(args.output_dir / "mann_whitney_results.json", result)
    helpers.write_csv(args.output_dir / "rule_tokens.csv", [
        {key: row[key] for key in ("rule_id", "group", "change_type", "content_source",
                                   "token_count", "tokenized_content")} for row in rows])
    lines = [
        "Token complexity: retained versus filtered rules", "",
        "Source: 1077 unique rules; retained: 160 IDs from the compliance CSV; filtered: the remaining 917.",
        "The 917-rule group is defined by set difference, not by the Gemini can_detect flag alone.",
        "Complexity: token count with tiktoken cl100k_base, encode_ordinary.",
        "Modified +/- snippets use post-change text, with diff prefixes removed and old lines excluded.",
        "Modified records with only a description retain that description, as in the preceding 160-rule analysis.",
        "", result["test"],
        f"U (retained group) = {result['U_x']:.2f}",
        f"p = {result['p_value']:.12g}",
        f"alpha = {args.alpha}; significant = {result['significant']}",
        f"Cliff's delta = {result['cliffs_delta']:.6f} (identical to rank-biserial correlation)",
        "Effect direction: positive means retained rules tend to be longer; negative means filtered rules tend to be longer.",
        "", "Descriptive statistics (tokens)",
        "Group\tN\tMean\tSD\tMin\tQ1\tMedian\tQ3\tMax",
    ]
    for group, stats in result["descriptive_statistics"].items():
        values = [stats[key] for key in ("Mean", "Sample standard deviation", "Minimum",
                                         "Q1 (25th percentile)", "Median", "Q3 (75th percentile)", "Maximum")]
        lines.append(f"{group}\t{stats['N']}\t" + "\t".join(f"{v:.2f}" for v in values))
    lines += ["", "Interpretation notes:",
              "This rank test does not directly test arithmetic means; token length is a proxy for complexity.",
              "Rules are treated as independent observations; project/file clustering is not adjusted for.",
              "Only one group comparison is performed; no multiple-testing correction is applied.",
              f"Content extraction: {json.dumps(result['content_extraction'])}",
              f"Token cache: hits={hits}, computed={computed}.",
              f"Source: {args.source.resolve()}", f"Selected IDs: {args.selected_csv.resolve()}",
              "Method: https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.mannwhitneyu.html"]
    summary = "\n".join(lines) + "\n"
    (args.output_dir / "summary.txt").write_text(summary, encoding="utf-8")
    print(summary)


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, ImportError) as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)
