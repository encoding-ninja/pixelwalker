# -*- coding: utf-8 -*-

import subprocess
import sys
import os
import json
import datetime

FFMPEG_PATH = os.path.join(os.path.abspath(sys.path[0]), 'worker', 'provider', 'dependencies', 'ffmpeg.exe')

def process_ssim(task, callback_task) :
    error = False
    command = [FFMPEG_PATH,
                '-hide_banner',
                '-i', task.media.file.path,
                '-i', task.assessment.reference_media.file.path,
                '-lavfi', '[0]scale='+str(task.assessment.reference_media.width)+':'+str(task.assessment.reference_media.height)+'[scaled];[scaled][1]ssim=stats_file=-',
                '-f', 'null', '-']

    p = subprocess.Popen(command, stderr=subprocess.PIPE, stdout=subprocess.PIPE, universal_newlines=True)
    task.process_pid = p.pid
    task.save()

    out, err = p.communicate()
    task.message = err
    task.save()

    if p.returncode > 0:
        error = True

    try:
        chart_labels = []

        dataset = {}
        dataset['label'] = task.media.name
        dataset['backgroundColor'] = '{backgroundColor}'
        dataset['borderColor'] = '{borderColor}'
        dataset['fill'] = '{false}'
        dataset['pointRadius'] = '{pointRadius}'
        dataset['pointHoverRadius'] = '{pointHoverRadius}'
        dataset['data'] = []

        raw_data = out.splitlines()
        sum_data = 0
        nb_data = 1
        for line in raw_data:
            chart_labels.append(str(datetime.timedelta(seconds=(nb_data/task.media.framerate))))
            value = float(line[line.find('All:')+4:line.find('(')].strip())
            dataset['data'].append(value)
            sum_data += value
            nb_data+=1

        task.average_score = sum_data / nb_data
        task.save()

        task.save_chart_dataset(dataset)
        task.save_chart_labels(chart_labels)

    except:
        error = True

    if error is True:
        task.message = err
        task.save()

    callback_task(task, error)


def process_psnr(task, callback_task) :
    error = False
    command = [FFMPEG_PATH,
                '-hide_banner',
                '-i', task.media.file.path,
                '-i', task.assessment.reference_media.file.path,
                '-lavfi', '[0]scale='+str(task.assessment.reference_media.width)+':'+str(task.assessment.reference_media.height)+'[scaled];[scaled][1]psnr=stats_file=-',
                '-f', 'null', '-']
    p = subprocess.Popen(command, stderr=subprocess.PIPE, stdout=subprocess.PIPE, universal_newlines=True)
    task.process_pid = p.pid
    task.save()

    out, err = p.communicate()
    task.message = err
    task.save()
    
    if p.returncode > 0 :
        error = True

    try:
        chart_labels = []

        dataset = {}
        dataset['label'] = task.media.name
        dataset['backgroundColor'] = '{backgroundColor}'
        dataset['borderColor'] = '{borderColor}'
        dataset['fill'] = '{false}'
        dataset['pointRadius'] = '{pointRadius}'
        dataset['pointHoverRadius'] = '{pointHoverRadius}'
        dataset['data'] = []

        raw_data = out.splitlines()
        sum_data = 0
        nb_data = 1
        for line in raw_data:
            chart_labels.append(str(datetime.timedelta(seconds=(nb_data/task.media.framerate))))
            value = float(line[line.find('psnr_avg:')+9:line.find('psnr_y:')].strip())
            if str(value) == 'inf':
                value = 100
            dataset['data'].append(value)
            sum_data += value
            nb_data+=1

        task.average_score = sum_data / nb_data
        task.save()

        task.save_chart_dataset(dataset)
        task.save_chart_labels(chart_labels)

    except:
        error = True

    if error is True:
        task.message = err
        task.save()

    callback_task(task, error)


def generate_thumbnail(task, callback_task) :
    error = False

    output_img_path = os.path.join(os.path.dirname(task.media.file.path), task.media.name+"_"+task.metric.name+"_"+str(task.id)+".jpg")
    
    command = [FFMPEG_PATH,
                '-hide_banner',
                '-ss', '1',
                '-i', task.media.file.path,
                '-vf', 'select=gt(scene\,0.5),scale=320:-1',
                '-frames:v', '1', '-y', output_img_path]

    p = subprocess.Popen(command, stderr=subprocess.PIPE, stdout=subprocess.PIPE, universal_newlines=True)
    task.process_pid = p.pid
    task.save()

    out, err = p.communicate()
    task.message = err
    task.save()

    if p.returncode > 0:
        error = True

    try:
        task.output_data_path = output_img_path
        task.save()

    except:
        error = True

    if error is True:
        task.message = err
        task.save()

    callback_task(task, error)