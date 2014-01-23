#-*- coding:utf-8 -*-

"""
This file is part of qnotero.

qnotero is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

qnotero is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with qnotero.  If not, see <http://www.gnu.org/licenses/>.
"""

import sys
import os
import subprocess
from PyQt4.QtGui import QMainWindow, QListWidgetItem, QLabel, QDesktopWidget, \
	QMessageBox
from PyQt4.QtCore import QSettings, QSize, QCoreApplication
from libqnotero.sysTray import SysTray
from libqnotero.config import saveConfig, restoreConfig, setConfig, getConfig
from libqnotero.qnoteroUi import Ui_Qnotero
from libqnotero.qnoteroItemDelegate import QnoteroItemDelegate
from libqnotero.qnoteroItem import QnoteroItem
from libzotero.libzotero import LibZotero

class Qnotero(QMainWindow):

	"""The main class of the Qnotero GUI"""

	version = u"1.0.0~pre1"

	def __init__(self, systray=True, debug=False, reset=False, parent=None):

		"""
		Constructor.

		Keyword arguments:
		systray		--	Enables the system tray icon (default=True)
		debug		--	Enable debugging output (default=False)
		reset		--	Reset preferences (default=False)
		parent		--	Parent QWidget (default=None)
		"""

		QMainWindow.__init__(self, parent)
		self.ui = Ui_Qnotero()
		self.ui.setupUi(self)
		if not reset:
			self.restoreState()
		self.debug = debug
		self.reInit()
		self.noResults()
		if systray:
			self.sysTray = SysTray(self)
			self.sysTray.show()
			self.minimizeOnClose = True
		else:
			self.minimizeOnClose = False
		if getConfig(u"firstRun"):
			self.preferences(firstRun=True)
		if getConfig(u"autoUpdateCheck"):
			self.updateCheck()

	def close(self):

		"""Exits the program."""

		self.minimizeOnClose = False
		QMainWindow.close(self)

	def closeEvent(self, e):

		"""
		Close or minimze to tray, depending on when the function is called

		Arguments:
		e -- a QCloseEvent
		"""

		if self.minimizeOnClose:
			self.popDown()
			e.ignore()
		else:
			e.accept()
			if self.listener != None:
				self.listener.alive = False
			sys.exit()

	def hideNoteHint(self):

		"""Hide the note available message"""

		self.ui.labelNoteAvailable.hide()

	def leaveEvent(self, e):

		"""Hide the Window when the mouse is lost"""

		self.popDown()

	def openNote(self):

		"""Open the active note"""

		self.activeNote.open()

	def noResults(self, query=None):

		"""
		Displays the no results message

		Keyword arguments:
		query -- a query (default=None)
		"""

		if query != None:
			self.showResultMsg(u"No results for %s" % query)
		else:
			self.showResultMsg(u"Please enter a search term")

	def popDown(self):

		"""Minimize to the tray"""

		if self.minimizeOnClose:
			self.hide()
		else:
			self.close()

	def popUp(self):

		"""Popup from the tray"""

		# Reposition the window
		r = QDesktopWidget().availableGeometry()
		s = self.size()
		pos = getConfig(u"pos")
		if pos == u"Top right":
			x = r.left() + r.width()-s.width()
			y = r.top()
		elif pos == u"Top left":
			x = r.left()
			y = r.top()
		elif pos == u"Bottom right":
			x = r.left() + r.width()-s.width()
			y = r.top() + r.height()-s.height()
		elif pos == u"Bottom left":
			x = r.left()
			y = r.top() + r.height()-s.height()
		else:
			x = r.left() + r.width()/2 - s.width()/2
			y = r.top() + r.height()/2 - s.height()/2
		self.move(x, y)

		# Show it
		self.show()
		QCoreApplication.processEvents()
		self.raise_()
		self.activateWindow()

		# Focus the search box
		self.ui.lineEditQuery.selectAll()
		self.ui.lineEditQuery.setFocus()

	def preferences(self, firstRun=False):

		"""
		Show the preferences dialog

		Keyword arguments:
		firstRun -- indicates if the first run message should be shown
					(default=False)
		"""

		from libqnotero.preferences import Preferences
		Preferences(self, firstRun=firstRun).exec_()

	def previewNote(self, note):

		"""
		Show the note preview

		Arguments:
		note -- the Note to preview
		"""

		self.activeNote = note
		self.ui.labelNote.setText(note.preview)
		self.hideNoteHint()
		self.ui.widgetNote.show()
		self.ui.listWidgetResults.hide()

	def reInit(self):

		"""Re-inits the parts of the GUI that can be changed at runtime."""

		self.setTheme()
		self.setupUi()
		self.noteProvider = []
		if getConfig(u'noteProvider') == u'gnote':
			from libzotero._noteProvider.gnoteProvider import GnoteProvider
			print(u"qnotero.reInit(): using GnoteProvider")
			self.noteProvider = GnoteProvider(self)
		self.zotero = LibZotero(getConfig(u"zoteroPath"), self.noteProvider)
		if hasattr(self, u"sysTray"):
			self.sysTray.setIcon(self.theme.icon(u"qnotero"))

	def restoreState(self):

		"""Restore the settings"""

		settings = QSettings(u"cogscinl", u"qnotero")
		settings.beginGroup(u"Qnotero");
		restoreConfig(settings)
		settings.endGroup()

	def runResult(self, listWidgetItem):

		"""Handle clicks on a result"""

		if listWidgetItem.zoteroItem.fulltext == None:
			return
		pdf = listWidgetItem.zoteroItem.fulltext
		if os.name == u"nt":
			os.startfile(pdf)
		else:
			# For some reason, the file must be encoded with latin-1, despite
			# the fact that it's a utf-8 encoded database and filesystem!
			pdf = pdf.encode(u'latin-1')
			reader = getConfig(u'pdfReader').encode(sys.getfilesystemencoding())
			pid = subprocess.Popen([reader, pdf])
		self.popDown()

	def saveState(self):

		"""Save the settings"""

		settings = QSettings(u"cogscinl", u"qnotero")
		settings.beginGroup(u"Qnotero")
		saveConfig(settings)
		settings.endGroup()

	def search(self, setFocus=False):

		"""
		Execute a search

		Keyword arguments:
		setFocus -- indicates whether the listWidgetResults needs to receive
					focus (default=False)
		"""

		self.ui.labelNoteAvailable.hide()
		self.ui.widgetNote.hide()
		self.ui.listWidgetResults.show()
		self.ui.listWidgetResults.clear()
		self.ui.lineEditQuery.needUpdate = False
		self.ui.lineEditQuery.timer.stop()
		query = unicode(self.ui.lineEditQuery.text())
		if len(query) < getConfig(u"minQueryLength"):
			self.noResults()
			return
		zoteroItemList = self.zotero.search(query)
		if len(zoteroItemList) == 0:
			self.noResults(query)
			return
		self.showResultMsg(u"%d results for %s" % (len(zoteroItemList), query))
		for zoteroItem in zoteroItemList:
			qnoteroItem = QnoteroItem(self, zoteroItem, \
				self.ui.listWidgetResults)
			self.ui.listWidgetResults.addItem(qnoteroItem)
		if setFocus:
			self.ui.listWidgetResults.setFocus()

	def setSize(self, size):

		"""
		Set the window size

		Arguments:
		size -- a QSize
		"""

		self.setMinimumSize(size)
		self.setMaximumSize(size)

	def setTheme(self):

		"""Load a theme"""

		theme = getConfig(u'theme')
		mod = __import__(u'libqnotero._themes.%s' % theme.lower(), fromlist= \
			[u'dummy'])
		cls = getattr(mod, theme.capitalize())
		self.theme = cls(self)

	def setupUi(self):

		"""Setup the GUI"""

		self.ui.pushButtonSearch.setIcon(self.theme.icon(u"search"))
		self.ui.pushButtonSearch.clicked.connect(self.search)
		self.ui.lineEditQuery.qnotero = self
		self.ui.listWidgetResults.qnotero = self
		self.ui.listWidgetResults.setItemDelegate(QnoteroItemDelegate(self))
		self.ui.listWidgetResults.itemActivated.connect(self.runResult)
		self.ui.widgetNote.hide()
		self.ui.labelNoteAvailable.hide()
		self.ui.pushButtonOpenNote.clicked.connect(self.openNote)

	def showNoteHint(self):

		"""Indicate that a note is available"""

		self.ui.labelNoteAvailable.show()

	def showResultMsg(self, msg):

		"""
		Shows a status message.

		Arguments:
		msg 	--	A message.
		"""

		self.ui.labelResultMsg.setText(u"<small><i>%s</i></small>" % msg)

	def updateCheck(self):

		"""Checks for updates if update checking is on."""

		if not getConfig(u"autoUpdateCheck"):
			return True

		import urllib
		print(u"qnotero.updateCheck(): opening %s" % getConfig(u"updateUrl"))
		try:
			fd = urllib.urlopen(getConfig(u"updateUrl"))
			mrv = float(fd.read().strip())
		except:
			print(u"qnotero.updateCheck(): failed to check for update")
			return
		print(u"qnotero.updateCheck(): most recent version is %.2f" % mrv)
		if mrv > self.version:
			QMessageBox.information(self, u"Update found", \
				u"A new version of Qnotero %s is available! Please visit http://www.cogsci.nl/ for more information." \
				% mrv)
