# Tension codebook, version 2 (Protocol B)

> **Agreed on 2026-11-11 by Ega and Alexis.** Written after the calibration
> round (10 rows, coded by Ega and Alexis, files received 2026-11-11). Rules
> marked **[v2]** are new or changed compared with version 1. Main coding uses
> this version.

Used to code each row of `results/evidence/source_claims.csv`: one claim that
the manuscript attributes to one cited source. Two coders (Ega, Alexis) code a
sample independently; agreement is computed before any discussion.

Code the **source**, not the manuscript sentence: read the supporting passage in
the cited publication and ask what that publication reports. If the passage is
not available (metadata-only record, no access), code `NA` and say why.

## Working independently [v2]

* Start from the **blank** file issued to you. Never start from, copy or look at
  the other coder's file, including an earlier draft of it, before both main
  files are finished.
* Write `page`, `supporting_passage` and `note` in your own words from your own
  reading.
* Do not change the pre-filled columns (`claim_id` to `evidence_level`). If you
  think a pre-filled value is wrong, say so in `note`.
* `note` must match what you did. Do not write "could not read the source" next
  to a quotation from it.

## Field 1: `claim_type`

| Code                  | Use when the source ...                                                                                  |
| --------------------- | -------------------------------------------------------------------------------------------------------- |
| `finding`           | reports a result it observed or measured (evaluation, case, survey, legal or policy analysis conclusion) |
| `proposal`          | proposes a design, architecture, model or mechanism, with or without a prototype                         |
| `description`       | describes a regulation, initiative, standard or the state of the field                                   |
| `review_assessment` | the manuscript statement is the review team's own assessment, not something the source states            |

**[v2] Code the passage, not the paper type.**

* A paper that proposes a system and then evaluates it is `finding` when the
  passage you use is the evaluation result (for example a measured latency),
  and `proposal` when the passage is the design itself.
* A legal or policy analysis that concludes a rule is unclear, insufficient or
  hard to enforce is `finding`, also when it ends with recommendations. It is
  never `proposal`.
* A source that only sets out what a law or regulation contains is
  `description`.

**[v2] When to use `review_assessment`.** Use it only when the source supports
**none** of the substantive point of the manuscript sentence; `tension` is then
`T0`. When the source supports part of the sentence, code the source's own
`claim_type` and `tension` for that part, and write in `note` which part is the
review's own (for example "the 'centralized vs distributed' clause is the
review's").

## Field 2: `tension`

Exactly one code per row. When two fit, pick the one the supporting passage
addresses most directly and note the other in `note`.

### T1 Regulation versus routine

**Include** when the source shows or argues a gap between a formal rule
(law, regulation, contract, policy) and how organizations decide or act: rules
that are hard to apply to a concrete data set or partner, uneven enforcement,
uncertainty about which instrument applies, compliance effort in practice.

**Exclude** a source that only describes what a regulation says, with no
statement about its application (code `T0`).

*Ambiguous:* a legal analysis predicting application problems for a proposal
text. Code T1, `claim_type = finding`, and write "proposal-stage" in `note`.

### T2 Interoperability across heterogeneous environments

**Include** when the source observes or explicitly analyses an incompatibility
between connectors, protocols, data models, vocabularies, usage conditions or
organizational interpretations, or the effort needed to overcome it.

**Exclude** a source that presents an interoperability standard or ontology
without reporting an incompatibility or the effort to bridge it (code `T0`).

**[v2]** A stated aim ("to enable seamless sharing", "a unified data model") or
a mapping that is presented as done, without a reported mismatch or bridging
effort, is `T0`. The word "interoperability" in the passage is not enough.

*Ambiguous:* a design-options classification that lists many connector
variants. Code T2 only if the source itself says the variety hinders exchange.

### T3 Privacy-preserving technology versus everyday workflows

**Include** when the source reports implementation effort, cost, skills,
operational constraints, adoption, or measured trade-offs (performance,
accuracy, usability) of a privacy-preserving or security technique.

**Exclude** a source that only proposes or describes an algorithm or
architecture without any of the above (code `T0`). The existence of a technique
is not evidence for T3.

**[v2]**

* A passage of the form "we propose X" is never T3, however relevant X is.
* T3 applies only to privacy-preserving or security **techniques**. Laws,
  legislative frameworks and governance arrangements are never T3; check them
  against T1.
* Design goals ("must prove identity and integrity") are not measured effort.

*Ambiguous:* a performance benchmark. Code T3 only for trade-offs that affect
operation (latency, cost, accuracy loss), and note which.

### T0 No direct tension evidence

The source supports the manuscript sentence but says nothing that bears on
T1 to T3. This is a normal code, not a failure; most descriptive citations
will be T0.

### Counterevidence flag (`counter = 1`)

Set when the source reports the opposite of a tension: a rule that made
exchange easier, interoperability achieved with little effort, a privacy
technique adopted without the expected cost.

**[v2] Mixed evidence.** When the source measures a cost **and** its authors
conclude the cost is acceptable for the intended use, keep the tension code,
set `counter = 1`, and write both in `note` ("measured X; authors judge it
acceptable"). Leave `counter` empty when the authors call the cost a
limitation or say nothing about its acceptability.

## Field 3: `evidence_depth`

Pre-filled from `results/audit/placements.csv` for corpus records (A, S, M);
`full_text` when the coder read the full text for this row; `context` for
sources outside the 189.

## Decision rules

* A row coded T1 to T3 needs a supporting passage and page in
  `supporting_passage` and `page`.
* **[v2] `page`:** the printed page number. If the source has none (HTML
  version), the section number or heading. Write `abstract` only when the
  passage is from the abstract.
* A metadata-only (M) source can be coded only T0 or NA.
* Do not change a code to make a tension look stronger; if support is weak,
  that is the result.

## Calibration

Before the main coding, both coders code the same 10 rows, compare, and
clarify this codebook. Changes go into `tension_codebook_v2.md` with a dated
note; the 10 calibration rows are then recoded and excluded from the agreement
figure.

### Calibration round, 2026-11-11

Agreement before discussion: `tension` 7 of 10 rows, `claim_type` 4 of 10.
These figures overstate independent agreement: both files were edited from a
common earlier draft (identical `note` text in 6 rows, identical passages in
4), so the round tests the codebook, not the coders' independence.

| Row         | Source             | Ega                                       | Alexis               | Proposed consensus under v2                               | Rule                                                                         |
| ----------- | ------------------ | ----------------------------------------- | -------------------- | --------------------------------------------------------- | ---------------------------------------------------------------------------- |
| CL-5c41d6fd | Ryan2024           | proposal T1                               | finding T1           | finding T1                                                | legal analysis conclusion = finding                                          |
| CL-92519577 | Carrapico2025      | finding T1                                | review_assessment T1 | finding T1; note: architecture clause is the review's     | review_assessment only if no part supported                                  |
| CL-84bcbce4 | Chrysakis2025      | proposal T2                               | proposal T2          | proposal T0                                               | aim or mapping without mismatch = T0                                         |
| CL-0c5d1a92 | Arroyo2025         | review_assessment T1 (level changed to S) | proposal T1          | finding T1                                                | policy analysis with recommendations = finding; do not edit pre-filled level |
| CL-cd6995f3 | AlaejosHerrero2026 | proposal T3                               | proposal T3          | finding T3, counter 1                                     | evaluation passage = finding; mixed evidence rule                            |
| CL-0f698db3 | Choque2026         | proposal T2                               | proposal T2          | finding T2                                                | reported incompatibility (OAuth2 vs IDS) = observed result                   |
| CL-16f4a523 | Terzis2023         | review_assessment T0                      | review_assessment T0 | review_assessment T0                                      | agreed                                                                       |
| CL-4d36602a | Hajszan2026        | proposal T3                               | finding T2           | proposal T0                                               | "we propose" is never T3; no mismatch reported, so not T2                    |
| CL-2d4e1987 | Su2025             | finding T3                                | review_assessment T1 | description T0; note: multi-regime clause is the review's | laws are never T3; description of law without application = T0               |
| CL-9437ed81 | Huber2022          | proposal T3                               | review_assessment T0 | proposal T0                                               | design goals are not measured effort; source supports the row                |

The consensus column was the starting point for the discussion on
2026-11-11. The binding record of the calibration codes is each coder's recoded
calibration file under v2.
