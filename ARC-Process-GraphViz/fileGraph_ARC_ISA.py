import os
from arctrl.arc import ARC
from arctrl.Contract.contract import Contract, DTO
from pathlib import Path
from arctrl.arctrl import ArcInvestigation, ArcTable, CompositeCell
from fsspreadsheet.xlsx import Xlsx
from dash import Dash, html
import dash_cytoscape as cyto


def write(arc_path, arc: ARC):
    contracts = arc.GetWriteContracts()
    for contract in contracts:
        # from Contracts.js docs
        fulfill_write_contract(arc_path, contract)

# Setup
def normalize_path_separators(path_str: str):
    normalized_path = os.path.normpath(path_str)
    return normalized_path.replace('//', '/')

def get_all_file_paths(base_path):
    files_list = []
    def loop(dir_path):
        files = os.listdir(dir_path)
        for file_name in files:
            file_path = os.path.join(dir_path, file_name)
            if os.path.isdir(file_path):
                loop(file_path)
            else:
                relative_path = os.path.relpath(file_path, base_path)
                normalize_path = normalize_path_separators(relative_path)
                files_list.append(normalize_path)
    loop(base_path)
    return files_list

def fulfill_write_contract (basePath : str, contract : Contract) :
    def ensure_directory (filePath: Path) :
        if filePath.suffix or filePath.name.startswith(".") :
            filePath = filePath.parent    
        path_str = str(filePath)
        # Split the path into individual directories
        directories = path_str.split(os.path.sep)
        current_path = ""
        # Iterate through each directory in the path
        for directory in directories:
            # Append the current directory to the current path
            current_path = os.path.join(current_path, directory)
            # Check if the current path exists as a directory
            exists = os.path.exists(current_path)
            if not exists:
                os.makedirs(current_path)

        
    p = Path(basePath).joinpath(contract.Path)
    if contract.Operation == "CREATE" :
        if contract.DTO == None :
            ensure_directory(p)
            Path.write_text(p, "")
        elif contract.DTOType.name == "ISA_Assay" or contract.DTOType.name == "ISA_Study" or contract.DTOType.name == "ISA_Investigation" :
            ensure_directory(p)
            Xlsx.to_xlsx_file(p, contract.DTO.fields[0])
        elif contract.DTOType == "PlainText" :
            ensure_directory(p)
            Path.write_text(p, contract.DTO.fields[0])
        else :
            print("Warning: The given contract is not a correct ARC write contract: ", contract)      
    
#  Read
def fulfill_read_contract (basePath : str, contract : Contract) :
    if contract.Operation == "READ" :
        normalizedPath = os.path.normpath(Path(basePath).joinpath(contract.Path))
        if contract.DTOType.name == "ISA_Assay" or contract.DTOType.name == "ISA_Study" or contract.DTOType.name == "ISA_Investigation" :        
            fswb = Xlsx.from_xlsx_file(normalizedPath)
            contract.DTO = DTO(0, fswb)
        elif contract.DTOType == "PlainText" :
            content = Path.read_text(normalizedPath)
            contract.DTO = DTO(1, content)
        else :
            print("Handling of ${contract.DTOType} in a READ contract is not yet implemented")
    else :
        print("Error (fulfillReadContract): ${contract} is not a READ contract")

# put it all together
def read(base_path):
    all_file_paths = get_all_file_paths(base_path)
    arc = ARC.from_file_paths(all_file_paths)
    read_contracts = arc.GetReadContracts()
    fcontracts = [fulfill_read_contract(base_path, contract) for contract in read_contracts]
    arc.SetISAFromContracts(read_contracts)
    return arc

# create graph for investigation, studies, assays
def graph_investigation(arc:ARC, app):
    
    # ---  graph elements
    graph_edges = []
    graph_nodes_studies = []
    graph_nodes_assays = []

    ## investigation, study, assay names for nodes
    name_investigation = arc.ISA.Identifier
    study_names = arc.ISA.StudyIdentifiers
    assay_names = arc.ISA.AssayIdentifiers

    # -- node with investigation only
    graph_nodes = [{
        'data': {'id': name_investigation, 'label': 'investigation'},
        }]
    
    # -- nodes for each study; default connected to investigation
    for i, study in enumerate(study_names):
        graph_nodes_studies.append({
            'data': {'id': study, 'label': 'study'},
        })

        graph_edges.append({
        'data': {'source': name_investigation, 'target': study}},  
        )

        # -- edges for registered assays
        for assay in arc.ISA.Studies[i].RegisteredAssayIdentifiers:
            graph_edges.append({
                'data': {'source': study, 'target': assay}},  
            )
        
    # -- nodes for each assay
    for assay in assay_names:
        graph_nodes_assays.append({
            'data': {'id': assay, 'label': 'assay'},
        })

    graph_input = graph_nodes + graph_nodes_studies + graph_nodes_assays + graph_edges

    # --- create graph viz
    # -- color settings
    color_investigation = '#1FC7FF' ## turquoise
    color_studies = '#B4CE8F' ## green
    color_assays= '#FFC000' ## yellow

    app.layout = html.Div([
        cyto.Cytoscape(
            id='cytoscape-styling-3',
            layout={
                'name': 'breadthfirst',
                'roots': '[label = "investigation"]'
            },
            style={'width': '100%', 'height': '600px'},
            elements=graph_input,
            stylesheet=[
                # Group selectors
                {
                    'selector': 'node',
                    'style': {
                        'content': 'data(id)'
                    }
                },
                {
                    'selector': '[label = "investigation"]',
                    'style': {
                        'background-color': color_investigation
                    }},
                {
                    'selector': '[label = "study"]',
                    'style': {
                        'background-color': color_studies
                    }},
                {
                    'selector': '[label = "assay"]',
                    'style': {
                        'background-color': color_assays
                    }},
                    {
                    'selector': 'edge',
                    'style': {
                        # The default curve style does not work with certain arrows
                        'curve-style': 'bezier',
                        'target-arrow-shape': 'vee',
                        'arrow-scale' : 2,
                    }
                },
            ])
    ])


def main():
    # Create
    arc = ARC()

    # --- ARC path ### the ARC path / ARC should come from ARCitect
    arc_root_path = "./TalinumPhotosynthesis"

    # --- read ARC
    arc = read(arc_root_path)

    # -- start Dash
    app = Dash(__name__) 
    
    # --- graph with investigation, studies, assays
    graph_investigation(arc, app)

    app.run(debug=True)


if __name__ == '__main__':
    main()