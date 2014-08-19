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

import socket
from libqnotero.config import getConfig
from threading import Thread
from PyQt4.QtCore import SIGNAL

class Listener(Thread):

	"""Listens for commands"""

	def __init__(self, qnotero=None):
	
		"""
		Constructor
		
		Arguments:
		qnotero -- a Qnotero instance
		"""
	
		self.port = getConfig("listenerPort")
		self.qnotero = qnotero
		self.alive = True
		Thread.__init__(self)
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.sock.bind(("", self.port))			
		self.sock.settimeout(1.)

	def run(self):

		"""Listenes for activation signals and pops up the Qnotero window"""
		
		while self.alive:
			try:
				s, comm_addr = self.sock.recvfrom(128)
			except:
				s = None
			if s != None:
				print("listener.run(): received '%s'" % s)
				if b"activate" == s[:8]:
					print("listener.run(): activating")
					self.qnotero.sysTray.emit(SIGNAL("listenerActivated"))

