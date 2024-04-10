# FAIRagro middleware & search portal

The aim of these two small projects was to test the new Python transpiled version of the ARCtrl library for creating ARCs for the pull strategy of the FAIRagro middleware and developing roadmap for the next steps (1) and planning the integration of an ARC-based middleware in the FAIRagro central search service (2).


## (1) FAIRagro middleware
- currently the FAIRagro RDIs provide metadata dumps as JSON-LD files based on schema.org or own metadata format
- discussed potential solutions to build ARCs for all proviced datasets
- ARCtrl provides functionality to create ARCs out of JSON, but requires a RO-Crate JSON or at least ISA compliant JSON; will not work on schema.org dumps
    - need to integrate ARC contexts for the JSON dumps to make them compatible
    - therefore all RDIs need to support the same compliant JSON markup
    - will develop recommendation for this and share this as soon as possible with the RDI providers
    - e!DAL-PGP will act as prototype for testing, because we have direct access and can easily modify mark-up
- worked on the GitLab API for pushing ARCs into test instance


## (2) FAIRagro centra search service
- backgrounds:
	- basic metadata search functionality based on The Dataverse Project
	- further requirement: offering variable catalog searches (e.g. via Mica, as in NFDI4Health)
- got familiar with the ARC metadata registry search functions. Results:
	- due to its parameter searches, it may be a powerful replacement for Mica when the data comes from an ARC-based middleware
	- applicability depends on how much of the search requirements can be satisfied by contents of the metadata schema defined by FAIRagro TA3 (currently in development)
- tested the integration of ARC-JSON files in Dataverse. Details:
	- Dataverse uses a custom TSV-based format for defining metadata blocks, and for loading dataset metadata
	- converters from JSON and JSON-Schema to Dataverse-TSVs are available (from NFDI4Health)
	- converters were tested using ARC-JSON metadata and the ISA JSON Schema (unfinished as of 10.4., 11:00)
