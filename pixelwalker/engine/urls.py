from django.urls import path

from .api.v1 import views as api
from .webgui import views_assessment as assessment
from .webgui import views_media as media
from .webgui import views_encoding_provider as encoding_provider
from .webgui import views_task as task
from .webgui import views_app_settings as app_settings

urlpatterns = [
	# API v1
    path('api/v1/', api.index, name='index'),
    # WEBGUI
    # Assessment
    path('', assessment.list, name='webgui_assessment-list'),   
    path('assessment', assessment.list, name='webgui_assessment-list'),   
    path('assessment/create', assessment.create, name='webgui_assessment-create'),   
    path('assessment/<int:assessment_id>', assessment.read, name='webgui_assessment-read'),   
    path('assessment/<int:assessment_id>/update', assessment.update, name='webgui_assessment-update'),   
    path('assessment/<int:assessment_id>/delete', assessment.delete, name='webgui_assessment-delete'),
    # Media
    path('media', media.list, name='webgui_media-list'),  
    path('media/create', media.create, name='webgui_media-create'),  
    path('media/<int:media_id>', media.read, name='webgui_media-read'),  
    path('media/<int:media_id>/update', media.update, name='webgui_media-update'),  
    path('media/<int:media_id>/delete', media.delete, name='webgui_media-delete'),  
    # EncodingProvider
    path('encoding_provider', encoding_provider.list, name='webgui_encoding-provider-list'),   
    path('encoding_provider/create', encoding_provider.create, name='webgui_encoding-provider-create'),   
    path('encoding_provider/<int:encoding_provider_id>', encoding_provider.read, name='webgui_encoding-provider-read'),   
    path('encoding_provider/<int:encoding_provider_id>/update', encoding_provider.update, name='webgui_encoding-provider-update'),   
    path('encoding_provider/<int:encoding_provider_id>/delete', encoding_provider.delete, name='webgui_encoding-provider-delete'),   
    # Task
    path('task', task.list, name='webgui_task-list'), 
    # AppSettings
    path('app_settings', app_settings.read, name='webgui_app-settings-read'),   
    path('app_settings/update', app_settings.update, name='webgui_app-settings-update'), 
]