#r "nuget: ARCtrl.NET, 1.1.0"
#r "nuget: ARCtrl.QueryModel, 1.0.5"

open ARCtrl.NET
open ARCtrl
open ARCtrl.ISA
open ARCtrl.QueryModel

let datahubPath = "/Users/dominikbrilhaus/datahub-dataplant/"
let arcInHubPath = "ARC-Process-GraphViz-Example"
let arcPath = datahubPath + arcInHubPath
let arc = ARC.load(arcPath)

let table1 = arc.ISA.Value.ArcTables[0]
let table2 = arc.ISA.Value.ArcTables[1]


let isPreviousProcessOf (processA: ArcTable) (processB: ArcTable) : bool = 
    Set.intersect (set processA.OutputNames) (set processB.InputNames)
    |> Seq.length 
    |> fun x -> x > 0

isPreviousProcessOf table1 table2


let assayToSubgraph (assay: ArcAssay) : string list =
    [
        sprintf "subgraph %s" assay.Identifier
        for p in assay do
            "\t" + p.Name        
        "end"
    ]
    
let studyToSubgraph (study: ArcStudy) : string list =
    [
        sprintf "subgraph %s" study.Identifier
        for p in study do
            "\t" + p.Name        
        "end"
    ]

let mermaidGraphLR (c : string list) = 
    [
        "```mermaid"
        "graph LR"
        yield! c
        "```"
    ]

let assay1 = arc.ISA.Value.Assays[0]
let study1 = arc.ISA.Value.Studies[0]

let collectSubGraphs (inv : ArcInvestigation) : string list = 
    [
        for study in inv.Studies do
            yield! studyToSubgraph study
        for assay in inv.Assays do
            yield! assayToSubgraph assay
    ]

let getEdges (processes : ArcTables) : string list =
    [
        for p1 in processes do
            for p2 in processes do

                if isPreviousProcessOf p1 p2 then
                    sprintf "%s --> %s" p1.Name p2.Name
    ]


getEdges arc.ISA.Value.ArcTables
// |> fun sg -> sg @ getEdges arc.ISA.Value.ArcTables
|> List.append (collectSubGraphs arc.ISA.Value)
|> mermaidGraphLR
|> fun c -> System.IO.File.WriteAllLines("./test.md", c)





    

