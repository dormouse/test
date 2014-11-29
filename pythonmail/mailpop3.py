#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import logging
import ConfigParser

import poplib
import email
from email.mime.text import MIMEText
from email.header import Header

logging.basicConfig(level=logging.DEBUG,
        format='%(asctime)s %(name)s %(levelname)s %(message)s')

#参考：https://docs.python.org/2/library/imaplib.html

class MailNetease():
    def __init__(self, uname, upass, host):
        self.log = logging.getLogger("MailNetease")
        self.uname = uname
        self.upass = upass
        self.host = host

    def login(self):
        self.con = poplib.POP3(self.host)
        try:
            self.con.user(self.uname)
            self.con.pass_(self.upass)
        except poplib.error_proto,e:
            self.log.error("Login fialed:")
            self.log.error(e)
        self.log.debug('Login done.')

    def logout(self):
        self.con.quit()
        self.log.debug('Logout done.')
        
    def status(self):
        msg_count, msg_size = self.con.stat()
        self.log.debug("%s mails, size:%s", msg_count, msg_size)

    def list_mail(self):
        l = self.con.list()
        self.log.debug(l)
        mails = self.con.list()[1]
        self.log.debug(mails)
        uids = self.con.uidl()
        self.log.debug(uids)

def test():
    log = logging.getLogger("test")
    config = ConfigParser.ConfigParser()
    config.read('conf.ini')
    username = config.get('163', 'username')
    password = config.get('163', 'password')
    my163 = MailNetease(username, password, 'pop.163.com')
    my163.login()

    #my163.status()
    my163.list_mail()

    my163.logout()

if __name__ == "__main__":
    test()

