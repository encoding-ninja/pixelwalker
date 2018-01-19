# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.conf import settings

import os
import shutil
import json
import json2table

# import db models
from ..models import Assessment, Media, EncodingProvider, Task, TaskType


# List all medias
def list(request):
    media_list = Media.objects.all().order_by('name')
    return render(request, 'media/list.html', {'media_list':media_list})
