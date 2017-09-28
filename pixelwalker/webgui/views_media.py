# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone

import os
import shutil

# import db models
from engine.models import EncodingProvider, Media, Assessment
from worker.models import Metric, Task


# List all medias
def list(request):
    media_list = Media.objects.all().order_by('name')
    return render(request, 'media/list.html', {'media_list':media_list})


#Crud
def create(request):
    # Submitting values for new media
    if request.POST:
        new_media = Media()

        # Updload the file
        new_media.file = request.FILES['file']

        # Set default name
        new_media.name = new_media.file.name
        new_media.date_added = timezone.now()

        # Set encoding provider
        if request.POST.get('encoding_provider') != "None":
            new_media.encoding_provider = EncodingProvider.objects.filter(id=request.POST.get('encoding_provider'))[0]
        else:
            new_media.encoding_provider = None

        new_media.save()

        #Ask for probing task
        new_task = Task()
        new_task.assessment = None
        new_task.media = Media.objects.get(id=new_media.id)
        new_task.metric = Metric.objects.get(name='PROBE')
        new_task.save()

        return HttpResponseRedirect(reverse('webgui:media_read', args=(new_media.id,)))

    # Asking for the new media form
    else:
        encoding_provider_list = EncodingProvider.objects.all().order_by('name')
        return render(request, 'media/create.html', {'encoding_provider_list': encoding_provider_list})


#cRud
def read(request, media_id):
    media = get_object_or_404(Media, pk=media_id)
    assessment_reference_list = Assessment.objects.filter(reference_media=media)

    probe_data_path = Task.objects.get(media=media, metric=Metric.objects.get(name='PROBE')).output_data_path
    if probe_data_path:
        with open (probe_data_path, "r") as f:
            probe = f.readlines()
    else:
        probe = None

    return render(request, 'media/read.html', {'media': media, 'assessment_reference_list': assessment_reference_list, 'probe':probe})


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
            #shutil.rmtree(os.path.dirname(media.file.path))
            media.delete()
            return HttpResponseRedirect(reverse('webgui:media_list'))
        else:
            return render(request, 'media/read.html', {'media': media})

    # Asking for the delete confirmation form
    else:
        return render(request, 'media/delete.html', {'media': media})
