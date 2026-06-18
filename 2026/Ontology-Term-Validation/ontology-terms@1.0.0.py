PACKAGE_METADATA = """
---
Name: ontology-terms
MajorVersion: 1
MinorVersion: 0
PatchVersion: 0
Publish: false
Summary: Validates that ontology/CV annotations in ARC ISA tables are complete, well-formed, declared, and resolvable.
Description: |
  Checks ontology term annotations on Characteristic/Parameter/Factor/Component building
  blocks across all study and assay tables. Offline: source/accession pairing,
  well-formedness, source declaration, prefix consistency, free-text coverage. Online
  (when the TIB Terminology Service is reachable): accession resolution and label match.
Author:
  - FullName: Mohamed Abouzid
    Email: m.abouzid@fz-juelich.de
    Affiliation: Forschungszentrum Juelich
Tags:
  - Name: ontology
  - Name: controlled vocabulary
  - Name: FAIR
  - Name: annotation
  - Name: quality control
---
"""

# /// script
# dependencies = [
#   "arctrl",
#   "requests",
# ]
# ///

NAME = "ontology-terms"
VERSION = "1.0.0"
TIB_API = "https://api.terminology.tib.eu/api/search"
OLS_API = "https://www.ebi.ac.uk/ols4/api/search"


import json
import os
import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path
from xml.dom import minidom

_PREFIXED_RE = re.compile(r"^[A-Za-z][A-Za-z0-9.\-_]*:[A-Za-z0-9._\-]+$")
_IRI_RE = re.compile(r"^https?://\S+$")


@dataclass(frozen=True)
class TermOccurrence:
    name: str
    source: str       # Term Source REF, "" if absent
    accession: str    # Term Accession Number, "" if absent
    location: str     # human-readable: "<container>/<table>/<where>"


@dataclass
class Finding:
    check_id: str
    severity: str     # "error" | "warning"
    status: str       # "passed" | "failed" | "skipped"
    message: str
    location: str


def load_arc(arc_dir):
    from arctrl import ARC
    return ARC.load(arc_dir)


def declared_sources(arc):
    out = set()
    for ref in arc.OntologySourceReferences:
        name = getattr(ref, "Name", None)
        if name:
            out.add(str(name).strip())
    return out


def _to_occurrence(oa, location):
    return TermOccurrence(
        name=(oa.Name or "").strip(),
        source=(oa.TermSourceREF or "").strip(),
        accession=(oa.TermAccessionNumber or "").strip(),
        location=location,
    )


def collect_terms(arc):
    occs = []
    containers = list(arc.Studies) + list(arc.Assays)
    for container in containers:
        cid = getattr(container, "Identifier", "?")
        for table in container.Tables:
            tname = table.Name
            for col in table.Columns:
                header = col.Header
                hterm = None
                try:
                    hterm = header.TryGetTerm()
                except Exception:
                    hterm = None
                if hterm is not None and not hterm.is_empty():
                    occs.append(_to_occurrence(hterm, f"{cid}/{tname}/header[{header}]"))
                for i, cell in enumerate(col.Cells):
                    oa = None
                    try:
                        if cell.is_term:
                            oa = cell.AsTerm
                        elif cell.is_unitized:
                            _, oa = cell.AsUnitized
                    except Exception:
                        oa = None
                    if oa is not None and not oa.is_empty():
                        occs.append(_to_occurrence(oa, f"{cid}/{tname}/{header}/row{i + 1}"))
    return occs


def _is_iri(accession):
    return bool(_IRI_RE.match(accession))


def _pass(check_id, severity, occ):
    return Finding(check_id=check_id, severity=severity, status="passed",
                   message="ok", location=occ.location)


def check_pairing(occ):
    has_s, has_a = bool(occ.source), bool(occ.accession)
    if has_s == has_a:
        return _pass("pairing", "error", occ)
    missing = "Term Accession Number" if has_s else "Term Source REF"
    return Finding("pairing", "error", "failed",
                   f"'{occ.name}' has only one of source/accession; missing {missing}.",
                   occ.location)


def check_wellformed(occ):
    if not occ.accession:
        return Finding("wellformed", "error", "skipped", "no accession", occ.location)
    if _PREFIXED_RE.match(occ.accession) or _IRI_RE.match(occ.accession):
        return _pass("wellformed", "error", occ)
    return Finding("wellformed", "error", "failed",
                   f"Accession '{occ.accession}' is not a valid PREFIX:LOCAL id or IRI.",
                   occ.location)


def check_source_declared(occ, declared):
    if not occ.source:
        return Finding("source_declared", "error", "skipped", "no source", occ.location)
    declared_lower = {d.lower() for d in declared}
    if occ.source.lower() in declared_lower:
        return _pass("source_declared", "error", occ)
    return Finding("source_declared", "error", "failed",
                   f"Term Source REF '{occ.source}' is not declared in the "
                   f"investigation ONTOLOGY SOURCE REFERENCE section.",
                   occ.location)


def check_prefix_consistency(occ):
    if not (occ.source and occ.accession):
        return Finding("prefix_consistency", "error", "skipped", "needs both", occ.location)
    if _is_iri(occ.accession):
        return Finding("prefix_consistency", "error", "skipped", "iri accession", occ.location)
    prefix = occ.accession.split(":", 1)[0]
    if prefix.lower() == occ.source.lower():
        return _pass("prefix_consistency", "error", occ)
    return Finding("prefix_consistency", "error", "failed",
                   f"Accession prefix '{prefix}' does not match Term Source REF '{occ.source}'.",
                   occ.location)


def check_coverage(occ):
    if occ.name and not occ.source and not occ.accession:
        return Finding("coverage", "warning", "failed",
                       f"'{occ.name}' is free text with no ontology annotation.",
                       occ.location)
    return _pass("coverage", "warning", occ)


def run_offline(occurrences, declared):
    findings = []
    for occ in occurrences:
        findings.append(check_pairing(occ))
        findings.append(check_wellformed(occ))
        findings.append(check_source_declared(occ, declared))
        findings.append(check_prefix_consistency(occ))
        findings.append(check_coverage(occ))
    return findings


def _query_id(accession):
    """Convert an OBO-style IRI to a prefixed obo_id; pass prefixed ids through unchanged."""
    if accession.startswith("http"):
        segment = accession.rstrip("/").rsplit("/", 1)[-1]
        if "_" in segment:
            prefix, local = segment.rsplit("_", 1)
            return f"{prefix}:{local}"
        return segment
    return accession


def _try_search(api, query_id, session):
    """Return (doc_or_None, responded) where responded is False only on transient error."""
    for _attempt in range(2):
        try:
            r = session.get(api,
                            params={"q": query_id, "queryFields": "obo_id",
                                    "exact": "true", "rows": 1},
                            timeout=5)
            r.raise_for_status()
            docs = r.json().get("response", {}).get("docs", [])
            return (docs[0] if docs else None), True
        except Exception:
            continue
    return None, False


def resolve(accession, session, cache):
    if accession in cache:
        return cache[accession]
    query_id = _query_id(accession)
    found_doc = None
    any_response = False
    for api in (TIB_API, OLS_API):
        doc, responded = _try_search(api, query_id, session)
        any_response = any_response or responded
        if doc is not None:
            found_doc = doc
            break
    if found_doc is not None:
        result = {"found": True, "label": found_doc.get("label")}
    elif any_response:
        result = {"found": False, "label": None}   # a service answered; term genuinely absent
    else:
        result = None                              # every service errored -> skip
    cache[accession] = result
    return result


def check_resolves(occ, resolved):
    if resolved is None:
        return Finding("resolves", "error", "skipped",
                       "terminology service unreachable", occ.location)
    if resolved["found"]:
        return _pass("resolves", "error", occ)
    return Finding("resolves", "error", "failed",
                   f"Accession '{occ.accession}' does not resolve in the terminology service.",
                   occ.location)


def check_label(occ, resolved):
    if resolved is None or not resolved.get("found"):
        return Finding("label_match", "warning", "skipped",
                       "not resolved", occ.location)
    canonical = (resolved.get("label") or "").strip().casefold()
    given = (occ.name or "").strip().casefold()
    if not canonical or canonical == given:
        return _pass("label_match", "warning", occ)
    return Finding("label_match", "warning", "failed",
                   f"Annotation name '{occ.name}' differs from canonical label "
                   f"'{resolved.get('label')}' for {occ.accession}.",
                   occ.location)


def run_online(occurrences, session):
    findings = []
    cache = {}
    for occ in occurrences:
        if not occ.accession:
            continue
        resolved = resolve(occ.accession, session, cache)
        findings.append(check_resolves(occ, resolved))
        findings.append(check_label(occ, resolved))
    return findings


def _counts(findings):
    passed = sum(1 for f in findings if f.status == "passed")
    skipped = sum(1 for f in findings if f.status == "skipped")
    failed_errors = sum(1 for f in findings if f.status == "failed" and f.severity == "error")
    warnings = sum(1 for f in findings if f.status == "failed" and f.severity == "warning")
    return passed, failed_errors, warnings, skipped


def write_junit(findings, path):
    suites = ET.Element("testsuites", name=NAME)
    for severity, suite_name in (("error", "errors"), ("warning", "warnings")):
        group = [f for f in findings if f.severity == severity]
        suite = ET.SubElement(suites, "testsuite", name=suite_name,
                              tests=str(len(group)),
                              failures=str(sum(1 for f in group if f.status == "failed")),
                              skipped=str(sum(1 for f in group if f.status == "skipped")))
        for f in group:
            case = ET.SubElement(suite, "testcase", classname=f.check_id, name=f.location)
            if f.status == "failed":
                fail = ET.SubElement(case, "failure", type=f.severity, message=f.message)
                fail.text = f.message
            elif f.status == "skipped":
                sk = ET.SubElement(case, "skipped", message=f.message)
                sk.text = f.message
    xml = minidom.parseString(ET.tostring(suites)).toprettyxml(indent="  ")
    Path(path).write_text(xml, encoding="utf-8")


def write_summary(findings, path):
    passed, failed_errors, warnings, skipped = _counts(findings)
    data = {
        "package": NAME,
        "version": VERSION,
        "total": len(findings),
        "passed": passed,
        "failed_errors": failed_errors,
        "warnings": warnings,
        "skipped": skipped,
        "critical": failed_errors > 0,
    }
    Path(path).write_text(json.dumps(data, indent=2), encoding="utf-8")


def write_badge(findings, path):
    _, failed_errors, warnings, _ = _counts(findings)
    if failed_errors:
        color, status = "#e05d44", f"{failed_errors} errors"
    elif warnings:
        color, status = "#dfb317", f"{warnings} warnings"
    else:
        color, status = "#4c1", "passed"
    label = "ontology-terms"
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="220" height="20" role="img" aria-label="{label}: {status}">
  <rect width="130" height="20" fill="#555"/>
  <rect x="130" width="90" height="20" fill="{color}"/>
  <g fill="#fff" font-family="Verdana,Geneva,sans-serif" font-size="11">
    <text x="8" y="14">{label}</text>
    <text x="138" y="14">{status}</text>
  </g>
</svg>'''
    Path(path).write_text(svg, encoding="utf-8")


def _offline_forced():
    return os.environ.get("ONTOLOGY_TERMS_OFFLINE", "").strip() in ("1", "true", "True")


def main(argv=None):
    arc_dir = os.environ.get("ARC_PATH") or os.getcwd()
    out_dir = Path(arc_dir) / ".arc-validate-results" / f"{NAME}@{VERSION}"
    out_dir.mkdir(parents=True, exist_ok=True)

    arc = load_arc(arc_dir)
    declared = declared_sources(arc)
    occurrences = collect_terms(arc)

    findings = run_offline(occurrences, declared)
    if _offline_forced():
        for occ in occurrences:
            if occ.accession:
                findings.append(Finding("resolves", "error", "skipped", "offline mode", occ.location))
                findings.append(Finding("label_match", "warning", "skipped", "offline mode", occ.location))
    else:
        import requests
        session = requests.Session()
        findings += run_online(occurrences, session)

    write_junit(findings, out_dir / "validation_report.xml")
    write_summary(findings, out_dir / "validation_summary.json")
    write_badge(findings, out_dir / "badge.svg")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main(sys.argv[1:]))
