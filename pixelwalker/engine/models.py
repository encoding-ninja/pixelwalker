# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
import os, json, json2table

from . import utils


class AppSettings(models.Model):
    media_library_path = models.CharField(max_length=200, null=True)
    max_parallel_tasks = models.IntegerField(default=1, null=False)
    worker_pulling_interval = models.IntegerField(default=10, null=False)
    

class EncodingProvider(models.Model):
    name = models.CharField(max_length=200, null=False, default='unnamed encoding provider')

    def get_number_of_media(self):
        media_list = Media.objects.filter(encoding_provider=self)
        return len(media_list)

    def get_some_media_preview(self):
        media_list = Media.objects.filter(encoding_provider=self).order_by('-id')[:5]
        return media_list


class Media(models.Model):
    name = models.CharField(max_length=200, null=False, default='unnamed media')
    file = models.FileField(null=True, upload_to=utils.get_upload_path)
    encoding_provider = models.ForeignKey(EncodingProvider, null=True, on_delete=models.SET_NULL)
    width = models.IntegerField(null=True)
    height = models.IntegerField(null=True)
    average_bitrate = models.CharField(max_length=50, null=True)
    video_codec = models.CharField(max_length=50, null=True)
    framerate = models.IntegerField(null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)

    def extension(self):
        name, extension = os.path.splitext(self.file.name)
        return extension

    def auto_submit_task(self, type_name):
        new_task = Task()
        new_task.assessment = None
        new_task.media = Media.objects.get(id=self.id)
        new_task.type = TaskType.objects.get(name=type_name)
        new_task.save()

    def get_thumbnail_url(self):
        task = Task.objects.filter(media=self, type=TaskType.objects.get(name='THUMBNAIL')).last()
        output = TaskOutput.objects.filter(task=task, type=TaskOutput.MEDIA).last()
        if output is not None:
            return output.get_url()
        else:
            return None
    
    def get_probe_html_table(self):
        task = Task.objects.filter(media=self, type=TaskType.objects.get(name='PROBE')).last()
        output = TaskOutput.objects.filter(task=task, type=TaskOutput.JSON).last()
        if output is not None:
            return json2table.convert(json.load(open(output.file_path)), build_direction="LEFT_TO_RIGHT", table_attributes={"class" : "table table-bordered table-hover table-condensed"})
        else:
            return None
    
    def get_bitrate_json(self):
        task = Task.objects.filter(media=self, type=TaskType.objects.get(name='BITRATE')).last()
        output = TaskOutput.objects.filter(task=task, type=TaskOutput.CHART_DATA).last()
        if output is not None:
            with open(output.file_path) as f:
                bitrate_chart_data = f.readlines()[0]
            return bitrate_chart_data
        else:
            return None

    

class Assessment(models.Model):
    name = models.CharField(max_length=200, null=False, default='unnamed assessment')
    description = models.CharField(max_length=500, null=True)
    encoded_media_list = models.ManyToManyField(Media, related_name='encoded_media_list')
    reference_media = models.ForeignKey(Media, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)



class TaskType(models.Model):
    name = models.CharField(max_length=200, null=False, default='unnamed task type')
    is_video_metric = models.BooleanField(default=False)
    auto_submit_on_new_media = models.BooleanField(default=False)


class Task(models.Model):
    media = models.ForeignKey(Media, null=False, on_delete=models.CASCADE)
    assessment = models.ForeignKey(Assessment, null=True, on_delete=models.CASCADE)
    type = models.ForeignKey(TaskType, null=False, on_delete=models.CASCADE)

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
    state = models.IntegerField(default=QUEUED, choices=STATE_CHOICES)
    progress = models.IntegerField(null=True)
        
    date_created = models.DateTimeField('date created', null=False, auto_now_add=True)
    date_queued = models.DateTimeField('date queued', null=True)
    date_started = models.DateTimeField('date started', null=True)
    date_ended = models.DateTimeField('date ended', null=True)


class TaskOutput(models.Model):
    task = models.ForeignKey(Task, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    file_path = models.CharField(max_length=200, null=True)
    average = models.FloatField(null=True)

    CHART_DATA = 0
    CHART_LABELS = 1
    JSON = 2
    PLAIN = 3
    MEDIA = 4
    OUTPUT_TYPES = (
        (CHART_DATA, 'ChartData'),
        (CHART_LABELS, 'ChartLabels'),
        (JSON, 'Json'),
        (PLAIN, 'Plain'),
        (MEDIA, 'Media'),
    )
    type = models.IntegerField(default=PLAIN, choices=OUTPUT_TYPES)

    def get_url(self):
        return settings.MEDIA_URL+self.file_path.replace(settings.MEDIA_ROOT+'\\','').replace(settings.MEDIA_ROOT+'/','').replace('\\','/')
