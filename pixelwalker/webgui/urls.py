from django.conf.urls import url

from . import views
from . import views_assessment
from . import views_encoding_provider
from . import views_media
from . import views_task

urlpatterns = [
    url(r'^$', views.hello_world, name='index'),
    # Assessment
    url(r'^assessment/$', views_assessment.list, name='assessment_list'),
    url(r'^assessment/create/$', views_assessment.create, name='assessment_create'),
    url(r'^assessment/(?P<assessment_id>[0-9]+)/$', views_assessment.read, name='assessment_read'),
    url(r'^assessment/(?P<assessment_id>[0-9]+)/update/$', views_assessment.update, name='assessment_update'),
    url(r'^assessment/(?P<assessment_id>[0-9]+)/delete/$', views_assessment.delete, name='assessment_delete'),
    url(r'^assessment/(?P<assessment_id>[0-9]+)/chart/$', views_assessment.chart, name='assessment_chart'),
	# EncodingProvider
    url(r'^encoding_provider/$', views_encoding_provider.list, name='encoding_provider_list'),
    url(r'^encoding_provider/create/$', views_encoding_provider.create, name='encoding_provider_create'),
    url(r'^encoding_provider/(?P<encoding_provider_id>[0-9]+)/$', views_encoding_provider.read, name='encoding_provider_read'),
    url(r'^encoding_provider/(?P<encoding_provider_id>[0-9]+)/update/$', views_encoding_provider.update, name='encoding_provider_update'),
    url(r'^encoding_provider/(?P<encoding_provider_id>[0-9]+)/delete/$', views_encoding_provider.delete, name='encoding_provider_delete'),
    # Media
    url(r'^media/$', views_media.list, name='media_list'),
    url(r'^media/create/$', views_media.create, name='media_create'),
    url(r'^media/(?P<media_id>[0-9]+)/$', views_media.read, name='media_read'),
    url(r'^media/(?P<media_id>[0-9]+)/update/$', views_media.update, name='media_update'),
    url(r'^media/(?P<media_id>[0-9]+)/delete/$', views_media.delete, name='media_delete'),
    # Task
     url(r'^task/$', views_task.list, name='task_list'),
     url(r'^task/(?P<task_id>[0-9]+)/$', views_task.read, name='task_read'),
     url(r'^task/(?P<task_id>[0-9]+)/delete/$', views_task.delete, name='task_delete'),
]