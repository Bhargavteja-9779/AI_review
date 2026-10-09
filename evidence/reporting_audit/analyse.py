#!/usr/bin/env python3
"""Reporting audit of the 37 anchor studies against the 12-item EVAL-AWARE checklist (Section 5.4, Table 8).

Inputs : coder_A*.json (primary coding, full texts), coder_B.json (independent second coding of a random 10, seed 20261009)
Outputs: audit_primary.csv (study x item codes), audit_summary.json (adherence per item, agreement statistics),
         ../../manuscript/figures/fig5_reporting_audit.png
Adherence = (Y + 0.5 P) / (Y + P + N) among studies to which the item applies.
"""
import csv, json, pathlib
from collections import Counter
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent.parent
ITEMS = [str(i) for i in range(1, 13)]
SHORT = ["1 Construct named", "2 Format-decorrelated probes", "3 Probe layer + control", "4 Generator + transfer",
         "5 Bias direction", "6 Elicitation effort", "7 With/without exclusions", "8 Cue-ablated variant",
         "9 Verbalised rate as bound", "10 Per-model results", "11 Uncertainty", "12 Access level"]

primary = {}
for f in sorted(HERE.glob("coder_A*.json")):
    primary.update(json.loads(f.read_text()))
second = json.loads((HERE / "coder_B.json").read_text())
anchors = list(csv.DictReader((ROOT / "evidence/anchor_set.tsv").open(), delimiter="\t"))
ids = [a["id"].replace("arXiv:", "") for a in anchors]
cite = {a["id"].replace("arXiv:", ""): a["cite"] for a in anchors}
assert set(ids) == set(primary), set(ids) ^ set(primary)

code = lambda d, s, i: d[s][i]["code"].strip().upper()
with (HERE / "audit_primary.csv").open("w", newline="") as fh:
    w = csv.writer(fh); w.writerow(["arxiv_id", "cite"] + [f"item{i}" for i in ITEMS])
    for s in ids:
        w.writerow([s, cite[s]] + [code(primary, s, i) for i in ITEMS])

per_item = {}
for i, lab in zip(ITEMS, SHORT):
    c = Counter(code(primary, s, i) for s in ids)
    app = c["Y"] + c["P"] + c["N"]
    per_item[lab] = {"Y": c["Y"], "P": c["P"], "N": c["N"], "NA": c["NA"], "applicable": app,
                     "adherence": round((c["Y"] + 0.5 * c["P"]) / app, 3) if app else None}
study_adh = []
for s in ids:
    c = Counter(code(primary, s, i) for i in ITEMS); app = c["Y"] + c["P"] + c["N"]
    study_adh.append((c["Y"] + 0.5 * c["P"]) / app)
study_adh.sort()

def kappa(pairs):
    n = len(pairs); po = sum(a == b for a, b in pairs) / n
    ca, cb = Counter(a for a, _ in pairs), Counter(b for _, b in pairs)
    pe = sum(ca[k] * cb[k] for k in set(ca) | set(cb)) / n / n
    return round(po, 3), round((po - pe) / (1 - pe), 3)

dual = sorted(second)
pairs4 = [(code(primary, s, i), code(second, s, i)) for s in dual for i in ITEMS]
appl = [("NA" if a == "NA" else "A", "NA" if b == "NA" else "A") for a, b in pairs4]
both = [(a, b) for a, b in pairs4 if a != "NA" and b != "NA"]
ord3 = [(a, b) for a, b in both]
summary = {
    "n_studies": len(ids), "per_item": per_item,
    "study_adherence": {"median": round(study_adh[len(study_adh) // 2], 3), "min": round(study_adh[0], 3),
                        "max": round(study_adh[-1], 3)},
    "agreement": {"dual_coded_studies": len(dual), "cells": len(pairs4),
                  "four_category": dict(zip(("agreement", "kappa"), kappa(pairs4))),
                  "applicability": dict(zip(("agreement", "kappa"), kappa(appl))),
                  "code_given_both_applicable": dict(zip(("agreement", "kappa"), kappa(ord3))) | {"n": len(ord3)}},
}
(HERE / "audit_summary.json").write_text(json.dumps(summary, indent=2))
print(json.dumps(summary, indent=2))

# figure: studies x items heatmap
val = {"Y": 3, "P": 2, "N": 1, "NA": 0}
order = sorted(ids, key=lambda s: (-sum(val[code(primary, s, i)] for i in ITEMS)))
data = [[val[code(primary, s, i)] for i in ITEMS] for s in order]
cmap = ListedColormap(["#f1f0ec", "#eb6834", "#9cc3ef", "#2a78d6"])
fig, ax = plt.subplots(figsize=(7.4, 8.6))
ax.imshow(data, cmap=cmap, vmin=-0.5, vmax=3.5, aspect="auto")
ax.set_xticks(range(12), SHORT, rotation=55, ha="right", fontsize=7.5)
ax.set_yticks(range(len(order)), [cite[s] for s in order], fontsize=7)
ax.set_xticks([x - 0.5 for x in range(1, 12)], minor=True); ax.set_yticks([y - 0.5 for y in range(1, len(order))], minor=True)
ax.grid(which="minor", color="#ffffff", lw=1.2); ax.tick_params(which="both", length=0)
for sp in ax.spines.values(): sp.set_visible(False)
adh = [per_item[l]["adherence"] for l in SHORT]
for j, a in enumerate(adh):
    ax.text(j, -0.9, "–" if a is None else f"{100*a:.0f}%", ha="center", va="bottom", fontsize=7, color="#0b0b0b")
ax.text(-0.6, -0.9, "Adherence", ha="right", va="bottom", fontsize=7, color="#52514e")
from matplotlib.patches import Patch
ax.legend(handles=[Patch(color="#2a78d6", label="Reported (Y)"), Patch(color="#9cc3ef", label="Partly (P)"),
                   Patch(color="#eb6834", label="Not reported (N)"), Patch(color="#f1f0ec", label="Not applicable")],
          loc="upper center", bbox_to_anchor=(0.5, -0.2), ncol=4, frameon=False, fontsize=7.5)
fig.savefig(ROOT / "manuscript/figures/fig5_reporting_audit.png", dpi=300, bbox_inches="tight", facecolor="#ffffff")
