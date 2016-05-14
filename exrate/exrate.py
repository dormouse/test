#!/usr/bin/env python
# -*- coding: UTF-8 -*

# 文件名: exrate.py
# 用途: 货币换算
# 创建时间: 2016/05/12
# 修改时间: 2016/05/14
# 作者: dormouse.young@gmail.com

import wx
import logging
import sys  

DEBUG = True
if DEBUG:
    logging.basicConfig(level=logging.DEBUG,
        format='%(asctime)s %(name)s %(levelname)s %(message)s')
else:
    logging.basicConfig(level=logging.INFO,
        format='%(asctime)s %(name)s %(levelname)s %(message)s')

ID_TC1 = 10
ID_TC2 = 20
RETURN_CODE = 13

class Rate():
    """ all about currency rate """
    def __init__(self):
        # 货币缩写来源：https://zh.wikipedia.org/wiki/ISO_4217
        # 汇率来源：招商银行 http://fx.cmbchina.com/hq/
        #           中国银行 http://www.boc.cn/sourcedb/whpj/index.html
        self.curr ={
                'rmb': {'name': u'人民币', 'rate': 10000},
                'hkd': {'name': u'港币', 'rate': 11909},
                'twd': {'name': u'新台币', 'rate': 49925},
                'usd': {'name': u'美元', 'rate': 1534},
        }
        self.name_en = self.curr.keys()
        self.name_zh = [self.curr[k]['name'] for k in self.name_en]
        self.rate = [self.curr[k]['rate'] for k in self.name_en]

    def GetNameZh(self, index):
        return self.name_zh[index]

    def GetNameEn(self, index):
        return self.name_en[index]

    def GetRate(self, index):
        return self.rate[index]

class MainFrame(wx.Frame):
    """
    This is MyFrame.  It just shows a few controls on a wxPanel,
    and has a simple menu.
    """
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, -1, title,
                          pos=(150, 150), size=(350, 250))
        self.log = logging.getLogger("main frame")  
        self.rate = Rate()
        
        # Create the menubar
        menuBar = wx.MenuBar()

        # and a menu 
        menu = wx.Menu()

        # add an item to the menu, using \tKeyName automatically
        # creates an accelerator, the third param is some help text
        # that will show up in the statusbar
        menu.Append(wx.ID_EXIT, "E&xit\tAlt-X", "Exit this simple sample")

        # bind the menu event to an event handler
        self.Bind(wx.EVT_MENU, self.OnClose, id=wx.ID_EXIT)

        # and put the menu on the menubar
        menuBar.Append(menu, "&File")
        self.SetMenuBar(menuBar)

        self.CreateStatusBar()
        

        # Now create the Panel to put the other controls on.
        panel = wx.Panel(self)

        # and a few controls
        text = wx.StaticText(panel, -1, u"汇率转换")
        text.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.BOLD))
        text.SetSize(text.GetBestSize())

        self.ch1 = wx.Choice(self, -1, (100, 50), choices = self.rate.name_zh)
        self.ch2 = wx.Choice(self, -1, (100, 50), choices = self.rate.name_zh)
        self.tc1 = wx.TextCtrl(self, ID_TC1, "0", size=(125, -1))
        self.tc2 = wx.TextCtrl(self, ID_TC2, "0", size=(125, -1))

        self.Bind(wx.EVT_CHOICE, self.EvtChoice, self.ch1)
        self.Bind(wx.EVT_CHOICE, self.EvtChoice, self.ch2)
        self.Bind(wx.EVT_TEXT, self.EvtText, self.tc1)
        self.Bind(wx.EVT_TEXT, self.EvtText, self.tc2)
        self.tc1.Bind(wx.EVT_CHAR, self.EvtChar)
        self.tc2.Bind(wx.EVT_CHAR, self.EvtChar)
        self.tc1.Bind(wx.EVT_SET_FOCUS, self.OnSetFocus)
        self.tc2.Bind(wx.EVT_SET_FOCUS, self.OnSetFocus)

        # Use a sizer to layout the controls, stacked vertically and with
        # a 10 pixel border around each

        gbs = self.gbs = wx.GridBagSizer(5, 5)
        gbs.Add(text, (0,0), (1,2), wx.ALIGN_CENTER | wx.ALL, 5)
        gbs.Add(self.ch1, (1,0))
        gbs.Add(self.tc1, (1,1))
        gbs.Add(self.ch2, (2,0))
        gbs.Add(self.tc2, (2,1))

        panel.SetSizer(gbs)
        panel.Layout()

        # And also use a sizer to manage the size of the panel such
        # that it fills the frame
        sizer = wx.BoxSizer()
        sizer.Add(panel, 1, wx.EXPAND, 5)
        self.SetSizer(sizer)
        

    def EvtChoice(self, event):
        self.log.debug('EvtChoice: %s\n' % event.GetString())

    def EvtText(self, event):
        txt = event.GetString()

    def EvtTextEnter(self, event):
        self.log.debug('EvtTextEnter\n')
        event.Skip()

    def EvtChar(self, event):
        self.log.debug('EvtChar1: %d\n' % event.GetKeyCode())
        key_code = event.GetKeyCode()
        if key_code == RETURN_CODE:
            self.calc()
        event.Skip()

    def calc(self):
        self.log.debug("start calc")
        self.log.debug("current ctrlid:")
        self.log.debug(self.ctrl_id)

        index = self.ch1.GetCurrentSelection()
        name_zh1 = self.rate.GetNameZh(index)
        rate1 = self.rate.GetRate(index)
        self.log.debug(u"ch1:%s，汇率：%s", name_zh1, rate1)

        index = self.ch2.GetCurrentSelection()
        name_zh2 = self.rate.GetNameZh(index)
        rate2 = self.rate.GetRate(index)
        self.log.debug(u"ch2:%s，汇率：%s", name_zh2, rate2)


        if self.ctrl_id == ID_TC1:
            txt = self.tc1.GetValue()
            try:
                twd = float(txt) * rate2 / rate1
                self.tc2.SetValue(str(twd))
            except Exception as e:
                self.log.error(e)

        if self.ctrl_id == ID_TC2:
            txt = self.tc2.GetValue()
            try:
                rmb = float(txt) * rate1 / rate2
                self.tc1.SetValue(str(rmb))
            except Exception as e:
                self.log.error(e)

    def OnClose(self, event):
        self.Close(True)

    def OnSetFocus(self, event):
        tc_id = event.GetWindow().GetId()
        self.log.debug('OnSetFocus: %d\n' % tc_id)
        if tc_id in [ID_TC1, ID_TC2]:
            self.ctrl_id = tc_id
        event.Skip()

if __name__ == '__main__':
    app = wx.App()
    frame = MainFrame(None, title=u"汇率转换")
    frame.Show()
    app.MainLoop()

