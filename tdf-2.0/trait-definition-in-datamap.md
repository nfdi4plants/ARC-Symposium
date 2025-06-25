# Trait Definition Files

---
- Category: Interoperability, Standardisation
- Platform: Data Map
- Status: EFO:0001795 ! in preparation
---

## Context
Within the Trait Definition File in MIAPPE we define what Observation Variable was recorded in a phenotyping experiment. The Observation Variable is build from a Trait (e.g. Plant Length or Flower Color), the Method (e.g. Measurement or Estimation) and the Scale (e.g. cm or 1:yellow;2:blue;3:red). This information needs to be available within the ARC. The Data Map expects the values to be annotated by an ontology. 

## Decision
We will annotate the result file using a Data Map. We will link the explication to an ontology term. If not available yet, we will provide a local file containing the ontology definition for the observation variables. 

### Data Map
In the Data Map, we will use the Parameter[Explication] defined term to specify the Observation Variable of an ontology. The observation variable needs to define its Scale. Depending on the data file structure the selector points to the cells containing the observation values. In the MIAPPE case, we will use a long format and every row in the assay points to a row in the data file.

### Local Ontology File
We will use a local .obo formated ontology, if there exists no ontology where the scale is sufficiently described. This ontology should describe the Trait, the Method and the Scale refer to by a Observation Variable through has_trait, has_method and has_scale relationships. If the scale is categorical, the Scale will link through a has_scale_item relationship to the key value pairs coding the valid values.

## Consequences
There is a trade-off between using wide and long data formats. While the wide format, where variables are represented as columns, is generally easier to annotate, it can result in the loss of important information such as observation timestamps, which are essential for error tracing. To prevent this, it is important to ensure that such metadata is preserved. Additionally, although the long (verbose) format may appear more complex, it enables the generation of concise, aggregated views of the data file, making it easier to summarize and analyze the observations. By allowing local ontologies, we keep the style of referencing ontology terms while allowing users to keep flexibility to define their custom traits and scales.

## Automation
We need to implement a validation package for the MIAPPE standard, checking for the existence of a trait-definition ontology referenced in the data map for the output column in an assay. Upon full compliance, the MIAPPE compliant badge will be displayed.