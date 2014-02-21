#!/usr/bin/env python
import os, 	sys
##
# this python file is a script that imports all readable TEI data from the disk.
##
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "decommentariis.settings")
os.environ.setdefault("CTS_DATA_PATH", "/Users/smcphee/Development/sources/commentarius/data/canonical/CTS_XML_TEI/perseus/")
from decommentariis.models import TEIEntry, TEISection
from decommentariis.xml_file import TEIDataSource
print(TEIEntry.objects.all())
path = os.environ.get("CTS_DATA_PATH")

## functions for the script.
def open_source(path, filename):
	return open(path + filename, 'r')

def save_sections(section_numbers, entry):
	if section_numbers and (len(section_numbers)):
		for section in section_numbers:
			#if not entry.teisection_set.filter(section_ref=section).exists():
			teiSection = TEISection()
			teiSection.entry = entry
			teiSection.section_ref = section
			print('\t\tSection {0} in {1}'.format(teiSection.section_ref, entry.cts_urn))
			teiSection.save()

def savedb(urn):
	#if not TEIEntry.objects.filter(urn).exists():
	entry = TEIEntry(urn)
	section_numbers = entry.loadURN()
	print('NEW {0}\n\t{1}'.format(urn, entry.bibliographic_entry))
	entry.save()
	save_sections(section_numbers, entry)
	# else:
	# 	entry = TEIEntry.objects.get(urn)
	# 	section_numbers = entry.loadURN()
	# 	print('UPDATE {0}\n\t{1}'.format(urn, entry.bibliographic_entry))
	# 	entry.save(section_numbers, entry)


def readdatafromline(line, prefix):
	line = line.rstrip().rstrip('.xml')
	pathcomponents = line.split('/')
	if len(pathcomponents):
		urn = prefix + pathcomponents[len(pathcomponents)-1]
		try:
			savedb(urn)
		except Exception as ex:
			print("\n!!! {0} has unparseable data: {1}".format(urn, ex))

## the script
latinFile = open_source(path, "latinLit.txt")
for line in latinFile.readlines():
	readdatafromline(line, 'urn:cts:latinLit:')




