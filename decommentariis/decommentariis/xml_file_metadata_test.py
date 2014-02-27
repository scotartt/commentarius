import unittest, json, os
from xml_file import TEIDataSource

sallust_cataline = "urn:cts:latinLit:phi0631.phi001.perseus-lat2"
homer_iliad = "urn:cts:greekLit:tlg0012.tlg001.perseus-grc1"
caesar_gallic = "urn:cts:latinLit:phi0448.phi001.perseus-lat1"
cicero_derepublica ="urn:cts:latinLit:phi0474.phi043.perseus-lat1"
junk_cts = "asjgk:sajgksa:asdgsag:.sagjksa"
urncts_junk_cts = "urn:cts:asdgsag:.sagjksa"
urnctslatinlit_junk_cts = "urn:cts:latinLit:phoo123.sagjksa"
does_not_exist_cts = "urn:cts:latinLit:phi9999.phi999.perseus-lat9"
strabo_geo = "urn:cts:greekLit:tlg0099.tlg001.perseus-grc1"

# where the files are.
if not os.environ.get("CTS_DATA_PATH"):
	os.environ.setdefault("CTS_DATA_PATH", "/Users/smcphee/Development/sources/commentarius/data/canonical/CTS_XML_TEI/perseus/")

class TestTEIDataSource(unittest.TestCase):
 
	def setUp(self):
		pass

	
	def test_sallust_load(self):
		print("\n======================\n%s" % sallust_cataline)
		# this is a test document URI
		tds = TEIDataSource(sallust_cataline)
		self.assertNotEqual(tds.source_desc, None)
		i = 0
		for s in tds.sections:
			i += 1
			# print(str(i) + "=" + s)
		self.assertEqual(i, 1)
		self.assertEqual(tds.delim, ',') #default
		self.assertIsNotNone(tds.document_metastructure)
		self.printdetail(tds)

		

	def test_caesar_load(self):
		print("\n======================\n%s" % caesar_gallic)
		tds = TEIDataSource(caesar_gallic)
		self.assertNotEqual(tds.source_desc, None)
		i = 0
		for s in tds.sections:
			i += 1
			# print(str(i) + "=" + s)
		self.assertEqual(i, 3)
		self.assertEqual(tds.delim, ".")
		self.assertIsNotNone(tds.document_metastructure)
		self.printdetail(tds)

	def test_cicero_load(self):
		print("\n======================\n%s" % cicero_derepublica)
		tds = TEIDataSource(cicero_derepublica)
		self.assertIsNotNone(tds.source_desc)
		i = 0
		for s in tds.sections:
			i += 1
			#print(str(i) + "=" + s)
		self.assertEqual(i, 2)
		self.assertEqual(tds.delim, ',') #default
		self.assertIsNotNone(tds.document_metastructure)
		self.printdetail(tds)

	def test_strabo_load(self):
		print("\n======================\n%s" % strabo_geo)
		tds = TEIDataSource(strabo_geo)
		self.assertNotEqual(tds.source_desc, None)
		i = 0
		for s in tds.sections:
			i += 1
			# print(str(i) + "=" + s)
		self.assertEqual(i, 3)
		#self.assertEqual(tds.delim, ".")
		self.assertIsNotNone(tds.document_metastructure)
		self.assertEqual("Strabo", tds.author)
		self.printdetail(tds)

	def printdetail(self, tds):
		print(str(tds.author) + ", '" + str(tds.title) + "', " + str(tds.editor) + ", " + str(tds.publisher) + ": " + str(tds.pubPlace) + ", " + str(tds.date))

if __name__ == '__main__':
	unittest.main()
