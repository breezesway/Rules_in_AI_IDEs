from __future__ import annotations

from pathlib import Path
import textwrap
import re

import matplotlib
import pandas as pd
from matplotlib import colors

matplotlib.use("Agg")
import matplotlib.pyplot as plt


BASE_DIR = Path(__file__).resolve().parent
Q4_INPUT_CSV = BASE_DIR / "q4_role_counts.csv"
Q5_INPUT_CSV = BASE_DIR / "q5_domain_counts.csv"
Q6_INPUT_CSV = BASE_DIR / "q6_ide_usage_counts.csv"
OUTPUT_PDF = BASE_DIR / "q4_q5_q6_vertical_bars.pdf"


def _build_gradient_colors(values: list[int], cmap_name: str) -> list:
    max_val = max(values) if values else 0
    min_val = min(values) if values else 0
    if max_val == min_val:
        return ["#5e92f3"] * len(values)

    norm = colors.Normalize(vmin=min_val, vmax=max_val)
    cmap = matplotlib.colormaps[cmap_name]
    return [cmap(0.35 + 0.6 * norm(v)) for v in values]


def _wrap_labels(labels: list[str], width: int = 18) -> list[str]:
    return ["\n".join(textwrap.wrap(label, width=width)) for label in labels]


def _shorten_q6_labels(labels: list[str]) -> list[str]:
    # Keep only product names in Q6 chart labels, e.g. "Windsurf (by Codeium)" -> "Windsurf".
    return [re.sub(r"\s*\(.*?\)\s*", "", label).strip() for label in labels]


def _prepare_q6_plot_data(q6_df: pd.DataFrame, target_ides: set[str]) -> tuple[list[str], list[int]]:
    tmp = q6_df.copy()
    tmp["display_ide"] = _shorten_q6_labels(tmp["ide"].astype(str).tolist())
    tmp["is_target"] = tmp["display_ide"].isin(target_ides)
    # Put target IDEs on the left and non-target IDEs on the right.
    tmp = tmp.sort_values(["is_target", "count"], ascending=[False, False], kind="stable")
    return tmp["display_ide"].tolist(), tmp["count"].astype(int).tolist()


def _draw_vertical_bar(
    ax,
    labels: list[str],
    counts: list[int],
    *,
    cmap_name: str,
    x_label: str,
    y_label: str,
    y_max: int,
    y_ticks: list[int],
    highlight_labels: set[str] | None = None,
) -> None:
    wrapped_labels = _wrap_labels(labels, width=18)
    if highlight_labels is None:
        bar_colors = _build_gradient_colors(counts, cmap_name)
    else:
        base_colors = _build_gradient_colors(counts, cmap_name)
        bar_colors = [
            base_colors[i] if labels[i] in highlight_labels else "#d1d5db"
            for i in range(len(labels))
        ]
    bars = ax.bar(wrapped_labels, counts, color=bar_colors, edgecolor="none", width=0.60)

    ax.set_ylim(0, y_max)
    ax.set_yticks(y_ticks)
    ax.set_xlabel(x_label, fontsize=24, fontweight="bold")
    ax.set_ylabel(y_label, fontsize=24, fontweight="bold")
    ax.tick_params(axis="x", labelsize=21, rotation=60)
    ax.tick_params(axis="y", labelsize=22)
    for label in ax.get_xticklabels():
        label.set_ha("right")
        label.set_va("top")
        label.set_linespacing(1.05)
        if highlight_labels is not None:
            plain = label.get_text().replace("\n", " ")
            if plain in highlight_labels:
                label.set_fontweight("bold")
                label.set_color("#111827")
            else:
                label.set_fontweight("normal")
                label.set_color("#111827")

    for bar, count in zip(bars, counts):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.6,
            str(count),
            ha="center",
            va="bottom",
            fontsize=21,
            color="#1f2937",
        )

    ax.grid(axis="y", linestyle="--", alpha=0.25, color="#9ca3af")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def main() -> None:
    q4_df = pd.read_csv(Q4_INPUT_CSV)
    q5_df = pd.read_csv(Q5_INPUT_CSV)
    q6_df = pd.read_csv(Q6_INPUT_CSV)

    q4_df = q4_df.sort_values("count", ascending=False)
    q5_df = q5_df.sort_values("count", ascending=False)
    q6_df = q6_df.sort_values("count", ascending=False)
    target_ides = {"Cursor", "Windsurf", "Trae", "Qoder", "Kiro"}
    q6_labels, q6_counts = _prepare_q6_plot_data(q6_df, target_ides)

    all_counts = (
        q4_df["count"].astype(int).tolist()
        + q5_df["count"].astype(int).tolist()
        + q6_df["count"].astype(int).tolist()
    )
    global_max = max(all_counts) if all_counts else 0
    y_max = ((global_max + 9) // 10) * 10
    y_ticks = list(range(0, y_max + 1, 10))

    fig, axes = plt.subplots(1, 3, figsize=(34, 8), sharey=True)
    fig.subplots_adjust(wspace=0.20, bottom=0.37, top=0.995)

    _draw_vertical_bar(
        axes[0],
        q4_df["role"].tolist(),
        q4_df["count"].astype(int).tolist(),
        cmap_name="Blues",
        x_label="Professional Role (SQ4)",
        y_label="Number of Selections",
        y_max=y_max,
        y_ticks=y_ticks,
    )
    _draw_vertical_bar(
        axes[1],
        q5_df["domain"].tolist(),
        q5_df["count"].astype(int).tolist(),
        cmap_name="Oranges",
        x_label="Project Domain (SQ5)",
        y_label="Number of Selections",
        y_max=y_max,
        y_ticks=y_ticks,
    )
    _draw_vertical_bar(
        axes[2],
        q6_labels,
        q6_counts,
        cmap_name="Purples",
        x_label="AI IDE Tool (SQ6)",
        y_label="Number of Selections",
        y_max=y_max,
        y_ticks=y_ticks,
        highlight_labels=target_ides,
    )

    # Show y-axis tick labels on non-left subplots as well.
    axes[1].tick_params(axis="y", labelleft=True)
    axes[2].tick_params(axis="y", labelleft=True)

    # Force all x-axis labels to use the same vertical position.
    axes[0].xaxis.set_label_coords(0.5, -0.5)
    axes[1].xaxis.set_label_coords(0.5, -0.5)
    axes[2].xaxis.set_label_coords(0.5, -0.5)

    plt.savefig(OUTPUT_PDF, format="pdf", bbox_inches="tight", pad_inches=0)
    plt.close(fig)
    print(f"Saved: {OUTPUT_PDF}")


if __name__ == "__main__":
    main()
