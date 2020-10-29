import sys
sys.path.append("")
import tweepy
import json
import datetime
from pytz import timezone

last_date = datetime.datetime.now().astimezone(timezone('Asia/Tokyo'))


class TwitterControl:

    def __init__(self):
        keys = json.load(open('api_key.json', 'r'))
        self.twitter_key = keys["twitter"]
        auth = tweepy.OAuthHandler(self.twitter_key["api"], self.twitter_key["api-secret"])
        auth.set_access_token(self.twitter_key["token"], self.twitter_key["token-secret"])
        self.api = tweepy.API(auth)

    def getTweetList(self):
        global last_date
        new_tweets = []
        now_date = datetime.datetime.now().astimezone(timezone('Asia/Tokyo'))
        for num in range(len(self.twitter_key["list_id"])):
            tweets = self.api.list_timeline(list_id=self.twitter_key["list_id"][num])
            list_tweet = []
            for tweet in tweets:
                created_at = self.changeStrToTime(tweet._json['created_at'])
                if created_at > last_date:
                    list_tweet.append(
                        'https://twitter.com/{0}/status/{1}/'.format(tweet._json["user"]['screen_name'],
                                                                     tweet._json["id_str"])
                    )
            new_tweets.append(list_tweet)
            print("listId = {0}, newTweets = {1}".format(self.twitter_key["list_id"][num], new_tweets[num]))
        last_date = now_date
        return new_tweets

    def changeStrToTime(self, str):
        time_data = datetime.datetime.strptime(str, '%a %b %d %H:%M:%S %z %Y')
        time_data.astimezone(timezone('Asia/Tokyo'))
        return time_data
