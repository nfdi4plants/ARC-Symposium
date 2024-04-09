## Main aim

The connections in the knowledge graph that represents the users domain(?), might not be fully representable in the format restrictions that arise from the underlying ARC knowledge graph. 
To tackle this, we want ways to enable the user extending the knowledge graph explicitly depicted by the format with his own connections. This mechanism should be sound in regard of RDF annotation principles. 

in short: make ARC more RDF complete 

## Concepts

- **RDF Blob** a user-definec json-ld file or online ressource which is in itself, a depiction of a concept that the user understands

- **(SPARQL) mapping** emphasizing and regrouping entities (classes and instances) of a user defined knowledge graph into different logical connections

- **(SPARQL) indexing** flattening of a knowledge graph into concepts and terms (consumable by ISA/ARC tools like Swate)

- **ARC RDF resolution** inclusion of referenced RDF-based knowledge when mapping from the ARC filesystem representation to the ARC RDF (json-ld/RO-Crate) representation

## Approaches

### RDF (Blob) reference approach

For this, we need to extend the ARC-specification in a way to allow unambiguous referencing of external **RDF object**, when the ARC is then converted to json-ld this RDF object needs to be put in the place it referenced from (i.e. resolved). THis approach is relatively straight forward programmatically, if an **RDF Blob** is referenced, as the tool does not need to have RDF-capabilities. On the other hand, this approach might give a bigger load on the user, as he needs to manage the creation of the **RDF Blob**. 
    
- How well does the RDF object integrate into the ARC knowledge graph
  - Invalid RDF -> fail
  - Low quality RDF (explanation needed)
  - High quality foreign RDF
  - High quality native RDF (close to ARC concepts)

### SPARQL(?)

In the SPARQL approach, we define ways to ingest knowledge from an existing knowledge graph using SPARQL.

Probably the most pressing questions for ingesting knowledge using SPARQL are:

    - Where do these SPARQL queries exist and when are they resolved?
    - Are they only part of the tooling, leading to the knowledge being included in some part of the ARC? 
    - Or, are the queries themselves stored, being resolved when converting to json-ld (e.g. on commit in the DataHub)? These would be kind of lazy columns.
