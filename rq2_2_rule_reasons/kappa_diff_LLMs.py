"""
Compute Kappa agreement on tier_1 (Unclear vs non-Unclear) across multiple reason_results files.
- Fleiss' Kappa: agreement among multiple raters (multiple files)
- Cohen's Kappa: pairwise Cohen's Kappa coefficients
"""

import json
from pathlib import Path
from typing import List, Dict, Any, Tuple
import numpy as np
from sklearn.metrics import cohen_kappa_score
from itertools import combinations

# ---------------------------------------------------------------------------
# Input filenames for Kappa computation (relative to this script's directory)
# ---------------------------------------------------------------------------
INPUT_FILES = [
    # Example:
    "reason_results_glm-5.json",
    "reason_results_qwen3-max.json",
    "reason_results_gemini-3-flash-preview.json",
]


def load_json_file(file_path: Path) -> List[Dict[Any, Any]]:
    """Load a JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            else:
                print(f"Error: {file_path} is not a JSON array")
                return []
    except json.JSONDecodeError as e:
        print(f"Error: unable to parse JSON file {file_path}: {e}")
        return []
    except Exception as e:
        print(f"Error: unable to read file {file_path}: {e}")
        return []


def calculate_fleiss_kappa(data: np.ndarray) -> Tuple[float, Dict[str, Any]]:
    """
    Compute Fleiss' Kappa.

    Args:
        data: numpy array of shape (n_items, n_raters)
              each row is an item, each column is one rater's label

    Returns:
        (kappa, stats): Kappa coefficient and summary statistics
    """
    n_items, n_raters = data.shape

    # All unique categories
    unique_categories = sorted(set(data.flatten()))
    n_categories = len(unique_categories)

    # Category -> index mapping
    category_to_idx = {cat: idx for idx, cat in enumerate(unique_categories)}

    # Count ratings per category per item
    # P[i][j] = number of raters assigning category j to item i
    P = np.zeros((n_items, n_categories))
    for i in range(n_items):
        for j in range(n_raters):
            category = data[i, j]
            cat_idx = category_to_idx[category]
            P[i, cat_idx] += 1

    # Per-item agreement Pi
    Pi = np.zeros(n_items)
    for i in range(n_items):
        sum_squared = np.sum(P[i, :] ** 2)
        Pi[i] = (sum_squared - n_raters) / (n_raters * (n_raters - 1))

    # Mean agreement Pbar across items
    Pbar = np.mean(Pi)

    # Overall category proportions Pj
    Pj = np.zeros(n_categories)
    for j in range(n_categories):
        Pj[j] = np.sum(P[:, j]) / (n_items * n_raters)

    # Expected agreement Pe
    Pe = np.sum(Pj ** 2)

    # Fleiss' Kappa
    if Pe == 1.0:
        kappa = 1.0
    else:
        kappa = (Pbar - Pe) / (1 - Pe)

    stats = {
        'n_items': n_items,
        'n_raters': n_raters,
        'n_categories': n_categories,
        'Pbar': Pbar,
        'Pe': Pe,
        'kappa': kappa,
        'category_distribution': {unique_categories[i]: float(Pj[i]) for i in range(n_categories)},
        'Pi': Pi.tolist()
    }

    return kappa, stats


def calculate_cohen_kappa(y1: List[Any], y2: List[Any]) -> Tuple[float, Dict[str, Any]]:
    """Compute Cohen's Kappa and return detailed statistics."""
    if len(y1) != len(y2):
        raise ValueError("Both lists must have the same length")

    kappa = cohen_kappa_score(y1, y2)

    # Confusion matrix
    unique_labels = sorted(set(y1 + y2))
    confusion_matrix = {}
    for label1 in unique_labels:
        for label2 in unique_labels:
            confusion_matrix[(label1, label2)] = 0

    for i in range(len(y1)):
        confusion_matrix[(y1[i], y2[i])] = confusion_matrix.get((y1[i], y2[i]), 0) + 1

    agreement_count = sum(confusion_matrix.get((label, label), 0) for label in unique_labels)
    disagreement_count = len(y1) - agreement_count

    stats = {
        'n': len(y1),
        'kappa': kappa,
        'agreement_count': agreement_count,
        'disagreement_count': disagreement_count,
        'agreement_rate': agreement_count / len(y1) if len(y1) > 0 else 0,
        'confusion_matrix': confusion_matrix
    }

    return kappa, stats


def interpret_kappa(kappa: float) -> str:
    """Interpret a Kappa coefficient."""
    if kappa < 0:
        return "No agreement (Poor)"
    elif kappa < 0.20:
        return "Slight agreement (Slight)"
    elif kappa < 0.40:
        return "Fair agreement (Fair)"
    elif kappa < 0.60:
        return "Moderate agreement (Moderate)"
    elif kappa < 0.80:
        return "Substantial agreement (Substantial)"
    else:
        return "Almost perfect agreement (Almost Perfect)"


def main():
    """Main entry point."""
    script_dir = Path(__file__).parent
    llm_filter_dir = script_dir / "LLM_filter"

    print("=" * 80)
    print("Computing Kappa for tier_1 (Unclear vs non-Unclear) across reason_results files")
    print("=" * 80)

    # Use INPUT_FILES configured at the top of the script
    result_files = []
    for name in INPUT_FILES:
        path = llm_filter_dir / name.strip()
        if path.exists():
            result_files.append(path)
        else:
            print(f"Warning: file not found, skipped: {name}")

    if len(result_files) < 2:
        print(f"\nError: at least 2 valid files are required to compute Kappa")
        print(f"Add at least 2 existing filenames to INPUT_FILES; valid files now: {len(result_files)}")
        return

    print(f"\nUsing {len(result_files)} specified file(s)")

    # Load all files
    all_data = {}
    for result_file in result_files:
        filename = result_file.name
        print(f"\nReading file: {filename}")
        data = load_json_file(result_file)
        if data:
            all_data[filename] = data
            print(f"  Loaded {len(data)} object(s)")
        else:
            print(f"  Warning: file {filename} is empty or unreadable")

    if len(all_data) < 2:
        print("\nError: at least 2 valid files are required to compute Kappa")
        return

    # Build rule_id -> binary tier_1 maps: Unclear=1, non-Unclear=0
    data_dicts = {}
    for filename, data in all_data.items():
        data_dict = {}
        for item in data:
            if 'rule_id' in item:
                rule_id = item['rule_id']
                tier_1 = item.get('tier_1', '')
                is_unclear = 1 if tier_1 == 'Unclear' else 0
                data_dict[rule_id] = is_unclear
        data_dicts[filename] = data_dict
        unclear_count = sum(1 for v in data_dict.values() if v == 1)
        print(f"  {filename}: extracted {len(data_dict)} valid tier_1 value(s), {unclear_count} Unclear")

    # Intersect rule_ids across all files
    if len(data_dicts) > 0:
        common_rule_ids = set(list(data_dicts.values())[0].keys())
        for data_dict in data_dicts.values():
            common_rule_ids &= set(data_dict.keys())

    print(f"\nCommon rule_id count: {len(common_rule_ids)}")

    if len(common_rule_ids) == 0:
        print("Error: no common rule_id values; cannot compute Kappa")
        return

    # Extract aligned values per file (sorted rule_ids for consistent order)
    sorted_rule_ids = sorted(common_rule_ids)
    all_values = {}
    for filename, data_dict in data_dicts.items():
        all_values[filename] = [data_dict[rule_id] for rule_id in sorted_rule_ids]

    # Fleiss' Kappa (requires 3+ files)
    fleiss_kappa = None
    if len(all_data) >= 3:
        print("\n" + "=" * 80)
        print("Fleiss' Kappa (multi-rater agreement)")
        print("=" * 80)

        # Each row is an item, each column is a rater
        n_items = len(sorted_rule_ids)
        n_raters = len(all_data)
        data_array = np.zeros((n_items, n_raters), dtype=int)

        filenames_list = list(all_data.keys())
        for i, rule_id in enumerate(sorted_rule_ids):
            for j, filename in enumerate(filenames_list):
                data_array[i, j] = all_values[filename][i]

        fleiss_kappa, fleiss_stats = calculate_fleiss_kappa(data_array)

        print(f"Fleiss' Kappa: {fleiss_kappa:.4f}")
        print(f"Interpretation: {interpret_kappa(fleiss_kappa)}")
        print(f"\nDetailed statistics:")
        print(f"  Items (n_items): {fleiss_stats['n_items']}")
        print(f"  Raters (n_raters): {fleiss_stats['n_raters']}")
        print(f"  Categories (n_categories): {fleiss_stats['n_categories']}")
        print(f"  Mean agreement (Pbar): {fleiss_stats['Pbar']:.4f}")
        print(f"  Expected agreement (Pe): {fleiss_stats['Pe']:.4f}")
        print(f"\nCategory distribution:")
        for category, prob in fleiss_stats['category_distribution'].items():
            category_name = "Unclear" if category == 1 else "non-Unclear"
            print(f"  {category_name} ({category}): {prob:.2%}")
    else:
        print("\n" + "=" * 80)
        print("Fleiss' Kappa (multi-rater agreement)")
        print("=" * 80)
        print(f"Note: Fleiss' Kappa requires 3 or more raters")
        print(f"Only {len(all_data)} file(s) available; skipping Fleiss' Kappa")
        print("=" * 80)

    # Pairwise Cohen's Kappa
    print("\n" + "=" * 80)
    print("Cohen's Kappa (pairwise comparison)")
    print("=" * 80)

    filenames_list = list(all_data.keys())
    pairwise_results = []

    for (i, filename1), (j, filename2) in combinations(enumerate(filenames_list), 2):
        values1 = all_values[filename1]
        values2 = all_values[filename2]

        kappa, stats = calculate_cohen_kappa(values1, values2)
        pairwise_results.append({
            'file1': filename1,
            'file2': filename2,
            'kappa': kappa,
            'stats': stats
        })

        short_name1 = filename1.replace('reason_results_', '').replace('.json', '')
        short_name2 = filename2.replace('reason_results_', '').replace('.json', '')

        print(f"\n{short_name1} vs {short_name2}")
        print(f"  Cohen's Kappa: {kappa:.4f}")
        print(f"  Interpretation: {interpret_kappa(kappa)}")
        print(f"  Agreement: {stats['agreement_count']}/{stats['n']} ({stats['agreement_rate']:.2%})")
        print(f"  Disagreement: {stats['disagreement_count']}/{stats['n']}")

        print(f"  Confusion matrix:")
        print("    file1 \\ file2", end="")
        for label in [0, 1]:
            label_name = "non-Unclear" if label == 0 else "Unclear"
            print(f"  {label_name:>10}", end="")
        print()
        for label1 in [0, 1]:
            label1_name = "non-Unclear" if label1 == 0 else "Unclear"
            print(f"    {label1_name:>15}", end="")
            for label2 in [0, 1]:
                count = stats['confusion_matrix'].get((label1, label2), 0)
                print(f"  {count:>10}", end="")
            print()

    # Summary
    print("\n" + "=" * 80)
    print("Summary")
    print("=" * 80)

    if fleiss_kappa is not None:
        print(f"Fleiss' Kappa ({len(all_data)} raters): {fleiss_kappa:.4f} - {interpret_kappa(fleiss_kappa)}")
    else:
        print(f"Fleiss' Kappa: not computed (requires 3 or more files)")

    print("\nPairwise Cohen's Kappa matrix:")
    if pairwise_results:
        avg_kappa = np.mean([r['kappa'] for r in pairwise_results])
        print(f"  Mean Cohen's Kappa: {avg_kappa:.4f}\n")

        kappa_matrix = {}
        for result in pairwise_results:
            file1 = result['file1']
            file2 = result['file2']
            kappa = result['kappa']
            if file1 not in kappa_matrix:
                kappa_matrix[file1] = {}
            if file2 not in kappa_matrix:
                kappa_matrix[file2] = {}
            kappa_matrix[file1][file2] = kappa
            kappa_matrix[file2][file1] = kappa  # symmetric matrix

        all_filenames = sorted(filenames_list)

        short_names = [f.replace("reason_results_", "").replace(".json", "") for f in all_filenames]
        max_short_name_len = max(len(sn) for sn in short_names) if short_names else 12
        col_width = max(max_short_name_len, 12)

        # Table header
        print(" " * (col_width + 2), end="")
        for filename in all_filenames:
            short_name = filename.replace("reason_results_", "").replace(".json", "")
            print(f"{short_name:>12}", end="")
        print()

        print(" " * (col_width + 2) + "-" * (12 * len(all_filenames)))

        # Matrix body
        for filename1 in all_filenames:
            short_name1 = filename1.replace("reason_results_", "").replace(".json", "")
            print(f"{short_name1:>{col_width}}", end="  ")
            for filename2 in all_filenames:
                if filename1 == filename2:
                    print(f"{1.0000:>12.4f}", end="")
                else:
                    kappa = kappa_matrix.get(filename1, {}).get(filename2, 0.0)
                    print(f"{kappa:>12.4f}", end="")
            print()
    else:
        print("  No pairwise comparison results")

    print("=" * 80)


if __name__ == "__main__":
    main()
