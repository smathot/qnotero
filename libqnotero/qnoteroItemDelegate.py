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

from PyQt4.QtGui import QStyledItemDelegate, QStyle, QPen, QPalette, \
	QApplication, QFont, QFontMetrics
from PyQt4.QtCore import Qt, QRect, QSize
from libqnotero.config import getConfig
from libzotero.zotero_item import cache as zoteroCache

class QnoteroItemDelegate(QStyledItemDelegate):

	"""Draws pretty result items"""

	def __init__(self, qnotero):

		"""
		Constructor

		Arguments:
		qnotero -- a Qnotero instance
		"""

		QStyledItemDelegate.__init__(self, qnotero)
		self.qnotero = qnotero
		self.boldFont = QFont()
		self.boldFont.setBold(True)
		self.regularFont = QFont()
		self.italicFont = QFont()
		self.italicFont.setItalic(True)
		self.tagFont = QFont()
		self.tagFont.setBold(True)
		self.tagFont.setPointSize(self.boldFont.pointSize() - 2)
		self.dy = QFontMetrics(self.boldFont) \
			.size(Qt.TextSingleLine, u"Dummy").height() \
			*self.qnotero.theme.lineHeight()
		self.margin = 0.5*self.dy
		self._margin = 0.1*self.dy
		self.height = 5*self.dy+self._margin
		self.noPdfPixmap = self.qnotero.theme.pixmap(u"nopdf")
		self.pdfPixmap = self.qnotero.theme.pixmap(u"pdf")
		self.aboutPixmap = self.qnotero.theme.pixmap(u"about")
		self.notePixmap = self.qnotero.theme.pixmap(u"note")
		self.pixmapSize = self.pdfPixmap.height()+0.5*self.dy
		self.roundness = self.qnotero.theme.roundness()

	def sizeHint(self, option, index):

		"""
		Suggest a size for the widget

		Arguments:
		option -- a QStyleOptionView
		index -- a QModelIndex

		Returns:
		A QSize
		"""

		return QSize(0, self.height)

	def paint(self, painter, option, index):

		"""
		Draws the widget

		Arguments:
		painter -- a QPainter
		option -- a QStyleOptionView
		index -- a QModelIndex
		"""

		# Retrieve the data
		model = index.model()
		record = model.data(index)
		text = record.toString()
		zoteroItem = zoteroCache[unicode(text)]
		l = zoteroItem.full_format().split(u"\n")
		if zoteroItem.fulltext == None:
			pixmap = self.noPdfPixmap
		else:
			pixmap = self.pdfPixmap

		# Choose the colors
		self.palette = self.qnotero.ui.listWidgetResults.palette()
		if option.state & QStyle.State_MouseOver:
			background = self.palette.Highlight
			foreground = self.palette.HighlightedText
			_note = zoteroItem.get_note()
			if _note != None:
				self.qnotero.showNoteHint()
			else:
				self.qnotero.hideNoteHint()

		elif option.state & QStyle.State_Selected:
			background = self.palette.Dark
			foreground = self.palette.WindowText
		else:
			background = self.palette.Base
			foreground = self.palette.WindowText

		# Draw the frame
		_rect = option.rect.adjusted(self._margin, self._margin, \
			-2*self._margin, -self._margin)
		pen = painter.pen()
		pen.setColor(self.palette.color(background))
		painter.setPen(pen)
		painter.setBrush(self.palette.brush(background))
		painter.drawRoundedRect(_rect, self.roundness, self.roundness)
		font = painter.font
		pen = painter.pen()
		pen.setColor(self.palette.color(foreground))
		painter.setPen(pen)

		# Draw icon
		_rect = QRect(option.rect)
		_rect.moveBottom(_rect.bottom() + 0.5*self.dy)
		_rect.moveLeft(_rect.left() + 0.5*self.dy)
		_rect.setHeight(self.pixmapSize)
		_rect.setWidth(self.pixmapSize)
		painter.drawPixmap(_rect, pixmap)

		# Draw the text
		_rect = option.rect.adjusted(self.pixmapSize+self.dy, 0.5*self.dy, \
			-self.dy, 0)

		f = [self.tagFont, self.italicFont, self.regularFont, \
			self.boldFont]
		l.reverse()
		while len(l) > 0:
			s = l.pop()
			if len(f) > 0:
				painter.setFont(f.pop())
			painter.drawText(_rect, Qt.AlignLeft, s)
			_rect = _rect.adjusted(0, self.dy, 0, 0)


