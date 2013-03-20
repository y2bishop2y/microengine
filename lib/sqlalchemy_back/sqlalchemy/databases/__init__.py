# databases/__init__.py
# Copyright (C) 2005-2012 the SQLAlchemy authors and contributors <see AUTHORS file>
#
# This module is part of SQLAlchemy and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

"""Include imports from the sqlalchemy.dialects package for backwards
compatibility with pre 0.6 versions.

"""
postgres = postgresql

__all__ = (
    'access',
    'drizzle',
    'firebird',
    'informix',
    'maxdb',
    'mssql',
    'mysql',
    'postgresql',
    'sqlite',
    'oracle',
    'sybase',
    )
