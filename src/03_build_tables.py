"""Step 3. Merge the parsed corpus with the OpenAlex snapshot and count.

Input : data/processed/corpus_189.csv, data/external/openalex_189.json
Output: data/processed/corpus_enriched.csv
        results/*.csv, results/numbers.json

Counting rules (also stated in the manuscript):
  * unit of analysis = unique DOI (189 records), not placement (250);
  * year = year of the review list (earliest registered date); OpenAlex year is
    kept for comparison;
  * country = affiliation country of any author, a record counts once per country
    (whole counting); records without affiliation data are reported separately;
  * keyword = OpenAlex keyword (algorithmic, lower case), counted once per record;
  * author = OpenAlex author name, counted once per record.
"""
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
corpus = list(csv.DictReader((ROOT / "data/processed/corpus_189.csv").open(encoding="utf-8")))
snap = json.loads((ROOT / "data/external/openalex_189.json").read_text(encoding="utf-8"))
oa = {w["doi"].replace("https://doi.org/", "").lower(): w for w in snap["works"]}

COUNTRY = {
    "AT": "Austria", "AU": "Australia", "BE": "Belgium", "BR": "Brazil", "CA": "Canada",
    "CH": "Switzerland", "CN": "China", "CY": "Cyprus", "CZ": "Czechia", "DE": "Germany",
    "DK": "Denmark", "EE": "Estonia", "ES": "Spain", "FI": "Finland", "FR": "France",
    "GB": "United Kingdom", "GR": "Greece", "HK": "Hong Kong", "HU": "Hungary",
    "IE": "Ireland", "IL": "Israel", "IN": "India", "IT": "Italy", "JP": "Japan",
    "KR": "South Korea", "LU": "Luxembourg", "NL": "Netherlands", "NO": "Norway",
    "PL": "Poland", "PT": "Portugal", "RO": "Romania", "SE": "Sweden", "SG": "Singapore",
    "SI": "Slovenia", "TR": "Turkey", "US": "United States", "ZA": "South Africa",
    "SA": "Saudi Arabia", "AE": "United Arab Emirates", "LT": "Lithuania", "LV": "Latvia",
    "HR": "Croatia", "BG": "Bulgaria", "SK": "Slovakia", "EG": "Egypt", "PK": "Pakistan",
}

enriched = []
for r in corpus:
    w = oa[r["doi"]]
    countries = sorted({c for a in w["authorships"] for c in (a.get("countries") or [])})
    authors = []
    for a in w["authorships"]:
        n = (a.get("author") or {}).get("display_name")
        if n and n not in authors:
            authors.append(n)
    kws = sorted({k["display_name"].lower() for k in (w.get("keywords") or [])})
    topic = (w.get("primary_topic") or {}).get("display_name", "")
    field = ((w.get("primary_topic") or {}).get("field") or {}).get("display_name", "")
    src = ((w.get("primary_location") or {}).get("source") or {}).get("display_name", "")
    r.update(
        year=int(r["year_list"]) if r["year_list"] else w["publication_year"],
        year_openalex=w["publication_year"],
        type=w.get("type", ""),
        venue=src,
        n_authors=len(authors),
        authors="; ".join(authors),
        countries=";".join(countries),
        keywords=";".join(kws),
        primary_topic=topic,
        primary_field=field,
        cited_by=w.get("cited_by_count", 0),
    )
    enriched.append(r)

cols = list(enriched[0].keys())
with (ROOT / "data/processed/corpus_enriched.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=cols)
    w.writeheader()
    w.writerows(enriched)


def write(name, header, rows):
    with (ROOT / "results" / name).open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)


RQS = ["RQ1", "RQ2", "RQ3", "RQ4", "RQ5"]
years = sorted({r["year"] for r in enriched})

# 1. records per year, by RQ membership (a record counts once in each RQ it serves)
ybr = {y: {q: 0 for q in RQS} for y in years}
for r in enriched:
    for q in RQS:
        if r[q] == "1":
            ybr[r["year"]][q] += 1
write("year_by_rq.csv", ["year", *RQS, "unique_records"],
      [[y, *[ybr[y][q] for q in RQS], sum(1 for r in enriched if r["year"] == y)] for y in years])

# 2. evidence level by RQ
ebr = {q: Counter() for q in RQS}
for r in enriched:
    for q in RQS:
        if r[q] == "1":
            ebr[q][r["evidence"]] += 1
write("evidence_by_rq.csv", ["rq", "A", "S", "M", "total"],
      [[q, ebr[q]["A"], ebr[q]["S"], ebr[q]["M"], sum(ebr[q].values())] for q in RQS])

# 3. keywords
kw = Counter(k for r in enriched for k in r["keywords"].split(";") if k)
write("keywords_top.csv", ["keyword", "records"], kw.most_common(40))

# 4. countries
cc = Counter(c for r in enriched for c in r["countries"].split(";") if c)
write("countries.csv", ["iso", "country", "records"],
      [[c, COUNTRY.get(c, c), n] for c, n in cc.most_common()])
n_country = sum(1 for r in enriched if r["countries"])

# 5. authors
au = Counter(a for r in enriched for a in r["authors"].split("; ") if a)
write("authors_top.csv", ["author", "records"], au.most_common(30))

# 6. venues
ven = Counter(r["venue"] for r in enriched if r["venue"])
write("venues_top.csv", ["venue", "records"], ven.most_common(30))

# 7. primary field / document type
fld = Counter(r["primary_field"] for r in enriched if r["primary_field"])
write("primary_field.csv", ["field", "records"], fld.most_common())
typ = Counter(r["type"] for r in enriched)
write("document_type.csv", ["type", "records"], typ.most_common())

# 8. year consistency between list and OpenAlex
diff = sum(1 for r in enriched if r["year"] != r["year_openalex"])

numbers = dict(
    retrieved=snap["retrieved"],
    n_unique=len(enriched),
    n_placements=sum(int(r["n_rq"]) for r in enriched),
    year_counts={y: sum(1 for r in enriched if r["year"] == y) for y in years},
    n_with_country=n_country,
    n_countries=len(cc),
    n_with_keywords=sum(1 for r in enriched if r["keywords"]),
    n_distinct_keywords=len(kw),
    n_distinct_authors=len(au),
    n_distinct_venues=len(ven),
    n_year_differs_openalex=diff,
    evidence_total=dict(Counter(r["evidence"] for r in enriched)),
    top_countries=cc.most_common(8),
    top_keywords=kw.most_common(10),
    top_authors=au.most_common(5),
    top_venues=ven.most_common(5),
    multi_rq=dict(Counter(int(r["n_rq"]) for r in enriched)),
)
(ROOT / "results/numbers.json").write_text(
    json.dumps(numbers, indent=1, ensure_ascii=False), encoding="utf-8")
print(json.dumps(numbers, indent=1, ensure_ascii=False))
