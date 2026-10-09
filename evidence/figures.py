#!/usr/bin/env python3
"""Generate manuscript figures from prisma_counts.json and map_counts.json (no hard-coded counts)."""
import json, pathlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE.parent / "manuscript" / "figures"
OUT.mkdir(parents=True, exist_ok=True)
P = json.loads((HERE / "prisma_counts.json").read_text())
M = json.loads((HERE / "map_counts.json").read_text())

INK, INK2, MUTED, GRID, SURF = "#0b0b0b", "#52514e", "#8a8984", "#e4e3df", "#ffffff"
S1, S2, S3 = "#2a78d6", "#eb6834", "#1baf7a"  # validated categorical slots 1-3
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "text.color": INK, "axes.labelcolor": INK2,
                     "xtick.color": INK2, "ytick.color": INK2, "axes.edgecolor": MUTED})


def box(ax, x, y, w, h, text, fc="#f4f3f0", ec=MUTED, bold=False, fs=8.5):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.02", fc=fc, ec=ec, lw=1))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs,
            fontweight="bold" if bold else "normal", color=INK)


def arrow(ax, x1, y1, x2, y2):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle="-|>", color=INK2, lw=1))


def fig_flow():
    fig, ax = plt.subplots(figsize=(7.2, 6.4)); ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis("off")
    L, W = 0.4, 5.0
    box(ax, L, 8.6, W, 1.1, f"Records identified in logged\nweb-search batches (9 Oct 2026)\nn = {P['records_identified_websearch_batches']}")
    box(ax, L, 6.9, W, 0.9, f"Records after duplicate removal\nn = {P['records_screened']}")
    box(ax, 6.0, 6.9, 3.6, 0.9, f"Duplicates removed\nn = {P['duplicates_removed']}", fc=SURF)
    box(ax, L, 5.0, W, 1.1, f"Records screened on title, abstract and\nretrievable metadata\nn = {P['records_screened']}")
    excl = (f"Excluded n = {P['excluded_E6_unverifiable_metadata'] + P['excluded_E1_out_of_scope'] + P['excluded_E3_non_archival']}\n"
            f"E6 unverifiable metadata: {P['excluded_E6_unverifiable_metadata']}\n"
            f"E1 out of scope: {P['excluded_E1_out_of_scope']}\n"
            f"E3 non-archival forum post: {P['excluded_E3_non_archival']}")
    box(ax, 6.0, 4.75, 3.6, 1.6, excl, fc=SURF)
    box(ax, L, 3.1, W, 1.1, f"Eligible publications\nn = {P['sources_included_in_evidence_map'] + P['contextual_references_not_charted']}")
    box(ax, 6.0, 3.1, 3.6, 1.1, f"Contextual / methodological\nreferences (not charted)\nn = {P['contextual_references_not_charted']}", fc=SURF)
    t = M["by_type"]
    box(ax, L, 0.9, W, 1.5, f"Sources charted in the evidence map\nn = {P['sources_included_in_evidence_map']}\n"
        f"preprints {t['Preprint']} | peer-reviewed {t['Peer-reviewed']}\ngrey literature {t['Grey literature']}*",
        fc="#e8f1fb", ec=S1, bold=False)
    for y1, y2 in ((8.6, 7.8), (6.9, 6.1), (5.0, 4.2), (3.1, 2.4)):
        arrow(ax, L + W / 2, y1, L + W / 2, y2)
    for y in (7.35, 5.55, 3.65):
        arrow(ax, L + W, y, 6.0, y)
    ax.text(0.4, 0.25, "*Source type assigned by evidence/chart.py; all counts reproduced by evidence/screen.py and chart.py.",
            fontsize=7, color=INK2)
    fig.savefig(OUT / "fig1_selection_flow.png", dpi=300, bbox_inches="tight", facecolor=SURF); plt.close(fig)


def fig_framework():
    fig, ax = plt.subplots(figsize=(7.2, 3.8)); ax.set_xlim(0, 12); ax.set_ylim(0, 6.3); ax.axis("off")
    layers = [("L1  CONTEXT\nSIGNAL", "Evaluation properties\nmaking it\nrecognisable: format,\nrealism, synthetic\nprompts, honeypot cues"),
              ("L2  AWARENESS", "Model recognition:\nrepresented (probes),\nverbalised (CoT),\nelicited\n(classification)"),
              ("L3  BEHAVIOURAL\nDIVERGENCE", "Evaluation-conditioned\nbehaviour: sandbagging,\nalignment/eval faking,\nstrategic dishonesty,\ntest/grader gaming"),
              ("L4  VALIDITY\nCONSEQUENCE", "Score-to-deployment\ngap and responses:\ndetection, elicitation,\nsuppression, redesign,\nreporting")]
    x = 0.2
    for i, (h, b) in enumerate(layers):
        box(ax, x, 3.3, 2.7, 1.3, h, fc="#e8f1fb" if i < 3 else "#fdeee7", ec=S1 if i < 3 else S2, bold=True, fs=8)
        box(ax, x, 0.5, 2.7, 2.5, b, fc=SURF, fs=7)
        if i < 3:
            arrow(ax, x + 2.7, 3.95, x + 3.0, 3.95)
        x += 3.0
    ax.annotate("", xy=(1.55, 4.75), xytext=(10.55, 4.75),
                arrowprops=dict(arrowstyle="-|>", color=S2, lw=1, connectionstyle="arc3,rad=0.12", linestyle="--"))
    ax.text(6.0, 5.95, "Countermeasures act back on L1-L3 (realism engineering, steering, elicitation, training)",
            ha="center", fontsize=8, color=INK2)
    fig.savefig(OUT / "fig4_framework.png", dpi=300, bbox_inches="tight", facecolor=SURF); plt.close(fig)


def fig_years():
    yt = M["by_year_type"]; years = sorted(yt)
    types = [("Peer-reviewed", S1), ("Preprint", S2), ("Grey literature", S3)]
    fig, ax = plt.subplots(figsize=(6.0, 3.2))
    bottom = [0] * len(years)
    for name, c in types:
        vals = [yt[y].get(name, 0) for y in years]
        ax.bar(years, vals, bottom=bottom, color=c, width=0.6, label=name, edgecolor=SURF, linewidth=2)
        bottom = [b + v for b, v in zip(bottom, vals)]
    for x, b in zip(years, bottom):
        ax.text(x, b + 1.5, str(b), ha="center", fontsize=8, color=INK)
    ax.set_ylabel("Charted sources (n)"); ax.spines[["top", "right"]].set_visible(False)
    ax.yaxis.grid(True, color=GRID, lw=0.6); ax.set_axisbelow(True)
    ax.legend(frameon=False, fontsize=8, loc="upper left")
    ax.text(1.0, -0.22, "2026 covers January to early October only.", transform=ax.transAxes, ha="right", fontsize=7, color=INK2)
    fig.savefig(OUT / "fig2_sources_by_year.png", dpi=300, bbox_inches="tight", facecolor=SURF); plt.close(fig)


def fig_map():
    lm = M["layer_x_method"]
    layers = ["L1 Context signal", "L2 Awareness", "L3 Behavioural divergence", "L4 Validity consequence and response"]
    methods = ["Behavioural contrast (black-box)", "Benchmark / environment construction", "Reasoning-trace / transcript monitoring",
               "White-box (probes, steering, features)", "Training- or weight-based (elicitation, organisms)", "Developer or third-party audit"]
    data = [[lm.get(l, {}).get(m, 0) for m in methods] for l in layers]
    ramp = matplotlib.colors.LinearSegmentedColormap.from_list("blue", ["#f3f7fd", "#9cc3ef", "#2a78d6", "#123f78"])
    fig, ax = plt.subplots(figsize=(7.2, 3.4))
    im = ax.imshow(data, cmap=ramp, aspect="auto")
    vmax = max(max(r) for r in data)
    for i, r in enumerate(data):
        for j, v in enumerate(r):
            ax.text(j, i, v, ha="center", va="center", fontsize=9, color="#ffffff" if v > vmax * 0.55 else INK)
    short = ["Behavioural\ncontrast", "Benchmark /\nenvironment", "Reasoning-trace\nmonitoring", "White-box\n(probes, steering)", "Training- /\nweight-based", "Developer /\nthird-party audit"]
    ax.set_xticks(range(len(methods)), short, fontsize=7)
    ax.set_yticks(range(len(layers)), [l.replace(" and ", "\nand ") for l in layers], fontsize=8)
    ax.set_xticks([x - 0.5 for x in range(1, len(methods))], minor=True); ax.set_yticks([y - 0.5 for y in range(1, len(layers))], minor=True)
    ax.grid(which="minor", color=SURF, lw=2); ax.tick_params(which="both", length=0)
    for s in ax.spines.values(): s.set_visible(False)
    cb = fig.colorbar(im, ax=ax, fraction=0.03, pad=0.02); cb.outline.set_visible(False); cb.set_label("Charted sources (n)", fontsize=8)
    fig.savefig(OUT / "fig3_evidence_map.png", dpi=300, bbox_inches="tight", facecolor=SURF); plt.close(fig)


if __name__ == "__main__":
    fig_flow(); fig_framework(); fig_years(); fig_map()
    print(sorted(p.name for p in OUT.iterdir()))
