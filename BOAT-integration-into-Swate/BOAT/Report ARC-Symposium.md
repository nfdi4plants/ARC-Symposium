# General workload in the ARC Symposium 2026

-Helping out in the new Electron [Swate](https://github.com/nfdi4plants/Swate/tree/epic/SwateApp) App (ARCitect) by doing style adjustments and erasing small bugs.
-Improving the view and look-and-feel mechanic in the [Provenace Table Editor](https://github.com/nfdi4plants/Swate/tree/feature/TableEditor) in Swate, alongside with [Caroline Ott](https://github.com/caroott).
- Setting up the components of [BOAT](https://github.com/nfdi4plants/Swate/tree/feature/BOATAddon) in the Swate playground and adjusting the Swate styling to be integrated into the Electron Swate App.

In more detail:

## Electron Swate App
Small bugs, such as a markdown editor for the Note components, were adjusted to maintain a stable, uniform height view. A background bug, which caused the background to change color if a certain height was reached in the markdown editor, was fixed. Found and reported further issues.

## Provenance Tool
Look-and-feel mechanics, such as multiple tooltips and button highlighting, were integrated. In addition, confusing and unnecessary highlighting and bordering of elements were removed.

## Integration of BOAT into Swate
As a main project of the ARC-Symposium 2026, I took the elements of my own BOAT tool, already part of the DataPLANT (link)environment, and turned them into usable components for the Electron Swate App. They're not integrated into the Swate App yet, due to time constraints, but can be used in the playground inside the components and will be integrated into the Swate App as the next step. [This folder](https://github.com/Rookabu/Integrate-BOAT-into-Swate-environment/tree/BOAT-Integration/BOAT-integration-into-Swate/BOAT) contains all the new files created inside the the [Components](https://github.com/nfdi4plants/Swate/tree/feature/BOATAddon/src/Components/src/Page/BOAT) of Swate.