#!/usr/bin/env python3
"""Chart included sources onto the CUE-AWARE-ACT-RESPOND framework (deterministic assignment rules).

Assignment rules (documented in the manuscript, Section 3.6 and Table 4):
  Layer   - from the scope_area recorded at identification (mapping LAYER below); system cards and
            third-party evaluation reports are assigned to L4 (they report validity consequences).
  Method  - keyword rules on title + scope_area, applied in the order of METHOD_RULES (first match wins).
  Type    - peer-reviewed (named archival venue), preprint, or grey literature (developer/evaluator report).
Output: charting_included.csv, map_counts.json
"""
import csv, json, pathlib, re
from collections import Counter

HERE = pathlib.Path(__file__).resolve().parent

LAYER = [
    (r"eval-realism|honeypot", "L1 Context signal"),
    (r"awareness-measurement|awareness-benchmark|awareness-scaling|awareness-conceptual|awareness-overview|"
     r"situational-awareness|self-recognition|introspection|self-report|awareness \(|conceptual precursor", "L2 Awareness"),
    (r"awareness-behaviour|awareness->|eval-validity-deception|alignment-faking$|^sandbagging$|sandbagging-RL|"
     r"behavioural divergence|reward-hacking$|reward-hacking-eval|agentic-misalignment|shutdown|scheming-eval|"
     r"sabotage-eval|deception-eval|honesty-eval|conditional-behaviour|model-organisms|alternative-explanation|"
     r"reward-seeking|awareness as confound", "L3 Behavioural divergence"),
    (r".*", "L4 Validity consequence and response"),
]
METHOD_RULES = [
    (r"system card|system-card|third-party-eval|evaluation report|preparedness|pre-deployment|case-study|validity consequence",
     "Developer or third-party audit"),
    (r"probe|steer|activation|sparse autoencoder|representation|oracle|interpretab|latent|mechanis|internals|white-box|linear",
     "White-box (probes, steering, features)"),
    (r"chain-of-thought|chain of thought|\bcot\b|reasoning|monitor|faithful|verbali|hiding their reasoning|steganograph",
     "Reasoning-trace / transcript monitoring"),
    (r"noise|weight|fine-tun|finetun|password|\brl\b|training|elicit|unlearn|tamper|inoculation|supervision|exploration hacking|organism",
     "Training- or weight-based (elicitation, organisms)"),
    (r"bench|arena|dataset|environment|honeypot|replay|realis|suite|evaluations for|setting",
     "Benchmark / environment construction"),
    (r".*", "Behavioural contrast (black-box)"),
]


# Manual overrides for multi-method studies whose titles do not reveal the primary method (charted from abstracts).
OVERRIDE = {
    "arXiv:2509.13333": "White-box (probes, steering, features)", "arXiv:2507.01786": "White-box (probes, steering, features)",
    "arXiv:2505.14617": "White-box (probes, steering, features)", "arXiv:2510.20487": "White-box (probes, steering, features)",
    "arXiv:2608.21766": "White-box (probes, steering, features)", "arXiv:2606.23583": "White-box (probes, steering, features)",
    "arXiv:2603.19426": "White-box (probes, steering, features)", "arXiv:2606.29196": "White-box (probes, steering, features)",
    "arXiv:2509.18058": "White-box (probes, steering, features)", "arXiv:2509.00591": "White-box (probes, steering, features)",
    "arXiv:2505.23836": "Behavioural contrast (black-box)", "arXiv:2609.01611": "Behavioural contrast (black-box)",
    "arXiv:2605.23055": "Benchmark / environment construction", "arXiv:2605.29729": "Benchmark / environment construction",
    "arXiv:2605.26438": "Benchmark / environment construction", "arXiv:2609.22119": "Reasoning-trace / transcript monitoring",
    "arXiv:2508.00943": "Reasoning-trace / transcript monitoring", "arXiv:2603.03824": "Reasoning-trace / transcript monitoring",
    "arXiv:2509.15541": "Reasoning-trace / transcript monitoring", "arXiv:2505.17815": "Reasoning-trace / transcript monitoring",
    "arXiv:2412.01784": "Training- or weight-based (elicitation, organisms)", "arXiv:2405.19550": "Training- or weight-based (elicitation, organisms)",
    "arXiv:2502.02180": "Training- or weight-based (elicitation, organisms)", "arXiv:2512.07810": "Training- or weight-based (elicitation, organisms)",
    "arXiv:2604.28182": "Training- or weight-based (elicitation, organisms)", "arXiv:2604.00788": "Developer or third-party audit",
    "arXiv:2604.24618": "Developer or third-party audit", "arXiv:2412.04984": "Behavioural contrast (black-box)",
    "arXiv:2510.05179": "Behavioural contrast (black-box)", "arXiv:2412.14093": "Behavioural contrast (black-box)",
}


def first(rules, text):
    for pat, lab in rules:
        if re.search(pat, text, re.I):
            return lab


def src_type(r):
    v = r["venue_or_type"]
    if r["id"].startswith("grey:") or any(k in v.lower() for k in ("system card", "report", "blog", "policy")) and "preprint" not in v.lower():
        return "Grey literature"
    if "preprint" in v.lower():
        return "Preprint"
    return "Peer-reviewed"


def main():
    rows = [r for r in csv.DictReader((HERE / "screening.csv").open()) if r["decision"] == "INCLUDED"]
    out = []
    for r in rows:
        area = r["scope_area"]
        layer = "L4 Validity consequence and response" if re.search(r"system-card|third-party-eval", area) else first(LAYER, area)
        method = OVERRIDE.get(r["id"]) or first(METHOD_RULES, f"{r['title']} {area}")
        out.append({"id": r["id"], "title": r["title"], "first_author_or_org": r["first_author_or_org"], "year": r["year"],
                    "venue_or_type": r["venue_or_type"], "source_type": src_type(r), "framework_layer": layer,
                    "method_family": method, "scope_area": area, "read_level": "abstract/metadata (full text not accessible)"})
    with (HERE / "charting_included.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, out[0].keys()); w.writeheader(); w.writerows(out)
    counts = {
        "n": len(out),
        "by_layer": Counter(o["framework_layer"] for o in out),
        "by_method": Counter(o["method_family"] for o in out),
        "by_type": Counter(o["source_type"] for o in out),
        "by_year_type": {y: Counter(o["source_type"] for o in out if o["year"] == y) for y in sorted({o["year"] for o in out})},
        "layer_x_method": {l: Counter(o["method_family"] for o in out if o["framework_layer"] == l)
                           for l in sorted({o["framework_layer"] for o in out})},
    }
    (HERE / "map_counts.json").write_text(json.dumps(counts, indent=2, default=dict))
    print(json.dumps(counts, indent=2, default=dict))


if __name__ == "__main__":
    main()
