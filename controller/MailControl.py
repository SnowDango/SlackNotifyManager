from simplegmail import Gmail
from targetmodel import MailTargetModel


class MailControl:

    def __init__(self):
        self.gmail = Gmail()

    def unreadMailList(self):
        unreadMails = {0: [], 1: [], 2: [], 3: []}
        target = MailTargetModel.MailTargetModel()
        target_address = target.getTarget()
        messages = self.gmail.get_unread_inbox()
        for message in messages:
            message.mark_as_read()
            to = message.recipient
            from_ = message.sender
            subject = message.subject
            date = message.date
            num = self.isTarget(from_, target_address)
            try:
                body = message.plain
                unreadMails[num].append("to: {0}\nfrom: {1}\ndate: {2}\nsubject: {3}\n{4}".format(
                    to, from_, date, subject, body
                ))
            except Exception as e:
                body = "can't decode mail"
                unreadMails[num].append("to: {0}\nfrom: {1}\ndate: {2}\nsubject: {3}\n{4}".format(
                    to, from_, date, subject, body
                ))
                continue
        print("unread mails = {}".format(unreadMails))
        return unreadMails

    def isTarget(self, from_, target_address):
        num = 0
        if target_address["syukatu"].count(from_) != 0:
            num = 1
        elif target_address["syumi"].count(from_) != 0:
            num = 2
        elif target_address["baito"].count(from_) != 0:
            num = 3
        return num

