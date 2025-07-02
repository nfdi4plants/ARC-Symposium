#r "nuget: OBO.NET, 0.6.0"

open OBO.NET
open OboProvider

let [<Literal>] oboPath = @"OboProvider/some_go_terms.obo"

type go = OboTermsProvider<oboPath>

go.``adult scape``

go.``adult scape``.Synonyms
|> List.map (fun x -> x.Text)