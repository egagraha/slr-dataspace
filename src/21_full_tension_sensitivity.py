"""Step 21. Tension support over the full claim ledger (Package 3, Protocol B step 5).

Same settings and the same rule as step 15, applied to every coded claim-source row
instead of the 50-pair sample:

  final codes = sample codes carried over by step 19 (carried_over.csv)
              + full-round codes: the shared code where both coders agree, else the
                agreed code from full_coding/disagreements.csv
  evidence level = the current level in results/evidence/source_claims.csv

  S1  all coded pairs
  S2  without metadata-only sources (level M)
  S3  proxy: agreed claim type `finding` with a supporting passage located beyond the
      abstract by at least one coder (no source was quality-appraised)
  S4a S1 without publications from 2026
  S4b S1 without the most represented OpenAlex primary field

Support is counted in distinct sources; `counter` rows are counted separately and do
not count as support. Rule (unchanged from step 15): robust = 3 or more supporting
sources, weakened = 1 or 2, not supported = 0.

Output: results/evidence/final_tension_codes_full.csv
        results/evidence/sensitivity_tensions_full.csv
Step 15 and its sample outputs are left as they are.

Until both coders have finished and every disagreement has an agreed code, the step
prints SKIPPED and changes nothing, so that run_all.sh keeps working during coding.
"""
import csv
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EV = ROOT / "results/evidence"
FC = EV / "full_coding"
TENSIONS = ("T1", "T2", "T3")
key = lambda r: (r["claim_id"], r["cite_key"])


def read(path):
    return list(csv.DictReader(path.open(encoding="utf-8")))


def skip(why):
    print(f"step 21 SKIPPED: {why}")
    sys.exit(0)


ega, alexis = ({key(r): r for r in read(FC / f"coding_{n}.csv")} for n in ("Ega", "Alexis"))
if not any(r["tension"].strip() for r in ega.values()) or not any(r["tension"].strip() for r in alexis.values()):
    skip("the full-ledger coding files are not filled in yet")
if not (FC / "disagreements.csv").exists():
    skip("run src/20_full_coding_agreement.py first")
dis = {key(r): r for r in read(FC / "disagreements.csv")}
if any(not d["agreed_tension"].strip() for d in dis.values()):
    skip("disagreements.csv still has rows without agreed_tension")
if set(ega) != set(alexis) or not set(dis) <= set(ega):
    raise SystemExit("coding files and disagreements.csv do not match")

ledger = {key(r): r for r in read(EV / "source_claims.csv")}
corpus = {r["doi"].strip().lower(): r for r in read(ROOT / "data/processed/corpus_enriched.csv")}
sample = {key(r): r for r in read(EV / "final_tension_codes.csv")}
carried = [key(r) for r in read(FC / "carried_over.csv") if r["decision"] == "carried over"]
overlap = set(carried) & set(ega)
if overlap:
    raise SystemExit(f"rows both carried over and coded again: {sorted(overlap)[:5]}")


def record(k, ctype, tension, counter, beyond, source):
    l = ledger[k]
    c = corpus.get(l["doi"].strip().lower(), {})
    year = c.get("year") or (re.search(r"(19|20)\d\d", k[1]) or [""])[0]
    return dict(claim_id=k[0], cite_key=k[1], doi=l["doi"], rq=l["rq"], evidence_level=l["evidence_level"],
                claim_type=ctype.strip(), tension=tension.strip(), counter=counter.strip(), year=str(year),
                primary_field=c.get("primary_field", "") or "not in corpus",
                passage_beyond_abstract=int(beyond), coded_in=source)


final = []
for k in carried:
    s = sample[k]
    final.append(record(k, s["claim_type"], s["tension"], s["counter"], s["passage_beyond_abstract"] == "1",
                        "sample (carried over)"))
for k, e in sorted(ega.items()):
    a = alexis[k]
    if k in dis:
        d = dis[k]
        ctype, tension, counter = d["agreed_claim_type"], d["agreed_tension"], d["agreed_counter"]
    else:
        ctype, tension, counter = e["claim_type"], e["tension"], e["counter"]
    beyond = any(p.strip() and p.strip().lower() != "abstract" for p in (e["page"], a["page"]))
    final.append(record(k, ctype, tension, counter, beyond, "full round"))

missing = [k for k in ledger if ledger[k]["doi"] and k not in {key(r) for r in final}]
if missing:
    raise SystemExit(f"{len(missing)} ledger rows with a DOI have no code, e.g. {missing[:5]}")

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

for name, data in (("final_tension_codes_full.csv", final), ("sensitivity_tensions_full.csv", out)):
    with (EV / name).open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(data[0]))
        w.writeheader()
        w.writerows(data)
print(f"{len(final)} coded pairs ({len(carried)} carried over from the sample)")
for r in out:
    print(f'{r["setting"]:<48} {r["tension"]} rows={r["rows"]:>3} support={r["supporting_sources"]:>2} '
          f'counter={r["counter_sources"]} {r["status"]}')
