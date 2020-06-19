import requests
import json


class State(object):
    def __init__(self, code):
        self.code = code
        self.name = None
        self.info = None

    def get_info(self) -> None:
        if self.code.lower() != "all":
            response = requests.get("https://covidtracking.com/api/v1/states/info.json")
            content = json.loads(response.content)
            self.info = next((dcty for dcty in content if dcty['state'] == self.code), None)
            self.name = self.info['name']
        else:
            self.name = "USA"
            self.info = {}
