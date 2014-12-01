#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import logging
import ConfigParser
import cPickle as pickle

import poplib
import email
from email.mime.text import MIMEText
from email.header import Header

logging.basicConfig(level=logging.INFO,
        format='%(asctime)s %(name)s %(levelname)s %(message)s')

class MailPop3():
    def __init__(self, uname, upass, host):
        self.log = logging.getLogger("MailPop3")
        self.uname = uname
        self.upass = upass
        self.host = host
        if os.path.isfile("mails_seen.db"):
            f=open("mails_seen.db", "rb")
            self.mails_seen = pickle.load(f)
            f.close()
        else:
            self.mails_seen = []

    def decode_header_str(self, header_str):
        """解码形如： =?gbk?Q?=CF=E0=C6=AC.rar?= 的字符串 """

        if header_str:
            txt, code = email.Header.decode_header(header_str)[0]
            return txt.decode(code,'ignore') if code else txt
        else:
            return None

    def is_unread(self, message):
        index, msg = message
        msgid = msg['msgid']
        if msgid in self.mails_seen:
            return False
        else:
            self.mails_seen.append(msgid)
            f = open("mails_seen.db", "wb")
            pickle.dump(self.mails_seen, f)
            f.close()
            return True

    def is_vip(self, message):
        index, msg = message
        from_addr = msg['from_addr']
        if from_addr in self.vips:
            return True
        else:
            return False

    def login(self):
        self.con = poplib.POP3(self.host)
        try:
            self.con.user(self.uname)
            self.con.pass_(self.upass)
        except poplib.error_proto,e:
            self.log.error("Login fialed:")
            self.log.error(e)

    def logout(self):
        self.con.quit()
        
    def list_top14(self):
        resp, lines, octets = self.con.list()
        if resp[:3] == '+OK':
            indexs = [int(line.split()[0]) for line in lines]
            msgs = map(self.parse_mail_top14, indexs)
            return zip(indexs, msgs)
        else:
            self.log.error("mail server list error, resp:%s", resp)
            return []


    def parse_mail_top14(self, index):
        """parse mail top 14 lines"""

        resp, msg_lines, octet = self.con.top(index, 14)
        msg = email.message_from_string("\n".join(msg_lines))
        mail = {}
        mail['subject'] = self.decode_header_str(msg.get('Subject'))
        name, addr = email.utils.parseaddr(msg.get('From'))
        mail['from_name'] = self.decode_header_str(name)
        mail['from_addr'] = addr
        mail['date'] = msg.get('Date')
        mail['msgid'] = msg.get('Message-Id')
        return mail

    def parse_mail(self, index):
        """解析整个邮件内容"""
        resp, msg_lines, octet = self.con.retr(index)
        msg = email.message_from_string("\n".join(msg_lines))
        mail = {}
        """
        msg.keys(): ['Received', 'Content-Type', 'MIME-Version',
            'Content-Transfer-Encoding', 'Subject', 'X-CM-TRANSID',
            'Message-Id', 'X-Coremail-Antispam', 'X-Originating-IP',
            'Date', 'From', 'X-CM-SenderInfo']
        """
        mail['subject'] = self.decode_header_str(msg.get('Subject'))
        #From info
        name, addr = email.utils.parseaddr(msg.get('From'))
        mail['from_name'] = self.decode_header_str(name)
        mail['from_addr'] = addr
        mail['date'] = msg.get('Date')
        mail['contents'] = self.parse_content(msg)
        return mail

    def parse_content(self, msg):
        """解析邮件的内容块"""
        contents = []
        parts = [part for part in msg.walk() if not part.is_multipart()]
        for part in parts:
            content = {}
            contenttype = part.get_content_type()     
            self.log.debug("type:%s"%contenttype)
            filename = part.get_filename()   
            if filename:
                content['type'] = 'file'
                content['filename'] = self.decode_header_str(Header(filename))
                self.log.debug("filename:%s"%content['filename'])
            else:
                #不是附件，是文本内容
                content['type'] = 'notfile'
            content['data'] = part.get_payload(decode=True) 
            self.log.debug(content['type'])
            contents.append(content)
        return  contents

    def set_vip(self, vips):
        self.vips = vips

    def status(self):
        """get mail count and mail size"""
        msg_count, msg_size = self.con.stat()
        return (msg_count, msg_size)

def test():
    log = logging.getLogger("test")
    config = ConfigParser.ConfigParser()
    config.read('conf.ini')
    username = config.get('163', 'username')
    password = config.get('163', 'password')
    my163 = MailPop3(username, password, 'pop.163.com')
    my163.login()
    msgids = my163.list_msgid()
    my163.logout()

if __name__ == "__main__":
    test()

