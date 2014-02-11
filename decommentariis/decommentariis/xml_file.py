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

	def read_fragment(self, ref="1.1"):
		"reads a fragment from the source. ref must be dot-separated reference compliant with the expected schema of the source"
		fo = self.open_source()
		parser = etree.XMLParser(ns_clean=True, resolve_entities=False)
		root = etree.parse(fo, parser)
		## see http://lxml.de/xpathxslt.html for more detail to expand
		elems = root.xpath(".//div1[@type='chapter'][@n='1']")
		for e in elems:
			for p in e.iter("p"):
				print(etree.tostring(p))

	def close_source(self):
		self.fo.close()

	def open_source(self):
		cts_uri_frag = self.get_path_component(self.urn)
		the_file_name = self.get_file_name(cts_uri_frag)
		self.fo = open(self.corpus + self.file_name, 'r')
		return self.fo

	def get_file_name(self, cts_uri_frag=None):
		path_part = cts_uri_frag.split(".")
		path_part = path_part[:len(path_part)-1] #don't want the last part of the path, it's not a directory.
		for p in path_part:
			if not p.startswith(self.corpus_prefix):
				raise Exception("Corpus must be '" + self.corpus_prefix + "': " + self.urn)
		self.file_name = "/".join(path_part) + "/" + cts_uri_frag + ".xml"
		print("file is " + self.file_name)
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


# this is a test document URI
sallust_cataline = "urn:cts:latinLit:phi0631.phi001.perseus-lat2"
tds = TEIDataSource(sallust_cataline)
fo = tds.open_source()
print("Name of the file: ", fo.name)
print("Closed or not : ", fo.closed)
print("Opening mode : ", fo.mode)
tds.close_source()
tds.read_fragment("1.1")



