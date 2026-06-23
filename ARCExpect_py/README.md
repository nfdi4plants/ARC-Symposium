---
title: 'ARCExpect python library'
tags:
  - ARC
  - Validation
authors:
  - name: Heinrich Lukas Weil
    orcid: 0000-0003-1945-6342
    role: Developer
affiliations:
  - name: DataPLANT, RPTU Kaiserslautern-Landaus
date: 23 June 2026
---

# Background

ARCs support a mechanism called **Continuous Quality Control (CQC)** to continuously assess whether an ARC meets a defined set of quality criteria.
The unit of quality assessment is a **validation package** — a self-contained, executable script that checks a collection of requirements against an ARC and produces three standardized output artefacts: a JUnit XML report, a JSON summary, and an SVG badge.
Validation packages are published to and served by the [ARC Validation Package Registry (AVPR)](https://avpr.nfdi4plants.org/), from which the `arc-validate` CLI tool installs and runs them inside DataHUB CI/CD pipelines.

To make authoring these packages easier, the [ARCExpect](https://github.com/nfdi4plants/arc-validate/tree/release/src/ARCExpect.Core/ARCExpect.Core) library was developed for F#.
It provides a concise API for declaring validation cases, executing them, and writing the required output files — abstracting away all boilerplate so that package authors can focus on the domain logic of their checks.
A typical F# validation package using ARCExpect looks like this:

```fsharp
#r "nuget: ARCExpect, 5.0.1"

let [<Literal>] PACKAGE_METADATA = """(*
---
Name: my-package
MajorVersion: 1
MinorVersion: 0
PatchVersion: 0
Summary: Checks the basic structure of an ARC.
Description: |
  A minimal ARC validation package.
---
*)"""

Setup.ValidationPackage(
    metadata = Setup.Metadata(PACKAGE_METADATA),
    CriticalValidationCases = [
        testList "ARC structure" [
            testCase "investigation exists" <| fun () ->
                Expect.isTrue (File.Exists "isa.investigation.xlsx") "isa.investigation.xlsx not found"
        ]
    ]
)
|> Execute.ValidationPipeline(basePath = __SOURCE_DIRECTORY__)
```

While F# was well-served by this tooling, **Python is equally a first-class citizen** in the ARC validation ecosystem: AVPR accepts Python packages (`.py`) alongside F# scripts (`.fsx`), and Python packages can be executed via `uv run`.
However, Python package authors had no equivalent helper library — they were required to manually implement result file generation, badge creation, YAML frontmatter parsing, and test orchestration from scratch, making Python packages considerably more burdensome to write and maintain.
This disparity became clearly apparent during the symposium, motivating the development of a Python equivalent to ARCExpect.

# ARCExpect py

During and shortly following the symposium, a Fable-compatible F# repository was created at [HLWeil/ARCExpect](https://github.com/HLWeil/ARCExpect) to bring ARCExpect to Python.
[Fable](https://fable.io/) is a compiler that transpiles F# source code to other target languages, including Python.
This approach allows the core logic of ARCExpect — test case definition, execution, result serialization, badge generation — to be written once in F# and compiled to a native Python package, ensuring both implementations stay consistent.

The library was published to PyPI as [`arcexpect`](https://pypi.org/project/arcexpect/) and exposes an API that mirrors the F# original as closely as Python syntax allows:

| Concept | F# ARCExpect | Python arcexpect |
|---|---|---|
| Define a single check | ```testCase "name" (fun () -> ...)``` | `test_case("name", fn)` |
| Group checks | ```testList "name" [...]``` | `test_list("name", [...])` |
| Skip a check | ```ptestCase "name" (fun () -> ...)``` | `pending_test_case("name", fn)` |
| Assert truthy | ```Expect.isTrue expr msg``` | `Expect.is_true(expr, msg)` |
| Assert equality | ```Expect.equal actual expected msg``` | `Expect.equal(actual, expected, msg)` |
| Build package from script | ```Setup.ValidationPackage(metadata = ..., ...)``` | `Setup.validation_package_from_script(__file__, critical=[...])` |
| Run pipeline & write output | ```Execute.ValidationPipeline(basePath = ...)``` | `Execute.validation_pipeline(package, output_path)` |

A minimal Python validation package using `arcexpect` looks like this:

```python
# /// script
# requires-python = ">=3.11"
# dependencies = ["arcexpect", "arctrl"]
# ///

"""
---
Name: example-validator
MajorVersion: 1
MinorVersion: 0
PatchVersion: 0
Summary: Checks the basic structure of an ARC.
Description: |
  A minimal native-Python ARC validation package.
---
"""

import argparse
from pathlib import Path
from arcexpect import Execute, Expect, Setup, test_case, test_list

parser = argparse.ArgumentParser()
parser.add_argument("--input", "-i", required=True, type=Path)
parser.add_argument("--output", "-o", required=True, type=Path)
args = parser.parse_args()

def investigation_exists() -> None:
    Expect.is_true(
        (args.input / "isa.investigation.xlsx").is_file(),
        "isa.investigation.xlsx not found"
    )

package = Setup.validation_package_from_script(
    __file__,
    critical=[
        test_list("ARC structure", [
            test_case("investigation exists", investigation_exists),
        ])
    ],
)

Execute.validation_pipeline(package, str(args.output))
```

Running this script produces the expected output layout:

```
output/
└── .arc-validate-results/
    └── example-validator@1.0.0/
        ├── badge.svg
        ├── validation_report.xml
        └── validation_summary.json
```

The library correctly distinguishes critical and non-critical checks: a failing non-critical test is recorded in the report but does not cause the badge to signal a critical error, matching the behaviour of the F# library.

# Updated edal package

As a concrete validation of the new library, the existing [`edal`](https://github.com/nfdi4plants/arc-validate-package-registry/tree/main/StagingArea/edal) validation package — a Python package that checks whether an ARC meets the submission requirements of the [e!DAL Plant Genomics & Phenomics Research Data Repository](https://edal-pgp.ipk-gatersleben.de/) — was ported to use `arcexpect` in [PR #100](https://github.com/nfdi4plants/arc-validate-package-registry/pull/100).

Before the update, the package (version `0.0.4`) manually maintained hard-coded output paths, built the JSON summary dictionary by hand, and implemented test registration through a custom `add_test_case` helper function.
This amounted to roughly 164 lines, of which the majority was infrastructure rather than validation logic.

After porting to `arcexpect` (version `0.0.5`), the package was reduced to approximately 100 lines, with all boilerplate eliminated.
The validation logic itself becomes the central focus:

```python
def arc_has_valid_contacts() -> None:
    contacts = arc.Contacts
    Expect.is_true(len(contacts) > 0, "No contacts found.")
    for c in contacts:
        Expect.is_true(c.FirstName != "", f"No first name found for contact: {c}")
        Expect.is_true(c.LastName  != "", f"No last name found for contact: {c}")
        Expect.is_true(c.Affiliation != "", f"No affiliation found for contact: {c}")
        Expect.is_true(c.EMail != "", f"No email found for contact: {c}")
        Expect.is_true(c.ORCID != "", f"No ORCID found for contact: {c}")

package = Setup.validation_package_from_script(
    __file__,
    critical=[
        test_list("e!DAL ARC validation", [
            test_case("load ARC",    load_arc),
            test_case("Title",       arc_has_title),
            test_case("Description", arc_has_description),
            test_case("Contacts",    arc_has_valid_contacts),
            test_case("License",     arc_has_license),
        ])
    ],
)

Execute.validation_pipeline(package, output_dir)
```

The package was tested against a real ARC ([facultativeCA](https://git.nfdi4plants.org/brilator/Facultative-CAM-in-Talinum)) and all checks passed.
This serves as a proof of concept that the `arcexpect` library is a viable replacement for ad-hoc boilerplate in Python validation packages.

# Outlook

The availability of `arcexpect` on PyPI substantially lowers the barrier to authoring Python-based ARC validation packages.
Community members who are more familiar with Python than with F# can now write and contribute packages with the same level of structural support that F# authors have had from the start.

Going forward, two areas of follow-up work were identified:

1. **Documentation**: The current knowledge base documentation for authoring validation packages focuses primarily on the F# workflow.
   It should be restructured to give Python equal prominence, with dedicated examples and references to the `arcexpect` library, its PyPI page, and the updated API surface.

2. **Library placement**: The `arcexpect` Python package currently lives in a personal repository ([HLWeil/ARCExpect](https://github.com/HLWeil/ARCExpect)) as a development placeholder.
   The code should be moved into the DataPLANT organization — most naturally into the existing [arc-validate](https://github.com/nfdi4plants/arc-validate) repository alongside its F# counterpart — and a proper release and maintenance workflow established.
