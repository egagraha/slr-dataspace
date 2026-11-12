"""Step 17. Blank coding files for the metadata-only upgrade (Package 2).

One row per M placement (74). Each row gives the placement as listed (research
question, title, area of work, the review team's gap assessment) and the abstract
from step 16. Two coders fill in the same blank file independently; the procedure is
in results/evidence/upgrade/README_upgrade.md.

Rows are in a seeded random order (the same for both coders) so that the coders do
not work through one research question at a time.

Input : results/audit/placements.csv, data/raw/References-Lists.md,
        data/external/metadata_only_abstracts.json
Output: results/evidence/upgrade/coding_Ega.csv, coding_Alexis.csv (identical, blank)
Refuses to overwrite a coding file that already has a filled-in decision.
"""
import csv
import json
import random
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/evidence/upgrade"
CODERS = ("Ega", "Alexis")
FILL = ["relevant_to_rq", "gap_assessment", "revised_gap_text", "note"]

placements = [r for r in csv.DictReader((ROOT / "results/audit/placements.csv").open(encoding="utf-8"))
              if r["evidence_placement"] == "M"]
gap = {}
for line in (ROOT / "data/raw/References-Lists.md").read_text(encoding="utf-8").splitlines():
    m = re.match(r"^\| (RQ\d\.\d\d) .*\| \[M\] (.*?) \|\s*$", line)
    if m:
        gap[m.group(1)] = m.group(2).strip()
missing = [p["placement_id"] for p in placements if p["placement_id"] not in gap]
if missing:
    raise SystemExit(f"no [M] gap text found for {missing}")
abstracts = json.loads((ROOT / "data/external/metadata_only_abstracts.json").read_text(encoding="utf-8"))["records"]

rows = []
for p in placements:
    a = abstracts.get(p["doi"].strip().lower(), {})
    rows.append(dict(placement_id=p["placement_id"], rq=p["rq"], doi=p["doi"], title=p["title"],
                     author_year=p["author_year"], area=p["area"], gap_text=gap[p["placement_id"]],
                     abstract_source=a.get("source", "none"),
                     abstract=a.get("abstract") or "NO ABSTRACT FOUND - leave relevant_to_rq empty; the placement stays M",
                     **{f: "" for f in FILL}))
random.Random(20261112).shuffle(rows)

OUT.mkdir(parents=True, exist_ok=True)
for name in CODERS:
    path = OUT / f"coding_{name}.csv"
    if path.exists() and any(r["relevant_to_rq"].strip()
                             for r in csv.DictReader(path.open(encoding="utf-8"))):
        raise SystemExit(f"{path.name} already has decisions; not overwritten")
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
print(f"{len(rows)} rows written for {', '.join(CODERS)}; "
      f"{sum(r['abstract_source'] == 'none' for r in rows)} without an abstract")
