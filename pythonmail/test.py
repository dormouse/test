#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import smtplib
import email
from email.mime.text import MIMEText
from email.header import Header
from email.utils import getaddresses



import os
import re
import datetime
import logging
import imaplib
import ConfigParser
from imapclient import imap_utf7

logging.basicConfig(level=logging.DEBUG,
        format='%(asctime)s %(name)s %(levelname)s %(message)s')

#参考：https://docs.python.org/2/library/imaplib.html

class Mail163():
    def __init__(self, username, password):
        self.log = logging.getLogger("Mail163")
        self.imaphost = 'imap.163.com'
        self.smtphost = 'smtp.163.com'
        self.username = username
        self.password = password
        self.con = imaplib.IMAP4(self.imaphost)
    
    def login(self):
        self.con.login(self.username, self.password)
        self.con.select()
        self.log.debug('Login done.')

    def logout(self):
        self.con.close()
        self.con.logout()
        self.log.debug('Logout done.')

    def list_mailbox(self):
        resp, datas = self.con.list()
        if resp == 'OK':
            return [imap_utf7.decode(data) for data in datas]
        else:
            return None

    def parse_header(self, header_str):
        """解码象=?gbk?Q?=CF=E0=C6=AC.rar?=这样的字符串"""

        if header_str:
            txt, code = email.Header.decode_header(header_str)[0]
            if code:
                txt = txt.decode(code,'ignore')
            return txt
        else:
            return None


    def parse_mail(self, index):
        """解析整个邮件内容"""
        mail = {}
        resp, data = self.con.fetch(index, "(RFC822)")
        if resp == 'OK':
            text = data[0][1]
            msg = email.message_from_string(text)
            """
            msg.key(): ['Received', 'Content-Type', 'MIME-Version',
                'Content-Transfer-Encoding', 'Subject', 'X-CM-TRANSID',
                'Message-Id', 'X-Coremail-Antispam', 'X-Originating-IP',
                'Date', 'From', 'X-CM-SenderInfo']
            """
            mail['subject'] = self.parse_header(msg.get('Subject'))
            #From info
            name, addr = email.utils.parseaddr(msg.get('From'))
            mail['from_name'] = self.parse_header(name)
            mail['from_addr'] = addr
            mail['date'] = msg.get('Date')
            mail['contents'] = self.parse_msg(msg)
            """
            self.log.debug(email.utils.parseaddr(msg.get('From')))
            tos = msg.get_all('to', [])
            ccs = msg.get_all('cc', [])
            resent_tos = msg.get_all('resent-to', [])
            resent_ccs = msg.get_all('resent-cc', [])
            recipients_tos = getaddresses(tos)
            self.log.debug(recipients_tos)
            recipients_ccs = getaddresses(ccs)
            self.log.debug(recipients_ccs)
            recipients_resent_tos = getaddresses(resent_tos)
            self.log.debug(recipients_resent_tos)
            recipients_resent_ccs = getaddresses(resent_ccs)
            self.log.debug(recipients_resent_ccs)
            """
        return mail

    def parse_msg(self, msg):
        """解析邮件的内容块"""
        contents = []
        for part in msg.walk():        
            if not part.is_multipart():
                content = {}
                contenttype = part.get_content_type()     
                filename = part.get_filename()   
                if filename:
                    content['type'] = 'file'
                    h = Header(filename)
                    fname = self.parse_header(h)
                    fdata = part.get_payload(decode=True)
                    content['filename'] = fname
                    content['data'] = fdata
                    """
                    try:
                        f = open(fname, 'wb')
                    except:
                        today = datetime.date.today().strftime("Y%m%d")
                        fname = today+ self.autoindex
                        self.autoindex += 1
                        #附件名有非法字符，自动换一个
                        f = open(fanme, 'wb')
                    f.write(fdata)
                    f.close()
                    """
                else:
                    #不是附件，是文本内容
                    content['type'] = 'notfile'
                    content['data'] = part.get_payload(decode=True) 
                contents.append(content)
        return  contents

    def get_all_mail(self):
        self.con.login(self.username, self.password)
        self.con.select()
        # list items on server
        resp, items = self.con.search(None, "ALL")
        """
        ALL         All Messages.
        Recent      Message has not been read.
        Seen        Message has been read.
        Answered    Message has been answered.
        Flagged     Message is "flagged" for urgent/special attention.
        Deleted     Message has been deleted, python无法看到已删除邮件
        Draft       Message in Draft, python无法看到草稿箱内的邮件
        """
        if resp == 'OK':
            return items[0].split()
        else:
            self.log.error(u"收取邮件出错，响应代码：%s", resp)
            return None

    def get_unread_mail(self):
        """获得未读邮件的编号"""
        resp, items = self.con.search(None, "Recent")
        if resp == 'OK':
            return items[0].split()
        else:
            self.log.error(u"收取邮件出错，响应代码：%s", resp)
            return None

    def mark_as_unread(self, index):
        """把邮件标记为未读邮件"""
        self.con.store(index, '-FLAGS', '\\SEEN')

    def mark_as_answered(self, index):
        """把邮件标记为已回复邮件"""
        self.con.store(index, '+FLAGS', '\\Answered')

    def smtp_login(self):
        self.smtp = smtplib.SMTP()
        self.smtp.connect(self.smtphost)
        self.smtp.login(self.username, self.password)

    def smtp_send_mail(self, sender, receiver, subject, txt):
        text, subtype, charset = txt
        msg_txt = MIMEText(text, subtype, charset)
        msg_txt['Subject'] = Header(subject, 'utf-8')
        self.smtp.sendmail(sender, receiver, msg_txt.as_string())

    def smtp_logout(self):
        self.smtp.quit()



def test():
    log = logging.getLogger("test")
    config = ConfigParser.ConfigParser()
    config.read('conf.ini')
    username = config.get('163', 'username')
    password = config.get('163', 'password')
    my163 = Mail163(username, password)
    my163.login()

    mailboxs = my163.list_mailbox()
    log.debug("邮箱盒子列表如下：")
    for box in mailboxs:
        log.debug(box)

    indexs = my163.get_unread_mail()
    log.debug(u"共有%s封未读邮件", len(indexs))
    log.debug(u"未读邮件的编号为:%s", ' '.join(indexs))

    for index in indexs:
        mail = my163.parse_mail(index)
        log.debug("subject:%s", mail['subject'])
        log.debug("from_name:%s", mail['from_name'])
        log.debug("from_addr:%s", mail['from_addr'])
        log.debug("date:%s", mail['date'])
        my163.mark_as_unread(index)
        my163.mark_as_answered(index)

    my163.logout()
    
    my163.smtp_login()
    #test send mail
    sender = 'mouselinux@163.com'
    receiver = 'mouselinux@163.com'
    #test mail plain
    subject = u'python 测试邮件-纯文本'
    txt = (u'你好','plain','utf-8')
    my163.smtp_send_mail(sender, receiver, subject, txt)
    #test mail html
    subject = u'python 测试邮件-HTML'
    txt = (u'<html><h1>你好</h1></html>','html','utf-8')
    my163.smtp_send_mail(sender, receiver, subject, txt)
    my163.smtp_logout()

if __name__ == "__main__":
    test()

