"""Generate all figures for the QAM link-performance report."""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle

OUT = os.path.join(os.path.dirname(__file__), "figures")
os.makedirs(OUT, exist_ok=True)

BLUE, GREEN, RED = "#2E6BF6", "#00A88A", "#F2536D"
INK, MUTED, LINE = "#101418", "#5b6472", "#e6eaf0"

plt.rcParams.update({
    "font.family": "Helvetica",
    "font.size": 9,
    "axes.edgecolor": "#c9d0d9",
    "axes.labelcolor": INK,
    "text.color": INK,
    "xtick.color": MUTED,
    "ytick.color": MUTED,
    "axes.grid": True,
    "grid.color": "#eef1f5",
    "grid.linewidth": 0.8,
    "savefig.dpi": 220,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.05,
})


def qfunc(x):
    from math import erfc, sqrt
    return 0.5 * np.vectorize(erfc)(x / sqrt(2))


def ber(k, M, ebn0_db):
    ebn0 = 10 ** (np.asarray(ebn0_db, dtype=float) / 10)
    arg = np.sqrt(3 * k / (M - 1) * ebn0)
    return (4 / k) * (1 - 1 / np.sqrt(M)) * qfunc(arg)


def points(M):
    side = int(round(np.sqrt(M)))
    norm = np.sqrt(2 * (M - 1) / 3)
    return np.array([((2 * i - (side - 1)) / norm, (2 * j - (side - 1)) / norm)
                     for i in range(side) for j in range(side)])


# ------------------------------------------------------------------ figure 1
def fig_generations():
    fig, ax = plt.subplots(figsize=(6.3, 2.5))
    ax.set_xlim(0, 10); ax.set_ylim(0, 4); ax.axis("off")
    gens = [
        ("1G", "1980s", "Analogue\nFM voice", "—", "#b6bec9"),
        ("2G", "1991", "Digital voice\nGMSK", "64 kbps", "#9aa3b0"),
        ("3G", "2001", "Mobile data\nQPSK · 16-QAM", "2 Mbps", "#7f8b9c"),
        ("4G", "2009", "Broadband\n64-QAM · OFDMA", "1 Gbps", BLUE),
        ("5G", "2019", "Enhanced mobile\n256-QAM · NR", "20 Gbps", GREEN),
    ]
    w, gap = 1.62, 0.28
    for i, (g, yr, tech, rate, col) in enumerate(gens):
        x = 0.28 + i * (w + gap)
        ax.add_patch(FancyBboxPatch((x, 1.35), w, 1.9, boxstyle="round,pad=0.02,rounding_size=0.10",
                                    linewidth=1.1, edgecolor=col, facecolor="white"))
        ax.text(x + w / 2, 2.92, g, ha="center", va="center", fontsize=13,
                fontweight="bold", color=col)
        ax.text(x + w / 2, 2.58, yr, ha="center", va="center", fontsize=7, color=MUTED)
        ax.text(x + w / 2, 2.02, tech, ha="center", va="center", fontsize=6.6, color=INK,
                linespacing=1.5)
        ax.text(x + w / 2, 1.55, rate, ha="center", va="center", fontsize=6.4, color=col)
        if i < 4:
            ax.add_patch(FancyArrowPatch((x + w + 0.02, 2.3), (x + w + gap - 0.02, 2.3),
                                         arrowstyle="-|>", mutation_scale=8,
                                         color="#b6bec9", linewidth=1))
    ax.set_ylim(1.15, 3.45)
    fig.savefig(f"{OUT}/fig_generations.png")
    plt.close(fig)


# ------------------------------------------------------------------ figure 2
def fig_system():
    fig, ax = plt.subplots(figsize=(6.3, 1.85))
    ax.set_xlim(0, 10); ax.set_ylim(0, 3); ax.axis("off")

    def box(x, y, w, h, title, sub, col=INK):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.08",
                                    linewidth=1.0, edgecolor="#c9d0d9", facecolor="#fbfcfe"))
        ax.text(x + w / 2, y + h * 0.63, title, ha="center", va="center", fontsize=7.2,
                fontweight="bold", color=col)
        ax.text(x + w / 2, y + h * 0.28, sub, ha="center", va="center", fontsize=6.1, color=MUTED)

    def arrow(x0, x1, y=1.5, style="-|>", col="#9aa3b0"):
        ax.add_patch(FancyArrowPatch((x0, y), (x1, y), arrowstyle=style,
                                     mutation_scale=9, color=col, linewidth=1.1))

    box(0.05, 0.85, 1.45, 1.35, "Binary source", "random bits")
    arrow(1.52, 1.92)
    box(1.94, 0.85, 1.75, 1.35, "Symbol mapper", "QPSK / 16-QAM\n/ 64-QAM", BLUE)
    arrow(3.71, 4.11)
    box(4.13, 0.85, 1.60, 1.35, "AWGN channel", r"n ~ N(0, σ²)", GREEN)
    arrow(5.75, 6.15)
    box(6.17, 0.85, 1.90, 1.35, "ML demodulator", "nearest point", RED)
    arrow(8.09, 8.49)
    box(8.51, 0.85, 1.44, 1.35, "Error counter", "BER, Es/N₀")

    ax.text(5.0, 0.42, "unit symbol energy  ·  σ = 1/√(2·Es/N₀) per dimension  ·  Gray-mapped labels",
            ha="center", fontsize=6.4, color=MUTED)
    fig.savefig(f"{OUT}/fig_system.png")
    plt.close(fig)


# ------------------------------------------------------- figures 3, 4, 5
def gray_label(M, i, j, bits_per_axis):
    """Gray-coded label for point (i=in-phase index, j=quadrature index)."""
    def gray(n):
        return n ^ (n >> 1)
    side = int(round(np.sqrt(M)))
    gi = gray(side - 1 - i)      # in-phase bits, MSB first
    gj = gray(side - 1 - j)      # quadrature bits
    return format(gi, f"0{bits_per_axis}b") + format(gj, f"0{bits_per_axis}b")


def fig_constellation(M, name, colour, fname, show_labels=True):
    pts = points(M)
    side = int(round(np.sqrt(M)))
    bpa = int(np.log2(side))
    fig, ax = plt.subplots(figsize=(3.0, 3.0))
    ax.scatter(pts[:, 0], pts[:, 1], s=26, facecolors="white", edgecolors=colour,
               linewidths=1.0, zorder=3)
    if show_labels:
        for i in range(side):
            for j in range(side):
                x, y = pts[i * side + j]
                ax.text(x, y + 0.105, gray_label(M, i, j, bpa), ha="center", va="bottom",
                        fontsize=5.4, color=MUTED)
    ax.axhline(0, color="#eef1f5", linewidth=0.9, zorder=1)
    ax.axvline(0, color="#eef1f5", linewidth=0.9, zorder=1)
    ax.set_xlim(-1.28, 1.28); ax.set_ylim(-1.28, 1.36)
    ax.set_aspect("equal")
    ax.set_xlabel("In-phase  I", fontsize=7)
    ax.set_ylabel("Quadrature  Q", fontsize=7)
    ax.tick_params(labelsize=6, length=2)
    ax.grid(False)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    fig.savefig(f"{OUT}/{fname}")
    plt.close(fig)


# ------------------------------------------------------------------ figure 6
def fig_ber():
    fig, ax = plt.subplots(figsize=(5.6, 3.3))
    db = np.linspace(0, 20, 400)
    for k, M, name, col in ((2, 4, "QPSK", BLUE), (4, 16, "16-QAM", GREEN), (6, 64, "64-QAM", RED)):
        ax.semilogy(db, ber(k, M, db), color=col, linewidth=1.6, label=name)
    for x, y, col in ((6.8, 1e-3, BLUE), (10.5, 1e-3, GREEN), (14.8, 1e-3, RED)):
        ax.plot([x], [y], "o", markersize=5, color=col, zorder=5)
    ax.axhline(1e-3, color="#ccd4de", linewidth=0.9, linestyle=(0, (3, 3)), zorder=1)
    ax.text(19.6, 1.3e-3, r"BER = $10^{-3}$", fontsize=6.8, color=MUTED, ha="right")
    ax.set_xlim(0, 20); ax.set_ylim(1e-7, 1)
    ax.set_xlabel("Eb/N₀  (dB)", fontsize=8)
    ax.set_ylabel("Bit error rate", fontsize=8)
    ax.legend(frameon=False, fontsize=7.5, loc="upper right")
    ax.grid(True, which="both", color="#f4f6f9", linewidth=0.7)
    fig.savefig(f"{OUT}/fig_ber.png")
    plt.close(fig)


# ------------------------------------------------------------------ figure 7
def fig_efficiency():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(6.3, 2.5))
    names = ["QPSK", "16-QAM", "64-QAM"]
    ks = [2, 4, 6]
    cols = [BLUE, GREEN, RED]
    a1.bar(names, ks, color=cols, width=0.52)
    for i, k in enumerate(ks):
        a1.text(i, k + 0.12, f"{k} bit/sym", ha="center", fontsize=7, color=MUTED)
    a1.set_ylim(0, 7.2); a1.set_ylabel("Spectral efficiency", fontsize=8)
    a1.set_title("(a) Throughput per symbol", fontsize=8, color=INK)
    a1.grid(axis="x", visible=False)

    targets = [1e-2, 1e-3, 1e-4, 1e-5]
    for k, M, name, col in ((2, 4, "QPSK", BLUE), (4, 16, "16-QAM", GREEN), (6, 64, "64-QAM", RED)):
        req = []
        for t in targets:
            lo, hi = -10.0, 40.0
            for _ in range(80):
                mid = (lo + hi) / 2
                if ber(k, M, mid) > t:
                    lo = mid
                else:
                    hi = mid
            req.append((lo + hi) / 2)
        a2.plot(req, range(len(targets)), "o-", color=col, markersize=4.5, linewidth=1.4, label=name)
    a2.set_yticks(range(len(targets)))
    a2.set_yticklabels([f"10⁻{e}" for e in range(2, 6)], fontsize=7)
    a2.set_xlabel("Eb/N₀ required  (dB)", fontsize=8)
    a2.set_title("(b) Eb/N₀ needed per target BER", fontsize=8, color=INK)
    a2.invert_yaxis()
    a2.legend(frameon=False, fontsize=6.4, loc="upper right", handlelength=1.4,
              borderaxespad=0.2)
    for ax in (a1, a2):
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
    fig.tight_layout()
    fig.savefig(f"{OUT}/fig_efficiency.png")
    plt.close(fig)


# ------------------------------------------------------------------ figure 8
def fig_evm():
    fig, ax = plt.subplots(figsize=(5.0, 2.9))
    es = np.linspace(2, 26, 400)
    ax.plot(es, 100 / np.sqrt(10 ** (es / 10)), color="#101418", linewidth=1.5,
            label="EVM = 100/√(Es/N₀)")
    marks = [(9.79, 2, "QPSK", BLUE), (16.54, 4, "16-QAM", GREEN), (22.55, 6, "64-QAM", RED)]
    for x, k, name, col in marks:
        y = 100 / np.sqrt(10 ** (x / 10))
        ax.plot([x], [y], "o", color=col, markersize=7, zorder=5)
        ax.annotate(f"{name}\n{x:.1f} dB · {y:.0f}%", (x, y), textcoords="offset points",
                    xytext=(8, 10), fontsize=6.4, color=col)
    ax.set_xlim(0, 26); ax.set_ylim(0, 90)
    ax.set_xlabel("Es/N₀  (dB)", fontsize=8)
    ax.set_ylabel("EVM  (%)", fontsize=8)
    ax.set_title("Error vector magnitude, marked at BER = $10^{-3}$", fontsize=8)
    ax.legend(frameon=False, fontsize=7, loc="upper right")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    fig.savefig(f"{OUT}/fig_evm.png")
    plt.close(fig)


if __name__ == "__main__":
    fig_generations()
    fig_system()
    fig_constellation(4, "QPSK", BLUE, "fig_qpsk.png")
    fig_constellation(16, "16-QAM", GREEN, "fig_16qam.png")
    fig_constellation(64, "64-QAM", RED, "fig_64qam.png")
    fig_ber()
    fig_efficiency()
    fig_evm()
    print("figures:", sorted(os.listdir(OUT)))
