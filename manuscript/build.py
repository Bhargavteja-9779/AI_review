#!/usr/bin/env python3
"""Assemble sections + reference list into manuscript.md, then DOCX (pandoc) and PDF (LibreOffice)."""
import pathlib, subprocess, sys, re
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from references import REFS

def sort_key(entry):
    s = entry.lstrip("*").lower()
    s = s.replace("ł", "l").replace("ö", "o").replace("ı", "i").replace("van der weij", "weij")
    return s

body = "\n\n".join(p.read_text() for p in sorted((HERE / "sections").glob("*.md")))
refs = sorted(REFS.values(), key=sort_key)
md = body + "\n\n## References\n\n" + "\n\n".join(refs) + "\n"
(HERE / "manuscript.md").write_text(md)
words = len(re.sub(r"^\|.*$", "", body.split("## References")[0], flags=re.M).split())
abstract = re.search(r"## Abstract\n\n(.*?)\n\n\*\*Keywords", body, re.S).group(1)
print("main-text words (excl. tables, refs):", words, "| abstract words:", len(abstract.split()), "| references:", len(refs))
subprocess.run(["pandoc", "manuscript.md", "-o", "manuscript.docx", "--resource-path=.", "-f", "markdown+pipe_tables+superscript",
                "--reference-doc=reference.docx"] if (HERE / "reference.docx").exists() else
               ["pandoc", "manuscript.md", "-o", "manuscript.docx", "--resource-path=.", "-f", "markdown+pipe_tables+superscript"],
               cwd=HERE, check=True)
subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "manuscript.docx"], cwd=HERE, check=True,
               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print("built:", [p.name for p in HERE.iterdir() if p.suffix in (".docx", ".pdf", ".md") and p.stem == "manuscript"])
