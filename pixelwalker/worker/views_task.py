from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic


# import db models
from engine.models import EncodingProvider, Media, Assessment
from worker.models import Metric, Task, Provider, Result

#Crud
def create(request):
    # Submitting values for new assessment
    if request.POST:

        # list all possible metrics
        metric_list = Metric.objects.all()
        for metric in metric_list:
        	requested_metric_list = request.POST.getlist(metric.name+'[]')
        	if len(requested_metric_list) > 0:
        		for media_id in requested_metric_list:
        			# set simple task values
        			new_task = Task()
        			new_task.assessment = Assessment.objects.get(id=request.POST.get('assessment_id'))
        			new_task.media = Media.objects.get(id=media_id)
        			new_task.metric = metric
        			new_task.save()
        			print new_task.media.name +"-"+new_task.metric.name
        
        return HttpResponseRedirect(reverse('webgui:assessment_read', args=(request.POST.get('assessment_id'))))

    # Return to assessment list
    else:
        return render(request, 'assessment/list.html')
