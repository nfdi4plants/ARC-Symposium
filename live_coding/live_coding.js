import { XlsxController, ArcStudy, ArcInvestigation, JsonController } from "@nfdi4plants/arctrl";
import {Xlsx} from "@fslab/fsspreadsheet";
import fs from "fs";
import path from "path";

async function main() {
    const fswb = await Xlsx.fromXlsxFile("./assay.xlsx");
    const assay = XlsxController.Assay.fromFsWorkbook(fswb);
    console.log(assay);
    const study = ArcStudy.init("My super Study");
    const investigation = ArcInvestigation.init("My interesting Investigation");
    investigation.AddStudy(study);
    study.AddRegisteredAssay(assay);
    const json = JsonController.Investigation.toROCrateJsonString(investigation);
    fs.writeFileSync("./ro_crate.json", json);
}

main()