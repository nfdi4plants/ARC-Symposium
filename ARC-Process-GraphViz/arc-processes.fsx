#r "nuget: ARCtrl.NET, 1.1.0"
#r "nuget: ARCtrl.QueryModel, 1.0.5"
#r "nuget: Deedle, 3.0.0-beta.1"

open Deedle

do fsi.AddPrinter(fun (printer:Deedle.Internal.IFsiFormattable) -> "\n" + (printer.Format()))

open ARCtrl.NET
open ARCtrl
open ARCtrl.ISA
open ARCtrl.QueryModel

let datahubPath = "/Users/dominikbrilhaus/datahub-dataplant/"
let arcInHubPath = "ARC-Process-GraphViz-Example"

let arcPath = datahubPath + arcInHubPath

let arc = ARC.load(arcPath)

// arc.ISA
let i = arc.ISA.Value

let assayTables = 
    [for assay in i.Assays do
        for table in assay.Tables do
            table, assay.Identifier, "a"]
            
let studyTables = 
    [for study in i.Studies do
        for table in study.Tables do
            table, study.Identifier, "s"]
        
let allTables = 
    List.append assayTables studyTables

allTables
|> List.map (fun (t, id, assayOrStudy) -> t.Values)

allTables
|> List.map (fun (t, id, assayOrStudy) -> t.TryGetInputColumn())

// let Inputs = 
//     allTables
//     |> List.choose (fun (t, id, assayOrStudy) -> t.TryGetInputColumn())

let inputs = 
    allTables
    |> List.choose (fun (t, id, assayOrStudy) -> 
        t.TryGetInputColumn() 
        |> Option.map (fun o -> {|column = o; id = id; assayOrStudy = assayOrStudy; tableName = t.Name|})
    )
    |> List.collect (fun o ->
        o.column.Cells
        |> Array.map (fun c -> 
            {|cell = c.AsFreeText; id = o.id; assayOrStudy = o.assayOrStudy; tableName = o.tableName|})
        |> List.ofArray
    )

let outputs = 
    allTables
    |> List.choose (fun (t, id, assayOrStudy) -> 
        t.TryGetOutputColumn() 
        |> Option.map (fun o -> {|column = o; id = id; assayOrStudy = assayOrStudy; tableName = t.Name|})
    )
    |> List.collect (fun o ->
        o.column.Cells
        |> Array.map (fun c -> 
            {|cell = c.AsFreeText; id = o.id; assayOrStudy = o.assayOrStudy; tableName = o.tableName|})
        |> List.ofArray
    )

// let outputs = 
//     allTables
//     |> List.choose (fun (t, id, assayOrStudy) -> t.TryGetOutputColumn() |> Option.map (fun o -> o, id, assayOrStudy))

let matches = 
    inputs
    |> List.map (fun i -> 
        i, outputs |> List.filter (fun o -> o.cell = i.cell)
    )




arc.ISA.Value.StudyIdentifiers

arc.ISA.Value.AssayIdentifiers

arc.ISA.Value.Assays


let nodes = arc.ISA.Value.ArcTables.Nodes

nodes
|> Array.ofSeq
|> Array.map (fun x -> x.Name)
// |> fun x -> x.[2]

arc.ISA.Value.ArcTables.LastNodes.Count
arc.ISA.Value.ArcTables.FirstNodes.Count
arc.ISA.Value.ArcTables.Nodes.Length


let arcTables = arc.ISA.Value.ArcTables

let arcProcesses = arc.ISA.Value.ArcTables.GetProcesses()

arc.ISA.Value.ArcTables.TableNames

arc.ISA.Value.ArcTables.Tables[1].InputNames


arc.ISA.Value.ArcTables.Tables[1].OutputNames


arc.ISA.Value.ArcTables.Tables[1].InputNames.ToString()



// 


let pullProcessInfoFunctionIntoSeriesOfValues (table: ArcTable) (f: ArcTable -> string list) = 
    f table
    |> Series.ofValues

[for table in arc.ISA.Value.ArcTables.Tables do
    [
        "inputs", pullProcessInfoFunctionIntoSeriesOfValues table (fun table -> table.InputNames)
        "outputs", pullProcessInfoFunctionIntoSeriesOfValues table (fun table -> table.OutputNames)
        "process", pullProcessInfoFunctionIntoSeriesOfValues table 
            (fun (table:ArcTable) -> List.init table.RowCount (fun _ -> table.Name))
        "inputType", pullProcessInfoFunctionIntoSeriesOfValues table 
            (fun (table:ArcTable) -> List.init table.RowCount (fun _ -> table.InputType.ToString()))
        "outputType", pullProcessInfoFunctionIntoSeriesOfValues table 
            (fun (table:ArcTable) -> List.init table.RowCount (fun _ -> table.OutputType.ToString()))
    ]
    |> Frame.ofColumns
]



// let inputNames1 = Series.ofValues arc.ISA.Value.ArcTables.Tables[1].InputNames
// let outputNames1 = Series.ofValues arc.ISA.Value.ArcTables.Tables[1].OutputNames


let processNamesSeries = 
    List.init
        arc.ISA.Value.ArcTables.Tables[1].InputNames.Length
        (fun x -> arc.ISA.Value.ArcTables.Tables[1].Name)
    |> Series.ofValues
    
let inputTypeSeries = 
    List.init
        arc.ISA.Value.ArcTables.Tables[1].InputNames.Length 
        (fun x -> arc.ISA.Value.ArcTables.Tables[1].InputType.ToString())
    |> Series.ofValues
    
let outputTypeSeries = 
    List.init
        arc.ISA.Value.ArcTables.Tables[1].InputNames.Length 
        (fun x -> arc.ISA.Value.ArcTables.Tables[1].OutputType.ToString())
    |> Series.ofValues

let table1 = 
    Frame.ofColumns [
        "inputs", inputNames1;
        "outputs", outputNames1;
        "process", processNamesSeries;
        "inputType", inputTypeSeries;
        "outputType", outputTypeSeries
    ]


"inputs", 
"outputs", 
"process", 
"inputType", 
"outputType", 





