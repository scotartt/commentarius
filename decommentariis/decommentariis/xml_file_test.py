import unittest
import xml_file
 
sallust_cataline = "urn:cts:latinLit:phi0631.phi001.perseus-lat2"
homer_iliad = "urn:cts:greekLit:tlg0012.tlg001.perseus-grc1"
caesar_gallic = "urn:cts:latinLit:phi0448.phi001.perseus-lat1"

class TestTEIDataSource(unittest.TestCase):
 
	def setUp(self):
		pass


	def test_sallust_loads(self):
		print("")
		# this is a test document URI
		tds = xml_file.TEIDataSource(sallust_cataline)
		fo = tds.open_source()
		# print("Name of the file: ", fo.name)
		# print("Closed or not : ", fo.closed)
		# print("Opening mode : ", fo.mode)
		tds.close_source(fo)

	def test_homer_loads(self):
		print("")
		# this is a test document URI
		tds = xml_file.TEIDataSource(homer_iliad)
		fo = tds.open_source()
		# print("Name of the file: ", fo.name)
		# print("Closed or not : ", fo.closed)
		# print("Opening mode : ", fo.mode)
		tds.close_source(fo)

	def test_sallust_reads_chapt1(self):
		print("")
		tds = xml_file.TEIDataSource(sallust_cataline)
		text = tds.read_fragment('1')
		#print(text)

	def test_caesar_reads_chapt2_3_4(self):
		print("")
		tds = xml_file.TEIDataSource(caesar_gallic)
		text = tds.read_fragment('2.3.4')
		#print(text)
	

	def test_sallust_doesnotread_chapt1000000(self):
		print("")
		tds = xml_file.TEIDataSource(sallust_cataline)
		fo = tds.open_source()
		text = tds.read_fragment('1000000')
		tds.close_source()
		print(text)


	def test_sallust_reads_metadata(self):
		print("")
		tds = xml_file.TEIDataSource(sallust_cataline)
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
		tds = xml_file.TEIDataSource(caesar_gallic)
		tds.read_doc_metadata()
		self.assertNotEqual(tds.source_desc, None)
		print(tds.source_desc)
		i = 0
		for s in tds.sections:
			i += 1
			# print(str(i) + "=" + s)
		self.assertEqual(i, 3)
		self.assertEqual(tds.delim, ".")
		# print("delimiter=" + tds.delim)
 

if __name__ == '__main__':
	unittest.main()
