"""Step 16. Abstracts for the metadata-only (M) placements (evidence upgrade, Package 2).

74 of the 250 placements (60 distinct DOIs) were assessed on title and bibliographic
metadata only. This script retrieves an abstract for each DOI so that two coders can
decide independently whether the placement can be upgraded to A (abstract assessed).

Sources, in order: OpenAlex (abstract_inverted_index), Crossref (abstract field),
Semantic Scholar Graph API (abstract). The first non-empty abstract is kept; the
source and retrieval date are recorded. DOIs that no API covers were looked up by
hand on the publisher page; those abstracts are stored verbatim in
data/external/metadata_only_abstracts_manual.json and merged here (source =
"publisher_page"). A DOI still without an abstract keeps source = "none" and stays M.

Output: data/external/metadata_only_abstracts.json   one record per DOI (snapshot)
        results/evidence/upgrade/abstract_retrieval.csv  DOI, source, length
Network: OpenAlex, Crossref, Semantic Scholar. The snapshot written on the first
run is the one the coders use; rerunning overwrites it.
"""
import csv
import json
import re
import ssl
import time
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

import certifi

ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "data/external/metadata_only_abstracts.json"
OUT_DIR = ROOT / "results/evidence/upgrade"
CTX = ssl.create_default_context(cafile=certifi.where())
UA = {"User-Agent": "slr-dataspace/0.1 (research replication script)"}


def get(url):
    req = urllib.request.Request(url, headers=UA)
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=30) as r:
            return json.loads(r.read().decode("utf-8"))
    except Exception:
        return None


def clean(text):
    text = re.sub(r"<[^>]+>", " ", text or "")
    text = re.sub(r"^\s*(abstract|summary)[\s:.]*", "", text, flags=re.I)
    return re.sub(r"\s+", " ", text).strip().lstrip(":;.,- ").strip()


def openalex(doi):
    w = get("https://api.openalex.org/works/https://doi.org/" + urllib.parse.quote(doi))
    ii = (w or {}).get("abstract_inverted_index")
    if not ii:
        return ""
    pos = {p: word for word, ps in ii.items() for p in ps}
    return " ".join(pos[i] for i in sorted(pos))


def crossref(doi):
    m = (get("https://api.crossref.org/works/" + urllib.parse.quote(doi)) or {}).get("message", {})
    return m.get("abstract", "")


def semantic_scholar(doi):
    w = get("https://api.semanticscholar.org/graph/v1/paper/DOI:" + urllib.parse.quote(doi)
            + "?fields=abstract")
    return (w or {}).get("abstract") or ""


placements = [r for r in csv.DictReader((ROOT / "results/audit/placements.csv").open(encoding="utf-8"))
              if r["evidence_placement"] == "M"]
dois = sorted({r["doi"].strip().lower() for r in placements})
records = {}
for doi in dois:
    abstract, source = "", "none"
    for name, fn in (("openalex", openalex), ("crossref", crossref), ("semantic_scholar", semantic_scholar)):
        text = clean(fn(doi))
        time.sleep(0.4)
        if len(text) >= 200:  # shorter strings are usually a stub or a copyright line
            abstract, source = text, name
            break
    records[doi] = {"doi": doi, "source": source, "abstract": abstract}
    print(f"{source:<17} {len(abstract):>5}  {doi}")

# abstracts copied by hand from publisher pages for DOIs that no API covers
manual = json.loads((ROOT / "data/external/metadata_only_abstracts_manual.json").read_text(encoding="utf-8"))
for doi, text in manual["records"].items():
    if doi in records and not records[doi]["abstract"]:
        records[doi] = {"doi": doi, "source": "publisher_page", "abstract": text}

OUT_JSON.write_text(json.dumps({"retrieved": date.today().isoformat(), "n": len(records),
                                "records": records}, ensure_ascii=False, indent=1), encoding="utf-8")
OUT_DIR.mkdir(parents=True, exist_ok=True)
with (OUT_DIR / "abstract_retrieval.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["doi", "source", "abstract_chars"])
    for d, r in records.items():
        w.writerow([d, r["source"], len(r["abstract"])])
found = sum(1 for r in records.values() if r["abstract"])
print(f"{found} of {len(records)} DOIs have an abstract")
