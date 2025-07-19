import json
from pprint import pprint

filename = "working-dir/gist-vscode-profile-abm-autobuildmarlin.json"

with open(filename, 'r') as json_file:
    profile = json.load(json_file)

settings_dict = json.loads(profile['settings'])
# for s in dict(settings_dict).values():
#     print(s)
# print(settings_dict["settings"])

try:
    settings = json.loads(settings_dict["settings"])
except json.decoder.JSONDecodeError as e:
    print (e)
print(settings)