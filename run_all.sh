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
