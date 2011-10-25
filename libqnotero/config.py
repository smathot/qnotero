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

config = {
	"attachToSysTray" : True,
	"autoUpdateCheck" : True,
	"cfgVer" : 0,
	"firstRun" : True,	
	"minQueryLength" : 3,
	"noteProvider" : "gnote",
	"pdfReader" : "xdg-open",	
	"theme" : "Default",
	"updateUrl" : \
		"http://files.cogsci.nl/software/gnotero/MOST_RECENT_VERSION.TXT",
	"zoteroPath" : "",	
	}

def getConfig(setting):

	"""
	Retrieve a setting
	
	Returns:
	A setting or False if the setting does not exist
	"""

	return config[setting]
	
def setConfig(setting, value):

	"""
	Set a setting
	
	Arguments:
	setting -- the setting name
	value -- the setting value
	"""	
	
	config[setting] = value
	config["cfgVer"] += 1
	
def restoreConfig(settings):

	"""
	Restore settings from a QSetting
	
	Arguments:
	settings -- a QSetting
	"""

	for setting, default in config.items():
		if type(default) == bool:
			value = settings.value(setting, default).toBool()
		elif type(default) == str:
			try:
				value = str(settings.value(setting, default).toString())
			except:
				value = default
		elif type(default) == int:
			value = settings.value(setting, default).toInt()[0]	
		setConfig(setting, value)
	
def saveConfig(settings):

	"""
	Save settings to a QSetting
	
	Arguments:
	setting -- a QSetting
	"""
	
	for setting, value in config.items():
		settings.setValue(setting, value)

