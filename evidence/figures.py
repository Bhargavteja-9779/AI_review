#!/usr/bin/env python3
"""Generate manuscript figures from screening/prisma2020.json and master_counts.json (no hard-coded counts)."""
import json, pathlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE.parent / "manuscript" / "figures"
OUT.mkdir(parents=True, exist_ok=True)
P = json.loads((HERE.parent / "screening" / "prisma2020.json").read_text())
M = json.loads((HERE / "master_counts.json").read_text())

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
    """PRISMA 2020 flow: databases and other methods; automation-tool exclusions shown separately (screening/prisma2020.json)."""
    d, o, t = P["databases"], P["other_methods"], M["by_type"]
    src = d["identified_by_source"]
    fbox = lambda *a, **k: box(*a, **{"fs": 7.0, **k})
    fig, ax = plt.subplots(figsize=(7.8, 9.2)); ax.set_xlim(0, 12); ax.set_ylim(-0.3, 14.4); ax.axis("off")
    ax.text(1.8, 14.25, "Identification via databases", ha="center", fontsize=9, fontweight="bold", color=S1)
    ax.text(9.55, 14.25, "Identification via other methods", ha="center", fontsize=9, fontweight="bold", color=S2)
    fbox(ax, 0.1, 12.3, 3.4, 1.6, f"Records identified\n(9 Oct 2026) n = {d['identified_total']}\nScopus {src['Scopus']} | arXiv {src['arXiv']}\n"
         f"Semantic Scholar {src['SemanticScholar']}", fc="#e8f1fb", ec=S1)
    fbox(ax, 3.75, 12.3, 3.1, 1.6, f"Removed before screening\nduplicates (automatic): {d['duplicates_removed_automatic']}\n"
         f"version duplicates\n(manual): {d['version_duplicates_removed_manual']}", fc=SURF)
    fbox(ax, 7.2, 12.3, 4.7, 1.6, f"Records identified in 25 logged\nweb-search batches n = {o['identified_web_batches']}\n"
         f"duplicates within batches removed: {o['duplicates_within_web']}\nunique web records n = {o['web_records']}", fc="#fdeee7", ec=S2)
    auto = d["excluded_stage1_rule"] + d["excluded_rescue_screen"] + 27
    fbox(ax, 0.1, 10.1, 3.4, 1.4, f"Records after deduplication\nn = {d['records_screened']}")
    fbox(ax, 3.75, 9.75, 3.1, 2.1, f"Marked ineligible by\nautomation tool (rule-based\npre-screen): {auto}\nof which re-flagged by\nrescue pattern and\nscreened manually: 399", fc=SURF, fs=6.6)
    manual = d["records_screened"] - d["excluded_stage1_rule"]
    fbox(ax, 0.1, 7.7, 3.4, 1.4, f"Records screened manually\n(title and abstract)\nn = {manual}")
    fbox(ax, 3.75, 7.45, 3.1, 1.9, f"Records excluded n = {d['excluded_rescue_screen'] + d['excluded_stage2_title_abstract'] - (d['excluded_stage1_rule'] + d['excluded_rescue_screen'] + d['excluded_stage2_title_abstract'] - d['final_excluded'])}\n"
         f"rescue set: {d['excluded_rescue_screen']}\nstage 2: {d['excluded_stage2_title_abstract']}\n(1 reinstated at\nreconciliation)", fc=SURF, fs=6.6)
    fbox(ax, 7.2, 9.9, 4.7, 1.5, f"Already retrieved by the database\nsearch (counted there) n = {o['already_retrieved_by_databases']}\n"
         f"Records screened (title, venue,\nsummary) n = {o['records_assessed']}")
    ex = o["excluded_by_code"]
    fbox(ax, 7.2, 7.6, 4.7, 1.7, f"Records excluded n = {sum(ex.values())}\nE6 unverifiable metadata: {ex['E6']}\n"
         f"E1 out of scope: {ex['E1']}\nE3 non-archival post: {ex['E3']}", fc=SURF)
    fbox(ax, 0.1, 5.2, 3.4, 1.6, f"Eligible records n = {d['final_included'] + d['final_context']}\n(eligibility judged on title\nand abstract; no full-text\nexclusion stage)")
    fbox(ax, 3.75, 5.2, 3.1, 1.6, f"Contextual references\n(not charted) n = {d['final_context']}", fc=SURF)
    fbox(ax, 7.2, 5.2, 4.7, 1.6, f"Eligible records n = {o['final_included'] + o['final_context']}\n"
         f"contextual references\n(not charted): {o['final_context']}")
    fbox(ax, 2.4, 3.55, 7.2, 0.95, f"Studies charted n = {P['total_included']} (databases {d['final_included']} | other methods {o['final_included']});\n"
         "one written tier rule applied to every study (Section 3.2)", fs=7.0)
    fbox(ax, 0.6, 1.25, 5.0, 1.75, f"Core studies: evidence map\nn = {P['total_core']}\n(databases {d['final_core']} | other methods {o['final_core']})\n"
         f"anchor set read in full: 37", fc="#e8f1fb", ec=S1, bold=True, fs=7.6)
    fbox(ax, 6.4, 1.25, 5.0, 1.75, f"Adjacent studies: charted,\nused in Section 4.8\nn = {P['total_adjacent']}\n(databases {d['final_adjacent']} | other methods {o['final_adjacent']})",
         fc="#f4f3f0", ec=MUTED, fs=7.6)
    ax.text(6.0, 0.85, f"Core tier by source type: archival peer-reviewed {t['Peer-reviewed (archival)']} | workshop {t['Workshop paper']} | "
            f"preprint {t['Preprint']} | grey literature {t['Grey literature']}", ha="center", fontsize=7, color=INK2)
    arrow(ax, 1.8, 12.3, 1.8, 11.5); arrow(ax, 1.8, 10.1, 1.8, 9.1); arrow(ax, 1.8, 7.7, 1.8, 6.8); arrow(ax, 1.8, 5.2, 4.2, 4.5)
    arrow(ax, 3.5, 13.1, 3.75, 13.1); arrow(ax, 3.5, 10.8, 3.75, 10.8); arrow(ax, 3.5, 8.4, 3.75, 8.4); arrow(ax, 3.5, 6.0, 3.75, 6.0)
    arrow(ax, 9.55, 12.3, 9.55, 11.4); arrow(ax, 9.55, 9.9, 9.55, 9.3); arrow(ax, 9.55, 7.6, 9.55, 6.8); arrow(ax, 9.55, 5.2, 7.8, 4.5)
    arrow(ax, 4.5, 3.55, 3.1, 3.0); arrow(ax, 7.5, 3.55, 8.9, 3.0)
    ax.text(0.1, 0.45, "Records found by both routes are counted once, in the databases column. Tiers are assigned independently of the route of identification.\n"
            "Counts are generated by search/dedup.py, screening/screen_db.py and screening/merge.py.", fontsize=6.3, color=INK2, va="top")
    fig.savefig(OUT / "fig1_selection_flow.png", dpi=300, bbox_inches="tight", facecolor=SURF); plt.close(fig)


def fig_framework():
    fig, ax = plt.subplots(figsize=(7.2, 4.4)); ax.set_xlim(0, 12); ax.set_ylim(-0.2, 7.0); ax.axis("off")
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
    for i, lab in enumerate([r"$S\sim Q_c(\cdot\,|\,x)$", r"$A=a(x,S)$", r"$\Delta_{\mathrm{ctx}}$", r"$\Delta_{\mathrm{score}},\ \Delta_{\mathrm{elic}};\ \theta_E-\theta_D$"]):
        ax.text(0.2 + 3.0 * i + 1.35, 0.15, lab, ha="center", va="center", fontsize=8, color=S1 if i < 3 else S2)
    ax.annotate("", xy=(1.55, 4.65), xytext=(10.55, 4.65),
                arrowprops=dict(arrowstyle="-|>", color=S2, lw=1, connectionstyle="arc3,rad=0.3", linestyle="--"))
    ax.text(6.0, 6.55, "Countermeasures act back on L1-L3 (realism engineering, steering, elicitation, training)",
            ha="center", fontsize=8, color=S2)
    ax.annotate("", xy=(7.4, 4.65), xytext=(1.9, 4.65),
                arrowprops=dict(arrowstyle="-|>", color=INK2, lw=0.9, connectionstyle="arc3,rad=-0.12"))
    ax.text(4.65, 5.05, "direct cue-reactive path (no change in awareness)", ha="center", fontsize=7, color=INK2,
            bbox=dict(fc=SURF, ec="none", pad=0.5))
    fig.savefig(OUT / "fig4_framework.png", dpi=300, bbox_inches="tight", facecolor=SURF); plt.close(fig)


def fig_years():
    yt = M["by_year_type"]; years = sorted(yt)
    types = [("Peer-reviewed (archival)", S1), ("Workshop paper", "#9cc3ef"), ("Preprint", S2), ("Grey literature", S3)]
    fig, ax = plt.subplots(figsize=(6.0, 3.2))
    bottom = [0] * len(years)
    for name, c in types:
        vals = [yt[y].get(name, 0) for y in years]
        ax.bar(years, vals, bottom=bottom, color=c, width=0.6, label=name, edgecolor=SURF, linewidth=2)
        bottom = [b + v for b, v in zip(bottom, vals)]
    for x, b in zip(years, bottom):
        ax.text(x, b + 2, str(b), ha="center", fontsize=8, color=INK)
    ax.set_ylabel("Core studies (n)"); ax.spines[["top", "right"]].set_visible(False)
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
    cb = fig.colorbar(im, ax=ax, fraction=0.03, pad=0.02); cb.outline.set_visible(False); cb.set_label("Core studies (n)", fontsize=8)
    fig.savefig(OUT / "fig3_evidence_map.png", dpi=300, bbox_inches="tight", facecolor=SURF); plt.close(fig)


if __name__ == "__main__":
    fig_flow(); fig_framework(); fig_years(); fig_map()
    print(sorted(p.name for p in OUT.iterdir()))
