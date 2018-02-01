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