#!/usr/bin/env python3
"""Merge, deduplicate and screen all logged records; write the screening log and PRISMA-style counts.

Inputs  (unchanged): register.jsonl (detailed entries), candidates.tsv (search log of identified records)
Outputs: records_all.csv, screening.csv, prisma_counts.json

Rules are deterministic and documented in docs/03_protocol.md section 6 (v0.2 amendment):
  R0 duplicate        - same identifier already seen (first occurrence kept)
  E6 unverifiable     - identifier/title could not be confirmed from retrieved metadata ("id only", "description only",
                        placeholder titles in parentheses, or "VERIFY" with no confirmed title)
  E1 out of scope     - flagged at title/abstract screening as a different construct or a method paper unrelated to
                        evaluation validity
  E3 non-archival     - community forum posts / informal blogs (LessWrong, Alignment Forum, Substack) without an
                        archival or organisational report
  CONTEXT             - eligible publication but outside the phenomenon boundary (methodology, background theory,
                        adjacent evaluation-validity literature); retained as a contextual reference, not charted
  INCLUDED            - charted source of evidence (primary study, benchmark/method paper, developer system card
                        or third-party evaluation report)
"""
import csv, json, pathlib, re

HERE = pathlib.Path(__file__).resolve().parent

CORE = re.compile(r"^(awareness|situational-awareness$|sandbagging|alignment-faking|eval-validity-deception|eval-realism|"
                  r"countermeasure|system-card|third-party-eval|scheming-eval|sabotage-eval|honeypot-eval|cot-monitoring|"
                  r"deception-probes|probe-validity|probe-robustness|reward-hacking|elicitation$|hidden-capability|"
                  r"conditional-behaviour|model-organisms|self-recognition|introspection|self-report-validity|"
                  r"cot-faithfulness|control-|eval-validity-theory|alignment-audit|auditing-tool|backdoor-detection|"
                  r"encoded-reasoning|deception-eval|honesty-eval|agentic-misalignment|shutdown-resistance|"
                  r"training-intervention|reward-seeking|alternative-explanation|deception-detection|white-box-validity|"
                  r"behavioural|awareness->|detection|validity consequence|conceptual precursor)")


def classify(r):
    status = r["metadata_status"].lower()
    area = r["scope_area"]
    title = r["title"]
    venue = r["venue_or_type"].lower()
    if "id only" in status or "description only" in status or title.startswith("(") or \
       ("verify" in status and not any(k in status for k in ("title", "author"))):
        return "EXCLUDED", "E6", "metadata (title/identifier) not confirmable from retrieved records"
    if "exclude e1" in area.lower():
        return "EXCLUDED", "E1", "different construct or method unrelated to evaluation validity"
    if any(k in venue for k in ("lesswrong", "alignment forum", "substack")) or venue.endswith("post"):
        return "EXCLUDED", "E3", "non-archival community post"
    if CORE.match(area):
        return "INCLUDED", "", "model-originated threat to evaluation validity, or method/countermeasure addressing one"
    return "CONTEXT", "", "eligible publication outside phenomenon boundary; cited for context/method only"


def main():
    rows = []
    for line in (HERE / "register.jsonl").open():
        e = json.loads(line)
        rows.append({"id": e["id"], "title": e["title"], "first_author_or_org": e["authors"].split(",")[0],
                     "year": str(e["year"]), "venue_or_type": e["venue"], "search_batch": "B1(register)",
                     "metadata_status": e["verified_via"], "scope_area": e["layer"]})
    with (HERE / "candidates.tsv").open() as f:
        rows += list(csv.DictReader(f, delimiter="\t"))
    for r in rows:
        r["id"] = r["id"].strip()

    seen, out = {}, []
    for r in rows:
        key = r["id"].lower()
        if key in seen:
            out.append({**r, "decision": "DUPLICATE", "code": "R0", "reason": f"duplicate of row {seen[key]}"})
            continue
        seen[key] = len(out) + 1
        d, c, why = classify(r)
        out.append({**r, "decision": d, "code": c, "reason": why})

    fields = ["id", "title", "first_author_or_org", "year", "venue_or_type", "search_batch", "metadata_status",
              "scope_area", "decision", "code", "reason"]
    with (HERE / "screening.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(out)

    cnt = lambda pred: sum(1 for r in out if pred(r))
    identified = len(out)
    dup = cnt(lambda r: r["decision"] == "DUPLICATE")
    screened = identified - dup
    e6 = cnt(lambda r: r["code"] == "E6")
    e1 = cnt(lambda r: r["code"] == "E1")
    e3 = cnt(lambda r: r["code"] == "E3")
    context = cnt(lambda r: r["decision"] == "CONTEXT")
    included = cnt(lambda r: r["decision"] == "INCLUDED")
    inc = [r for r in out if r["decision"] == "INCLUDED"]
    counts = {
        "records_identified_websearch_batches": identified,
        "duplicates_removed": dup,
        "records_screened": screened,
        "excluded_E6_unverifiable_metadata": e6,
        "excluded_E1_out_of_scope": e1,
        "excluded_E3_non_archival": e3,
        "contextual_references_not_charted": context,
        "sources_included_in_evidence_map": included,
        "included_by_year": {y: sum(r["year"] == y for r in inc) for y in sorted({r["year"] for r in inc})},
    }
    assert screened == e6 + e1 + e3 + context + included, "count reconciliation failed"
    (HERE / "prisma_counts.json").write_text(json.dumps(counts, indent=2))
    print(json.dumps(counts, indent=2))


if __name__ == "__main__":
    main()
