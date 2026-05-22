from pathlib import Path
from typing import List

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import colormaps, colors
import matplotlib.patheffects as pe
from matplotlib.patches import Patch, Rectangle


SCRIPT_DIR = Path(__file__).resolve().parent
INPUT_CSV = SCRIPT_DIR / "rq2_1_change_rate_stats.csv"
OUTPUT_PNG = SCRIPT_DIR / "rq2_1_change_overview.png"
OUTPUT_PDF = SCRIPT_DIR / "rq2_1_change_overview.pdf"


def to_percent_text(value: float) -> str:
    return f"{value * 100:.2f}%"


def to_percent_text_compact_zero(value: float) -> str:
    if abs(value) < 1e-12:
        return "0%"
    return f"{value * 100:.2f}%"


def main() -> None:
    if not INPUT_CSV.is_file():
        raise FileNotFoundError(f"Input CSV not found: {INPUT_CSV}")

    df = pd.read_csv(INPUT_CSV)

    required_cols = [
        "category_name",
        "evolved_count",
        "change_rate",
        "added_ratio_in_category",
        "modified_ratio_in_category",
        "deleted_ratio_in_category",
    ]
    missing_cols = [c for c in required_cols if c not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")

    categories = df["category_name"].astype(str).tolist()
    category_levels = df["category_level"].astype(str).tolist()
    evolved_counts = df["evolved_count"].astype(int).tolist()
    change_rate = df["change_rate"].astype(float).to_numpy()
    added_ratio = df["added_ratio_in_category"].astype(float).to_numpy()
    modified_ratio = df["modified_ratio_in_category"].astype(float).to_numpy()
    deleted_ratio = df["deleted_ratio_in_category"].astype(float).to_numpy()

    n = len(df)
    row_spacing = 1.15
    first_level_extra_gap = 0.5
    y_positions = []
    current_y = 0.0
    for idx, level in enumerate(category_levels):
        if level == "first_level" and idx != 0:
            current_y += first_level_extra_gap
        y_positions.append(current_y)
        current_y += row_spacing
    y = np.array(y_positions)

    # Paper-friendly palette (colorblind-safe + high contrast)
    color_change_rate = "#1f77b4"  # blue
    color_added = "#C5C0F0"        # light peach
    color_modified = "#C7E9F1"     # light cyan
    color_deleted = "#F6D6AD"      # light lavender
    color_grid = "#D9D9D9"
    color_text = "#1A1A1A"

    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 17,
            "axes.titlesize": 19,
            "axes.labelsize": 18,
            "xtick.labelsize": 16.5,
            "ytick.labelsize": 16.5,
        }
    )

    fig, (ax_left, ax_mid, ax_right) = plt.subplots(
        1,
        3,
        figsize=(16, max(12, n * 0.48)),
        gridspec_kw={"width_ratios": [2.2, 2.7, 2.7]},
    )

    # ----- Left: lollipop chart for change rate -----
    norm = colors.Normalize(vmin=float(change_rate.min()), vmax=float(change_rate.max()) if n > 0 else 1.0)
    cmap = colormaps["Blues"]
    line_right_anchor = float(change_rate.max()) * 1.10 if n > 0 else 1.0

    def darker(hex_or_rgba, factor: float = 0.72):
        r, g, b, _a = colors.to_rgba(hex_or_rgba)
        return (r * factor, g * factor, b * factor, 1.0)

    for yi, rate, level in zip(y, change_rate, category_levels):
        c = cmap(0.30 + 0.65 * norm(rate))
        is_first = level == "first_level"
        line_w = 7.5 if is_first else 3.2
        dot_s = 340 if is_first else 130
        line = ax_left.hlines(y=yi, xmin=0, xmax=rate, color=c, alpha=0.95, linewidth=line_w)
        dot = ax_left.scatter(rate, yi, color=c, s=dot_s, zorder=4, edgecolor="white", linewidth=1.2)
        if is_first:
            outline_c = darker(c)
            line.set_path_effects(
                [
                    pe.Stroke(linewidth=line_w + 2.0, foreground=outline_c, alpha=0.95),
                    pe.Normal(),
                ]
            )
            dot.set_edgecolor(outline_c)
            dot.set_linewidth(2.0)

    ax_left.set_yticks(y)
    ax_left.set_yticklabels([])
    ax_left.tick_params(axis="y", length=0)
    ax_left.set_ylim(y[-1] + 0.5 * row_spacing, -0.5 * row_spacing)
    max_rate = float(np.max(change_rate)) if n > 0 else 0.0
    ax_left.set_xlim(line_right_anchor, 0)

    if max_rate > 0:
        max_pct = int(np.ceil(max_rate * 100))
        step = 20
        max_pct_rounded = int(np.ceil(max_pct / step) * step)
        ticks_pct = np.arange(0, max_pct_rounded + 1, step)
        xticks = ticks_pct / 100.0
    else:
        xticks = np.array([0.0])
    ax_left.set_xticks(xticks)
    ax_left.set_xticklabels([to_percent_text(x) for x in xticks])
    ax_left.tick_params(axis="x", length=0)
    ax_left.set_xticklabels([])

    for yi, rate in zip(y, change_rate):
        ax_left.text(
            min(rate + max_rate * 0.07, line_right_anchor * 0.995),
            yi,
            to_percent_text(rate),
            va="center",
            ha="right",
            fontsize=15,
            color=color_text,
        )

    # ----- Middle: category labels + evolved count -----
    center_labels = []
    for cat, level in zip(categories, category_levels):
        display_cat = cat
        if cat == "Development Workflow & Project Management":
            display_cat = "Development Workflow &\nProject Management"
        if level == "second_level":
            display_cat = "      " + display_cat
        center_labels.append(display_cat)
    ax_mid.set_xlim(0, 1)
    ax_mid.set_ylim(y[-1] + 0.5 * row_spacing, -0.5 * row_spacing)
    ax_mid.axis("off")

    for yi, label, _count, level in zip(y, center_labels, evolved_counts, category_levels):
        current_fontsize = 16.4
        current_y = yi
        current_weight = "bold" if level == "first_level" else "normal"
        if label.startswith("Development Workflow &\nProject Management"):
            current_fontsize = 15.2
            current_y = yi - 0.05
        ax_mid.text(
            0.04,
            current_y,
            label,
            ha="left",
            va="center",
            fontsize=current_fontsize,
            color=color_text,
            fontweight=current_weight,
        )

    # ----- Right: stacked bar for added/modified/deleted ratio -----
    base_bar_h = 0.72
    for yi, a, m, d, level in zip(y, added_ratio, modified_ratio, deleted_ratio, category_levels):
        is_first = level == "first_level"
        bar_h = 0.86 if is_first else base_bar_h
        edge_c = "#9370DB" if is_first else "none"
        edge_w = 1.3 if is_first else 0.0
        alpha = 1.0 if is_first else 0.92
        # Do not add borders to each segment to avoid internal divider lines
        ax_right.barh(yi, a, height=bar_h, color=color_added, edgecolor="none", linewidth=0, alpha=alpha)
        ax_right.barh(yi, m, height=bar_h, left=a, color=color_modified, edgecolor="none", linewidth=0, alpha=alpha)
        ax_right.barh(yi, d, height=bar_h, left=a + m, color=color_deleted, edgecolor="none", linewidth=0, alpha=alpha)
        # For first-level categories, draw only the outer outline of the full bar
        if is_first:
            total_w = a + m + d
            ax_right.add_patch(
                Rectangle(
                    (0, yi - bar_h / 2),
                    total_w,
                    bar_h,
                    fill=False,
                    edgecolor=edge_c,
                    linewidth=edge_w,
                )
            )

    ax_right.set_xlim(-0.14, 1.0)
    ax_right.set_yticks(y)
    ax_right.set_yticklabels([])
    ax_right.tick_params(axis="y", length=0)
    ax_right.set_ylim(y[-1] + 0.5 * row_spacing, -0.5 * row_spacing)
    ax_right.set_xticks([])
    ax_right.tick_params(axis="x", length=0)

    deleted_label_shift_categories = {
        "Business Logic",
        "Project Documentation",
        "Environment Configuration",
        "Version Control",
        "Dependency Management",
        "Logging Standards",
        "Code Review",
        "AI Context Management",
        "AI Tool Usage",
    }
    deleted_label_extra_shift_categories = {
        "Business Logic",
        "Version Control",
        "Code Review",
    }

    for yi, a, m, d, cat, count in zip(y, added_ratio, modified_ratio, deleted_ratio, categories, evolved_counts):
        # Show evolved count to the left of the Added segment (right-aligned)
        ax_right.text(
            -0.075,
            yi,
            str(count),
            ha="right",
            va="center",
            fontsize=13.0,
            color=color_text,
            clip_on=False,
        )

        segments = [(0.0, a), (a, m), (a + m, d)]
        for seg_idx, (left, width) in enumerate(segments):
            x = left + width / 2
            if width <= 0:
                text = "0%"
                x = left
                ha = "center"
                txt_color = color_text
            else:
                text = to_percent_text_compact_zero(width)
                ha = "center"
                txt_color = color_text

                # Labels in the right-edge critical zone may be clipped; allow overflow and keep dark text.
                if (left + width > 0.95 and width < 0.12) or (x > 0.96):
                    txt_color = color_text

            # For selected rows, shift the overlapping deleted-segment label to the right.
            if cat in deleted_label_shift_categories and seg_idx == 2:
                x += 0.03
            if cat in deleted_label_extra_shift_categories and seg_idx == 2:
                x += 0.02

            ax_right.text(
                x,
                yi,
                text,
                ha=ha,
                va="center",
                fontsize=12.3,
                color=txt_color,
                clip_on=False,
            )

    # Legend at top-center for paper layout
    handles = [
        Patch(facecolor=color_added, edgecolor="none", label="Added"),
        Patch(facecolor=color_modified, edgecolor="none", label="Modified"),
        Patch(facecolor=color_deleted, edgecolor="none", label="Deleted"),
    ]
    labels = ["Added", "Modified", "Deleted"]
    fig.legend(
        handles,
        labels,
        loc="lower right",
        ncol=3,
        bbox_to_anchor=(0.90, 0.045),
        frameon=False,
        fontsize=15,
        columnspacing=0.8,
        handletextpad=0.4,
    )

    # Remove all boxes and background grid/frames.
    for ax in (ax_left, ax_mid, ax_right):
        for spine in ax.spines.values():
            spine.set_visible(False)
        ax.grid(False)
        ax.set_facecolor("none")

    # Put panel titles under each side chart.
    ax_left.text(
        0.5,
        -0.065,
        "Change Rate",
        transform=ax_left.transAxes,
        ha="center",
        va="top",
        fontsize=17.5,
        color=color_text,
        fontweight="semibold",
    )
    ax_right.text(
        0.5,
        -0.065,
        "Change Type Composition",
        transform=ax_right.transAxes,
        ha="center",
        va="top",
        fontsize=17.5,
        color=color_text,
        fontweight="semibold",
    )

    plt.subplots_adjust(left=0.05, right=0.87, top=0.98, bottom=0.10, wspace=0.01)

    fig.savefig(OUTPUT_PNG, dpi=400, bbox_inches="tight")
    fig.savefig(OUTPUT_PDF, bbox_inches="tight")
    plt.close(fig)

    print(f"Saved PNG: {OUTPUT_PNG}")
    print(f"Saved PDF: {OUTPUT_PDF}")


if __name__ == "__main__":
    main()
