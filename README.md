# Sovereign data spaces: review corpus, analysis and figures

Supplementary Material S1 for a systematic literature review on data sovereignty,
interoperability and trust in data spaces for open innovation. The repository
holds the list of reviewed publications, the search and selection log, the code
that turns the list into counts and figures, and the results.

## What is in the review

* 5 research questions (RQ1 frameworks, standards and regulations; RQ2 security
  and privacy mechanisms; RQ3 interoperability; RQ4 gaps and challenges;
  RQ5 emerging technologies), 50 records each.
* 250 placements, 189 unique DOI-identified publications, 61 repeat placements.
* Publication window 8 November 2021 to 8 November 2026; Crossref searches and
  verification on 8 November 2026.
* Evidence level per record: **A** abstract assessed, **S** sections read,
  **M** metadata only. M records support topic statements only.

The selection is bounded and evidence-labelled. It is not an exhaustive
systematic review: there was no dual screening, no full-text appraisal of every
record and no subscription-database search. See `data/raw/References-Lists.md`,
sections "Scope and assessment method" and "Search log and verification notes".

## Folder structure

```
data/raw/        References-Lists.md          list, PRISMA-style counts, search log (input)
data/external/   openalex_189.json            OpenAlex snapshot for the 189 DOIs (retrieval date inside)
data/processed/  corpus_189.csv               one row per unique DOI: RQ membership, evidence level
                 corpus_enriched.csv          + year, authors, countries, keywords (OpenAlex)
                 references_189.bib           BibTeX for all 189 records (Crossref), for reference managers
src/             01_parse_reference_list.py   list -> corpus_189.csv, prisma_counts.csv
                 02_fetch_openalex.py         DOIs -> OpenAlex snapshot (needs network)
                 03_build_tables.py           counts -> results/*.csv, numbers.json
                 04_make_figures.py           results -> figures/fig_bib_*.drawio + .png
                 05_graphical_abstract.py     numbers -> figures/graphical_abstract.drawio + .png
                 drawio_lib.py                small draw.io writer and PNG exporter
results/         year_by_rq.csv, evidence_by_rq.csv, keywords_top.csv, countries.csv,
                 authors_top.csv, venues_top.csv, primary_field.csv, document_type.csv,
                 prisma_counts.csv, numbers.json, figure_cutoffs.json
figures/         *.drawio (editable source) and *.png (3x, for the manuscript)
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
* Figures 3 to 5 show the entries at or above the smallest count that keeps the
  list within the cap (`results/figure_cutoffs.json`), so a cut never splits a tie.

## Limits to keep in mind

* OpenAlex keywords and affiliations are incomplete and partly algorithmic.
* Records from 2026 are partly missing metadata at the time of retrieval.
* The 50-record cap per question shapes every count; the counts describe this
  corpus and not the volume of publication on the topic.

## Licence

To be set by the repository owner before the repository is made public for
review. Code and data would normally carry separate licences.
