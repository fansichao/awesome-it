# -*- coding: utf-8 -*-
"""
    wsgi
    ##########
    yinsho wsgi module
"""
import sys
import os
import site

BASEPATH = os.environ["HOME"]
ALLDIRS = [BASEPATH + '/env/lib/python2.7/site-packages']
activate_this = BASEPATH + '/env/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

sys.stdout = sys.stderr
# Remember original sys.path.
prev_sys_path = list(sys.path)
# Add each new site-packages directory.
for directory in ALLDIRS:
        site.addsitedir(directory)
# Reorder sys.path so new directories at the front.
new_sys_path = []
for item in list(sys.path):
        if item not in prev_sys_path:
                new_sys_path.append(item)
                sys.path.remove(item)
sys.path[:0] = new_sys_path


sys.path.insert(1, BASEPATH+ '/fabs')
os.environ['PYTHON_EGG_CACHE'] = BASEPATH + '/.python-eggs'

from fabs.views import app as application
application.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
