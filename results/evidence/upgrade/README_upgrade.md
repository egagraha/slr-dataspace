# Upgrading the metadata-only placements (Package 2): instructions for both coders

74 of the 250 placements were assessed on title and bibliographic metadata only
(evidence level **M**). Abstracts have now been retrieved for 59 of the 60 DOIs behind
them (`src/16_metadata_only_abstracts.py`; snapshot in
`data/external/metadata_only_abstracts.json`). Reading the abstract makes a placement
level **A** by the definition in `data/raw/References-Lists.md`. Your task is to check,
independently, whether each placement still stands once the abstract is read.

## Files

| File | Use |
|---|---|
| `coding_Ega.csv` | Ega fills in this file only |
| `coding_Alexis.csv` | Alexis fills in this file only |

Both start identical and blank. Rows are in a random order (the same in both files).
Do not change the pre-filled columns (`placement_id` to `abstract`).

## Working independently

* Fill in **only your own file**. Do not open, copy or discuss the other file until
  both are finished and committed.
* Base each decision on the abstract in the row. You may open the DOI if the abstract
  is unclear; if you do, say so in `note`.
* Write `revised_gap_text` and `note` in your own words.

## Columns to fill in

### `relevant_to_rq`: does the publication belong under this research question?

Read `rq`, `area` and the abstract.

| Code | Use when |
|---|---|
| `yes` | the abstract shows the publication addresses the research question and the listed area of work |
| `no` | the abstract shows it does not (wrong topic, or the data-space link is only nominal) |
| `unclear` | the abstract is too short or too vague to decide; say why in `note` |

Research questions: RQ1 frameworks, standards and regulations; RQ2 security and
privacy mechanisms; RQ3 interoperability; RQ4 gaps and challenges; RQ5 emerging
technologies.

For the one row marked `NO ABSTRACT FOUND`, leave `relevant_to_rq` and
`gap_assessment` empty. That placement stays M.

### `gap_assessment`: does the review's open question (`gap_text`) still hold?

`gap_text` is the review team's own assessment, written from the title only. It is
not a limitation the authors report.

| Code | Use when |
|---|---|
| `holds` | the abstract is consistent with it |
| `revise` | it is roughly right but should be reworded, for example because the abstract shows that part of it has already been done (a prototype was evaluated, a use case was implemented) |
| `not_supported` | the abstract contradicts it, or it describes a different paper |

For `revise` or `not_supported`, write a replacement in `revised_gap_text`. Keep it to
one sentence in the style of the existing gap texts: an open question or a validation
need, not a summary of the paper.

### `note`

Free text. It is required for `no`, `unclear` and `not_supported`.

## After both files are finished

1. Commit both files (or send them to Ega), without having looked at the other one.
2. Run `uv run python src/18_upgrade_agreement.py`. It writes `agreement.csv`
   (percent agreement and Cohen's κ, computed before any discussion) and
   `disagreements.csv`. That file lists every row where your codes differ, plus every
   row coded `revise` or `not_supported`, because those need one agreed text.
3. Meet and fill in the `agreed_*` columns of `disagreements.csv`. Keep your original
   files unchanged; they are the audit trail.
4. Run `uv run python src/18_upgrade_agreement.py --apply`. For each placement with an
   abstract, it changes `[M]` to `[A]` and the register wording in
   `data/raw/References-Lists.md`, and writes the agreed gap texts. It also writes
   `upgrade_decisions.csv`. A placement agreed as not relevant is kept but flagged
   there, as was done for the screening sample, so that the corpus counts do not
   change.
5. Rerun `run_all.sh`. The new A/S/M counts flow into the tables, figures and audit
   checks. One audit check, "evidence A/S/M over 250 placements (manuscript: 146/30/74)"
   in `src/07_audit_tables.py`, will then report a difference on purpose: it is the
   reminder that the abstract, Table 3, the text and the graphical abstract still
   carry the old numbers. Update the manuscript by hand, then update that expected
   value so that all 50 checks pass again.
