'''
Created on 2022年3月14日

@author: chu
'''
from django.apps import AppConfig

class SchedulerConfig(AppConfig):
    name = 'scheduler'
    def ready(self):
        print('in scheduler app')
        from scheduler import scheduler
        scheduler.start()