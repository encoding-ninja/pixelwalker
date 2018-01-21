from django.urls import path

from .api.v1 import endpoints as api

urlpatterns = [
	# API v1
    path('api/v1/worker', api.index, name='api-worker_root'),
    path('api/v1/worker/task', api.task_submit, name='api-worker_task'),
]