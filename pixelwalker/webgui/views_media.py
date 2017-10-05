# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
from django.conf import settings

import os
import shutil
import json
import json2table

# import db models
from engine.models import EncodingProvider, Media, Assessment, AppSettings
from worker.models import Metric, Task


# List all medias
def list(request):
    media_list = Media.objects.all().order_by('name')
    return render(request, 'media/list.html', {'media_list':media_list})


#Crud
def create(request):
    # Submitting values for new media
    if request.POST:
        for f in request.FILES.getlist('files'):
            new_media = Media()

            # Updload the file
            new_media.file = f

            # Set default name
            new_media.name = new_media.file.name
            new_media.date_added = timezone.now()

            # Set encoding provider
            if request.POST.get('encoding_provider') != "None":
                new_media.encoding_provider = EncodingProvider.objects.filter(id=request.POST.get('encoding_provider'))[0]
            else:
                new_media.encoding_provider = None

            new_media.save()

            # Get app settings
            app_settings = AppSettings.objects.get(id=1)

            #Ask for probing task
            if app_settings.auto_probe_media:
                new_media.probe()

            #Ask for bitrate task
            if app_settings.auto_bitrate_analysis:
                new_media.bitrate()

            #Ask for thumbnail task
            if app_settings.auto_generate_thumbnail:
                new_media.generate_thumbnail()

        if len(request.FILES.getlist('files')) > 1:
            return HttpResponseRedirect(reverse('webgui:media_list'))
        else:
            return HttpResponseRedirect(reverse('webgui:media_read', args=(new_media.id,)))

    # Asking for the new media form
    else:
        encoding_provider_list = EncodingProvider.objects.all().order_by('name')
        return render(request, 'media/create.html', {'encoding_provider_list': encoding_provider_list})


#cRud
def read(request, media_id):
    media = get_object_or_404(Media, pk=media_id)
    assessment_reference_list = Assessment.objects.filter(reference_media=media)

    thumb_tasks = Task.objects.filter(media=media, state=Task.SUCCESS, metric=Metric.objects.get(name='THUMBNAIL')).order_by('-id')
    if len(thumb_tasks) > 0:
        thumb_path = thumb_tasks[0].output_data_path
        thumb_url = settings.MEDIA_URL+thumb_path.replace(settings.MEDIA_ROOT+'\\','').replace('\\','/')
    else:
        thumb_url = None

    probe_tasks = Task.objects.filter(media=media, state=Task.SUCCESS, metric=Metric.objects.get(name='PROBE')).order_by('-id')
    if len(probe_tasks) > 0:
        probe_data_path = probe_tasks[0].output_data_path
    else:
        probe_data_path = None
    if probe_data_path:
        with open(probe_data_path) as f:
            probe_json = json.load(f)
        probe = json2table.convert(probe_json, build_direction="LEFT_TO_RIGHT", table_attributes={"class" : "table table-bordered table-hover table-condensed"})
    else:
        probe = None

    bitrate_tasks = Task.objects.filter(media=media, state=Task.SUCCESS, metric=Metric.objects.get(name='BITRATE')).order_by('-id')
    if len(bitrate_tasks) > 0:
        bitrate_data_path = bitrate_tasks[0].output_data_path
    else:
        bitrate_data_path = None
    if bitrate_data_path:
        with open(bitrate_data_path) as f:
            bitrate_chart_data = f.readlines()[0]
    else:
        bitrate_chart_data = None

    return render(request, 'media/read.html', {'media': media, 'assessment_reference_list': assessment_reference_list, 'thumb_url':thumb_url, 'probe':probe, 'bitrate_chart_data':bitrate_chart_data})


#crUd
def update(request, media_id):
    media = get_object_or_404(Media, pk=media_id)

    # Submitting values for updating media
    if request.POST:
        # update values
        media.name = request.POST.get('name')
        if request.POST.get('encoding_provider') != "None":
            media.encoding_provider = EncodingProvider.objects.filter(id=request.POST.get('encoding_provider'))[0]
        else:
            media.encoding_provider = None
        media.save()
        return HttpResponseRedirect(reverse('webgui:media_read', args=(media.id,)))

    # Asking for the new media form
    else:
        encoding_provider_list = EncodingProvider.objects.all().order_by('name')
        return render(request, 'media/update.html', {'media': media, 'encoding_provider_list': encoding_provider_list})


#cruD
def delete(request, media_id):
    media = Media.objects.filter(id=media_id)[0]

    # If delete confirm
    if request.POST:
        # delete the media object
        if media_id == request.POST.get('delete_id'):
            shutil.rmtree(os.path.dirname(media.file.path))
            media.delete()
            return HttpResponseRedirect(reverse('webgui:media_list'))
        else:
            return render(request, 'media/read.html', {'media': media})

    # Asking for the delete confirmation form
    else:
        return render(request, 'media/delete.html', {'media': media})


def probe(request, media_id):
    media = get_object_or_404(Media, pk=media_id)
    media.probe()
    return HttpResponseRedirect(reverse('webgui:task_list'))


def bitrate(request, media_id):
    media = get_object_or_404(Media, pk=media_id)
    media.bitrate()
    return HttpResponseRedirect(reverse('webgui:task_list'))


def generate_thumbnail(request, media_id):
    media = get_object_or_404(Media, pk=media_id)
    media.generate_thumbnail()
    return HttpResponseRedirect(reverse('webgui:task_list'))