#!/usr/bin/python

import sys
import os

# from google.appengine.ext.webapp.util import run_wsgi_app
sys.path.append(os.path.join(os.path.abspath('.'), 'lib'))
import application

__author__ = 'emilianoberenbaum'



if __name__ == '__main__':
    application.app.run()


