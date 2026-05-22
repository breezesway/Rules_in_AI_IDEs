from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.colors import Normalize, to_rgb
import math
from matplotlib.offsetbox import AnnotationBbox, HPacker, TextArea
from matplotlib.patches import Rectangle

plt.rcParams["font.size"] = 17
plt.rcParams["axes.titlesize"] = 18


SCRIPT_DIR = Path(__file__).resolve().parent
RULES_DIR = SCRIPT_DIR.parent / "rules"

MAJOR_SURVEY_CSV = SCRIPT_DIR / "q9_major_category_stats.csv"
DETAIL_SURVEY_CSV = SCRIPT_DIR / "q9_score_counts_combined.csv"

OUT_PNG = SCRIPT_DIR / "rq1_rule_survey_distribution_table.png"
OUT_PDF = SCRIPT_DIR / "rq1_rule_survey_distribution_table.pdf"
OUT_CSV = SCRIPT_DIR / "rq1_rule_survey_distribution_table_data.csv"


# Explicit alignment for minor naming differences between rule data and survey data
SECOND_LEVEL_RULE_TO_SURVEY = {
    "Architecture Patterns": "System Architecture",
    "Design Principles": "Design Principles & Patterns",
}

# Importance: 1→5 light green → yellow → orange
LIKERT_COLORS = {
    1: "#F4A460",
    2: "#9ACD32",
    3: "#ffe082",
    4: "#ffb74d",
    5: "#e65100",
}

# Shift divisor: larger values pull bars toward center (less left-right swing)
LIKERT_SHIFT_DIVISOR = 2.85
# Global left bias in data coordinates (negative = left)
LIKERT_GLOBAL_BIAS = -0.72
# Horizontal scale for stacked segments (keeps proportions; widens xlim accordingly)
LIKERT_WIDTH_SCALE = 1.6

# Max half-width accumulated by draw_likert_bar; main() sets xlim from this
_LIKERT_X_HALF_SPAN: list[float] = [0.0]


def _luminance(hex_color: str) -> float:
    r, g, b = to_rgb(hex_color)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def _label_color_for_stack(ws: tuple[float, float, float, float, float]) -> str:
    lum = sum(ws[i - 1] * _luminance(LIKERT_COLORS[i]) for i in range(1, 6))
    return "#1a1a1a" if lum > 0.55 else "white"


def draw_rule_count_style_barh(
    ax: plt.Axes,
    y: float,
    count: int,
    max_count: int,
    total_rules: int,
    rule_norm: Normalize,
    rule_cmap,
    *,
    height: float = 0.62,
    bar_left: float = 0.0,
    label_x: float | None = None,
    width_scale: float = 1.0,
    label_dark_threshold: int = 200,
    bar_color: str | None = None,
) -> None:
    bar_w = (float(count) / max_count) if max_count > 0 else 0.0
    bar_w_draw = bar_w * width_scale
    if bar_color is None:
        bar_color = rule_cmap(0.22 + 0.70 * rule_norm(float(count)))
    ax.barh(y, bar_w_draw, left=bar_left, height=height, color=bar_color, edgecolor="none", zorder=1)
    pct = (count / total_rules * 100) if total_rules > 0 else 0.0
    label = f"{int(count)}, {pct:.2f}%"
    if bar_color is None:
        lbl_color = "black" if int(count) < label_dark_threshold else "white"
    else:
        lum = _luminance(bar_color)
        lbl_color = "#1a1a1a" if lum > 0.55 else "white"
    lx = bar_left + 0.02 if label_x is None else label_x
    ax.text(
        lx,
        y,
        label,
        va="center",
        ha="left",
        fontsize=17,
        color=lbl_color,
        zorder=2,
        clip_on=True,
    )


def format_category_label(text: str, max_len: int = 42) -> str:
    """Wrap category labels: break after & for Development Workflow…; long names after first &; short names unchanged."""
    s = str(text).strip()
    if "Development Workflow" in s and " & " in s:
        return s.replace(" & ", " &\n", 1)
    if " & " in s and len(s) > max_len:
        return s.replace(" & ", " &\n", 1)
    return s


def find_json_files(root: Path) -> list[Path]:
    return sorted([p for p in root.rglob("*.json") if p.is_file()])


def load_rule_distribution() -> tuple[pd.DataFrame, int]:
    files = find_json_files(RULES_DIR)
    total = 0
    combo_counter: dict[tuple[str, str], int] = defaultdict(int)

    for fp in files:
        try:
            data = json.loads(fp.read_text(encoding="utf-8"))
        except Exception:
            continue
        if not isinstance(data, list):
            continue
        for obj in data:
            if not isinstance(obj, dict):
                continue
            first_level = str(obj.get("first_level", "Unknown")).strip() or "Unknown"
            second_level = str(obj.get("second_level", "Unknown")).strip() or "Unknown"
            second_level = SECOND_LEVEL_RULE_TO_SURVEY.get(second_level, second_level)
            combo_counter[(first_level, second_level)] += 1
            total += 1

    rows = []
    for (first_level, second_level), count in combo_counter.items():
        rows.append(
            {
                "major_category": first_level,
                "subcategory": second_level,
                "rule_count": int(count),
                "rule_pct": (count / total * 100) if total > 0 else 0.0,
            }
        )

    df = pd.DataFrame(rows)
    return df, total


def draw_likert_bar(
    ax: plt.Axes,
    y: float,
    counts: dict[int, int],
    total: int,
    mean: float,
    std: float,
    reference_mean: float,
    height: float = 0.72,
    *,
    width_scale: float | None = None,
    mean_label_x_bias: float = 0.0,
) -> None:
    if total <= 0:
        return

    ws = LIKERT_WIDTH_SCALE if width_scale is None else width_scale
    p = {k: counts.get(k, 0) / total for k in range(1, 6)}
    # Total width fixed at 1 (segment widths = score proportions); horizontal shift from (mean - reference_mean)
    center_shift = (mean - reference_mean) / LIKERT_SHIFT_DIVISOR + LIKERT_GLOBAL_BIAS
    w1, w2, w3, w4, w5 = (p[1] * ws, p[2] * ws, p[3] * ws, p[4] * ws, p[5] * ws)

    # Center neutral (3) at midpoint; 1-2 on the left, 4-5 on the right
    x_w3_left = center_shift - w3 / 2
    x_w3_right = center_shift + w3 / 2
    x_w2_left = x_w3_left - w2
    x_w1_left = x_w2_left - w1
    x_w4_left = x_w3_right
    x_w5_left = x_w4_left + w4

    ax.barh(y, w1, left=x_w1_left, height=height, color=LIKERT_COLORS[1], edgecolor="none")
    ax.barh(y, w2, left=x_w2_left, height=height, color=LIKERT_COLORS[2], edgecolor="none")
    ax.barh(y, w3, left=x_w3_left, height=height, color=LIKERT_COLORS[3], edgecolor="none")
    ax.barh(y, w4, left=x_w4_left, height=height, color=LIKERT_COLORS[4], edgecolor="none")
    ax.barh(y, w5, left=x_w5_left, height=height, color=LIKERT_COLORS[5], edgecolor="none")

    # Place label at geometric center of stacked bar (width-weighted midpoint)
    x_label = (
        w1 * (x_w1_left + w1 / 2)
        + w2 * (x_w2_left + w2 / 2)
        + w3 * (x_w3_left + w3 / 2)
        + w4 * (x_w4_left + w4 / 2)
        + w5 * (x_w5_left + w5 / 2)
    )

    lbl_color = _label_color_for_stack((w1, w2, w3, w4, w5))
    # Fixed font sizes decoupled from bar height (avoids oversized Mean±SD from HPacker spacing)
    mean_fs, pm_fs, std_fs = 17, 14, 14

    mean_txt = f"{mean:.2f}"
    std_txt = f"{std:.2f}"
    pm_txt = "±"

    pack = HPacker(
        children=[
            TextArea(mean_txt, textprops=dict(color=lbl_color, fontsize=mean_fs)),
            TextArea(pm_txt, textprops=dict(color=lbl_color, fontsize=pm_fs)),
            TextArea(std_txt, textprops=dict(color=lbl_color, fontsize=std_fs)),
        ],
        align="center",
        pad=0,
        sep=1,
    )
    x_label_draw = x_label + mean_label_x_bias
    ab = AnnotationBbox(
        pack,
        (x_label_draw, y),
        xycoords=ax.transData,
        box_alignment=(0.5, 0.5),
        bboxprops=dict(boxstyle="square,pad=0", fc="none", ec="none"),
        frameon=False,
        pad=0,
    )
    ax.add_artist(ab)

    left_edge = x_w1_left
    right_edge = x_w5_left + w5
    margin = 0.12
    # Widen half-span when label shifts right so Mean±SD does not clip
    need = max(abs(left_edge), abs(right_edge) + max(0.0, mean_label_x_bias)) + margin
    if need > _LIKERT_X_HALF_SPAN[0]:
        _LIKERT_X_HALF_SPAN[0] = need


def main() -> None:
    major_df = pd.read_csv(MAJOR_SURVEY_CSV)
    detail_df = pd.read_csv(DETAIL_SURVEY_CSV)
    rule_df, total_rules = load_rule_distribution()

    merged = rule_df.merge(
        detail_df[
            [
                "major_category",
                "subcategory",
                "score_1_count",
                "score_2_count",
                "score_3_count",
                "score_4_count",
                "score_5_count",
                "total_responses",
                "mean_score",
                "std_score",
            ]
        ],
        on=["major_category", "subcategory"],
        how="left",
    ).merge(
        major_df[
            [
                "major_category",
                "score_1_count",
                "score_2_count",
                "score_3_count",
                "score_4_count",
                "score_5_count",
                "total_responses",
                "mean_score",
                "std_score",
            ]
        ].rename(
            columns={
                "score_1_count": "major_score_1_count",
                "score_2_count": "major_score_2_count",
                "score_3_count": "major_score_3_count",
                "score_4_count": "major_score_4_count",
                "score_5_count": "major_score_5_count",
                "total_responses": "major_total_responses",
                "mean_score": "major_mean_score",
                "std_score": "major_std_score",
            }
        ),
        on="major_category",
        how="left",
    )

    # Combined table for direct citation in paper text/appendix
    merged["rule_count_pct"] = merged.apply(lambda r: f"{int(r['rule_count'])}, {r['rule_pct']:.2f}%", axis=1)
    merged = merged.sort_values(["major_category", "rule_count"], ascending=[True, False]).reset_index(drop=True)

    # Move AI Collaboration Specifications block to bottom (other majors keep relative order)
    ai_name = "AI Collaboration Specifications"
    others = merged[merged["major_category"] != ai_name]
    ai_block = merged[merged["major_category"] == ai_name]
    merged = pd.concat([others, ai_block], ignore_index=True)
    merged.to_csv(OUT_CSV, index=False, encoding="utf-8")

    ref_mean_second = float(pd.to_numeric(detail_df["mean_score"], errors="coerce").mean())

    n = len(merged)
    fig = plt.figure(figsize=(17, max(12, n * 0.62)), constrained_layout=False)
    gs = fig.add_gridspec(1, 4, width_ratios=[3.3, 3.6, 5.2, 2.8], wspace=0.015)

    ax_primary = fig.add_subplot(gs[0, 0])
    ax_second = fig.add_subplot(gs[0, 1], sharey=ax_primary)
    ax_rule = fig.add_subplot(gs[0, 2], sharey=ax_primary)
    ax_second_bar = fig.add_subplot(gs[0, 3], sharey=ax_primary)

    for ax in [ax_primary, ax_second, ax_rule, ax_second_bar]:
        ax.set_ylim(-0.5, n - 0.5)
        ax.invert_yaxis()

    _LIKERT_X_HALF_SPAN[0] = 0.0

    # Text column + primary-level importance bars below group labels
    max_rule_count = int(merged["rule_count"].max()) if not merged.empty else 1
    min_rule_count = int(merged["rule_count"].min()) if not merged.empty else 0
    rule_norm = Normalize(vmin=min_rule_count, vmax=max_rule_count if max_rule_count > min_rule_count else max_rule_count + 1)
    rule_cmap = plt.get_cmap("Blues")
    major_rule_totals = merged.groupby("major_category", sort=False)["rule_count"].sum()
    max_major_rule = int(major_rule_totals.max()) if not major_rule_totals.empty else 1
    major_vals = [int(v) for v in major_rule_totals.tolist()] if not major_rule_totals.empty else [0]
    major_min_rule = min(major_vals)
    pending_major_rule_bars: list[dict] = []
    for i, row in merged.iterrows():
        show_major = i == 0 or merged.loc[i - 1, "major_category"] != row["major_category"]
        if show_major:
            major_lbl = format_category_label(row["major_category"])
            multiline = "\n" in major_lbl
            # invert_yaxis: larger y is lower; shift major name and both bars down together
            text_y = i + 0.20 if multiline else i - 0.02
            cnt_y = i + 1.22 if multiline else i + 0.74
            imp_y = i + 2.14 if multiline else i + 1.66
            maj_bar_h = 0.70
            ax_primary.text(
                -1.52,
                text_y,
                major_lbl,
                va="center",
                ha="left",
                fontsize=16,
            )
            major_total_rules = int(major_rule_totals.get(row["major_category"], 0))
            pending_major_rule_bars.append(
                dict(y=cnt_y, count=major_total_rules, max_count=max_major_rule, height=0.72)
            )
            major_counts = {
                1: int(row["major_score_1_count"]),
                2: int(row["major_score_2_count"]),
                3: int(row["major_score_3_count"]),
                4: int(row["major_score_4_count"]),
                5: int(row["major_score_5_count"]),
            }
            draw_likert_bar(
                ax_primary,
                imp_y,
                major_counts,
                int(row["major_total_responses"]),
                float(row["major_mean_score"]),
                float(row["major_std_score"]),
                ref_mean_second,
                height=maj_bar_h,
                width_scale=1.95,
            )
        ax_second.text(0.0, i, format_category_label(row["subcategory"]), va="center", fontsize=16)
        draw_rule_count_style_barh(
            ax_rule,
            i,
            int(row["rule_count"]),
            max_rule_count,
            total_rules,
            rule_norm,
            rule_cmap,
        )

    # Secondary importance: one bar per row
    for i, row in merged.iterrows():
        second_counts = {
            1: int(row["score_1_count"]),
            2: int(row["score_2_count"]),
            3: int(row["score_3_count"]),
            4: int(row["score_4_count"]),
            5: int(row["score_5_count"]),
        }
        draw_likert_bar(
            ax_second_bar,
            i,
            second_counts,
            int(row["total_responses"]),
            float(row["mean_score"]),
            float(row["std_score"]),
            ref_mean_second,
            mean_label_x_bias=0.14,
        )

    half = max(_LIKERT_X_HALF_SPAN[0], 1.55)
    # Primary column: Likert centered at 0; major rule-count bars start at left edge
    pad_x = 0.06 * half
    bar_origin = -half + pad_x
    usable_w = max(2.0 * half - 2.0 * pad_x, 1e-6)
    major_sqrt_min = math.sqrt(float(max(major_min_rule, 0)))
    major_sqrt_max = math.sqrt(float(max_major_rule))
    if major_sqrt_max <= major_sqrt_min:
        major_sqrt_max = major_sqrt_min + 1.0
    major_rule_norm = Normalize(vmin=major_sqrt_min, vmax=major_sqrt_max)
    major_rule_cmap = plt.get_cmap("Blues")

    for item in pending_major_rule_bars:
        c = int(item["count"])
        t = major_rule_norm(math.sqrt(float(max(c, 0))))
        bar_color = major_rule_cmap(0.18 + 0.72 * float(t))
        draw_rule_count_style_barh(
            ax_primary,
            float(item["y"]),
            c,
            int(item["max_count"]),
            total_rules,
            rule_norm,
            rule_cmap,
            height=float(item["height"]),
            bar_left=bar_origin,
            width_scale=usable_w,
            bar_color=bar_color,
        )

    ax_primary.set_xlim(-half, half)
    ax_second_bar.set_xlim(-half, half)

    # Styling and column headers
    for ax in [ax_second, ax_rule]:
        ax.set_xlim(0, 1)
        ax.set_xticks([])
        ax.set_yticks([])
        for sp in ax.spines.values():
            sp.set_visible(False)

    for ax in [ax_primary, ax_second_bar]:
        ax.set_xticks([])
        ax.set_yticks([])
        for sp in ["top", "left", "right", "bottom"]:
            ax.spines[sp].set_visible(False)

    title_kw = dict(fontsize=18, pad=18, fontweight="bold")
    ax_primary.set_title("Primary Category", **title_kw)
    ax_second.set_title("Secondary Category", **title_kw)
    ax_rule.set_title("Rule Count(#, %)", **title_kw)
    ax_second_bar.set_title("Importance (Mean ± SD)", **title_kw)

    fig.subplots_adjust(left=0.05, right=0.98, top=0.90, bottom=0.20, wspace=0.02)
    fig.canvas.draw()

    # Three-line table: top rule around headers, line under headers, bottom rule around body
    left = ax_primary.get_position().x0
    right = ax_second_bar.get_position().x1

    renderer = fig.canvas.get_renderer()
    title_boxes = [
        ax_primary.title.get_window_extent(renderer=renderer),
        ax_second.title.get_window_extent(renderer=renderer),
        ax_rule.title.get_window_extent(renderer=renderer),
        ax_second_bar.title.get_window_extent(renderer=renderer),
    ]
    inv = fig.transFigure.inverted()
    title_top_fig = max(inv.transform_bbox(b).ymax for b in title_boxes)
    title_bottom_fig = min(inv.transform_bbox(b).ymin for b in title_boxes)

    y_top_line = min(0.985, title_top_fig + 0.012)
    y_header_sep = title_bottom_fig - 0.006
    y_bottom_line = ax_primary.get_position().y0 - 0.008

    for y, lw in [(y_top_line, 1.6), (y_header_sep, 1.0), (y_bottom_line, 1.6)]:
        fig.add_artist(
            plt.Line2D([left, right], [y, y], transform=fig.transFigure, color="black", linewidth=lw, solid_capstyle="butt")
        )

    # Legend below table to avoid overlap
    handles = [
        Rectangle((0, 0), 1, 1, facecolor=LIKERT_COLORS[s], edgecolor="none", linewidth=0) for s in range(1, 6)
    ]
    labels = ["1 (Least Important)", "2", "3", "4", "5 (Most Important)"]
    legend_y = max(0.02, y_bottom_line - 0.048)
    fig.legend(
        handles,
        labels,
        ncol=5,
        loc="lower right",
        bbox_to_anchor=(0.98, legend_y),
        frameon=False,
        fontsize=17,
        columnspacing=1.6,
        handletextpad=0.55,
        handlelength=1.75,
        handleheight=1.0,
        borderaxespad=0.6,
    )
    fig.savefig(OUT_PNG, dpi=300, bbox_inches="tight")
    fig.savefig(OUT_PDF, bbox_inches="tight")
    plt.close(fig)

    print(f"Wrote data table: {OUT_CSV}")
    print(f"Wrote image: {OUT_PNG}")
    print(f"Wrote PDF: {OUT_PDF}")


if __name__ == "__main__":
    main()
