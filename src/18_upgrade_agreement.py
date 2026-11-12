"""Step 18. Agreement and application of the metadata-only upgrade (Package 2).

Without arguments: compares the two independent coding files and writes
  results/evidence/upgrade/agreement.csv       raw agreement and Cohen's kappa
  results/evidence/upgrade/disagreements.csv   rows where the codes differ, and every row
                                               coded revise / not_supported (one agreed
                                               text is needed); agreed_* columns blank
It refuses to overwrite a disagreements.csv whose agreed_* columns have been filled in.

With --apply (after the agreed_* columns are filled in):
  * every placement with an abstract becomes level A in data/raw/References-Lists.md
    ([M] -> [A] in the list; register wording -> "Abstract (<source>), read by two
    coders"), with the agreed gap text where it was revised;
  * results/evidence/upgrade/upgrade_decisions.csv records the final decision per row.
A placement agreed as not relevant stays in the corpus and is flagged in
upgrade_decisions.csv, so that the corpus counts do not change.
Procedure: results/evidence/upgrade/README_upgrade.md.
"""
import csv
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / "results/evidence/upgrade"
LIST = ROOT / "data/raw/References-Lists.md"
A, B = "Ega", "Alexis"
VALID = {"relevant_to_rq": {"yes", "no", "unclear"},
         "gap_assessment": {"holds", "revise", "not_supported"}}
SOURCE_NAME = {"openalex": "OpenAlex", "crossref": "Crossref",
               "semantic_scholar": "Semantic Scholar", "publisher_page": "publisher page"}


def load(name):
    rows = {r["placement_id"]: r for r in csv.DictReader((DIR / f"coding_{name}.csv").open(encoding="utf-8"))}
    for pid, r in rows.items():
        if r["abstract_source"] == "none":
            continue
        for f, ok in VALID.items():
            if r[f].strip() not in ok:
                raise SystemExit(f"{name}: {pid} has {f} = '{r[f]}'")
        if r["gap_assessment"].strip() != "holds" and not r["revised_gap_text"].strip():
            raise SystemExit(f"{name}: {pid} is {r['gap_assessment']} but has no revised_gap_text")
    return rows


def kappa(pairs):
    n = len(pairs)
    po = sum(a == b for a, b in pairs) / n
    ca, cb = Counter(a for a, _ in pairs), Counter(b for _, b in pairs)
    pe = sum(ca[k] * cb[k] for k in set(ca) | set(cb)) / n ** 2
    return po, (po - pe) / (1 - pe) if pe < 1 else float("nan")


ra, rb = load(A), load(B)
if set(ra) != set(rb):
    raise SystemExit("the two files do not hold the same placements")
ids = sorted(pid for pid in ra if ra[pid]["abstract_source"] != "none")
v = lambda pid, f: (ra[pid][f].strip(), rb[pid][f].strip())

if "--apply" not in sys.argv:
    out = []
    for f in VALID:
        po, k = kappa([v(i, f) for i in ids])
        out.append(dict(measure=f, n=len(ids), raw_agreement=f"{po:.3f}", cohen_kappa=f"{k:.3f}"))
    for name, rows in ((A, ra), (B, rb)):
        for f in VALID:
            c = Counter(rows[i][f].strip() for i in ids)
            out.append(dict(measure=f"{name}: {f}", n=len(ids),
                            raw_agreement=" / ".join(f"{k} {c[k]}" for k in sorted(VALID[f])), cohen_kappa=""))
    with (DIR / "agreement.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["measure", "n", "raw_agreement", "cohen_kappa"])
        w.writeheader()
        w.writerows(out)
    dpath = DIR / "disagreements.csv"
    if dpath.exists() and any(r["agreed_relevant_to_rq"].strip()
                              for r in csv.DictReader(dpath.open(encoding="utf-8"))):
        raise SystemExit("disagreements.csv already has agreed values; not overwritten")
    with dpath.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["placement_id", "rq", "title", "gap_text", "differs_in",
                    f"relevant_{A}", f"gap_{A}", f"revised_{A}", f"note_{A}",
                    f"relevant_{B}", f"gap_{B}", f"revised_{B}", f"note_{B}",
                    "agreed_relevant_to_rq", "agreed_gap_assessment", "agreed_gap_text", "resolution_note"])
        n = 0
        for i in ids:
            diff = [f for f in VALID if v(i, f)[0] != v(i, f)[1]]
            needs_text = v(i, "gap_assessment") != ("holds", "holds")
            if diff or needs_text:
                a, b = ra[i], rb[i]
                w.writerow([i, a["rq"], a["title"], a["gap_text"], "+".join(diff) or "text",
                            a["relevant_to_rq"], a["gap_assessment"], a["revised_gap_text"], a["note"],
                            b["relevant_to_rq"], b["gap_assessment"], b["revised_gap_text"], b["note"],
                            "", "", "", ""])
                n += 1
    for r in out:
        print(r)
    print(f"{n} rows to resolve in disagreements.csv")
    sys.exit(0)

# ---- apply -------------------------------------------------------------------
dis = {r["placement_id"]: r for r in csv.DictReader((DIR / "disagreements.csv").open(encoding="utf-8"))}
decisions = []
for i in sorted(ra):
    a = ra[i]
    if a["abstract_source"] == "none":
        decisions.append(dict(placement_id=i, rq=a["rq"], level="M", relevant_to_rq="", gap_assessment="",
                              gap_text=a["gap_text"], source="none", note="no abstract found"))
        continue
    if i in dis:
        d = dis[i]
        rel, gap = d["agreed_relevant_to_rq"].strip(), d["agreed_gap_assessment"].strip()
        if rel not in VALID["relevant_to_rq"] or gap not in VALID["gap_assessment"]:
            raise SystemExit(f"disagreements.csv: {i} has no valid agreed values")
        text = d["agreed_gap_text"].strip() if gap != "holds" else a["gap_text"]
        if not text:
            raise SystemExit(f"disagreements.csv: {i} needs agreed_gap_text")
        note = d["resolution_note"]
    else:
        rel, gap, text, note = a["relevant_to_rq"].strip(), "holds", a["gap_text"], ""
    decisions.append(dict(placement_id=i, rq=a["rq"], level="A", relevant_to_rq=rel, gap_assessment=gap,
                          gap_text=text, source=a["abstract_source"],
                          note=("retained, judged not relevant; " if rel == "no" else "") + note))

lines = LIST.read_text(encoding="utf-8").splitlines(keepends=True)
by_id = {d["placement_id"]: d for d in decisions if d["level"] == "A"}
changed = Counter()
for n, line in enumerate(lines):
    for pid, d in by_id.items():
        old_gap = ra[pid]["gap_text"]
        if line.startswith(f"| {pid} ") and f"| [M] {old_gap} |" in line:
            lines[n] = line.replace(f"| [M] {old_gap} |", f"| [A] {d['gap_text']} |")
            changed["list"] += 1
        elif line.startswith(f"| {pid} | Title and bibliographic metadata"):
            lines[n] = re.sub(r"^(\| \S+ \| )Title and bibliographic metadata[^|]*\|",
                              lambda m: f"{m.group(1)}Abstract ({SOURCE_NAME[d['source']]}), read by two coders |",
                              line)
            changed["register"] += 1
if changed["list"] != len(by_id) or changed["register"] != len(by_id):
    raise SystemExit(f"expected {len(by_id)} list and register rows, changed {dict(changed)}; nothing written")
LIST.write_text("".join(lines), encoding="utf-8")
with (DIR / "upgrade_decisions.csv").open("w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=list(decisions[0]))
    w.writeheader()
    w.writerows(decisions)
c = Counter(d["level"] for d in decisions)
print(f"upgraded to A: {c['A']}; still M: {c['M']}; "
      f"judged not relevant (retained): {sum(d['relevant_to_rq'] == 'no' for d in decisions)}")
print("now rerun run_all.sh")
