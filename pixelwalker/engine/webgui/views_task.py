# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone


# import db models
from ..models import Assessment, Media, EncodingProvider, Task, TaskType, TaskOutput


# List all tasks
def list(request):
    task_list = Task.objects.all().order_by('-id')
    return render(request, 'task/list.html', {'task_list':task_list})

#Crud
def create(request):
    # Submitting values for new assessment
    if request.POST:
        # list all possible metrics
        task_type_list = TaskType.objects.all()
        for task_type in task_type_list:
            print(str(task_type.name))
            requested_task_list = request.POST.getlist(task_type.name+'[]')
            print(str(len(requested_task_list)))
            if len(requested_task_list) > 0:
                for media_id in requested_task_list:
                    print(media_id)
                    # set simple task values
                    new_task = Task()
                    new_task.assessment = Assessment.objects.get(id=request.POST.get('assessment_id'))
                    new_task.media = Media.objects.get(id=media_id)
                    new_task.type = task_type
                    new_task.save()
                    new_task.submit()

        return HttpResponseRedirect(request.META['HTTP_REFERER'])

    # Return to task list
    else:
        return HttpResponseRedirect(reverse('webgui_task-list'))

#cRud
def read(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    output_list = TaskOutput.objects.filter(task=task)
    return render(request, 'task/read.html', {'task': task, 'output_list': output_list})

def redo(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    task.submit()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

def abort(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    task.state = Task.ABORTED
    task.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
