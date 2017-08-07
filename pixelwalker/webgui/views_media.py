# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone


# import db models
from engine.models import EncodingProvider, Media, Media


# List all medias
def list(request):
    media_list = Media.objects.all().order_by('name')
    return render(request, 'media/list.html', {'media_list':media_list})


#Crud
def create(request):
    # Submitting values for new media
    if request.POST:
        new_media = Media()
        # set values
        new_media.name = request.POST.get('name')
        new_media.file_path = request.POST.get('file_path')
        new_media.date_added = timezone.now()
        new_media.encoding_provider = EncodingProvider.objects.filter(id=request.POST.get('encoding_provider_id'))[0]
        new_media.save()
        return HttpResponseRedirect(reverse('webgui:media_read', args=(new_media.id,)))

    # Asking for the new media form
    else:
        return render(request, 'media/create.html')


#cRud
def read(request, media_id):
    media = get_object_or_404(Media, pk=media_id)
    return render(request, 'media/read.html', {'media': media})


#crUd
def update(request, media_id):
    media = get_object_or_404(Media, pk=media_id)

    # Submitting values for updating media
    if request.POST:
        # update values
        media.name = request.POST.get('name')
        media.file_path = request.POST.get('file_path')
        media.encoding_provider = EncodingProvider.objects.filter(id=request.POST.get('encoding_provider_id'))[0]
        media.save()
        return HttpResponseRedirect(reverse('webgui:media_read', args=(media.id,)))

    # Asking for the new media form
    else:
        return render(request, 'media/update.html', {'media': media})


#cruD
def delete(request, media_id):
    media = Media.objects.filter(id=media_id)[0]

    # If delete confirm
    if request.POST:
        # delete the media object
        if media_id == request.POST.get('delete_id'):
            media.delete()
            return HttpResponseRedirect(reverse('webgui:media_list'))
        else:
            return render(request, 'media/read.html', {'media': media})

    # Asking for the delete confirmation form
    else:
        return render(request, 'media/delete.html', {'media': media})
