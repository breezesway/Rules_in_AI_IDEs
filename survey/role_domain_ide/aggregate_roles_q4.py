from __future__ import annotations

from collections import Counter
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
RESULTS_DIR = BASE_DIR / "survey_results"
ENGLISH_XLSX = RESULTS_DIR / "Survey on AI IDE Rules_English.xlsx"
CHINESE_XLSX = RESULTS_DIR / "Survey on AI IDE Rules_Chinese.xlsx"

ROLE_COUNTS_CSV = Path(__file__).resolve().parent / "q4_role_counts.csv"
OTHER_DETAILS_CSV = Path(__file__).resolve().parent / "q4_other_details.csv"

FIXED_ENGLISH_ROLES = [
    "Software Developer / Engineer",
    "System / Software Architect",
    "Tech Lead / Engineering Manager",
    "DevOps / SRE",
    "QA / Test Engineer",
    "Product / Project Manager",
    "Student / Researcher",
]

CHINESE_TO_ENGLISH_ROLE = {
    "软件开发工程师": "Software Developer / Engineer",
    "系统/软件架构师": "System / Software Architect",
    "技术主管/工程经理": "Tech Lead / Engineering Manager",
    "运维/可靠性工程师": "DevOps / SRE",
    "测试/质量保证工程师": "QA / Test Engineer",
    "产品/项目经理": "Product / Project Manager",
    "学生/学术研究人员": "Student / Researcher",
}


def _pick_column(columns: list[str], starts_with: str | None = None, contains: str | None = None) -> str:
    for col in columns:
        col_str = str(col)
        if starts_with and col_str.startswith(starts_with):
            return col_str
        if contains and contains in col_str:
            return col_str
    raise ValueError("Cannot find target column in worksheet.")


def main() -> None:
    english_df = pd.read_excel(ENGLISH_XLSX)
    chinese_df = pd.read_excel(CHINESE_XLSX, sheet_name="同步数据表")

    role_counter: Counter[str] = Counter()
    other_entries: list[str] = []

    # English Q4: comma-separated multi-select in one column.
    english_q4_col = _pick_column(list(english_df.columns), starts_with="Q4")
    for value in english_df[english_q4_col].dropna().astype(str):
        options = [item.strip() for item in value.split(",") if item.strip()]
        for option in options:
            if option in FIXED_ENGLISH_ROLES:
                role_counter[option] += 1
            else:
                role_counter["Other"] += 1
                other_entries.append(option)

    # Chinese Q4: 7 fixed option columns + other marker + other free-text column.
    for zh_role, en_role in CHINESE_TO_ENGLISH_ROLE.items():
        col = _pick_column(list(chinese_df.columns), contains=f":{zh_role}")
        role_counter[en_role] += int(chinese_df[col].notna().sum())

    chinese_other_col = _pick_column(list(chinese_df.columns), contains=":其他____")
    chinese_other_text_col = _pick_column(list(chinese_df.columns), contains=":其他____[选项填空]")
    chinese_other_count = int(chinese_df[chinese_other_col].notna().sum())
    role_counter["Other"] += chinese_other_count

    chinese_other_texts = chinese_df[chinese_other_text_col].dropna().astype(str).str.strip()
    for text in chinese_other_texts:
        if text:
            other_entries.append(text)

    role_rows = [{"role": role, "count": int(role_counter.get(role, 0))} for role in FIXED_ENGLISH_ROLES]
    role_rows.append({"role": "Other", "count": int(role_counter.get("Other", 0))})
    pd.DataFrame(role_rows).to_csv(ROLE_COUNTS_CSV, index=False, encoding="utf-8")

    other_counter = Counter(entry for entry in other_entries if entry)
    other_rows = [{"other_role_text": text, "count": int(cnt)} for text, cnt in other_counter.most_common()]
    pd.DataFrame(other_rows).to_csv(OTHER_DETAILS_CSV, index=False, encoding="utf-8")

    print(f"Saved: {ROLE_COUNTS_CSV}")
    print(f"Saved: {OTHER_DETAILS_CSV}")


if __name__ == "__main__":
    main()
