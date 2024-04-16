
# ARC Process GraphViz

- [Example ARC](#example-arc)
- [Goal](#goal)
  - [Level 1 ("ISA registration" Level)](#level-1-isa-registration-level)
  - [Level 2 ("Process" Level)](#level-2-process-level)
  - [Level 3 ("Sample / data item" Level)](#level-3-sample--data-item-level)
- [Code base](#code-base)
- [Viz ideas](#viz-ideas)
- [Additional / Future](#additional--future)
- [Data ingest](#data-ingest)
- [Node-edge table](#node-edge-table)
- [Assumptions / challenges](#assumptions--challenges)
- [Model notes](#model-notes)
- [Setup (ana)conda for python scripts](#setup-anaconda-for-python-scripts)


## Example ARC

For test purposes

https://git2.nfdi4plants.org/brilator/ARC-Process-GraphViz-Example


## Goal

- Visualize flow of (experimental) samples / processes in an ARC
  - Sample-to-sample-to-data(-to-result)
- List studies and assays of an ARC
  1. Detail 1: Which assay is linked to which study?
  2. Detail 2: Which sample goes through which study (processes) and assay (processes) (to which workflow)
- Interactive (add remove complexity, detail)

### Level 1 ("ISA registration" Level)

```mermaid
graph LR

i["ARC(Investigation)"]
s1["study 1"]
s2["study 2"]
s3["study 3"]

a1["assay 1"]
a2["assay 2"]
a3["assay 3"]

i --> s1
i --> s2
i --> s3

s1 --> a1
s2 --> a2
s2 --> a3
s3 --> a3
```

### Level 2 ("Process" Level)

```mermaid
graph LR

i["ARC(Investigation)"]

subgraph s1["study 1"]
  p1 --> p2   
end

subgraph s2["study 2"]
  p3 --> p4   
end

subgraph s3["study 3"]
  p5 --> p6   
end

p2 --> p7

subgraph a1["assay 1"]
  p7 --> p8   
end

subgraph a2["assay 2"]
  p9 --> p10
end

subgraph a3["assay 3"]
  p11 --> p12  
end

i --> s1
i --> s2
i --> s3

p4 --> p9
p4 --> p11
p6 --> p11
```

### Level 3 ("Sample / data item" Level)

```mermaid
graph LR

i["ARC(Investigation)"]

i --> s1
i --> s2

subgraph s1["study 1"]
  subgraph pA["processA"]
    sample1 --> sample1-A
    sample2 --> sample2-A
    sample3 --> sample3-A
  end

  subgraph pB["processB"]
    sample1-A --> sample1-B
    sample2-A --> sample1-B
    sample3-A --> sample1-B
  end
end

subgraph s2["study 2"]
  subgraph pC["processC"]
    sample4 --> sample4-C
    sample5 --> sample5-C
    sample6 --> sample6-C
    sample7 --> sample7-C
    sample8 --> sample8-C
    sample9 --> sample9-C
  end

  subgraph pD["processD"]
    sample4-C --> sample4-D
    sample5-C --> sample5-D
    sample6-C --> sample6-D
  end
  subgraph pE["processE"]
    sample7-C --> sample7-E
    sample8-C --> sample8-E
    sample9-C --> sample9-E
  end
end

subgraph a2["assay 2"]
  subgraph pF["processF"]
    sample4-D --> sample4-F
    sample5-D --> sample5-F
    sample6-D --> sample6-F
  end
end

subgraph w1["workflow 1"]
  subgraph r1["run1"]
    sample4-F --> dataFile1
    sample5-F --> dataFile1
    sample6-F --> dataFile1
  end
end
```

## Code base

1. Read / wrangle ARC metadata model
   1. ARCtrl - read ARC
   2. find overlapping samples between ISA processes
2. Visualize / Graph
   1. Cytoscape, Cy.js
   2. Obsidian
   3. sankey diagram
   4. Plotly / Plotly-Cytoscape

## Viz ideas

- directed acyclic graph
- Nodes = sample / data items
  - edges = processes
- nodes = Study / Assay
  - subnode = StudyProcesses / AssayProcesses
    - subsubnode = Sample
- edge-size
  - map to number of samples
- display contributor info
  - ISA contacts
  - git blame

## Additional / Future

- computational workflows

## Data ingest

1. Read ARC
2. List processes (ignore whether study or assay)
3. List input / output IDs (sample / data items)
4. Find overlapping items
5. Assign process


## Node-edge table

input | process | output
------|---------|-------
sample0 | study1:processA | sample0-A
sample1 | study1:processA | sample1-A
sample2 | study1:processA | sample2-A
sample0-A | study1:processB | sample0-B
sample1-A | study1:processB | sample1-B
sample2-A | study1:processB | sample2-B
sample4 | study2:processC | sample4-C
sample5 | study2:processC | sample5-C
sample6 | study2:processC | sample6-C
sample7 | study2:processC | sample7-C
sample8 | study2:processC | sample8-C
sample9 | study2:processC | sample9-C
sample4-C | study2:processD | sample4-D
sample5-C | study2:processD | sample5-D
sample6-C | study2:processD | sample6-D
sample7 | study2:processE | sample7-E
sample8 | study2:processE | sample8-E
sample9 | study2:processE | sample9-E
sample4-D | assay2:processF | sample4-F
sample5-D | assay2:processF | sample5-F
sample6-D | assay2:processF | sample6-F

## Assumptions / challenges

1. unique IDs
2. relative paths / references across the ARC studies / assays
3. process names
   1. fallback: sheet name of study / assay workbooks
   2. additional detail: Protocol REF



## Model notes

trying to model / keep notes of what to display where


```mermaid

classDiagram
    
direction TD

    investigation --> "0..n" study
    study --> "0..n" assay
    assay --> "0..n" workflow

    process "0..n" --* study
    process "0..n" --* assay

    inputNode "1" -- process
    process --> "1" outputNode

    inputNode <-- "0..n" inputItem
    outputNode <-- "0..n" outputItem

    inputItem -- outputItem

    class inputItem {
        label = 
    }

    class outputItem {
        label = 
    }

    class study {
        label = studyIdentifier
        + mapFill() <= StudyOrAssayOrWorkflow
        + mapOnClickLink() => link to study (Folder)
        + mapOnClickUnfold() => show processes
    }

    class assay {
        label = assayIdentifier
        + mapFill() <= StudyOrAssayOrWorkflow
        + mapOnClickLink() => link to assay (Folder)
        + mapOnClickUnfold() => show processes
    }

    class process {
        label = processTableName
        additional label = Protocol REF
        + mapLineSize() <= numberOfProcessedSamples (rowCount)
        + mapOnClickLink() => link to Protocol REF (File)
        + mapOnClickUnfold() => show InputOutput Nodes
    }

    class inputNode {
        label = inputNode Name
        + mapFill() <= inputType     
    }

    class outputNode {
        label = outputNode Name
        + mapFill() <= outputType     
    }

    class people{
        + Investigation Contacts
        + Study Contacts
        + Assay Performers
}


style investigation fill: #2D3E50,color:#ECEBEB;
style study fill: #B4CE82
style assay fill: #FFC000
style process fill: #4FB3D9
    
```

## Setup (ana)conda for python scripts

1. Store as `environment.yml`:

```yml
name: arc-process-graph
channels:
  - defaults
dependencies:
  - pip
  - python=3.12
  - pip:
    - arctrl
    - fsspreadsheet
    - dash
    - dash_cytoscape
```

2. Create conda environment

```bash
conda env create -f environment.yml
```

3. Activate conda environment

```bash
conda activate arc-process-graph
```

4. Deactivate conda environment

```bash
conda deactivate arc-process-graph
```
