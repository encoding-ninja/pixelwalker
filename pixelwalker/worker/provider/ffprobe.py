import subprocess
import sys
import os

FFPROBE_PATH = os.path.join(os.path.abspath(sys.path[0]), 'worker', 'provider', 'dependencies', 'ffprobe.exe')

def execute(task, callback_task, input_file_path) :
    command = [FFPROBE_PATH,
                '-hide_banner',
                '-i', input_file_path,
                '-show_format', '-show_streams', 
                '-print_format', 'json', '-pretty']
    print command
    p = subprocess.Popen(command, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    out, err = p.communicate()

    callback_task(task, out)