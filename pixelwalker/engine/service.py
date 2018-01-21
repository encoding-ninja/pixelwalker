# -*- coding: utf8 -*-
import time, threading, json, requests
from .models import AppSettings, Task


class Service(object):
    """This class defines a task pulling service"""

    def __init__(self):
        self.running = False
        self.app_settings = AppSettings.objects.first()
    
    def start(self):
        print("Starting service...")
        
        # Reset processing task at startup
        for task in self.get_processing_tasks():
            task.state = Task.QUEUED
            task.save()

        self.pulling_thread = threading.Thread(target=self.pulling_tasks, args=(), kwargs={})
        self.pulling_thread.start()

    def pulling_tasks(self):
        self.running = True
        print("Service started")

        # Pulling tasks
        while True:
            # Refresh App Settings
            self.app_settings = AppSettings.objects.first()

            # Sleep interval
            time.sleep(int(self.app_settings.worker_pulling_interval))

            # For queued tasks
            for task in self.get_queued_tasks():
                if self.get_empty_task_slot() > 0:
                    # Prepare to send task to available worker
                    data = {}
                    data['id'] = task.id
                    data['media_file_path'] = task.media.file.path
                    data['type'] = task.type.name

                    url = "http://localhost:8000/api/v1/worker/task"
                    headers = {'content-type': 'application/json'}
                    r=requests.post(url, data=json.dumps(data), headers=headers)

                    if r.status_code == 200:
                        # Task correctly received by worker
                        task.state = Task.PROCESSING
                    else:
                        task.state = Task.ERROR
                    task.save()
            
    def get_processing_tasks(self):
        return Task.objects.filter(state=Task.PROCESSING).order_by("id")

    def get_queued_tasks(self):
        return Task.objects.filter(state=Task.QUEUED).order_by("id")

    def get_empty_task_slot(self):
        return (self.app_settings.max_parallel_tasks - len(Task.objects.filter(state=Task.PROCESSING)))
