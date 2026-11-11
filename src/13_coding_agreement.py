"""Step 13. Agreement between the two independent tension coders (Protocol B).

Input : results/evidence/double_coding/coding_Ega.csv, coding_Alexis.csv (filled in,
        following protocol/tension_codebook_v2.md)
Output: results/evidence/double_coding/agreement.csv      one row per measure
        results/evidence/double_coding/disagreements.csv  rows where tension, claim_type
                                                          or counter differ
Run only after both files are complete. The calibration rows are not used.
"""
import csv
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / "results/evidence/double_coding"
A, B = "Ega", "Alexis"
FIELDS = {"claim_type": {"finding", "proposal", "description", "review_assessment"},
          "tension": {"T1", "T2", "T3", "T0", "NA"},
          "counter": {"", "1"}}


def load(name):
    # claim_id names the manuscript sentence; a sentence citing two sources gives two rows
    rows = {(r["claim_id"], r["cite_key"]): r
            for r in csv.DictReader((DIR / f"coding_{name}.csv").open(encoding="utf-8"))}
    for f, valid in FIELDS.items():
        bad = [i for i, r in rows.items() if r[f].strip() not in valid]
        if bad:
            raise SystemExit(f"{name}: {len(bad)} rows with an invalid {f}, e.g. {bad[:5]}")
    return rows


def kappa(pairs):
    n = len(pairs)
    po = sum(a == b for a, b in pairs) / n
    ca, cb = Counter(a for a, _ in pairs), Counter(b for _, b in pairs)
    pe = sum(ca[k] * cb[k] for k in set(ca) | set(cb)) / n ** 2
    return po, (po - pe) / (1 - pe) if pe < 1 else float("nan")


ra, rb = load(A), load(B)
if set(ra) != set(rb):
    raise SystemExit("the two files do not hold the same claim_ids")
ids = sorted(ra)
val = lambda i, f: (ra[i][f].strip(), rb[i][f].strip())

out = []
def add(measure, pairs):
    po, k = kappa(pairs)
    out.append(dict(measure=measure, n=len(pairs), raw_agreement=f"{po:.3f}", cohen_kappa=f"{k:.3f}"))

add("tension (T1/T2/T3/T0/NA)", [val(i, "tension") for i in ids])
no_na = [i for i in ids if "NA" not in val(i, "tension")]
add("tension, rows with any NA dropped", [val(i, "tension") for i in no_na])
add("any tension (T1-T3) vs T0, rows with any NA dropped",
    [tuple("T" if v in ("T1", "T2", "T3") else "0" for v in val(i, "tension")) for i in no_na])
add("claim_type", [val(i, "claim_type") for i in ids])
add("counter", [val(i, "counter") for i in ids])
for name, rows in ((A, ra), (B, rb)):
    c = Counter(r["tension"].strip() for r in rows.values())
    out.append(dict(measure=f"{name}: rows coded T1/T2/T3/T0/NA", n=len(ids),
                    raw_agreement=" / ".join(str(c[t]) for t in ("T1", "T2", "T3", "T0", "NA")), cohen_kappa=""))
with (DIR / "agreement.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["measure", "n", "raw_agreement", "cohen_kappa"])
    w.writeheader()
    w.writerows(out)

with (DIR / "disagreements.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["claim_id", "rq", "cite_key", "doi", "evidence_level", "differs_in",
                f"claim_type_{A}", f"tension_{A}", f"counter_{A}", f"page_{A}", f"passage_{A}", f"note_{A}",
                f"claim_type_{B}", f"tension_{B}", f"counter_{B}", f"page_{B}", f"passage_{B}", f"note_{B}",
                "agreed_claim_type", "agreed_tension", "agreed_counter", "resolution_note"])
    for i in ids:
        diff = [f for f in FIELDS if val(i, f)[0] != val(i, f)[1]]
        if diff:
            a, b = ra[i], rb[i]
            w.writerow([i[0], a["rq"], a["cite_key"], a["doi"], a["evidence_level"], "+".join(diff),
                        a["claim_type"], a["tension"], a["counter"], a["page"], a["supporting_passage"], a["note"],
                        b["claim_type"], b["tension"], b["counter"], b["page"], b["supporting_passage"], b["note"],
                        "", "", "", ""])
for r in out:
    print(r)
