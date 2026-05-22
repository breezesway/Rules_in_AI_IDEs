"""
Q10 multi-select: Phi heatmap + pairwise tests (two-sided Fisher exact, Benjamini–Hochberg FDR).

Input: parent dir `rq2.2_result/q10_combined_responses_no_source_timestamp.csv`
       (maintained after running `aggregate_survey_q10.py`).
Output (this dir `q10_phi_cooccurrence/`):
  - q10_pairwise_associations.csv  (φ, 2×2 cells, Fisher p, OR, BH-FDR q; marginal p_a/p_b/p_ab)
  - q10_association_heatmap_phi.pdf / .png

Stats: Fisher exact test on all 15 pairs from 6 choose 2 (H0: independence);
       p-values adjusted with BH-FDR (m=15); q_bh < 0.05 at α=0.05 counts as significant.
"""

from __future__ import annotations

from itertools import combinations
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import fisher_exact

SCRIPT_DIR = Path(__file__).resolve().parent
RESULT_DIR = SCRIPT_DIR.parent
INPUT_CSV = RESULT_DIR / "q10_combined_responses_no_source_timestamp.csv"

ORDER = [
    "Correction",
    "Refinement",
    "Synchronization",
    "Context Enrichment",
    "Expansion",
    "Pruning",
]

# Phi heatmap: row/column order (top→bottom, left→right) and axis labels (full names)
PHI_HEATMAP_ORDER = [
    "Expansion",
    "Context Enrichment",
    "Synchronization",
    "Refinement",
    "Correction",
    "Pruning",
]


def load_matrix() -> pd.DataFrame:
    df = pd.read_csv(INPUT_CSV)
    return df[ORDER].astype(int)


def contingency_11_10_01_00(x: np.ndarray, y: np.ndarray) -> tuple[int, int, int, int]:
    """Row=A, col=B: [[(1,1),(1,0)],[(0,1),(0,0)]] — matches scipy.stats.fisher_exact."""
    a11 = int(((x == 1) & (y == 1)).sum())
    a10 = int(((x == 1) & (y == 0)).sum())
    a01 = int(((x == 0) & (y == 1)).sum())
    a00 = int(((x == 0) & (y == 0)).sum())
    return a11, a10, a01, a00


def phi_coefficient(x: np.ndarray, y: np.ndarray) -> float:
    a11, a10, a01, a00 = contingency_11_10_01_00(x, y)
    num = a11 * a00 - a10 * a01
    den = np.sqrt((a11 + a10) * (a01 + a00) * (a11 + a01) * (a10 + a00))
    return float(num / den) if den else 0.0


def benjamini_hochberg_qvalues(pvals: np.ndarray) -> np.ndarray:
    """Benjamini–Hochberg: return FDR-adjusted p-values (q-values) per hypothesis."""
    pvals = np.asarray(pvals, dtype=float)
    m = len(pvals)
    if m == 0:
        return pvals
    order = np.argsort(pvals)
    ranked = pvals[order]
    adjusted_sorted = np.empty(m)
    prev = 1.0
    for i in range(m - 1, -1, -1):
        adjusted_sorted[i] = min(ranked[i] * m / (i + 1), prev)
        prev = adjusted_sorted[i]
    out = np.empty(m)
    out[order] = adjusted_sorted
    return np.clip(out, 0.0, 1.0)


def phi_matrix(X: pd.DataFrame) -> pd.DataFrame:
    """Symmetric φ matrix (plotting only; not written to CSV)."""
    cols = list(X.columns)
    n = len(cols)
    mat = np.eye(n)
    for i, a in enumerate(cols):
        for j, b in enumerate(cols):
            if i >= j:
                continue
            p = phi_coefficient(X[a].values, X[b].values)
            mat[i, j] = mat[j, i] = p
    return pd.DataFrame(mat, index=cols, columns=cols)


def pairwise_long(X: pd.DataFrame) -> pd.DataFrame:
    rows = []
    n = len(X)
    pvals: list[float] = []
    for a, b in combinations(ORDER, 2):
        xa, xb = X[a].values, X[b].values
        a11, a10, a01, a00 = contingency_11_10_01_00(xa, xb)
        both = a11
        either = int(((X[a] == 1) | (X[b] == 1)).sum())
        phi = phi_coefficient(xa, xb)
        p_a, p_b = X[a].mean(), X[b].mean()
        p_ab = both / n
        table = [[a11, a10], [a01, a00]]
        odds_ratio, fisher_p = fisher_exact(table, alternative="two-sided")
        pvals.append(float(fisher_p))
        or_val = float(odds_ratio) if np.isfinite(odds_ratio) else np.nan
        rows.append(
            {
                "motive_a": a,
                "motive_b": b,
                "n11_both": a11,
                "n10_a_only": a10,
                "n01_b_only": a01,
                "n00_neither": a00,
                "co_occurrence_n": both,
                "union_n": either,
                "phi": round(phi, 4),
                "fisher_odds_ratio": round(or_val, 4) if np.isfinite(or_val) else np.nan,
                "fisher_p_two_sided": fisher_p,
                "p_a": round(p_a, 4),
                "p_b": round(p_b, 4),
                "p_ab": round(p_ab, 4),
            }
        )
    out = pd.DataFrame(rows)
    q_bh = benjamini_hochberg_qvalues(out["fisher_p_two_sided"].values)
    out["fdr_q_bh"] = q_bh
    out["fisher_p_two_sided"] = out["fisher_p_two_sided"].round(6)
    out["fdr_q_bh"] = out["fdr_q_bh"].round(6)
    return out.sort_values("phi", ascending=False).reset_index(drop=True)


def _setup_rc() -> None:
    plt.rcParams.update(
        {
            "font.family": "serif",
            "font.serif": ["Times New Roman", "DejaVu Serif", "Liberation Serif", "Noto Serif"],
            "font.size": 14,
        }
    )


def plot_phi_heatmap(phi: pd.DataFrame, out_base: Path) -> None:
    _setup_rc()
    phi_ord = phi.reindex(index=PHI_HEATMAP_ORDER, columns=PHI_HEATMAP_ORDER)
    cols = list(phi_ord.columns)
    labels = cols  # full names, same as CSV column names
    data = phi_ord.values.astype(float).copy()
    np.fill_diagonal(data, np.nan)

    vmin, vmax = -0.15, 0.45
    fig, ax = plt.subplots(figsize=(9.2, 7.4), dpi=150)
    fig.patch.set_facecolor("white")

    cmap = plt.get_cmap("RdBu_r").copy()
    cmap.set_bad(color="#f0f0f0")

    im = ax.imshow(data, cmap=cmap, vmin=vmin, vmax=vmax, aspect="equal")
    ax.set_xticks(range(len(cols)))
    ax.set_yticks(range(len(cols)))
    ax.set_xticklabels(labels, rotation=40, ha="right", fontsize=13)
    ax.set_yticklabels(labels, fontsize=13)

    for i in range(len(cols)):
        for j in range(len(cols)):
            val = data[i, j]
            if np.isnan(val):
                txt = "—"
                color = "#888888"
            else:
                txt = format(val, "+.2f")
                color = "white" if val > (vmin + 0.55 * (vmax - vmin)) else "#222222"
            ax.text(j, i, txt, ha="center", va="center", fontsize=13, color=color)

    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.ax.tick_params(labelsize=12)

    fig.tight_layout()
    for ext in (".pdf", ".png"):
        fig.savefig(out_base.with_suffix(ext), bbox_inches="tight", facecolor="white")
    plt.close(fig)


def main() -> None:
    X = load_matrix()
    n = len(X)

    phi = phi_matrix(X)
    long_df = pairwise_long(X)

    long_df.to_csv(SCRIPT_DIR / "q10_pairwise_associations.csv", index=False)
    plot_phi_heatmap(phi, SCRIPT_DIR / "q10_association_heatmap_phi")

    print(f"Loaded {n} respondents from {INPUT_CSV}")
    print("Wrote:")
    print("  - q10_pairwise_associations.csv")
    print("  - q10_association_heatmap_phi.pdf / .png")
    print("\nTop pairwise associations (by phi):")
    cols_show = [
        "motive_a",
        "motive_b",
        "phi",
        "fisher_p_two_sided",
        "fdr_q_bh",
        "co_occurrence_n",
    ]
    print(long_df[cols_show].head(8).to_string(index=False))
    sig = long_df[long_df["fdr_q_bh"] < 0.05]
    print("\nPairs with FDR q_bh < 0.05 (15 tests, Benjamini–Hochberg):")
    if sig.empty:
        print("  (none)")
    else:
        print(sig[cols_show].to_string(index=False))


if __name__ == "__main__":
    main()
