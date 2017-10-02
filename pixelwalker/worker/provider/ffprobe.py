# -*- coding: utf-8 -*-

import subprocess
import sys
import os
import json

FFPROBE_PATH = os.path.join(os.path.abspath(sys.path[0]), 'worker', 'provider', 'dependencies', 'ffprobe.exe')

def execute(task, callback_task) :
    error = False

    command = [FFPROBE_PATH,
                '-hide_banner',
                '-i', task.media.file.path,
                '-show_format', '-show_streams', 
                '-print_format', 'json', '-pretty']

    p = subprocess.Popen(command, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    out, err = p.communicate()

    if p.returncode > 0:
    	error = True

    probe = json.loads(out)
    for stream in probe['streams']:
    	if stream['codec_type'] == 'video':
            task.media.width = int(stream['width'])
            task.media.height = int(stream['height'])
            task.media.average_bitrate = probe['format']['bit_rate']
            task.media.video_codec = stream['codec_name']
            task.media.framerate = int(stream['r_frame_rate'].replace('/1',''))
            task.media.save()

    task.save_chart_dataset(out)

    callback_task(task, error)


def frame_bitrate_analysis(task, callback_task) :
    error = False

    command = [FFPROBE_PATH,
                '-hide_banner',
                '-i', task.media.file.path,
                '-select_streams', 'v:0',
                '-show_frames', 
                '-print_format', 'json']

    p = subprocess.Popen(command, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    out, err = p.communicate()

    if p.returncode > 0:
    	error = True

    #Get json results from ffprobe
    data_json = json.loads(out)

    # create json file Chart.js enabled
    chart_data = {}
    chart_data['labels'] = []
    chart_data['datasets'] = []

    dataset_I = {}
    dataset_I['label'] = 'I Frames'
    dataset_I['backgroundColor'] = 'red'
    dataset_I['data'] = []

    dataset_P = {}
    dataset_P['label'] = 'P Frames'
    dataset_P['backgroundColor'] = 'orange'
    dataset_P['data'] = []

    dataset_B = {}
    dataset_B['label'] = 'B Frames'
    dataset_B['backgroundColor'] = 'blue'
    dataset_B['data'] = []

    for frame in data_json['frames']:
    	chart_data['labels'].append(int(frame['coded_picture_number']))
    	if frame['pict_type'] == 'I':
    		dataset_I['data'].append(int(frame['pkt_size']))
    		dataset_P['data'].append(0)
    		dataset_B['data'].append(0)
    	elif frame['pict_type'] == 'P':
    		dataset_I['data'].append(0)
    		dataset_P['data'].append(int(frame['pkt_size']))
    		dataset_B['data'].append(0)
    	elif frame['pict_type'] == 'B':
    		dataset_I['data'].append(0)
    		dataset_P['data'].append(0)
    		dataset_B['data'].append(int(frame['pkt_size']))

    chart_data['datasets'].append(dataset_I)
    chart_data['datasets'].append(dataset_P)
    chart_data['datasets'].append(dataset_B)

    task.save_chart_dataset(chart_data)

    callback_task(task, error)