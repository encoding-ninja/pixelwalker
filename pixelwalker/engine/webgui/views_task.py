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

#cRud
def read(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    output_list = TaskOutput.objects.filter(task=task)
    return render(request, 'task/read.html', {'task': task, 'output_list': output_list})

def redo(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    task.submit()
    task.state = Task.QUEUED
    task.date_queued = timezone.now()
    task.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

def abort(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    task.state = Task.ABORTED
    task.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
