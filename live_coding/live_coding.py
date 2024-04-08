from arctrl.arctrl import ARC, JsonController
import json

f = open('ro_crate.json')

data = json.load(f)
jsonString = json.dumps(data)
investigation = JsonController.Investigation().from_rocrate_json_string(jsonString)

print(investigation)