# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import os
import utils

import worker

class EncodingProvider(models.Model):
    name = models.CharField(max_length=200, null=False, default='unknown')


class Media(models.Model):
    name = models.CharField(max_length=200, null=True)
    file = models.FileField(null=True, upload_to=utils.get_upload_path)
    encoding_provider = models.ForeignKey(EncodingProvider, null=True, on_delete=models.SET_NULL)
    width = models.IntegerField(null=True)
    height = models.IntegerField(null=True)
    average_bitrate = models.CharField(max_length=50, null=True)
    video_codec = models.CharField(max_length=50, null=True)
    framerate = models.IntegerField(null=True)

    def __str__(self):              # __unicode__ on Python 2
        return self.name

    class Meta:
        ordering = ('name',)

    def extension(self):
        name, extension = os.path.splitext(self.file.name)
        return extension

    def probe(self):
        new_task = worker.models.Task()
        new_task.assessment = None
        new_task.media = Media.objects.get(id=self.id)
        new_task.metric = worker.models.Metric.objects.get(name='PROBE')
        new_task.save()

    def bitrate(self):
        new_task = worker.models.Task()
        new_task.assessment = None
        new_task.media = Media.objects.get(id=self.id)
        new_task.metric = worker.models.Metric.objects.get(name='BITRATE')
        new_task.save()

    def generate_thumbnail(self):
        new_task = worker.models.Task()
        new_task.assessment = None
        new_task.media = Media.objects.get(id=self.id)
        new_task.metric = worker.models.Metric.objects.get(name='THUMBNAIL')
        new_task.save()
    

class Assessment(models.Model):
    name = models.CharField(max_length=200, null=True)
    description = models.CharField(max_length=500, null=True)
    encoded_media_list = models.ManyToManyField(Media, related_name='encoded_media_list')
    reference_media = models.ForeignKey(Media, null=True, on_delete=models.SET_NULL)

    def __str__(self):              # __unicode__ on Python 2
        return self.name

    class Meta:
        ordering = ('name',)


class AppSettings(models.Model):
    media_library_path = models.CharField(max_length=200, null=True)
    max_parallel_tasks = models.IntegerField(default=1)
    worker_pulling_interval = models.IntegerField(default=10)
    auto_probe_media = models.BooleanField(default=True)
    auto_bitrate_analysis = models.BooleanField(default=True)
    auto_generate_thumbnail = models.BooleanField(default=True)
    