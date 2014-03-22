import json
from tastypie.utils.timezone import now
from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from decommentariis.xml_file import TEIDataSource
from decommentariis.signals import *


class TEIEntry(models.Model):
	cts_urn = models.CharField(max_length=200, primary_key=True)
	creation_date = models.DateTimeField(default=now)
	author = models.CharField(max_length=200, null=True, db_index=True)
	title = models.CharField(max_length=200, null=True, db_index=True)
	editor = models.CharField(max_length=200, null=True, db_index=True)
	publisher = models.CharField(max_length=200, null=True)
	pub_place = models.CharField(max_length=200, null=True)
	pub_date = models.CharField(max_length=30, null=True)
	bibliographic_entry = models.CharField(max_length=1024,null=True, db_index=True)
	metadata = models.TextField(null=True)

	def save(self, *args, **kwargs):
		return super(TEIEntry, self).save(*args, **kwargs)

	def __str__(self):
		fnone = lambda s: str(s) if s else "-"
		return "{0} :: {1} :: '{2}'".format(self.cts_urn, fnone(self.author), fnone(self.title))

	def sections(self):
		return self.teisection_set.all()

	def section_refs(self):
		tei = TEIDataSource(self.cts_urn)
		return tei.document_metastructure_flat #its a []

	def loadURN(self):
		tei = TEIDataSource(self.cts_urn)
		self.metadata = json.dumps(tei.document_metastructure, sort_keys=True, indent=2, separators=(',', ': '))
		self.author = tei.author
		self.title = tei.title
		self.editor = tei.editor
		self.publisher = tei.publisher
		self.pub_place = tei.pubPlace
		self.pub_date = tei.date
		self.bibliographic_entry = tei.print_bib_detail()
		return tei.document_metastructure_flat

	class Meta:
		ordering = ['cts_urn']

class TEISection(models.Model):
	cts_urn = models.CharField(max_length=244, primary_key=True)
	entry = models.ForeignKey(TEIEntry)
	section_ref = models.CharField(max_length=32)
	cts_sequence = models.IntegerField(editable=False)
	_tei = None

	def __str__(self):
		return "{0} :: {1}".format(self.entry.cts_urn, str(self.section_ref))

	def tei(self):
		if  self._tei:
			return self._tei
		else:
			self._tei = TEIDataSource(self.entry.cts_urn)
			return self._tei

	def readData(self):
		return self.tei().read_fragment(self.section_ref)

	def children(self):
		teiDS = self.tei()
		sections = teiDS.document_metastructure_flat
		level_count = len(self.section_ref.split(teiDS.delim))
		index = sections.index(self.section_ref)
		plusone = index+1
		last = len(sections)
		if plusone < last:
			_nextsect = sections[plusone]
			_nslevel_count = len(_nextsect.split(teiDS.delim))
			if level_count >= _nslevel_count:
				return []
			queries = []
			queries.append(Q(section_ref=_nextsect))
			while level_count < _nslevel_count and plusone < last-1:
				plusone += 1
				_nextsect = sections[plusone]
				_nslevel_count = len(_nextsect.split(teiDS.delim))
				if level_count < _nslevel_count:
					queries.append(Q(section_ref=_nextsect))
			query = Q()
			for q in queries:
				query |= q
			return list(TEISection.objects.filter(query, entry=self.entry))
		else:
			return []

	def siblings(self):
		teiDS = self.tei()
		sections = teiDS.document_metastructure_flat
		level_count = len(self.section_ref.split(teiDS.delim))
		index = sections.index(self.section_ref)
		plusone = index+1
		minusone = index-1
		last = len(sections)
		siblings = {}
		if minusone >= 0:
			_prevsect = sections[minusone]
			_pslevel_count = len(_prevsect.split(teiDS.delim))
			# if the above isn't the same number of sections,
			# i.e. so 1.1.1 to 1.1.2 and 1.1 to 1.2 etc
			while level_count != _pslevel_count and minusone >= 0:
				minusone = minusone - 1 # decrement
				_prevsect = sections[minusone]
				_pslevel_count = len(_prevsect.split(teiDS.delim))
			# either it's the first one or none
			if level_count == _pslevel_count and minusone >= 0: # if not there was never a match
				siblings['prev'] = TEISection.objects.get(section_ref=_prevsect, entry = self.entry)
		if plusone < last:
			_nextsect = sections[plusone]
			_nslevel_count = len(_nextsect.split(teiDS.delim))
			while level_count != _nslevel_count and plusone < last-1:
				plusone = plusone + 1 # increment
				_nextsect = sections[plusone]
				_nslevel_count = len(_nextsect.split(teiDS.delim))
			if level_count == _nslevel_count and plusone < last: # if not there was never a match
				siblings['next'] = TEISection.objects.get(section_ref=_nextsect, entry = self.entry)
		return siblings

	def parents(self):
		return self._parents(self.section_ref, self.tei())

	def _parents(self, section_ref, teiDS):
		sections = teiDS.document_metastructure_flat
		delim = teiDS.delim
		elements = section_ref.split(delim)
		elements_len = len(elements)
		if elements_len > 0:
			parentelement = ""
			queries = []
			i = 0
			for e in elements:
				if i==0:
					parentelement += e
				else:
					parentelement += delim + e
				i += 1
				queries.append(Q(section_ref=parentelement))
			query = Q()
			for q in queries:
				query |= q
			return list(TEISection.objects.filter(query, entry=self.entry))
		else:
			return []

	class Meta:
		unique_together = ('entry', 'section_ref')
		ordering = ['entry', 'cts_sequence']


class CommentaryEntry(models.Model):
	commentary = models.TextField(null=False)
	section = models.ForeignKey(TEISection)
	user = models.ForeignKey(User)
	creation_date = models.DateTimeField(default=now)
	votes = models.IntegerField(default=0)

	def __str__(self):
		return '{0} :: ({1}) >>> {2} :: {3} :: "{4}"'.format(self.section.entry, self.section.section_ref, self.user.username, self.creation_date, self.commentary)
	class Meta:
		ordering = ['-votes', 'creation_date']
	
class CommentaryEntryVoter(models.Model):
	entry = models.ForeignKey(CommentaryEntry)
	user = models.ForeignKey(User)
	vote_date = models.DateTimeField(default=now)
	class Meta:
		unique_together = ('entry', 'user')


