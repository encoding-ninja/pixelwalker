from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

import json, requests, threading

from ...task_providers import thumbnail

def index(request):
    return HttpResponse("Hello, world. You're at the api root.")

@csrf_exempt
@require_http_methods(["POST"])
def task_submit(request):
    """ Task Endpoint """

    # Parse json body
    try:
        data=json.loads(request.body)
        task_id = int(data['id'])
        task_type = str(data['type'])
        task_media_file_path = str(data['media_file_path'])
    except:
        return HttpResponseBadRequest("Request Body is not a parsable JSON")
    
    # new job for the task
    if task_type == 'THUMBNAIL':
        task_provider = thumbnail.ThumbnailProvider(task_id, task_media_file_path)
    else:
        return HttpResponseBadRequest("The task type of the request is not available: "+str(data['type']))

    provider_thread = threading.Thread(target=task_provider.execute, args=(), kwargs={})
    provider_thread.start()

    return HttpResponse("OK")
