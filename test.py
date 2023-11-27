import json

with open("files.json", "r") as data_file:
    json_file = json.load(data_file)
    print(list(json_file.keys()))