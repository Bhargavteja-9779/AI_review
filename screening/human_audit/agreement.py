#!/usr/bin/env python3
"""Human-AI agreement for the audit samples (run after the human columns are filled in)."""
import csv, pathlib
from collections import Counter
HERE = pathlib.Path(__file__).resolve().parent

def kappa(pairs):
    n = len(pairs); po = sum(a == b for a, b in pairs) / n
    ca, cb = Counter(a for a, _ in pairs), Counter(b for _, b in pairs)
    pe = sum(ca[k] * cb[k] for k in set(ca) | set(cb)) / n / n
    return n, round(po, 3), round((po - pe) / (1 - pe), 3) if pe < 1 else None

rows = list(csv.DictReader((HERE / "screening_sample.csv").open()))
p = [(r["ai_decision_hidden"].strip().upper(), r["human_decision (INCLUDED/CONTEXT/EXCLUDED)"].strip().upper()) for r in rows
     if r["human_decision (INCLUDED/CONTEXT/EXCLUDED)"].strip()]
print("screening (n, agreement, kappa):", kappa(p) if p else "not yet coded")
rows = list(csv.DictReader((HERE / "tier_sample.csv").open()))
t = [(r["ai_tier_hidden"].strip().lower(), r["human_tier (core/adjacent)"].strip().lower()) for r in rows if r["human_tier (core/adjacent)"].strip()]
l = [(r["ai_layer_hidden"].strip().upper(), r["human_layer (L1-L4)"].strip().upper()) for r in rows if r["human_layer (L1-L4)"].strip()]
print("tier (n, agreement, kappa):", kappa(t) if t else "not yet coded")
print("layer (n, agreement, kappa):", kappa(l) if l else "not yet coded")
