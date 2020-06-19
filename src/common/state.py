import requests
import json

raw_list = json.loads(requests.get("https://covidtracking.com/api/v1/states/info.json").content)
code_name = [{"state": ele["state"], "name": ele["name"]} for ele in raw_list]
code_name.append({"state": "ALL", "name": "USA"})


class State(object):
    def __init__(self, code, name=None):
        if code:
            self.code = code.upper()
            self.info = next((dcty for dcty in code_name if dcty['state'] == self.code), None)
            self.name = self.info['name']
        elif name:
            if name.upper() == "USA":
                self.name = name.upper()
            else:
                self.name = name.title()
            self.info = next((dcty for dcty in code_name if dcty['name'] == self.name), None)
            self.code = self.info['state']