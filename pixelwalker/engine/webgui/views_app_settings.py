# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic


# import db models
from ..models import AppSettings


#cRud
def read(request):
    app_settings = get_object_or_404(AppSettings, pk=1)
    return render(request, 'app_settings/read.html', {'app_settings': app_settings})

#crUd
def update(request):
    app_settings = get_object_or_404(AppSettings, pk=1)

    # Submitting values for updating encoding provider
    if request.POST:
        # update values
        app_settings.max_parallel_tasks = request.POST.get('max_parallel_tasks')
        app_settings.worker_pulling_interval = request.POST.get('worker_pulling_interval')
        app_settings.save()
        return HttpResponseRedirect(reverse('webgui_app-settings-read'))

    # Asking for the edit encoding provider form
    else:
        return render(request, 'app_settings/update.html', {'app_settings': app_settings})

