import unittest, os
from xml_file import TEIDataSource
 
sallust_cataline = "urn:cts:latinLit:phi0631.phi001.perseus-lat2"
homer_iliad = "urn:cts:greekLit:tlg0012.tlg001.perseus-grc1"
caesar_gallic = "urn:cts:latinLit:phi0448.phi001.perseus-lat1"
cicero_derepublica ="urn:cts:latinLit:phi0474.phi043.perseus-lat1"
propertius = "urn:cts:latinLit:phi0620.phi001.perseus-lat2"
junk_cts = "asjgk:sajgksa:asdgsag:.sagjksa"
urncts_junk_cts = "urn:cts:asdgsag:.sagjksa"
urnctslatinlit_junk_cts = "urn:cts:latinLit:phoo123.sagjksa"
does_not_exist_cts = "urn:cts:latinLit:phi9999.phi999.perseus-lat9"
# where the files are.
if not os.environ.get("CTS_DATA_PATH"):
	os.environ.setdefault("CTS_DATA_PATH", "/Users/smcphee/Development/sources/commentarius/data/canonical/CTS_XML_TEI/perseus/")


class TestTEIDataSource(unittest.TestCase):
 
	def setUp(self):
		pass

	def test_junk_cts_fails(self):
		print("")
		# this is a test document URI
		with self.assertRaises(Exception):
			tds = TEIDataSource(junk_cts)

	def test_sallust_loads(self):
		print("")
		# this is a test document URI
		tds = TEIDataSource(sallust_cataline)
		fo = tds.open_source()
		# print("Name of the file: ", fo.name)
		# print("Closed or not : ", fo.closed)
		# print("Opening mode : ", fo.mode)
		tds.close_source(fo)

	def test_homer_loads(self):
		print("")
		# this is a test document URI
		tds = TEIDataSource(homer_iliad)
		fo = tds.open_source()
		# print("Name of the file: ", fo.name)
		# print("Closed or not : ", fo.closed)
		# print("Opening mode : ", fo.mode)
		tds.close_source(fo)

	def test_homer_unreadable(self):
		print("")
		tds = TEIDataSource(homer_iliad)
		with self.assertRaises(Exception): #, "No text part with ref: 1"):
			text = tds.read_fragment('1')
			#print(text)


	def test_sallust_reads_metadata(self):
		print("")
		tds = TEIDataSource(sallust_cataline)
		tds.read_doc_metadata()
		self.assertNotEqual(tds.source_desc, None)
		# print(tds.source_desc)
		i = 0
		for s in tds.sections:
			i += 1
			# print(str(i) + "=" + s)
		self.assertEqual(i, 1)
		self.assertIsNone(tds.delim)
		# print("delimiter=" + str(tds.delim))

	def test_caesar_reads_metadata(self):
		print("")
		tds = TEIDataSource(caesar_gallic)
		tds.read_doc_metadata()
		self.assertNotEqual(tds.source_desc, None)
		#print(tds.source_desc)
		i = 0
		for s in tds.sections:
			i += 1
			# print(str(i) + "=" + s)
		self.assertEqual(i, 3)
		self.assertEqual(tds.delim, ".")
		# print("delimiter=" + tds.delim)

	def test_propertius_reads_1_2(self):
		print("")
		tds = TEIDataSource(propertius)
		text = tds.read_fragment('1.2')
		print(text)

	def test_sallust_reads_chapt1(self):
		print("")
		tds = TEIDataSource(sallust_cataline)
		text = tds.read_fragment('1')
		#print(text)

	def test_caesar_reads_chapt2_3_4(self):
		print("")
		tds = TEIDataSource(caesar_gallic)
		text = tds.read_fragment('2.3.4')
		#print(text)
	

	def test_sallust_doesnotread_chapt1000000(self):
		print("")
		tds = TEIDataSource(sallust_cataline)
		with self.assertRaises(Exception): # "No text part with ref: 1000000"):
			tds.read_fragment('1000000')

	def test_cicero_derepublica_metadata(self):
		print(cicero_derepublica)
		tds = TEIDataSource(cicero_derepublica)
		tds.read_doc_metadata()
		self.assertIsNotNone(tds.source_desc)
		#print(tds.source_desc)
		i = 0
		for s in tds.sections:
			i += 1
			#print(str(i) + "=" + s)
		self.assertEqual(i, 2)
		self.assertEqual(tds.delim, None)
		# print("delimiter=" + tds.delim)
	def test_cicero_reads_chapt2_2(self):
		print("")
		tds = TEIDataSource(cicero_derepublica)
		text = tds.read_fragment('2 2')
		self.assertIsNotNone(text)
		#print(text)

if __name__ == '__main__':
	unittest.main()
