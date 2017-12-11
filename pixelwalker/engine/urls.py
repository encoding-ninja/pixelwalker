from django.urls import path

from .api.v1 import views as api
from .webgui import views_assessment as assessment

urlpatterns = [
	# API v1
    path('api/v1/', api.index, name='index'),
    # WEBGUI
    path('', assessment.list, name='assessment_list'),   
]