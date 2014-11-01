#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.header import Header

import imaplib
import os
import ConfigParser
import re
import pprint
from imapclient import imap_utf7

#参考：https://docs.python.org/2/library/imaplib.html

sender = 'mouselinux@163.com'
receiver = 'mouselinux@163.com'

class MailImap163():
    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password
        self.ipc = imaplib.IMAP4(self.host)

    def list_mailbox(self):
        self.ipc.login(self.username, self.password)
        try:
            code, data = self.ipc.list()
            print 'Response code:', code
            print 'Response:'
            print type(data)
            for i in data:
                print imap_utf7.decode(i)
        finally:
            self.ipc.logout()

def smtp_send_mail():

    subject = u'python 测试邮件-纯文本'
    msg_txt = MIMEText(u'你好','plain','utf-8')
    msg_txt['Subject'] = Header(subject, 'utf-8')

    subject = u'python 测试邮件-HTML'
    msg_htm = MIMEText(u'<html><h1>你好</h1></html>','html','utf-8')
    msg_htm['Subject'] = subject

    smtp = smtplib.SMTP()
    smtp.connect(smtpserver)
    smtp.login(username, password)

    #smtp.sendmail(sender, receiver, msg_txt.as_string())
    smtp.sendmail(sender, receiver, msg_htm.as_string())

    smtp.quit()

def test():
    config = ConfigParser.ConfigParser()
    config.read('conf.ini')
    host = config.get('163', 'imaphost')
    username = config.get('163', 'username')
    password = config.get('163', 'password')
    my163 = MailImap163(host, username, password)
    my163.list_mailbox()

if __name__ == "__main__":
    #smtp_send_mail()
    test()

