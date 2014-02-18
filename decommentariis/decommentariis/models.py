import json
from tastypie.utils.timezone import now
from django.db import models
from decommentariis.xml_file import TEIDataSource

class TEIEntry(models.Model):
	cts_urn = models.CharField(max_length=200, primary_key=True)
	creation_date = models.DateTimeField(default=now)
	author = models.CharField(max_length=200)
	title = models.CharField(max_length=200)
	editor = models.CharField(max_length=200)
	publisher = models.CharField(max_length=200)
	pubPlace = models.CharField(max_length=200)
	pubDate = models.CharField(max_length=30)
	metadata = models.TextField()

	def save(self, *args, **kwargs):
		return super(TEIEntry, self).save(*args, **kwargs)

	def __str__(self):
		return self.cts_urn

	def readURN(self):
		tei = TEIDataSource(self.cts_urn)
		self.metadata = json.dumps(tei.document_metastructure, sort_keys=True, indent=2, separators=(',', ': '))
		self.author = tei.author
		self.title = tei.title
		self.editor = tei.editor
		self.publisher = tei.publisher
		self.pubPlace = tei.pubPlace
		self.pubDate = tei.date

	def readData(self, ref):
		tei = TEIDataSource(self.cts_urn)
		return tei.read_fragment(ref)
