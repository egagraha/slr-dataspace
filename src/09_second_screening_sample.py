"""Step 9. Blinded double-screening sample (Protocol A4).

Two screeners judge the same sample independently against
protocol/eligibility_rules.csv. The sample mixes, per research question,
  * 8 included placements (random, from results/audit/placements.csv), and
  * 10 records that were not included: hits of two logged Crossref queries for that
    question, re-run now with the same date filter, that are not among the 189.
The original "not selected" label mixes ineligible records with relevant records
cut by the 50-record cap, so agreement is computed between the two screeners, not
against the original decisions. The share of included placements that the
screeners judge eligible is reported separately.

Output: results/audit/second_screening/screening_<name>.csv   (identical, blinded)
        private/second_screening_key.csv                        (which rows were included;
                                                                 git-ignored until both are done)
Network: Crossref and OpenAlex. Seeded, but the live indexes change, so a rerun on
another day can draw different not-included records; the files written on the
first run are the ones to use.
"""
import csv
import json
import random
import ssl
import time
import urllib.parse
import urllib.request
from pathlib import Path

import certifi

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/audit/second_screening"
KEY = ROOT / "private/second_screening_key.csv"
SCREENERS = ["Ega", "Alexis"]
SEED = 20261110
N_INCLUDED, N_OTHER, N_QUERIES = 8, 10, 2
RQS = ["RQ1", "RQ2", "RQ3", "RQ4", "RQ5"]
RQ_TEXT = {
    "RQ1": "What frameworks, standards, and regulations govern data sovereignty and compliance in cross-border data exchange?",
    "RQ2": "What security and privacy-preserving mechanisms are proposed or implemented to ensure compliant and sovereign data sharing?",
    "RQ3": "How is interoperability achieved in sovereign data spaces, and what roles do standardized data connectors and semantic frameworks play?",
    "RQ4": "What are the research gaps, limitations, and challenges in achieving secure, compliant, and interoperable cross-border data exchange?",
    "RQ5": "How do emerging technologies, such as distributed ledger technologies and federated learning, enhance data sovereignty and secure data exchange in data spaces?",
}
CTX = ssl.create_default_context(cafile=certifi.where())
UA = {"User-Agent": "slr-dataspace-screening-sample/1.0"}


def get(url):
    for attempt in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), context=CTX, timeout=60) as r:
                return json.load(r)
        except Exception:
            if attempt == 2:
                raise
            time.sleep(3)


def crossref(kind, q, rows):
    param = {"crossref query.bibliographic": "query.bibliographic", "crossref query": "query"}[kind]
    qs = urllib.parse.urlencode({param: q, "rows": rows,
                                 "filter": "from-pub-date:2021-11-01,until-pub-date:2026-11-30",
                                 "select": "DOI,title,type"})
    return get("https://api.crossref.org/works?" + qs)["message"]["items"]


def openalex(doi):
    try:
        w = get("https://api.openalex.org/works/doi:" + urllib.parse.quote(doi))
    except Exception:
        return {}
    inv = w.get("abstract_inverted_index") or {}
    words = sorted((p, t) for t, ps in inv.items() for p in ps)
    return dict(title=w.get("title") or "", year=w.get("publication_year") or "",
                type=w.get("type") or "", abstract=" ".join(t for _, t in words),
                venue=((w.get("primary_location") or {}).get("source") or {}).get("display_name") or "")


if OUT.exists() and any(OUT.glob("screening_*.csv")):
    raise SystemExit(f"{OUT} already holds screening files; delete them first to draw a new sample.")

rng = random.Random(SEED)
placements = list(csv.DictReader((ROOT / "results/audit/placements.csv").open(encoding="utf-8")))
search = list(csv.DictReader((ROOT / "results/audit/search_log.csv").open(encoding="utf-8")))
corpus = {p["doi"] for p in placements}
eligible_types = {"journal-article", "proceedings-article", "book-chapter", "posted-content",
                  "dataset", "peer-review", "proceedings", "book", "monograph", "other",
                  "component", "report", "edited-book", "reference-entry"}  # all kept: screeners decide

sample = []
for rq in RQS:
    inc = rng.sample([p for p in placements if p["rq"] == rq], N_INCLUDED)
    sample += [dict(rq=rq, doi=p["doi"], included=1, source=f"placement {p['placement_id']}") for p in inc]
    queries = [s for s in search if s["rq_coverage"] == rq and s["kind"] in ("crossref query.bibliographic", "crossref query")]
    pool, seen = [], set()
    for s in rng.sample(queries, N_QUERIES):
        for it in crossref(s["kind"], s["query_or_lookup"], int(s["retrieved"])):
            d = it["DOI"].lower()
            if d not in corpus and d not in seen and it.get("type") in eligible_types:
                seen.add(d)
                pool.append(dict(rq=rq, doi=d, included=0, source=f"re-run {s['search_id']}"))
        time.sleep(1)
    if len(pool) < N_OTHER:
        raise SystemExit(f"{rq}: only {len(pool)} not-included candidates")
    sample += rng.sample(pool, N_OTHER)

rng.shuffle(sample)
for i, r in enumerate(sample, start=1):
    r["sample_id"] = f"X{i:03d}"
    r.update(openalex(r["doi"]))
    time.sleep(0.2)

OUT.mkdir(parents=True, exist_ok=True)
cols = ["sample_id", "rq", "research_question", "doi", "title", "year", "type", "venue", "abstract",
        "decision", "rule", "note"]
for name in SCREENERS:
    with (OUT / f"screening_{name}.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for r in sample:
            w.writerow({**r, "research_question": RQ_TEXT[r["rq"]], "decision": "", "rule": "", "note": ""})
KEY.parent.mkdir(exist_ok=True)
with KEY.open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["sample_id", "rq", "doi", "included", "source"], extrasaction="ignore")
    w.writeheader()
    w.writerows(sample)
no_abs = sum(1 for r in sample if not r.get("abstract"))
print(f"{len(sample)} records ({sum(r['included'] for r in sample)} included); "
      f"{no_abs} without an OpenAlex abstract (screen from title and DOI page)")
