import tweepy
import json
import datetime
from pytz import timezone


class TwitterControl:

    def __init__(self):
        self.keys = json.load(open('/Users/ochiaiyuuki/PycharmProjects/SlackNotifyMnager/controller/key.json', 'r'))
        auth = tweepy.OAuthHandler(self.keys["api"], self.keys["api-secret"])
        auth.set_access_token(self.keys["token"], self.keys["token-secret"])
        self.api = tweepy.API(auth)
        self.last_date = datetime.datetime.now().astimezone(timezone('Asia/Tokyo'))

    def getTweetList(self):
        new_tweets = []
        tweets = self.api.list_timeline(list_id=self.keys["list_id"])
        last_date = datetime.datetime.now().astimezone(timezone('Asia/Tokyo'))
        for tweet in tweets:
            created_at = self.changeStrtoTime(tweet._json['created_at'])
            if created_at > self.last_date:
                new_tweets.append(
                    'https://twitter.com/{0}/status/{1}/'.format(tweet._json["user"]['screen_name'],
                                                                 tweet._json["id_str"])
                )
        print('tweet scan : {}'.format(new_tweets))
        self.last_date = last_date
        return new_tweets

    def changeStrtoTime(self, str):
        time_data = datetime.datetime.strptime(str, '%a %b %d %H:%M:%S %z %Y')
        time_data.astimezone(timezone('Asia/Tokyo'))
        return time_data
