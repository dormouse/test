#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import logging
import ConfigParser
import re

from mailnetease import Mail163
logging.basicConfig(level=logging.DEBUG,
        format='%(asctime)s %(name)s %(levelname)s %(message)s')

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

    x, y=my163.con.status('INBOX', '(MESSAGES UNSEEN)')
    messages=int(re.search('MESSAGES\s+(\d+)', y[0]).group(1))
    unseen=int(re.search('UNSEEN\s+(\d+)', y[0]).group(1))

    log.debug("total %s messages, unread %s", messages, unseen)
    
    """
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
    """

if __name__ == "__main__":
    test()
