from tastypie.utils.timezone import now
from django.db import models

class TEIEntry(models.Model):
    cts_urn = models.CharField(max_length=200, primary_key=True)
    creation_date = models.DateTimeField(default=now)
    author = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    metadata = models.TextField();

    def save(self, *args, **kwargs):
        return super(Entry, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.cts_urn
