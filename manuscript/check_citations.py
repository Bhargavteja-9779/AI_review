#!/usr/bin/env python3
"""Cross-check in-text citations against references.py (both directions). Exit 1 on any mismatch."""
import pathlib, re, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from references import REFS

text = "\n".join(p.read_text() for p in sorted((pathlib.Path(__file__).parent / "sections").glob("*.md")))
plain = text.replace("*", "")
used, missing = set(), []
for k in REFS:
    m = re.match(r"(.*?)\s(\d{4}[a-c]?)$", k)
    name, yr = m.group(1), m.group(2)
    if re.search(re.escape(name) + r"\s\(?" + re.escape(yr) + r"\b", plain):
        used.add(k)
unused = sorted(set(REFS) - used)
# find citation-like strings and check each maps to a key
pat = re.compile(r"([A-ZŁÖÜ][\w'’ıłöüé\-]+(?: [A-Z])?(?: et al\.| and [A-ZŁÖÜ][\w'’ıłöüé\-]+)?) \(?(\d{4}[a-c]?)\)?")
cands = set()
for m in pat.finditer(plain):
    s = f"{m.group(1)} {m.group(2)}"
    if not any(s == k or k.endswith(s) or s.endswith(k) for k in REFS):
        cands.add(s)
noise = re.compile(r"^(In|Fig|Table|Section|Version|January|October|September|Since|The|Both|Of|And|Across|From|Oct|Supplementary|ICML|ICLR|NeurIPS|PRISMA|AUC|GPT|Claude|Llama|Qwen|Gemini|Opus|Sonnet|Mythos|Before|First|Second|Third|Relative|Reports|Charted|To|At|Twenty|With|For|Earlier|Only|After|Up|Under|Each|When|Unlike|This|Some|However|Several|Evidence|Deliberate|Scholar|Xiv|Scopus)\b")
cands = sorted(c for c in cands if not noise.match(c))
print("references:", len(REFS), "cited:", len(used))
print("UNCITED references:", unused)
print("POSSIBLE citations without reference:", cands)
sys.exit(1 if unused or cands else 0)
