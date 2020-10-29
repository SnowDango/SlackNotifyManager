import json
import requests


class MailTargetModel:

    def __init__(self):
        keys = json.load(open('api.json', 'r'))
        self.api = keys["api"]

    def getTarget(self):
        res = requests.get(self.api)
        data = res.json()
        print(data)
        return data
