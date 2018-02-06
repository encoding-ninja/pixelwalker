from django import template
register = template.Library()

import json

from ..models import Assessment, Media, Task, TaskType, TaskOutput

@register.simple_tag
def assessment_media_tasktype_exists(assessment, media, tasktype):
    task = Task.objects.filter(assessment=assessment, media=media, type=tasktype)
    return task

@register.simple_tag
def media_tasktype_exists(media, tasktype):
    task = Task.objects.filter(media=media, type=tasktype)
    return task

@register.simple_tag
def is_best_assessment_task(assessment, task):
    assessment_task_list = Task.objects.filter(assessment=assessment, type=task.type, state=Task.SUCCESS)
    if task.get_average_score() == max(t.get_average_score() for t in assessment_task_list):
        return True
    else:
        return False

@register.simple_tag
def is_worst_assessment_task(assessment, task):
    assessment_task_list = Task.objects.filter(assessment=assessment, type=task.type, state=Task.SUCCESS)
    if task.get_average_score() == min(t.get_average_score() for t in assessment_task_list):
        return True
    else:
        return False

@register.simple_tag
def get_assessment_media_metric_average(assessment, media, tasktype):
    task = Task.objects.filter(assessment=assessment, media=media, type=tasktype, state=Task.SUCCESS).last()
    if task:
        return task.get_average_score()
    else:
        return None

@register.simple_tag
def get_assessment_media_metric_data(assessment, media, tasktype):
    task = Task.objects.filter(assessment=assessment, media=media, type=tasktype, state=Task.SUCCESS).last()
    if task:
        output = TaskOutput.objects.filter(task=task, type=TaskOutput.CHART_DATA).last()
        labels = json.load(open(output.file_path))
        return json.dumps(labels)
    else:
        return '[]'

@register.simple_tag
def get_assessment_definition_bitrate_metric_average(assessment, definition, bitrate, tasktype):
    width = int(definition.split("x")[0])
    height = int(definition.split("x")[1])
    media = Media.objects.filter(width=width, height=height, average_bitrate=bitrate).last()
    task = Task.objects.filter(assessment=assessment, media=media, type=tasktype, state=Task.SUCCESS).last()
    if task:
        return task.get_average_score()
    else:
        return 'null'




@register.filter
def human_bitrate(bitrate):
    human_bitrate = str(bitrate)   
    try:
        bitrate = float(bitrate)
        if bitrate > 1000000:
            human_bitrate = str(round(bitrate/1000000, 3))+' Mbps'
        elif bitrate > 1000:
            human_bitrate = str(round(bitrate/1000, 3))+' kbps'
        else:
            human_bitrate = str(bitrate)+' bps'
    except:
        pass

    return human_bitrate

