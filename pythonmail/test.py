#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import smtplib
import email
from email.mime.text import MIMEText
from email.header import Header

import os
import re
import time
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
        self.ipc = imaplib.IMAP4(self.host)

    def list_mailbox(self):
        self.ipc.login(self.username, self.password)
        try:
            resp, data = self.ipc.list()
            print 'Response code:', resp
            print 'Response:'
            for i in data:
                print imap_utf7.decode(i)
        finally:
            self.ipc.logout()

    def parse_mail(self, msg):
        # 循环信件中的每一个mime的数据块
        mailContentDict = {}
        fileList = []
        mailContent = ''
        for part in msg.walk():        
            if not part.is_multipart(): # 这里要判断是否是multipart，是的话，里面的数据是无用的，至于为什么可以了解mime相关知识。
                contenttype = part.get_content_type()     
                filename = part.get_filename()   
                if filename:
                    # 下面的三行代码只是为了解码象=?gbk?Q?=CF=E0=C6=AC.rar?=这样的文件名
                    h = email.Header.Header(filename)
                    dh = email.Header.decode_header(h)
                    fname = dh[0][0]
                    encodeStr = dh[0][1]
                    #将附件名转换为unicode
                    fname = fname.decode(encodeStr,'ignore') 
                    data = part.get_payload(decode=True) # 解码出附件数据，然后存储到文件中
                    fileDict = {}
                    fileDict["fileName"] = fname
                    fileDict["fileContent"] = data
                    fileList.append(fileDict)                
                else:
                    #不是附件，是文本内容
                    mailContent =  part.get_payload(decode=True) # 解码出文本内容，直接输出来就可以了。            
        
        mailContentDict["mailContent"] = mailContent
        mailContentDict["fileList"] = fileList 
        return  mailContentDict

    def get_unread_mail(self):
        self.ipc.login(self.username, self.password)
        self.ipc.select()
        # list items on server
        resp, items = self.ipc.search(None, "ALL")       #all Message.
        #mailResp, items = self.ipc.search(None, "Recent")    #Message has not been read.
        #resp, items = self.ipc.search(None, "Seen")      #Message has been read.
        #resp, items = self.ipc.search(None, "Answered")   #Message has been answered.
        #resp, items = self.ipc.search(None, "Flagged")   #Message is "flagged" for urgent/special attention.
        #resp, items = self.ipc.search(None, "Deleted")   ##python无法看到已删除邮件                                                                       
        #resp, items = self.ipc.search(None, "Draft")     ##python无法看到草稿箱内的邮件
        if resp == 'OK':
            mail_index = items[0].split()
            print u"一共有%s封邮件"%len(mail_index)
        else:
            print u"收取邮件出错，响应代码：%s"%resp

        self.ipc.close()
        self.ipc.logout()
            
        """
        for i in items[0].split():
            resp, mailData = self.ipc.fetch(i, "(RFC822)")    ##读取邮件信息
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

