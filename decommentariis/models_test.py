import unittest, os, sys
##
# this python file is a script that imports all readable TEI data from the disk.
##
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "decommentariis.settings")
os.environ.setdefault("CTS_DATA_PATH", "/Users/smcphee/Development/sources/commentarius/data/canonical/CTS_XML_TEI/perseus/")
from decommentariis.models import TEIEntry, TEISection
from decommentariis.xml_file import TEIDataSource

caesar_gallic = "urn:cts:latinLit:phi0448.phi001.perseus-lat1"
sallust_cataline = "urn:cts:latinLit:phi0631.phi001.perseus-lat2"

class TestTEISection(unittest.TestCase):

	def test_load_section(self):
		section = caesar_gallic + ":1.1.1"
		teisection = TEISection.objects.get(cts_urn=section)
		self.assertIsNotNone(teisection)

	def test_load_section_parents111(self):
		section = caesar_gallic + ":1.1.1"
		teisection = TEISection.objects.get(cts_urn=section)
		parents = teisection.parents()
		self.assertIsNotNone(parents)
		for p in parents:
			self.assertIsNotNone(p)
			self.assertTrue(teisection.section_ref.startswith(p.section_ref))
			#print(str(p))
		self.assertEqual(3, len(parents)) ## includes self at end

	def test_load_section_parents123(self):
		section = caesar_gallic + ":1.2.3"
		teisection = TEISection.objects.get(cts_urn=section)
		parents = teisection.parents()
		self.assertIsNotNone(parents)
		for p in parents:
			self.assertIsNotNone(p)
			self.assertTrue(teisection.section_ref.startswith(p.section_ref))
			#print(str(p))
		self.assertEqual(3, len(parents))

	def test_load_section_parents321(self):
		section = caesar_gallic + ":3.2.1"
		teisection = TEISection.objects.get(cts_urn=section)
		parents = teisection.parents()
		self.assertIsNotNone(parents)
		for p in parents:
			self.assertIsNotNone(p)
			self.assertTrue(teisection.section_ref.startswith(p.section_ref))
			#print(str(p))
		self.assertEqual(3, len(parents))

	def test_load_section_parents57(self):
		section = caesar_gallic + ":5.7"
		teisection = TEISection.objects.get(cts_urn=section)
		parents = teisection.parents()
		self.assertIsNotNone(parents)
		for p in parents:
			self.assertIsNotNone(p)
			self.assertTrue(teisection.section_ref.startswith(p.section_ref))
			#print(str(p))
		self.assertEqual(2, len(parents))

	def test_load_section_sallustparents21(self):
		section = sallust_cataline + ":21"
		teisection = TEISection.objects.get(cts_urn=section)
		parents = teisection.parents()
		self.assertIsNotNone(parents)
		for p in parents:
			self.assertIsNotNone(p)
			self.assertEqual(teisection.section_ref, p.section_ref)
			self.assertEqual("21", p.section_ref)
			#print(str(p))
		self.assertEqual(1, len(parents))

	def test_load_section_siblings111(self):
		section = caesar_gallic + ":1.1.1"
		## the siblings are 1.1 and 1.1.2
		teisection = TEISection.objects.get(cts_urn=section)
		siblings = teisection.siblings()
		self.assertIsNotNone(siblings)
		nxt = siblings['next']
		self.assertIsNotNone(nxt)
		# print(str(nxt))
		self.assertEqual(1, len(siblings))

	def test_load_section_siblings1(self):
		section = caesar_gallic + ":1"
		## the siblings are 1.1
		teisection = TEISection.objects.get(cts_urn=section)
		siblings = teisection.siblings()
		self.assertIsNotNone(siblings)
		nxt = siblings['next']
		self.assertIsNotNone(nxt)
		# print(str(nxt))
		self.assertEqual(1, len(siblings))

	def test_load_section_siblings5(self):
		section = caesar_gallic + ":5"
		## the siblings are 1.1
		teisection = TEISection.objects.get(cts_urn=section)
		siblings = teisection.siblings()
		self.assertIsNotNone(siblings)
		prev = siblings['prev']
		self.assertIsNotNone(prev)
		# print(str(prev))
		nxt = siblings['next']
		self.assertIsNotNone(nxt)
		# print(str(nxt))
		self.assertEqual(2, len(siblings))

	def test_load_section_siblings5_liketolike(self):
		section = caesar_gallic + ":5"
		## the siblings are 1.1
		teisection = TEISection.objects.get(cts_urn=section)
		siblings = teisection.siblings()
		self.assertIsNotNone(siblings)
		prev = siblings['prev']
		self.assertIsNotNone(prev)
		self.assertEqual('4', prev.section_ref)
		nxt = siblings['next']
		self.assertIsNotNone(nxt)
		self.assertEqual('6', nxt.section_ref)
		self.assertEqual(2, len(siblings))

	def test_load_section_siblings51_liketolike(self):
		section = caesar_gallic + ":5.1"
		## the siblings are 1.1
		teisection = TEISection.objects.get(cts_urn=section)
		siblings = teisection.siblings()
		self.assertIsNotNone(siblings)
		prev = siblings['prev']
		self.assertIsNotNone(prev)
		self.assertEqual('4.38', prev.section_ref)
		nxt = siblings['next']
		self.assertIsNotNone(nxt)
		self.assertEqual('5.2', nxt.section_ref)
		self.assertEqual(2, len(siblings))

	def test_load_section_siblings511_liketolike(self):
		section = caesar_gallic + ":5.1.1"
		## the siblings are 1.1
		teisection = TEISection.objects.get(cts_urn=section)
		siblings = teisection.siblings()
		self.assertIsNotNone(siblings)
		prev = siblings['prev']
		self.assertIsNotNone(prev)
		self.assertEqual('4.38.5', prev.section_ref)
		nxt = siblings['next']
		self.assertIsNotNone(nxt)
		self.assertEqual('5.1.2', nxt.section_ref)
		self.assertEqual(2, len(siblings))

	def test_load_section_siblings111_liketolike(self):
		section = caesar_gallic + ":1.1.1"
		## the siblings are 1.1
		teisection = TEISection.objects.get(cts_urn=section)
		siblings = teisection.siblings()
		self.assertIsNotNone(siblings)
		nxt = siblings['next']
		self.assertIsNotNone(nxt)
		self.assertEqual('1.1.2', nxt.section_ref)
		self.assertEqual(1, len(siblings))

	def test_load_section_siblings_last8552(self):
		section = caesar_gallic + ":8.55.2" #last section of caesar bg
		## the siblings are 8.55.1
		teisection = TEISection.objects.get(cts_urn=section)
		siblings = teisection.siblings()
		self.assertIsNotNone(siblings)
		prev = siblings['prev']
		self.assertIsNotNone(prev)
		self.assertEqual('8.55.1', prev.section_ref)
		# print(str(prev))
		self.assertEqual(1, len(siblings))

	def test_load_section_siblings_last855(self):
		section = caesar_gallic + ":8.55" #last section of caesar bg
		## the siblings are 8.54
		teisection = TEISection.objects.get(cts_urn=section)
		siblings = teisection.siblings()
		self.assertIsNotNone(siblings)
		prev = siblings['prev']
		self.assertIsNotNone(prev)
		self.assertEqual('8.54', prev.section_ref)
		# print(str(prev))
		self.assertEqual(1, len(siblings))

	def test_load_section_siblings_last8(self):
		section = caesar_gallic + ":8" #last section of caesar bg
		teisection = TEISection.objects.get(cts_urn=section)
		siblings = teisection.siblings()
		self.assertIsNotNone(siblings)
		prev = siblings['prev']
		self.assertIsNotNone(prev)
		self.assertEqual('7', prev.section_ref)
		# print(str(prev))
		self.assertEqual(1, len(siblings))

	def test_load_section_siblings_first1(self):
		section = caesar_gallic + ":1" #last section of caesar bg
		teisection = TEISection.objects.get(cts_urn=section)
		siblings = teisection.siblings()
		self.assertIsNotNone(siblings)
		nxt = siblings['next']
		self.assertIsNotNone(nxt)
		self.assertEqual('2', nxt.section_ref)
		# print(str(prev))
		self.assertEqual(1, len(siblings))

	def test_load_section_siblings_first11(self):
		section = caesar_gallic + ":1.1" #last section of caesar bg
		teisection = TEISection.objects.get(cts_urn=section)
		siblings = teisection.siblings()
		self.assertIsNotNone(siblings)
		nxt = siblings['next']
		self.assertIsNotNone(nxt)
		self.assertEqual('1.2', nxt.section_ref)
		# print(str(prev))
		self.assertEqual(1, len(siblings))

if __name__ == '__main__':
	unittest.main()
