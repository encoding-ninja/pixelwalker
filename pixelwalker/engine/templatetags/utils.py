from django import template
register = template.Library()

from ..models import Assessment, Media, Task, TaskType, TaskOutput

@register.simple_tag
def assessment_media_tasktype_exists(assessment, media, tasktype):
    task = Task.objects.filter(assessment=assessment, media=media, type=tasktype)
    return task