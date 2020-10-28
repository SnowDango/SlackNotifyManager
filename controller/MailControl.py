import re
import imaplib
import email
import email.parser
import email.header
import email.utils
import json


class MailControl:

    def __init__(self):
        self.imap = imaplib.IMAP4_SSL("imap.gmail.com", '993')
        self.keys = json.load(open('', 'r'))
        self.UserName = self.keys["user_name"]
        self.PassWord = self.keys["pass"]

    msg_id_re = re.compile(r"<([^>]+)>")
    rcv_date_re = re.compile(r"^(?:.+)\s+for\s?<[^>]+>\s?;\s?([A-Za-z]{3}\s?,\s?[0-9]+\s+[A-Za-z]{3}\s+[0-9]{4}\s+[0-9]+:[0-9]+:[0-9]+\s+[\+\-]?[0-9]{4})", re.MULTILINE | re.DOTALL)
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
            email_data = email.message_from_bytes(body)
            header = email.header.decode_header(email_data.get('Subject'))
            log_header.append(header)
            msg_encoding = header[0][1] or 'iso-2022-jp'
            if not email_data.is_multipart():  # シングルパート
                byt = bytearray(email.get_payload(), msg_encoding)
                body = byt.decode(encoding=msg_encoding)
                bodys.append(body)
                log_header.append(header)
            else:  # マルチパート
                prt = email_data.get_payload()[0]
                byt = prt.get_payload(decode=True)
                body = byt.decode(encoding=msg_encoding)
                bodys.append(body)
                log_header.append(header)
        print('mail scan : {}'.format(log_header))
        return bodys
