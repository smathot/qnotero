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

term_collection = None, "collection"
term_tag = None, "tag"
term_author = None, "author"
term_date = None, "date", "year"
term_publication = None, "publication", "journal"
term_title = None, "title"

cache = {}

class zoteroItem:

	"""
	Contains a single zotero item.
	"""

	def __init__(self, init=None, noteProvider=None):

		"""
		Initialization can be done using a dictionary or
		and int (which is interpreted as the item id)
		"""

		self.gnotero_format_str = None
		self.simple_format_str = None
		self.filename_format_str = None
		self.collection_color = "#000000"
		self.noteProvider = noteProvider
		self.note = -1

		if type(init) == dict:

			if "item_id" in item:
				self.id = item["item_id"]
			else:
				self.id = None

			if "publicationTitle" in item:
				self.publication = item["publicationTitle"]
			else:
				self.publication = None

			if "title" in item:
				self.title = item["title"]
			else:
				self.title = None

			if "author" in item:
				self.authors = item["author"]
			else:
				self.authors = []

			if "date" in item:
				self.date = item["date"]
			else:
				self.date = None

			if "issue" in item:
				self.issue = item["issue"]
			else:
				self.issue = None

			if "volume" in item:
				self.volume = item["volume"]
			else:
				self.volume = None

			if "fulltext" in item:
				self.fulltext = item["fulltext"]
			else:
				self.fulltext = None

			if "collections" in item:
				self.collections = item["collections"]
			else:
				self.collections = []
				
			if "tags" in item:
				self.tags = item["tags"]
			else:
				self.tags = []

			if "key" in item:
				self.key = item["key"]
			else:
				self.key = None

		else:
			self.title = None
			self.collections = []
			self.publication = None
			self.authors = []
			self.tags = []
			self.issue = None
			self.volume = None
			self.fulltext = None
			self.date = None
			self.key = None

			if type(init) == int:
				self.id = init
			else:
				self.id = None

	def match(self, terms):

		"""
		Returns true if this item matches the specified
		search terms (e.g., author: "Doe"), else returns
		false
		"""

		global term_collection, term_author, term_title, term_date, \
			term_publication, term_tag

		# Author is a required field. Without it we don't search
		if len(self.authors) > 0:

			# Do all criteria match?
			match_all = True

			# Walk through all search terms
			for term_type, term in terms:

				match = False

				if term_type in term_tag:
					for tag in self.tags:
						if term in tag.lower():
							match = True
							
				if term_type in term_collection:
					for collection in self.collections:
						if term in collection.lower():
							match = True

				if not match and term_type in term_author:
					for author in self.authors:
						if term in author.lower():
							match = True

				if not match and self.date != None and term_type in term_date:
					if term in self.date:
						match = True

				if not match and self.title != None and term_type in term_title and term in self.title.lower():
					match = True

				if not match and self.publication != None and term_type in term_publication and term in self.publication.lower():
					match = True
								
				if not match:
					match_all = False
					break

			return match_all

		return False

	def get_note(self):

		"""Retrieve a note"""

		if self.note != -1:
			return self.note

		self.note = self.noteProvider.search(self)
		return self.note

	def format_author(self):

		"""
		Give a nice representation of the author
		"""

		if self.authors == []:
			return "Unkown author"

		if len(self.authors) > 5:
			return "%s et al." % self.authors[0]

		if len(self.authors) > 2:
			return ", ".join(self.authors[:-1]) + ", & " + self.authors[-1]

		if len(self.authors) == 2:
			return self.authors[0] + " & " + self.authors[1]

		return self.authors[0]

	def format_date(self):

		"""
		Give a nice representation of the date
		"""

		if self.date == None:
			return "(Date unknown)"

		return "(" + self.date + ")"

	def format_title(self):

		"""
		Give a nice representation of the date
		"""

		if self.title == None:
			return "Unknown title"

		return self.title

	def format_publication(self):

		"""
		Give a nice representation of the date
		"""

		if self.publication == None:
			return "Unknown journal"

		return self.publication
	
	def format_tags(self):
		
		"""
		Give a nice representation of the tags
		"""
		
		return ", ".join(self.tags)

	def gnotero_format(self):

		"""
		Gives a nice apa-like representation of the item, which can
		be used a label in gnotero
		"""

		if self.gnotero_format_str == None:
			s =  "<b>" + self.format_author() + " " + self.format_date() + "</b>"
			if self.title != None:
				s += "\n<small>" + self.title
			if self.publication != None:
				s += "\n<i>" + self.publication
				if self.volume != None:
					s += ", %s" % self.volume
				s += "</i>"
				if self.issue != None:
					s += "(%s)" % self.issue
			s += "</small>"

			self.gnotero_format_str = s.replace("&", "&amp;")

		return self.gnotero_format_str

	def full_format(self):

		if self.gnotero_format_str == None:
			s =  self.format_author() + " " + self.format_date()
			if self.title != None:
				s += "\n" + self.title
			if self.publication != None:
				s += "\n" + self.publication
				if self.volume != None:
					s += ", %s" % self.volume
				if self.issue != None:
					s += "(%s)" % self.issue
			else:
				s += "\n"
			if self.tags != None:
				s += "\n" + self.format_tags()

			self.gnotero_format_str = s

		return self.gnotero_format_str

	def simple_format(self):

		if self.simple_format_str == None:
			self.simple_format_str = self.format_author() + " " + self.format_date()
		return self.simple_format_str

	def filename_format(self):

		if self.filename_format_str == None:
			self.filename_format_str = self.format_author() + " " + self.format_date().encode("ascii", "ignore").replace("\\", "")
		return self.filename_format_str

	def hashKey(self):

		global cache
		hashKey = unicode(self)
		cache[hashKey] = self
		return hashKey
