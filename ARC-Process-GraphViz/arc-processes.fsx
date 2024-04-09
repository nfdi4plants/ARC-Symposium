#r "nuget: ARCtrl.NET, 1.1.0"

open ARCtrl.NET
open ARCtrl
open ARCtrl.ISA

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