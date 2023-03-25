from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events
from django.utils import timezone
from django_apscheduler.models import DjangoJobExecution
import sys
from ..models import Prescription
from django_thread import Thread
import threading
import schedule
import time

class ExampleThread(threading.Thread):
    def __init__(self):
        prescriptions =Prescription.objects.filter(cancelation_date=None)
        self.prescription = [p for p in  prescriptions]
        threading.Thread.__init__(self)        
    
    
    def run(self):
        try:
        # print('Threading is started')
        
        # run this job every 24 hours
            for p in self.prescription:
                # self.scheduler.add_job(p.isCanceled, 'interval', seconds=4,jobstore='default')
                schedule.every(1).minutes.do(p.isCanceled)
                # schedule.every().hour.do(p.isCanceled)
                schedule.every().day.at("00:00").do(p.isCanceled)

            #     register_events(self.scheduler) 
            #     self.scheduler.start()
            # self.scheduler.join()
                    
            while 1:
                schedule.run_pending()
                time.sleep(1)
        
        except Exception as e:
            print(e)
    # print("Scheduler started...", file=sys.stdout)