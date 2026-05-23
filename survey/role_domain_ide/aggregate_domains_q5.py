from __future__ import annotations

from collections import Counter
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
RESULTS_DIR = BASE_DIR / "survey_results"
ENGLISH_XLSX = RESULTS_DIR / "Survey on AI IDE Rules_English.xlsx"
CHINESE_XLSX = RESULTS_DIR / "Survey on AI IDE Rules_Chinese.xlsx"

DOMAIN_COUNTS_CSV = Path(__file__).resolve().parent / "q5_domain_counts.csv"
OTHER_DETAILS_CSV = Path(__file__).resolve().parent / "q5_other_details.csv"

FIXED_ENGLISH_DOMAINS = [
    "Web Application (Frontend/Backend/Full-stack)",
    "Mobile Application",
    "Desktop Application",
    "Library / Framework / SDK",
    "AI / Machine Learning / Agent",
    "Data Science / Data Analytics",
    "Game Development",
    "Cloud / Infrastructure / DevOps",
]

CHINESE_TO_ENGLISH_DOMAIN = {
    "Web应用": "Web Application (Frontend/Backend/Full-stack)",
    "移动应用": "Mobile Application",
    "桌面应用": "Desktop Application",
    "开源库/框架/SDK": "Library / Framework / SDK",
    "AI应用/机器学习/智能体": "AI / Machine Learning / Agent",
    "数据科学/数据分析": "Data Science / Data Analytics",
    "游戏开发": "Game Development",
    "云/基础设施/运维脚本": "Cloud / Infrastructure / DevOps",
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

    domain_counter: Counter[str] = Counter()
    other_entries: list[str] = []

    # English Q5: comma-separated multi-select in one column.
    english_q5_col = _pick_column(list(english_df.columns), starts_with="Q5")
    for value in english_df[english_q5_col].dropna().astype(str):
        options = [item.strip() for item in value.split(",") if item.strip()]
        for option in options:
            if option in FIXED_ENGLISH_DOMAINS:
                domain_counter[option] += 1
            else:
                domain_counter["Other"] += 1
                other_entries.append(option)

    q5_columns = [str(col) for col in chinese_df.columns if str(col).startswith("6.Q5")]

    # Chinese Q5: 8 fixed option columns + other marker + other free-text column.
    for zh_domain, en_domain in CHINESE_TO_ENGLISH_DOMAIN.items():
        col = _pick_column(q5_columns, contains=f":{zh_domain}")
        domain_counter[en_domain] += int(chinese_df[col].notna().sum())

    chinese_other_col = _pick_column(q5_columns, contains=":其他____")
    chinese_other_text_col = _pick_column(q5_columns, contains=":其他____[选项填空]")
    chinese_other_count = int(chinese_df[chinese_other_col].notna().sum())
    domain_counter["Other"] += chinese_other_count

    chinese_other_texts = chinese_df[chinese_other_text_col].dropna().astype(str).str.strip()
    for text in chinese_other_texts:
        if text:
            other_entries.append(text)

    domain_rows = [{"domain": domain, "count": int(domain_counter.get(domain, 0))} for domain in FIXED_ENGLISH_DOMAINS]
    domain_rows.append({"domain": "Other", "count": int(domain_counter.get("Other", 0))})
    pd.DataFrame(domain_rows).to_csv(DOMAIN_COUNTS_CSV, index=False, encoding="utf-8")

    other_counter = Counter(entry for entry in other_entries if entry)
    other_rows = [{"other_domain_text": text, "count": int(cnt)} for text, cnt in other_counter.most_common()]
    pd.DataFrame(other_rows).to_csv(OTHER_DETAILS_CSV, index=False, encoding="utf-8")

    print(f"Saved: {DOMAIN_COUNTS_CSV}")
    print(f"Saved: {OTHER_DETAILS_CSV}")


if __name__ == "__main__":
    main()
