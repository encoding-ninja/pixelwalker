# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic


# import db models
from ..models import Assessment, Media, EncodingProvider, Task, TaskType, TaskOutput


# List all tasks
def list(request):
    task_list = Task.objects.all().order_by('-id')
    return render(request, 'task/list.html', {'task_list':task_list})

#cRud
def read(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    return render(request, 'task/read.html', {'task': task})
