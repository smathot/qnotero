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

from libqnotero._themes.default import Default
from PyQt4.QtGui import QIcon, QPixmap, QLabel
from PyQt4.QtCore import Qt

class Chameleon(Default):

	"""A theme that blends in with the desktop"""	
	
	mapping = {"qnotero" : "accessoires-dictionary", \
		"close" : "window-close", \
		"pdf" : "application-pdf", \
		"nopdf" : "text-plain", \
		"preferences" : "preferences-other", \
		"search" : "system-search", \
		}
	
	def __init__(self, qnotero):
	
		"""
		Constructor
		
		qnotero -- a Qnotero instance
		"""
	
		self.qnotero = qnotero		
		self.qnotero.setWindowFlags(Qt.Popup)
		self.qnotero.ui.listWidgetResults.setHorizontalScrollBarPolicy( \
			Qt.ScrollBarAlwaysOff)
		self.qnotero.ui.listWidgetResults.setVerticalScrollBarPolicy( \
			Qt.ScrollBarAlwaysOff)
		self.setThemeFolder()
		self.qnotero.ui.lineEditQuery.setFrame(True)		
		
	def icon(self, iconName):
	
		"""
		Retrieves an icon from the theme
		
		Arguments:
		iconName -- the name of the icon
		
		Returns:
		A QIcon		
		"""
	
		if iconName in self.mapping:
			icon = self.mapping[iconName]
		else:
			icon = "edit-undo"			
		if not QIcon.hasThemeIcon(icon):
			print "libqnotero._themes.icon(): failed to find '%s'" % icon
		return QIcon.fromTheme("icon", Default.icon(self, iconName))
		
	def pixmap(self, pixmapName):
	
		"""
		Retrieves an icon (as QPixmap) from the theme
		
		Arguments:
		pixmapName -- the name of the icon
		
		Returns:
		A QPixmap
		"""		
		
		icon = self.icon(pixmapName)
		return icon.pixmap(32,32)
		
		