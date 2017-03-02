"""
These python classes are used to get the data off the file system.
"""
from lxml import etree
import os
import locale
import sys

data_dir = "/var/www/commentarius/data/canonical/CTS_XML_TEI/perseus/"
if os.environ.get("CTS_DATA_PATH"):
	data_dir = os.environ.get("CTS_DATA_PATH")
else:
	print('Using default value for "data_dir":"' + data_dir + '"')

latin_lit = data_dir + "latinLit/"
greek_lit = data_dir + "greekLit/"
latin_corpus_prefix = "phi"  # package humanities institute
latin_corpus_prefix_2 = "stoa"  # stoa texts
greek_corpus_prefix = "tlg"  # thesaurus linguae graecae
default_delim = ","

print('encoding is ' + locale.getpreferredencoding(False), file=sys.stderr)


class TEIDataSource:
	"""This class abstracts access to the XML data in the Perseus TEI files.
Expects CTS compliant URN to be passed to constructor."""
	# These fields (strings) simply encode various attributes parsed either
	# from the given argument or out of the document.
	urn = None
	corpus = None
	file_name = None
	author = None
	title = None
	publisher = None
	pubPlace = None
	date = None
	editor = None
	# These fields (data structures) that tell us about the structure of the document
	current_text = None
	prev_text = None
	source_desc = None
	delim = None
	sections = []
	xml_sections_list = []
	document_metastructure = {}
	document_metastructure_flat = []
	
	def __init__(self, urn=None):
		if urn:
			self.load(urn)
		else:
			pass
	
	def load(self, urn=""):
		if not urn.startswith("urn:cts:"):
			raise Exception("The URN is not a CTS URN. " + urn)
		self.urn = urn
		cts_uri_frag = self.get_path_component(self.urn)
		self.file_name = self.get_file_name(cts_uri_frag)
		self.current_text = str()
		self.prev_text = str()
		self.read_doc_metadata()
	
	def read_fragment(self, ref="1"):
		"""reads a fragment from the source. ref must be dot-separated reference
		compliant with the expected schema of the source"""

		if ref not in self.document_metastructure_flat:
			msg = "This ref '" + ref + "' not in valid refs list: " + str(self.document_metastructure_flat)
			print(msg)
			raise Exception(msg)
		refs = []
		if ref and self.delim:
			refs = ref.split(self.delim)
		elif ref:
			refs = ref.split(default_delim)
		else:
			raise Exception("No ref given.")
		
		fo = self.open_source()
		parser = self.parser()
		root = etree.parse(fo, parser)
		i = 0
		xpathstr = "./"
		for r in refs:
			# print("Adding " + r + " to " + xpathstr)
			i += 1
			xpathstr = "{0}/div{1}[@type='{2}'][@n='{3}']".format(xpathstr, str(i), self.sections[i - 1], r)
		# e.g. {xpathstr}/div1[@type='book'][@n='2']
		# print("query on %s = %s" % (self.file_name, xpathstr))	
		# see http://lxml.de/xpathxslt.html for more detail to expand
		elems = root.xpath(xpathstr)
		
		if elems and len(elems):
			self.prev_text = self.current_text
			self.current_text = str()
			for e in elems:
				self.current_text += str(etree.tostring(e, pretty_print=True), encoding='utf-8')
		else:
			self.close_source(fo)
			raise Exception("No text part with ref: " + str(ref))
		
		self.close_source(fo)
		return self.current_text
	
	def read_doc_metadata(self):
		""""loads the sourceDesc element (title and author details) of the document and chapter breakdown."""
		self.source_desc = ""
		fo = self.open_source()
		parser = self.parser()
		root = etree.parse(fo, parser)
		src_elems = root.xpath("/TEI.2/teiHeader/fileDesc/titleStmt")
		# | /TEI.2/teiHeader/fileDesc/sourceDesc")
		# get them all. first one found for each field wins.
		for e in src_elems:
			self.source_desc += str(etree.tostring(e, pretty_print=True), encoding='utf-8')
			self.populate_bib_fields(src_elems[0])
		src_elems = root.xpath("/TEI.2/teiHeader/fileDesc/sourceDesc")
		# | /TEI.2/teiHeader/fileDesc/sourceDesc")
		# get them all. first one found for each field wins.
		for e in src_elems:
			self.source_desc += str(etree.tostring(e, pretty_print=True), encoding='utf-8')
			self.populate_bib_fields(src_elems[0])
		self.get_metadata_sections(root)
		self.close_source(fo)
	
	def populate_bib_fields(self, e):
		author_e = e.xpath(".//author")
		if len(author_e) and not self.author:
			self.author = author_e[0].text
		
		title_e = e.xpath(".//title[@type != 'sub']")
		if len(title_e) and not self.title:
			self.title = ""
			i = 0
			for t in title_e:
				if t.text:
					if i > 0:
						self.title += "; "
					self.title += t.text
					i += 1
		# end
		
		if not self.title or len(self.title) < 3:
			title_e = e.xpath(".//title[not(@type)]")
			if len(title_e):
				self.title = ""
				i = 0
				for t in title_e:
					if t.text:
						if i > 0:
							self.title += "; "
						self.title += t.text
						i += 1
		# end
		
		publisher_e = e.xpath(".//publisher")
		if len(publisher_e) and not self.publisher:
			self.publisher = ""
			i = 0
			for p in publisher_e:
				if p.text:
					if i > 0:
						self.publisher += ", "
					self.publisher += p.text
					i += 1
		# end
		
		date_e = e.xpath(".//date")
		if len(date_e) and not self.date:
			self.date = date_e[0].text
		
		editor_e = e.xpath(".//editor")
		if len(editor_e) and not self.editor:
			self.editor = ""
			i = 0
			for ed in editor_e:
				if ed.text:
					if i > 0:
						self.editor += ", "
					self.editor += ed.text
					i += 1
		# end
		
		pub_place_e = e.xpath(".//pubPlace")
		if len(pub_place_e) and not self.pubPlace:
			self.pubPlace = ""
			i = 0
			for pp in pub_place_e:
				if pp.text:
					if i > 0:
						self.pubPlace += ", "
					self.pubPlace += pp.text
					i += 1
				# end
	
	# end function
	
	def get_metadata_sections(self, root):
		"""this method extracts the metadata about the document sections."""
		self.sections = []
		self.delim = None
		sect_elems = root.xpath(
			"/TEI.2/teiHeader/encodingDesc/refsDecl/state | /TEI.2/teiHeader/encodingDesc/refsDecl/step")
		if sect_elems and len(sect_elems):
			# print("found refsDecl/state elems count=" + str(len(sect_elems)))
			for sect in sect_elems:
				if sect.get("unit"):
					self.sections.append(sect.get("unit"))
				elif sect.get("refunit"):
					self.sections.append(sect.get("refunit"))
				if sect.get("delim"):
					self.delim = sect.get("delim")
			self.get_sections(root)
		else:
			raise Exception("No parsable metadata!")
	
	def get_sections(self, root):
		"""this method gets each type of section in the document and
		creates a navigable document structure indicator"""
		if self.sections:
			self.xml_sections_list = []
			i = 0
			self.xml_sections_list = self.xml_element_recursion(i, root)
			self.doc_structure()
	
	def xml_element_recursion(self, i, container):
		"""This method parses TEI compatible XML for recursive document elements
		according to the metadata extracted about those document elements"""
		# method below here
		maxi = len(self.sections)
		if i < maxi:
			xpathstr = ".//div%d" % (i + 1)
			sect = self.sections[i]
			typestr = "[@type='%s']" % sect
			xpathstr += typestr
			divs = container.xpath(xpathstr)
			_temp = []
			for div in divs:
				div_dict = dict(div.attrib)
				# print(div_dict['type'] + "=" + div_dict['n'])
				children = self.xml_element_recursion(i + 1, div)
				if children:
					div_dict["children"] = children
				_temp.append(div_dict)
			return _temp
		else:
			return None
		# method ends here
	
	def doc_structure(self):
		"""This method gets the list of valid references in the document.
		The references are formatted with the metadata specified delimiter, e.g. 1.2.3.
		There are two structures. One is a 'proper' structure i.e. a map of the document.
		The other is a simple 'flat' list of the valid reference strings."""
		if not self.delim:
			self.delim = default_delim
		delim = self.delim
		self.document_metastructure = {
			'_metadata_structure_list': self.sections,
			'_metadata_structure_delim': delim,
			'_metadata_document_urn': self.urn,
			'_metadata_document_description': self.source_desc,
			'document_structure': []
			}
		self.document_metastructure_flat = []
		for section_elem in self.xml_sections_list:
			tree_top_elem = {
				'ref_type': str(section_elem['type']),
				'ref_n': str(section_elem['n'])
			}
			self.document_metastructure_flat.append(str(section_elem['n']))
			if 'children' in section_elem:
				children = self.doc_structure_recurse(delim, section_elem['children'], str(section_elem['n']))
				if children:
					tree_top_elem['xchildren'] = children
			self.document_metastructure['document_structure'].append(tree_top_elem)
	
	def doc_structure_recurse(self, delim, child_list, parent_str):
		"""This is the recursive method used by doc_structure().
		Each child contains the full reference to the parent.child relationship
		with the nominated delimiter, in the tree_item['ref_n'] entry of the returned dict."""
		if child_list:
			child_tree_items = []
			for child in child_list:
				refstr = "%s%s%s" % (parent_str, delim, str(child['n']))
				self.document_metastructure_flat.append(refstr)
				tree_item = {
					'ref_type': child['type'],
					'ref_n': refstr
				}
				if 'children' in child:
					children = self.doc_structure_recurse(delim, child['children'], refstr)
					if children:
						tree_item['xchildren'] = children
				# end if
				child_tree_items.append(tree_item)
			# end for
			return child_tree_items
		else:
			return None
	
	@staticmethod
	def parser():
		return etree.XMLParser(ns_clean=True, resolve_entities=False, no_network=True, encoding='utf-8')
	
	@staticmethod
	def close_source(fo=None):
		if fo:
			fo.close()
	
	def open_source(self):
		"""Opens the source file nominated from the URN give at construction."""
		return open(self.corpus + self.file_name, 'r')
	
	@staticmethod
	def get_file_name(cts_uri_frag=None):
		"""Given the URN, determines the file name which should contain the data."""
		dirs_part = cts_uri_frag.split(".")
		dirs_part = dirs_part[:len(dirs_part) - 1]  # don't want the last part of the path, it's not a directory.
		file_name = "/".join(dirs_part) + "/" + cts_uri_frag + ".xml"
		# print("file is " + self.file_name)
		return file_name
	
	def get_path_component(self, urn="urn:cts:"):
		path_component = urn.replace("urn:cts:", "")
		if path_component.startswith("latinLit:"):
			self.corpus = latin_lit
			path_component = path_component.replace("latinLit:", "")
		elif path_component.startswith("greekLit:"):
			self.corpus = greek_lit
			path_component = path_component.replace("greekLit:", "")
		else:
			raise Exception("The URN is not a Latin or Greek corpus. " + urn)
		return path_component
	
	def print_bib_detail(self):
		fnone = lambda s: str(s) if s else "-"
		return "{0}, '{1}', (ed. {2}), {3} : {4}, {5}".format(fnone(self.author), fnone(self.title), fnone(self.editor),
															  fnone(self.publisher), fnone(self.pubPlace),
															  fnone(self.date)).replace("\n", " ").replace("  ", " ")
