# -*- coding: utf8 -*-

from .generic import TaskProvider

import os, json

class ProbeProvider(TaskProvider):
    """This class defines a Probe task"""

    def __init__(self, task_id, input_file_path):
        """Probe initialization
        
        :param task_id: The task identifier
        :type task_id: int
        :param input_file_path: The input video file path
        :type input_file_path: str
        """
        TaskProvider.__init__(self, task_id, input_file_path)

    def execute(self):
        """Using FFprobe to get input video file informations"""
        command = ['ffprobe',
                '-hide_banner',
                '-i', self.input_file_path,
                '-show_format', '-show_streams', 
                '-print_format', 'json']
        TaskProvider.execute(self, command)

        try:
            self.output_file_path = os.path.join(os.path.dirname(self.input_file_path), self.input_file_name+"_task-"+str(self.task_id)+"-probe.json")
            probe_data = json.loads(self.subprocess_out.decode('utf-8').strip())
            with open(self.output_file_path, "w") as f:
                f.write(json.dumps(probe_data))
        
            data = {}
            data['outputs'] = []
            output = {}
            output['name'] = 'Probe'
            output['file_path'] = self.output_file_path
            output['average'] = None
            output['type'] = 'JSON'
            data['outputs'].append(output)
            self.acknowledge_success(data)

        except:
            self.acknowledge_error() 
