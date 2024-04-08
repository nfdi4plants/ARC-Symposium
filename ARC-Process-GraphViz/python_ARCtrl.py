import os
from arctrl.arctrl import ARC;
from arctrl.arctrl import ArcInvestigation;
from fsspreadsheet.xlsx import Xlsx
from pathlib import Path
from arctrl.Contract.contract import Contract

#print(ARC) #// <class 'arctrl.arc.ARC'>

def read(base_path):
    all_file_paths = get_all_file_paths(base_path)
    arc = ARC.from_file_paths(all_file_paths)
    read_contracts = arc.GetReadContracts()
    #print(read_contracts)
    #print(base_path)
    
    fcontracts = (fulfill_read_contract(base_path, contract) for contract in read_contracts)
    for contract, content in zip(read_contracts, fcontracts):
        contract.DTO = content
    arc.SetISAFromContracts(fcontracts)
    return arc

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

# put it all together
def fulfill_read_contract (basePath : str, contract : Contract) :
    if contract.Operation == "READ" :
        print(contract)
        #exit()

        normalizedPath = os.path.normpath(Path.joinpath(basePath, contract.Path))
        if contract.DTOType == "ISA_Assay" or contract.DTOType == "ISA_Assay" or contract.DTOType == "ISA_Investigation" :        
            fswb = Xlsx.from_xlsx_file(normalizedPath)
            contract.DTO = fswb
        elif contract.DTOType ==  "PlainText" :
            content = Path.read_text(normalizedPath)
            contract.DTO = content
        else :
            print("Handling of ${contract.DTOType} in a READ contract is not yet implemented")

    else :
        print("Error (fulfillReadContract): ${contract} is not a READ contract")

# Setup
def normalize_path_separators(path_str: str):
    normalized_path = os.path.normpath(path_str)
    print(normalized_path)
    
    return normalized_path.replace('\\', '/')
    #rep_path = normalized_path.replace('\\', '/')
    #return rep_path

my_arc= "C:/Users/bfrommer/sciebo/dataPlant/TalinumPhotosynthesis"
print(my_arc)
#normalized_path = os.path.normpath(my_arc)
#print(normalized_path)
#normalize_path_separators(my_arc)

read(my_arc)
