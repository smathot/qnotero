# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/qnotero.ui'
#
# Created: Tue Oct 25 15:42:52 2011
#      by: PyQt4 UI code generator 4.8.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Qnotero(object):
    def setupUi(self, Qnotero):
        Qnotero.setObjectName(_fromUtf8("Qnotero"))
        Qnotero.resize(400, 577)
        Qnotero.setMinimumSize(QtCore.QSize(400, 0))
        Qnotero.setWindowTitle(QtGui.QApplication.translate("Qnotero", "Qnotero", None, QtGui.QApplication.UnicodeUTF8))
        self.centralwidget = QtGui.QWidget(Qnotero)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.widgetSearch = QtGui.QWidget(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widgetSearch.sizePolicy().hasHeightForWidth())
        self.widgetSearch.setSizePolicy(sizePolicy)
        self.widgetSearch.setObjectName(_fromUtf8("widgetSearch"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.widgetSearch)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.lineEditQuery = QtGui.QLineEdit(self.widgetSearch)
        self.lineEditQuery.setMinimumSize(QtCore.QSize(0, 32))
        self.lineEditQuery.setFrame(False)
        self.lineEditQuery.setObjectName(_fromUtf8("lineEditQuery"))
        self.horizontalLayout.addWidget(self.lineEditQuery)
        self.pushButtonSearch = QtGui.QPushButton(self.widgetSearch)
        self.pushButtonSearch.setText(_fromUtf8(""))
        self.pushButtonSearch.setIconSize(QtCore.QSize(32, 32))
        self.pushButtonSearch.setFlat(True)
        self.pushButtonSearch.setObjectName(_fromUtf8("pushButtonSearch"))
        self.horizontalLayout.addWidget(self.pushButtonSearch)
        self.verticalLayout.addWidget(self.widgetSearch)
        self.labelResultMsg = QtGui.QLabel(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelResultMsg.sizePolicy().hasHeightForWidth())
        self.labelResultMsg.setSizePolicy(sizePolicy)
        self.labelResultMsg.setText(QtGui.QApplication.translate("Qnotero", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.labelResultMsg.setObjectName(_fromUtf8("labelResultMsg"))
        self.verticalLayout.addWidget(self.labelResultMsg)
        self.listWidgetResults = QnoteroResults(self.centralwidget)
        self.listWidgetResults.setFrameShape(QtGui.QFrame.NoFrame)
        self.listWidgetResults.setDragEnabled(True)
        self.listWidgetResults.setDragDropMode(QtGui.QAbstractItemView.DragOnly)
        self.listWidgetResults.setDefaultDropAction(QtCore.Qt.CopyAction)
        self.listWidgetResults.setObjectName(_fromUtf8("listWidgetResults"))
        self.verticalLayout.addWidget(self.listWidgetResults)
        self.labelNoteAvailable = QtGui.QLabel(self.centralwidget)
        self.labelNoteAvailable.setText(QtGui.QApplication.translate("Qnotero", "Right click on item to view note", None, QtGui.QApplication.UnicodeUTF8))
        self.labelNoteAvailable.setObjectName(_fromUtf8("labelNoteAvailable"))
        self.verticalLayout.addWidget(self.labelNoteAvailable)
        self.widgetNote = QtGui.QWidget(self.centralwidget)
        self.widgetNote.setObjectName(_fromUtf8("widgetNote"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.widgetNote)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.labelNote = QtGui.QLabel(self.widgetNote)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelNote.sizePolicy().hasHeightForWidth())
        self.labelNote.setSizePolicy(sizePolicy)
        self.labelNote.setText(QtGui.QApplication.translate("Qnotero", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.labelNote.setTextFormat(QtCore.Qt.RichText)
        self.labelNote.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.labelNote.setWordWrap(True)
        self.labelNote.setObjectName(_fromUtf8("labelNote"))
        self.verticalLayout_2.addWidget(self.labelNote)
        self.widget = QtGui.QWidget(self.widgetNote)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.widget)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.pushButtonOpenNote = QtGui.QPushButton(self.widget)
        self.pushButtonOpenNote.setText(QtGui.QApplication.translate("Qnotero", "Open note", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonOpenNote.setObjectName(_fromUtf8("pushButtonOpenNote"))
        self.horizontalLayout_2.addWidget(self.pushButtonOpenNote)
        self.pushButtonReturnFromNote = QtGui.QPushButton(self.widget)
        self.pushButtonReturnFromNote.setText(QtGui.QApplication.translate("Qnotero", "Return", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonReturnFromNote.setObjectName(_fromUtf8("pushButtonReturnFromNote"))
        self.horizontalLayout_2.addWidget(self.pushButtonReturnFromNote)
        self.verticalLayout_2.addWidget(self.widget)
        self.verticalLayout.addWidget(self.widgetNote)
        Qnotero.setCentralWidget(self.centralwidget)

        self.retranslateUi(Qnotero)
        QtCore.QObject.connect(self.pushButtonReturnFromNote, QtCore.SIGNAL(_fromUtf8("clicked()")), self.listWidgetResults.show)
        QtCore.QObject.connect(self.pushButtonReturnFromNote, QtCore.SIGNAL(_fromUtf8("clicked()")), self.widgetNote.hide)
        QtCore.QMetaObject.connectSlotsByName(Qnotero)

    def retranslateUi(self, Qnotero):
        pass

from qnoteroResults import QnoteroResults
