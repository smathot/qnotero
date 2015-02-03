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

from libqnotero.qt.QtGui import QSystemTrayIcon, QMenu
from libqnotero.qt.QtCore import Qt, QObject, pyqtSignal
from libqnotero.config import getConfig

class SysTray(QSystemTrayIcon):

	"""The Qnotero system tray icon"""

	listenerActivated = pyqtSignal()
	
	def __init__(self, qnotero):
	
		"""
		Constructor
		
		Arguments:
		qnotero -- a Qnotero instance
		"""
	
		QSystemTrayIcon.__init__(self, qnotero)
		self.qnotero = qnotero		
		self.setIcon(self.qnotero.theme.icon("qnotero"))		
		self.menu = QMenu()
		self.menu.addAction(self.qnotero.theme.icon("qnotero"), "Show",
			self.qnotero.popUp)
		self.menu.addAction(self.qnotero.theme.icon("preferences"),
			"Preferences", self.qnotero.preferences)
		self.menu.addAction(self.qnotero.theme.icon("close"), "Close",
			self.qnotero.close)
		self.setContextMenu(self.menu)
		self.activated.connect(self.activate)
		self.listenerActivated.connect(self.activate)
				
	def activate(self, reason=None):
	
		"""
		Handle clicks on the systray icon
		
		Keyword arguments:
		reason -- the reason for activation (default=None)
		"""
	
		
		if reason == QSystemTrayIcon.Context:
			return		
		if self.qnotero.isVisible():
			self.qnotero.popDown()
		else:
			self.qnotero.popUp()
