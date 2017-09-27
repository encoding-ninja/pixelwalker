from django.conf.urls import url

from . import views
from . import views_task

urlpatterns = [
    # Task
    url(r'^task/create/$', views_task.create, name='task_create'),
]