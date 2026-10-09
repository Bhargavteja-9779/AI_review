#!/usr/bin/env python3
"""Reliability statistics reported in Section 3: stage-1 audit (Wilson 95% CI) and layer-assignment agreement
(rule-based charting vs. independent manual layer coding of the 37 anchor studies)."""
import csv, json, math, pathlib
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parent.parent


def wilson(k, n, z=1.96):
    p = k / n; d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d; h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return round(c - h, 4), round(c + h, 4)


def kappa(x, y):
    n = len(x); po = sum(a == b for a, b in zip(x, y)) / n
    cx, cy = Counter(x), Counter(y); pe = sum(cx[k] * cy[k] for k in set(x) | set(y)) / n / n
    return round(po, 3), round((po - pe) / (1 - pe), 3)


m = {r["id"]: r for r in csv.DictReader((ROOT / "evidence/master_included.csv").open())}
a = list(csv.DictReader((ROOT / "evidence/anchor_set.tsv").open(), delimiter="\t"))
x = [m[r["id"]]["framework_layer"][:2] for r in a]; y = [r["layer"][:2] for r in a]
po, k = kappa(x, y)
out = {"stage1_audit": {"sample": 120, "false_negatives": 1, "rate": round(1 / 120, 4), "wilson95": wilson(1, 120)},
       "layer_assignment_anchor": {"n": len(a), "agreement": po, "cohen_kappa": k,
                                   "disagreements": [r["id"] for r, i, j in zip(a, x, y) if i != j]},
       "interpass_screening": json.loads((ROOT / "screening/interpass_agreement.json").read_text())}
(ROOT / "screening/reliability.json").write_text(json.dumps(out, indent=2))
print(json.dumps(out, indent=2))
