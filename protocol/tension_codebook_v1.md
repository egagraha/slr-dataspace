# Tension codebook, version 1 (Protocol B)

Used to code each row of `results/evidence/source_claims.csv`: one claim that
the manuscript attributes to one cited source. Two coders (Ega, Alexis) code a
sample independently; agreement is computed before any discussion.

Code the **source**, not the manuscript sentence: read the supporting passage in
the cited publication and ask what that publication reports. If the passage is
not available (metadata-only record, no access), code `NA` and say why.

## Field 1: `claim_type`

| Code | Use when the source ... |
|---|---|
| `finding` | reports a result it observed or measured (evaluation, case, survey, legal analysis conclusion) |
| `proposal` | proposes a design, architecture, model or mechanism, with or without a prototype |
| `description` | describes a regulation, initiative, standard or the state of the field |
| `review_assessment` | the manuscript statement is the review team's own assessment, not something the source states |

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

*Ambiguous:* a design-options classification that lists many connector
variants. Code T2 only if the source itself says the variety hinders exchange.

### T3 Privacy-preserving technology versus everyday workflows

**Include** when the source reports implementation effort, cost, skills,
operational constraints, adoption, or measured trade-offs (performance,
accuracy, usability) of a privacy-preserving or security technique.

**Exclude** a source that only proposes or describes an algorithm or
architecture without any of the above (code `T0`). The existence of a technique
is not evidence for T3.

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

## Field 3: `evidence_depth`

Pre-filled from `results/audit/placements.csv` for corpus records (A, S, M);
`full_text` when the coder read the full text for this row; `context` for
sources outside the 189.

## Decision rules

* A row coded T1 to T3 needs a supporting passage and page in
  `supporting_passage` and `page`.
* A metadata-only (M) source can be coded only T0 or NA.
* Do not change a code to make a tension look stronger; if support is weak,
  that is the result.

## Calibration

Before the main coding, both coders code the same 10 rows, compare, and
clarify this codebook. Changes go into `tension_codebook_v2.md` with a dated
note; the 10 calibration rows are then recoded and excluded from the agreement
figure.
