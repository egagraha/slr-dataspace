# Coding the full claim ledger (Package 3): instructions for both coders

The 50-pair sample showed which tensions the cited sources support (§4.7 of the
manuscript), but a sample of 50 cannot show whether tensions 2 and 3 are weak in
general or only in the sample. This round codes **every other claim-source row** of
the ledger, so that the sensitivity analysis can be rerun on the whole ledger.

Codebook: `protocol/tension_codebook_v2.md`, unchanged. It is the version you both
agreed after calibration, so there is no new calibration round. Reread it before
you start; the coding rules and worked examples in
`results/evidence/double_coding/README_coders.md` also still apply.

## Files

| File | Use |
|---|---|
| `coding_Ega.csv` | Ega fills in this file only |
| `coding_Alexis.csv` | Alexis fills in this file only |
| `carried_over.csv` | Read only. Which sample codes are reused and why four are not |

Both coding files start identical and blank, with 152 rows (85 distinct sources) in
a random order that is the same in both files.

### Which rows are in the files

The ledger (`results/evidence/source_claims.csv`) was rebuilt from the current
manuscript. It has 218 claim-source rows.

* **46 rows are not in your file.** They are the sample rows you already coded and
  agreed; their agreed codes are reused.
* **4 sample rows are coded again** and so are in your file. Two belong to sentences
  that changed in the manuscript (Zhang 2026, Qin 2026: the "metadata-level evidence"
  note was removed). In two, the source (Giess 2025) was at level M when you coded
  it, so you could only code T0 or NA; it is now level A.
* **20 rows are not coded**: they cite laws or W3C standards without a DOI, as in
  the sample.
* No row is at level M any more, so the rule "an M-level source can only be T0 or
  NA" does not apply in this round. `evidence_level = context` means the source is
  cited but is not one of the 189 reviewed publications; code it the same way.

## Working independently

* Fill in **only your own file**, from your own reading. Do not open, copy or
  discuss the other file until both are finished.
* Do not change the pre-filled columns (`claim_id` to `evidence_level`). If a
  pre-filled value looks wrong, say so in `note`.
* Open the source with `doi_url`. Code what the **source** reports, not what the
  manuscript sentence says. Many sources appear in several rows; code each row for
  the part of the sentence that cites that source.

## Columns to fill in

| Column | Codes | Rule |
|---|---|---|
| `claim_type` | `finding`, `proposal`, `description`, `review_assessment` | Code the passage, not the paper type (codebook v2) |
| `tension` | `T1`, `T2`, `T3`, `T0`, `NA` | Exactly one. `NA` only if the source cannot be read; say why in `note` |
| `counter` | `1` or empty | `1` if the source reports the opposite of the tension, or measures a cost that its authors judge acceptable |
| `page` | printed page, else section heading; `abstract` only if the passage is from the abstract | **Required for T1, T2, T3** |
| `supporting_passage` | short quotation or close paraphrase | **Required for T1, T2, T3** |
| `note` | free text | Say if you read the full text, and name a second tension that also fits |

The agreement script stops with an error if a row coded T1–T3 has no page or passage,
so that nothing is lost at the end.

**Time:** the sample took about one day for 50 rows, so allow about three days for 152.
Because the 85 sources repeat, the later rows go faster.

## After both files are finished

1. Commit both files, or send them to Ega, without having looked at the other one.
2. Run `uv run python src/20_full_coding_agreement.py`. It writes `agreement.csv`
   (raw agreement and Cohen's κ, before discussion, with the same measures as the
   sample) and `disagreements.csv` (every row where `claim_type`, `tension` or
   `counter` differs).
3. Meet and fill in `agreed_claim_type`, `agreed_tension`, `agreed_counter` and
   `resolution_note` for every row of `disagreements.csv`. Keep your own coding files
   unchanged; they are the audit trail.
4. Rerun `SKIP_FETCH=1 bash run_all.sh`. Step 21 then writes
   `final_tension_codes_full.csv` (198 coded pairs) and
   `sensitivity_tensions_full.csv` (S1–S4 over the whole ledger, same rule as the
   sample: robust 3 or more supporting sources, weakened 1–2, not supported 0).
   Until step 3 is done, step 21 prints `SKIPPED` and changes nothing.
5. Ega updates §4.7, Table 9 and the guideline review with the full-ledger result.
   The sample result (`sensitivity_tensions.csv`, step 15) is kept as it is.
