"""
This file is part of Gnotero.

Gnotero is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Gnotero is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Gnotero.  If not, see <http://www.gnu.org/licenses/>.
"""

import sqlite3
import os
import os.path
import sys
import shutil
import sys
import time
from zotero_item import zoteroItem as zotero_item

class LibZotero:
	
	"""
	Libzotero provides access to the zotero database.	
	This is an object oriented reimplementation of the
	original zoterotools.
	"""
	
	attachment_query = """
		select items.itemID, itemAttachments.path, itemAttachments.itemID
		from items, itemAttachments
		where items.itemID = itemAttachments.sourceItemID
		"""

	info_query = """
		select items.itemID, fields.fieldName, itemDataValues.value, items.key
		from items, itemData, fields, itemDataValues
		where
			items.itemID = itemData.itemID
			and itemData.fieldID = fields.fieldID
			and itemData.valueID = itemDataValues.valueID
			and (fields.fieldName = "date" or fields.fieldName = "publicationTitle" or fields.fieldName = "volume" or fields.fieldName = "issue" or fields.fieldName = "title")
		"""
	
	author_query = """
		select items.itemID, creatorData.lastName
		from items, itemCreators, creators, creatorData
		where
			items.itemID = itemCreators.itemID
			and itemCreators.creatorID = creators.creatorID
			and creators.creatorDataID = creatorData.creatorDataID
		order by itemCreators.orderIndex
		"""
	
	collection_query = """
		select items.itemID, collections.collectionName
		from items, collections, collectionItems
		where
			items.itemID = collectionItems.itemID
			and collections.collectionID = collectionItems.collectionID
		order by collections.collectionName != "To Read", collections.collectionName
		"""
	
	deleted_query = "select itemID from deletedItems"	
	
	def __init__(self, zotero_path, noteProvider=None):
		
		"""
		Intialize libzotero
		"""
		
		print "libzotero.__init__(): zotero_path = %s" % zotero_path
		
		# Set paths
		self.zotero_path = zotero_path
		self.storage_path = os.path.join(self.zotero_path, "storage")
		self.zotero_database = os.path.join(self.zotero_path, "zotero.sqlite")
		self.noteProvider = noteProvider

		if os.name == "nt":
			home_folder = unicode(os.environ["USERPROFILE"])
		elif os.name == "posix":
		
			home_folder = unicode(os.environ["HOME"])
		else:
			print "libzotero.__init__(): you appear to be running an unsupported OS"
				
		self.gnotero_database = os.path.join(home_folder, ".gnotero.sqlite")
		
		# Remember search results so results speed up over time
		self.search_cache = {}
				
		# Check whether verbosity is turned on
		self.verbose = "-v" in sys.argv
		
		# These dates are treated as special and are not parsed into a year representation
		self.special_dates = "in press", "submitted", "in preparation", "unpublished"		
		
		# These extensions are recognized as fulltext attachments
		self.attachment_ext = ".pdf", ".epub"
		
		self.index = {}
		self.collection_index = []
		self.last_update = None
		
		# The notry parameter can be used to show errors which would
		# otherwise be obscured by the try clause
		if "--notry" in sys.argv:
			self.search("dummy")
		
		# Start by updating the database
		try:
			self.search("dummy")
			self.error = False
		except Exception as e:
			print e
			self.error = True				
		
	def update(self, force = False):
		
		"""
		This function checks if the local copy of the zotero
		database is up to date. If not, the data is also indexed.
		"""
						
		try:
			stats = os.stat(self.zotero_database)		
		except Exception as e:
			print "libzotero.update(): %s" % e
			return False

		# Only update if necessary		
		if not force and stats[8] > self.last_update:
			
			t = time.time()
			
			self.last_update = stats[8]
			self.index = {}
			self.collection_index = []
			self.search_cache = {}

			# Copy the zotero database to the gnotero copy
			shutil.copyfile(self.zotero_database, self.gnotero_database)
			self.conn = sqlite3.connect(self.gnotero_database)	
			self.cur = self.conn.cursor()
			
			# First create a list of deleted items, so we can ignore those later
			deleted = []
			self.cur.execute(self.deleted_query)	
			for item in self.cur.fetchall():	
				deleted.append(item[0])
				
			# Retrieve information about date, publication, volume, issue and title
			self.cur.execute(self.info_query)
			for item in self.cur.fetchall():
				item_id = item[0]
				key = item[3]
				if item_id not in deleted:
					item_name = item[1]
	
					# Parse date fields, because we only want a year or a 'special' date
					if item_name == "date":
						item_value = None
						for sd in self.special_dates:
							if sd in item[2].lower():
								item_value = sd
								break
						if item_value == None:
							item_value = item[2][-4:]
					else:
						item_value = item[2]		
						
					if item_id not in self.index:
						self.index[item_id] = zotero_item(item_id, \
							noteProvider=self.noteProvider)
						self.index[item_id].key = key
						
					if item_name == "publicationTitle":
						self.index[item_id].publication = item_value
					elif item_name == "date":
						self.index[item_id].date = item_value
					elif item_name == "volume":
						self.index[item_id].volume = item_value 
					elif item_name == "issue":
						self.index[item_id].issue = item_value
					elif item_name == "title":
						self.index[item_id].title = item_value
					
			# Retrieve author information
			self.cur.execute(self.author_query)
			for item in self.cur.fetchall():
				item_id = item[0]
				if item_id not in deleted:
					item_author = item[1].capitalize()
					if item_id not in self.index:
						self.index[item_id] = zotero_item(item_id)
					self.index[item_id].authors.append(item_author)	
		
			# Retrieve collection information
			self.cur.execute(self.collection_query)
			for item in self.cur.fetchall():
				item_id = item[0]
				if item_id not in deleted:
					item_collection = item[1]
					if item_id not in self.index:
						self.index[item_id] = zotero_item(item_id)
					self.index[item_id].collections.append(item_collection)
					if item_collection not in self.collection_index:
						self.collection_index.append(item_collection)		
						
			# Retrieve attachments
			self.cur.execute(self.attachment_query)
			for item in self.cur.fetchall():
				item_id = item[0]
				if item_id not in deleted:
					if item[1] != None:
					
						att = item[1]

						# If the attachment is stored in the Zotero folder, it is preceded
						# by "storage:"
						if att[:8] == "storage:":
							item_attachment = att[8:]
							attachment_id = item[2]								   
							if item_attachment[-4:].lower() in self.attachment_ext:
								if item_id not in self.index:
									self.index[item_id] = zotero_item(item_id)
								self.cur.execute("select items.key from items where itemID = %d" % attachment_id)
								key = self.cur.fetchone()[0]							
								self.index[item_id].fulltext = os.path.join(self.storage_path, key, item_attachment)
								
						# If the attachment is linked, it is simply the full path to the attachment
						else:
							self.index[item_id].fulltext = att	

			self.cur.close()
			
			print "libzotero.update(): indexing completed in %.3fs" % (time.time() - t)
		return True
			
	def parse_query(self, query):
	
		"""
		Parses a text search query into a list of tuples,
		which are acceptable for zotero_item.match()
		"""
		
		# Make sure that spaces are handled correctly after
		# semicolons. E.g., Author: Mathot
		while ": " in query:
			query = query.replace(": ", ":")
	
		# Parse the terms into a suitable format
		terms = []
		# Check if the criterium is type-specified, like "author: doe"		
		import shlex
		for term in query.strip().lower().split():
			s = term.split(":")
			if len(s) == 2:
				terms.append( (s[0].strip(), s[1].strip()) )
			else:
				terms.append( (None, term.strip()) )	
		return terms				
		
	def search(self, query):
		
		"""
		Search the zotero database
		"""
		
		if not self.update():
			return []
		
		if query in self.search_cache:
			print "libzotero.search(): retrieving results for '%s' from cache" % query
			return self.search_cache[query]
		
		t = time.time()		
		terms = self.parse_query(query)
		results = []		
		for item_id, item in self.index.items():			
			if item.match(terms):					
				results.append(item)
		self.search_cache[query] = results	
		print "libzotero.search(): search for '%s' completed in %.3fs" % (query, time.time() - t)
				
		return results	
			
def valid_location(path):

	"""
	Checks if a given path is a valid Zotero folder,
	i.e., if it it contains zotero.sqlite
	"""	
	
	return os.path.exists(os.path.join(path, "zotero.sqlite"))
	