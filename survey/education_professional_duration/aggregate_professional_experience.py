from __future__ import annotations

from pathlib import Path
import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
RESULTS_DIR = BASE_DIR / "survey_results"
ENGLISH_XLSX = RESULTS_DIR / "Survey on AI IDE Rules_English.xlsx"
CHINESE_XLSX = RESULTS_DIR / "Survey on AI IDE Rules_Chinese.xlsx"
OUTPUT_CSV = Path(__file__).resolve().parent / "professional_experience_counts.csv"

# Chinese and English options are semantically equivalent; map Chinese work experience to English labels.
CN_TO_EN_EXPERIENCE = {
    "少于 1 年": "Less than 1 year",
    "1 - 2 年": "1 – 2 years",
    "3 - 5 年": "3 – 5 years",
    "6 - 10 年": "6 – 10 years",
    "11 - 20 年": "11 – 20 years",
    "超过 20 年": "More than 20 years",
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

    english_q3_col = _pick_column(list(english_df.columns), starts_with="Q3")
    chinese_q3_col = _pick_column(list(chinese_df.columns), contains="Q3")

    english_series = _normalize_series(english_df[english_q3_col])
    chinese_series = _normalize_series(chinese_df[chinese_q3_col]).map(CN_TO_EN_EXPERIENCE)

    english_order = list(dict.fromkeys(english_series.tolist()))

    combined = pd.concat([english_series, chinese_series.dropna()], ignore_index=True)
    counts = combined.value_counts()

    result_df = pd.DataFrame(
        {
            "professional_experience": english_order,
            "count": [int(counts.get(level, 0)) for level in english_order],
        }
    )

    result_df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8")
    print(f"Saved: {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
