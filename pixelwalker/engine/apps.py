from django.apps import AppConfig

class EngineConfig(AppConfig):
    name = 'engine'
    
    def ready(self):
        print("App ready!")
        from .service import Service
        self.task_service = Service()
        
        if not self.task_service.running:
            self.task_service.start()
