---
authors:
  - name: Luiz Gadelha
    orcid: 0000-0002-8122-9522
    affiliation: GreenRobust
  - name: Vandana Jha
    orcid: 0000-0002-6629-0042
    affiliation: GreenRobust
---
# Motivation and Solution

The [Cluster of Excellence GreenRobust](https://www.greenrobust.de) started its activities in January 2026 with the objective of elucidating plant robustness. A Plant Perturbation Atlas (PPA) will be created using greenhouse plant sowing results and the plant samples will be analyzed at phenotypic and molecular levels. The cluster will create a Central Data Hub (CDH) that will follow the DataPLANT tooling and standards. In the symposium, data stewards from the cluster explored topics like ARC templates, ARC validation, and tools like SWATE and ARCtrl. The following activities were peformed:
  - Templates available in the [DataPLANT Template Registry Service](https://str.nfdi4plants.org/) were surveyed and a first attempt was made to map them to the data types used in the cluter. Many of the existing templates could potentially be reused, for instance:
    - gene expression (RNA-seq)
			- RNA extraction (DataPLANT)
			- RNASeq assay (DataPLANT)
			- RNASeq computational analysis (DataPLANT)
			- ENA / GEO submission (DataPLANT)
    - metabolomics - Heidelberg
      - Metabolite_extraction (DataPLANT)
      - Metabolomics_MassSpec_assay (DataPLANT)
      - MetaboLights - Chromatography / Mass_spectrometry / Sample (DataPLANT)
      - Metabolomics_computational_analysis (DataPLANT)
      - MetaboLights - Data_transformation (DataPLANT)
      - MetaboLights submission (Metabolite abundance tables) (DataPLANT)
  - It was possible to identify also some templates that are not available and would be needed for the studies planned in GreenRobust, for example: ATAC-seq library preparation, ATAC-seq computational analysis, ATAC-seq ENA submission. Similarly, templates for single-cell sequencing will be needed (scRNA-seq, scATAC-seq, sciRNA-seq, sciATAC-seq).
  - A few draft templates (plant sowing and ATAC-seq computational analysis) were written and added to the [SWATE template registry repository](https://github.com/nfdi4plants/swate-template-registry/tree/main/templates/community/GreenRobust).
  - Making one ARC using ARCtrl where the complete process is added and linked with ontologies for plant species was also attempted.

