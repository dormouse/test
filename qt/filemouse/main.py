#!/usr/bin/python3
# -*- coding: utf8 -*-

# Create:   2015-07-09
# Modify:   2015-07-16
# Author:   Dormouse Young
# Email:    dormouse dot young at gmail dot com
# Licence:  GPLv3

# Todo:
#    show permission

# History:
#
#

# Knowing bug:
# 1. If no dir in path, will not select default item

import sys

from PyQt5.QtCore import (QFile, QFileInfo, QPoint, QRect, QSettings, QSize,
                          Qt, QTextStream)
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWidgets import (
    QAction,
    QApplication,
    QFileDialog,
    QMainWindow,
    QMessageBox,
    QSplitter,
    QTextEdit,
    QFileSystemModel,
    QTreeView)

__author__ = 'dormouse'
__version__ = '0.1'

class FileTree(QTreeView):
    def __init__(self):
        super(FileTree, self).__init__()
        self.model = QFileSystemModel()
        self.model.setRootPath('')
        self.setModel(self.model)
        self.setAnimated(False)
        self.setIndentation(20)
        self.setSortingEnabled(True)


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.createActions()
        self.createMenus()
        # self.createToolBars()
        self.createStatusBar()

        treeLeft = FileTree()
        treeRight = FileTree()
        sp = QSplitter(Qt.Horizontal)
        sp.addWidget(treeLeft)
        sp.addWidget(treeRight)

        self.setCentralWidget(sp)
        self.resize(640, 480)

    def about(self):
        QMessageBox.about(self, "About Application",
                "The <b>Application</b> example demonstrates how to write "
                "modern GUI applications using Qt, with a menu bar, "
                "toolbars, and a status bar.")

    def closeEvent(self, event):
        self.writeSettings()
        event.accept()

    def createActions(self):
        self.exitAct = QAction(
            "E&xit",
            self,
            shortcut="Ctrl+Q",
            statusTip="Exit the application",
            triggered=self.close)

        """
        self.copyAct = QAction(
            QIcon(':/images/copy.png'),
            "&Copy",
            self,
            shortcut=QKeySequence.Copy,
            statusTip="Copy the current selection's contents to the clipboard",
            triggered=self.textEdit.copy)
        """

        self.aboutAct = QAction("&About", self,
                                statusTip="Show the application's About box",
                                triggered=self.about)

        self.aboutQtAct = QAction("About &Qt", self,
                                  statusTip="Show the Qt library's About box",
                                  triggered=QApplication.instance().aboutQt)

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.exitAct)
        self.editMenu = self.menuBar().addMenu("&Edit")
        # self.editMenu.addAction(self.copyAct)
        self.menuBar().addSeparator()
        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)

    def createStatusBar(self):
        self.statusBar().showMessage("Ready")

    def readSettings(self):
        settings = QSettings("Trolltech", "Application Example")
        pos = settings.value("pos", QPoint(200, 200))
        size = settings.value("size", QSize(400, 400))
        self.resize(size)
        self.move(pos)

    def writeSettings(self):
        settings = QSettings("Trolltech", "Application Example")
        settings.setValue("pos", self.pos())
        settings.setValue("size", self.size())

if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
