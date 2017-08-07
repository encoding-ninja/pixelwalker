# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic


# import db models
from engine.models import EncodingProvider, Media, Assessment


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
        new_assessment.save()
        return HttpResponseRedirect(reverse('webgui:assessment_read', args=(new_assessment.id,)))

    # Asking for the new assessment form
    else:
        return render(request, 'assessment/create.html')


#cRud
def read(request, assessment_id):
    assessment = get_object_or_404(Assessment, pk=assessment_id)
    return render(request, 'assessment/read.html', {'assessment': assessment})


#crUd
def update(request, assessment_id):
    assessment = get_object_or_404(Assessment, pk=assessment_id)

    # Submitting values for updating assessment
    if request.POST:
        # update values
        assessment.name = request.POST.get('name')
        assessment.description = request.POST.get('description')
        assessment.save()
        return HttpResponseRedirect(reverse('webgui:assessment_read', args=(assessment.id,)))

    # Asking for the new assessment form
    else:
        return render(request, 'assessment/update.html', {'assessment': assessment})


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
