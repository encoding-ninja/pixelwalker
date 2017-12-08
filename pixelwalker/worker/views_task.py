from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone

import os
import signal

# import db models
from engine.models import EncodingProvider, Media, Assessment
from worker.models import Metric, Task

#Crud
def create(request):
    # Submitting values for new assessment
    if request.POST:

        # list all possible metrics
        metric_list = Metric.objects.all()
        for metric in metric_list:
            requested_metric_list = request.POST.getlist(metric.name+'[]')
            if len(requested_metric_list) > 0:
                for media_id in requested_metric_list:
                    # set simple task values
                    new_task = Task()
                    new_task.assessment = Assessment.objects.get(id=request.POST.get('assessment_id'))
                    new_task.media = Media.objects.get(id=media_id)
                    new_task.metric = metric
                    new_task.date_queued = timezone.now()
                    new_task.save()
        
        return HttpResponseRedirect(reverse('webgui:assessment_read', args=(new_task.assessment.id,)))

    # Return to assessment list
    else:
        return render(request, 'assessment/list.html')


#User abort
def abort(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    
    task.state = Task.ABORTED

    if task.output_data_path is not None:
        try:
            os.remove(task.output_data_path)
        except OSError:
            pass
        task.output_data_path = None

    if task.chart_labels_path is not None:
        try:
            os.remove(task.chart_labels_path)
        except OSError:
            pass
        task.chart_labels_path = None
    
    task.date_ended = timezone.now()
    task.save()

    if task.process_pid is not None:
        os.kill(task.process_pid, signal.SIGINT)
    task.process_pid = None
    task.save()

    return HttpResponseRedirect(reverse('webgui:task_list'))

#User retry
def retry(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    task.state = Task.QUEUED
    task.progress = 0

    if task.output_data_path is not None:
        try:
            os.remove(task.output_data_path)
        except OSError:
            pass
        task.output_data_path = None

    if task.chart_labels_path is not None:
        try:
            os.remove(task.chart_labels_path)
        except OSError:
            pass
        task.chart_labels_path = None
        
    task.process_pid = None
    task.date_queued = timezone.now()
    task.date_started = None
    task.date_ended = None
    task.save()
    return HttpResponseRedirect(reverse('webgui:task_list'))

#User delete
def remove(request, task_id):
    task = get_object_or_404(Task, pk=task_id)

    if task.output_data_path is not None:
        try:
            os.remove(task.output_data_path)
        except OSError:
            pass

    if task.chart_labels_path is not None:
        try:
            os.remove(task.chart_labels_path)
        except OSError:
            pass

    task.delete()
    return HttpResponseRedirect(reverse('webgui:task_list'))
