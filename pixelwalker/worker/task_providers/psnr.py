# -*- coding: utf8 -*-

from .generic import TaskProvider

import os, json, datetime

class PsnrProvider(TaskProvider):
    """This class defines a PSNR analysis task"""

    def __init__(self, task_id, input_file_path, input_framerate, reference_file_path, reference_width, reference_height):
        """PSNR analysis initialization
        
        :param task_id: The task identifier
        :type task_id: int
        :param input_file_path: The input video file path
        :type input_file_path: str
        :param input_framerate: The input video framerate
        :type input_framerate: int
        :param reference_file_path: The reference video file path
        :type reference_file_path: str
        :param reference_width: The reference video width
        :type reference_width: int
        :param reference_height: The reference video height
        :type reference_height: int
        """
        TaskProvider.__init__(self, task_id, input_file_path)

        if os.path.isfile(reference_file_path) is True:       
            self.reference_file_path = reference_file_path
            self.reference_file_name = os.path.basename(reference_file_path)
        else:
            self.acknowledge_error()

        self.reference_definition = str(reference_width)+':'+str(reference_height)
        self.input_framerate = input_framerate

    def execute(self):
        """Using FFmpeg for PSNR analysis"""
        command = ['ffmpeg',
                '-i', self.input_file_path,
                '-i', self.reference_file_path,
                '-lavfi', '[0]scale='+self.reference_definition+'[scaled];[scaled][1]psnr=stats_file=-',
                '-f', 'null', '-']
        TaskProvider.execute(self, command)

        try:
            chart_labels = []

            dataset = {}
            dataset['label'] = self.input_file_name
            dataset['data'] = []

            raw_data = self.subprocess_out.decode('utf-8').splitlines()
            sum_data = 0.
            nb_data = 1.
            for line in raw_data:
                chart_labels.append(str(datetime.timedelta(seconds=(nb_data/self.input_framerate))))
                value = str(line[line.find('psnr_avg:')+9:line.find('psnr_y:')]).strip()
                if value == 'inf':
                    value = 100.
                else:
                    value = float(value)
                dataset['data'].append(value)
                sum_data += value
                nb_data+=1

            average_score = sum_data / nb_data
        except:
            self.acknowledge_error() 

        try:
            data = {}
            data['outputs'] = []

            self.output_file_path = os.path.join(os.path.dirname(self.input_file_path), self.input_file_name+"_task-"+str(self.task_id)+"-psnr-labels.json")
            with open(self.output_file_path, "w") as f:
                f.write(json.dumps(chart_labels))
            output = {}
            output['name'] = 'PSNR Labels'
            output['file_path'] = self.output_file_path
            output['average'] = None
            output['type'] = 'ChartLabels'
            data['outputs'].append(output)

            self.output_file_path = os.path.join(os.path.dirname(self.input_file_path), self.input_file_name+"_task-"+str(self.task_id)+"-psnr-chart.json")
            with open(self.output_file_path, "w") as f:
                f.write(json.dumps(dataset['data']))
            output = {}
            output['name'] = 'PSNR Data'
            output['file_path'] = self.output_file_path
            output['average'] = average_score
            output['type'] = 'ChartData'
            data['outputs'].append(output)
            
            self.acknowledge_success(data)

        except:
            self.acknowledge_error() 
