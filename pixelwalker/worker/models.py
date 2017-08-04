# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import engine.models


class Metric(models.Model):
    name = models.CharField(max_length=200, null=True)


class Provider(models.Model):
    name = models.CharField(max_length=200, null=True)
    available_metrics = models.ManyToManyField(Metric)


class Task(models.Model):
    media = models.ForeignKey(engine.models.Media, null=True, on_delete=models.CASCADE)
    assessment = models.ForeignKey(engine.models.Assessment, null=True, on_delete=models.CASCADE)
    provider = models.ForeignKey(Provider, null=True, on_delete=models.CASCADE)
    metric = models.ForeignKey(Metric, null=True, on_delete=models.CASCADE)
    state = models.CharField(max_length=30, null=True)
    progress = models.IntegerField(null=True)
    date_queued = models.DateTimeField('date queued', null=True)
    date_started = models.DateTimeField('date started', null=True)
    date_last_update = models.DateTimeField('date last update', null=True)
    date_complete = models.DateTimeField('date completed', null=True)


class Result(models.Model):
    media = models.ForeignKey(engine.models.Media, null=True, on_delete=models.CASCADE)
    encoding_provider = models.ForeignKey(engine.models.EncodingProvider, null=True, on_delete=models.SET_NULL)
    assessment = models.ForeignKey(engine.models.Assessment, null=True, on_delete=models.CASCADE)
    metric = models.ForeignKey(Metric, null=True, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, null=True, on_delete=models.SET_NULL)
    data_json_path = models.CharField(max_length=200, null=True)
    average_score = models.IntegerField(null=True)
    date = models.DateTimeField('data insert date', null=True)