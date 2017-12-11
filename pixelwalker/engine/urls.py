from django.urls import path

from .api.v1 import views as api
from .webgui import views as webgui

urlpatterns = [
	# API v1
    path('api/v1/', api.index, name='index'),
    # WEBGUI
    path('', webgui.index, name='index'),   
]