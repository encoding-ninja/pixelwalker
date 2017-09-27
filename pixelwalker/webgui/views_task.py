# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic


# import db models
from engine.models import EncodingProvider, Media, Assessment
from worker.models import Metric, Task, Result


# List all assessments
def list(request):
    task_list = Task.objects.all().order_by('-id')
    return render(request, 'task/list.html', {'task_list':task_list})
