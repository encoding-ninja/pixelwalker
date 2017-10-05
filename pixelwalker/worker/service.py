# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils import timezone

import os
import time
import threading

# import db models
from engine.models import EncodingProvider, Media, Assessment, AppSettings
from worker.models import Metric, Task
from worker.provider import ffprobe, ffmpeg

# global variables
app_settings = AppSettings.objects.get(id=1)
current_tasks = []


def empty_slots():
    # Refersh settings
    app_settings = AppSettings.objects.get(id=1)
    return (app_settings.max_parallel_tasks - len(current_tasks))


def start():

    #Reset all tasks
    processing_tasks = Task.objects.filter(state=Task.PROCESSING)
    for task in processing_tasks:
        task.state = Task.QUEUED
        task.save()

    # Start interval pulling tasks
    while True:
        # Refersh settings
        app_settings = AppSettings.objects.get(id=1)

        # Wait
        time.sleep(app_settings.worker_pulling_interval)

        #Work
        print 'worker pulling'

        for task in current_tasks:
            if task.state == Task.ABORTED:
                current_tasks.remove(task)

        print "current tasks = " + str(len(current_tasks))
        print "empty slots = " + str(empty_slots())

        #Get new tasks
        task_list = []
        if empty_slots() > 0:
            task_list = get_queued_tasks(empty_slots())
            print "queued tasks retrieved = " + str(len(task_list))

        if len(task_list) > 0:
            for task in task_list:
                if empty_slots() > 0:
                    start_task(task)


def start_task(task):
    current_tasks.append(task)
    task.state = Task.PROCESSING
    task.date_started = timezone.now()
    task.save()

    if task.metric == Metric.objects.get(name='PROBE'):
        thr = threading.Thread(target=ffprobe.execute, args=(task, callback_task), kwargs={})
        thr.start()

    elif task.metric == Metric.objects.get(name='BITRATE'):
        thr = threading.Thread(target=ffprobe.frame_bitrate_analysis, args=(task, callback_task), kwargs={})
        thr.start()

    elif task.metric == Metric.objects.get(name='SSIM'):
        thr = threading.Thread(target=ffmpeg.process_ssim, args=(task, callback_task), kwargs={})
        thr.start()

    elif task.metric == Metric.objects.get(name='PSNR'):
        thr = threading.Thread(target=ffmpeg.process_psnr, args=(task, callback_task), kwargs={})
        thr.start()

    else:
        task.state = Task.ERROR
        task.save()
        current_tasks.remove(task)


def callback_task(task, error):

    if task.state == Task.ABORTED:
        task.state = Task.ABORTED
        current_tasks.remove(task)

    else:
        if error:
            task.state = Task.ERROR
            if task.output_data_path is not None:
                os.remove(task.output_data_path)
                task.output_data_path = None
            if task.chart_labels_path is not None:
                os.remove(task.chart_labels_path)
                task.chart_labels_path = None

        else:
            task.state = Task.SUCCESS
    
    task.date_ended = timezone.now()
    task.process_pid = None
    task.save()
    current_tasks.remove(task)


def get_queued_tasks(fetch_limit):
    return Task.objects.filter(state=Task.QUEUED).order_by('date_queued')[:fetch_limit]
