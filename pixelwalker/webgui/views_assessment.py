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
        new_assessment.save()
        return HttpResponseRedirect(reverse('assessment:assessment_read', args=(new_assessment.id,)))

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
        assessment.save()
        return HttpResponseRedirect(reverse('assessment:assessment_read', args=(assessment.id,)))

    # Asking for the new assessment form
    else:
        return render(request, 'assessment/create.html')


#cruD
def delete(request, assessment_id):
    assessment = Assessment.objects.filter(id=assessment_id)[0]
    assessment.delete()
    return HttpResponseRedirect(reverse('assessment:assessment_list'))
