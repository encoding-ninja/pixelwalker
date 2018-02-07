# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task

import threading
from .task_providers import thumbnail, probe, frame, ssim, psnr

@shared_task
def add(data):
    try:
        task_id = int(data['id'])
        task_type = str(data['type'])
        task_media_file_path = str(data['media_file_path'])
        task_media_framerate = int(data.get('media_framerate', 0))
        task_reference_file_path = str(data.get('reference_file_path', 'unknown'))
        task_reference_width = int(data.get('reference_width', 0))
        task_reference_height = int(data.get('reference_height', 0))
    except:
        # TODO: error management
        pass

    # new job for the task
    if task_type == 'GENERATE THUMBNAILS':
        task_provider = thumbnail.ThumbnailProvider(task_id, task_media_file_path)
    elif task_type == 'PROBE':
        task_provider = probe.ProbeProvider(task_id, task_media_file_path)
    elif task_type == 'FRAMES ANALYSIS':
        task_provider = frame.FrameProvider(task_id, task_media_file_path)
    elif task_type == 'SSIM':
        task_provider = ssim.SsimProvider(task_id, task_media_file_path, task_media_framerate, 
                                          task_reference_file_path, task_reference_width, task_reference_height)
    elif task_type == 'PSNR':
        task_provider = psnr.PsnrProvider(task_id, task_media_file_path, task_media_framerate, 
                                          task_reference_file_path, task_reference_width, task_reference_height)
    else:
        # TODO: error management
        pass
    
    task_provider.execute()
