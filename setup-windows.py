#!/usr/bin/env python3

from distutils.core import setup
import glob
import py2exe
import os
import os.path
import shutil

# Create empty destination folders
if os.path.exists("dist"):
	shutil.rmtree("dist")
os.mkdir("dist")

# Setup options
setup(

	# Use 'console' to have the programs run in a terminal and
	# 'windows' to run them normally.
	windows = [{
		"script" : "qnotero",
		'icon_resources': [(0, os.path.join("data", "qnotero.ico"))],
		}],
	options = {
		'py2exe' : {
		'compressed' : True,
		'optimize': 2,
		'bundle_files': 3,
		'includes': 'sip, libqnotero._themes.*',
		"dll_excludes" : ["MSVCP90.DLL"]
		},
		},
	)

# Copy the resources
shutil.copytree("resources", os.path.join("dist", "resources"))

