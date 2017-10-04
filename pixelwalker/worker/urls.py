from django.conf.urls import url

from . import views
from . import views_task
from . import service

import threading

urlpatterns = [
    # Task
    url(r'^task/create/$', views_task.create, name='task_create'),
    url(r'^task/(?P<task_id>[0-9]+)/abort/$', views_task.abort, name='task_abort'),
    url(r'^task/(?P<task_id>[0-9]+)/retry/$', views_task.retry, name='task_retry'),
    url(r'^task/(?P<task_id>[0-9]+)/remove/$', views_task.remove, name='task_remove'),
]

thr = threading.Thread(target=service.start, args=(), kwargs={})
thr.start()