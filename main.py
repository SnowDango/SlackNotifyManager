# import
import datetime
import threading
import time
from controller import SlackControl, MailControl, TwitterControl


def mailJob():
    gmail = MailControl.MailControl()
    mails = gmail.unreadMailList()
    if mails is not None:
        slack = SlackControl.SlackControl()
        slack.sendSlackMail(mails)


def tweetJob():
    twitter = TwitterControl.TwitterControl()
    tweet_list = twitter.getTweetList()
    if tweet_list is not None:
        slack = SlackControl.SlackControl()
        slack.sendSlackTweet(tweet_list)


if __name__ == '__main__':
    print('start')
    while True:
        t1 = threading.Thread(target=mailJob())
        t2 = threading.Thread(target=tweetJob())
        t1.start()
        t2.start()
        time.sleep(10)
