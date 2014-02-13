import unittest
import xml_file
 
sallust_cataline = "urn:cts:latinLit:phi0631.phi001.perseus-lat2"
homer_iliad = "urn:cts:greekLit:tlg0012.tlg001.perseus-grc1"
caesar_gallic = "urn:cts:latinLit:phi0448.phi001.perseus-lat1"
cicero_derepublica ="urn:cts:latinLit:phi0474.phi043.perseus-lat1"
junk_cts = "asjgk:sajgksa:asdgsag:.sagjksa"
urncts_junk_cts = "urn:cts:asdgsag:.sagjksa"
urnctslatinlit_junk_cts = "urn:cts:latinLit:phoo123.sagjksa"
does_not_exist_cts = "urn:cts:latinLit:phi9999.phi999.perseus-lat9"

class TestTEIDataSource(unittest.TestCase):
 
	def setUp(self):
		pass

	
	def test_sallust_load(self):
		print("\n======================\n%s" % sallust_cataline)
		# this is a test document URI
		tds = xml_file.TEIDataSource(sallust_cataline)
		self.assertNotEqual(tds.source_desc, None)
		i = 0
		for s in tds.sections:
			i += 1
			# print(str(i) + "=" + s)
		self.assertEqual(i, 1)
		self.assertEqual(tds.delim, None)
		# print("delimiter=" + tds.delim)
		

	def test_caesar_load(self):
		print("\n======================\n%s" % caesar_gallic)
		tds = xml_file.TEIDataSource(caesar_gallic)
		self.assertNotEqual(tds.source_desc, None)
		i = 0
		for s in tds.sections:
			i += 1
			# print(str(i) + "=" + s)
		self.assertEqual(i, 3)
		self.assertEqual(tds.delim, ".")
		# print("delimiter=" + tds.delim)
		print("got list of length " + str(len(tds.sectionslist)))
		llist = tds.sectionslist
		for e in llist:
			print(e['n'])
			if 'children' in e:
					self.recurse(e['children'], e['n'])
			print("\n")
		

	def recurse(self, alist, parent):
		if alist:
			for e in alist:
				#print("im doing it more " + str(e))
				print(parent + "." + e['n'])
				if 'children' in e:
					self.recurse(e['children'], parent + "." + e['n'])

	def test_cicero_load(self):
		print("\n======================\n%s" % cicero_derepublica)
		tds = xml_file.TEIDataSource(cicero_derepublica)
		self.assertIsNotNone(tds.source_desc)
		i = 0
		for s in tds.sections:
			i += 1
			#print(str(i) + "=" + s)
		self.assertEqual(i, 2)
		self.assertEqual(tds.delim, None)
		
		# print("delimiter=" + tds.delim)

	

if __name__ == '__main__':
	unittest.main()
