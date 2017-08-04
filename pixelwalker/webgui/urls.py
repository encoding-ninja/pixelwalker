from django.conf.urls import url

from . import views
from . import views_assessment

urlpatterns = [
    url(r'^$', views.hello_world, name='index'),
    #assessment
    url(r'^assessment/$', views_assessment.list, name='assessment_list'),
    url(r'^assessment/create/$', views_assessment.create, name='assessment_create'),
    url(r'^assessment/(?P<assessment_id>[0-9]+)/$', views_assessment.read, name='assessment_read'),
    url(r'^assessment/(?P<assessment_id>[0-9]+)/update/$', views_assessment.update, name='assessment_update'),
    url(r'^assessment/(?P<assessment_id>[0-9]+)/delete/$', views_assessment.delete, name='assessment_delete'),

]