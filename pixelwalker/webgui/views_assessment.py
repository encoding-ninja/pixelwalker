# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic


# import db models
from engine.models import EncodingProvider, Media, Assessment
from worker.models import Metric, Task


# List all assessments
def list(request):
    assessment_list = Assessment.objects.all().order_by('name')
    return render(request, 'assessment/list.html', {'assessment_list':assessment_list})


#Crud
def create(request):
    # Submitting values for new assessment
    if request.POST:
        new_assessment = Assessment()
        # set values
        new_assessment.name = request.POST.get('name')
        new_assessment.description = request.POST.get('description')

        if request.POST.get('reference_media') != "None":
            new_assessment.reference_media = Media.objects.get(id=request.POST.get('reference_media'))
        else:
            new_assessment.reference_media = None

        new_assessment.save()

        if len(request.POST.getlist('encoded_media_list')) > 0:
            for encoded_media in request.POST.getlist('encoded_media_list'):
                new_assessment.encoded_media_list.add(Media.objects.get(id=encoded_media))
            new_assessment.save()
        
        return HttpResponseRedirect(reverse('webgui:assessment_read', args=(new_assessment.id,)))

    # Asking for the new assessment form
    else:
        media_list = Media.objects.all().order_by('name')
        return render(request, 'assessment/create.html', {'media_list':media_list})


#cRud
def read(request, assessment_id):
    assessment = get_object_or_404(Assessment, pk=assessment_id)
    metric_list = Metric.objects.filter(hidden=False).order_by('id')
    task_list = Task.objects.filter(assessment=assessment)
    return render(request, 'assessment/read.html', {'assessment': assessment, 'metric_list': metric_list, 'task_list': task_list})


#crUd
def update(request, assessment_id):
    assessment = get_object_or_404(Assessment, pk=assessment_id)

    # Submitting values for updating assessment
    if request.POST:
        # update values
        assessment.name = request.POST.get('name')
        assessment.description = request.POST.get('description')

        if request.POST.get('reference_media') != "None":
            assessment.reference_media = Media.objects.get(id=request.POST.get('reference_media'))
        else:
            assessment.reference_media = None

        if len(request.POST.getlist('encoded_media_list')) > 0:
            assessment.encoded_media_list.clear()
            for encoded_media in request.POST.getlist('encoded_media_list'):
                assessment.encoded_media_list.add(Media.objects.get(id=encoded_media))
        else:
            assessment.encoded_media_list.clear()

        assessment.save()
        return HttpResponseRedirect(reverse('webgui:assessment_read', args=(assessment.id,)))

    # Asking for the new assessment form
    else:
        media_list = Media.objects.all().order_by('name')
        return render(request, 'assessment/update.html', {'assessment': assessment, 'media_list':media_list})


#cruD
def delete(request, assessment_id):
    assessment = Assessment.objects.filter(id=assessment_id)[0]

    # If delete confirm
    if request.POST:
        # delete the assessment object
        if assessment_id == request.POST.get('delete_id'):
            assessment.delete()
            return HttpResponseRedirect(reverse('webgui:assessment_list'))
        else:
            return render(request, 'assessment/read.html', {'assessment': assessment})

    # Asking for the delete confirmation form
    else:
        return render(request, 'assessment/delete.html', {'assessment': assessment})
