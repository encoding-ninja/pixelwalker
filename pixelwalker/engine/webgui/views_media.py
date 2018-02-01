# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.conf import settings

import os
import shutil
import json
import json2table

# import db models
from ..models import Assessment, Media, EncodingProvider, Task, TaskType


# List all medias
def list(request):
    media_list = Media.objects.all().order_by('-id')
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

            # Auto submit task
            task_type_list = TaskType.objects.filter(auto_submit_on_new_media=True).order_by('-name')
            for task_type in task_type_list:
                new_media.auto_submit_task(task_type.name)

        if len(request.FILES.getlist('files')) > 1:
            return HttpResponseRedirect(reverse('webgui_media-list'))
        else:
            return HttpResponseRedirect(reverse('webgui_media-read', args=(new_media.id,)))

    # Asking for the new media form
    else:
        encoding_provider_list = EncodingProvider.objects.all().order_by('name')
        return render(request, 'media/create.html', {'encoding_provider_list': encoding_provider_list})

#cRud
def read(request, media_id):
    media = get_object_or_404(Media, pk=media_id)
    assessment_reference_list = Assessment.objects.filter(reference_media=media)
    task_list = Task.objects.filter(media=media).order_by('-id')
    return render(request, 'media/read.html', {'media': media, 'assessment_reference_list': assessment_reference_list, 'task_list': task_list})

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
        return HttpResponseRedirect(reverse('webgui_media-read', args=(media.id,)))

    # Asking for the update media form
    else:
        encoding_provider_list = EncodingProvider.objects.all().order_by('name')
        return render(request, 'media/update.html', {'media': media, 'encoding_provider_list': encoding_provider_list})

#cruD
def delete(request, media_id):
    media = Media.objects.filter(id=media_id)[0]

    # If delete confirm
    if request.POST:
        # delete the media object
        if int(media_id) == int(request.POST.get('delete_id')):
            try:
                shutil.rmtree(os.path.dirname(media.file.path))
            except:
                pass
            media.delete()
            return HttpResponseRedirect(reverse('webgui_media-list'))
        else:
            return render(request, 'media/read.html', {'media': media})

    # Asking for the delete confirmation form
    else:
        return render(request, 'media/delete.html', {'media': media})
