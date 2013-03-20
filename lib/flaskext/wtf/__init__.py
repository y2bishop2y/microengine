# -*- coding: utf-8 -*-
"""
    flaskext.wtf
    ~~~~~~~~~~~~

    Flask-WTF extension

    :copyright: (c) 2010 by Dan Jacob.
    :license: BSD, see LICENSE for more details.
"""
from lib.wtforms import fields, validators, widgets

try:
    _is_sqlalchemy = True
except ImportError:
    _is_sqlalchemy = False

from lib.wtforms.fields import *

from lib.flaskext.wtf import html5, recaptcha
from lib.flaskext.wtf.form import Form

from lib.flaskext.wtf.recaptcha.fields import RecaptchaField
from lib.flaskext.wtf.recaptcha.widgets import RecaptchaWidget
from lib.flaskext.wtf.recaptcha.validators import Recaptcha

fields.RecaptchaField = RecaptchaField
widgets.RecaptchaWidget = RecaptchaWidget
validators.Recaptcha = Recaptcha

from lib.flaskext.wtf.file import FileField
from lib.flaskext.wtf.file import FileAllowed, FileRequired, file_allowed, \
        file_required

fields.FileField = FileField

validators.file_allowed = file_allowed
validators.file_required = file_required
validators.FileAllowed = FileAllowed
validators.FileRequired = FileRequired


__all__  = ['Form', 'ValidationError',
            'fields', 'validators', 'widgets', 'html5']

__all__ += validators.__all__
__all__ += fields.__all__ if hasattr(fields, '__all__') else lib.wtforms.fields.core.__all__
__all__ += widgets.__all__ if hasattr(widgets, '__all__') else lib.wtforms.widgets.core.__all__
__all__ += recaptcha.__all__

if _is_sqlalchemy:
    from lib.wtforms.ext.sqlalchemy.fields import QuerySelectField, \
        QuerySelectMultipleField

    __all__ += ['QuerySelectField', 
                'QuerySelectMultipleField']

    for field in (QuerySelectField, 
                  QuerySelectMultipleField):

        setattr(fields, field.__name__, field)

