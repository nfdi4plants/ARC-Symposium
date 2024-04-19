open ARCtrl.NET
open ARCtrl
open ARCtrl.ISA
open ARCtrl.QueryModel
open Argu


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
let mermaidGraphLR (i: string) (c : string list) = 
    [
        "# " + i
        ""
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

let arcProcesses2mermaid (arcpath: string) (outpath: string)  =

    // load ARC to data model
    let arc = ARC.load(arcpath)

    getEdges arc.ISA.Value.ArcTables
    |> List.append (getInvToStudyEdges arc.ISA.Value)
    |> List.append (collectSubGraphs arc.ISA.Value)
    |> mermaidGraphLR arc.ISA.Value.Identifier
    |> fun c -> System.IO.File.WriteAllLines(outpath, c)


type CliArguments =
    | [<AltCommandLine("-a")>][<Unique>] Arcpath of path:string
    | [<AltCommandLine("-o")>][<Unique>] Outfile of path:string

    interface IArgParserTemplate with
        member s.Usage =
            match s with
            | Arcpath _ -> "Specify path to an ARC"
            | Outfile _ -> "Specify a (text) file to write results to (Default: `processMermaid.md`)"

[<EntryPoint>]
let main(args) =

    let parser = ArgumentParser.Create<CliArguments>()

    let results = parser.Parse (args)

    match results.TryGetResult(CliArguments.Arcpath) with
    | Some i -> 
        match results.TryGetResult(CliArguments.Outfile) with
        | Some o -> 
            arcProcesses2mermaid i o
            1
        | None -> 
            let defaultOut = i + "/processMermaid.md"
            printfn "Outfile missing; Defaulting to %s inside the ARC" defaultOut
            arcProcesses2mermaid i defaultOut
            1
    | None ->
        printfn "Arcpath missing"
        0
