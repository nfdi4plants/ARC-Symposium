---
authors:
  - name: Lukas Weil
    orcid: https://orcid.org/0000-0003-1945-6342
    affiliation: DataPLANT
  - name: Timo Mühlhaus
    orcid: https://orcid.org/0000-0003-3925-6778
    affiliation: DataPLANT
  - name: Jonathan Bauer 
    orcid: https://orcid.org/0000-0002-5624-2055
    affiliation: DataPLANT
  - name: Julian Weidhase
    orcid: https://orcid.org/0009-0005-7138-4763
    affiliation: DataPLANT
  - name: Jonas Lukasczyk
    orcid: https://orcid.org/0000-0001-6650-770X
    affiliation: DataPLANT
---

## Initial problem: 
Issue of consistency of ARCs published in Invenio. 

The publication middleware does not currently require for the ARC to be public to trigger a publication. Thus, users can publish private ARC, which results in the link-back to the DataHub to be only available for members of the ARC. 

There was a case of a user setting the ARC back to private after publishing which made the data unaccessible from the Publication page. Even if we would require ARCs to be public to allow a publication (which we don't want to!), it does not prevent the issue that a user can publish a public ARC and set it to private afterwards.

## Solution approach

- In theory, the publication represents a snapshop of the ARC
- RO-Crate contains all necessary metadata, can act as a full snapshot
- LFS Data blobs are present but not accessible without a link 
    - If all information necessary to retrieve the LFS files is in the RO-Crate we wouldn't need more


## Technical requirements

### Invenio

Invenio view plugin which has previews the RO-Crate metadata as a file tree and resolves the file references to storage

### ARCitect

ARCitect makes sure that all files referenced in the metadata are tracked by git LFS

### Representation in RO-Crate

FIles annotated in the RO-Crate MUST contain all information necessary to identify the LFS 

https://schema.org/MediaObject contains property `sha256`


# Solution Sketch

```mermaid
graph LR
    RO_Crate["RO-Crate
    ---------------------
    {Filename: ... }
    {SHA256: ... }
    ..."]
    Invenio["Invenio Plugin"]
    LFS["LFS-Resolver"]

    RO_Crate -->|Filename, OID| Invenio
    Invenio -->|SHA256| LFS
    LFS -->|Presigned S3-URL| Invenio
```

## Prototypical implementation

During the symposium we implemented a first prototype of a LFS object resolver micro-service.

https://github.com/nfdi4plants/lfs-object-resolver
