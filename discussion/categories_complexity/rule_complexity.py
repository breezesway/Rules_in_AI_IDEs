"""Compare rule-body token counts by second-level category. Run this script directly; use --help for options."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import platform
import statistics
import sys
import time
from collections import defaultdict
from datetime import datetime, timezone
from importlib.metadata import version
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[1]
DEFAULT_DATA_DIR = REPO_ROOT / "rq1_rules" / "rules"
DEFAULT_OUTPUT_DIR = HERE / "rule_complexity_results"
DEFAULT_CACHE = HERE / "rule_token_cache.json"
CACHE_SCHEMA = 1


def write_json(path, data):
    """Write via a temporary file and atomic replace so an interrupt cannot corrupt an existing cache."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False)
                    + "\n", encoding="utf-8")
    temp.replace(path)


def write_csv(path, rows):
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def load_categories(prompt):
    """Load the taxonomy table and check that each second-level name maps to one first-level name.

    The markdown table starts at a header cell named "First-level category".
    Column 2 is the first-level name and column 4 is the second-level name.
    """
    categories = {}
    in_category_table = False
    for line in prompt.read_text(encoding="utf-8").splitlines():
        if not line.strip().startswith("|"):
            if in_category_table:
                break
            continue
        cells = [cell.strip().replace("**", "") for cell in line.split("|")]
        if not in_category_table:
            in_category_table = len(cells) >= 6 and cells[2] == "First-level category"
            continue
        if len(cells) < 6:
            continue
        first, second = cells[2], cells[4]
        if not first or first == "First-level category" or set(first) <= set(" :-"):
            continue
        key = second.casefold()
        if key in categories and categories[key][0] != first:
            raise ValueError(f"Second-level category maps to more than one first-level category: {second}")
        categories[key] = (first, second)
    if not categories:
        raise ValueError(f"No categories were read from the taxonomy table: {prompt}")
    return categories


def load_rules(data_dir, categories=None):
    """Load rule JSON files.

    When categories is omitted, the taxonomy is taken from the JSON itself.
    Each second-level name may still belong to only one first-level name.
    """
    files = sorted(data_dir.rglob("*.json"))
    if not files:
        raise ValueError(f"No JSON files found: {data_dir}")
    rows, seen, inferred = [], set(), {}
    for path in files:
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, list):
            raise ValueError(f"JSON top level is not an array: {path}")
        for index, obj in enumerate(data, 1):
            location = f"{path} item {index}"
            if not isinstance(obj, dict):
                raise ValueError(f"Rule is not an object: {location}")
            for field in ("id", "content", "first_level", "second_level", "project", "file"):
                if not isinstance(obj.get(field), str) or not obj[field].strip():
                    raise ValueError(f"{field} is missing, not a string, or empty: {location}")
            if obj["id"] in seen:
                raise ValueError(f"Duplicate rule ID: {obj['id']} ({location})")
            seen.add(obj["id"])
            key = obj["second_level"].strip().casefold()
            observed = (obj["first_level"].strip(), obj["second_level"].strip())
            if categories is None:
                previous = inferred.get(key)
                if previous is not None and previous[0].casefold() != observed[0].casefold():
                    raise ValueError(
                        f"Second-level category maps to more than one first-level category: {observed[1]}")
                category = inferred.setdefault(key, observed)
            else:
                category = categories.get(key)
                if category is None or category[0].casefold() != observed[0].casefold():
                    raise ValueError(f"Category is invalid or the first- and second-level names do not match: {location}")
            # Keep the body unchanged: do not strip it or append labels, filenames, or JSON metadata.
            content = obj["content"]
            rows.append({
                "id": obj["id"], "project": obj["project"], "file": obj["file"],
                "source_json": path.relative_to(data_dir).as_posix(),
                "first_level": category[0], "second_level": category[1],
                "content": content,
                "content_sha256": hashlib.sha256(content.encode("utf-8")).hexdigest(),
            })
    return rows, len(files)


def count_tokens(rows, cache_path, encoding_name):
    import tiktoken

    metadata = {"schema": CACHE_SCHEMA, "encoding": encoding_name,
                "tiktoken_version": version("tiktoken"),
                "method": "encode_ordinary(content); no normalization"}
    cache = {"metadata": metadata, "rules": {}}
    if cache_path.exists():
        previous = json.loads(cache_path.read_text(encoding="utf-8"))
        if not isinstance(previous, dict):
            raise ValueError(f"Invalid cache format: {cache_path}")
        if previous.get("metadata") == metadata:
            if not isinstance(previous.get("rules"), dict):
                raise ValueError(f"Invalid cache rules format: {cache_path}")
            cache = previous
        else:
            print("Cached encoding, library version, or counting method changed; recounting.", flush=True)

    hits, computed = 0, 0
    encoder = None  # Skip loading the vocabulary, and any vocabulary download, when every row hits the cache.
    try:
        for index, row in enumerate(rows, 1):
            entry = cache["rules"].get(row["id"])
            valid = (isinstance(entry, dict)
                     and entry.get("content_sha256") == row["content_sha256"]
                     and type(entry.get("token_count")) is int
                     and entry["token_count"] > 0)
            if valid:
                hits += 1
                row["token_count"] = entry["token_count"]
            else:
                if encoder is None:
                    encoder = tiktoken.get_encoding(encoding_name)
                row["token_count"] = len(encoder.encode_ordinary(row["content"]))
                cache["rules"][row["id"]] = {
                    "content_sha256": row["content_sha256"],
                    "token_count": row["token_count"],
                }
                computed += 1
                if computed % 500 == 0:
                    write_json(cache_path, cache)
            if index % 1000 == 0:
                print(f"Token progress: {index}/{len(rows)}", flush=True)
    finally:
        # Keep entries already counted if the user interrupts or counting fails.
        write_json(cache_path, cache)
    return {"hits": hits, "computed": computed, "path": str(cache_path)}, metadata


def analyze(rows, alpha):
    import numpy as np
    from scipy.stats import kruskal

    groups = defaultdict(list)
    parents = {}
    for row in rows:
        groups[row["second_level"]].append(row["token_count"])
        parents[row["second_level"]] = row["first_level"]
    names = sorted(groups)
    n, k = len(rows), len(names)
    if k < 2 or n <= k:
        raise ValueError("Kruskal-Wallis requires at least two groups, and the total sample size must exceed the number of groups.")
    summaries = []
    for name in names:
        values = groups[name]
        q1, q3 = np.percentile(values, [25, 75])
        summaries.append({
            "first_level": parents[name], "second_level": name, "n": len(values),
            "mean_tokens": statistics.mean(values),
            "median_tokens": statistics.median(values),
            "sd_tokens": statistics.stdev(values) if len(values) > 1 else None,
            "q1_tokens": float(q1), "q3_tokens": float(q3),
            "min_tokens": min(values), "max_tokens": max(values),
        })
    all_identical = len({row["token_count"] for row in rows}) == 1
    if all_identical:
        # SciPy raises when every value is identical; this degenerate case uses H=0 and p=1.
        h, p = 0.0, 1.0
    else:
        test = kruskal(*(groups[name] for name in names), nan_policy="raise")
        h, p = float(test.statistic), float(test.pvalue)
    eta_raw = (h - k + 1) / (n - k)
    eta = max(0.0, eta_raw)  # A finite-sample estimate can be negative; the raw value is kept as well.
    result = {
        "test": "Kruskal-Wallis H (tie-corrected; chi-square approximation)",
        "grouping": "second_level", "metric": "content token count",
        "n": n, "k": k, "df": k - 1, "H": h, "p_value": p,
        "alpha": alpha, "significant": p < alpha,
        "decision": "Significant: reject the null hypothesis that the category distributions are identical" if p < alpha
                    else "Not significant: do not reject the null hypothesis that the category distributions are identical",
        "eta_squared_H": eta,
        "eta_squared_H_raw": eta_raw,
        "eta_squared_H_formula": "max(0, (H - k + 1) / (n - k))",
        "rank_epsilon_squared": h / (n - 1),
        "rank_epsilon_squared_formula": "H / (n - 1)",
        "all_values_identical": all_identical,
        "small_groups_n_lt_5": [name for name in names if len(groups[name]) < 5],
    }
    return summaries, result


def cliffs_delta(left, right):
    """P(left > right) - P(left < right). Ties contribute 0."""
    import numpy as np

    right_sorted = np.sort(right)
    wins = np.searchsorted(right_sorted, left, side="left").sum()
    losses = (len(right_sorted) - np.searchsorted(right_sorted, left, side="right")).sum()
    return float((wins - losses) / (len(left) * len(right)))


def format_p(p):
    return "<0.01" if p < 0.01 else f"{p:.2f}"


def dunn_holm(rows, alpha):
    """Two-sided Dunn test: one ranking of all observations, tie correction, Holm correction over every category pair.

    Var(rank) = N(N+1)/12 - sum(t^3-t)/(12(N-1)).
    The tie correction matches Glantz's correction in scikit-posthocs posthoc_dunn.
    The sign of z is the mean rank of group_1 minus the mean rank of group_2.
    """
    import numpy as np
    from scipy.stats import norm, rankdata
    from statsmodels.stats.multitest import multipletests
    from itertools import combinations

    values = np.asarray([row["token_count"] for row in rows])
    ranks = rankdata(values, method="average")
    groups = defaultdict(list)
    for row, rank in zip(rows, ranks):
        groups[row["second_level"]].append(float(rank))
    names = sorted(groups)
    n = len(rows)
    if len(names) < 2:
        raise ValueError("The Dunn test requires at least two categories")
    _, ties = np.unique(values, return_counts=True)
    tie_sum = sum(int(t) ** 3 - int(t) for t in ties)
    variance = n * (n + 1) / 12.0 - tie_sum / (12.0 * (n - 1))
    mean_ranks = {name: statistics.mean(groups[name]) for name in names}
    mean_tokens = {name: statistics.mean([row["token_count"] for row in rows
                                        if row["second_level"] == name]) for name in names}
    tokens = defaultdict(list)
    for row in rows:
        tokens[row["second_level"]].append(row["token_count"])
    pairs = []
    for left, right in combinations(names, 2):
        n1, n2 = len(groups[left]), len(groups[right])
        difference = mean_ranks[left] - mean_ranks[right]
        se = float(np.sqrt(max(0.0, variance) * (1.0 / n1 + 1.0 / n2)))
        # Identical values leave no testable difference, matching the omnibus degenerate case.
        z = difference / se if se > 0 else 0.0
        pairs.append({
            "group_1": left, "group_2": right, "n_1": n1, "n_2": n2,
            "mean_tokens_1": mean_tokens[left], "mean_tokens_2": mean_tokens[right],
            "mean_rank_1": mean_ranks[left], "mean_rank_2": mean_ranks[right],
            "mean_rank_difference_1_minus_2": difference,
            "z_1_minus_2": z, "p_raw": float(2 * norm.sf(abs(z))),
            "cliffs_delta_1_minus_2": cliffs_delta(tokens[left], tokens[right]),
        })
    adjusted = multipletests([pair["p_raw"] for pair in pairs], method="holm")[1]
    for pair, p_holm in zip(pairs, adjusted):
        pair["p_holm"] = float(p_holm)
        pair["significant_holm"] = bool(p_holm < alpha)
        pair["higher_mean_rank_group"] = (pair["group_1"] if pair["z_1_minus_2"] > 0
                                          else pair["group_2"] if pair["z_1_minus_2"] < 0
                                          else "equal")
    pairs.sort(key=lambda pair: (pair["p_holm"], pair["p_raw"], pair["group_1"], pair["group_2"]))
    metadata = {
        "test": "Dunn (two-sided normal approximation, pooled average ranks, tie-corrected)",
        "correction": "Holm step-down Bonferroni; family = all unordered category pairs",
        "alpha": alpha, "comparisons": len(pairs),
        "significant_pairs": sum(pair["significant_holm"] for pair in pairs),
        "not_significant_pairs": sum(not pair["significant_holm"] for pair in pairs),
        "pooled_rank_variance": variance,
        "direction_note": "Direction refers to mean-rank size, not a test of mean differences and not an effect size.",
    }
    return pairs, metadata


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=DEFAULT_DATA_DIR)
    parser.add_argument("--prompt", type=Path, default=None,
                        help="Optional taxonomy table. When omitted, use the first- and second-level categories already stored in the JSON.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--cache", type=Path, default=DEFAULT_CACHE)
    parser.add_argument("--encoding", default="cl100k_base")
    parser.add_argument("--alpha", type=float, default=0.05)
    parser.add_argument("--expected-rules", type=int, default=7310,
                        help="Expected rule count; 0 skips the check")
    parser.add_argument("--expected-categories", type=int, default=25,
                        help="Expected second-level category count; 0 skips the check")
    args = parser.parse_args()
    if not 0 < args.alpha < 1:
        parser.error("alpha must be between 0 and 1")
    if args.expected_rules < 0 or args.expected_categories < 0:
        parser.error("Expected counts must not be negative")
    args.data_dir = args.data_dir.expanduser().resolve()
    if not args.data_dir.is_dir():
        parser.error(f"Input path does not exist or is not a directory: {args.data_dir}")
    if args.prompt is not None:
        args.prompt = args.prompt.expanduser().resolve()
        if not args.prompt.is_file():
            parser.error(f"Taxonomy table does not exist or is not a file: {args.prompt}")
    args.output_dir = args.output_dir.expanduser().resolve()
    if args.output_dir.exists() and not args.output_dir.is_dir():
        parser.error(f"Output path exists but is not a directory: {args.output_dir}")
    args.cache = args.cache.expanduser().resolve()
    if args.cache.exists() and not args.cache.is_file():
        parser.error(f"Cache path exists but is not a file: {args.cache}")
    if args.cache == args.output_dir or args.output_dir in args.cache.parents:
        parser.error("The cache must be stored outside the output directory")
    started = time.perf_counter()
    categories = load_categories(args.prompt) if args.prompt is not None else None
    rows, file_count = load_rules(args.data_dir, categories)
    observed_categories = len({row["second_level"] for row in rows})
    for label, actual, expected in (("rules", len(rows), args.expected_rules),
                                     ("second-level categories", observed_categories, args.expected_categories)):
        if expected and actual != expected:
            raise ValueError(f"{label} count mismatch: found {actual}, expected {expected}; stopping.")
    if not rows:
        raise ValueError("No rules to analyze")
    print(f"Read {file_count} JSON files, {len(rows)} rules, and {observed_categories} second-level categories.",
          flush=True)
    cache_stats, token_metadata = count_tokens(rows, args.cache, args.encoding)
    summaries, result = analyze(rows, args.alpha)
    pairs, posthoc = dunn_holm(rows, args.alpha)
    result["posthoc"] = posthoc
    result.update({
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "data_dir": str(args.data_dir), "json_files": file_count,
        "category_prompt": None if args.prompt is None else str(args.prompt),
        "tokenizer": token_metadata, "cache": cache_stats,
        "versions": {"python": platform.python_version(), "scipy": version("scipy"),
                     "numpy": version("numpy"), "tiktoken": version("tiktoken"),
                     "statsmodels": version("statsmodels")},
        "elapsed_seconds": time.perf_counter() - started,
        "notes": [
            "Token count is a proxy for text length and does not fully represent semantic or cognitive complexity.",
            "Kruskal-Wallis is an omnibus rank test and does not test means directly; interpret it as a location or median difference only when group distribution shapes are similar.",
            "Pairwise follow-up tests use two-sided Dunn tests with one Holm correction across all category pairs. A pair is significant when p_holm < alpha.",
            "Dunn direction describes a mean-rank difference. A non-significant pair cannot be interpreted as equivalence.",
            "Rules in the same project or file may be dependent. This test treats rules as independent observations and does not adjust for clustering.",
            "A non-significant result does not prove that the categories are the same.",
            "A p_value of 0 indicates floating-point underflow and should not be reported as a true probability of zero.",
        ],
        "references": [
            "https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.kruskal.html",
            "https://search.r-project.org/CRAN/refmans/rstatix/html/kruskal_effsize.html",
            "https://github.com/kassambara/rstatix/blob/master/R/kruskal_effesize.R",
            "https://scikit-posthocs.readthedocs.io/en/stable/generated/scikit_posthocs.posthoc_dunn.html",
            "https://www.statsmodels.org/stable/generated/statsmodels.stats.multitest.multipletests.html",
            "https://easystats.github.io/effectsize/reference/rank_biserial.html",
        ],
    })
    args.output_dir.mkdir(parents=True, exist_ok=True)
    # Order rows and columns by descending mean token count.
    ordered_summaries = sorted(summaries, key=lambda s: (-s["mean_tokens"], s["second_level"]))
    names = [s["second_level"] for s in ordered_summaries]
    means = {s["second_level"]: s["mean_tokens"] for s in ordered_summaries}
    lookup = {frozenset((pair["group_1"], pair["group_2"])): pair for pair in pairs}
    matrix = []
    for name in names:
        matrix_row = {"second_level": name}
        for other in names:
            if name == other:
                matrix_row[other] = "—"
                continue
            pair = lookup[frozenset((name, other))]
            delta = pair["cliffs_delta_1_minus_2"] * (1 if name == pair["group_1"] else -1)
            # Avoid printing -0.000. Significance uses the unrounded p value.
            delta = 0.0 if abs(delta) < 0.0005 else delta
            p_text = format_p(pair["p_holm"])
            p_text = f"p{p_text}" if p_text.startswith("<") else f"p={p_text}"
            star = " *" if pair["significant_holm"] else ""
            matrix_row[other] = (f"{p_text}{star}; δ={delta:+.3f}; "
                                 f"row mean={means[name]:.2f}; column mean={means[other]:.2f}")
        matrix.append(matrix_row)
    write_csv(args.output_dir / "dunn_holm_matrix.csv", matrix)
    lines = [
        "Rule-body token complexity", "",
        "Data and metric",
        f"Source: {args.data_dir}; {file_count} JSON files.",
        f"N={result['n']}, k={result['k']}, df={result['df']}",
        f"Only the raw content field is counted; tiktoken encoding={args.encoding}, excluding categories and other metadata.",
        "", "Tests and main results",
        "Omnibus comparison: Kruskal-Wallis H test, tie-corrected, with a chi-square approximation for the p value.",
        f"H={result['H']:.6f}, p{format_p(result['p_value']) if result['p_value'] < 0.01 else '=' + format_p(result['p_value'])}, alpha={args.alpha}",
        result["decision"],
        f"Overall effect size eta^2_H={result['eta_squared_H']:.4f}; formula=max(0, (H-k+1)/(N-k)).",
        f"Overall effect size rank epsilon^2={result['rank_epsilon_squared']:.4f}; formula=H/(N-1).",
        "Post hoc comparison: two-sided Dunn tests on average ranks of all observations, with tie correction and a normal approximation for p values.",
        f"Holm (step-down Bonferroni) correction is applied once to all {posthoc['comparisons']} unordered category pairs, controlling the family-wise error rate.",
        f"Significance uses the unrounded p_holm < {args.alpha}: "
        f"{posthoc['significant_pairs']} pairs significant, {posthoc['not_significant_pairs']} pairs not significant.",
        "", "Matrix notes: dunn_holm_matrix.csv",
        f"{len(names)}x{len(names)} data cells, plus row and column category labels; rows and columns are ordered by descending mean token count.",
        "Each cell has the form p=0.03 *; delta=+0.123; row mean=20.50; column mean=15.25.",
        "Every p is a two-sided Holm-adjusted p value. Row and column means are the arithmetic mean token counts of those categories, shown to two decimals.",
        "p is shown to two decimals, and values below 0.01 are shown as <0.01. * marks significance after correction.",
        "The asterisk uses the unrounded p value, so a cell displayed as 0.05 can still be significant. Use the asterisk.",
        "delta is Cliff's delta for the two categories, shown to three decimals, with range [-1, 1].",
        "delta = P(row-category tokens > column-category tokens) - P(row-category tokens < column-category tokens). Ties contribute 0.",
        "delta>0 means the row category tends to be longer; delta<0 means the column category tends to be longer. A larger absolute value means a larger dominance difference.",
        "delta is a separate two-group distributional effect size. It is not converted from Dunn's z and is not Holm-adjusted.",
        "The transposed cell has the same p and the opposite sign of delta. The diagonal — means a category is not tested against itself.",
        "", "Descriptive statistics by second-level category (tokens)",
        "second_level\tn\tmean\tmedian\tsd\tQ1\tQ3",
    ]
    for s in ordered_summaries:
        sd = f"{s['sd_tokens']:.2f}" if s["sd_tokens"] is not None else "NA"
        lines.append(f"{s['second_level']}\t{s['n']}\t{s['mean_tokens']:.2f}\t"
                     f"{s['median_tokens']:.2f}\t{sd}\t{s['q1_tokens']:.2f}\t{s['q3_tokens']:.2f}")
    lines.extend(["", "Interpretation and limitations", *result["notes"]])
    lines.extend(["", "Run information",
                  f"Cache hits={cache_stats['hits']}, newly computed={cache_stats['computed']}.",
                  f"Cache stored outside the results directory: {args.cache}",
                  f"Generated at (UTC): {result['created_at_utc']}",
                  "Library versions: " + json.dumps(result["versions"], ensure_ascii=False),
                  "", "Method references", *result["references"]])
    if result["small_groups_n_lt_5"]:
        lines.append("Warning: the following groups have fewer than 5 rules, so the chi-square approximation may be unreliable: "
                     f"{result['small_groups_n_lt_5']}")
    report = "\n".join(lines) + "\n"
    (args.output_dir / "summary.txt").write_text(report, encoding="utf-8")
    # Remove only known outputs from older versions of this script. Leave other files and the token cache in place.
    for old_name in ("rule_tokens.csv", "category_summary.csv", "dunn_holm_pairs.csv",
                     "dunn_holm_p_matrix.csv", "kruskal_wallis.json"):
        (args.output_dir / old_name).unlink(missing_ok=True)
    print(report)
    print(f"Results directory: {args.output_dir}")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, ImportError) as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)
