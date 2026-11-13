"""Step 19. Blank coding files for the full claim ledger (Package 3, Protocol B).

The 50-pair sample (steps 12-13) was coded and agreed. This step issues every other
claim-source row of results/evidence/source_claims.csv that has a DOI, so that the
whole ledger is coded by two coders with codebook v2.

Carried over from the sample: the agreed codes of every pair that is still in the
ledger under the same claim_id and whose source was not metadata-only (M) when it
was coded. Pairs coded at level M could only be coded T0 or NA; their sources are
now at level A, so they are coded again here. Rows without a DOI (laws, W3C
standards) are not coded, as in the sample.

Rows are in a seeded random order (the same for both coders).

Input : results/evidence/source_claims.csv   (rebuilt by step 11 from the manuscript)
        results/evidence/final_tension_codes.csv  (agreed sample codes, step 15)
Output: results/evidence/full_coding/coding_Ega.csv, coding_Alexis.csv   (blank, identical)
        results/evidence/full_coding/carried_over.csv  sample codes reused, and why others are not
Refuses to overwrite a coding file that already holds a decision.
"""
import csv
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/evidence/full_coding"
CODERS = ("Ega", "Alexis")
SEED = 20261113
PREFILLED = ["claim_id", "rq", "subsection", "location", "sentence", "cite_key", "doi", "doi_url",
             "evidence_level"]
FILL = ["claim_type", "tension", "counter", "page", "supporting_passage", "note"]

key = lambda r: (r["claim_id"], r["cite_key"])
ledger = [r for r in csv.DictReader((ROOT / "results/evidence/source_claims.csv").open(encoding="utf-8"))]
in_ledger = {key(r): r for r in ledger}
sample = list(csv.DictReader((ROOT / "results/evidence/final_tension_codes.csv").open(encoding="utf-8")))

carried, audit = set(), []
for s in sample:
    k = key(s)
    if k not in in_ledger:
        reason = "sentence changed in the manuscript (new claim_id); coded again"
    elif s["evidence_level"] == "M":
        reason = f"coded at level M (T0/NA only); source now {in_ledger[k]['evidence_level']}; coded again"
    else:
        reason = "carried over"
        carried.add(k)
    audit.append(dict(claim_id=s["claim_id"], cite_key=s["cite_key"], evidence_level_at_coding=s["evidence_level"],
                      tension=s["tension"], claim_type=s["claim_type"], counter=s["counter"], decision=reason))

rows = []
for r in ledger:
    if not r["doi"] or key(r) in carried:
        continue
    rows.append({**{c: r.get(c, "") for c in PREFILLED if c != "doi_url"},
                 "doi_url": "https://doi.org/" + r["doi"], **{f: "" for f in FILL}})
rows = [{c: r[c] for c in PREFILLED + FILL} for r in rows]
random.Random(SEED).shuffle(rows)

OUT.mkdir(parents=True, exist_ok=True)
for name in CODERS:
    path = OUT / f"coding_{name}.csv"
    if path.exists() and any(r["tension"].strip() for r in csv.DictReader(path.open(encoding="utf-8"))):
        raise SystemExit(f"{path.name} already has decisions; not overwritten")
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=PREFILLED + FILL)
        w.writeheader()
        w.writerows(rows)
with (OUT / "carried_over.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(audit[0]))
    w.writeheader()
    w.writerows(audit)

no_doi = sum(1 for r in ledger if not r["doi"])
print(f"ledger rows: {len(ledger)}; without DOI (not coded): {no_doi}; "
      f"sample codes carried over: {len(carried)}; rows issued to each coder: {len(rows)}")
