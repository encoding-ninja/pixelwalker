from django.apps import AppConfig
from .service import Service
import sched, time



class EngineConfig(AppConfig):
    name = 'engine'
    task_service = Service()
    
    def ready(self):
        print("App ready!")
        if not self.task_service.running:
            self.task_service.start()
        
   
        
        


        
