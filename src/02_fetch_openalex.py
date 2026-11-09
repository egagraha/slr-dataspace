"""Step 2. Download bibliographic metadata for the 189 DOIs from OpenAlex.

Input : data/processed/corpus_189.csv
Output: data/external/openalex_189.json   (raw snapshot, with retrieval date)

OpenAlex is a living index; the snapshot is stored so that the figures can be
rebuilt without network access. Keywords and topics in OpenAlex are assigned
algorithmically and are not author keywords.
"""
import csv
import datetime as dt
import json
import time
import urllib.parse
import ssl
import urllib.request

import certifi
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "data/processed/corpus_189.csv"
OUT = ROOT / "data/external/openalex_189.json"

FIELDS = ("id,doi,title,publication_year,publication_date,type,authorships,"
          "keywords,primary_topic,topics,primary_location,cited_by_count")
BATCH = 50
CTX = ssl.create_default_context(cafile=certifi.where())

dois = [r["doi"] for r in csv.DictReader(CORPUS.open(encoding="utf-8"))]
works = []
for i in range(0, len(dois), BATCH):
    chunk = dois[i:i + BATCH]
    flt = "doi:" + "|".join("https://doi.org/" + d for d in chunk)
    q = urllib.parse.urlencode({"filter": flt, "per-page": BATCH, "select": FIELDS},
                               safe=":|/")
    url = "https://api.openalex.org/works?" + q
    with urllib.request.urlopen(url, timeout=60, context=CTX) as resp:
        data = json.load(resp)
    works.extend(data["results"])
    print(f"batch {i // BATCH + 1}: {len(data['results'])} of {len(chunk)}")
    time.sleep(0.5)

found = {w["doi"].replace("https://doi.org/", "").lower() for w in works}
missing = [d for d in dois if d not in found]
snapshot = dict(
    retrieved=dt.date.today().isoformat(),
    source="https://api.openalex.org/works",
    n_requested=len(dois),
    n_found=len(works),
    missing=missing,
    works=works,
)
OUT.write_text(json.dumps(snapshot, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"found {len(works)} of {len(dois)}; missing: {missing}")
