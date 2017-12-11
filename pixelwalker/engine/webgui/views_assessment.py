from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic

import json


# List all assessments
def list(request):
    return render(request, 'assessment/list.html')