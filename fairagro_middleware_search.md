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

### schema.org to ARC #

[ARCCtrl](https://github.com/nfdi4plants/ARCtrl/tree/update_docs_v2) can deal with JSON-LD representations of ARCs that are compatible to [ISA](https://isa-specs.readthedocs.io/en/latest/) as used within the ARCs. In principle ARC investigations, studies and assays correspond and can be converted to [schema.org datasets](https://schema.org/Dataset). The other way round is not as simple as the ARC metadata scheme does not support all dataset features.

The principle approach to convert schema.org JSON-LD to ARC is:

* take the JSON-LD and [expand](http://niem.github.io/json/reference/json-ld/expanded/) it
* use the ARC-specfic JSON-LD context to compact the JSON-LD again
* import this JSON-LD into ARCCtrl

The python code would look like this:

```python
from pyld import jsonld
from arctrl.arctrl import JsonController
import json

with open('dataset.jsonld', 'r') as f:
    dataset = json.loads(f.read())

with open('context.jsonld', 'r') as f:
    context = json.loads(f.read())

expanded = jsonld.expand(dataset)
compacted = jsonld.compact(expanded, context)

arc = JsonController.Investigation().from_json_string(compacted)
```

Dealing with unsupported schema.org dataset features requires some effort. There are two approaches:

* The preferred approach is to require all schema.org JSON-LD files that are processed by the FAIRagro middleware to conform to the [ARC profile](https://github.com/nfdi4plants/isa-ro-crate-profile/blob/main/profile/isa_ro_crate.md).
* In case the first approach is not possible or takes too much time, there is the possibility to sanitize JSON-LD file before importing them, i.e. replacing all unsupported features by supported ones. This requires JSON-LD transformation which could be done, e.g., with [SPARQL](https://en.wikipedia.org/wiki/SPARQL) -- using `INSERT` and `DELETE` statements.

An example for schema.org <-> ARC imcompatibilities:

A valid schema.org person:

```yaml
{
    "@context": "http://schema.org",
    "@type": "Person",
    "address": {
        "@type": "PostalAddress",
        "addressCountry": "Germany",
        "addressLocality": "Musterstadt",
        "postalCode": "12345",
        "streetAddress": "Maxstraße 42"
    },
    "familyName": "Musterfrau",
    "givenName": "Erika",
    "name": "Erika Musterfrau"
}
```

ARC compatible version:

```yaml
{
    "@context": {
        "@vocab": "http://schema.org/"
    },
    "@type": "Person",
    "address": "Maxstraße 42\n12345 Musterstadt\nGermany"
    "familyName": "Musterfrau",
    "givenName": "Erika",
}
```

The differences are:

* The context definition: the context URI needs to end in '/' and has to be specified as `@vocab` field. Note: in fact this is no requirement by ARCtrl but by PyLD, the python JSON-LD library we are currently using.
* The address field: schema.org allows to use the type `PostalAddress`, but ARC does only support a simple string.
* The name field: it's not supported by ARC (, but if present, it will be ignored by ARCCtrl). 



## (2) FAIRagro central search service
- backgrounds:
	- basic metadata search functionality based on The Dataverse Project
	- further requirement: offering variable catalog searches (e.g. via Mica, as in NFDI4Health)
- got familiar with the ARC metadata registry search functions. Results:
	- due to its parameter searches, it may be a powerful replacement for Mica when the data comes from an ARC-based middleware
	- applicability depends on how much of the search requirements can be satisfied by contents of the metadata schema defined by FAIRagro TA3 (currently in development)
- tested the integration of ARC-JSON files in Dataverse. Details:
	- Dataverse uses a custom TSV-based format for defining metadata blocks, and for loading dataset metadata
	- converters from JSON and JSON-Schema to Dataverse-TSVs are available (from NFDI4Health)
	- as a proof-of-concept, converters were used to load parts of the ISA JSON Schema as a Dataverse metadata block, and ARC-JSON metadata as a corresponding Dataverse dataset.
