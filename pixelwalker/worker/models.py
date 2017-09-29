# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import engine.models


class Metric(models.Model):
    name = models.CharField(max_length=200, null=True)
    hidden = models.BooleanField(default=False)


class Task(models.Model):
    QUEUED = 0
    PROCESSING = 1
    SUCCESS = 2
    ERROR = 3
    ABORTED = 4
    STATE_CHOICES = (
        (QUEUED, 'Queued'),
        (PROCESSING, 'Processing'),
        (SUCCESS, 'Success'),
        (ERROR, 'Error'),
        (ABORTED, 'Aborted'),
    )
    media = models.ForeignKey(engine.models.Media, null=True, on_delete=models.CASCADE)
    assessment = models.ForeignKey(engine.models.Assessment, null=True, on_delete=models.CASCADE)
    metric = models.ForeignKey(Metric, null=True, on_delete=models.CASCADE)
    state = models.IntegerField(default=QUEUED, choices=STATE_CHOICES)
    progress = models.IntegerField(null=True)
    message = models.CharField(max_length=200, null=True)
    output_data_path = models.CharField(max_length=200, null=True)
    average_score = models.FloatField(null=True)
