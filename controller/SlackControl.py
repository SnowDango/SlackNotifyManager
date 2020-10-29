import requests
import json


class SlackControl:

    def __init__(self):
        keys = json.load(open('key.json', 'r'))
        self.OTHER_WEB_HOOK_URL = keys["other_webhook"]
        self.IDOL_WEB_HOOK_URL = keys["idol_webhook"]

    def sendSlackMail(self, bodys):
        for body in bodys:
            requests.post(self.OTHER_WEB_HOOK_URL, data=json.dumps({
                'text': '```{}```'.format(body)
            }))

    def sendSlackTweet(self, tweets):
        for tweet in tweets:
            requests.post(self.IDOL_WEB_HOOK_URL, data=json.dumps({'text': tweet, "unfurl_links": True}))

