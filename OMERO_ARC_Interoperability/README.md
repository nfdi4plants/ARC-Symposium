---
authors:
  - name: Niraj Kandpal
    orcid: 0009-0007-5101-4786
    affiliation: 1
  - name: Heinrich Lukas Weil
    affiliation: 2
    orcid: 0000-0003-1945-6342
  - name: Kevin Schneider
    affiliation: 2
    orcid: 0000-0002-2198-5262
  - name: Manual Feser
    affiliation: 3
    orcid: 0000-0001-6546-1818

affiliations:
  - name: CECAD Imaging Facility, University of Cologne, Cologne, Germany
    index: 1
  - name: Computational Systems Biology, University of Kaiserslautern-Landau, Kaiserslautern, Germany
    index: 2
  - name: Leibniz-Institut für Pflanzengenetik und Kulturpflanzenforschung (IPK) Seeland, Sachsen-Anhalt, DE
    index: 3
  

---


### Introduction

In this project we explore the interoperability between [OMERO](https://www.openmicroscopy.org/omero/) and [ARC](https://nfdi4plants.github.io/nfdi4plants.knowledgebase/core-concepts/arc/) via RO-Crate. The project involves parsing an RO-Crate file from of an ARC and adding the necessary metadata(key-value pairs) with contextual metadata into OMERO as omero key-value pairs. Here we explore simple prototype/workflow to achieve this interoperability.

### Methodology

We first start with generating ro-crate metdata file in the json-ld format. This is usually created automatically in DataPLANT DATAHUB at the Deploy -> Package Registory -> isa_arc_json. The generated file i.e. *arc-ro-crate-metadataNew.json* was read & isa investigation key-values were extracted with python's json package and read in omero webclient as key-value pair metadata using python's omero-py package. 

### Attached Files
1. **arc-ro-crate-metadataNew.json** : This is the json-ld output file for an ARC named [LarvaeDrosophila](https://git.nfdi4plants.org/NKandpal/LarvaeDrosophila) in DataPLANT's dataHUB. It contains investigation, study and assay metadata and contextual information.
2. **ReaderjsonNew.py** : This is a python script that opens and reads the *arc-ro-crate-metadata.json* file using python's json library, it then extracts the investigation metadata values. Here, in this script we also try to compare and resolve the keys with isa.investigation.xlsx. In the end the script prints the metadata as key-value pairs.
3. **arc-ro-crate-metadataOld.json** : This is the older version of *arc-ro-crate-metadataNew.json* above.
4. **ReaderjsonOld.py** : This script opens and reads *arc-ro-crate-metadataOld.json* file similar to *ReaderjsonNew.py*. Additionaly it writes the metadata in omero-webclient using omero-py library.
5. **OMERO_KV_pairs.png** : This is simply a screenshot of metadata written in omero-weblcient using *ReaderjsonOld.py* script.



### Results and Limitations

Reading and extracting metdata from the json-ld file *arc-to-ro-crate-metdataNew.json* worked as expected when compared with isa.investigation.xlsx metadata and specific metadata for investigation was read/extracted and uploaded into omero as can be seen in the image file *OMERO_KV_pairs.png*. Reading/Extracting the contextual metadata and adding it as metadata namespaces in OMERO was also on of the goals which needs to be further explored.
The json-ld file *arc-to-ro-crate-metdataNew.json* was read using python with json library to extract the metadata. Except confusion regarding few keys like *Term Source Name* and *Investigation Publication Status Term Source REF* for investigation metadata, this worked as expected. The contextual information about the metatadata still need to be extracted and represented in omero webclient as key-value pairs with namespaces.

### Future Work

Future works involves parsing the *arc-to-ro-crate-metdataNew.json* file, both key-value metdata and contextual information for investigation, study & assays metadata and adding them to omero webclient metadata. The intented goal will be to attain interoperability between OMERO and ARC using RO-Crate metadata. 

### Miscellaneous

Inside the folder you might find files and scripts with Old and New in the end of their names. This is due to the fact that there were changes in the [ISA RO-Crate profile](isa-ro-crate-profile](https://github.com/nfdi4plants/isa-ro-crate-profile/tree/release) and the files with Old ending represent the Older version and the files with New ending represent the newer version.

