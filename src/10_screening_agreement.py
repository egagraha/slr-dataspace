"""Step 10. Agreement between the two independent screeners (Protocol A4).

Input : results/audit/second_screening/screening_Ega.csv, screening_Alexis.csv (filled in)
        private/second_screening_key.csv
Output: results/audit/second_screening/agreement.csv      one row per measure
        results/audit/second_screening/disagreements.csv  records the screeners judged differently
Run only after both files are complete; the key is read here for the secondary measure.
"""
import csv
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / "results/audit/second_screening"
A, B = "Ega", "Alexis"
VALID = {"include", "exclude", "unsure"}


def load(name):
    rows = {r["sample_id"]: r for r in csv.DictReader((DIR / f"screening_{name}.csv").open(encoding="utf-8"))}
    bad = [i for i, r in rows.items() if r["decision"].strip().lower() not in VALID]
    if bad:
        raise SystemExit(f"{name}: {len(bad)} rows without a valid decision, e.g. {bad[:5]}")
    return rows


def kappa(pairs):
    n = len(pairs)
    po = sum(a == b for a, b in pairs) / n
    ca, cb = Counter(a for a, _ in pairs), Counter(b for _, b in pairs)
    pe = sum(ca[k] * cb[k] for k in set(ca) | set(cb)) / n ** 2
    return po, (po - pe) / (1 - pe) if pe < 1 else float("nan")


ra, rb = load(A), load(B)
key = {r["sample_id"]: r for r in csv.DictReader((ROOT / "private/second_screening_key.csv").open(encoding="utf-8"))}
ids = sorted(ra)
dec = {i: (ra[i]["decision"].strip().lower(), rb[i]["decision"].strip().lower()) for i in ids}

out = []
po, k = kappa([dec[i] for i in ids])
out.append(dict(measure="three categories (include/exclude/unsure)", n=len(ids),
                raw_agreement=f"{po:.3f}", cohen_kappa=f"{k:.3f}"))
binary = [dec[i] for i in ids if "unsure" not in dec[i]]
po, k = kappa(binary)
out.append(dict(measure="include vs exclude, rows with any 'unsure' dropped", n=len(binary),
                raw_agreement=f"{po:.3f}", cohen_kappa=f"{k:.3f}"))
inc = [i for i in ids if key[i]["included"] == "1"]
for name, rows in ((A, ra), (B, rb)):
    share = sum(rows[i]["decision"].strip().lower() == "include" for i in inc) / len(inc)
    out.append(dict(measure=f"{name}: share of included placements judged 'include'", n=len(inc),
                    raw_agreement=f"{share:.3f}", cohen_kappa=""))
with (DIR / "agreement.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["measure", "n", "raw_agreement", "cohen_kappa"])
    w.writeheader()
    w.writerows(out)

with (DIR / "disagreements.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["sample_id", "rq", "doi", "title", f"decision_{A}", f"rule_{A}", f"decision_{B}",
                f"rule_{B}", "included_in_review", "resolution", "resolution_note"])
    for i in ids:
        if dec[i][0] != dec[i][1]:
            w.writerow([i, ra[i]["rq"], ra[i]["doi"], ra[i]["title"], dec[i][0], ra[i]["rule"],
                        dec[i][1], rb[i]["rule"], key[i]["included"], "", ""])
for r in out:
    print(r)
print("note: rows without an abstract are more common among records not included; report this with the result")
