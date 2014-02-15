"""
This python class is used to get the data off the file system.
"""
from lxml import etree
import os

data_dir = "../../data/canonical/CTS_XML_TEI/perseus/"
latin_lit = data_dir + "latinLit/"
greek_lit = data_dir + "greekLit/"
latin_corpus_prefix = "phi" # package humanities institute
greek_corpus_prefix = "tlg" # thesaurus linguae graecae

class TEIDataSource:
	"This class abstracts access to the XML data in the Perseus TEI files. Expects CTS compliant URN to be passed to constructor."
	def __init__(self, urn=""):
		if not urn.startswith("urn:cts:"):
			raise Exception("The URN is not a CTS URN. " + urn)
		self.urn = urn
		cts_uri_frag = self.get_path_component(self.urn)
		the_file_name = self.get_file_name(cts_uri_frag)
		self.current_text = str()
		self.prev_text = str()
		self.read_doc_metadata()

	def read_fragment(self, ref="1"):
		"reads a fragment from the source. ref must be dot-separated reference compliant with the expected schema of the source"
		if not ref in self.document_struct_flat:
			msg = "This ref '" + ref + "' not in valid refs list: " + str(self.document_struct_flat)
			print(msg)
			raise Exception(msg)
		refs=[]
		if ref and self.delim:
			refs = ref.split(self.delim)
		elif ref:
			refs = ref.split() #i.e. white space
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
			xpathstr += "/div%s" % str(i) #div1, div2, div3 etc
			xpathstr += "[@type='%s']" % self.sections[i-1]
			xpathstr += "[@n='%s']" % r

		print("query on %s = %s" % (self.file_name, xpathstr))	
		## see http://lxml.de/xpathxslt.html for more detail to expand
		elems = root.xpath(xpathstr)

		if elems and len(elems):
			self.prev_text = self.current_text
			self.current_text = str()
			for e in elems:
				self.current_text += str(etree.tostring(e, pretty_print=True), encoding='utf-8')
		else:
			self.close_source(fo) 
			raise Exception("No text part with ref: "+ str(ref))

		self.close_source(fo) 
		return self.current_text


	def read_doc_metadata(self):
		"loads the sourceDesc element (title and author details) of the document and chapter breakdown."
		self.source_desc = ""
		fo = self.open_source()
		parser = self.parser()
		root = etree.parse(fo, parser)
		src_elems = root.xpath("/TEI.2/teiHeader/fileDesc/sourceDesc")
		for e in src_elems:
			self.source_desc += str(etree.tostring(e, pretty_print=True), encoding='utf-8')
		self.get_metadata_sections(root)
		self.close_source(fo)

	def get_metadata_sections(self, root):
		"this method extracts the metadata about the document sections."
		self.sections = []
		self.delim = None
		sect_elems = root.xpath("/TEI.2/teiHeader/encodingDesc/refsDecl/state")
		## print("found refsDecl/state elems count=" + str(len(sect_elems)))
		for sect in sect_elems:
			self.sections.append(sect.get("unit"))
			if sect.get("delim"):
				self.delim = sect.get("delim")
		self.get_sections(root)

	def get_sections(self, root):
		"this method gets each type of section in the document and creates a navigable document structure indicator"
		if self.sections:
			self.sectionslist = []
			i = 0
			self.sectionslist = self.xml_element_recursion(i, root)
			self.doc_struct()

	def xml_element_recursion(self, i, container):
		"This method parses TEI compatible XML for recursive document elements according to the metadata extracted about those document elements"
		# method below here
		maxi = len(self.sections)
		if  i < maxi:
			xpathstr = ".//div%d" % (i+1)
			sect = self.sections[i]
			typestr = "[@type='%s']" % sect
			xpathstr += typestr
			divs = container.xpath(xpathstr)
			_temp = []
			for div in divs:
				div_dict = dict(div.attrib)
				#print(div_dict['type'] + "=" + div_dict['n'])
				children = self.xml_element_recursion(i+1, div)
				if children :
					div_dict["children"] = children
				_temp.append(div_dict)
			return _temp
		else:
			return None
		# method ends here

	def doc_struct(self):
		"This method gets the list of valid references in the document. The references are formatted with the metadata specified delimiter, e.g. 1.2.3. There are two structures. One is a 'proper' structure i.e. a map of the document. The other is a simple 'flat' list of the valid reference strings."
		delim = self.delim
		if not delim:
			delim = " "
		self.document_struct = {}
		self.document_struct['_metadata_structure_list'] = self.sections
		self.document_struct['_metadata_structure_delim'] = delim
		self.document_struct['_metadata_document_urn'] = self.urn
		self.document_struct['_metadata_document_description'] = self.source_desc
		self.document_struct['document_structure'] = []
		self.document_struct_flat = []
		for section_elem in self.sectionslist:
			tree_top_elem = {}
			tree_top_elem["ref_type"] = str(section_elem['type'])
			tree_top_elem["ref_n"] = str(section_elem['n'])
			self.document_struct_flat.append(str(section_elem['n']))
			if 'children' in section_elem:
				children = self.doc_struct_recurse(delim, section_elem['children'], str(section_elem['n']))
				if children:
					tree_top_elem['xchildren'] = children
			self.document_struct['document_structure'].append(tree_top_elem)

	def doc_struct_recurse(self, delim, child_list, parent_str):
		"This is the recursive method used by doc_struct()"
		if child_list:
			child_tree_items =[]
			for child in child_list:
				refstr = "%s%s%s" % (parent_str, delim, str(child['n']))
				self.document_struct_flat.append(refstr)
				tree_item = {}
				tree_item['ref_type'] = child['type']
				tree_item['ref_n'] = refstr
				if 'children' in child:
					children = self.doc_struct_recurse(delim, child['children'], refstr)
					if children:
						tree_item['xchildren'] = children
				# end if
				child_tree_items.append(tree_item)
			# end for
			return child_tree_items
		else:
			return None

	def parser(self):
		return etree.XMLParser(ns_clean=True, resolve_entities=False, no_network=True)

	def close_source(self, fo=None):
		if fo:
			fo.close()
			
	def open_source(self):
		return open(self.corpus + self.file_name, 'r')

	def get_file_name(self, cts_uri_frag=None):
		dirs_part = cts_uri_frag.split(".")
		dirs_part = dirs_part[:len(dirs_part)-1] #don't want the last part of the path, it's not a directory.
		for d in dirs_part:
			if not d.startswith(self.corpus_prefix):
				raise Exception("Corpus must be '" + self.corpus_prefix + "': " + self.urn)
		self.file_name = "/".join(dirs_part) + "/" + cts_uri_frag + ".xml"
		# print("file is " + self.file_name)
		return self.file_name

	def get_path_component(self, urn="urn:cts:"):
		path_component = urn.replace("urn:cts:", "")
		if path_component.startswith("latinLit:"):
			self.corpus = latin_lit
			self.corpus_prefix = latin_corpus_prefix
			path_component = path_component.replace("latinLit:", "")
		elif path_component.startswith("greekLit:"):
			self.corpus = greek_lit
			self.corpus_prefix = greek_corpus_prefix
			path_component = path_component.replace("greekLit:", "")
		else:
			raise Exception("The URN is not a Latin or Greek corpus. " + urn)
		return path_component
