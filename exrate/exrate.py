#!/usr/bin/env python
# -*- coding: UTF-8 -*

# 文件名: exrate.py
# 版本: 0.1
# 用途: 货币换算
# 创建时间: 2016/05/12
# 修改时间: 2016/05/14
# 作者: dormouse.young@gmail.com
# Change log:
#     2016/05/16 显示为两位小数
#     2016/05/18 从中国银行网页（已经保存的本文件）读入汇率，记录当前选择

import json
import logging
import os
import sys
import wx
from getrate import BocRate

DEBUG = True
if DEBUG:
    level = logging.DEBUG
else:
    level = logging.INFO
logging.basicConfig(level=level,
                    format='%(asctime)s %(name)s %(levelname)s %(message)s')

RETURN_CODE = 13


class Rate():
    """ all about currency rate """

    def __init__(self):
        # 货币缩写来源：https://zh.wikipedia.org/wiki/ISO_4217
        # 汇率来源：招商银行 http://fx.cmbchina.com/hq/
        #           中国银行 http://www.boc.cn/sourcedb/whpj/index.html
        self.curr = BocRate().GetRate()
        self.name_en = [item[0] for item in self.curr]
        self.name_zh = [item[1] for item in self.curr]
        self.rate = [item[2] for item in self.curr]

    def GetNameZh(self, index):
        """ 获得中文名称 """
        return self.name_zh[index]

    def GetNameEn(self, index):
        """ 获得英文名称 """
        return self.name_en[index]

    def GetRate(self, index):
        """ 获得汇率 """
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
        self.conf_file = 'conf.json'
        self.LoadConf()

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

        # make controls
        self.chs = map(self.MakeCh, range(
            self.conf['ch_count']))  # all Choice contrls
        self.tcs = map(self.MakeTc, range(
            self.conf['ch_count']))  # all TextCtrls
        self.tc_ids = map(self.GetTcId, self.tcs)  # all TextCtrls Ids

        # Set default selection in choices
        for index, ch in enumerate(self.chs):
            ch.SetSelection(self.conf['chs'][index])

        # Bind all controls
        for ch in self.chs:
            self.Bind(wx.EVT_CHOICE, self.EvtChoice, ch)

        for tc in self.tcs:
            self.Bind(wx.EVT_TEXT, self.EvtText, tc)
            tc.Bind(wx.EVT_CHAR, self.EvtChar)
            tc.Bind(wx.EVT_SET_FOCUS, self.OnSetFocus)

        self.Bind(wx.EVT_CLOSE, self.OnClose)

        # Use a sizer to layout the controls, stacked vertically and with
        # a 10 pixel border around each
        gbs = self.gbs = wx.GridBagSizer(5, 5)
        for index, ch in enumerate(self.chs):
            gbs.Add(ch, (index, 0))
        for index, tc in enumerate(self.tcs):
            gbs.Add(tc, (index, 1))
        panel.SetSizer(gbs)
        panel.Layout()

        # And also use a sizer to manage the size of the panel such
        # that it fills the frame
        sizer = wx.BoxSizer()
        sizer.Add(panel, 1, wx.EXPAND, 5)
        self.SetSizer(sizer)

    def GetTcId(self, tc):
        return tc.GetId()

    def MakeCh(self, index):
        ch = wx.Choice(self, wx.NewId(), (100, 50), choices=self.rate.name_zh)
        return ch

    def MakeTc(self, index):
        tc = wx.TextCtrl(self, wx.NewId(), "0", size=(125, -1))
        return tc

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
        self.log.debug("current ctrlid:%s", self.ctrl_id)

        # get base textctrl index and base rate
        base_index = self.tc_ids.index(self.ctrl_id)
        base_value = float(self.tcs[base_index].GetValue())
        base_rate = self.rate.GetRate(
            self.chs[base_index].GetCurrentSelection())

        # set other textctrl's value
        for index, tc in enumerate(self.tcs):
            if base_index != index:
                target_rate = self.rate.GetRate(
                    self.chs[index].GetCurrentSelection())
                target_value = base_value * base_rate / target_rate
                format_value = float('%.2f' % target_value)
                tc.SetValue(str(format_value))

    def OnClose(self, event):
        self.SaveConf()
        self.Destroy()
        # self.Close(True)

    def OnSetFocus(self, event):
        tc_id = event.GetWindow().GetId()
        self.log.debug('OnSetFocus: %d\n' % tc_id)
        if tc_id in self.tc_ids:
            self.ctrl_id = tc_id
        event.Skip()

    def LoadConf(self):
        """
        if os.path.exists(self.conf_file):
            with open(self.conf_file) as fp:
                self.conf = json.load(fp)
        else:
            self.conf = {'chs': [0, 1, 2, 3, 4]}
        """
        try:
            with open(self.conf_file) as fp:
                self.conf = json.load(fp)
        except:
            self.conf = {
                "ch_count": 5,  # MAX five line
                'chs': [0, 1, 2, 3, 4]}

    def SaveConf(self):
        # save currency selection
        self.conf['chs'] = [ch.GetCurrentSelection() for ch in self.chs]
        with open(self.conf_file, 'w') as fp:
            json.dump(self.conf, fp)

if __name__ == '__main__':
    app = wx.App()
    frame = MainFrame(None, title=u"汇率转换")
    frame.Show()
    app.MainLoop()
