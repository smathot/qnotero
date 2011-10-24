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
from PyQt4.QtGui import QMainWindow, QListWidgetItem, QLabel, QDesktopWidget
from PyQt4.QtCore import QSettings, QSize
from libqnotero.sysTray import SysTray
from libqnotero.config import saveConfig, restoreConfig, setConfig, getConfig
from libqnotero.qnoteroUi import Ui_Qnotero
from libqnotero.qnoteroItemDelegate import QnoteroItemDelegate
from libqnotero.qnoteroItem import QnoteroItem
from libzotero.libzotero import LibZotero

class Qnotero(QMainWindow):

	"""The main class of the Qnotero GUI"""
	
	version = "0.45-pre1"

	def __init__(self, systray=True, debug=False, reset=False, parent=None):

		"""
		Constructor

		Keyword arguments:
		systray -- enables the system tray icon (default=True)		
		debug -- enable debugging output (default=False)
		reset -- reset preferences (default=False)
		parent -- parent QWidget (default=None)
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
			
		if getConfig("firstRun"):
			self.preferences()		
		
	def close(self):
	
		"""Exit the program"""
	
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
			exit()			
			
	def hideNoteHint(self):
	
		"""Hide the note available message"""
				
		self.ui.labelNoteAvailable.hide()
		
	def openNote(self, note):
	
		"""
		Show the note preview
		
		Arguments:
		note -- the Note to preview
		"""
	
		self.ui.labelNote.setText(note.preview)
		self.hideNoteHint()
		self.ui.widgetNote.show()
		self.ui.listWidgetResults.hide()
			
	def moveSafe(self, topLeft):
	
		"""
		Move the window while respecting the screen boundaries
		
		Arguments:
		topLeft -- a QPoint for the top left
		"""
		
		rect = QDesktopWidget().availableGeometry()
		if not rect.contains(topLeft):
			pos = rect.topRight()
			self.move(pos.x()-self.size().width(), pos.y())
		else:		
			self.move(topLeft)
			
	def moveToCenter(self):
	
		"""Move the window the display center"""
		
		pos = QDesktopWidget().availableGeometry().center()
		x = pos.x()
		y = pos.y()
		s = self.size()
		h = s.height()
		w = s.width()
		self.move(x-w/2, y-h/2)
			
	def noResults(self, query=None):
	
		"""
		Displays the no results message
		
		Keyword arguments:
		query -- a query (default=None)
		"""
		
		if query != None:	
			self.showResultMsg("No results for %s" % query)
		else:
			self.showResultMsg("Please enter a search term")
						
	def popDown(self):
	
		"""Minimize to the tray"""
	
		self.hide()		
	
	def popUp(self, topLeft=None):
	
		"""
		Popup from the tray
		
		Keyword arguments:
		topLeft -- a QPoint for the top left (default=None)		
		"""
	
		if topLeft != None:
			self.moveSafe(topLeft)
		else:
			self.moveToCenter()
		self.show()
		self.ui.lineEditQuery.setFocus()			
		
	def preferences(self):
	
		"""Show the preferences dialog"""
		
		from libqnotero.preferences import Preferences
		Preferences(self).exec_()		
		
	def reInit(self):
	
		"""Re-init the parts of the GUI that can be changed at runtime"""
				
		self.setTheme()				
		self.setupUi()		
		if getConfig("noteProvider") == "gnote":
			from libzotero._noteProvider.gnoteProvider import GnoteProvider
			print "qnotero.reInit(): using GnoteProvider"
			self.noteProvider = GnoteProvider()
		else:
			self.noteProvider = None						
		self.zotero = LibZotero(getConfig("zoteroPath"), self.noteProvider)		
		
	def restoreState(self):

		"""Restore the settings"""

		settings = QSettings("cogscinl", "qnotero")
		settings.beginGroup("Qnotero");
		restoreConfig(settings)
		settings.endGroup()	
		
	def runResult(self, listWidgetItem):
	
		"""Handle clicks on a result"""
		
		if listWidgetItem.zoteroItem.fulltext == None:
			return			
		pdf = listWidgetItem.zoteroItem.fulltext.encode("latin-1")
		if os.name == "nt":			
			os.startfile(pdf)
		else:
			pid = subprocess.Popen([getConfig("pdfReader"), pdf])
		self.popDown()

	def saveState(self):

		"""Save the settings"""

		settings = QSettings("cogscinl", "qnotero")
		settings.beginGroup("Qnotero")
		saveConfig(settings)
		settings.endGroup()	
		
	def search(self):
	
		"""Execute a search"""
		
		self.ui.labelNoteAvailable.hide()
		self.ui.widgetNote.hide()
		self.ui.listWidgetResults.show()
		self.ui.listWidgetResults.clear()				
		query = unicode(self.ui.lineEditQuery.text())
		if len(query) < getConfig("minQueryLength"):
			self.noResults()
			return		
		zoteroItemList = self.zotero.search(query)		
		if len(zoteroItemList) == 0:
			self.noResults(query)
			return			
		self.showResultMsg("%d results for %s" % (len(zoteroItemList), query))				
		for zoteroItem in zoteroItemList:
			qnoteroItem = QnoteroItem(self, zoteroItem, \
				self.ui.listWidgetResults)
			self.ui.listWidgetResults.addItem(qnoteroItem)		
			
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
		
		theme = getConfig("theme")
		exec("from libqnotero._themes.%s import %s as Theme" % (theme.lower(), \
			theme.capitalize()))
		self.theme = Theme(self)
		
	def setupUi(self):
	
		"""Setup the GUI"""
						
		self.ui.pushButtonSearch.setIcon(self.theme.icon("search"))
		self.ui.pushButtonSearch.clicked.connect(self.search)
		self.ui.lineEditQuery.returnPressed.connect(self.search)
		self.ui.listWidgetResults.qnotero = self
		self.ui.listWidgetResults.setItemDelegate(QnoteroItemDelegate(self))		
		self.ui.listWidgetResults.itemActivated.connect(self.runResult)				
		self.ui.widgetNote.hide()
		self.ui.labelNoteAvailable.hide()		
		
	def showNoteHint(self):
	
		"""Indicate that a note is available"""
	
		self.ui.labelNoteAvailable.show()		
		
	def showResultMsg(self, msg):
	
		"""
		Show a status message
		
		Arguments:
		msg -- a message
		"""
			
		self.ui.labelResultMsg.setText("<small><i>%s</i></small>" % msg)		