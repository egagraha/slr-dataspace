# Review protocol, version 1

**Status: documented after the fact.** This file records the rules that were
applied in the November 2026 search and selection, as reported in
`data/raw/References-Lists.md`. It was written on 10 November 2026, after the
selection was complete. It is not a pre-registered protocol and must not be
described as one. Any later change to these rules gets a new version number
(`protocol_v2.md`) and a dated entry in the change log at the end of this file.

## 1. Design

* **Design:** bounded literature mapping and thematic synthesis (manuscript
  Section 3). Not a systematic review: there was no pre-registration, no
  independent dual screening, no systematic full-text eligibility stage and no
  risk-of-bias appraisal.
* **Why this design fits the research questions:** RQ1 to RQ5 ask which
  frameworks, mechanisms, interoperability approaches, gaps and technologies the
  literature describes. A mapping answers "what is described and where"; it does
  not answer "how often" or "how well it works".
* **Synthesis method:** thematic synthesis by research question, consolidated
  into three proposed tensions and the DD-DSF framework.

## 2. Units of count

| Unit | Definition | Value |
|---|---|---|
| Retrieved record instance | one record returned by one search or lookup, counted within each RQ | 3,507 (sum over RQs) |
| Distinct retrieved DOI | one DOI, however often it was retrieved | 2,047 (from the retrieval ledgers; ledgers not in this repository) |
| Screened record | distinct DOI within one RQ after within-RQ deduplication | 3,221 (sum over RQs) |
| Placement | one publication included under one RQ | 250 (50 per RQ) |
| Unique publication | one DOI-identified publication, whatever the number of placements | 189 |

All values except 2,047 are re-derived and checked by `src/07_audit_tables.py`
(see `results/audit/audit_checks.csv`).

## 3. Sources and search

* **Registry:** Crossref REST API, `query.bibliographic`, `query` and
  `query.title` searches. Results are relevance-ranked (Elasticsearch BM25), not
  Boolean. Publication-date filter 2021-11 to 2026-11. Searches run in
  November 2026.
* **Supplementary routes:** targeted publisher, institutional-repository and
  author-source searches; citation chasing; each ending in an exact Crossref DOI
  lookup.
* **Not searched:** subscription databases (Scopus, Web of Science, IEEE
  Xplore, ACM Digital Library, ScienceDirect search).
* **Every search and lookup:** `results/audit/search_log.csv` (84 rows).

## 4. Eligibility

The rules are listed one per row in `protocol/eligibility_rules.csv`.

## 5. Screening and selection

1. Within each RQ, DOI duplicates removed; alternative versions of one study
   not selected twice.
2. Rule-assisted checks of publication type and date.
3. Manual assessment of candidate titles; targeted reading of abstracts,
   synopses and selected text where available.
4. Retention for direct relevance to the RQ or a clear enabling mechanism.
5. **Cap:** at most 50 placements per RQ. When the cap was reached, relevant
   lower-priority records were not selected. The "excluded or not selected"
   count therefore mixes ineligible records with relevant records that were not
   prioritized; the two were not recorded separately.
6. Screening by the research team; no independent second screener (see
   Section 8 for the planned agreement check).

## 6. Evidence level per placement

| Level | Meaning | Use in the manuscript |
|---|---|---|
| A | abstract, synopsis or primary-source summary assessed | may support statements about what a source proposes or reports |
| S | selected sections or excerpts read | as A, plus statements drawn from the sections read |
| M | title and bibliographic metadata only | topic statements only; never evidence of findings, effectiveness or behaviour |

The level describes reading depth, not study quality. Per-placement levels and
the source of each assessment are in `results/audit/placements.csv`.

## 7. Synthesis

* For each RQ: area of work and contribution of each placement collected and
  grouped into the comparison tables (manuscript Tables 4 to 8).
* Gap statements are the review team's assessments, not limitations reported
  by the original authors.
* The three tensions are derived across RQs; they are hypotheses grounded in
  the literature, not observations of practice.

## 8. Planned strengthening (revision, November 2026)

These steps are planned, not done. Results will be added to this repository
with their own files, and this section will be updated when each is complete.

| Step | Protocol | Output | Status (2026-11-11) |
|---|---|---|---|
| Coverage check in ScienceDirect | A3 | `protocol/coverage_check.md`, `results/audit/coverage_*.csv` | script ready; searches to run |
| Double screening of a blinded sample (90 records: 40 included, 50 not included) by Ega and Alexis | A4 | `results/audit/second_screening/` | screening done 2026-11-11: kappa 0.666 (3 categories, n = 90), 0.844 (include/exclude, n = 80); 16 disagreements to resolve |
| Claim-level evidence ledger for the tensions | B | `results/evidence/source_claims.csv` | 218 rows extracted; coding open |
| Double coding of tensions (10 calibration + 50 rows) by Ega and Alexis | B | `results/evidence/double_coding/`, `protocol/tension_codebook_v2.md` | calibration done, codebook v2 agreed 2026-11-11; main coding open |
| Comparison with earlier frameworks | C | `protocol/comparator_matrix.csv` | template ready; PDFs needed |

In A4 the two screeners are compared with each other, not with the original
decisions, because the original "not selected" label mixes ineligible records
with relevant records cut by the cap.

## Change log

| Version | Date | Change |
|---|---|---|
| 1 | 2026-11-10 | First written record of the rules applied in November 2026. |
