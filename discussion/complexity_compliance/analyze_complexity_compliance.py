"""Spearman correlations between rule token counts and compliance rates.

Run with /opt/anaconda3/bin/python; use --help for input and output options.
Compliance rates are displayed to two decimals but analyzed at source precision.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import sys
from collections import Counter
from datetime import datetime, timezone
from importlib.metadata import version
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent.parent
JUDGE = PROJECT / "rq2_3_rule_compliance" / "rule_judge"
DEFAULT_CSV = (JUDGE / "rule_compliance_judge" / "rule_compliance_outputs" / "stats_rule_compliance_matrix.csv")
FIELDS = {"before": "before5%", "current": "current%", "after": "after5%"}


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False) + "\n",
                         encoding="utf-8")
    temporary.replace(path)


def write_csv(path, rows):
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def parse_rate(value):
    value = value.strip()
    if value in ("", "-"):
        return None
    rate = float(value[:-1]) / 100 if value.endswith("%") else float(value)
    if not math.isfinite(rate) or not 0 <= rate <= 1:
        raise ValueError(f"Invalid compliance rate: {value!r}")
    return rate


def load_data(csv_path, rules_path, expected_rules):
    with csv_path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        required = {"rule_id", *FIELDS.values()}
        if not required.issubset(reader.fieldnames or []):
            raise ValueError(f"CSV must contain {sorted(required)}")
        records = list(reader)
    if expected_rules and len(records) != expected_rules:
        raise ValueError(f"Expected {expected_rules} rules, found {len(records)}")
    if not records:
        raise ValueError("No rule rows")
    ids = [row["rule_id"] for row in records]
    if len(ids) != len(set(ids)) or any(not rid.strip() for rid in ids):
        raise ValueError("Missing or duplicate CSV rule IDs")
    source = json.loads(rules_path.read_text(encoding="utf-8"))
    if not isinstance(source, list):
        raise ValueError("Rule source must be a JSON array")
    matched = {}
    for rule in source:
        rid = rule.get("rule_id")
        if rid not in ids:
            continue
        if rid in matched:
            raise ValueError(f"Duplicate source rule ID: {rid}")
        if not isinstance(rule.get("rule_content"), str) or not rule["rule_content"].strip():
            raise ValueError(f"Empty rule content: {rid}")
        matched[rid] = rule
    missing = set(ids) - matched.keys()
    if missing:
        raise ValueError(f"Rule IDs missing from JSON: {sorted(missing)}")
    rows = []
    for record in records:
        source_rule = matched[record["rule_id"]]
        row = {"rule_id": record["rule_id"], "project": source_rule.get("project", ""),
               "change_type": source_rule.get("change_type", ""),
               "original_content": source_rule["rule_content"]}
        row.update({name: parse_rate(record[field]) for name, field in FIELDS.items()})
        row["after_minus_before"] = (row["after"] - row["before"]
                                     if row["after"] is not None and row["before"] is not None
                                     else None)
        rows.append(row)
    return rows


def select_content(content, change_type, mode):
    if mode == "after" and change_type == "modified":
        lines = content.splitlines()
        if any(line.startswith("+") for line in lines) and any(line.startswith("-") for line in lines):
            # These source records contain rule-level +/- snippets, not full unified patches.
            if any(line.startswith(("+++", "---", "@@")) for line in lines):
                raise ValueError("Unexpected unified patch headers; inspect source text")
            selected = "\n".join(line[1:] if line.startswith("+") else line
                                 for line in lines if not line.startswith("-"))
            if not selected.strip():
                raise ValueError("No post-change content in modified rule")
            return selected, "post_change_diff_lines"
        return content, "modified_description_as_provided"
    return content, "raw_rule_content"


def add_token_counts(rows, cache_path, encoding, mode):
    import tiktoken

    # Reuse the previously downloaded vocabulary without depending on network access.
    vocab = HERE.parent / "rule_complexity" / ".tiktoken_cache"
    if vocab.is_dir():
        os.environ.setdefault("TIKTOKEN_CACHE_DIR", str(vocab))
    metadata = {"schema": 1, "encoding": encoding, "tiktoken_version": version("tiktoken"),
                "content_mode": mode, "method": "encode_ordinary; select_content_v1"}
    cache = {"metadata": metadata, "rules": {}}
    if cache_path.exists():
        previous = json.loads(cache_path.read_text(encoding="utf-8"))
        if previous.get("metadata") == metadata:
            cache = previous
    hits, computed, tokenizer = 0, 0, None
    try:
        for row in rows:
            text, extraction = select_content(row["original_content"], row["change_type"], mode)
            row["tokenized_content"] = text
            row["content_source"] = extraction
            digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
            entry = cache["rules"].get(row["rule_id"], {})
            if (entry.get("content_sha256") == digest
                    and type(entry.get("token_count")) is int and entry["token_count"] > 0):
                row["token_count"] = entry["token_count"]
                hits += 1
            else:
                if tokenizer is None:
                    tokenizer = tiktoken.get_encoding(encoding)
                row["token_count"] = len(tokenizer.encode_ordinary(text))
                cache["rules"][row["rule_id"]] = {
                    "content_sha256": digest, "token_count": row["token_count"]}
                computed += 1
    finally:
        write_json(cache_path, cache)
    return hits, computed


def correlate(rows, alpha):
    from scipy.stats import spearmanr

    results = []
    for metric in ("before", "current", "after", "after_minus_before"):
        valid = [row for row in rows if row[metric] is not None]
        x, y = [r["token_count"] for r in valid], [r[metric] for r in valid]
        rho, p = None, None
        if len(valid) < 3 or len(set(x)) < 2 or len(set(y)) < 2:
            status = "Not testable: fewer than 3 pairs or a constant variable"
        else:
            test = spearmanr(x, y, alternative="two-sided", nan_policy="raise")
            rho, p = float(test.statistic), float(test.pvalue)
            status = "Significant" if p < alpha else "Not significant"
        results.append({"metric": metric, "n": len(valid), "excluded": len(rows) - len(valid),
                        "spearman_rho": rho, "p_value": p, "alpha": alpha, "result": status})
    return results


def describe_tokens(rows):
    """Describe all matched rules, including those missing a compliance rate."""
    import numpy as np

    tokens = np.asarray([row["token_count"] for row in rows], dtype=float)
    q1, median, q3 = np.percentile(tokens, [25, 50, 75], method="linear")
    return {
        "N": len(tokens),
        "Mean": float(tokens.mean()),
        "Sample standard deviation": float(tokens.std(ddof=1)) if len(tokens) > 1 else None,
        "Minimum": float(tokens.min()),
        "Q1 (25th percentile)": float(q1),
        "Median": float(median),
        "Q3 (75th percentile)": float(q3),
        "Maximum": float(tokens.max()),
        "IQR (Q3 - Q1)": float(q3 - q1),
        "Total tokens": int(tokens.sum()),
    }


def token_distribution(rows):
    """Integer token intervals: finer bins near the center, wider bins in the tail."""
    bounds = [(0, 5), (5, 10), (10, 15), (15, 20), (20, 30),
              (30, 50), (50, 100), (100, 150), (150, 200), (200, None)]
    distribution = []
    for lower, upper in bounds:
        count = sum(lower <= row["token_count"] and
                    (upper is None or row["token_count"] < upper) for row in rows)
        label = f"{lower}–{upper - 1}" if upper is not None else f"{lower}+"
        distribution.append((label, count, count / len(rows) * 100))
    if sum(count for _, count, _ in distribution) != len(rows):
        raise ValueError("Token intervals do not cover all rules")
    return distribution


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", type=Path, default=DEFAULT_CSV)
    parser.add_argument("--rules", type=Path, default=JUDGE / "detect_rules.json")
    parser.add_argument("--output-dir", type=Path, default=HERE / "results")
    parser.add_argument("--cache", type=Path, default=HERE / "rule_token_cache.json")
    parser.add_argument("--encoding", default="cl100k_base")
    parser.add_argument("--content-mode", choices=("after", "raw"), default="after",
                        help="after: use new lines for modified diffs; raw: tokenize original diff")
    parser.add_argument("--expected-rules", type=int, default=160)
    parser.add_argument("--alpha", type=float, default=0.05)
    args = parser.parse_args()
    if not 0 < args.alpha < 1 or args.expected_rules < 0:
        parser.error("Require 0 < alpha < 1 and expected-rules >= 0")
    rows = load_data(args.csv, args.rules, args.expected_rules)
    hits, computed = add_token_counts(rows, args.cache, args.encoding, args.content_mode)
    descriptives = describe_tokens(rows)
    tests = correlate(rows, args.alpha)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    details = []
    for row in rows:
        detail = {key: row[key] for key in ("rule_id", "project", "change_type", "content_source", "token_count")}
        detail.update({metric: f"{row[metric]:.2f}" if row[metric] is not None else ""
                       for metric in ("before", "current", "after", "after_minus_before")})
        detail["tokenized_content"] = row["tokenized_content"]
        details.append(detail)
    write_csv(args.output_dir / "rule_data.csv", details)
    write_csv(args.output_dir / "spearman_results.csv", tests)
    lines = [
        "Rule complexity and compliance: Spearman correlation", "",
        f"Rules: {len(rows)}. Complexity: original rule text token count; encoding={args.encoding}.",
        f"Content mode: {args.content_mode}. Extraction: {dict(Counter(r['content_source'] for r in rows))}.",
        "In after mode, modified +/- snippets retain only new lines and unmarked context; diff prefixes are removed.",
        "Modified rules without +/- snippets retain the supplied description, which is not a recovered full rule version.",
        "", "Token complexity: descriptive statistics (all matched rules)",
        "All statistics are in tokens; standard deviation uses N-1; quantiles use linear interpolation.",
        *[f"{name}: {value if isinstance(value, int) else format(value, '.2f') if value is not None else 'NA'}"
          for name, value in descriptives.items()],
        "", "Token count distribution (all matched rules)",
        "Integer intervals include both displayed endpoints; intervals do not overlap.",
        "Token interval\tRules\tPercentage",
        *[f"{label}\t{count}\t{percent:.2f}%" for label, count, percent in token_distribution(rows)],
        "", "Spearman correlations",
        "Rates: CSV 前5% -> before; 本次% -> current; 后5% -> after; change = after - before.",
        "Rates are proportions (0–1), displayed to two decimals; correlations and differences use source precision.",
        "Missing rates are excluded separately for each test, never replaced with zero.",
        "Test: two-sided Spearman rank correlation (average ranks for ties; SciPy asymptotic p values).",
        f"Significance: unadjusted p < {args.alpha}; four tests, no multiple-testing correction.", "",
        "Metric\tN\tExcluded\tSpearman rho\tp-value\tResult",
    ]
    for test in tests:
        rho = f"{test['spearman_rho']:.2f}" if test["spearman_rho"] is not None else "NA"
        p = f"{test['p_value']:.6g}" if test["p_value"] is not None else "NA"
        lines.append(f"{test['metric']}\t{test['n']}\t{test['excluded']}\t{rho}\t{p}\t{test['result']}")
    lines.extend(["", "Token length is a proxy for complexity. Correlation does not imply causation.",
                  "Rules may be clustered within projects; these tests do not adjust for clustering.",
                  "CSV source rates are already rounded to 4 decimals; display rounding is not used for inference.",
                  f"Token cache: hits={hits}, computed={computed}; {args.cache.resolve()}",
                  f"Source CSV: {args.csv.resolve()}", f"Rule source: {args.rules.resolve()}",
                  f"Versions: scipy={version('scipy')}, tiktoken={version('tiktoken')}",
                  f"Generated (UTC): {datetime.now(timezone.utc).isoformat()}"])
    summary = "\n".join(lines) + "\n"
    (args.output_dir / "summary.txt").write_text(summary, encoding="utf-8")
    print(summary)


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, ImportError) as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)
