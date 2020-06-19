import requests
import json


class State(object):
    def __init__(self, code, name=None):
        self.code = code
        self.name = name
        self.info = None

    def get_info_by_code(self) -> None:
        if self.code.lower() != "all":
            response = requests.get("https://covidtracking.com/api/v1/states/info.json")
            content = json.loads(response.content)
            self.info = next((dcty for dcty in content if dcty['state'] == self.code), None)
            self.name = self.info['name']
        else:
            self.name = "USA"
            self.info = {}
