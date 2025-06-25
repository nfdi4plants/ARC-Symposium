import json

with open("arc-ro-crate-metadataNew.json", "r", encoding="utf-8") as f:
    crate = json.load(f)

graph = crate["@graph"]

# --- Investigation ---
investigation = next(
    item for item in graph
    if item.get("@type") == "Dataset" and item.get("additionalType") == "Investigation"
)

creator_id = investigation.get("creator", {}).get("@id")
person = next((p for p in graph if p.get("@id") == creator_id and p.get("@type") == "Person"), {})
affiliation_id = person.get("affiliation", {}).get("@id")
affiliation = next((a for a in graph if a.get("@id") == affiliation_id), {})
role_id = person.get("jobTitle", {}).get("@id")
role = next((r for r in graph if r.get("@id") == role_id), {})

# --- Publication Info ---
publication_id = investigation.get("citation", {}).get("@id")
publication = next((p for p in graph if p.get("@id") == publication_id), {})

# Get PubMed ID and DOI from identifiers
pubmed_id = ""
doi = ""
for ident in publication.get("identifier", []):
    ident_obj = next((x for x in graph if x["@id"] == ident["@id"]), {})
    prop_id = ident_obj.get("propertyID", "")
    if "OBI_0001617" in prop_id:
        pubmed_id = ident_obj.get("value", "")
    elif "OBI_0002110" in prop_id:
        doi = ident_obj.get("value", "")

# Resolve authors
authors = []
for a in publication.get("author", []):
    person_ref = next((p for p in graph if p.get("@id") == a["@id"]), {})
    authors.append(person_ref.get("givenName", "").strip())

# Resolve publication status
status_id = publication.get("creativeWorkStatus", {}).get("@id", "")
status = next((s for s in graph if s.get("@id") == status_id), {})
status_name = status.get("name", "")
status_code = status.get("termCode", "")
status_source = status.get("@id", "")

# --- Build Output Dictionary ---
output = {
    # Investigation Person
    "Investigation Person Last Name": person.get("familyName", ""),
    "Investigation Person First Name": person.get("givenName", ""),
    "Investigation Person Mid Initials": "",
    "Investigation Person Email": person.get("email", ""),
    "Investigation Person Phone": person.get("telephone", ""),
    "Investigation Person Fax": "",
    "Investigation Person Address": person.get("address", ""),
    "Investigation Person Affiliation": affiliation.get("name", ""),
    "Investigation Person Roles": role.get("name", ""),
    "Investigation Person Roles Term Accession Number": role.get("termCode", ""),
    "Investigation Person Roles Term Source REF": role.get("@id", ""),
    "Comment[ORCID]": person.get("@id", ""),

    # Investigation Metadata
    "Investigation Identifier": investigation.get("identifier", ""),
    "Investigation Title": investigation.get("name", ""),
    "Investigation Description": investigation.get("description", ""),
    "Investigation Submission Date": investigation.get("datePublished", ""),
    "Investigation Public Release Date": investigation.get("datePublished", ""),

    # Publication Metadata
    "Investigation Publication PubMed ID": pubmed_id,
    "Investigation Publication DOI": doi,
    "Investigation Publication Author List": "; ".join(authors),
    "Investigation Publication Title": publication.get("headline", ""),
    "Investigation Publication Status": status_name,
    "Investigation Publication Status Term Accession Number": status_code,
    "Investigation Publication Status Term Source REF": status_source
}

# --- Now Add Term Source Fields ---
term_sources = [entry for entry in graph if entry.get("@type") == "DefinedTerm"]

output["Term Source Name"] = ", ".join(
    entry.get("name", "") for entry in term_sources if entry.get("name")
)
output["Term Source File"] = ", ".join(
    entry.get("@id", "") for entry in term_sources if entry.get("@id")
)
output["Term Source Version"] = ", ".join(
    entry.get("termCode", "") for entry in term_sources if entry.get("termCode")
)
output["Term Source Description"] = ", ".join(
    entry.get("description", "") for entry in term_sources if entry.get("description")
)

# --- Print Output ---
for key, value in output.items():
    print(f"{key}: {value}")
