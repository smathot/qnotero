#!/usr/bin/env python3

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

---
desc:
	Windows packaging procedure:
	
	1. Build Qnotero into `dist` with `setup-win.py py2exe`		
	2. Create `.exe` installer with `.nsi` script
	3. Rename `.exe` installer
	4. Rename `dist` and pack it into `.zip` for portable distribution
---
"""

from distutils.core import setup
import glob
import py2exe
import os
import shutil
import sys

class safe_print(object):
	
	"""
	desc:
		Used to redirect standard output, so that Python doesn't crash when
		printing special characters to a terminal.
	"""
	
	errors = 'strict'
	encoding = 'utf-8'	
	
	def write(self, msg):	
		if isinstance(msg, str):
			msg = msg.encode('ascii', 'ignore')
		sys.__stdout__.write(msg.decode('ascii'))
		
	def flush(self):
		pass

# Redirect standard output to safe printer
sys.stdout = safe_print()

# Create empty destination folders
if os.path.exists("dist"):
	shutil.rmtree("dist")
os.mkdir("dist")

# Setup options
setup(
	windows = [{
		"script" : "qnotero",
		'icon_resources': [
			(0, os.path.join("data", "qnotero.ico"))
			],
		}],
	data_files = [
		('resources/default', glob.glob('resources/default/*')),
		('resources/elementary', glob.glob('resources/elementary/*')),		
		('resources/tango', glob.glob('resources/tango/*')),
		('libqnotero/ui', glob.glob('libqnotero/ui/*')),
		('data', ['data/qnotero.ico'])
		],
	options = {
		'py2exe' : {
			'compressed' : True,
			'optimize': 2,
			'bundle_files': 3,
			'includes': [
				'sip',
				],
			'packages' : [
				"libqnotero",
				"libzotero",
				"libqnotero._themes",
				"libzotero._noteProvider",
				],					
			"dll_excludes" : ["MSVCP90.DLL"],
			},
		},
	)
