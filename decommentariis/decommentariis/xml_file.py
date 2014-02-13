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
		if self.sections:
			self.sectionslist = []
			i = 0
			self.sectionslist = self.recursion_of_elements(i, root)
			#print ("COMPLETE METADATA")	

	def recursion_of_elements(self, i, container):
		# method below here
		maxi = len(self.sections)
		if  i < maxi:
			xpathstr = ".//div%d" % (i+1)
			sect = self.sections[i]
			typestr = "[@type='%s']" % sect
			xpathstr += typestr
			#print(str(i) + " = " + xpathstr)
			div1s = container.xpath(xpathstr)
			_temp = []
			#print("AT %d THE COUNT OF CHILDREN IS %d" % (i, len(div1s)))
			for d in div1s:
				ddict = dict(d.attrib)
				#print(ddict['type'] + "=" + ddict['n'])
				childs = self.recursion_of_elements(i+1, d)
				ddict["children"] = childs
				_temp.append(ddict)

			##print ("DONE NOW %d with %s, have count %d" % (i, sect, len(_temp)))
			return _temp
		else:
			#print("The test has ended at %d attempts" % i)
			return None
		# method ends here


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
