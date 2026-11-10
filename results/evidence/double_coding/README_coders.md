# Tension coding: instructions for Ega and Alexis

Codebook: `protocol/tension_codebook_v1.md`. Read it before starting.

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
