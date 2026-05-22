from __future__ import annotations

from collections import Counter
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
RESULTS_DIR = BASE_DIR / "results"
ENGLISH_XLSX = RESULTS_DIR / "Survey on AI IDE Rules_English.xlsx"
CHINESE_XLSX = RESULTS_DIR / "Survey on AI IDE Rules_Chinese.xlsx"

COUNTS_CSV = Path(__file__).resolve().parent / "q7_rule_file_time_counts.csv"
OTHER_CSV = Path(__file__).resolve().parent / "q7_rule_file_time_other_details.csv"

FIXED_TIME_OPTIONS = [
    "Less than 1 month",
    "1 – 3 months",
    "3 – 6 months",
    "6 months – 1 year",
    "More than 1 year",
]

CHINESE_TO_ENGLISH_TIME = {
    "少于 1 个月": "Less than 1 month",
    "1 - 3 个月": "1 – 3 months",
    "3 - 6 个月": "3 – 6 months",
    "6 个月 - 1 年": "6 months – 1 year",
    "超过 1 年": "More than 1 year",
}


def _pick_column(columns: list[str], *, starts_with: str | None = None, contains: str | None = None) -> str:
    for col in columns:
        col_str = str(col)
        if starts_with and col_str.startswith(starts_with):
            return col_str
        if contains and contains in col_str:
            return col_str
    raise ValueError("Cannot find target column in worksheet.")


def _normalize(series: pd.Series) -> pd.Series:
    return series.dropna().astype(str).str.strip()


def main() -> None:
    english_df = pd.read_excel(ENGLISH_XLSX)
    chinese_df = pd.read_excel(CHINESE_XLSX, sheet_name="同步数据表")

    counter: Counter[str] = Counter()
    other_entries: list[str] = []

    # English Q7: single-select in one column.
    english_q7_col = _pick_column(list(english_df.columns), starts_with="Q7")
    for option in _normalize(english_df[english_q7_col]):
        if option in FIXED_TIME_OPTIONS:
            counter[option] += 1
        else:
            other_entries.append(option)

    # Chinese Q7: single-select column + optional free-text for other.
    q7_columns = [str(col) for col in chinese_df.columns if str(col).startswith("8.Q7.")]
    chinese_q7_col = next(col for col in q7_columns if "选项填空" not in col)
    chinese_q7_text_col = next((col for col in q7_columns if "选项填空" in col), None)

    for option in _normalize(chinese_df[chinese_q7_col]):
        mapped = CHINESE_TO_ENGLISH_TIME.get(option)
        if mapped:
            counter[mapped] += 1
        else:
            # Keep other answers only in the details CSV.
            other_entries.append(option)

    if chinese_q7_text_col:
        for text in _normalize(chinese_df[chinese_q7_text_col]):
            if text:
                other_entries.append(text)

    rows = [{"rule_file_usage_time": opt, "count": int(counter.get(opt, 0))} for opt in FIXED_TIME_OPTIONS]
    pd.DataFrame(rows).to_csv(COUNTS_CSV, index=False, encoding="utf-8")

    other_counter = Counter(item for item in other_entries if item)
    other_rows = [{"other_time_text": text, "count": int(cnt)} for text, cnt in other_counter.most_common()]
    pd.DataFrame(other_rows).to_csv(OTHER_CSV, index=False, encoding="utf-8")

    print(f"Saved: {COUNTS_CSV}")
    print(f"Saved: {OTHER_CSV}")


if __name__ == "__main__":
    main()
