#!/usr/bin/env python
import os, sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "decommentariis.settings")
os.environ.setdefault("CTS_DATA_PATH", "/Users/smcphee/Development/sources/commentarius/data/canonical/CTS_XML_TEI/perseus/")
from decommentariis.models import TEIEntry
from decommentariis.xml_file import TEIDataSource
print(TEIEntry.objects.all())
path = os.environ.get("CTS_DATA_PATH")

def open_source(path, filename):
	return open(path + filename, 'r')
def readdatafromline(line, prefix):
	line = line.rstrip().rstrip('.xml')
	pathcomponents = line.split('/')
	if len(pathcomponents):
		urn = prefix + pathcomponents[len(pathcomponents)-1]
		try:
			entry = TEIEntry(urn)
			entry.readURN()
			print(urn + "\n\t" + entry.bibliographic_entry)
			entry.save()
		except Exception as ex:
			print("\n!!! {0} has unparseable data: {1}".format(urn, ex))

latinFile = open_source(path, "latinLit.txt")
for line in latinFile.readlines():
	readdatafromline(line, 'urn:cts:latinLit:')




