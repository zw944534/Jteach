'''
Created on 2022年3月14日

@author: chu
'''
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events
from django.utils import timezone
from django_apscheduler.models import DjangoJobExecution
import sys

def deactivate_expired_accounts():
    today = timezone.now()
    ...
    print('in deactivate');
    # get accounts, expire them, etc.
    ...

def start():
    print('in start');
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")
    # run this job every 24 hours
    scheduler.add_job(deactivate_expired_accounts, 'interval', hours=24, name='clean_accounts', jobstore='default')
    register_events(scheduler)
    scheduler.start()
    print("Scheduler started...", file=sys.stdout)