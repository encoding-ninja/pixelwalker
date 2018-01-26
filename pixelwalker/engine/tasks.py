# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.shortcuts import get_object_or_404
from django.utils import timezone

from .models import Task, TaskOutput, TaskType
import json

@shared_task
def acknowledge(data):
    # Parse json body
    try:
        task_id = int(data['id'])
        task_state = str(data['state'])
    except:
        # TODO: error managment
        pass

    task = get_object_or_404(Task, pk=task_id)
    if task.state is not Task.ABORTED:
        if task_state == 'SUCCESS':
            task.state = Task.SUCCESS
            task.date_ended = timezone.now()

        elif task_state == 'ERROR':
            task.state = Task.ERROR
            task.date_ended = timezone.now()

        elif task_state == 'PROCESSING':
            task.state = Task.PROCESSING
            task.date_started = timezone.now()

        elif task_state == 'QUEUED':
            task.state = Task.QUEUED
            task.date_queued = timezone.now()

        else:
            # TODO: error managment
            pass

        if data['outputs'] is not None:
            # Remove previous ouputs of this task
            TaskOutput.objects.filter(task=task).delete()

            # For every new output
            for output in data['outputs']:
                new_output = TaskOutput()
                new_output.task = task
                new_output.name = output['name']
                new_output.file_path = output['file_path']
                new_output.average = output['average']

                if output['type'] == 'ChartData':
                    new_output.type = TaskOutput.CHART_DATA
                elif output['type'] == 'ChartLabels':
                    new_output.type = TaskOutput.CHART_LABELS
                elif output['type'] == 'JSON':
                    new_output.type = TaskOutput.JSON
                elif output['type'] == 'PLAIN':
                    new_output.type = TaskOutput.PLAIN
                elif output['type'] == 'MEDIA':
                    new_output.type = TaskOutput.MEDIA
                else:
                    new_output.type = TaskOutput.PLAIN

                new_output.save()

                # Specific to the probe ouput, get some info back to the media object
                if new_output.name == 'Probe':
                    probe = json.load(open(new_output.file_path))
                    for stream in probe['streams']:
                        if stream['codec_type'] == 'video':
                            task.media.width = int(stream['width'])
                            task.media.height = int(stream['height'])
                            task.media.average_bitrate = probe['format']['bit_rate']
                            task.media.video_codec = stream['codec_name']
                            task.media.framerate = int(stream['r_frame_rate'].replace('/1',''))
                    task.media.save()

    task.save()
    return task.state