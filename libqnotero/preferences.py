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
import os.path
import pkgutil
from PyQt4.QtGui import QDialog, QFileDialog, QMessageBox, QApplication
from PyQt4 import uic
from libqnotero.config import getConfig, setConfig
from libzotero.libzotero import valid_location

class Preferences(QDialog):

	"""Qnotero preferences dialog"""

	def __init__(self, qnotero, firstRun=False):

		"""
		Constructor

		Arguments:
		qnotero -- a Qnotero instance

		Keyword arguments:
		firstRun -- indicates if the first run message should be shown
					(default=False)
		"""

		QDialog.__init__(self)
		self.qnotero = qnotero
		uiPath = os.path.join(os.path.dirname(__file__), 'ui', 'preferences.ui')
		print('Preferences.__init__(): loading preferences ui from %s' % uiPath)
		self.ui = uic.loadUi(uiPath, self)
		self.ui.labelLocatePath.hide()
		if not firstRun:
			self.ui.labelFirstRun.hide()
		self.ui.labelTitleMsg.setText( \
			self.ui.labelTitleMsg.text().replace(u"[version]", \
			self.qnotero.version))
		self.ui.pushButtonZoteroPathAutoDetect.clicked.connect( \
			self.zoteroPathAutoDetect)
		self.ui.pushButtonZoteroPathBrowse.clicked.connect( \
			self.zoteroPathBrowse)
		self.ui.checkBoxAutoUpdateCheck.setChecked(getConfig(u"autoUpdateCheck"))
		self.ui.lineEditZoteroPath.setText(getConfig(u"zoteroPath"))
		i = 0
		import libqnotero._themes
		themePath = os.path.dirname(libqnotero._themes.__file__)
		for _, theme, _ in pkgutil.iter_modules([themePath]):
			self.ui.comboBoxTheme.addItem(theme)
			if theme == getConfig(u"theme").lower():
				self.ui.comboBoxTheme.setCurrentIndex(i)
			i += 1
		self.setStyleSheet(self.qnotero.styleSheet())
		self.adjustSize()

	def accept(self):

		"""Accept the changes"""

		if self.ui.labelLocatePath.isVisible():
			return
		print('saving!')
		setConfig(u"firstRun", False)
		setConfig(u"pos", self.ui.comboBoxPos.currentText())
		setConfig(u"autoUpdateCheck", \
			self.ui.checkBoxAutoUpdateCheck.isChecked())
		setConfig(u"zoteroPath", self.ui.lineEditZoteroPath.text())
		setConfig(u"theme", self.ui.comboBoxTheme.currentText().capitalize())
		self.qnotero.saveState()
		self.qnotero.reInit()
		QDialog.accept(self)

	def locate(self, path, target):

		"""
		Tries to find the location of a target file

		Arguments:
		path -- the path to search
		target -- the target file

		Returns:
		The full path to the target file or None if it wasn't found
		"""

		self.ui.labelLocatePath.setText(u"Scanning: ...%s" % path[-32:])
		QApplication.processEvents()
		# Don't scan filesystems that may contain recursions
		if u".gvfs" in path or u".wine" in path:
			return None
		for (dirpath, dirnames, filenames) in os.walk(path):
			for filename in filenames:
				if filename == target:
					return dirpath
			for dirname in dirnames:
				location = self.locate(os.path.join(dirpath, dirname), target)
				if location != None:
					return location
		return None

	def reject(self):

		"""Reject changes"""

		if not self.ui.labelLocatePath.isVisible():
			QDialog.reject(self)

	def setZoteroPath(self, path):

		"""
		Validate and set the Zotero path

		Arguments:
		path -- the Zotero path
		"""

		if valid_location(path):
			self.ui.lineEditZoteroPath.setText(path)
		else:
			QMessageBox.information(self, u"Invalid Zotero path", \
				u"The folder you selected does not contain 'zotero.sqlite'")

	def zoteroPathAutoDetect(self):

		"""Auto-detect the Zotero folder"""

		self.ui.labelLocatePath.show()
		if os.name == u"nt":
			home= os.environ[u"USERPROFILE"]
		elif os.name == u"posix":
			home = os.environ[u"HOME"]
		zoteroPath = self.locate(home, u"zotero.sqlite")
		if zoteroPath == None:
			QMessageBox.information(self, u"Unable to find Zotero", \
				u"Unable to find Zotero. Please specify the Zotero folder manually.")
		else:
			self.ui.lineEditZoteroPath.setText(zoteroPath)
		self.ui.labelLocatePath.hide()

	def zoteroPathBrowse(self):

		"""Select the Zotero folder manually"""

		path = QFileDialog.getExistingDirectory(self, u"Locate Zotero folder")
		if path != u"":
			self.setZoteroPath(path)

