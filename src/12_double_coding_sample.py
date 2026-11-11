"""Step 12. Double-coding sample for the tension codebook (Protocol B, step 3).

Draws, per research question, 12 claim-source rows with a DOI from
results/evidence/source_claims.csv (seeded): the first 2 per RQ form the
calibration set (10 rows), the other 10 per RQ the agreement set (50 rows).
Writes identical files for both coders; the coders fill claim_type, tension,
counter, page, supporting_passage and note, following protocol/tension_codebook_v2.md.

Output: results/evidence/double_coding/calibration_<name>.csv
        results/evidence/double_coding/coding_<name>.csv
"""
import csv
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/evidence/double_coding"
CODERS = ["Ega", "Alexis"]
SEED, PER_RQ, CAL_PER_RQ = 20261110, 12, 2

if OUT.exists() and any(OUT.glob("*.csv")):
    raise SystemExit(f"{OUT} already holds coding files; delete them first to draw a new sample.")
rows = [r for r in csv.DictReader((ROOT / "results/evidence/source_claims.csv").open(encoding="utf-8")) if r["doi"]]
rng = random.Random(SEED)
cal, main = [], []
for rq in ["RQ1", "RQ2", "RQ3", "RQ4", "RQ5"]:
    pick = rng.sample([r for r in rows if r["rq"] == rq], PER_RQ)
    cal += pick[:CAL_PER_RQ]
    main += pick[CAL_PER_RQ:]
rng.shuffle(cal)
rng.shuffle(main)
cols = ["claim_id", "rq", "sentence", "cite_key", "doi", "evidence_level",
        "claim_type", "tension", "counter", "page", "supporting_passage", "note"]
OUT.mkdir(parents=True, exist_ok=True)
for name in CODERS:
    for label, data in (("calibration", cal), ("coding", main)):
        with (OUT / f"{label}_{name}.csv").open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
            w.writeheader()
            for r in data:
                w.writerow({**r, "claim_type": "", "tension": "", "counter": "", "page": "",
                            "supporting_passage": "", "note": ""})
print(f"calibration rows: {len(cal)}, coding rows: {len(main)}, coders: {', '.join(CODERS)}")
