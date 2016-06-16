from __future__ import unicode_literals
from django.db import models


class URL(models.Model):
    url = models.CharField(max_length=50)

    def __unicode__(self):
        return self.url


class Keyword(models.Model):
    keyword = models.CharField(max_length=50)
    urls = models.ManyToManyField(URL)

    def __unicode__(self):
        return self.keyword







