# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.utils import timezone
import os, json, json2table
from celery.execute import send_task

from . import utils


class AppSetting(models.Model):
    key = models.CharField(max_length=32, null=False, default='unnamed parameter')
    value = models.CharField(max_length=32, null=True)
    is_bool = models.BooleanField(default=False)
    description = models.CharField(max_length=280, null=True)
    

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
        new_task.submit()

    def get_file_url(self):
        return settings.MEDIA_URL+self.file.path.replace(settings.MEDIA_ROOT+'\\','').replace(settings.MEDIA_ROOT+'/','').replace('\\','/')

    def get_thumbnail_url(self):
        task = Task.objects.filter(media=self, type=TaskType.objects.get(name='GENERATE THUMBNAILS'), state=Task.SUCCESS).last()
        output = TaskOutput.objects.filter(task=task, type=TaskOutput.MEDIA).last()
        if output is not None:
            return output.get_url().replace("%05d","00001")
        else:
            return None
    
    def get_probe_html_table(self):
        task = Task.objects.filter(media=self, type=TaskType.objects.get(name='PROBE'), state=Task.SUCCESS).last()
        output = TaskOutput.objects.filter(task=task, type=TaskOutput.JSON).last()
        if output is not None:
            return json2table.convert(json.load(open(output.file_path)), build_direction="LEFT_TO_RIGHT", table_attributes={"class" : "table table-bordered table-hover table-condensed"})
        else:
            return None
    
    def get_frames_labels(self):
        task = Task.objects.filter(media=self, type=TaskType.objects.get(name='FRAMES ANALYSIS'), state=Task.SUCCESS).last()
        if task:
            return task.get_output_labels()
        else:
            return None

    def get_frames_PTS(self):
        task = Task.objects.filter(media=self, type=TaskType.objects.get(name='FRAMES ANALYSIS'), state=Task.SUCCESS).last()
        if task:
            return task.get_output_data_by_name('PTS Time')
        else:
            return '[]'
    
    def get_frames_I(self):
        task = Task.objects.filter(media=self, type=TaskType.objects.get(name='FRAMES ANALYSIS'), state=Task.SUCCESS).last()
        if task:
            return task.get_output_data_by_name('I Frames')
        else:
            return '[]'

    def get_frames_I_count(self):
        task = Task.objects.filter(media=self, type=TaskType.objects.get(name='FRAMES ANALYSIS'), state=Task.SUCCESS).last()
        if task:
            return int(task.get_output_average_by_name('I Frames'))
        else:
            return 0
    
    def get_frames_P(self):
        task = Task.objects.filter(media=self, type=TaskType.objects.get(name='FRAMES ANALYSIS'), state=Task.SUCCESS).last()
        if task:
            return task.get_output_data_by_name('P Frames')
        else:
            return '[]'

    def get_frames_P_count(self):
        task = Task.objects.filter(media=self, type=TaskType.objects.get(name='FRAMES ANALYSIS'), state=Task.SUCCESS).last()
        if task:
            return int(task.get_output_average_by_name('P Frames'))
        else:
            return 0

    def get_frames_B(self):
        task = Task.objects.filter(media=self, type=TaskType.objects.get(name='FRAMES ANALYSIS'), state=Task.SUCCESS).last()
        if task:
            return task.get_output_data_by_name('B Frames')
        else:
            return '[]'
    
    def get_frames_B_count(self):
        task = Task.objects.filter(media=self, type=TaskType.objects.get(name='FRAMES ANALYSIS'), state=Task.SUCCESS).last()
        if task:
            return int(task.get_output_average_by_name('B Frames'))
        else:
            return 0

    def get_definition(self):
        return str(self.width)+'x'+str(self.height)

    

class Assessment(models.Model):
    name = models.CharField(max_length=200, null=False, default='unnamed assessment')
    description = models.CharField(max_length=500, null=True)
    encoded_media_list = models.ManyToManyField(Media, related_name='encoded_media_list')
    reference_media = models.ForeignKey(Media, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)

    def get_definition_list(self):
        definition_list = []
        for media in self.encoded_media_list.all():
            if media.get_definition() not in definition_list:
                definition_list.append(media.get_definition())
        return definition_list

    def get_encoding_provider_list(self):
        encoding_provider_list = []
        for media in self.encoded_media_list.all():
            if media.encoding_provider not in encoding_provider_list:
                encoding_provider_list.append(media.encoding_provider)
        return encoding_provider_list

    def get_bitrate_list(self):
        bitrate_list = []
        for media in self.encoded_media_list.all().order_by('average_bitrate'):
            if media.average_bitrate not in bitrate_list:
                bitrate_list.append(media.average_bitrate)
        return bitrate_list
    
    def get_min_bitrate(self):
        return min(self.get_bitrate_list())
    
    def get_max_bitrate(self):
        return max(self.get_bitrate_list())

    def get_all_frames_labels(self):
        task = Task.objects.filter(assessment=self, state=Task.SUCCESS).last()
        if task:
            return task.get_output_labels()
        else:
            return '[]'
        




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

    def submit(self):
        self.date_queued = timezone.now()
        self.state = Task.QUEUED
        self.save()

        # Prepare to send task to available worker
        data = {}
        data['id'] = self.id
        data['media_file_path'] = self.media.file.path
        if self.media.framerate:
            data['media_framerate'] = self.media.framerate
        if self.assessment:
            data['reference_file_path'] = self.assessment.reference_media.file.path
            data['reference_width'] = self.assessment.reference_media.width
            data['reference_height'] = self.assessment.reference_media.height
        data['type'] = self.type.name
        send_task('worker.tasks.add', args=[data])
    
    def get_average_score(self):
        output = TaskOutput.objects.filter(task=self, type=TaskOutput.CHART_DATA).last()
        return output.average
    
    def get_output_labels(self):
        output = TaskOutput.objects.filter(task=self, type=TaskOutput.CHART_LABELS).last()
        if output:
            labels = json.load(open(output.file_path))
            return json.dumps(labels)
        else:
            return '[]'

    def get_output_data(self):
        output = TaskOutput.objects.filter(task=self, type=TaskOutput.CHART_DATA).last()
        if output:
            data = json.load(open(output.file_path))
            return json.dumps(data)
        else:
            return '[]'

    def get_output_data_by_name(self, ouput_name):
        output = TaskOutput.objects.filter(task=self, type=TaskOutput.CHART_DATA, name=ouput_name).last()
        if output:
            data = json.load(open(output.file_path))
            return json.dumps(data)
        else:
            return '[]'
    
    def get_output_average_by_name(self, ouput_name):
        output = TaskOutput.objects.filter(task=self, type=TaskOutput.CHART_DATA, name=ouput_name).last()
        if output:
            return output.average
        else:
            return 0


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
