# 00 — Execution Capability Audit

Audit date: 2026-10-09. Environment: managed cloud container (Linux), Python 3.13, pandoc, LibreOffice, Node 22. No LaTeX, no R, no matplotlib installed (installable from PyPI, which is reachable).

## Network findings (tested, not assumed)

| Resource | Test | Result |
|---|---|---|
| api.openalex.org | `curl` via agent proxy | **403 at proxy CONNECT (egress policy)** |
| api.crossref.org | same | **403** |
| api.semanticscholar.org | same | **403** |
| export.arxiv.org | same | **403** |
| dblp.org | same | **403** |
| api.elsevier.com (Scopus) | same | **403** (and would need an institutional key anyway) |
| doi.org | `curl` + WebFetch | **403 / DNS failure** |
| link.springer.com, www.springer.com, dl.acm.org, ieeexplore.ieee.org, aclanthology.org | `curl` + WebFetch | **403 / DNS failure** |
| WebSearch tool | live query | **Works**, but returns *summarized* results, not full records or full text |
| pypi.org | proxy noProxy list | reachable |

The user chose (2026-10-09) to widen network access. A re-test right after that answer was still blocked, consistent with policy changes applying to a new container.

## Operation classification

| Operation | Status |
|---|---|
| Topic scouting / novelty pilot via web search | EXECUTABLE WITH AVAILABLE TOOLS (done; see `02_topic_and_novelty.md`) |
| Journal policy verification | PARTIAL — only via search-result summaries; official pages unreachable |
| JCR metrics (Clarivate) | NOT CURRENTLY VERIFIABLE (licensed; no access) |
| Scopus / Web of Science searches | REQUIRES EXTERNAL ACCESS (licensed; not available in this container under any network setting without institutional credentials) |
| OpenAlex / arXiv / Semantic Scholar / Crossref / DBLP searches | REQUIRES EXTERNAL ACCESS — scripts written (`search/run_searches.py`), **not executed** |
| DOI resolution / reference verification | REQUIRES EXTERNAL ACCESS |
| Full-text screening and extraction | REQUIRES EXTERNAL ACCESS (arXiv/ACL/OpenReview PDFs) |
| Deduplication, count ledger, PRISMA arithmetic | DIRECTLY EXECUTABLE (script written; awaits data) |
| Manuscript drafting, figures, DOCX/PDF build | EXECUTABLE (pandoc + LibreOffice); deferred until evidence base exists (master prompt §30) |
| Plagiarism scan | NOT AVAILABLE — will not be claimed |
| Author details, declarations | REQUIRES USER-PROVIDED INFORMATION |
| Journal submission | NOT PERFORMED — authors only |

## Recovery route

1. In the cloud environment settings (session title bar → environment → Edit → Network access), allow at least:
   `api.openalex.org, api.crossref.org, api.semanticscholar.org, export.arxiv.org, arxiv.org, dblp.org, doi.org, aclanthology.org, openreview.net, link.springer.com, www.springer.com, dl.acm.org`
   (docs: https://code.claude.com/docs/en/cloud-environments#network-access).
2. Start a new session on branch `pnbt/keen-curie-urd5f4` (or this one after the container restarts) and run `python3 search/run_searches.py --execute`.
3. Scopus/WoS remain unavailable without an institutional API key; the manuscript will state this explicitly rather than claim those databases were searched.
