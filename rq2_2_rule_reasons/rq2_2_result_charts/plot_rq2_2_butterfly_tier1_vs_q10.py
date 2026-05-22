"""
Butterfly chart: left tier1 (N=504), right Q10 (N=99).
Center gap; split bottom axes + upward tick marks; categories sorted by left repo count descending.

Tunable: ROW_GAP, FIG_WIDTH/HEIGHT, BAR_HEIGHT; BOTTOM_AXIS_AXES_Y, LABEL_DY_AXES;
LEGEND_BBOX_*; FONT_CATEGORY / FONT_BAR_VALUE / FONT_TICK / FONT_LEGEND.
"""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.transforms import blended_transform_factory

SCRIPT_DIR = Path(__file__).resolve().parent
TIER1_CSV = SCRIPT_DIR / "tier1_distribution.csv"
Q10_CSV = SCRIPT_DIR / "q10_combined_responses.csv"
OUT_PDF = SCRIPT_DIR / "rq2_2_butterfly_tier1_vs_q10.pdf"
OUT_PNG = SCRIPT_DIR / "rq2_2_butterfly_tier1_vs_q10.png"

# CSV column order (read only); plot order follows descending left-side count
ORDER = [
    "Correction",
    "Refinement",
    "Synchronization",
    "Context Enrichment",
    "Expansion",
    "Pruning",
]

N_REPO = 504

# Layout tunables
# ---------------------------------------------------------------------------
# Center gap (horizontal fraction): larger → bar origins farther from center, wider label area.
# Suggested ~0.10–0.28; used with full x-axis span ±1.
G_MID_GAP = 0.25

# Outer padding beyond bar tips (data coords), slightly > 1 so labels/ticks are not clipped
X_PAD_OUTER = 0.06

# Figure size (inches): wide aspect; adjust freely for paper layout
FIG_WIDTH = 12.0
FIG_HEIGHT = 3.85

# Vertical: fixed bar thickness; ROW_GAP = gap between adjacent bars (data coords; smaller = tighter)
BAR_HEIGHT = 0.32
ROW_GAP = 0.18

# Baseline extension beyond full-scale endpoints (±1 → left 30% / right 80%) in data coords
BASELINE_EXTEND = 0.07

# Bottom axis line + tick stems share BOTTOM_AXIS_AXES_Y (axes fraction, 0 = subplot bottom)
BOTTOM_AXIS_AXES_Y = -0.03
# Tick stem height upward from that y (axes fraction)
TICK_UP_AXES = 0.02
# Tick label y: must be < BOTTOM_AXIS_AXES_Y so text sits below the axis line
LABEL_DY_AXES = -0.038

# Legend bbox_to_anchor (axes coords): x > 1 shifts right; negative y places it below the plot
LEGEND_BBOX_X = 1.05
LEGEND_BBOX_Y = -0.27

# Font sizes (pt)
FONT_CATEGORY = 19
FONT_BAR_VALUE = 17
FONT_TICK = 17
FONT_LEGEND = 17


def load_tier1() -> dict[str, tuple[int, float]]:
    out: dict[str, tuple[int, float]] = {}
    with TIER1_CSV.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            name = row["tier_1"].strip()
            c = int(row["count"])
            p = float(row["proportion"])
            out[name] = (c, p)
    return out


def load_q10_counts() -> tuple[dict[str, int], int]:
    cols = list(ORDER)
    sums = {c: 0 for c in cols}
    with Q10_CSV.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    n_survey = len(rows)
    for row in rows:
        for c in cols:
            sums[c] += int(row[c])
    return sums, n_survey


def _fmt_count_pct(count: int, pct: float) -> str:
    return f"{count:,}, {pct:.2f}%"


def main() -> None:
    tier1 = load_tier1()
    q10, n_survey = load_q10_counts()

    rows: list[tuple[str, int, float, int, float]] = []
    for lab in ORDER:
        c_r, p_r = tier1[lab]
        c_s = q10[lab]
        rows.append((lab, c_r, 100.0 * p_r, c_s, 100.0 * c_s / n_survey))
    rows.sort(key=lambda t: t[1], reverse=True)

    labels = [t[0] for t in rows]
    left_n = [t[1] for t in rows]
    left_pct = [t[2] for t in rows]
    right_n = [t[3] for t in rows]
    right_pct = [t[4] for t in rows]
    n = len(labels)

    mx_l = max(left_pct) if left_pct else 1.0
    mx_r = max(right_pct) if right_pct else 1.0

    l_max = max(10, int((mx_l + 9.999) // 10) * 10)
    r_max = max(20, int((mx_r + 19.999) // 20) * 20)

    g = G_MID_GAP
    span = 1.0 - g

    def x_left_tip(p_pct: float) -> float:
        return -g - (p_pct / l_max) * span

    def x_right_tip(p_pct: float) -> float:
        return g + (p_pct / r_max) * span

    bar_width_left = [-(left_pct[i] / l_max) * span for i in range(n)]
    bar_width_right = [(right_pct[i] / r_max) * span for i in range(n)]

    y_step = BAR_HEIGHT + ROW_GAP
    y_edge = max(0.15, 0.35 * y_step)

    plt.rcParams.update(
        {
            "font.family": "serif",
            "font.serif": ["Times New Roman", "DejaVu Serif", "Liberation Serif", "Noto Serif"],
        }
    )

    fig, ax = plt.subplots(figsize=(FIG_WIDTH, FIG_HEIGHT), dpi=150)
    fig.patch.set_facecolor("white")

    y = [i * y_step for i in range(n)]
    h = BAR_HEIGHT
    c_left = "#0072B2"
    c_right = "#D55E00"

    ax.barh(y, bar_width_left, left=-g, height=h, color=c_left, edgecolor="white", linewidth=0.6, zorder=2)
    ax.barh(y, bar_width_right, left=g, height=h, color=c_right, edgecolor="white", linewidth=0.6, zorder=2)

    ax.set_xlim(-1.0 - BASELINE_EXTEND - X_PAD_OUTER, 1.0 + BASELINE_EXTEND + X_PAD_OUTER)
    ax.set_ylim(-y_edge, (n - 1) * y_step + y_edge)
    ax.invert_yaxis()

    for yi, lab in zip(y, labels):
        ax.text(
            0.0,
            yi,
            lab,
            ha="center",
            va="center",
            fontsize=FONT_CATEGORY,
            color="#111111",
            zorder=6,
        )

    ax.set_yticks(y)
    ax.set_yticklabels([])

    for spine in ("top", "right", "left", "bottom"):
        ax.spines[spine].set_visible(False)
    ax.tick_params(axis="x", bottom=False, labelbottom=False, top=False)
    ax.tick_params(axis="y", left=False, right=False, labelleft=False)

    # Bottom axis: shared y for baseline and tick stems; shift vertically via BOTTOM_AXIS_AXES_Y
    trans_xaxes = blended_transform_factory(ax.transData, ax.transAxes)
    x_left_end = -1.0 - BASELINE_EXTEND
    x_right_end = 1.0 + BASELINE_EXTEND
    yb = BOTTOM_AXIS_AXES_Y
    ax.plot([x_left_end, -g], [yb, yb], transform=trans_xaxes, color="k", linewidth=0.9, clip_on=False, zorder=5)
    ax.plot([g, x_right_end], [yb, yb], transform=trans_xaxes, color="k", linewidth=0.9, clip_on=False, zorder=5)

    left_tick_specs: list[tuple[float, str]] = [
        (x_left_tip(float(p)), f"{p}%") for p in range(0, l_max + 1, 10)
    ]
    right_tick_specs: list[tuple[float, str]] = [
        (x_right_tip(float(p)), f"{p}%") for p in range(0, r_max + 1, 20)
    ]
    left_tick_specs.sort(key=lambda t: t[0])
    right_tick_specs.sort(key=lambda t: t[0])

    tick_kw = dict(transform=trans_xaxes, color="k", linewidth=0.85, clip_on=False, zorder=5)
    for x, _lab in left_tick_specs + right_tick_specs:
        y0 = BOTTOM_AXIS_AXES_Y
        y1 = BOTTOM_AXIS_AXES_Y + TICK_UP_AXES
        ax.plot([x, x], [y0, y1], **tick_kw)

    for x, lab in left_tick_specs + right_tick_specs:
        ax.text(
            x,
            LABEL_DY_AXES,
            lab,
            transform=trans_xaxes,
            ha="center",
            va="top",
            fontsize=FONT_TICK,
            color="#111111",
            clip_on=False,
            zorder=5,
        )

    pad = 0.022
    for i, yi in enumerate(y):
        xl_tip = x_left_tip(left_pct[i])
        xr_tip = x_right_tip(right_pct[i])
        ax.text(
            xl_tip - pad,
            yi,
            _fmt_count_pct(left_n[i], left_pct[i]),
            ha="right",
            va="center",
            fontsize=FONT_BAR_VALUE,
            color="#1a1a1a",
            zorder=4,
        )
        ax.text(
            xr_tip + pad,
            yi,
            _fmt_count_pct(right_n[i], right_pct[i]),
            ha="left",
            va="center",
            fontsize=FONT_BAR_VALUE,
            color="#1a1a1a",
            zorder=4,
        )

    leg = [
        mpatches.Patch(
            facecolor=c_left,
            edgecolor="none",
            label=f"Mining Repo (N={N_REPO})",
        ),
        mpatches.Patch(
            facecolor=c_right,
            edgecolor="none",
            label=f"Survey (N={n_survey})",
        ),
    ]
    ax.legend(
        handles=leg,
        bbox_to_anchor=(LEGEND_BBOX_X, LEGEND_BBOX_Y),
        loc="lower right",
        ncol=2,
        frameon=False,
        fontsize=FONT_LEGEND,
        borderaxespad=0.0,
        handlelength=1.2,
        handletextpad=0.6,
        columnspacing=1.0,
    )

    plt.tight_layout()
    fig.subplots_adjust(top=0.94, bottom=0.18, right=0.98)
    fig.savefig(OUT_PDF, bbox_inches="tight", pad_inches=0.05)
    fig.savefig(OUT_PNG, bbox_inches="tight", dpi=300, pad_inches=0.05)
    plt.close()
    print(f"Wrote {OUT_PDF}")
    print(f"Wrote {OUT_PNG}")


if __name__ == "__main__":
    main()
