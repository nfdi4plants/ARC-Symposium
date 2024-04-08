#r "nuget: ARCtrl, 2.0.0-alpha.2"
#r "nuget: FsSpreadsheet.Net, 6.1.0"

open ARCtrl

// init table on study
let growth = ArcTable.init("Growth")

// create ontology annotation for "species"
let oa_species =
    OntologyAnnotation(
        "species", "GO", "GO:0123456"
    )
// create ontology annotation for "chlamy"
let oa_chlamy = 
    OntologyAnnotation(
        "Chlamy", "NCBI", "NCBI:0123456"
    )

// append first column to table. 
// This will create an input column with one row cell.
// In xlsx this will be exactly 1 column.
growth.AddColumn(
    CompositeHeader.Input IOType.Source,
    [|CompositeCell.createFreeText "Input1"|]
)

growth.AddColumn(
    CompositeHeader.Output IOType.Sample,
    [|CompositeCell.createFreeText "Outpu1"|]
)

// append second column to table. 
// this will create an Characteristic [species] column with one row cell.
// in xlsx this will be exactly 3 columns.
growth.AddColumn(
    CompositeHeader.Characteristic oa_species, 
    [|CompositeCell.createTerm oa_chlamy|]
)

let assay = ArcAssay.init("My awesome Assay")

assay.AddTable(growth)

let kevin = Person(firstName="Kevin",lastName="Frey")
assay.Performers.Add(kevin)
let fswb = XlsxController.Assay.toFsWorkbook(assay)

open FsSpreadsheet.Net

fswb.ToXlsxFile("./assay.xlsx")