from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from .models import ControlMeta, Message, AuthenUser
from django.contrib.auth.models import User
from time import time
from django.db.models import Max
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
    MAX_CMT_NUM = 10

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
            try: ic = Message.objects.get(uid=icmt).id
            except: ic = -1
            # print(icmt, ic)
            lastcmt = Message.objects.latest('pk')
            imax = lastcmt.id
            lcmt = []
            if ic > 0:
                if ic < imax:
                    cmt = Message.objects.filter(id__gt = ic)[:LiveApiView.MAX_CMT_NUM]
                    for m in cmt:
                        lcmt.append(self.parseCmt(m))
                    data['lcmt'] = lcmt
                    data['icmt'] = cmt[len(cmt)-1].uid
                else: data['icmt'] = lastcmt.uid
            else:
                cmt = Message.objects.order_by('-id')[:LiveApiView.MAX_CMT_NUM].reverse()
                for m in cmt:
                    lcmt.append(self.parseCmt(m))
                data['lcmt'] = lcmt
                data['icmt'] = cmt[len(cmt) - 1].uid
            data['tstp'] = int(time())
            data['rv'], data['tv'] = 0, 0
            data['st'] = False
            try:
                data['st'] = ControlMeta.objects.get(pk = 1).is_start
            except: pass

            return JSONResponse(data)
        else: pass

        return JSONResponse({'icmt': -1, 'tstp': -1})

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            try:
                body = request.POST.get('body')
                au_uid = request.POST.get('author')
                msg = Message(author = AuthenUser.objects.get(uid=au_uid), content=body)
                msg.full_clean()
                msg.save()
                return JSONResponse({'ec': 1})
            except:
                return JSONResponse({'ec': -1})


        return JSONResponse({'ec': 0})




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
