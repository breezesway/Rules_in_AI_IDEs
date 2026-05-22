from __future__ import annotations

from pathlib import Path
import matplotlib
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt


BASE_DIR = Path(__file__).resolve().parent
EDUCATION_CSV = BASE_DIR / "education_experience_counts.csv"
EXPERIENCE_CSV = BASE_DIR / "professional_experience_counts.csv"
Q7_TIME_CSV = BASE_DIR / "q7_rule_file_time_counts.csv"
OUTPUT_PDF = BASE_DIR / "education_experience_overview.pdf"


def _build_legend_labels(labels: list[str], counts: list[int]) -> list[str]:
    return [f"{label} ({count})" for label, count in zip(labels, counts)]


def _draw_donut(
    ax,
    labels: list[str],
    counts: list[int],
    title: str,
    colors: list[str],
) -> None:
    wedges, _, autotexts = ax.pie(
        counts,
        colors=colors[: len(counts)],
        startangle=90,
        counterclock=False,
        wedgeprops={"width": 0.42, "edgecolor": "white"},
        autopct="%1.1f%%",
        pctdistance=0.78,
        textprops={"fontsize": 15, "color": "black"},
    )
    ax.set(aspect="equal")
    ax.text(0.5, 0.05, title, transform=ax.transAxes, ha="center", va="top", fontsize=19)
    ax.legend(
        wedges,
        _build_legend_labels(labels, counts),
        loc="lower center",
        bbox_to_anchor=(0.5, 0.92),
        frameon=False,
        fontsize=15,
        handlelength=0.8,
        handletextpad=0.6,
        ncol=1,
    )
    for text in autotexts:
        text.set_fontsize(15)


def main() -> None:
    edu_df = pd.read_csv(EDUCATION_CSV)
    exp_df = pd.read_csv(EXPERIENCE_CSV)
    q7_df = pd.read_csv(Q7_TIME_CSV)

    edu_labels = edu_df["education_level"].tolist()
    edu_counts = edu_df["count"].astype(int).tolist()

    exp_labels = exp_df["professional_experience"].tolist()
    exp_counts = exp_df["count"].astype(int).tolist()

    q7_labels = q7_df["rule_file_usage_time"].tolist()
    q7_counts = q7_df["count"].astype(int).tolist()

    fig, axes = plt.subplots(1, 3, figsize=(22, 7))
    fig.subplots_adjust(wspace=0.22, bottom=0.12, top=0.86)

    education_colors = ["#7cb342", "#90caf9", "#ffb300", "#ef6c00", "#8e24aa", "#26a69a"]
    experience_colors = ["#8bc34a", "#64b5f6", "#ffb74d", "#9575cd", "#bcaaa4", "#ce93d8"]
    q7_colors = ["#4db6ac", "#4fc3f7", "#ffb74d", "#9575cd", "#81c784"]

    _draw_donut(
        axes[0],
        edu_labels,
        edu_counts,
        "Education Experience",
        education_colors,
    )
    _draw_donut(
        axes[1],
        exp_labels,
        exp_counts,
        "Professional Experience",
        experience_colors,
    )
    _draw_donut(
        axes[2],
        q7_labels,
        q7_counts,
        "Rule File Usage Duration",
        q7_colors,
    )

    plt.savefig(OUTPUT_PDF, format="pdf", bbox_inches="tight", pad_inches=0)
    plt.close(fig)
    print(f"Saved: {OUTPUT_PDF}")


if __name__ == "__main__":
    main()
