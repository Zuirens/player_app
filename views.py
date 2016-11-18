from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from .models import ControlMeta
from django.contrib.auth.models import User
from time import time
import base64
import re
import json

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)



class LiveApiView(View):

    # we use get method to handle request for comments
    def get(self, request):
        if request.is_ajax():
            comment_id = request.GET.get('lcmt', None)
            timestamp = request.GET.get('tstp', None)
            return JSONResponse({'lcmt': 'ZUjd0-3jKSOI', 'tstp': int(time()), 'message': 'go to sleep'})

        return JSONResponse({'comment_id': -1, 'timestamp': -1})

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            pass
        return JSONResponse({'comment_id': -1, 'timestamp': -1})




def index(request):
    try:
        cm = ControlMeta.objects.get(pk = 1)
    except: pass
    abc = 10
    try:
        if request.user.is_authenticated():
            au_user = User.objects.get(username = request.user).authenuser
            au_user.extra_data = re.sub(r'[\n\r\s]+', r'', au_user.extra_data)
            print(au_user.extra_data)
            pass
        else: pass
    except: pass
    return render(request, 'index.html', locals())
