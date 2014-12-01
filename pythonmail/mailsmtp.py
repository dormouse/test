#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.header import Header

class MailSmtp():
    def __init__(self, uname, upass, host):
        self.uname = uname
        self.upass = upass
        self.host = host

    def smtp_login(self):
        self.smtp = smtplib.SMTP()
        self.smtp.connect(self.host)
        self.smtp.login(self.uname, self.upass)

    def smtp_send_mail(self, sender, receiver, subject, txt):
        text, subtype, charset = txt
        to_name, to_addr = receiver
        msg_txt = MIMEText(text, subtype, charset)
        msg_txt['Subject'] = Header(subject, 'utf-8')
        msg_txt['To'] = "%s <%s>"%(Header(to_name, 'utf-8'), to_addr)
        self.smtp.sendmail(sender, to_addr, msg_txt.as_string())

    def smtp_logout(self):
        self.smtp.quit()

