# Tension coding: instructions for Ega and Alexis

Codebook: `protocol/tension_codebook_v2.md` (agreed 2026-11-11 after calibration).
Read it before starting the main coding. Version 1 (`tension_codebook_v1.md`)
was used for the calibration round only.

1. **Calibration (10 rows).** Each of you codes `calibration_<name>.csv` alone.
   Then compare the two files together, clarify the codebook where you
   disagreed, and save the clarified version as `tension_codebook_v2.md` with a
   dated note. The calibration rows do not count towards agreement.
2. **Main coding (50 rows).** Each of you codes `coding_<name>.csv` alone,
   using codebook v2. Do not discuss rows until both files are finished.

For each row, open the cited source by its DOI and code what the **source**
reports, not what the manuscript sentence says:

* `claim_type`: finding, proposal, description or review_assessment
* `tension`: T1, T2, T3, T0 or NA (NA only if the source cannot be read; say why in `note`)
* `counter`: 1 if the source reports the opposite of a tension, else empty
* `page` and `supporting_passage`: required for T1, T2 and T3; a short quotation
  or close paraphrase
* A source with `evidence_level = M` can only be coded T0 or NA.

Time: about one day for the 50 main rows. Send the finished file to Ega.

## Worked examples

These rows are **invented** to show the format. The sources, pages and
passages do not exist and none of the rows is in your file. You fill only the
last six columns.

| manuscript sentence (shortened) | evidence_level | claim_type | tension | counter | page | supporting_passage | note |
|---|---|---|---|---|---|---|---|
| "X examine how the Data Act applies to IoT data." Source: a legal analysis concluding that companies cannot tell which instrument governs a mixed data set | A | finding | T1 | | 12 | "firms holding mixed personal and machine data face overlapping, unclear obligations" | legal analysis conclusion |
| "Y propose a usage-control architecture for connectors." Source: architecture and prototype, no cost or effort data | A | proposal | T0 | | | | existence of a mechanism is not T3 |
| "Z evaluate homomorphic encryption for aggregation." Source: benchmark reporting a 40-fold latency increase that rules out daily batch use | S | finding | T3 | | 9 | "latency rose by a factor of about 40, too slow for the daily reporting cycle" | operational trade-off |
| "W report a pilot where two connectors exchanged data." Source: case where the exchange worked after one configuration step | A | finding | T2 | 1 | 6 | "interoperation required only a single shared vocabulary mapping" | counterevidence: little effort needed |
| "V address verifiable sovereignty for vulnerable groups." Source known by metadata only; no access to the text | M | description | NA | | | | metadata only, full text not accessible |
| "Semantic alignment remains an open problem." The cited source describes an ontology but does not call alignment an open problem | A | review_assessment | T0 | | | | the "open problem" is the review's own statement |

Rules the examples show:
* Code what the **source** reports. If the manuscript says more than the
  source, use `review_assessment` and say so in `note`.
* T1, T2 and T3 always need a page and a passage; T0 and NA do not.
* An M-level source can only be T0 or NA (example 5).
* `counter = 1` marks evidence **against** a tension; keep the tension code it
  speaks to (example 4).
