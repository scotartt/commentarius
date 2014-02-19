import json
from tastypie.utils.timezone import now
from django.db import models
from decommentariis.xml_file import TEIDataSource

class TEIEntry(models.Model):
	cts_urn = models.CharField(max_length=200, primary_key=True)
	creation_date = models.DateTimeField(default=now)
	author = models.CharField(max_length=200, null=True, db_index=True)
	title = models.CharField(max_length=200, null=True, db_index=True)
	editor = models.CharField(max_length=200, null=True, db_index=True)
	publisher = models.CharField(max_length=200, null=True)
	pubPlace = models.CharField(max_length=200, null=True)
	pubDate = models.CharField(max_length=30, null=True)
	bibliographic_entry = models.CharField(max_length=1024,null=True, db_index=True)
	metadata = models.TextField(null=True)

	def save(self, *args, **kwargs):
		return super(TEIEntry, self).save(*args, **kwargs)

	def __str__(self):
		fnone = lambda s: str(s) if s else "-"
		return "{0} :: {1}, '{2}'".format(self.cts_urn, fnone(self.author), fnone(self.title))

	def readURN(self):
		tei = TEIDataSource(self.cts_urn)
		self.metadata = json.dumps(tei.document_metastructure, sort_keys=True, indent=2, separators=(',', ': '))
		self.author = tei.author
		self.title = tei.title
		self.editor = tei.editor
		self.publisher = tei.publisher
		self.pubPlace = tei.pubPlace
		self.pubDate = tei.date
		self.bibliographic_entry = tei.print_bib_detail()

	def readData(self, ref):
		tei = TEIDataSource(self.cts_urn)
		return tei.read_fragment(ref)
