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

import sys

config = {
	u"autoFire" : 500,
	u"autoUpdateCheck" : True,
	u"cfgVer" : 0,
	u"firstRun" : True,
	u"listenerPort" : 43250,
	u"minQueryLength" : 3,
	u"noteProvider" : u"gnote",
	u"pdfReader" : u"xdg-open",
	u"theme" : u"Default",
	u"updateUrl" : \
		u"http://files.cogsci.nl/software/qnotero/MOST_RECENT_VERSION.TXT",
	u"pos" : u"Top right",
	u"zoteroPath" : u"",
	u"mdNoteproviderPath" : u"",
	}

def getConfig(setting):

	"""
	Retrieve a setting

	Returns:
	A setting or False if the setting does not exist
	"""

	s = config[setting]
	if isinstance(s, str):
		s = s.decode(sys.getdefaultencoding())
	return config[setting]

def setConfig(setting, value):

	"""
	Set a setting

	Arguments:
	setting -- the setting name
	value -- the setting value
	"""

	assert(not isinstance(value, str))
	config[setting] = value
	config[u"cfgVer"] += 1

def restoreConfig(settings):

	"""
	Restore settings from a QSetting

	Arguments:
	settings -- a QSetting
	"""

	for setting, default in config.items():
		if isinstance(default, bool):
			value = settings.value(setting, default).toBool()
		elif isinstance(default, unicode):
			value = unicode(settings.value(setting, default).toString())
		elif isinstance(default, int):
			value = settings.value(setting, default).toInt()[0]
		elif isinstance(default, float):
			value = settings.value(setting, default).toFloat()[0]
		else:
			raise Exception(u'Unknown default type')
		setConfig(setting, value)

def saveConfig(settings):

	"""
	Save settings to a QSetting

	Arguments:
	setting -- a QSetting
	"""

	for setting, value in config.items():
		settings.setValue(setting, value)

