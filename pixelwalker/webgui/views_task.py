# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic


# import db models
from engine.models import EncodingProvider, Media, Assessment
from worker.models import Metric, Task


# List all taskss
def list(request):
    task_list = Task.objects.all().order_by('-date_queued')
    return render(request, 'task/list.html', {'task_list':task_list})

#cRud
def read(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    return render(request, 'task/read.html', {'task': task})

#cruD
def delete(request, task_id):
    task = get_object_or_404(Task, pk=task_id)

    # If delete confirm
    if request.POST:
        # delete the media object
        if task_id == request.POST.get('delete_id'):
            return HttpResponseRedirect(reverse('worker:task_remove', args=(task_id,)))
        else:
            return render(request, 'task/read.html', {'task': task})

    # Asking for the delete confirmation form
    else:
        return render(request, 'task/delete.html', {'task': task})