"""Step 8. Coverage check against ScienceDirect exports (Protocol A3).

Input : data/external/coverage/sciencedirect_<QUERY>_<DATE>*.ris  (RIS exports, unchanged)
        data/processed/corpus_189.csv
Output: results/audit/coverage_candidates.csv  one row per distinct record (DOI or title)
        results/audit/coverage_summary.csv     counts per query and, once screened, coverage

Screening columns (relevant, reason, screener) in coverage_candidates.csv are
kept when the script is run again, so it can be rerun after screening.
See protocol/coverage_check.md for the procedure.
"""
import csv
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IN_DIR = ROOT / "data/external/coverage"
OUT = ROOT / "results/audit"
CAND = OUT / "coverage_candidates.csv"
SUMMARY = OUT / "coverage_summary.csv"
WINDOW = ("2021-11", "2026-11")          # inclusive, YYYY-MM


def norm_doi(s):
    s = (s or "").strip().lower()
    s = re.sub(r"^(https?://(dx\.)?doi\.org/|doi:)", "", s)
    return s


def norm_title(s):
    return re.sub(r"[^a-z0-9]+", " ", (s or "").lower()).strip()


def read_ris(path):
    recs, cur = [], defaultdict(list)
    for line in path.read_text(encoding="utf-8-sig", errors="replace").splitlines():
        m = re.match(r"^([A-Z][A-Z0-9])  - ?(.*)$", line)
        if not m:
            continue
        tag, val = m.group(1), m.group(2).strip()
        if tag == "ER":
            recs.append(cur)
            cur = defaultdict(list)
        else:
            cur[tag].append(val)
    return recs


def year_month(rec):
    for tag in ("DA", "Y1", "PY"):
        for v in rec.get(tag, []):
            m = re.match(r"(\d{4})(?:[/-](\d{1,2}))?", v)
            if m:
                return f"{m.group(1)}-{int(m.group(2) or 0):02d}"
    return ""


def in_window(ym):
    if not ym:
        return True                      # keep undated records; flagged below
    y, m = ym.split("-")
    if m == "00":                        # year only: keep if the year overlaps the window
        return WINDOW[0][:4] <= y <= WINDOW[1][:4]
    return WINDOW[0] <= ym <= WINDOW[1]


files = sorted(IN_DIR.glob("sciencedirect_*.ris"))
if not files:
    raise SystemExit(f"No RIS files in {IN_DIR}. See protocol/coverage_check.md, step 2.")

corpus = {r["doi"].lower() for r in csv.DictReader((ROOT / "data/processed/corpus_189.csv").open(encoding="utf-8"))}
corpus_titles = {norm_title(r["title"]): r["doi"] for r in csv.DictReader((ROOT / "data/processed/corpus_189.csv").open(encoding="utf-8"))}

# keep screening already entered
previous = {}
if CAND.exists():
    for r in csv.DictReader(CAND.open(encoding="utf-8")):
        previous[r["record_key"]] = r

records, raw_per_query = {}, defaultdict(int)
for f in files:
    query = f.name.split("_")[1]
    for rec in read_ris(f):
        raw_per_query[query] += 1
        doi = norm_doi((rec.get("DO") or [""])[0])
        title = (rec.get("TI") or rec.get("T1") or [""])[0]
        key = doi or "title:" + norm_title(title)
        ym = year_month(rec)
        r = records.setdefault(key, dict(record_key=key, doi=doi, title=title, year_month=ym,
                                         journal=(rec.get("JO") or rec.get("T2") or [""])[0],
                                         queries=set()))
        r["queries"].add(query)

rows = []
for key, r in records.items():
    if not in_window(r["year_month"]):
        continue
    in_corpus = int(bool(r["doi"]) and r["doi"] in corpus)
    title_match = "" if in_corpus or r["doi"] else corpus_titles.get(norm_title(r["title"]), "")
    prev = previous.get(key, {})
    rows.append(dict(record_key=key, doi=r["doi"], title=r["title"], year_month=r["year_month"],
                     journal=r["journal"], queries=";".join(sorted(r["queries"])),
                     in_corpus=in_corpus, title_only_match=title_match,
                     relevant=prev.get("relevant", "1" if in_corpus else ""),
                     reason=prev.get("reason", "in corpus" if in_corpus else ""),
                     screener=prev.get("screener", "")))
rows.sort(key=lambda r: (-int(r["in_corpus"]), r["title"].lower()))
cols = ["record_key", "doi", "title", "year_month", "journal", "queries", "in_corpus",
        "title_only_match", "relevant", "reason", "screener"]
with CAND.open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=cols)
    w.writeheader()
    w.writerows(rows)


def summarise(subset):
    screened = [r for r in subset if r["relevant"] in ("0", "1")]
    relevant = [r for r in screened if r["relevant"] == "1"]
    found = sum(1 for r in relevant if r["in_corpus"] == 1)
    done = len(screened) == len(subset)
    return dict(records_in_window=len(subset), in_corpus=sum(r["in_corpus"] for r in subset),
                screened=len(screened), relevant=len(relevant),
                relevant_in_corpus=found,
                coverage=f"{found / len(relevant):.3f}" if done and relevant else "")


summary = []
for q in sorted(raw_per_query):
    sub = [r for r in rows if q in r["queries"].split(";")]
    summary.append(dict(query=q, exported_records=raw_per_query[q], **summarise(sub)))
summary.append(dict(query="all (distinct)", exported_records=len(records), **summarise(rows)))
with SUMMARY.open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(summary[0]))
    w.writeheader()
    w.writerows(summary)

for s in summary:
    print(s)
undated = sum(1 for r in rows if not r["year_month"])
if undated:
    print(f"note: {undated} records without a date were kept; check them by hand")
print("coverage is filled in once every record with in_corpus = 0 has relevant = 0 or 1")
