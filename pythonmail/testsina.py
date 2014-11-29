#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import logging
import ConfigParser

from mailnetease import MailSina
logging.basicConfig(level=logging.DEBUG,
        format='%(asctime)s %(name)s %(levelname)s %(message)s')

def test():
    log = logging.getLogger("test")
    config = ConfigParser.ConfigParser()
    config.read('conf.ini')
    username = config.get('sina', 'username')
    password = config.get('sina', 'password')
    mysina = MailSina(username, password)
    mysina.login()

    mailboxs = mysina.list_mailbox()
    log.debug("邮箱盒子列表如下：")
    for box in mailboxs:
        log.debug(box)


    """
    indexs = mysina.get_unread_mail()
    log.debug(u"共有%s封未读邮件", len(indexs))
    log.debug(u"未读邮件的编号为:%s", ' '.join(indexs))

    for index in indexs:
        mail = mysina.parse_mail(index)
        log.debug("subject:%s", mail['subject'])
        log.debug("from_name:%s", mail['from_name'])
        log.debug("from_addr:%s", mail['from_addr'])
        log.debug("date:%s", mail['date'])
        mysina.mark_as_unread(index)
        mysina.mark_as_answered(index)

    mysina.logout()
    
    mysina.smtp_login()
    #test send mail
    sender = 'mouselinux@sina.com'
    receiver = 'mouselinux@sina.com'
    #test mail plain
    subject = u'python 测试邮件-纯文本'
    txt = (u'你好','plain','utf-8')
    mysina.smtp_send_mail(sender, receiver, subject, txt)
    #test mail html
    subject = u'python 测试邮件-HTML'
    txt = (u'<html><h1>你好</h1></html>','html','utf-8')
    mysina.smtp_send_mail(sender, receiver, subject, txt)
    mysina.smtp_logout()
    """

if __name__ == "__main__":
    test()
