from __future__ import annotations

from collections import Counter
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
RESULTS_DIR = BASE_DIR / "survey_results"
ENGLISH_XLSX = RESULTS_DIR / "Survey on AI IDE Rules_English.xlsx"
CHINESE_XLSX = RESULTS_DIR / "Survey on AI IDE Rules_Chinese.xlsx"

COUNTS_CSV = Path(__file__).resolve().parent / "q6_ide_usage_counts.csv"
OTHER_CSV = Path(__file__).resolve().parent / "q6_ide_usage_other_details.csv"

FIXED_IDE_OPTIONS = [
    "Cursor",
    "Windsurf (by Codeium)",
    "Trae (by ByteDance)",
    "Qoder (by Alibaba)",
    "Kiro (by Amazon)",
    "Antigravity (by Google)",
    "VS Code + Copilot (by Microsoft)",
]

ENGLISH_ALIAS_TO_CANONICAL = {
    "Antigravity ( by Google)": "Antigravity (by Google)",
    "Antigravity": "Antigravity (by Google)",
    "Kiro": "Kiro (by Amazon)",
}

CHINESE_TO_ENGLISH_OPTION = {
    "Cursor": "Cursor",
    "Windsurf (by Codeium)": "Windsurf (by Codeium)",
    "Trae (by ByteDance)": "Trae (by ByteDance)",
    "Qoder (by Alibaba)": "Qoder (by Alibaba)",
    "Kiro (by Amazon)": "Kiro (by Amazon)",
    "Antigravity (by Google)": "Antigravity (by Google)",
    "VS Code + Copilot (by Microsoft)": "VS Code + Copilot (by Microsoft)",
}


def _pick_column(columns: list[str], *, starts_with: str | None = None, contains: str | None = None) -> str:
    for col in columns:
        col_str = str(col)
        if starts_with and col_str.startswith(starts_with):
            return col_str
        if contains and contains in col_str:
            return col_str
    raise ValueError("Cannot find target column in worksheet.")


def _canonicalize_english_q6_option(option: str) -> str:
    normalized = option.strip()
    return ENGLISH_ALIAS_TO_CANONICAL.get(normalized, normalized)


def main() -> None:
    english_df = pd.read_excel(ENGLISH_XLSX)
    chinese_df = pd.read_excel(CHINESE_XLSX, sheet_name="同步数据表")

    option_counter: Counter[str] = Counter()
    other_entries: list[str] = []

    # English Q6: one comma-separated multi-select column.
    english_q6_col = _pick_column(list(english_df.columns), contains="Q6.")
    for value in english_df[english_q6_col].dropna().astype(str):
        options = [item.strip() for item in value.split(",") if item.strip()]
        for option in options:
            canonical_option = _canonicalize_english_q6_option(option)
            if canonical_option in FIXED_IDE_OPTIONS:
                option_counter[canonical_option] += 1
            else:
                option_counter["Other"] += 1
                other_entries.append(canonical_option)

    # Chinese Q6: 7 fixed option columns + other marker + other free-text column.
    q6_columns = [str(col) for col in chinese_df.columns if "Q6." in str(col)]

    for zh_option, en_option in CHINESE_TO_ENGLISH_OPTION.items():
        col = _pick_column(q6_columns, contains=f":{zh_option}")
        option_counter[en_option] += int(chinese_df[col].notna().sum())

    chinese_other_col = _pick_column(q6_columns, contains=":其他____")
    chinese_other_text_col = _pick_column(q6_columns, contains=":其他____[选项填空]")
    option_counter["Other"] += int(chinese_df[chinese_other_col].notna().sum())

    chinese_other_texts = chinese_df[chinese_other_text_col].dropna().astype(str).str.strip()
    for text in chinese_other_texts:
        if text:
            other_entries.append(text)

    rows = [{"ide": ide, "count": int(option_counter.get(ide, 0))} for ide in FIXED_IDE_OPTIONS]
    rows.append({"ide": "Other", "count": int(option_counter.get("Other", 0))})
    pd.DataFrame(rows).to_csv(COUNTS_CSV, index=False, encoding="utf-8")

    other_counter = Counter(item for item in other_entries if item)
    other_rows = [{"other_ide_text": text, "count": int(cnt)} for text, cnt in other_counter.most_common()]
    pd.DataFrame(other_rows).to_csv(OTHER_CSV, index=False, encoding="utf-8")

    print(f"Saved: {COUNTS_CSV}")
    print(f"Saved: {OTHER_CSV}")


if __name__ == "__main__":
    main()
