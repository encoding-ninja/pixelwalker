# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic


# import db models
from ..models import AppSettings, TaskType


#cRud
def read(request):
    app_settings = get_object_or_404(AppSettings, pk=1)
    metric_list = TaskType.objects.filter(is_video_metric=False).order_by('name')
    return render(request, 'app_settings/read.html', {'app_settings': app_settings, 'metric_list': metric_list})

#crUd
def update(request):
    app_settings = get_object_or_404(AppSettings, pk=1)
    metric_list = TaskType.objects.filter(is_video_metric=False).order_by('name')

    # Submitting values for updating encoding provider
    if request.POST:
        
        # update task type values
        for metric in metric_list:
            if request.POST.get(str(metric.id)+'_auto_submit_on_new_media') is not None:
                metric.auto_submit_on_new_media = True
            else:
                metric.auto_submit_on_new_media = False
            metric.save()
            
        return HttpResponseRedirect(reverse('webgui_app-settings-read'))

    # Asking for the edit encoding provider form
    else:
        return render(request, 'app_settings/update.html', {'app_settings': app_settings, 'metric_list': metric_list})

