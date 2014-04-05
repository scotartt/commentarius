#!/usr/bin/env python
import os, sys, argparse
##
# this python file is a script that imports all readable TEI data from the disk.
##
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "decommentariis.settings")
os.environ.setdefault("CTS_DATA_PATH", "/Users/smcphee/Development/sources/commentarius/data/canonical/CTS_XML_TEI/perseus/")
from decommentariis.models import TEIEntry, TEISection
from decommentariis.xml_file import TEIDataSource
# print(TEIEntry.objects.all())
path = os.environ.get("CTS_DATA_PATH")
parser = argparse.ArgumentParser(description='Parse and import TEI XML document metadata into De Commentariis database')
parser.add_argument('-u','--update', default='no', choices=('yes', 'no'), help='Update existing documents, update=yes. Import only new documents, update=no. Default is "no"', required=False)
parser.add_argument('-c','--cts-urn', nargs='+', help='Import only the document that has the supplied CTS URN. (not working currently)', required=False)
args = vars(parser.parse_args())

is_update = (args['update'] == 'yes')
if is_update :
	print("Importing ALL PARSED TEI XML metadata.")
else :
	print("Only importing TEI XML metadata not already in the database.")


## functions for the script.
def open_source(path, filename):
	return open(path + filename, 'r')

def save_sections(section_numbers, entry):
	if section_numbers and (len(section_numbers)):
		i = 10
		for section in section_numbers:
			teiSection = None
			urn = '{0}:{1}'.format(entry.cts_urn, section)

			if TEISection.objects.filter(cts_urn = urn).exists():
				teiSection = TEISection.objects.get(cts_urn = urn)
				print('\t\tExisting Section {0}'.format(urn))
			else:
				teiSection = TEISection()
				teiSection.cts_urn = urn
				print('\t\tNew Section {0}'.format(urn))

			teiSection.entry = entry
			teiSection.section_ref = section
			teiSection.cts_sequence = i
			teiSection.save()
			i += 10
	else :
		# no section numbers, delete entry, it's pointless.
		print('\tNO SECTIONS PARSED, DELETING: {0}'.format(entry.cts_urn))
		entry.delete()

def savedb(urn):
	it_exists = TEIEntry.objects.filter(cts_urn = urn).exists()
	if is_update and it_exists:
		entry = TEIEntry.objects.get(cts_urn=urn)
		section_numbers = entry.loadURN()
		print('UPDATE {0}\n\t{1}'.format(urn, entry.bibliographic_entry))
		entry.save()
		save_sections(section_numbers, entry)
	elif it_exists :
		print('SKIP EXISTING {0}'.format(urn))	
	else :
		entry = TEIEntry(urn)
		section_numbers = entry.loadURN()
		print('NEW {0}\n\t{1}'.format(urn, entry.bibliographic_entry))
		entry.save()
		save_sections(section_numbers, entry)

def readdatafromline(line, prefix):
	line = line.rstrip().rstrip('.xml')
	pathcomponents = line.split('/')
	if len(pathcomponents):
		urn = prefix + pathcomponents[len(pathcomponents)-1]
		try:
			savedb(urn)
		except Exception as ex:
			print("!!!UNPARSED XML: {0} has unparseable data: {1}".format(urn, ex))

## the script
# first, the latins
latinFile = open_source(path, "latinLit.txt")
for line in latinFile.readlines():
	readdatafromline(line, 'urn:cts:latinLit:')

# then, the greeks
greekFile = open_source(path, "greekLit.txt")
for line in greekFile.readlines():
	readdatafromline(line, 'urn:cts:greekLit:')
