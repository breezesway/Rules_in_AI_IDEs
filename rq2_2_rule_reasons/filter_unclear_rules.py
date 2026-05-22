"""
Filter out rules that appear as Unclear in any input file.
If a rule is labeled Unclear in at least one file (Unclear count >= 1), drop it.
"""

import json
from pathlib import Path
from typing import Dict, List
from collections import defaultdict

# ---------------------------------------------------------------------------
# Input file list: add reason-result JSON filenames to include in filtering
# ---------------------------------------------------------------------------
REASON_RESULT_FILES = [
    "reason_results_gemini-3-flash-preview.json",
    "reason_results_glm-5.json",
    "reason_results_qwen3-max.json",
]


def load_reason_results(file_path: Path) -> List[Dict]:
    """Load a reason_results JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if not isinstance(data, list):
            return []
        return data
    except Exception as e:
        print(f"Warning: unable to read file {file_path}: {e}")
        return []


def main():
    """Main entry point."""
    script_dir = Path(__file__).parent
    llm_filter_dir = script_dir / "LLM_filter"

    # Use the configured file list
    result_files = []
    for name in REASON_RESULT_FILES:
        path = llm_filter_dir / name.strip()
        if not path.exists():
            print(f"Warning: file not found, skipped: {path}")
            continue
        result_files.append(path)

    if not result_files:
        print("No valid files found. Check REASON_RESULT_FILES at the top of the script.")
        return

    print(f"Using {len(result_files)} reason result file(s)\n")

    # Per-file data keyed by rule_id
    all_data_by_rule: Dict[str, Dict[str, Dict]] = defaultdict(dict)  # {rule_id: {file_name: rule_data}}
    # tier_1 values per rule_id across files
    rule_tier1_map: Dict[str, Dict[str, str]] = defaultdict(dict)  # {rule_id: {file_name: tier_1}}

    # Read all files
    for result_file in result_files:
        model_name = result_file.stem.replace('reason_results_', '')
        print(f"Reading file: {result_file.name}")

        data = load_reason_results(result_file)
        if not data:
            print(f"  Warning: file is empty or invalid\n")
            continue

        # Record each rule's data and tier_1
        for item in data:
            rule_id = item.get('rule_id')
            if rule_id:
                all_data_by_rule[rule_id][model_name] = item
                tier_1 = item.get('tier_1', '')
                rule_tier1_map[rule_id][model_name] = tier_1

        print(f"  Loaded {len(data)} rule(s)\n")

    # All rule_ids seen in at least one file
    all_rule_ids = set(rule_tier1_map.keys())
    print(f"Rules appearing in {len(result_files)} file(s): {len(all_rule_ids)}\n")

    # Count how many files label each rule as Unclear
    rule_unclear_counts = {}
    for rule_id in all_rule_ids:
        unclear_count = sum(1 for tier1 in rule_tier1_map[rule_id].values() if tier1 == 'Unclear')
        rule_unclear_counts[rule_id] = unclear_count

    # Keep rules with Unclear < 1 (never Unclear in any file)
    filtered_rule_ids = [rule_id for rule_id in all_rule_ids if rule_unclear_counts[rule_id] < 1]

    print("=" * 80)
    print("Filter summary:")
    print("=" * 80)
    print(f"Total rules: {len(all_rule_ids)}")
    print(f"Rules with Unclear (filtered out): {len(all_rule_ids) - len(filtered_rule_ids)}")
    print(f"Rules kept (Unclear in no file): {len(filtered_rule_ids)}")
    print()

    # Unclear count distribution
    unclear_distribution = {}
    for rule_id in all_rule_ids:
        count = rule_unclear_counts[rule_id]
        unclear_distribution[count] = unclear_distribution.get(count, 0) + 1

    print("Unclear count distribution:")
    for unclear_count in sorted(unclear_distribution.keys()):
        rule_count = unclear_distribution[unclear_count]
        status = "(filtered)" if unclear_count >= 1 else "(kept)"
        print(f"  {unclear_count} Unclear: {rule_count} rule(s) {status}")
    print()

    # Collect retained rules (use first file's row as representative)
    filtered_rules = []
    first_file_stem = result_files[0].stem.replace('reason_results_', '')
    for rule_id in sorted(filtered_rule_ids):
        if rule_id in all_data_by_rule:
            file_names = list(all_data_by_rule[rule_id].keys())
            use_name = first_file_stem if first_file_stem in file_names else file_names[0]
            filtered_rules.append(all_data_by_rule[rule_id][use_name])

    # Save output
    output_file = script_dir / 'reason_results_filtered_4.json'
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(filtered_rules, f, ensure_ascii=False, indent=2)
        print(f"Saved {len(filtered_rules)} rule(s) to: {output_file.name}")
    except Exception as e:
        print(f"Error: failed to save file: {e}")

    print("="*80)


if __name__ == '__main__':
    main()
