#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import smtplib
import email
from email.mime.text import MIMEText
from email.header import Header

import os
import re
import datetime
import imaplib
import ConfigParser
from imapclient import imap_utf7

from pprint import pprint

#参考：https://docs.python.org/2/library/imaplib.html

sender = 'mouselinux@163.com'
receiver = 'mouselinux@163.com'

class MailImap163():
    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password
        self.con = imaplib.IMAP4(self.host)
        self.auto_index = 0 #用于重命名含有非法字符的附件

    def list_mailbox(self):
        self.con.login(self.username, self.password)
        try:
            resp, data = self.con.list()
            print 'Response code:', resp
            print 'Response:'
            for i in data:
                print i
                print imap_utf7.decode(i)
        finally:
            self.con.logout()

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
        mail = {}
        resp, data = self.con.fetch(index, "(RFC822)")
        if resp == 'OK':
            text = data[0][1]
            msg = email.message_from_string(text)
            """
            msgkeys: ['Received', 'Content-Type', 'MIME-Version',
                'Content-Transfer-Encoding', 'Subject', 'X-CM-TRANSID',
                'Message-Id', 'X-Coremail-Antispam', 'X-Originating-IP',
                'Date', 'From', 'X-CM-SenderInfo']
            """
            mail['subject'] = self.parse_header(msg.get('Subject'))
            mail['from'] = msg.get('From')
            mail['date'] = msg.get('Date')
            mail['content'] = self.parse_msg(msg)

        """
        for i in items[0].split():
            resp, mailData = self.con.fetch(i, "(RFC822)")    ##读取邮件信息
            mailText = mailData[0][1]
            mail_message = email.message_from_string(mailText)
            mailContentDict = self.parse_mail(mail_message)
            nowTime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            #print mail_message

            print mail_message['subject']
            print mail_message['from']
            print mail_message['to']
            #pprint(mailContentDict)
            
        time.sleep(0)

        mailFile = StringIO.StringIO(mailText)
        mailMessage = rfc822.Message(mailFile)
        print message['from']
        newMail = dict(mailMessage.items())
        mailMessage.fp.read()
        #server.store(items[i], '+FLAGS', '\\Deleted')##删除指定的一份邮件
        """
        return mail

    def parse_msg(self, msg):
        mailContent = ''
        for part in msg.walk():        
            if not part.is_multipart():
                contenttype = part.get_content_type()     
                filename = part.get_filename()   
                if filename:
                    h = Header(filename)
                    fname = self.parse_header(h)
                    fdata = part.get_payload(decode=True) 
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
                else:
                    #不是附件，是文本内容
                    mailContent =  part.get_payload(decode=True) 
        return  mailContent

    def get_all_mail(self):
        self.con.login(self.username, self.password)
        self.con.select()
        # list items on server
        resp, items = self.con.search(None, "ALL")       #all Message.
        #mailResp, items = self.con.search(None, "Recent")    #Message has not been read.
        #resp, items = self.con.search(None, "Seen")      #Message has been read.
        #resp, items = self.con.search(None, "Answered")   #Message has been answered.
        #resp, items = self.con.search(None, "Flagged")   #Message is "flagged" for urgent/special attention.
        #resp, items = self.con.search(None, "Deleted")   ##python无法看到已删除邮件                                                                       
        #resp, items = self.con.search(None, "Draft")     ##python无法看到草稿箱内的邮件
        if resp == 'OK':
            mail_index = items[0].split()
            print u"一共有%s封邮件"%len(mail_index)
        else:
            print u"收取邮件出错，响应代码：%s"%resp

        self.con.close()
        self.con.logout()

    
    def get_unread_mail(self):
        self.con.login(self.username, self.password)
        self.con.select()
        resp, items = self.con.search(None, "Recent")
        if resp == 'OK':
            indexs = items[0].split()
            print u"共有%s封未读邮件"%len(indexs)
            print u"未读邮件的编号为:", indexs
            for index in indexs:
                mail = self.parse_mail(index)
                #for test start
                print 'subject:', mail['subject']
                print 'from:', mail['from']
                print 'date:', mail['date']
                self.mark_as_unread(index)
                #for test end

        else:
            print u"收取邮件出错，响应代码：%s"%resp
        self.con.close()
        self.con.logout()

    def mark_as_unread(self, index):
        self.con.store(index, '-FLAGS', '\SEEN')

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
    #my163.list_mailbox()
    my163.get_unread_mail()

if __name__ == "__main__":
    #smtp_send_mail()
    test()

