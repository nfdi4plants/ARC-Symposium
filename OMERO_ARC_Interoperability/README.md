#### Introduction

In this project we explore the interoperability between OMERO and ARC via RO-Crate. The project involves parsing an RO-Crate file from of an ARC and adding the necessary metadata(key-value pairs) with contextual metadata into OMERO as omero key-value pairs.

### Methodology

We first start with generating ro-crate metdata file in the json-ld format. This is usually created automatically in DataPLANT DATAHUB at the Deploy -> Package Registory -> isa_arc_json. The generated file i.e. arc-ro-crate-metadataOld.json was parsed with python's json package and read in omero webclient as key-value pair metadata. As there have been some changes in the ro-crate specification, here: [isa-ro-crate-profile](https://github.com/nfdi4plants/isa-ro-crate-profile/tree/release) , a new json-ld file named arc-ro-crate-metadataNew.json was generated and parsed using python.
