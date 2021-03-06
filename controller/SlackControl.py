import requests
import json
import datetime
from pytz import timezone
from utility import ErrorLogger


class SlackControl:

    def __init__(self):
        keys = json.load(open('.env/api_key.json', 'r'))
        self.mail_webhook = keys['mail']['mail-channel']
        self.twitter_webhook = keys["slack"]["twitter-channel"]

    def sendSlackMail(self, mails):
        try:
            for num in range(len(mails)):
                for mail in mails[num]:
                    requests.post(self.mail_webhook[num], data=json.dumps({'text': '```{}```'.format(mail)}))
        except Exception as e:
            ErrorLogger.logger(datetime.datetime.now().astimezone(timezone('Asia/Tokyo')), e)

    def sendSlackTweet(self, tweets_list):
        try:
            for num in range(len(tweets_list)):
                if tweets_list[num] is not None:
                    for tweet in tweets_list[num]:
                        requests.post(self.twitter_webhook[num], data=json.dumps({'text': tweet, "unfurl_link": True}))
                else:
                    continue
        except Exception as e:
            ErrorLogger.logger(datetime.datetime.now().astimezone(timezone('Asia/Tokyo')), e)



