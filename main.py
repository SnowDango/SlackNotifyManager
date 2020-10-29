# import
import datetime
import threading
import time
from controller import SlackControl, MailControl, TwitterControl


def mailJob():
    mail = MailControl.MailControl()
    mail.login()
    result, data_id = mail.getNewMailList()
    bodys = mail.getMailData(data_id)
    mail.logout()
    if not bodys:
        return
    else:
        slack = SlackControl.SlackControl()
        slack.sendSlackMail(bodys)


def tweetJob():
    twitter = TwitterControl.TwitterControl()
    tweet_list, tweet_list2 = twitter.getTweetList()
    if not tweet_list:
        return
    else:
        slack = SlackControl.SlackControl()
        slack.sendSlackTweet(tweet_list)
    if not tweet_list2:
        return
    else:
        slack = SlackControl.SlackControl()
        slack.sendSlackTweet(tweet_list2)


if __name__ == '__main__':
    print('start')
    while True:
        t1 = threading.Thread(target=mailJob())
        t2 = threading.Thread(target=tweetJob())
        t1.start()
        t2.start()
        time.sleep(10)
