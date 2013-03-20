"""
Initialize Flask app

"""

import os
from flask import Flask
from flask.ext.openid import OpenID
from flask.ext.login import LoginManager
from flask.ext.mail import Mail
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.babel import Babel, lazy_gettext

from flask.ext.babel import Babel

# from gae_mini_profiler import profiler, templatetags
from werkzeug.debug import DebuggedApplication

from settings import basedir, ADMINS, MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD
from momentjs import momentjs

app = Flask('application')

#-- Load configurations from Settings.py
app.config.from_object('application.settings')

# Enable jinja2 loop controls extension
app.jinja_env.add_extension('jinja2.ext.loopcontrols')

db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
lm.login_message = lazy_gettext('Please log in to access this page.')

oid = OpenID(app, os.path.join(basedir, 'tmp'))

mail = Mail(app)
babel = Babel(app)



babel = Babel(app)



@app.context_processor
def inject_profiler():
    return dict(profiler_includes=templatetags.profiler_includes())

# Pull in URL dispatch routes
# TODO import urls

# Flask-DebugToolbar (only enabled when DEBUG=True)
# toolbar = DebugToolbarExtension(app)

# Werkzeug Debugger (only enabled when DEBUG=True)
if app.debug:
    app = DebuggedApplication(app, evalex=True)

# GAE Mini Profiler (only enabled on dev server)
# app = profiler.ProfilerWSGIMiddleware(app)


__version__ = "1.0"
