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
            bitrate_data = json.loads(self.subprocess_out.decode('utf-8').strip())

            chart_labels = []
            dataset_I = []
            dataset_P = []
            dataset_B = []

            for frame in bitrate_data['frames']:
        	    chart_labels.append(int(frame['coded_picture_number']))
        	    if frame['pict_type'] == 'I':
        		    dataset_I.append(int(frame['pkt_size']))
        		    dataset_P.append(None)
        		    dataset_B.append(None)
        	    elif frame['pict_type'] == 'P':
        		    dataset_I.append(None)
        		    dataset_P.append(int(frame['pkt_size']))
        		    dataset_B.append(None)
        	    elif frame['pict_type'] == 'B':
        		    dataset_I.append(None)
        		    dataset_P.append(None)
        		    dataset_B.append(int(frame['pkt_size']))

            data = {}
            data['outputs'] = []

            # I Frames
            self.output_file_path = os.path.join(os.path.dirname(self.input_file_path), self.input_file_name+"_task-"+str(self.task_id)+"-IFrames.json")
            with open(self.output_file_path, "w") as f:
                f.write(json.dumps(dataset_I))
            output = {}
            output['name'] = 'I Frames'
            output['file_path'] = self.output_file_path
            output['average'] = None
            output['type'] = 'ChartData'
            data['outputs'].append(output)

            # P Frames
            self.output_file_path = os.path.join(os.path.dirname(self.input_file_path), self.input_file_name+"_task-"+str(self.task_id)+"-PFrames.json")
            with open(self.output_file_path, "w") as f:
                f.write(json.dumps(dataset_P))
            output = {}
            output['name'] = 'P Frames'
            output['file_path'] = self.output_file_path
            output['average'] = None
            output['type'] = 'ChartData'
            data['outputs'].append(output)

            # B Frames
            self.output_file_path = os.path.join(os.path.dirname(self.input_file_path), self.input_file_name+"_task-"+str(self.task_id)+"-BFrames.json")
            with open(self.output_file_path, "w") as f:
                f.write(json.dumps(dataset_B))
            output = {}
            output['name'] = 'B Frames'
            output['file_path'] = self.output_file_path
            output['average'] = None
            output['type'] = 'ChartData'
            data['outputs'].append(output)

            # Labels
            self.output_file_path = os.path.join(os.path.dirname(self.input_file_path), self.input_file_name+"_task-"+str(self.task_id)+"-Labels.json")
            with open(self.output_file_path, "w") as f:
                f.write(json.dumps(chart_labels))
            output = {}
            output['name'] = 'Frames Labels'
            output['file_path'] = self.output_file_path
            output['average'] = None
            output['type'] = 'ChartLabels'
            data['outputs'].append(output)

            self.acknowledge_success(data)

        except:
            self.acknowledge_error() 
