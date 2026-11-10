# Protocol A3: coverage check in ScienceDirect

## What this check can and cannot show

* ScienceDirect indexes Elsevier content only, so the check estimates coverage
  of relevant Elsevier publications, not of the whole literature.
* Crossref, the registry used for the review, also holds Elsevier DOIs. A
  relevant ScienceDirect record that is missing from the corpus was therefore
  missed because of query wording, relevance ranking or the 50-record cap, not
  because the registry lacked it. That is what the check tests.
* The result is reported as an estimate with its scope stated. It does not turn
  the mapping into a systematic review.

## Steps

### 1. Run the searches (you, in ScienceDirect Advanced Search)

Use the field **Title, abstract or author-specified keywords** and the years
**2021 to 2026**. ScienceDirect filters by year only; the script removes records
before November 2021 and after November 2026 using the export dates.

| ID | Query (Title, abstract, keywords) |
|---|---|
| SD1 | ("data space" OR "data spaces" OR dataspace) AND sovereignty |
| SD2 | "data sovereignty" |
| SD3 | ("data space" OR "data spaces" OR dataspace) AND interoperability |
| SD4 | "International Data Spaces" OR "Gaia-X" |

Article types: Research articles, Review articles, Book chapters, Short
communications. Leave all subject areas switched on.

### 2. Export (you)

For each query, export **all** results as **RIS** ("Export citation to RIS",
with abstracts). Save the files unchanged as

    data/external/coverage/sciencedirect_SD1_YYYY-MM-DD.ris

(one or more files per query if the export is split into pages). Write down the
result count ScienceDirect shows for each query and the date of the search.

### 3. Match against the corpus (script)

    uv run python src/08_coverage_check.py

The script reads every RIS file, normalizes DOIs, removes duplicates across
queries, applies the date window and writes

* `results/audit/coverage_candidates.csv`: every distinct record with
  `in_corpus` (1 if its DOI is among the 189) and empty columns for screening;
* `results/audit/coverage_summary.csv`: counts per query.

### 4. Screen the records that are not in the corpus (you, ideally with the second coder)

In `coverage_candidates.csv`, for each row with `in_corpus = 0`, fill
`relevant` (1 or 0) and `reason` using `protocol/eligibility_rules.csv` (for
example "E05 unrelated", "E04 front matter", or "relevant, RQ3"). Records with
`in_corpus = 1` need no screening.

### 5. Estimate coverage (script)

Run the script again. With the screening filled in it adds

    coverage = relevant records in the corpus / all relevant records

overall and per query, and lists the relevant records that were missed.

### 6. Report

Two sentences in manuscript Section 3.7 (scope, number of records, coverage
estimate) and the files in Supplementary Material S1. Missed relevant records
are not added to the corpus; adding them would change the 189 and every count
built on it.
