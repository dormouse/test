#!/usr/bin/env python
# -*- coding: UTF-8 -*

# 文件名: getrate.py
# 版本: 0.1
# 用途: 分析中国银行网页，得到汇率
# 创建时间: 2016/05/16
# 修改时间: 2016/05/16
# 作者: dormouse.young@gmail.com
# Change log:

from bs4 import BeautifulSoup


class BocRate(object):
    """ analysis web page of BOC, get currency exchange rate"""
    cur_code = [
        (u"AED", u"阿联酋迪拉姆"),
        (u"AUD", u"澳大利亚元"),
        (u"BRL", u"巴西里亚尔"),
        (u"CAD", u"加拿大元"),
        (u"CHF", u"瑞士法郎"),
        (u"DKK", u"丹麦克朗"),
        (u"EUR", u"欧元"),
        (u"GBP", u"英镑"),
        (u"HKD", u"港币"),
        (u"IDR", u"印尼卢比"),
        (u"INR", u"印度卢比"),
        (u"JPY", u"日元"),
        (u"KRW", u"韩国元"),
        (u"MOP", u"澳门元"),
        (u"MYR", u"林吉特"),
        (u"NOK", u"挪威克朗"),
        (u"NZD", u"新西兰元"),
        (u"PHP", u"菲律宾比索"),
        (u"RUB", u"卢布"),
        (u"SEK", u"瑞典克朗"),
        (u"SGD", u"新加坡元"),
        (u"THB", u"泰国铢"),
        (u"TWD", u"新台币"),
        (u"USD", u"美元"),
        (u"ZAR", u"南非兰特"),
    ]

    def __init__(self):
        super(BocRate, self).__init__()
        self.name_zh_dict = {key: value for value, key in self.cur_code}
        self.name_en_dict = {key: value for key, value in self.cur_code}
        url = 'http://www.boc.cn/sourcedb/whpj/index.html'
        local_file = 'boc.htm'
        with open(local_file) as f:
            self.soup = BeautifulSoup(f.read(), "html.parser")

    def GetCols(self, row):
        cols = row.find_all('td')
        name_zh = cols[0].string
        name_en = self.name_zh_dict[name_zh]
        rate = cols[5].string
        return (name_en, name_zh, float(rate))

    def GetRate(self):
        table = self.soup.find_all('table')[1]
        rows = table.find_all('tr')
        rates = [(u'RMB', u'人民币', 100), ] + map(self.GetCols, rows[1:])
        return rates


class Iso4217(object):
    """get corrency englist name and chinese name from Iso4217"""

    def __init__(self):
        super(Iso4217, self).__init__()
        url = 'https://zh.wikipedia.org/wiki/ISO_4217'
        local_file = 'ISO4217.htm'
        with open(local_file) as f:
            self.soup = BeautifulSoup(f.read(), "html.parser")

    def GetCols(self, row):
        cols = row.find_all('td')
        name_en = cols[0].string
        name_zh = cols[3].get_text()
        return (name_en, name_zh)

    def GetName(self):
        table = self.soup.find_all('table', class_='wikitable sortable')[0]
        rows = table.find_all('tr')
        names = map(self.GetCols, rows[1:])
        return names


def test_Iso4217():
    names = Iso4217().GetName()
    for name_en, name_zh in names:
        print name_en, name_zh


def test_BocRate():
    rates = BocRate().GetRate()
    for name_en, name_zh, rate in rates:
        print name_en, name_zh, rate

if __name__ == "__main__":
    test_BocRate()
