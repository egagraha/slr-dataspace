"""Step 14. Recount the selection from the original retrieval ledgers (Protocol A).

The ledgers were written during the November 2026 search and selection and are
stored unchanged in data/raw/retrieval_ledgers/:
  rq1.json ... rq5.json      per RQ: the queries (with the number of records each
                             returned), the screening ledger (one entry per distinct
                             DOI screened, with decision and reason) and the 50
                             included records
  crossref_responses/*.json  the Crossref responses (and DOI lookups) the queries
                             refer to; the "file" paths inside the ledgers point to
                             the original working folder, only the file name is used

Input : data/raw/retrieval_ledgers/, results/prisma_counts.csv, data/processed/corpus_189.csv
Output: results/audit/retrieval_recount.csv   one row per RQ plus one row over all RQs
Run before 07_audit_tables.py, which reads the output. Exits with an error if a
count does not reconcile.
"""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LED = ROOT / "data/raw/retrieval_ledgers"
RAW = LED / "crossref_responses"
OUT = ROOT / "results/audit/retrieval_recount.csv"


def dois_in_response(path):
    """DOIs in one stored response: a Crossref works list, a single work, or a list of records."""
    j = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(j, dict) and "message" in j:
        msg = j["message"]
        items = msg.get("items", [msg]) if isinstance(msg, dict) else []
    elif isinstance(j, dict):
        items = j.get("items", [j])
    else:
        items = j
    return {(it.get("DOI") or it.get("doi")).lower()
            for it in items if isinstance(it, dict) and (it.get("DOI") or it.get("doi"))}


prisma = {r["rq"]: r for r in csv.DictReader((ROOT / "results/prisma_counts.csv").open(encoding="utf-8"))}
corpus = {r["doi"].lower() for r in csv.DictReader((ROOT / "data/processed/corpus_189.csv").open(encoding="utf-8"))}

rows, all_screened, all_included, errors = [], set(), set(), []
for i in range(1, 6):
    rq = f"RQ{i}"
    d = json.loads((LED / f"rq{i}.json").read_text(encoding="utf-8"))
    identified = sum(q["returned"] for q in d["queries"])
    screened = {s["doi"].lower() for s in d["screening"]}
    included = {r["doi"].lower() for r in d["records"]}
    in_responses = set()
    for q in d["queries"]:
        in_responses |= dois_in_response(RAW / Path(q["file"]).name)
    not_in_responses = screened - in_responses
    rows.append(dict(rq=rq, queries_and_lookups=len(d["queries"]), identified=identified,
                     screened_distinct=len(screened), included=len(included),
                     screened_not_in_responses=len(not_in_responses)))
    p = prisma[rq]
    for name, ours, theirs in (("identified", identified, p["identified"]),
                               ("screened", len(screened), p["screened"]),
                               ("included", len(included), p["included"])):
        if ours != int(theirs):
            errors.append(f"{rq} {name}: ledgers {ours}, prisma_counts.csv {theirs}")
    if not_in_responses:
        errors.append(f"{rq}: {len(not_in_responses)} screened DOIs not found in the stored responses")
    all_screened |= screened
    all_included |= included

rows.append(dict(rq="all RQs (each DOI once)", queries_and_lookups="", identified=sum(r["identified"] for r in rows),
                 screened_distinct=len(all_screened), included=len(all_included), screened_not_in_responses=""))
if all_included != corpus:
    errors.append(f"included DOIs differ from corpus_189.csv: {len(all_included ^ corpus)} DOIs")

OUT.parent.mkdir(parents=True, exist_ok=True)
with OUT.open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader()
    w.writerows(rows)
for r in rows:
    print(r)
if errors:
    raise SystemExit("retrieval recount does not reconcile:\n  " + "\n  ".join(errors))
