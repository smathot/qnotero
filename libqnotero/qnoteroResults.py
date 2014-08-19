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
from PyQt4.QtCore import Qt, QUrl, QMimeData, QString
import urllib
import shutil
import tempfile
import os.path
import time

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
			item = self.itemAt(e.pos())
			if item == None:
				return
			note = item.zoteroItem.get_note()
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
		
		path = zoteroItem.fulltext.encode("latin-1")
		tmpName = '%s.pdf' % zoteroItem.filename_format()
		tmpFile = os.path.join(tempfile.gettempdir(), tmpName)
		suffix = 1
		while os.path.exists(tmpFile):
			tmpName = '%s-%d.pdf' % (zoteroItem.filename_format(), suffix)
			tmpFile = os.path.join(tempfile.gettempdir(), tmpName)			
			suffix += 1
		try:
			shutil.copy(path, tmpFile)
		except:
			print("qnoteroResults.mousePressEvent(): failed to copy file, sorry...")
			return
			
		print("qnoteroResults.mousePressEvent(): prepare to copy %s" % path)
		print("qnoteroResults.mousePressEvent(): prepare to copy (tmp) %s" \
			% tmpFile)
		mimeData = QMimeData()
		mimeData.setUrls([QUrl.fromLocalFile(tmpFile)])
		mimeData.setData("text/plain", tmpFile)
		drag = QDrag(self)
		drag.setMimeData(mimeData)
		drag.exec_(Qt.CopyAction)

	def keyPressEvent(self, e):

		"""
		Handle key presses

		Arguments:
		e -- a QKeyEvent
		"""

		if e.key() == Qt.Key_Up and self.currentRow() == 0:
			self.qnotero.ui.lineEditQuery.selectAll()
			self.qnotero.ui.lineEditQuery.setFocus()
			return
		QListWidget.keyPressEvent(self, e)
