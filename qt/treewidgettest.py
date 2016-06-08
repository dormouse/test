#!/usr/bin/python3
# -*- coding: utf8 -*-
# Filename: qt5test.py
# Purpose:  do some pyqt5 test
# Create:   2016-06-04
# Modify:   2016-06-04
# Author:   Dormouse Young
# Email:    dormouse dot young at gmail dot com
# Licence:  GPLv3

# Todo:
#

# History:
#
#

# Knowing bug:
#
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import (QAction, QActionGroup, QApplication, QFrame,
                             QLabel, QMainWindow, QMenu, QMessageBox,
                             QSizePolicy, QTreeWidget, QTreeWidgetItem,
                             QVBoxLayout, QWidget)


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.tree = self.createTree()
        self.tree.itemActivated.connect(self.onItemActivated)
        self.setWindowTitle('要Simple')
        self.status = self.statusBar()
        self.status.showMessage("This is StatusBar", 5000)
        self.setWindowTitle("PyQt MianWindow")
        self.setCentralWidget(self.tree)
        self.resize(250, 150)
        self.move(300, 300)

    def onItemActivated(self, item, col):
        print("hello %s" % item.text(0))

    def createTree(self):
        tree = QTreeWidget()
        tree.setColumnCount(1)
        root = QTreeWidgetItem(tree)
        root.setText(0, 'root')

        child1 = QTreeWidgetItem(root)
        child1.setText(0, 'child1')
        child1.setText(1, 'name1')
        child2 = QTreeWidgetItem(root)
        child2.setText(0, 'child2')
        child2.setText(1, 'name2')
        child3 = QTreeWidgetItem(root)
        child3.setText(0, 'child3')
        child4 = QTreeWidgetItem(child3)
        child4.setText(0, 'child4')
        child4.setText(1, 'name4')
        tree.addTopLevelItem(root)
        return tree


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
