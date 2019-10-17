# -*- coding: utf-8 -*-
"""
    wsgi
    ##########
    yinsho wsgi module
"""
import sys

from werkzeug.serving import run_simple
from werkzeug.wsgi import DispatcherMiddleware

from fdm.views import app


#print app.url_map
application = DispatcherMiddleware(app,{
    '/api': app
})

#print app.url_map

if __name__ == "__main__":
    run_simple('0.0.0.0', app.config['PORT'], application, use_reloader=True, use_debugger=True, threaded=True)
