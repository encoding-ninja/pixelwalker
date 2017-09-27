
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import uuid

def get_upload_path(instance, filename):
    return os.path.join(filename+"_"+str(uuid.uuid4().hex), filename)