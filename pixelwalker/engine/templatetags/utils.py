from django import template
register = template.Library()

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
    assessment_task_list = Task.objects.filter(assessment=assessment, type=task.type)
    if task.get_average_score() == max(t.get_average_score() for t in assessment_task_list):
        return True
    else:
        return False

@register.simple_tag
def is_worst_assessment_task(assessment, task):
    assessment_task_list = Task.objects.filter(assessment=assessment, type=task.type)
    if task.get_average_score() == min(t.get_average_score() for t in assessment_task_list):
        return True
    else:
        return False