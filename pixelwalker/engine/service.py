# -*- coding: utf8 -*-

class Service(object):
    """This class defines a task pulling service"""

    def __init__(self):
        self.running = False
    
    def start(self):
        print("Starting service...")
        self.running = True
        print("Service started")