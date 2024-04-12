// Script to write a minimal markdown file with a mermaid graph
// that displays an ARC's connections of ISA processes
// from ARC investigation through studies and assays

// Dependencies

// #r "nuget: ARCtrl.NET, 1.1.0"
// #r "nuget: ARCtrl.QueryModel, 1.0.5"

open ARCtrl.NET
open ARCtrl
open ARCtrl.ISA
open ARCtrl.QueryModel

// Load ARC
let datahubPath = "/Users/dominikbrilhaus/datahub-dataplant/"

let arcInHubPath = "ARC-Process-GraphViz-Example"
let arcPath = datahubPath + arcInHubPath
let arc = ARC.load(arcPath)

// Test wether one process precedes another
// based on min 1 intersecting Input/Output reference

let isPreviousProcessOf (processA: ArcTable) (processB: ArcTable) : bool = 
    Set.intersect (set processA.OutputNames) (set processB.InputNames)
    |> Seq.length
    |> fun x -> x > 0

// Write assay processes to a mermaid subgraph (only nodes, no edges)

let assayToSubgraph (assay: ArcAssay) : string list =
    [
        sprintf "subgraph %s" assay.Identifier
        for p in assay do
            "  " + p.Name        
        "end"
        ""
    ]

// Write study processes to a mermaid subgraph (only nodes, no edges)

let studyToSubgraph (study: ArcStudy) : string list =
    [
        sprintf "subgraph %s" study.Identifier
        for p in study do
            "  " + p.Name        
        "end"
        ""
    ]

// Wrap strings in a left-to-right mermaid graph
let mermaidGraphLR (c : string list) = 
    [
        "```mermaid"
        ""
        "graph LR"
        ""
        yield! c
        "```"
    ]

// Collect all studies and assays of an ARC as mermaid subgraphs
let collectSubGraphs (inv : ArcInvestigation) : string list = 
    [
        for study in inv.Studies do
            yield! studyToSubgraph study
        for assay in inv.Assays do
            yield! assayToSubgraph assay
        ""
    ]

// Get process-to-process edges for mermaid
let getEdges (processes : ArcTables) : string list =
    [
        for p1 in processes do
            for p2 in processes do

                if isPreviousProcessOf p1 p2 then
                    sprintf "%s --> %s" p1.Name p2.Name
        ""
    ]
    
// Get investigation-to-study edges for mermaid
let getInvToStudyEdges (inv : ArcInvestigation) : string list = 
    [
        for s in inv.Studies do
            sprintf "%s --> %s" inv.Identifier s.Identifier
        ""
    ]

// Put everything together and locally write to markdown in that ARC

getEdges arc.ISA.Value.ArcTables
|> List.append (getInvToStudyEdges arc.ISA.Value)
|> List.append (collectSubGraphs arc.ISA.Value)
|> mermaidGraphLR
|> fun c -> System.IO.File.WriteAllLines(arcPath + "/arc-processes-mermaid.md", c)
