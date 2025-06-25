import json
import omero
from omero.gateway import BlitzGateway


# Connect to the OMERO Server
conn = BlitzGateway('root', 'omero', host='localhost', port=4064)
connected = conn.connect()
if connected:
    print("Connected to OMERO server.")
else:
    print("Failed to connect to OMERO server.")



# Parse the JSON-LD file to get the metadata.
# Load the JSON-LD file
with open("arc-ro-crate-metadata2.json", "r", encoding="utf-8") as f:
    data = json.load(f)
    #print(data)

# Print top-level keys
#print(data["about"].keys())


# Access information from investigation, e.g., ONTOLOGY SOURCE REFERENCE

ontologyName = [ontologies["name"] for ontologies in data['about']['ontologySourceReferences']]
InvestigationOntologyName = ", ".join(ontologyName)  # Join names into a single string
ontologiyFile = [ontologies["file"] for ontologies in data['about']['ontologySourceReferences']]
InvestigationOntologyFile = ", ".join(ontologiyFile)  # Join file paths into a single string
ontologyVersion = [ontologies["version"] for ontologies in data['about']['ontologySourceReferences']]
InvestigationOntologyVersion = ", ".join(ontologyVersion)  # Join versions into a single string



# Access information from investigation, e.g., INVESTIGATION
# Use .get() to safely access keys that may not exist.
title = data["about"]["title"]
InvestigationIdentifier = data["about"]["identifier"]
InvestigationDescription = data["about"]["description"]
InvestigationSubmissionDate = data["about"]["submissionDate"]
# This is contextual information, not a direct key as it does not exist here.
InvestigationPublicReleaseDate = data['about']["@context"]["publicReleaseDate"] 


# Access information from investigation, for INVESTIGATION PUBLICATION
# This is a list therefore accesing the element using indexing.
first_publication = data["about"]["publications"][0]  # Acccessing the first publication. There is only one here.

InvestigationPublicationPubMedID = first_publication["pubMedID"]
InvestigationPublicationDOI = first_publication["doi"]
InvestigationPublicationTitle = first_publication["title"]
InvestigationPublicationStatus = first_publication["status"]['annotationValue']
InvestigationPublicationStatusTermAccessionNumber = first_publication["status"]["termAccession"]
InvestigationPublicationStatusTermSourceREF = first_publication["status"]["termSource"]
InvestigationPublicationAuthorList = first_publication["authorList"][0]['name']
# Looping through the authorList to get all authors
# This is a list of dictionaries, each with a 'name' key.
# Therefore, we can use a list comprehension to extract all names.
autor_names = [author['name'] for author in first_publication["authorList"]]
InvestigationPublicationAuthorList = ", ".join(autor_names)


# Access information from investigation, for INVESTIGATION CONTACT
first_contact = data["about"]["people"][0]

InvestigationPersonLastName = first_contact["lastName"]
InvestigationPersonFirstName = first_contact["firstName"]
#InvestigationPersonMidInitials = first_contact["midInitials"]
InvestigationPersonEmail = first_contact["email"]
InvestigationPersonPhone = first_contact["phone"]
#InvestigationPersonFax = first_contact["fax"]
InvestigationPersonAddress = first_contact["address"]
InvestigationPersonAffiliation = first_contact["affiliation"]["name"]
#InvestigationPersonRoles = first_contact["roles"]
#InvestigationPersonRolesTermAccessionNumber = first_contact["rolesTermAccessionNumber"]
#InvestigationPersonRolesTermSourceREF = first_contact["rolesTermSourceREF"]
InvestigationPersonRolesCommentsORCID = first_contact['orcid']


# Print the information





# Add key-value pairs and namespaces to omero. 
# Prepare key-value pairs
metadata = [
    ("Investigation Ontology Name", InvestigationOntologyName),
    ("Investigation Ontology File", InvestigationOntologyFile),
    ("Investigation Ontology Version", InvestigationOntologyVersion),
    ("Investigation Identifier", InvestigationIdentifier),
    ("Investigation Description", InvestigationDescription),
    ("Investigation Submission Date", InvestigationSubmissionDate),
    ("Investigation PubMed ID", InvestigationPublicationPubMedID),
    ("Investigation DOI", InvestigationPublicationDOI),
    ("Investigation Title", InvestigationPublicationTitle),
    ("Investigation Publication Status", InvestigationPublicationStatus),
    ("Investigation Publication Status Term Accession Number", InvestigationPublicationStatusTermAccessionNumber),
    ("Investigation Publication Status Term Source REF", InvestigationPublicationStatusTermSourceREF),
    ("Investigation Publication Author List", InvestigationPublicationAuthorList),
    ("Investigation Person Last Name", InvestigationPersonLastName),
    ("Investigation Person First Name", InvestigationPersonFirstName),
    ("Investigation Person Email", InvestigationPersonEmail),
    ("Investigation Person Phone", InvestigationPersonPhone),
    ("Investigation Person Address", InvestigationPersonAddress),
    ("Investigation Person Affiliation", InvestigationPersonAffiliation),
    ("Investigation Person Roles Comments ORCID", InvestigationPersonRolesCommentsORCID),
]



# Create and attach a MapAnnotation to the project
# Prepare key-value pairs as list of lists
key_value_data = [[str(k), str(v)] for k, v in metadata if v is not None]  # Filter out None values

map_ann = omero.gateway.MapAnnotationWrapper(conn)
namespace = omero.constants.metadata.NSCLIENTMAPANNOTATION
map_ann.setNs(namespace)
map_ann.setValue(key_value_data)
map_ann.save()
project = conn.getObject("Project", 251)  # Replace with your project ID
project.linkAnnotation(map_ann)
conn.close()
print("MapAnnotation created and linked to the project.")




