# -*- coding: utf8 -*-

import os
import json, requests
import subprocess
import uuid

class TaskProvider(object):
    """This class defines a processing task"""

    def __init__(self, task_id, input_file_path):
        """Task initialization
        
        :param task_id: The task identifier
        :type task_id: int
        :param input_file_path: The input video file path
        :type input_file_path: str
        """
        self.task_id = int(task_id)
        if os.path.isfile(input_file_path) is True:       
            self.input_file_path = input_file_path
            self.input_file_name = os.path.basename(input_file_path)
        else:
            raise ValueError('Cannot access the file: {}'.format(input_file_path))

        self.subprocess_pid = None
        self.subprocess_out = None
        self.subprocess_err = None

    def execute(self, command):
        """Launch a subprocess task
        :param command: Arguments array for the subprocess task
        :type command: str[]
        """
        proc = subprocess.Popen(command, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        self.subprocess_pid = proc.pid
        
        try:
            self.subprocess_out, self.subprocess_err = proc.communicate()
        except:
            self.acknowledge_error()

    def acknowledge_error(self):
        data = {}
        data['id'] = self.task_id
        data['state'] = 'ERROR'
        data['logs'] = str(self.subprocess_out) + str(self.subprocess_err)
        url = "http://localhost:8000/api/v1/engine/task/"+str(self.task_id)
        headers = {'content-type': 'application/json'}
        r=requests.post(url, data=json.dumps(data), headers=headers)

    def acknowledge_success(self, data):
        data['id'] = self.task_id
        data['state'] = 'SUCCESS'
        data['logs'] = str(self.subprocess_out) + str(self.subprocess_err)
        url = "http://localhost:8000/api/v1/engine/task/"+str(self.task_id)
        headers = {'content-type': 'application/json'}
        r=requests.post(url, data=json.dumps(data), headers=headers)

    