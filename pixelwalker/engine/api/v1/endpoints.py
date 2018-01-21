from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from ...models import Task, TaskOutput, TaskType
import json


def index(request):
    return HttpResponse("Hello, world. You're at the api root.")

@csrf_exempt
@require_http_methods(["POST"])
def task_acknowledge(request, task_id):
    """ Task Endpoint """

    # Parse json body
    try:
        data=json.loads(request.body)
        task_id = int(data['id'])
        task_state = str(data['state'])
    except:
        return HttpResponseBadRequest("Request Body is not a parsable JSON")

    task = get_object_or_404(Task, pk=task_id)
    if task.state is not Task.ABORTED:
        if task_state == 'SUCCESS':
            task.state = Task.SUCCESS
            task.date_ended = timezone.now()
            
        elif task_state == 'ERROR':
            task.state = Task.ERROR
            task.date_ended = timezone.now()
        
        elif task_state == 'PROCESSING':
            task.state = Task.PROCESSING
            task.date_started = timezone.now()

        elif task_state == 'QUEUED':
            task.state = Task.QUEUED
            task.date_queued = timezone.now()

        else:
            return HttpResponseBadRequest("Unknown task state")

    task.save()

    return HttpResponse("OK")