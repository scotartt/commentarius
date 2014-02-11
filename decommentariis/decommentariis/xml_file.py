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
	def __init__(self, urn=""):
		if not urn.startswith("urn:cts:"):
			raise Exception("The URN is not a CTS URN. " + urn)
		self.urn = urn

	def open_source(self):
		cts_uri_frag = self.get_path_components(self.urn)
		path_component = cts_uri_frag.split(".")
		path_component = path_component[:len(path_component)-1] #don't want the last part of the path, it's not a directory.
		self.file_name = "/".join(path_component) + "/" + cts_uri_frag + ".xml"
		print("file is " + self.file_name)
		self.fo = open(self.corpus + self.file_name, 'r')
		print("Name of the file: ", self.fo.name)
		print("Closed or not : ", self.fo.closed)
		print("Opening mode : ", self.fo.mode)
		return self.fo

	def get_path_components(self, urn="urn:cts:"):
		path_c = urn.replace("urn:cts:", "")
		if path_c.startswith("latinLit:"):
			self.corpus = latin_lit
			self.corpus_prefix = latin_corpus_prefix
			path_c = path_c.replace("latinLit:", "")
		elif path_c.startswith("greekLit:"):
			self.corpus = greek_lit
			self.corpus_prefix = greek_corpus_prefix
			path_c = path_c.replace("greekLit:", "")
		else:
			raise Exception("The URN is not a Latin or Greek corpus. " + urn)
		if not path_c.startswith(self.corpus_prefix):
			raise Exception("Corpus must be either 'phi' or 'tlg': " + urn)
		return path_c


# this is a test document URI
sallust_cataline = "urn:cts:latinLit:phi0631.phi001.perseus-lat2"
tds = TEIDataSource(sallust_cataline)
fo = tds.open_source()
fo.close()


