"""Step 15. Sensitivity of the tension support to the evidence rule (Protocol B, step 5).

Input : results/evidence/double_coding/coding_Ega.csv, coding_Alexis.csv, disagreements.csv
        (agreed labels for the rows on which the coders differed)
        data/processed/corpus_enriched.csv (publication year, OpenAlex primary field)
Output: results/evidence/sensitivity_tensions.csv   one row per setting x tension
        results/evidence/final_tension_codes.csv    the 50 agreed codes used here

The final code of a row is the shared code when both coders agree and the agreed code
from disagreements.csv otherwise. Settings:

  S1  all 50 coded claim-source pairs (descriptive mapping)
  S2  drop sources the review knows by metadata only (evidence level M)
  S3  only rows whose agreed claim type is `finding` and whose supporting passage at
      least one coder located beyond the abstract. This is a proxy: no source in the
      review was quality-appraised, so the guideline's S3 (fully appraised full-text
      empirical sources) cannot be run.
  S4a S1 without publications from 2026
  S4b S1 without the most represented OpenAlex primary field

Support is counted in distinct sources, not rows, because one source can back several
sentences. Rows marked `counter` (the source judges the cost or effect acceptable) are
counted separately and do not count as support. The rule, fixed before this script was
run and after the coding was finished: robust = 3 or more supporting sources,
weakened = 1 or 2, not supported = 0.
Counts describe the coded sample, not how often the tensions occur in operating data spaces.
"""
import csv
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DC = ROOT / "results/evidence/double_coding"
OUT = ROOT / "results/evidence"
TENSIONS = ("T1", "T2", "T3")


def rows(name):
    return {(r["claim_id"], r["cite_key"]): r
            for r in csv.DictReader((DC / name).open(encoding="utf-8"))}


ega, alexis, dis = rows("coding_Ega.csv"), rows("coding_Alexis.csv"), rows("disagreements.csv")
if set(ega) != set(alexis) or not set(dis) <= set(ega):
    raise SystemExit("coding files and disagreements.csv do not match")
corpus = {r["doi"].strip().lower(): r
          for r in csv.DictReader((ROOT / "data/processed/corpus_enriched.csv").open(encoding="utf-8"))}

final = []
for key, e in sorted(ega.items()):
    a = alexis[key]
    if key in dis:
        d = dis[key]
        tension, ctype, counter = d["agreed_tension"], d["agreed_claim_type"], d["agreed_counter"]
        if not tension:
            raise SystemExit(f"no agreed tension for {key}")
    else:
        tension, ctype, counter = e["tension"], e["claim_type"], e["counter"]
    c = corpus.get(e["doi"].strip().lower(), {})
    year = c.get("year") or (re.search(r"(19|20)\d\d", e["cite_key"]) or [""])[0]
    beyond_abstract = any(p.strip() and p.strip().lower() != "abstract"
                          for p in (e["page"], a["page"]))
    final.append(dict(claim_id=key[0], cite_key=key[1], doi=e["doi"], rq=e["rq"],
                      evidence_level=e["evidence_level"], claim_type=ctype.strip(),
                      tension=tension.strip(), counter=counter.strip(), year=str(year),
                      primary_field=c.get("primary_field", "") or "not in corpus",
                      passage_beyond_abstract=int(beyond_abstract)))

top_field = Counter(r["primary_field"] for r in final if r["primary_field"] != "not in corpus").most_common(1)[0][0]
settings = {
    "S1 all coded pairs": lambda r: True,
    "S2 without metadata-only sources": lambda r: r["evidence_level"] != "M",
    "S3 proxy: findings located beyond the abstract": lambda r: r["claim_type"] == "finding" and r["passage_beyond_abstract"],
    "S4a without 2026 publications": lambda r: r["year"] != "2026",
    f"S4b without {top_field}": lambda r: r["primary_field"] != top_field,
}

out = []
for name, keep in settings.items():
    sub = [r for r in final if keep(r)]
    for t in TENSIONS:
        hits = [r for r in sub if r["tension"] == t]
        support = sorted({r["cite_key"] for r in hits if not r["counter"]})
        counter = sorted({r["cite_key"] for r in hits if r["counter"]})
        n = len(support)
        out.append(dict(setting=name, rows_in_setting=len(sub), tension=t, rows=len(hits),
                        supporting_sources=n, counter_sources=len(counter),
                        status="robust" if n >= 3 else "weakened" if n else "not supported",
                        sources="; ".join(support), counter_keys="; ".join(counter)))

with (OUT / "final_tension_codes.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(final[0]))
    w.writeheader()
    w.writerows(final)
with (OUT / "sensitivity_tensions.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0]))
    w.writeheader()
    w.writerows(out)
for r in out:
    print(f'{r["setting"]:<48} {r["tension"]} rows={r["rows"]:>2} support={r["supporting_sources"]:>2} '
          f'counter={r["counter_sources"]} {r["status"]}')
