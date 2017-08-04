# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Media(models.Model):
    name = models.CharField(max_length=200, null=True)
    file_path = models.CharField(max_length=200)
    date_added = models.DateTimeField('added to library date', null=True)

    def __str__(self):              # __unicode__ on Python 2
        return self.name

    class Meta:
        ordering = ('name',)
    

class Assessment(models.Model):
    name = models.CharField(max_length=200, null=True)
    encoded_media_list = models.ManyToManyField(Media, related_name='encoded_media_list')
    reference_media = models.ForeignKey(Media, null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField('create assessment date', null=True)

    def __str__(self):              # __unicode__ on Python 2
        return self.name

    class Meta:
        ordering = ('name',)
