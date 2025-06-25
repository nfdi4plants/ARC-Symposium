# SQL_to_ARC

As part of the NFDI FAIRagro project, Measure 4.2 aim to connect several, heterogenous Research Data Infrastructures (RDI) with a common, integrated middleware that is
ARC / Datahub-based. Therefore the differnet RDIs and their used metadata formats needs to be homogenized.
To reduce the effort for the differente RDI providers and to keep their autonomy we to tackle the integration by implementing a generic approach ("SQL-to-ARC") that creates the needed ARCs based on the original relational structure of the databases in the backend of the RDIs

## Outline of the SQL-to-ARC converter

We assume to have access to the RDI's SQL database. We create new views in that database
that correspoond to entities within the ARC context. E.g:

* ARC_investigation
* ARC_study
* ARC_assay
* ARC_person
* ARC_sample
* ARC_sample_characteristic

Then we use an ARCtrl-based software (written in python) to perform the actual conversion.
The prototype can be found here: git@github.com:fairagro/m4.2_SQLToARC.git (currently private).

RoadMap / Next Steps

* [Carsten](https://github.com/Zalfsten) will set-up repo in FAIRagrio GitHub to develop ontology linkage
* invite [Jorge](https://github.com/jorgitogb) und [Lukas](https://github.com/HLWeil) to support
* idea: 
  * read ARC (arctrl) to create obo file
  * curate obo file (set x-ref and add terms from existing ontologies)
  * read updated obo file back into ARC (arctrl)
