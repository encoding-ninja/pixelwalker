# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic

import json

# import db models
from ..models import ChartAnnotation, Assessment, TaskType


#Crud
def create(request):
    # Submitting values for new encoding provider
    if request.POST:
        new_annotation = ChartAnnotation()
        # set values
        new_annotation.label = request.POST.get('label')
        new_annotation.x = float(request.POST.get('x'))
        new_annotation.y = float(request.POST.get('y'))

        new_annotation.assessment = Assessment.objects.get(pk=int(request.POST.get('assessment_id')))
        new_annotation.save()

        for metric_id in json.loads(str(request.POST.get('metric_list'))):
            new_annotation.metric_list.add(TaskType.objects.get(pk=int(metric_id)))
        
        if request.POST.get('display_type') is 'average':
            new_annotation.display_type = ChartAnnotation.AVERAGE
        elif request.POST.get('display_type') is 'all_frames':
            new_annotation.display_type = ChartAnnotation.ALL_FRAMES
            

        new_annotation.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])

#cruD
def delete(request, annotation_id):
    annotation = get_object_or_404(ChartAnnotation, pk=annotation_id)
    annotation.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
