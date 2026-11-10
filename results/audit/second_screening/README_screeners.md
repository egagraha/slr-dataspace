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

## When you are done

Save the file under the same name and send it to Ega. Ega runs the agreement
analysis; the answer key is opened only after both files are complete.
