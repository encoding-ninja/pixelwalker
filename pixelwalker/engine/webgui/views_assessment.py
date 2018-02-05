from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse

import json

from ..models import Assessment, Media, EncodingProvider, Task, TaskType

# List all assessments
def list(request):
    assessment_list = Assessment.objects.all().order_by('-id')
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
        
        return HttpResponseRedirect(reverse('webgui_assessment-read', args=(new_assessment.id,)))

    # Asking for the new assessment form
    else:
        media_list = Media.objects.all().order_by('name')
        return render(request, 'assessment/create.html', {'media_list':media_list})

#cRud
def read(request, assessment_id):
    assessment = get_object_or_404(Assessment, pk=assessment_id)
    metric_list = TaskType.objects.filter(is_video_metric=True).order_by('id')
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
            # Reference media changed => Delete previous assessment values
            if assessment.reference_media != Media.objects.get(id=request.POST.get('reference_media')):
                Task.objects.filter(assessment=assessment).delete()

            assessment.reference_media = Media.objects.get(id=request.POST.get('reference_media'))
        else:
            # There is no longer a reference media, delete all metric results
            assessment.reference_media = None
            Task.objects.filter(assessment=assessment).delete()

        # Update the list of media encoded variants
        if len(request.POST.getlist('encoded_media_list')) > 0:
            assessment.encoded_media_list.clear()
            for encoded_media in request.POST.getlist('encoded_media_list'):
                assessment.encoded_media_list.add(Media.objects.get(id=encoded_media))
        else:
            assessment.encoded_media_list.clear()

        assessment.save()

        # Remove task is the encoded media variant is no longer in assessment
        for task in Task.objects.filter(assessment=assessment):
            if task.media not in assessment.encoded_media_list.all():
                task.delete()

        assessment.save()
        return HttpResponseRedirect(reverse('webgui_assessment-read', args=(assessment.id,)))

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
        if assessment_id == int(request.POST.get('delete_id')):
            assessment.delete()
            return HttpResponseRedirect(reverse('webgui_assessment-list'))
        else:
            return render(request, 'assessment/read.html', {'assessment': assessment})

    # Asking for the delete confirmation form
    else:
        return render(request, 'assessment/delete.html', {'assessment': assessment})

# Chart details view
def chart(request, assessment_id):
    assessment = get_object_or_404(Assessment, pk=assessment_id)
    metric_list = TaskType.objects.filter(is_video_metric=True).order_by('id')
    chart_config = {}

    # Get Request POST
    if request.POST:
        chart_config['metrics'] = [ int(x) for x in request.POST.getlist('metrics') ]
        if len(chart_config['metrics']) == 0:
            # Default print all metrics
            for metric in metric_list:
                chart_config['metrics'].append(int(metric.id))
        
        chart_config['value_type'] = request.POST.get('value_type', 'average')
        chart_config['group_by'] = request.POST.get('group_by', 'metric')
    else:
        # Default config
        chart_config['metrics'] = []
        for metric in metric_list:
            chart_config['metrics'].append(int(metric.id))
        chart_config['value_type'] = 'average'
        chart_config['group_by'] = 'metric'

    return render(request, 'assessment/chart.html', {'assessment': assessment, 'metric_list': metric_list, 'chart_config':chart_config})