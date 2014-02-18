#!/usr/bin/env python
import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "decommentariis.settings")
os.environ.setdefault("CTS_DATA_PATH", "/Users/smcphee/Development/sources/commentarius/data/canonical/CTS_XML_TEI/perseus/")
from decommentariis.models import TEIEntry
from decommentariis.xml_file import TEIDataSource

def open_source(path, filename):
	return open(path + filename, 'r')

print(TEIEntry.objects.all())
path = os.environ.get("CTS_DATA_PATH")


latinFile = open_source(path, "latinLit.txt")

for line in latinFile.readlines():
	line = line.rstrip().rstrip('.xml')
	pathcomponents = line.split('/')
	if len(pathcomponents):
		urn = 'urn:cts:latinLit:' + pathcomponents[len(pathcomponents)-1]
		try:
			tei = TEIDataSource(urn)
			print(urn + "\n\t" + tei.print_bib_detail())
		except Exception:
			print("\n!!! " + urn + " has unparseable data\n")



