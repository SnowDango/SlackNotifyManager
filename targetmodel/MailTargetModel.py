import json
import requests
import datetime
from pytz import timezone
from utility import ErrorLogger


class MailTargetModel:

    def __init__(self):
        keys = json.load(open('.env/api.json', 'r'))
        self.api = keys["api"]

    def getTarget(self):
        try:
            res = requests.get(self.api)
            data = res.json()
            print(data)
            return data
        except Exception as e:
            ErrorLogger.logger(datetime.datetime.now().astimezone(timezone('Asia/Tokyo')), e)
            res = {"syumi": [], "syukatu": [], "baito": []}
            return res
