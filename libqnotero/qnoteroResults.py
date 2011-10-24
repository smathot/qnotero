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

from PyQt4.QtGui import QListWidget, QDrag
from PyQt4.QtCore import Qt, QUrl, QMimeData

class QnoteroResults(QListWidget):

	"""The Qnotero result list"""

	def __init__(self, qnotero):
	
		"""
		Constructor
		
		Arguments:
		qnotero -- a Qnotero instance
		"""
	
		QListWidget.__init__(self, qnotero)		
		self.setMouseTracking(True)
						
	def mousePressEvent(self, e):
	
		"""
		Start a drag operation
		
		Arguments:
		e -- a QMouseEvent
		"""
		
		if e.button() == Qt.RightButton:
			note = self.itemAt(e.pos()).zoteroItem.get_note()
			if note != None:
				self.qnotero.previewNote(note)
			return
			
		QListWidget.mousePressEvent(self, e)		
		qnoteroItem = self.currentItem()
		if qnoteroItem == None:
			return
		if not hasattr(qnoteroItem, "zoteroItem"):
			return
		zoteroItem = qnoteroItem.zoteroItem
		if zoteroItem.fulltext == None:
			return			
		mimeData = QMimeData()
		mimeData.setUrls([QUrl.fromLocalFile(zoteroItem.fulltext)])
		mimeData.setData("text/plain", zoteroItem.fulltext)
		drag = QDrag(self)
		drag.setMimeData(mimeData)
		drag.exec_()
