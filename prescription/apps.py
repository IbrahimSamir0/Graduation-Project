from django.apps import AppConfig

class PrescriptionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'prescription'
    # def ready(self):
    #     from .scheduler.scheduler import ExampleThread
    #     thread = ExampleThread()
    #     thread.start()
        
        
        # thread.stop()
        # do other things
        # thread.join()
        
