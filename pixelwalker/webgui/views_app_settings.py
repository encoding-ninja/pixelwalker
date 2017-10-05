# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic


# import db models
from engine.models import AppSettings


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

        if request.POST.get('auto_probe_media') == 'on':
        	app_settings.auto_probe_media = True
        else:
        	app_settings.auto_probe_media = False

        if request.POST.get('auto_bitrate_analysis') == 'on':
        	app_settings.auto_bitrate_analysis = True
        else:
        	app_settings.auto_bitrate_analysis = False
        	
        app_settings.save()
        return HttpResponseRedirect(reverse('webgui:app_settings_read'))

    # Asking for the edit encoding provider form
    else:
        return render(request, 'app_settings/update.html', {'app_settings': app_settings})

