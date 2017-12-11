# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic

# import db models
from ..models import Assessment, Media, EncodingProvider, Task, TaskType


# List all encoding providers
def list(request):
    encoding_provider_list = EncodingProvider.objects.all().order_by('name')
    media_list = Media.objects.all()
    return render(request, 'encoding_provider/list.html', {'encoding_provider_list':encoding_provider_list, 'media_list':media_list})


#Crud
def create(request):
    # Submitting values for new encoding provider
    if request.POST:
        new_encoding_provider = EncodingProvider()
        # set values
        new_encoding_provider.name = request.POST.get('name')
        new_encoding_provider.save()
        return HttpResponseRedirect(reverse('webgui_encoding-provider-read', args=(new_encoding_provider.id,)))

    # Asking for the new encoding provider form
    else:
        return render(request, 'encoding_provider/create.html')


#cRud
def read(request, encoding_provider_id):
    encoding_provider = get_object_or_404(EncodingProvider, pk=encoding_provider_id)
    media_list = Media.objects.filter(encoding_provider=encoding_provider)
    task_list = Task.objects.filter(media__in=media_list)
    return render(request, 'encoding_provider/read.html', {'encoding_provider': encoding_provider, 'media_list':media_list, 'task_list':task_list})


#crUd
def update(request, encoding_provider_id):
    encoding_provider = get_object_or_404(EncodingProvider, pk=encoding_provider_id)

    # Submitting values for updating encoding provider
    if request.POST:
        # update values
        encoding_provider.name = request.POST.get('name')
        encoding_provider.save()
        return HttpResponseRedirect(reverse('webgui_encoding-provider-read', args=(encoding_provider.id,)))

    # Asking for the edit encoding provider form
    else:
        return render(request, 'encoding_provider/update.html', {'encoding_provider': encoding_provider})


#cruD
def delete(request, encoding_provider_id):
    encoding_provider = get_object_or_404(EncodingProvider, pk=encoding_provider_id)

    # If delete confirm
    if request.POST:
        # delete the encoding provider object
        if encoding_provider_id == int(request.POST.get('delete_id')):
            encoding_provider.delete()
            return HttpResponseRedirect(reverse('webgui_encoding-provider-list'))
        else:
            return render(request, 'encoding_provider/read.html', {'encoding_provider': encoding_provider})

    # Asking for the delete confirmation form
    else:
        return render(request, 'encoding_provider/delete.html', {'encoding_provider': encoding_provider})
