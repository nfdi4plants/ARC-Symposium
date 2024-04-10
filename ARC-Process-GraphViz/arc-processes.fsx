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

let pullProcessInfoFunctionIntoSeriesOfValues (table: ArcTable) (f: ArcTable -> string list) = 
    f table
    |> Series.ofValues

let processTable = 
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
