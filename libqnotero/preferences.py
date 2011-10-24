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

import os
import os.path
import pkgutil
from PyQt4.QtGui import QDialog, QFileDialog, QMessageBox, QApplication
from libqnotero.preferencesUi import Ui_Preferences
from libqnotero.config import getConfig, setConfig
from libzotero.libzotero import valid_location

class Preferences(QDialog):

	"""Qnotero preferences dialog"""

	def __init__(self, qnotero):
	
		"""
		Constructor
		
		Arguments:
		qnotero -- a Qnotero instance
		"""
	
		QDialog.__init__(self)
		self.qnotero = qnotero
		self.ui = Ui_Preferences()		
		self.ui.setupUi(self)
		self.ui.labelTitleMsg.setText( \
			self.ui.labelTitleMsg.text().replace("[version]", \
			self.qnotero.version))
		self.setStyleSheet(self.qnotero.styleSheet())		
		self.ui.pushButtonZoteroPathAutoDetect.clicked.connect( \
			self.zoteroPathAutoDetect)
		self.ui.pushButtonZoteroPathBrowse.clicked.connect( \
			self.zoteroPathBrowse)					
		self.ui.checkBoxAttachToSysTray.setChecked(getConfig("attachToSysTray"))
		self.ui.lineEditZoteroPath.setText(getConfig("zoteroPath"))
		self.ui.labelLocatePath.hide()
		
		i = 0
		import libqnotero._themes
		themePath = os.path.dirname(libqnotero._themes.__file__)
		for _, theme, _ in pkgutil.iter_modules([themePath]):
			self.ui.comboBoxTheme.addItem(theme)
			if theme == getConfig("theme").lower():
				self.ui.comboBoxTheme.setCurrentIndex(i)
			i += 1		
				
	def accept(self):
	
		"""Accept the changes"""
		
		if self.ui.labelLocatePath.isVisible():
			return
		setConfig("firstRun", False)
		setConfig("attachToSysTray", \
			self.ui.checkBoxAttachToSysTray.isChecked())	
		setConfig("zoteroPath", unicode(self.ui.lineEditZoteroPath.text()))
		setConfig("theme", \
			unicode(self.ui.comboBoxTheme.currentText()).capitalize())
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
			
		self.ui.labelLocatePath.setText("Scanning: ...%s" % path[-32:])
		QApplication.processEvents()
		# Don't scan filesystems that may contain recursions
		if ".gvfs" in path or ".wine" in path:
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
		
		if valid_location(unicode(path)):
			self.ui.lineEditZoteroPath.setText(path)
		else:
			QMessageBox.information(self, "Invalid Zotero path", \
				"The folder you selected does not contain 'zotero.sqlite'")
				
	def zoteroPathAutoDetect(self):
	
		"""Auto-detect the Zotero folder"""
		
		self.ui.labelLocatePath.show()
		if os.name == "nt":
			home= os.environ["USERPROFILE"]			
		elif os.name == "posix":
			home = os.environ["HOME"]
		zoteroPath = self.locate(home, "zotero.sqlite")
		if zoteroPath == None:
			QMessageBox.information(self, "Unable to find Zotero", \
				"Unable to find Zotero. Please specify the Zotero folder manually.")
		else:
			self.ui.lineEditZoteroPath.setText(zoteroPath)
		self.ui.labelLocatePath.hide()
		
	def zoteroPathBrowse(self):
	
		"""Select the Zotero folder manually"""
		
		path = QFileDialog.getExistingDirectory(self, "Locate Zotero folder")
		if path != "":
			self.setZoteroPath(path)
		