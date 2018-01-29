# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task

import threading
from .task_providers import thumbnail, probe, bitrate

@shared_task
def add(data):
    try:
        task_id = int(data['id'])
        task_type = str(data['type'])
        task_media_file_path = str(data['media_file_path'])
    except:
        # TODO: error management
        pass

    # new job for the task
    if task_type == 'THUMBNAIL':
        task_provider = thumbnail.ThumbnailProvider(task_id, task_media_file_path)
    elif task_type == 'PROBE':
        task_provider = probe.ProbeProvider(task_id, task_media_file_path)
    elif task_type == 'BITRATE':
        task_provider = bitrate.BitrateProvider(task_id, task_media_file_path)
    else:
        # TODO: error management
        pass
    
    task_provider.execute()
