#!/usr/bin/env bash
# Rebuild every table and figure from the raw reference list.
# Step 2 needs network access; skip it to reuse the stored OpenAlex snapshot.
set -euo pipefail
cd "$(dirname "$0")"
uv run python src/01_parse_reference_list.py
[ "${SKIP_FETCH:-0}" = "1" ] || uv run python src/02_fetch_openalex.py
uv run python src/03_build_tables.py > /dev/null
uv run python src/04_make_figures.py      # PNG export needs the draw.io desktop app
uv run python src/05_graphical_abstract.py
uv run python src/06_framework_figure.py
uv run python src/14_retrieval_recount.py # original retrieval ledgers -> distinct DOIs (read by step 7)
uv run python src/07_audit_tables.py      # fails if a reported count does not reconcile
uv run python src/15_tension_sensitivity.py # agreed tension codes -> sensitivity S1-S4
# Coverage check only after the ScienceDirect exports are in data/external/coverage/
if ls data/external/coverage/sciencedirect_*.ris >/dev/null 2>&1; then
  uv run python src/08_coverage_check.py
fi
