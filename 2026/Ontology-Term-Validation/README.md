---
authors:
  - name: Mohamed Abouzid
    orcid: https://orcid.org/0009-0007-7035-4399
    affiliation: Forschungszentrum Jülich (IBG-4: Bioinformatics)
---

# Ontology Term Validation for ARCs (`ontology-terms`)

A Python ARC validation package that checks whether the ontology / controlled-vocabulary
(CV) annotations inside an ARC's ISA metadata are **complete, well-formed, declared, and
resolvable against a terminology service**. Built as an output of the 2026 Hands-On
Symposium and intended for contribution to the
[arc-validate-package-registry](https://github.com/nfdi4plants/arc-validate-package-registry).

## Motivation / Problem

ARCs encourage rich, ontology-backed annotation: every `Characteristic`, `Parameter`,
and `Factor` building block in a study or assay table can carry a *Term Source REF* and a
*Term Accession Number* that anchor a free-text value to a controlled vocabulary
(e.g. `Parameter [Temperature]` → `NCIT:C25206`). This is what makes ARC metadata
interoperable and FAIR.

However, the existing validation packages in the registry (invenio, pride, edal, odrl,
plant-growth, hhu-cmml, ceplas) target **publication readiness** or **terms-of-use**,
none of them check the *quality of the annotations themselves*. In practice this means a
range of real problems go completely unvalidated:

- a value annotated with an accession but no source (or vice versa);
- a malformed accession;
- a Term Source REF that is **never declared** in the Investigation's ONTOLOGY SOURCE
  REFERENCE section;
- an accession whose prefix disagrees with its declared source;
- an accession that simply **does not exist** in any terminology service (a typo, a dead
  term, or a non-canonical id).

Inspecting real ARCs from the DataHUB confirmed this is not hypothetical. The
*Geobacillus thermoleovorans* genomics ARC, for example, declares **zero** ontology
sources despite citing OBI, NCIT, EFO, DPBO, MIAPPE and NCBITaxon throughout its tables,
and stores several accessions in non-canonical, doubled-prefix form
(`EFO:EFO_0005061`, `…/obo/MICRO_MICRO_000052`).

A second, deliberate motivation: all seven existing packages are written in **F#**
(on the ARCExpect DSL). The registry supports Python (executed via `uv`), but no
non-trivial Python package existed. This package doubles as a demonstration that a
real-world validation package can be authored in Python end-to-end.

## Proposed Solution

A single self-contained Python package, `ontology-terms`, that flattens every ontology
annotation in an ARC into a uniform record and runs **seven checks** across two tiers:

| # | Check | Tier | Severity | What it verifies |
|---|-------|------|----------|------------------|
| 1 | `pairing` | offline | error | Term Source REF and Term Accession Number are either both present or both absent |
| 2 | `wellformed` | offline | error | the accession is a valid `PREFIX:LOCAL` id or IRI |
| 3 | `source_declared` | offline | error | the Term Source REF is declared in the Investigation ONTOLOGY SOURCE REFERENCE section |
| 4 | `prefix_consistency` | offline | error | the accession prefix matches its Term Source REF |
| 5 | `coverage` | offline | warning | flags free-text values that carry no ontology annotation |
| 6 | `resolves` | online | error | the accession actually exists in a terminology service |
| 7 | `label_match` | online | warning | the service's canonical label matches the annotation name |

The package emits the registry's standard three-file result contract into
`.arc-validate-results/ontology-terms@<version>/`: a JUnit `validation_report.xml`
(one case per check × term, located down to file/table/column/row), a
`validation_summary.json`, and a status `badge.svg`.

### Constraints discussed, and how they shaped the design

- **Validation runs in isolated CQC environments where network is not guaranteed.**
  Resolving an accession fundamentally requires a network call, which is at odds with
  reproducible, offline CI. → The checks are **tiered**: the five offline checks always
  run and are fully deterministic; the two online checks are attempted only when a
  terminology service is reachable and otherwise reported as `skipped` (never `failed`),
  so a network blip can never masquerade as an ARC defect. An
  `ONTOLOGY_TERMS_OFFLINE=1` switch forces deterministic, network-free runs.

- **ISA legitimately permits free-text values.** Flagging every unannotated value as an
  error would be wrong and noisy. → `coverage` is a **warning**, a nudge toward FAIR
  annotation rather than a gate.

- **No single terminology service hosts every ontology.** During testing, DataPLANT's
  canonical TIB Terminology Service returned the OBI/NCIT/EFO/DPBO terms but does **not**
  host NCBITaxon, which EBI OLS does. → `resolves` queries **TIB first, then falls back
  to OLS** before declaring a term unresolvable.

- **Accessions appear in both prefixed and IRI form.** Real ARCs store accessions as
  `NCIT:C25206` *and* as `http://purl.obolibrary.org/obo/NCBITAXON_33941`. A naive
  obo_id query silently fails for IRIs. → Accessions are **normalized** (OBO-style IRI →
  prefixed obo_id) before querying.

## Technical Details on Implementation

- **Language / packaging:** one self-contained Python file
  (`ontology-terms@1.0.0.py`) with YAML frontmatter metadata and a `uv` inline
  dependency block (`arctrl`, `requests`); executed by the registry/CQC pipeline via
  `uv run`.
- **ARC reading:** uses [**ARCtrl**](https://github.com/nfdi4plants/ARCtrl) (the polyglot
  ARC library, `pip install arctrl`). `ARC.load()` reads the ARC; the package then walks
  every study and assay table, extracting ontology annotations from both **column
  headers** (`header.TryGetTerm()`) and **term / unitized cells**, plus the declared
  ONTOLOGY SOURCE REFERENCE list. Reading through ARCtrl keeps the package aligned with
  the rest of the toolstack rather than re-parsing XLSX by hand.
- **Term resolution:** the TIB and OLS search APIs share a Solr-style response
  (`/api/search?q=<obo_id>&queryFields=obo_id&exact=true`). Unique `(source, accession)`
  pairs are de-duplicated and cached, queried with a short timeout and one retry, and
  fall back TIB → OLS. A service that answers "not found" yields a genuine `error`; a
  service that cannot be reached yields `skipped`.
- **Output / severity mapping:** `error`-severity failures are critical (badge red and
  `critical: true` in the summary); `warning`-severity failures are non-critical (badge
  yellow); `skipped` never affects the verdict.
- **Tests:** the checks are pure functions over a small data model, unit-tested without
  any ARC on disk; the ARCtrl wiring and the full three-file output are tested
  end-to-end against a real ARC fixture.

### Validated against a real ARC

Run against the *Geobacillus thermoleovorans* ARC, the package surfaced concrete,
correctly-located findings: ~287 `source_declared` errors (the ARC declares no ontology
sources at all), 119 free-text `coverage` warnings, and a handful of genuinely
unresolvable accessions - the non-canonical `EFO:EFO_0005061` and
`MICRO_MICRO_000052`, and `MIAPPE:0079` (MIAPPE is not hosted by TIB or OLS).
Developing the online tier on this ARC also caught a real false-negative class:
NCBITaxon accessions stored as IRIs were initially queried against the wrong field,
producing ~250 spurious "does not resolve" errors; the IRI-normalization + OLS-fallback
fix reduced the total error count from **542 to 294**, leaving only true findings.

## Automation / Enforcement

The package plugs directly into the existing DataPLANT automation chain, requiring no new
infrastructure:

1. **Distribution** - contribute the single `.py` file to `StagingArea/ontology-terms/`
   in the [arc-validate-package-registry](https://github.com/nfdi4plants/arc-validate-package-registry);
   the registry CI tests it and publishes it to [avpr.nfdi4plants.org](https://avpr.nfdi4plants.org).
2. **Execution** - `arc-validate package install ontology-terms` then
   `arc-validate validate -p ontology-terms` (the maintained, `uv`-equipped
   `arc-validate` container build).
3. **Continuous Quality Control** - once published, the package can be referenced in an
   ARC's `.arc/validation_packages.yml` and is pulled and executed automatically by the
   **DataHUB CQC pipelines** on every push, turning ontology-annotation quality into a
   continuously-enforced, badge-reported property of the ARC.

## Status & Next Steps

- v1.0.0 implemented and tested; will be submitted with `Publish: false` for DataPLANT review.
- Open items: confirm the summary/critical convention against the registry CI; consider
  an optional ontology-source-allowlist; evaluate whether non-canonical "doubled-prefix"
  accessions should be auto-normalized or kept as explicit findings.

## Payload

- `ontology-terms@1.0.0.py` - the validation package (add alongside this README).
