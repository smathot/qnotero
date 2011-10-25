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
from libqnotero.qnoteroException import QnoteroException
from PyQt4.QtGui import QIcon, QPixmap, QLabel
from PyQt4.QtCore import Qt

class Default:

	"""The default Qnotero theme"""	
	
	def __init__(self, qnotero):
	
		"""
		Constructor
		
		qnotero -- a Qnotero instance
		"""
	
		self.qnotero = qnotero		
		self.themeFolder = os.path.join(os.path.dirname(sys.argv[0]), \
			"resources", self.themeFolder())
		if not os.path.exists(self.themeFolder):
			self.themeFolder = os.path.join("/usr/share/qnotero/resources/", \
				self.themeFolder())
			if not os.path.exists(self.themeFolder):
				raise QnoteroException("Failed to find resource folder!")
		print "libqnotero._themes.default.__init__(): using '%s'" \
			% self.themeFolder
		self.setStyleSheet()
		self.qnotero.setWindowFlags(Qt.Popup)
		self.qnotero.ui.listWidgetResults.setHorizontalScrollBarPolicy( \
			Qt.ScrollBarAlwaysOff)
		self.qnotero.ui.listWidgetResults.setVerticalScrollBarPolicy( \
			Qt.ScrollBarAlwaysOff)						
		
	def icon(self, iconName):
	
		"""
		Retrieves an icon from the theme
		
		Arguments:
		iconName -- the name of the icon
		
		Returns:
		A QIcon		
		"""
	
		return QIcon(os.path.join(self.themeFolder, iconName) + ".png")
		
	def iconWidget(self, iconName):
	
		"""
		Return a QLabel with an icon
		
		Arguments:
		iconName -- the name of the icon
		
		Returns:
		A QLabel
		"""
	
		l = QLabel()
		l.setPixmap(self.pixmap(iconName))
		return l
		
	def lineHeight(self):
	
		"""
		Determines the line height of the results
		
		Returns:
		A float (e.g., 1.1) for the line height
		"""
		
		return 1.1
		
	def pixmap(self, pixmapName):
	
		"""
		Retrieves an icon (as QPixmap) from the theme
		
		Arguments:
		pixmapName -- the name of the icon
		
		Returns:
		A QPixmap
		"""		
		
		return QPixmap(os.path.join(self.themeFolder, pixmapName) + ".png")
		
	def roundness(self):
	
		"""
		Determines the roundness of various widgets
		
		Returns:
		A roundness as a radius in pixels
		"""
		
		return 10
		
	def setStyleSheet(self):
	
		"""Applies a stylesheet to Qnotero"""
	
		self.qnotero.setStyleSheet(open(os.path.join( \
			self.themeFolder, "stylesheet.qss")).read())
			
	def themeFolder(self):
	
		"""
		Determines the name of the folder containing the theme resources
		
		Returns:
		The name of the theme folder
		"""
		
		return "default"