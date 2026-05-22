from __future__ import annotations

import re
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[2]
SURVEY_DIR = BASE_DIR / "survey" / "survey_results"
OUTPUT_CSV = Path(__file__).resolve().parent / "q9_score_counts_combined.csv"
MAJOR_OUTPUT_CSV = Path(__file__).resolve().parent / "q9_major_category_stats.csv"

ENGLISH_FILE = SURVEY_DIR / "Survey on AI IDE Rules_English.xlsx"
CHINESE_FILE = SURVEY_DIR / "Survey on AI IDE Rules_Chinese.xlsx"

ZH_MAJOR_TO_EN = {
    "架构与设计": "Architecture & Design",
    "代码实现": "Code Implementation",
    "开发流程与项目管理": "Development Workflow & Project Management",
    "质量保障": "Quality Assurance",
    "AI协作规范": "AI Collaboration Specifications",
}

ZH_MINOR_TO_EN = {
    "系统架构": "System Architecture",
    "设计原则和模式": "Design Principles & Patterns",
    "设计参考与约束": "Design References & Constraints",
    "技术栈选择": "Technology Stack Selections",
    "语言特性": "Language Features",
    "框架使用": "Framework Usage",
    "代码风格规范": "Code Style Conventions",
    "业务逻辑": "Business Logic",
    "性能优化": "Performance Optimization",
    "错误与异常处理": "Error & Exception Handling",
    "工作流规范": "Workflow Conventions",
    "版本控制": "Version Control",
    "环境配置": "Environment Configuration",
    "目录结构": "Directory Structure",
    "依赖管理": "Dependency Management",
    "项目文档": "Project Documentation",
    "测试策略": "Testing Strategy",
    "安全实践": "Security Practices",
    "代码质量标准": "Code Quality Standards",
    "代码审查": "Code Review",
    "日志规范": "Logging Standards",
    "AI行为与决策策略": "AI Behavior & Decision Strategies",
    "AI上下文管理": "AI Context Management",
    "AI输出内容规范": "AI Output Content Guidelines",
    "AI工具使用": "AI Tool Usage",
}


def pick_chinese_sheet(path: Path) -> str:
    sheets = pd.read_excel(path, sheet_name=None)
    for name, df in sheets.items():
        q9_cols = [c for c in df.columns if "Q9." in str(c)]
        if q9_cols:
            return name
    return max(sheets, key=lambda n: sheets[n].shape[1])


def parse_english_q9(col: str) -> tuple[str, str] | None:
    match = re.match(r"^Q9\.\d+\s+(.+?)\s+\[(.+)\]\s*$", str(col))
    if not match:
        return None
    return match.group(1).strip(), match.group(2).strip()


def parse_chinese_q9(col: str) -> tuple[str, str] | None:
    text = str(col)
    match = re.search(r"\*\*Q9\.\d+\s*([^*]+)\*\*:\*\*([^*]+)\*\*", text)
    if not match:
        return None
    major_zh = match.group(1).strip()
    minor_zh = match.group(2).strip()
    major_en = ZH_MAJOR_TO_EN.get(major_zh)
    minor_en = ZH_MINOR_TO_EN.get(minor_zh)
    if major_en is None or minor_en is None:
        raise ValueError(f"No Chinese–English category mapping for: {text}")
    return major_en, minor_en


def score_counts(series: pd.Series) -> dict[int, int]:
    numeric = pd.to_numeric(series, errors="coerce")
    valid = numeric[numeric.isin([1, 2, 3, 4, 5])].astype(int)
    counts = valid.value_counts().to_dict()
    return {score: int(counts.get(score, 0)) for score in range(1, 6)}


def mean_std_from_counts(counts: dict[int, int]) -> tuple[float | None, float | None]:
    total = sum(counts.values())
    if total == 0:
        return None, None
    mean = sum(score * cnt for score, cnt in counts.items()) / total
    variance = sum(cnt * ((score - mean) ** 2) for score, cnt in counts.items()) / total
    std = variance**0.5
    return mean, std


def build_stats() -> pd.DataFrame:
    en_df = pd.read_excel(ENGLISH_FILE)
    zh_sheet = pick_chinese_sheet(CHINESE_FILE)
    zh_df = pd.read_excel(CHINESE_FILE, sheet_name=zh_sheet)

    aggregator: dict[tuple[str, str], dict[str, object]] = {}
    ordered_keys: list[tuple[str, str]] = []

    def ensure_entry(key: tuple[str, str]) -> dict[str, object]:
        if key not in aggregator:
            aggregator[key] = {
                "major_category": key[0],
                "subcategory": key[1],
                "score_1_count": 0,
                "score_2_count": 0,
                "score_3_count": 0,
                "score_4_count": 0,
                "score_5_count": 0,
                "total_responses": 0,
                "english_column_present": False,
                "chinese_column_present": False,
            }
            ordered_keys.append(key)
        return aggregator[key]

    for col in en_df.columns:
        parsed = parse_english_q9(str(col))
        if not parsed:
            continue
        stats = ensure_entry(parsed)
        counts = score_counts(en_df[col])
        for s in range(1, 6):
            stats[f"score_{s}_count"] = int(stats[f"score_{s}_count"]) + counts[s]
        stats["total_responses"] = int(stats["total_responses"]) + sum(counts.values())
        stats["english_column_present"] = True

    for col in zh_df.columns:
        if "Q9." not in str(col):
            continue
        parsed = parse_chinese_q9(str(col))
        if not parsed:
            continue
        stats = ensure_entry(parsed)
        counts = score_counts(zh_df[col])
        for s in range(1, 6):
            stats[f"score_{s}_count"] = int(stats[f"score_{s}_count"]) + counts[s]
        stats["total_responses"] = int(stats["total_responses"]) + sum(counts.values())
        stats["chinese_column_present"] = True

    result = pd.DataFrame([aggregator[k] for k in ordered_keys])
    score_cols = {s: f"score_{s}_count" for s in range(1, 6)}
    means: list[float | None] = []
    stds: list[float | None] = []
    for _, row in result.iterrows():
        counts = {s: int(row[col]) for s, col in score_cols.items()}
        mean, std = mean_std_from_counts(counts)
        means.append(round(mean, 3) if mean is not None else None)
        stds.append(round(std, 3) if std is not None else None)
    result["mean_score"] = means
    result["std_score"] = stds
    return result


def build_major_stats(detail_df: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for major, g in detail_df.groupby("major_category", sort=False):
        counts = {s: int(g[f"score_{s}_count"].sum()) for s in range(1, 6)}
        mean, std = mean_std_from_counts(counts)
        rows.append(
            {
                "major_category": major,
                "score_1_count": counts[1],
                "score_2_count": counts[2],
                "score_3_count": counts[3],
                "score_4_count": counts[4],
                "score_5_count": counts[5],
                "total_responses": int(sum(counts.values())),
                "mean_score": round(mean, 3) if mean is not None else None,
                "std_score": round(std, 3) if std is not None else None,
            }
        )
    return pd.DataFrame(rows)


def print_validation(df: pd.DataFrame) -> None:
    major_count = df["major_category"].nunique()
    minor_count = df["subcategory"].nunique()
    total_ok = bool((df["total_responses"] == 99).all())
    only_zh = df[(~df["english_column_present"]) & (df["chinese_column_present"])]
    only_en = df[(df["english_column_present"]) & (~df["chinese_column_present"])]

    print("=== Validation ===")
    print(f"Major-category check (expect 5): {'PASS' if major_count == 5 else 'FAIL'} (actual: {major_count})")
    print(f"Minor-category check (expect 25): {'PASS' if minor_count == 25 else 'FAIL'} (actual: {minor_count})")
    print(f"Total responses=99 per subcategory: {'PASS' if total_ok else 'FAIL'}")
    if not total_ok:
        mismatch = df[df["total_responses"] != 99][["major_category", "subcategory", "total_responses"]]
        print("Subcategories with total != 99:")
        print(mismatch.to_string(index=False))
    if not only_zh.empty:
        print("Subcategories present only in Chinese sheet:")
        print(only_zh[["major_category", "subcategory"]].to_string(index=False))
    if not only_en.empty:
        print("Subcategories present only in English sheet:")
        print(only_en[["major_category", "subcategory"]].to_string(index=False))


def main() -> None:
    df = build_stats()
    major_df = build_major_stats(df)
    df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8")
    major_df.to_csv(MAJOR_OUTPUT_CSV, index=False, encoding="utf-8")
    print(f"Wrote detail stats: {OUTPUT_CSV}")
    print(f"Wrote major-category summary: {MAJOR_OUTPUT_CSV}")
    print("=== Major-category mean and std ===")
    print(major_df[["major_category", "mean_score", "std_score"]].to_string(index=False))
    print_validation(df)


if __name__ == "__main__":
    main()
