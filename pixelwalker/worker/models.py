# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

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
    chart_labels_path = models.CharField(max_length=200, null=True)
    average_score = models.FloatField(null=True)
    date_created = models.DateTimeField('date created', null=True, auto_now_add=True)
    date_queued = models.DateTimeField('date queued', null=True)
    date_started = models.DateTimeField('date started', null=True)
    date_ended = models.DateTimeField('date ended', null=True)

    def save_chart_dataset(self, dataset):
        task = self

        # string manipulations
        dataset = str(dataset)
        dataset = dataset.replace("u'","'")
        dataset = dataset.replace('\n','').replace('\r','')
        dataset = dataset.replace("'{borderColor}'", "getcolor("+str(task.id)+")")
        dataset = dataset.replace("'{backgroundColor}'", "getcolor("+str(task.id)+")")
        dataset = dataset.replace("'{true}'", "true")
        dataset = dataset.replace("'{false}'", "false")
        dataset = dataset.replace("'{pointRadius}'", "0")
        dataset = dataset.replace("'{pointHoverRadius}'", "4")

        # save to file
        if task.assessment:
            task.output_data_path = os.path.join(os.path.dirname(task.media.file.path), task.media.name+"_"+task.assessment.name+"_"+task.metric.name+".json")
        else:
            task.output_data_path = os.path.join(os.path.dirname(task.media.file.path), task.media.name+"_"+task.metric.name+".json")
        with open(task.output_data_path, "w") as f:
            f.write(dataset)

        task.save()

    def save_chart_labels(self, labels):
        task = self

        # save to file
        if task.assessment:
            task.chart_labels_path = os.path.join(os.path.dirname(task.media.file.path), task.media.name+"_"+task.assessment.name+"_"+task.metric.name+"_labels.json")
        else:
            task.chart_labels_path = os.path.join(os.path.dirname(task.media.file.path), task.media.name+"_"+task.metric.name+"_labels.json")
        with open(task.chart_labels_path, "w") as f:
            f.write(str(labels))

        task.save()
