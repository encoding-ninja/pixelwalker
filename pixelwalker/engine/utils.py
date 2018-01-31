# -*- coding: utf-8 -*-
import os
import uuid

def get_upload_path(instance, filename):
    return os.path.join(filename+"_"+str(uuid.uuid4().hex), filename)