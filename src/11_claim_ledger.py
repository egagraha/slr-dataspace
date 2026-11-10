"""Step 11. Claim ledger for the Results section (Protocol B, step 2).

Extracts every sentence and table row in the manuscript's Results section that
cites a source, one row per (sentence, cited key), and links each key to its DOI
and to the evidence level of its placement under the research question of that
subsection. The coding columns are left empty; see protocol/tension_codebook_v1.md.

Usage:
    uv run python src/11_claim_ledger.py <manuscript.tex> <references.bib>

The manuscript is not part of this repository, so its path is passed in.
Output: results/evidence/source_claims.csv
"""
import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/evidence"
OUT.mkdir(parents=True, exist_ok=True)
tex_path, bib_path = Path(sys.argv[1]), Path(sys.argv[2])

tex = tex_path.read_text(encoding="utf-8")
tex = re.sub(r"(?<!\\)%.*", "", tex)
start = tex.index("\\section{Results}")
end = tex.index("\\section{", start + 10)
body = tex[start:end]

# bib: key -> doi
bib = bib_path.read_text(encoding="utf-8")
key_doi = {}
for m in re.finditer(r"@\w+\{([^,]+),(.*?)\n\}", bib, re.S):
    d = re.search(r"\bdoi\s*=\s*\{([^}]*)\}", m.group(2))
    key_doi[m.group(1).strip()] = d.group(1).strip().lower() if d else ""

# placements: doi -> {rq: evidence}
ev = {}
for p in csv.DictReader((ROOT / "results/audit/placements.csv").open(encoding="utf-8")):
    ev.setdefault(p["doi"], {})[p["rq"]] = p["evidence_placement"]

CITE = re.compile(r"\\cite(?:t|p|alt|alp|author|year)?\*?(?:\[[^\]]*\]){0,2}\{([^}]*)\}")
FINDING = re.compile(r"\b(show|shows|showed|find|finds|found|report|reports|reported|demonstrate|"
                     r"demonstrates|evaluate|evaluates|evaluated|measure|measures|measured|test|tests|tested)\b")
ABBR = ["et al.", "e.g.", "i.e.", "cf.", "vs.", "Fig.", "Sect.", "No."]


def plain(s):
    s = CITE.sub(lambda m: "[" + m.group(1) + "]", s)
    s = re.sub(r"\\(?:emph|textbf|textit)\{([^}]*)\}", r"\1", s)
    s = re.sub(r"~?\\ref\{[^}]*\}", " [ref]", s)
    s = s.replace("~", " ").replace("--", "-").replace("\\&", "&")
    return re.sub(r"\s+", " ", s).strip()


def sentences(par):
    for i, a in enumerate(ABBR):
        par = par.replace(a, f"@@{i}@@")
    parts = re.split(r"(?<=[.?!])\s+(?=[A-Z\\])", par)
    out = []
    for p in parts:
        for i, a in enumerate(ABBR):
            p = p.replace(f"@@{i}@@", a)
        out.append(p)
    return out


rows, n = [], 0
sub = "4 Results"
rq = ""
table = None
for line in body.splitlines():
    m = re.match(r"\\subsection\{(.*)\}", line)
    if m:
        sub = m.group(1)
        r = re.match(r"(RQ[1-5])", sub)
        rq = r.group(1) if r else ""
        continue
    m = re.search(r"\\label\{(tab:[^}]*)\}", line)
    if m:
        table = m.group(1)
    if "\\end{table}" in line:
        table = None
    if not CITE.search(line):
        continue
    units = [line] if table else sentences(re.sub(r"\\paragraph\{[^}]*\}", "", line))
    for u in units:
        keys = [k.strip() for m in CITE.finditer(u) for k in m.group(1).split(",")]
        if not keys:
            continue
        n += 1
        text = plain(u.rstrip("\\ ").strip())
        for k in dict.fromkeys(keys):
            doi = key_doi.get(k, "")
            lv = ev.get(doi, {})
            level = lv.get(rq) or (max(lv.values(), key="MSA".index) if lv else "")
            rows.append(dict(
                claim_id=f"CL{n:04d}", subsection=sub, rq=rq,
                location=f"table {table}" if table else "prose", sentence=text, cite_key=k, doi=doi,
                in_corpus=int(bool(lv)), evidence_level=level if lv else "context",
                evidence_from_same_rq=int(rq in lv) if lv else "",
                check_first=int(level == "M" and bool(FINDING.search(text))),
                claim_type="", tension="", counter="", supporting_passage="", page="",
                evidence_depth_used="", coder="", note=""))

cols = list(rows[0])
with (OUT / "source_claims.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=cols)
    w.writeheader()
    w.writerows(rows)
missing = sorted({r["cite_key"] for r in rows if not r["doi"]})
print(f"{n} citing sentences or table rows, {len(rows)} claim-source rows, "
      f"{len({r['cite_key'] for r in rows})} distinct sources")
print("evidence levels:", {k: sum(r["evidence_level"] == k for r in rows) for k in ("A", "S", "M", "context")})
print("flagged check_first (metadata-only source with a finding verb):", sum(r["check_first"] for r in rows))
if missing:
    print("keys without DOI (legislation or similar):", ", ".join(missing))
