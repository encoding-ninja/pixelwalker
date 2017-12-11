from django.urls import path

from .api.v1 import views as api
from .webgui import views_assessment as assessment

urlpatterns = [
	# API v1
    path('api/v1/', api.index, name='index'),
    # WEBGUI
    path('', assessment.list, name='webgui_assessment-list'),   
    path('assessment/create', assessment.create, name='webgui_assessment-create'),   
    path('assessment/<int:assessment_id>', assessment.read, name='webgui_assessment-read'),   
    path('assessment/<int:assessment_id>/update', assessment.update, name='webgui_assessment-update'),   
    path('assessment/<int:assessment_id>/delete', assessment.delete, name='webgui_assessment-delete'),   
]