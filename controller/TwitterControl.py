import tweepy
import json
import datetime
from pytz import timezone


class TwitterControl:

    def __init__(self):
        self.keys = json.load(open('', 'r'))
        auth = tweepy.OAuthHandler(self.keys["api"], self.keys["api-secret"])
        auth.set_access_token(self.keys["token"], self.keys["token-secret"])
        self.api = tweepy.API(auth)

    def getTweetList(self):
        new_tweets = []
        now = datetime.datetime.now().astimezone(timezone('Asia/Tokyo'))
        tweets = self.api.list_timeline(list_id=self.keys["list_id"])
        for tweet in tweets:
            created_at = self.changeStrtoTime(tweet._json['created_at'])
            now_delta = now + datetime.timedelta(seconds=-15)
            if created_at > now_delta:
                new_tweets.append(
                    'https://twitter.com/{0}/status/{1}'.format(tweet._json["user"]['screen_name'], tweet._json["id_str"])
                )
        print('tweet scan : {}'.format(new_tweets))
        return new_tweets

    def changeStrtoTime(self, str):
        time_data = datetime.datetime.strptime(str, '%a %b %d %H:%M:%S %z %Y')
        time_data.astimezone(timezone('Asia/Tokyo'))
        return time_data
