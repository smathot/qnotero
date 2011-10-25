# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/preferences.ui'
#
# Created: Tue Oct 25 16:50:08 2011
#      by: PyQt4 UI code generator 4.8.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Preferences(object):
    def setupUi(self, Preferences):
        Preferences.setObjectName(_fromUtf8("Preferences"))
        Preferences.resize(460, 296)
        Preferences.setWindowTitle(QtGui.QApplication.translate("Preferences", "Preferences", None, QtGui.QApplication.UnicodeUTF8))
        self.gridLayout = QtGui.QGridLayout(Preferences)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(Preferences)
        self.label.setText(QtGui.QApplication.translate("Preferences", "Zotero folder", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)
        self.lineEditZoteroPath = QtGui.QLineEdit(Preferences)
        self.lineEditZoteroPath.setObjectName(_fromUtf8("lineEditZoteroPath"))
        self.gridLayout.addWidget(self.lineEditZoteroPath, 2, 1, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(Preferences)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 7, 0, 1, 4)
        self.pushButtonZoteroPathBrowse = QtGui.QPushButton(Preferences)
        self.pushButtonZoteroPathBrowse.setText(QtGui.QApplication.translate("Preferences", "Browse", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonZoteroPathBrowse.setObjectName(_fromUtf8("pushButtonZoteroPathBrowse"))
        self.gridLayout.addWidget(self.pushButtonZoteroPathBrowse, 2, 2, 1, 1)
        self.pushButtonZoteroPathAutoDetect = QtGui.QPushButton(Preferences)
        self.pushButtonZoteroPathAutoDetect.setText(QtGui.QApplication.translate("Preferences", "Auto-detect", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonZoteroPathAutoDetect.setObjectName(_fromUtf8("pushButtonZoteroPathAutoDetect"))
        self.gridLayout.addWidget(self.pushButtonZoteroPathAutoDetect, 2, 3, 1, 1)
        self.checkBoxAttachToSysTray = QtGui.QCheckBox(Preferences)
        self.checkBoxAttachToSysTray.setText(QtGui.QApplication.translate("Preferences", "Attach Qnotero window to system tray icon", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxAttachToSysTray.setObjectName(_fromUtf8("checkBoxAttachToSysTray"))
        self.gridLayout.addWidget(self.checkBoxAttachToSysTray, 5, 0, 1, 4)
        self.label_2 = QtGui.QLabel(Preferences)
        self.label_2.setText(QtGui.QApplication.translate("Preferences", "Theme", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 4, 0, 1, 1)
        self.comboBoxTheme = QtGui.QComboBox(Preferences)
        self.comboBoxTheme.setObjectName(_fromUtf8("comboBoxTheme"))
        self.gridLayout.addWidget(self.comboBoxTheme, 4, 1, 1, 3)
        self.widget = QtGui.QWidget(Preferences)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.widget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.labelTitleMsg = QtGui.QLabel(self.widget)
        self.labelTitleMsg.setText(QtGui.QApplication.translate("Preferences", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Qnotero [version]</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt; font-style:italic;\">Copyright 2011 Sebastiaan Mathot</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt; font-style:italic;\">http://www.cogsci.nl/</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.labelTitleMsg.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.labelTitleMsg.setObjectName(_fromUtf8("labelTitleMsg"))
        self.horizontalLayout.addWidget(self.labelTitleMsg)
        self.gridLayout.addWidget(self.widget, 0, 0, 1, 4)
        self.labelLocatePath = QtGui.QLabel(Preferences)
        self.labelLocatePath.setText(QtGui.QApplication.translate("Preferences", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.labelLocatePath.setObjectName(_fromUtf8("labelLocatePath"))
        self.gridLayout.addWidget(self.labelLocatePath, 3, 0, 1, 4)
        self.checkBoxAutoUpdateCheck = QtGui.QCheckBox(Preferences)
        self.checkBoxAutoUpdateCheck.setText(QtGui.QApplication.translate("Preferences", "Automatically check for updates on start-up", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxAutoUpdateCheck.setObjectName(_fromUtf8("checkBoxAutoUpdateCheck"))
        self.gridLayout.addWidget(self.checkBoxAutoUpdateCheck, 6, 0, 1, 4)
        self.labelFirstRun = QtGui.QLabel(Preferences)
        self.labelFirstRun.setText(QtGui.QApplication.translate("Preferences", "This appears to be the first time that you run Qnotero! Getting started is easy, all you need to do is locate the Zotero folder. if you don\'t know where the Zotero folder is located, you can use the auto-detect function (but this may take a while).", None, QtGui.QApplication.UnicodeUTF8))
        self.labelFirstRun.setTextFormat(QtCore.Qt.PlainText)
        self.labelFirstRun.setWordWrap(True)
        self.labelFirstRun.setObjectName(_fromUtf8("labelFirstRun"))
        self.gridLayout.addWidget(self.labelFirstRun, 1, 0, 1, 4)

        self.retranslateUi(Preferences)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Preferences.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Preferences.reject)
        QtCore.QMetaObject.connectSlotsByName(Preferences)

    def retranslateUi(self, Preferences):
        pass

