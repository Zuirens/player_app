from uwsgidecorators import *
from .models import StreamStatistic
import os

TOTAL_USER = {}
REAL_USER = {}

@spool
def record_user(**kwargs):
    global TOTAL_USER, REAL_USER
    print('-----record_user-----')
    if 'user' in kwargs:
        ip = str(kwargs['user'])
        if not ip in TOTAL_USER: TOTAL_USER[ip] = 1
        else: TOTAL_USER[ip] += 1

        if not ip in REAL_USER: REAL_USER[ip] = 1
        else: REAL_USER[ip] += 1
    print('---------------------')


@timer(30, target='spooler')
def dump_record(args):
    global REAL_USER
    record = StreamStatistic(realtime_viewer=len(REAL_USER), total_viewer=len(TOTAL_USER))
    print('-----foo-----')
    try:
        record.clean()
        record.save()
    except Exception as e:
        print('[dump_record] exception:', e)
    print('-------------')
    REAL_USER = {}





