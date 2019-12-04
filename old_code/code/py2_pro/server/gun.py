# -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template_string
import os
from werkzeug.contrib.fixers import ProxyFix
from fdm.views import app


app.wsgi_app = ProxyFix(app.wsgi_app)

if __name__ == "__main__":
    app.run(processes=3)

