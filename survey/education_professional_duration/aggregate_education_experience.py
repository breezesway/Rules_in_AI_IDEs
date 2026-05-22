from __future__ import annotations

from pathlib import Path
import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
RESULTS_DIR = BASE_DIR / "results"
ENGLISH_XLSX = RESULTS_DIR / "Survey on AI IDE Rules_English.xlsx"
CHINESE_XLSX = RESULTS_DIR / "Survey on AI IDE Rules_Chinese.xlsx"
OUTPUT_CSV = Path(__file__).resolve().parent / "education_experience_counts.csv"

# Chinese and English options are semantically equivalent; map Chinese education levels to English labels.
CN_TO_EN_EDUCATION = {
    "高中及以下": "High School or below",
    "大学本科": "Bachelor's Degree",
    "硕士研究生": "Master's Degree",
    "博士研究生": "Doctoral Degree (PhD)",
}


def _pick_column(columns: list[str], starts_with: str | None = None, contains: str | None = None) -> str:
    for col in columns:
        col_str = str(col)
        if starts_with and col_str.startswith(starts_with):
            return col_str
        if contains and contains in col_str:
            return col_str
    raise ValueError("Cannot find target column in worksheet.")


def _normalize_series(series: pd.Series) -> pd.Series:
    return series.dropna().astype(str).str.strip()


def main() -> None:
    english_df = pd.read_excel(ENGLISH_XLSX)
    chinese_df = pd.read_excel(CHINESE_XLSX, sheet_name="同步数据表")

    english_q2_col = _pick_column(list(english_df.columns), starts_with="Q2")
    chinese_q2_col = _pick_column(list(chinese_df.columns), contains="Q2")

    english_series = _normalize_series(english_df[english_q2_col])
    chinese_series = _normalize_series(chinese_df[chinese_q2_col]).map(CN_TO_EN_EDUCATION)

    english_order = list(dict.fromkeys(english_series.tolist()))

    combined = pd.concat([english_series, chinese_series.dropna()], ignore_index=True)
    counts = combined.value_counts()

    result_df = pd.DataFrame(
        {
            "education_level": english_order,
            "count": [int(counts.get(level, 0)) for level in english_order],
        }
    )

    result_df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8")
    print(f"Saved: {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
