# -*- coding: utf8 -*-

from .generic import TaskProvider

import os

class ThumbnailProvider(TaskProvider):
    """This class defines a Thumbnail task"""

    def __init__(self, task_id, input_file_path):
        """Thumbnail initialization
        
        :param task_id: The task identifier
        :type task_id: int
        :param input_file_path: The input video file path
        :type input_file_path: str
        """
        TaskProvider.__init__(self, task_id, input_file_path)

    def execute(self):
        """Using FFmpeg to generate thumbnails"""

        output_directory = os.path.join(os.path.dirname(self.input_file_path), self.input_file_name+"_task-"+str(self.task_id)+"thumbnails")
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        self.output_file_path = os.path.join(output_directory, "thumb%05d.jpg")
        command = ['ffmpeg',
                '-i', self.input_file_path,
                '-vf', 'scale=250:-1',
                '-r', '1',
                '-f', 'image2',
                '-y', self.output_file_path]
        TaskProvider.execute(self, command)

        if os.path.isfile(self.output_file_path.replace("%05d", "00001")) is True:
            data = {}
            data['outputs'] = []
            output = {}
            output['name'] = 'Thumbnail'
            output['file_path'] = self.output_file_path
            output['average'] = None
            output['type'] = 'MEDIA'
            data['outputs'].append(output)
            self.acknowledge_success(data)
        else:
            self.acknowledge_error() 
        
        
