import re
import imaplib
import email
import email.parser
from email.header import decode_header
from email.utils import parsedate_to_datetime
import json


class MailControl:

    def __init__(self):
        self.imap = imaplib.IMAP4_SSL("imap.gmail.com", '993')
        self.keys = json.load(open('/Users/ochiaiyuuki/PycharmProjects/SlackNotifyMnager/controller/key.json', 'r'))
        self.UserName = self.keys["user_name"]
        self.PassWord = self.keys["pass"]

    msg_id_re = re.compile(r"<([^>]+)>")
    rcv_date_re = re.compile(
        r"^(?:.+)\s+for\s?<[^>]+>\s?;\s?([A-Za-z]{3}\s?,\s?[0-9]+\s+[A-Za-z]{3}\s+[0-9]{4}\s+[0-9]+:[0-9]+:[0-9]+\s+[\+\-]?[0-9]{4})",
        re.MULTILINE | re.DOTALL)
    flags_re = re.compile(r"^[0-9]+ \(FLAGS \(([A-Za-z\\\$ ]*)\)\)$")

    def login(self):
        self.imap.login(self.UserName, self.PassWord)

    def logout(self):
        self.imap.close()
        self.imap.logout()

    def getNewMailList(self):
        self.imap.select()
        result, data_id = self.imap.search(None, "UNSEEN")
        data_id = data_id[0].split()
        return result, data_id

    def getMailData(self, data_id):
        log_header = []
        bodys = []
        for ids in data_id:
            resp, data = self.imap.fetch(ids, "(RFC822)")
            body = data[0][1]
            subject, content, from_, date = self.fetchmail(body, 1)
            log_header.append(subject)
            mail_data = 'from: {0} \ndate: {1} \nsubject: {2} \n{3}'.format(from_, date, subject, content)
            bodys.append(mail_data)
        print('mail scan : {}'.format(log_header))
        return bodys

    def fetchmail(self, data, msg_no):
        msg = email.message_from_bytes(data)
        from_, date, subject, content = self.get_data(msg)
        return subject, content, from_, date

    def get_data(self, msg):
        from_, encode = self.get_header(msg, 'From')
        data, encode = self.get_header(msg, 'Date')
        subject, encode = self.get_header(msg, 'Subject')
        body = self.get_body(msg, encode)
        return from_, data, subject, body

    def get_body(self, msg, encode):
        try:
            body = msg.get_payload(decode='utf-8').decode(encoding='utf-8')
            return body
        except Exception as e:
            print(e)
            prt = msg.get_payload()[0]
            byt = prt.get_payload(decode=True)
            body = byt.decode(encoding='utf-8')
            return body

    def get_header(self, msg, name):
        header = email.header.decode_header(msg.get(name))
        data = self.header_decode(header)
        return data

    def header_decode(self, header):
        result_head = ''
        if len(header) >= 2:
            for head in header:
                if len(head) > 1:
                    if head[1] is not None:
                        result_head += head[0].decode(head[1])
                    else:
                        result_head += head[0].decode('utf-8')
                else:
                    result_head += head[0].decode('utf-8')
        else:
            if len(header[0]) > 1:
                if header[0][1] is not None:
                    result_head += header[0][0].decode(header[0][1])
                else:
                    result_head += header[0][0]
            else:
                result_head += header[0][0].decode('utf-8')
        if result_head == '':
            result_head = "no data"
        return result_head, header[0][1]
