# Protocol C: comparison of DD-DSF with earlier frameworks

Purpose: show, with page-level evidence, what DD-DSF describes that the closest
earlier work does not, and what it shares with it. The result replaces most of
the prose in manuscript Section 6.2 with one comparison table.

## 1. Comparator set

All eight are already cited in the manuscript. "Role" says why each belongs in
the set. Full texts must be read; no cell may be coded from a title or abstract.

| ID | Key | Reference | DOI | Role | Where to get the full text |
|---|---|---|---|---|---|
| C1 | Hummel2021 | Hummel et al. (2021), Big Data & Society | 10.1177/2053951720982012 | concept review of data sovereignty | publisher (SAGE) or library |
| C2 | Bacco2024 | Bacco et al. (2024), Data in Brief | 10.1016/j.dib.2024.110969 | survey of the data space field | ScienceDirect |
| C3 | Kovach2026 | Kovach et al. (2026), Computer Science Review | 10.1016/j.cosrev.2025.100819 | mapping of building blocks and sectoral adoption | ScienceDirect |
| C4 | Giess2025 | Gieß et al. (2025), Computers in Industry | 10.1016/j.compind.2024.104212 | design options for data spaces | ScienceDirect |
| C5 | Schleimer2023 | Schleimer et al. (2023), HICSS 56 | 10.24251/hicss.2023.447 | architecture design options | HICSS proceedings (ScholarSpace) |
| C6 | OttoJarke2019 | Otto and Jarke (2019), Electronic Markets | 10.1007/s12525-019-00362-x | IDS as a multi-sided platform | publisher (Springer) or library |
| C7 | Moller2024 | Möller et al. (2024), Electronic Markets | 10.1007/s12525-024-00724-0 | industrial data ecosystems | publisher (Springer) or library |
| C8 | Guggenberger2025 | Guggenberger et al. (2025), European Journal of Information Systems | 10.1080/0960085x.2025.2451250 | data spaces as meta-organisations | publisher (Taylor & Francis) or library |

Put the PDFs in `protocol/comparators_pdf/`. That folder is listed in
`.gitignore` because publisher PDFs must not be redistributed.

## 2. Features

| Code | Feature | "Explicit" means the paper ... |
|---|---|---|
| F1 | Regulatory translation | describes how legal or contractual rules become concrete decisions or technical policies for a data set and partner |
| F2 | Interoperability (connector and semantic) | describes how connectors, vocabularies or semantic models make exchange possible between heterogeneous participants |
| F3 | Explicit actor decisions | models the decision of a participant to share, restrict or reuse data as an element of the framework |
| F4 | Governance feedback | describes a route by which experience from operation changes rules or technical standards |
| F5 | Economic incentives | treats costs, benefits or business models of participation as part of the framework |
| F6 | Measurable innovation outcome | names an outcome beyond a completed exchange (new product, service, process or analytical capability) and how to observe it |
| F7 | Empirical validation | tests or applies the framework in one or more operating settings with reported evidence |

## 3. Rating scale

| Rating | Use when |
|---|---|
| explicit | the feature is a named element of the framework or a stated result |
| partial | the feature is mentioned or implied but not developed |
| not described | the full text was searched and the feature does not appear |
| not assessable | the paper's scope makes the question inapplicable (for example F7 for a pure concept review) |

Rules:
* Every cell needs a page, section or figure reference and a short quotation or
  close paraphrase in `protocol/comparator_matrix.csv`.
* "not described" requires that the whole full text was checked; write
  "searched full text" in the note column.
* Do not code DD-DSF itself in the same file; its row is added only after the
  eight comparators are done, so that the coding is not tuned to it.
* No claim of "first" or "only" in the manuscript unless every comparator is
  "not described" for that feature and the text says the comparison is limited
  to these eight works.

## 4. Coding steps

1. Read each full text once without coding.
2. Code F1 to F7 for each comparator in `protocol/comparator_matrix.csv`.
3. A second person checks every "not described" and every "explicit" cell
   against the cited page.
4. Agree the final ratings; keep the first and final rating in the file.
5. Draft the Section 6.2 table: rows = comparators plus DD-DSF, columns = F1 to
   F7, ratings only; the evidence stays in the CSV in Supplementary Material S1.

## 5. Follow-on files (Protocol C steps 3 and 4)

* `protocol/construct_dictionary.md`: one line per construct with a definition
  and a unit.
* `protocol/proposition_test_map.csv`: P1 to P4 with indicator, data source and
  one observation that would count against the proposition.
