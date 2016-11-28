from rest_framework.renderers import JSONRenderer
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import ControlMeta, Comment, FbAuthenUser, StreamStatistic
from time import time
import subprocess
import json
from random import random
TOTAL_VIEW = 0
TIME_STEP = 60
REALTIME_VIEW = 0
CURRENT_TIME = int(time())
ID = random.randint(1, 65536)

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)



class LoginView(View):
    def post(self, request):
        if request.is_ajax():
            try:
                uid = request.POST.get('id')
                nick_name = request.POST.get('name')
                link = request.POST.get('link')
                verified = request.POST.get('verified') == 'true'
                pic = request.POST.get('pic')
                user = FbAuthenUser(username=uid, nick_name=nick_name, picture=pic, verified=verified, link=link)
                print(user)
                try:
                    user.full_clean()
                    user.save()
                except: pass

                au_user = authenticate(username=uid)
                if au_user is not None:
                    login(request, au_user)
                return JSONResponse({'ec': 0})

            except Exception as e:
                print(repr(e))
                pass
        return JSONResponse({'ec': -1})

class LiveApiView(View):
    MAX_CMT_NUM = 1

    def parseCmt(self, msg_model):

        msg = {}
        au_model = msg_model.author
        au = {}
        au['uid'] = au_model.username
        au['link'] = au_model.link
        au['isb'] = au_model.is_blacklist
        au['name'] = au_model.nick_name
        # au['exd'] = re.sub(r'[\n\r\s]+', r'', au_model.extra_data)

        msg['body'] = msg_model.body
        msg['au'] = au
        msg['im'] = msg_model.uid
        msg['isb'] = msg_model.is_blacklist
        msg['tstp'] = int(msg_model.recieved_time.timestamp())

        return msg

    # we use get method to handle request for comments
    def get(self, request):
        global CURRENT_TIME, REALTIME_VIEW, TOTAL_VIEW
        t = int(time())
        if (t - CURRENT_TIME) > TIME_STEP:
            record = StreamStatistic(realtime_viewer=REALTIME_VIEW, total_viewer=TOTAL_VIEW)
            try:
                if random() <= 0.25:
                    record.clean()
                    record.save()
            except Exception as e:
                print(e)
            CURRENT_TIME = t
            REALTIME_VIEW = 0
        if request.is_ajax():
            d = {}
            for k, v in request.META.items():
                if type(v) == str or type(v) == int:
                    d[k] = v
                else: d[k] = repr(v)
            # with open('tt.txt', 'a') as f:
            #     json.dump(d, f)
            #     f.write('\n')
            # s = json.dumps(d)
            # cmd = 'echo \'' + s + '\' >>! tt.txt'
            # subprocess.run(cmd, shell=True)
            data = {}
            icmt = request.GET.get('icmt', '-1')
            try: ic = Comment.objects.get(uid=icmt).id
            except: ic = -9
            try:
                lastcmt = Comment.objects.latest('pk')
                imax = lastcmt.id
            except:
                imax = 0

            lcmt = []
            if imax > 0:
                if ic > 0:
                    if ic < imax:
                        cmt = Comment.objects.filter(id__gt = ic)[:LiveApiView.MAX_CMT_NUM]
                        for m in cmt:
                            lcmt.append(self.parseCmt(m))
                        data['lcmt'] = lcmt
                        data['icmt'] = cmt[len(cmt)-1].uid
                    else: data['icmt'] = lastcmt.uid
                else:
                    cmt = Comment.objects.order_by('-id')[:LiveApiView.MAX_CMT_NUM].reverse()
                    for m in cmt:
                        lcmt.append(self.parseCmt(m))
                    data['lcmt'] = lcmt
                    data['icmt'] = cmt[len(cmt) - 1].uid
            data['tstp'] = int(time())

            try:
                meta = ControlMeta.objects.latest('pk')
                data['st'] = meta.is_start
                data['rv'], data['tv'] = int(REALTIME_VIEW * meta.viewer_scaler), int(TOTAL_VIEW + meta.viewer_offset)
            except:
                data['st'] = False
                data['rv'], data['tv'] = REALTIME_VIEW, TOTAL_VIEW
            data['ec'] = 0
            return JSONResponse(data)
        else: return JSONResponse({'ec': 1})


    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            try:
                body = request.POST.get('body')
                au_uid = request.POST.get('author')
                msg = Comment(author = FbAuthenUser.objects.get(username=au_uid), body=body)
                msg.full_clean()
                msg.save()
                cmt = self.parseCmt(msg)
                return JSONResponse(cmt)
            except:
                return JSONResponse({'ec': 1})


        return JSONResponse({'ec': -1})



@ensure_csrf_cookie
def index(request):
    print('-------------------' + str(ID) + '-------------------')

    global TOTAL_VIEW, REALTIME_VIEW
    TOTAL_VIEW += 1
    REALTIME_VIEW += 1

    try:
        cm = ControlMeta.objects.latest('pk')
    except: pass

    return render(request, 'index.html', locals())
