# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import time
import threading

# import db models
from engine.models import EncodingProvider, Media, Assessment
from worker.models import Metric, Task
from worker.provider import ffprobe, ffmpeg


MAX_TASK = 1
current_tasks = []


def empty_slots():
	return (MAX_TASK - len(current_tasks))


def start():

	#Reset all tasks
	processing_tasks = Task.objects.filter(state=Task.PROCESSING)
	for task in processing_tasks:
		task.state = Task.QUEUED
		task.save()

	# Start interval pulling tasks
	while True:
		time.sleep(10)
		print 'worker pulling'
		print "current tasks = " + str(len(current_tasks))
		print "empty slots = " + str(empty_slots())

		#Get new tasks
		task_list = get_queued_tasks(empty_slots())
		print "queued tasks retrieved = " + str(len(task_list))

		if len(task_list) > 0:
			for task in task_list:
				if empty_slots() > 0:
					start_task(task)


def start_task(task):
	current_tasks.append(task)
	task.state = Task.PROCESSING
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


def callback_task(task, error, output_data):
	if error:
		task.state = Task.ERROR

	else:
		task.output_data_path = os.path.join(os.path.dirname(task.media.file.path), task.media.name+"_"+task.metric.name+".json")
		with open(task.output_data_path, "w") as json_file:
			json_file.write(output_data.replace('\n','').replace('\r',''))
	
		task.state = Task.SUCCESS
	
	task.save()
	current_tasks.remove(task)


def get_queued_tasks(fetch_limit):
	return Task.objects.filter(state=Task.QUEUED).order_by('id')[:fetch_limit]
