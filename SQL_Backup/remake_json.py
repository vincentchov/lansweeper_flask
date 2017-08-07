import json

filename = 'tsysAssetTypes.json'

with open(filename) as json_data:
    d = json.load(json_data)

with open(filename, 'w') as json_data:
    json_data.write(json.dumps(d, indent=4, sort_keys=True))
