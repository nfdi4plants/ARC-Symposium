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


# create process graph for samples
def graph_process(arc:ARC, app):
    graph_edges = []
    graph_nodes_samples = []

    # -- collect inputs & outputs from all studies
    all_tables = []
    for study in arc.ISA.Studies:
        for table in study.tables:
            input_samples_col = table.TryGetInputColumn()

            output_samples_col = table.TryGetOutputColumn()
            output_samples = []
            if output_samples_col != None:
                output_samples = output_samples_col.Cells

            # --- input & output sample cells must not be empty
            if input_samples_col != None:
                for i, sample in enumerate(input_samples_col.Cells):
                    if output_samples != [] and i < len(output_samples):
                        out_sam = str(output_samples[i])
                    else:
                        out_sam = None
                        
                    tn = table_nodes(str(sample), 'input', table.Name, None, study.Identifier, out_sam)
                    all_tables.append(tn)

    # -- collect inputs & outputs from all assays tables
    for assay in arc.ISA.Assays:
        for table in assay.tables:
            input_samples_col = table.TryGetInputColumn()
            
            output_samples_col = table.TryGetOutputColumn()
            output_samples = []
            if output_samples_col != None:
                output_samples = output_samples_col.Cells

            # --- input & output sample cells must not be empty
            if input_samples_col != None:
                for i, sample in enumerate(input_samples_col.Cells):
                    if output_samples != [] and i < len(output_samples):
                        out_sam = str(output_samples[i])
                    else:
                        out_sam = None
                    
                    tn = table_nodes(str(sample), 'input', table.Name, assay.Identifier, None, out_sam)
                    all_tables.append(tn)


    # --- make a unique list of table node objects aka sample objects
    # --- seems that this is not making a unique set of table_node objects
    # --- however, seems that cytoscape does not plot nodes with same ids 
    unique_sample_nodes:list[table_nodes]  = list(set(all_tables))     

    # --- create nodes & edges for each sample
    for sample in unique_sample_nodes:
        graph_nodes_samples.append({
            'data': {'id': sample.name, 'label': 'sample'},
        })
        if sample.output != None:
            graph_nodes_samples.append({
                'data': {'id': sample.output, 'label': 'sample'},
            })
            graph_edges.append({
                'data': {'source': sample.name, 'target': sample.output, 'label': sample.table_name }},  
            )
    
    graph_input = graph_edges + graph_nodes_samples

    # --- create graph viz
    # -- color settings
    color_samples = '#666666' ## gray
    
    app.layout = html.Div([
        cyto.Cytoscape(
            id='cytoscape',
            layout={'name': 'breadthfirst',},
            style={'width': '100%', 'height': '600px'},
            elements=graph_input,
            stylesheet=[
                # Group selectors
                {
                    'selector': 'node',
                    'style': {
                        'content': 'data(id)',
                    }
                },
                {
                    'selector': '[label = "sample"]',
                    'style': {
                        'background-color': color_samples
                    }
                },
                {
                    'selector': 'edge',
                    'style': {
                        # The default curve style does not work with certain arrows
                        'curve-style': 'bezier',
                        'target-arrow-shape': 'vee',
                        'arrow-scale' : 2,
                        'content': 'data(label)',
                    }
                },
            ]),
        ])
    

class table_nodes:
    def __init__(self, name:str, type:str, table_name:str, assayID:None|str, studyID:None|str, output:None|str):
        self.name = name
        self.type = type
        self.table_name = table_name
        self.assayID:None|str = assayID
        self.studyID:None|str = studyID
        self.output:None|str = output

    def __eq__(self, other):
        if not isinstance(other, table_nodes):
            return False
        return (self.name == other.name and
                self.type == other.type and
                self.table_name == other.table_name and
                self.assayID == other.assayID and
                self.studyID == other.studyID and
                self.output == other.output
                )
    
    def __hash__(self):
        return hash((self.name, self.type, self.table_name, self.assayID, self.studyID, self.output))
    
    def __str__(self):
        return f"Table node {{ \
            Name: {self.name}, \
            Type: {self.type}, \
            Table Name: {self.table_name}, \
            AssayID: {self.assayID}, \
            StudyID: {self.studyID}, \
            Output: {self.output} \
            }}"


def main():
    # Create
    arc = ARC()

    # --- ARC path ### the ARC path / ARC should come from ARCitect
    #arc_root_path = "./ARC-Process-GraphViz-Example-main" ## does not work because SWATE made invalid XML file
    #arc_root_path = "./TalinumPhotosynthesis" # has no SWATE metadata sheets
    arc_root_path = "C:/Users/bfrommer/sciebo/dataPlant/Nfdi Task Area 3/ARCitect/Genome-sequence-Chitinophaga-sp-and-Microbacterium-sp-sand-sample-2023"

    # --- read ARC
    arc = read(arc_root_path)
    
    # -- start Dash
    app = Dash(__name__) 
    
    # --- graph for processes
    graph_process(arc, app)
    app.run(debug=True)

    # --- if we add Workflows, Runs then this colors:
    #Workflows = blue #0B2D8F
    #Runs = Red #C00000

if __name__ == '__main__':
    main()