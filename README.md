# Sovereign data spaces: review corpus, analysis and figures

Supplementary Material S1 for a bounded literature mapping and thematic synthesis
on data sovereignty, interoperability and trust in data spaces for open innovation. The repository
holds the list of reviewed publications, the search and selection log, the code
that turns the list into counts and figures, and the results.

## What is in the review

* 5 research questions (RQ1 frameworks, standards and regulations; RQ2 security
  and privacy mechanisms; RQ3 interoperability; RQ4 gaps and challenges;
  RQ5 emerging technologies), 50 records each.
* 250 placements, 189 unique DOI-identified publications, 61 repeat placements.
* Publication window November 2021 to November 2026; Crossref searches and
  verification in November 2026.
* Evidence level per record: **A** abstract assessed, **S** sections read,
  **M** metadata only. M records support topic statements only.

The selection is bounded and evidence-labelled. It is not an exhaustive
systematic review: independent double screening covered only a blinded sample
of 90 records (`results/audit/second_screening/`), and there was no full-text
appraisal of every record and no subscription-database search. See `data/raw/References-Lists.md`,
sections "Scope and assessment method" and "Search log and verification notes".

## How the records were found (not part of the scripts)

The candidate records were retrieved from the Crossref REST API with
`query.bibliographic` and `query.title` searches. Crossref ranks these results
with the default Elasticsearch scoring, which is BM25 (statement by Crossref staff:
<https://community.crossref.org/t/ticket-of-the-month-march-2022-getting-started-with-rest-api-queries/2587>).
The searches are relevance-ranked and not Boolean. Each query returned up to
50 records (100 or 150 for broad title searches shared between questions). The queries and counts are in `data/raw/References-Lists.md`
("Search log and verification notes"). The Python scripts in `src/` start from the
resulting list: they do not query Crossref and they do not use BM25. The only
service they call is OpenAlex, by DOI lookup (`02_fetch_openalex.py`).

## Folder structure

```
data/raw/        References-Lists.md          list, PRISMA-style counts, search log (input)
                 retrieval_ledgers/           original ledgers of the November 2026 selection, unchanged:
                                              rq1-rq5.json (queries, screening ledger with decision and
                                              reason per DOI, included records) and crossref_responses/
                                              (the 84 stored Crossref responses and DOI lookups)
data/external/   openalex_189.json            OpenAlex snapshot for the 189 DOIs (retrieval date inside)
                 metadata_only_abstracts.json  abstracts for the 60 DOIs of the M placements (+ _manual.json)
                 coverage/                    ScienceDirect RIS exports for the coverage check (Protocol A3)
data/processed/  corpus_189.csv               one row per unique DOI: RQ membership, evidence level
                 corpus_enriched.csv          + year, authors, countries, keywords (OpenAlex)
                 references_189.bib           BibTeX for all 189 records (Crossref), for reference managers
src/             01_parse_reference_list.py   list -> corpus_189.csv, prisma_counts.csv
                 02_fetch_openalex.py         DOIs -> OpenAlex snapshot (needs network)
                 03_build_tables.py           counts -> results/*.csv, numbers.json
                 04_make_figures.py           results -> figures/fig_bib_*.drawio + .png
                 05_graphical_abstract.py     numbers -> figures/graphical_abstract.drawio + .png
                 06_framework_figure.py       DD-DSF layers + exchange-decision process -> figures/fig_ddsf_framework.drawio + .png
                 07_audit_tables.py           list -> results/audit/ search log, placements, reconciliation checks
                 08_coverage_check.py         ScienceDirect exports -> coverage candidates and estimate
                 09_second_screening_sample.py  blinded double-screening sample (Protocol A4)
                 10_screening_agreement.py    agreement between the two screeners
                 11_claim_ledger.py           manuscript Results -> one row per claim and cited source (Protocol B)
                 12_double_coding_sample.py   calibration and agreement sets for tension coding
                 14_retrieval_recount.py      retrieval ledgers -> identified, screened, included and
                                              2,047 distinct DOIs, checked against the list (runs before step 7)
                 15_tension_sensitivity.py    agreed tension codes -> support per tension under the
                                              evidence rules S1-S4 (Protocol B, step 5)
                 16_metadata_only_abstracts.py  M placements -> abstracts from OpenAlex, Crossref,
                                              Semantic Scholar (+ manual publisher look-ups) (needs network)
                 17_upgrade_coding_files.py   blank coding files for the M -> A upgrade (two coders)
                 18_upgrade_agreement.py      agreement and kappa; with --apply, writes the agreed
                                              upgrades into data/raw/References-Lists.md
                 19_full_ledger_coding_files.py  blank coding files for every ledger row not settled
                                              by the sample (Package 3, two coders)
                 20_full_coding_agreement.py  agreement and kappa on the full-ledger coding
                 21_full_tension_sensitivity.py  sample + full-round codes -> S1-S4 over the whole
                                              ledger (prints SKIPPED until the coding is resolved)
                 drawio_lib.py                small draw.io writer and PNG exporter
protocol/        protocol_v1.md               rules as applied (written after the selection, not pre-registered)
                 eligibility_rules.csv        one row per eligibility rule
                 coverage_check.md            Protocol A3 procedure
                 comparator_protocol.md       Protocol C procedure
                 construct_dictionary.md      definitions, layer, indicator and direction of each DD-DSF
                                              construct (Protocol C, step 3)
                 proposition_test_map.csv     P1-P4: indicator, data source, observation that counts
                                              against the proposition, suggested design (Protocol C, step 4)
                 comparator_matrix.csv        comparison with earlier frameworks (manuscript Table 11):
                                              8 related works and the DD-DSF x features F1-F7, with
                                              first and final rating, page, supporting quotation,
                                              coder and checker
results/         year_by_rq.csv, evidence_by_rq.csv, keywords_top.csv, countries.csv,
                 authors_top.csv, venues_top.csv, primary_field.csv, document_type.csv,
                 prisma_counts.csv, numbers.json, figure_cutoffs.json
results/audit/   search_log.csv, placements.csv, evidence_by_rq_placement.csv, audit_checks.csv;
                 second_screening/ (screening files of both screeners, agreement, resolved disagreements)
results/evidence/ source_claims.csv (claim ledger); double_coding/ (files for two coders, instructions);
                 final_tension_codes.csv (the 50 agreed codes); sensitivity_tensions.csv (support per
                 tension under S1-S4); upgrade/ (M -> A upgrade: abstract retrieval log,
                 coding files for two coders, instructions, agreement, decisions); full_coding/
                 (Package 3: full-ledger coding files, carried-over sample codes, instructions);
                 final_tension_codes_full.csv and sensitivity_tensions_full.csv once that coding is resolved
private/         answer key of the screening sample; git-ignored until both screeners are finished
figures/         *.drawio (editable source) and *.png, black and white. Manuscript figure numbers:
                 Fig. 1 fig_bib_1_records_per_year, Fig. 2 fig_bib_2_evidence_by_rq,
                 Fig. 3 fig_bib_3_countries, Fig. 4 fig_bib_4_keywords, Fig. 5 fig_ddsf_framework;
                 fig_bib_5_authors is supplementary; graphical_abstract is printed on page 1 and also uploaded separately
run_all.sh       rebuilds everything
```

## Reproduce

Requirements: [uv](https://docs.astral.sh/uv/) and, for PNG export only, the
[draw.io desktop app](https://github.com/jgraph/drawio-desktop) (the `.drawio`
files are written without it).

```bash
./run_all.sh                 # full rebuild, queries OpenAlex
SKIP_FETCH=1 ./run_all.sh    # reuse the stored snapshot, no network
```

Step 3 and later are deterministic given `data/external/openalex_189.json`.
OpenAlex is a living index, so a new download can differ slightly from the stored
snapshot; the retrieval date is recorded in the snapshot.

## Counting rules

* Unit of analysis: unique DOI (189), not placement (250).
* Year: earliest registered date in the list (Crossref or primary source).
  OpenAlex differs for 11 records, listed by comparing `year` and
  `year_openalex` in `corpus_enriched.csv`.
* Countries: affiliation countries of all authors, each record counted once per
  country. 168 of 189 records carry affiliation data; the other 21 are not
  assigned to any country.
* Keywords: OpenAlex keywords, assigned by an algorithm; they are not author
  keywords. Each keyword counts once per record.
* The country, keyword and author figures show the entries at or above the smallest count that keeps the
  list within the cap (`results/figure_cutoffs.json`), so a cut never splits a tie.

## Limits to keep in mind

* OpenAlex keywords and affiliations are incomplete and partly algorithmic.
* Records from 2026 are partly missing metadata at the time of retrieval.
* The 50-record cap per question shapes every count; the counts describe this
  corpus and not the volume of publication on the topic.

## Licence

* Code (`src/`, `run_all.sh`): MIT License.
* Data, protocol files, results and figures created for this review
  (`data/processed/`, `protocol/`, `results/`, `figures/`, `data/raw/References-Lists.md`):
  Creative Commons Attribution 4.0 International (CC BY 4.0).
* Third-party material keeps its original terms: the Crossref responses in
  `data/raw/retrieval_ledgers/crossref_responses/`, the OpenAlex snapshot in
  `data/external/` and the ScienceDirect exports in `data/external/coverage/`.
  Abstracts contained in these files remain under the publishers' copyright.
