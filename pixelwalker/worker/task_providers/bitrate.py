# -*- coding: utf8 -*-

from .generic import TaskProvider

import os, json

class BitrateProvider(TaskProvider):
    """This class defines a Bitrate analysis task"""

    def __init__(self, task_id, input_file_path):
        """Bitrate analysis initialization
        
        :param task_id: The task identifier
        :type task_id: int
        :param input_file_path: The input video file path
        :type input_file_path: str
        """
        TaskProvider.__init__(self, task_id, input_file_path)

    def execute(self):
        """Using FFprobe for Bitrate analysis"""
        command = ['ffprobe',
                '-hide_banner',
                '-i', self.input_file_path,
                '-select_streams', 'v:0',
                '-show_frames', 
                '-print_format', 'json']
        TaskProvider.execute(self, command)

        try:
            bitrate_data = json.loads(self.subprocess_out)

            # create json file Chart.js compatible
            chart_data = {}
            chart_data['labels'] = []
            chart_data['datasets'] = []

            dataset_I = {}
            dataset_I['label'] = 'I Frames'
            dataset_I['backgroundColor'] = 'red'
            dataset_I['data'] = []

            dataset_P = {}
            dataset_P['label'] = 'P Frames'
            dataset_P['backgroundColor'] = 'orange'
            dataset_P['data'] = []

            dataset_B = {}
            dataset_B['label'] = 'B Frames'
            dataset_B['backgroundColor'] = 'blue'
            dataset_B['data'] = []

            for frame in bitrate_data['frames']:
        	    chart_data['labels'].append(int(frame['coded_picture_number']))
        	    if frame['pict_type'] == 'I':
        		    dataset_I['data'].append(int(frame['pkt_size']))
        		    dataset_P['data'].append(0)
        		    dataset_B['data'].append(0)
        	    elif frame['pict_type'] == 'P':
        		    dataset_I['data'].append(0)
        		    dataset_P['data'].append(int(frame['pkt_size']))
        		    dataset_B['data'].append(0)
        	    elif frame['pict_type'] == 'B':
        		    dataset_I['data'].append(0)
        		    dataset_P['data'].append(0)
        		    dataset_B['data'].append(int(frame['pkt_size']))

            chart_data['datasets'].append(dataset_I)
            chart_data['datasets'].append(dataset_P)
            chart_data['datasets'].append(dataset_B)

            self.output_file_path = os.path.join(os.path.dirname(self.input_file_path), self.input_file_name+"_task-"+str(self.task_id)+"-bitrate-chart.json")
            with open(self.output_file_path, "w") as f:
                f.write(json.dumps(chart_data))
        
            data = {}
            data['outputs'] = []
            output = {}
            output['name'] = 'Bitrate'
            output['file_path'] = self.output_file_path
            output['average'] = None
            output['type'] = 'ChartData'
            data['outputs'].append(output)
            self.acknowledge_success(data)

        except:
            self.acknowledge_error() 
