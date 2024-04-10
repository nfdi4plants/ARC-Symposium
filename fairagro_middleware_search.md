# FAIRagro middleware & search portal

The aim of these two small projects was to test the new Python transpiled version of the ARCtrl library for creating ARCs for the pull strategy of the FAIRagro middleware and developing roadmap for the next steps (1) and getting familiar with the ARC metadata registry as data basis for the FAIRagro search portal (2).


## (1) FAIRagro middleware
- currently the FAIRagro RDIs provide metadata dumps as JSON-LD files based on schema.org or own metadata format
- discussed potential solutions to build ARCs for all proviced datasets
- ARCtrl provides functionality to create ARCs out of JSON, but requires a RO-Crate JSON or at least ISA compliant JSON; will not work on schema.org dumps
    - need to integrate ARC contexts for the JSON dumps to make them compatible
    - therefore all RDIs need to support the same compliant JSON markup
    - will develop recommendation for this and share this as soon as possible with the RDI providers
    - e!DAL-PGP will act as prototype for testing, because we have direct access and can easily modify mark-up
- worked on the GitLab API for pushing ARCs into test instance


## (2) FAIRagro search portal
