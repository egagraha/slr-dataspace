"""Step 1. Parse data/raw/References-Lists.md into one row per unique DOI.

Input : data/raw/References-Lists.md  (RQ1-RQ5 tables, 50 rows each)
Output: data/processed/corpus_189.csv
        results/prisma_counts.csv

The RQ tables have the columns
    Title | Author and year | DOI URL link | Area of work | Weakness or gap
and the evidence marker (A, S or M) is the first token of the last column.
"""
import csv
import re
from collections import OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "data/raw/References-Lists.md"
OUT = ROOT / "data/processed/corpus_189.csv"
PRISMA = ROOT / "results/prisma_counts.csv"

text = SRC.read_text(encoding="utf-8")
lines = text.splitlines()

records = OrderedDict()  # doi -> dict
placements = 0
section = None

for line in lines:
    m = re.match(r"^## (RQ[1-5])\b", line)
    if m:
        section = m.group(1)
        continue
    if line.startswith("## ") and not line.startswith("## RQ"):
        section = None
        continue
    if section is None or not line.startswith("| RQ"):
        continue
    cells = [c.strip() for c in line.strip().strip("|").split(" | ")]
    if len(cells) < 5:
        raise SystemExit(f"Unexpected row layout: {line[:80]}")
    title, author_year, link, area, gap = cells[:5]
    doi = re.search(r"https://doi\.org/(\S+?)\]", link)
    if not doi:
        raise SystemExit(f"No DOI in row: {line[:80]}")
    doi = doi.group(1).lower()
    title = re.sub(r"^RQ[1-5]\.\d+\s+", "", title)
    ev = re.match(r"\[([ASM])\]", gap)
    ev = ev.group(1) if ev else ""
    year = re.search(r"\((\d{4})\)\s*$", author_year)
    year = int(year.group(1)) if year else None
    placements += 1
    rec = records.setdefault(
        doi,
        dict(doi=doi, title=title, author_year=author_year, year_list=year,
             area=area, evidence=ev, rqs=[]),
    )
    rec["rqs"].append(section)
    # keep the strongest evidence level if a record is rated differently per RQ
    rank = {"A": 3, "S": 2, "M": 1, "": 0}
    if rank[ev] > rank[rec["evidence"]]:
        rec["evidence"] = ev

with OUT.open("w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["doi", "title", "author_year", "year_list", "evidence",
                "rq_list", "n_rq", "RQ1", "RQ2", "RQ3", "RQ4", "RQ5", "area"])
    for r in records.values():
        flags = [1 if f"RQ{i}" in r["rqs"] else 0 for i in range(1, 6)]
        w.writerow([r["doi"], r["title"], r["author_year"], r["year_list"],
                    r["evidence"], ";".join(r["rqs"]), len(r["rqs"]), *flags,
                    r["area"]])

# PRISMA table copied from the list (as reported by the search log)
rows = []
grab = False
for line in lines:
    if line.startswith("## PRISMA"):
        grab = True
        continue
    if grab and line.startswith("## "):
        break
    if grab and line.startswith("| RQ"):
        rows.append([c.strip() for c in line.strip("|").split("|")])
with PRISMA.open("w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["rq", "identified", "duplicates_removed", "screened",
                "excluded_or_not_selected", "included"])
    w.writerows(rows)

print(f"placements: {placements}")
print(f"unique DOIs: {len(records)}")
print(f"repeat placements: {placements - len(records)}")
