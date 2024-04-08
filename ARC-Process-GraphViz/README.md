---
# marp: true
headingDivider:
- 1
- 2
- 3
---

# ARC Process GraphViz

## Example ARC

For test purposes

https://git.nfdi4plants.org/brilator/ARC-Process-GraphViz-Example


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
   3. Plotly


## Viz ideas

- directed acyclic graph
- nodes = Study / Assay
  - subnode = StudyProcesses / AssayProcesses
    - subsubnode = Sample
- Nodes = sample / data items
  - edges = processes


## Additional / Future

- computational workflows

