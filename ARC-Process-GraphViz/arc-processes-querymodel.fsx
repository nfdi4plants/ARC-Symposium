// temp
#r "nuget: ARCtrl"
#r "nuget: ARCtrl.NET, 1.0.5"
#r "nuget: ARCtrl.QueryModel, 1.0.5"

open ARCtrl
open ARCtrl.NET
open ARCtrl.QueryModel

let arc = 
    ARC.load (__SOURCE_DIRECTORY__ + "/../")

let qi = 
    arc.ISA.Value

type InOutMapping = {
    In: string
    Out: string
    Process:string
    }

let inOutMappings = 
    qi.ArcTables.Tables
    |> Array.ofSeq
    |> Array.map (fun p -> 
        p.Rows 
        |> List.map (fun r -> r.Input, r.Output)
        |> List.distinct
        |> List.map (fun x -> {In = fst x; Out = snd x; Process = p.Name})
        |> Array.ofSeq
        ) 
    |> Array.concat 

type ProcessToProcess = {
    InProcess : string
    OutProcess : string
    }

let InputToProcessLookUp = 
    inOutMappings
    |> Array.map (fun x -> x.In,x.Process)
    |> Map.ofArray

let processToProcess =
    inOutMappings
    |> Array.choose (fun x -> 
            match InputToProcessLookUp |> Map.tryFind x.Out with 
            | Some outPutProcess ->  
                Some {InProcess=x.Process;OutProcess=outPutProcess}
            | None -> None
            
        )
    |> Array.distinct

