from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from .models import ControlMeta, Message
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

    def parseCmt(self, msg_model):
        msg = {}
        au_model = msg_model.author
        au = {}
        au['uid'] = au_model.uid
        au['exd'] = re.sub(r'[\n\r\s]+', r'', au_model.extra_data)
        au['isb'] = au_model.is_blacklist

        msg['body'] = msg_model.content
        msg['au'] = au
        msg['im'] = msg_model.uid
        msg['isb'] = msg_model.is_blacklist
        msg['tstp'] = int(msg_model.recieved_time.timestamp())

        return msg

    # we use get method to handle request for comments
    def get(self, request):
        if request.is_ajax():
            data = {}
            icmt = request.GET.get('icmt', '-1')
            tstp = request.GET.get('tstp', '-1')
            # print(icmt, tstp)
            cmt = Message.objects.all().order_by('recieved_time')
            lcmt = []
            for m in cmt:
                lcmt.append(self.parseCmt(m))
            data['lcmt'] = lcmt
            data['tstp'] = int(time())
            data['icmt'] = cmt.latest('recieved_time').uid
            data['rv'], data['tv'] = 0, 0
            data['st'] = False
            try:
                data['st'] = ControlMeta.objects.get(pk = 1).is_start
            except: pass

            return JSONResponse(data)

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
