"""Step 7. Audit tables for the selection (Protocol A, light version).

Rebuilds machine-readable versions of the search log and of the 250 placements
from data/raw/References-Lists.md and checks that every count reported in the
manuscript reconciles. Nothing here changes the corpus.

Input : data/raw/References-Lists.md, results/prisma_counts.csv,
        results/evidence_by_rq.csv, data/processed/corpus_189.csv
Output: results/audit/search_log.csv            one row per search or lookup
        results/audit/placements.csv            one row per RQ placement (publication-RQ link)
        results/audit/evidence_by_rq_placement.csv
        results/audit/audit_checks.csv          every check with expected, observed, status
The script exits with an error if a check marked "hard" fails.
"""
import csv
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "data/raw/References-Lists.md"
OUT = ROOT / "results/audit"
OUT.mkdir(parents=True, exist_ok=True)
RQS = ["RQ1", "RQ2", "RQ3", "RQ4", "RQ5"]

lines = SRC.read_text(encoding="utf-8").splitlines()


def section(title_prefix):
    """Lines of the '## ' section whose heading starts with title_prefix."""
    out, on = [], False
    for ln in lines:
        if ln.startswith("## "):
            on = ln[3:].startswith(title_prefix)
            continue
        if on:
            out.append(ln)
    return out


def table_rows(sec_lines):
    rows = []
    for ln in sec_lines:
        if ln.startswith("|") and not ln.startswith("| ---"):
            rows.append([c.strip() for c in ln.strip().strip("|").split(" | ")])
    return rows[1:]  # drop header


def norm_doi(s):
    s = (s or "").strip().lower()
    for p in ("https://doi.org/", "http://doi.org/", "doi:"):
        if s.startswith(p):
            s = s[len(p):]
    return s


# ---- 1. search log ----------------------------------------------------------
search = []
for i, (cov, what, n) in enumerate(table_rows(section("Search log")), start=1):
    rqs = [r.strip() for r in cov.split(",")]
    if what.startswith("query.bibliographic"):
        kind = "crossref query.bibliographic"
    elif what.startswith("query.title"):
        kind = "crossref query.title"
    elif what.startswith("query:"):
        kind = "crossref query"
    elif "Citation chasing" in what:
        kind = "citation chasing + DOI lookup"
    elif "Targeted DOI lookup" in what:
        kind = "targeted DOI lookup"
    elif "DOI lookup" in what:
        kind = "direct DOI lookup"
    else:
        kind = "other"
    q = re.sub(r"^(query\.bibliographic|query\.title|query)\s*[:=]\s*", "", what)
    doi = re.search(r"(10\.\S+)$", what)
    search.append(dict(search_id=f"S{i:03d}", rq_coverage=";".join(rqs), kind=kind,
                       query_or_lookup=q.strip('"'), doi=norm_doi(doi.group(1)) if doi else "",
                       retrieved=int(n), source="Crossref REST API",
                       date_filter="2021-11 to 2026-11", run="November 2026"))
with (OUT / "search_log.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(search[0]))
    w.writeheader()
    w.writerows(search)

# ---- 2. placements (publication-RQ links) -----------------------------------
register = {}
for entry, assessed, url, date in table_rows(section("Source assessment register")):
    register[entry] = dict(assessed=assessed, url=re.sub(r"^\[Source\]\((.*)\)$", r"\1", url),
                           date=date)

placements = []
for rq in RQS:
    for title, author_year, link, area, gap in (r[:5] for r in table_rows(section(rq + " "))):
        pid = re.match(r"(RQ[1-5]\.\d+)", title).group(1)
        doi = norm_doi(re.search(r"\((https://doi\.org/\S+?)\)", link).group(1))
        ev = re.match(r"\[([ASM])\]", gap)
        reg = register.get(pid, {})
        placements.append(dict(placement_id=pid, rq=rq, doi=doi,
                               evidence_placement=ev.group(1) if ev else "",
                               assessed_evidence=reg.get("assessed", ""),
                               evidence_url=reg.get("url", ""),
                               publication_date_used=reg.get("date", ""),
                               title=re.sub(r"^RQ[1-5]\.\d+\s+", "", title),
                               author_year=author_year, area=area))
first_seen = {}
for p in placements:
    first_seen.setdefault(p["doi"], p["placement_id"])
    p["publication_id"] = first_seen[p["doi"]]          # consolidated ID = first placement
    p["repeat_of_earlier_rq"] = int(first_seen[p["doi"]] != p["placement_id"])
cols = ["placement_id", "rq", "publication_id", "repeat_of_earlier_rq", "doi",
        "evidence_placement", "assessed_evidence", "publication_date_used", "evidence_url",
        "title", "author_year", "area"]
with (OUT / "placements.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
    w.writeheader()
    w.writerows(placements)

ev_pl = {rq: Counter(p["evidence_placement"] for p in placements if p["rq"] == rq) for rq in RQS}
with (OUT / "evidence_by_rq_placement.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["rq", "A", "S", "M", "total"])
    for rq in RQS:
        w.writerow([rq, ev_pl[rq]["A"], ev_pl[rq]["S"], ev_pl[rq]["M"], sum(ev_pl[rq].values())])

# ---- 3. checks ---------------------------------------------------------------
checks = []


def check(name, expected, observed, hard=True, note=""):
    ok = expected == observed
    checks.append(dict(check=name, expected=expected, observed=observed,
                       status="pass" if ok else ("FAIL" if hard else "differs"),
                       severity="hard" if hard else "soft", note=note))


prisma = {r["rq"]: {k: int(v) for k, v in r.items() if k != "rq"}
          for r in csv.DictReader((ROOT / "results/prisma_counts.csv").open(encoding="utf-8"))}
n_dois = len({p["doi"] for p in placements})
check("placements", 250, len(placements))
check("unique publications (DOI)", 189, n_dois)
check("repeat placements", 61, len(placements) - n_dois)
check("placement IDs unique", len(placements), len({p["placement_id"] for p in placements}))
for rq in RQS:
    n_rq = sum(1 for p in placements if p["rq"] == rq)
    check(f"{rq} included = 50", 50, n_rq)
    check(f"{rq} included matches PRISMA table", prisma[rq]["included"], n_rq)
    logged = sum(s["retrieved"] for s in search if rq in s["rq_coverage"].split(";"))
    check(f"{rq} identified = sum of search-log rows covering it", prisma[rq]["identified"], logged)
    check(f"{rq} screened = identified - duplicates", prisma[rq]["screened"],
          prisma[rq]["identified"] - prisma[rq]["duplicates_removed"])
    check(f"{rq} excluded or not selected = screened - included",
          prisma[rq]["excluded_or_not_selected"], prisma[rq]["screened"] - prisma[rq]["included"])
check("identified record instances, all RQs", 3507, sum(v["identified"] for v in prisma.values()))
check("screened records, all RQs", 3221, sum(v["screened"] for v in prisma.values()))
check("register entries cover every placement", 250,
      sum(1 for p in placements if p["assessed_evidence"]))
# evidence marker against the register wording
kind = {"A": ("abstract", "summary", "synopsis"),
        "S": ("section", "excerpt", "text", "discussion", "conclusion"),
        "M": ("title and bibliographic metadata",)}
mismatch = [p["placement_id"] for p in placements
            if not any(k in p["assessed_evidence"].lower() for k in kind.get(p["evidence_placement"], ()))]
check("evidence marker agrees with register wording", 0, len(mismatch), hard=False,
      note=" ".join(mismatch[:20]))
# evidence counts: per placement (marker in the list) versus results/evidence_by_rq.csv
old = {r["rq"]: r for r in csv.DictReader((ROOT / "results/evidence_by_rq.csv").open(encoding="utf-8"))}
for rq in RQS:
    for lvl in "ASM":
        check(f"{rq} evidence {lvl}: per-placement marker vs evidence_by_rq.csv",
              int(old[rq][lvl]), ev_pl[rq][lvl], hard=False,
              note="evidence_by_rq.csv uses the highest level of the publication across RQs")
tot = Counter(p["evidence_placement"] for p in placements)
check("evidence A/S/M over 250 placements (manuscript: 146/30/74)", "146/30/74",
      f"{tot['A']}/{tot['S']}/{tot['M']}", hard=False)
checks.append(dict(check="2,047 distinct retrieved DOIs", expected=2047, observed="not reproducible",
                   status="not checkable", severity="soft",
                   note="the per-query retrieval ledgers are not in the repository; the figure is taken from the list"))

with (OUT / "audit_checks.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["check", "expected", "observed", "status", "severity", "note"])
    w.writeheader()
    w.writerows(checks)

for c in checks:
    if c["status"] != "pass":
        print(f"{c['status']:>14}  {c['check']}: expected {c['expected']}, observed {c['observed']}")
print(f"{sum(c['status'] == 'pass' for c in checks)} of {len(checks)} checks pass; "
      f"{len(search)} search-log rows; {len(placements)} placements")
if any(c["status"] == "FAIL" for c in checks):
    raise SystemExit("hard check failed")
