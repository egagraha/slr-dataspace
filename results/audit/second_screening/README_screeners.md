# Double screening: instructions for Ega and Alexis

Time: about half a day. Work alone; do not discuss records until both files
are finished.

## Your file

`screening_Ega.csv` or `screening_Alexis.csv`. Both hold the same 90 records
(IDs X001 to X090), mixed across the five research questions. Some were
included in the review and some were not; the file does not say which, and you
should not check the reference list or `results/audit/placements.csv` while
screening.

## For each row

1. Read the research question in column `research_question`, then the title
   and abstract. If the abstract is empty, open `https://doi.org/<doi>` and use
   the abstract on the publisher page; if there is none, decide from the title
   and write "title only" in `note`.
2. Fill `decision` with one word:
   * `include`: the record meets every rule below **and** is directly relevant
     to that research question (or describes a clear enabling mechanism for RQ2
     or RQ5);
   * `exclude`: at least one rule fails;
   * `unsure`: you cannot decide from the information available.
3. For `exclude`, put the first rule that fails in `rule` (for example `E04`).
   For `include` or `unsure`, leave `rule` empty or note the doubt in `note`.

Judge eligibility and relevance only. Ignore the 50-record cap (rule E08):
you are not asked whether the record would have been among the top 50.

## Rules (full text in protocol/eligibility_rules.csv)

| Rule | Exclude when |
|---|---|
| E01 | first published before November 2021 or after November 2026 |
| E03/E04 | it is not a journal article, conference paper, substantive book chapter or scholarly review; preprints, data sets, peer-review reports, supplementary files, whole proceedings and front matter are excluded |
| E05 | it is clearly unrelated to data spaces, data sovereignty or sovereign data sharing |
| E06 | it is not relevant to the research question in that row and does not describe an enabling mechanism (RQ2, RQ5) |
| E07 | it is an alternative version of a record you have already judged in this file |

## Worked examples

These records are **invented** to show the format. None of them is in your
file. Only the last three columns are yours to fill.

| sample_id | rq | title (type, year) | what the abstract says | decision | rule | note |
|---|---|---|---|---|---|---|
| EX1 | RQ3 | A semantic connector registry for cross-company data exchange in manufacturing data spaces (article, 2024) | describes and evaluates a registry that lets participants find connectors by vocabulary and policy | include | | connector discovery, directly RQ3 |
| EX2 | RQ2 | Usage control for sovereign data sharing: a policy enforcement architecture (preprint, 2025) | proposes an enforcement architecture | exclude | E04 | preprint |
| EX3 | RQ2 | Review of: "Trust anchors in data spaces" (peer-review, 2024) | reviewer report | exclude | E04 | peer-review report |
| EX4 | RQ4 | Dataspace exploration methods for spacecraft telemetry (article, 2023) | about storing satellite telemetry | exclude | E05 | unrelated meaning of "data space" |
| EX5 | RQ1 | Improving model accuracy in federated medical imaging (article, 2025) | accuracy of a federated model; no governance, regulation or sovereignty | exclude | E06 | not relevant to RQ1 (could matter for RQ5, but the row asks RQ1) |
| EX6 | RQ5 | Blockchain-based consent logs for health data spaces (conference paper, 2020) | ledger for consent records | exclude | E01 | published before November 2021 |
| EX7 | RQ2 | Towards trustworthy data ecosystems (book chapter, 2023) | no abstract; publisher page shows only the title | unsure | | title only; could be RQ2 or general |

Notes on the examples:
* EX5: judge relevance to the research question **of that row**, not to the
  review in general.
* EX7: use `unsure` rather than guessing; give the reason in `note`.
* Give only the **first** rule that fails, even if several do.

## When you are done

Save the file under the same name and send it to Ega. Ega runs the agreement
analysis; the answer key is opened only after both files are complete.
