# sybase/pyodbc.py
# Copyright (C) 2005-2012 the SQLAlchemy authors and contributors <see AUTHORS file>
#
# This module is part of SQLAlchemy and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

"""
Support for Sybase via pyodbc.

http://pypi.python.org/pypi/pyodbc/

Connect strings are of the form::

    sybase+pyodbc://<username>:<password>@<dsn>/
    sybase+pyodbc://<username>:<password>@<host>/<database>

Unicode Support
---------------

The pyodbc driver currently supports usage of these Sybase types with
Unicode or multibyte strings::

    CHAR
    NCHAR
    NVARCHAR
    TEXT
    VARCHAR

Currently *not* supported are::

    UNICHAR
    UNITEXT
    UNIVARCHAR

"""

from lib.sqlalchemy.dialects.sybase.base import SybaseDialect,\
                                            SybaseExecutionContext
from lib.sqlalchemy.connectors.pyodbc import PyODBCConnector
from lib.sqlalchemy import processors
from lib.sqlalchemy.util.compat import decimal

class _SybNumeric_pyodbc(sqltypes.Numeric):
    """Turns Decimals with adjusted() < -6 into floats.

    It's not yet known how to get decimals with many
    significant digits or very large adjusted() into Sybase
    via pyodbc.

    """

    def bind_processor(self, dialect):
        super_process = super(_SybNumeric_pyodbc,self).\
                                    bind_processor(dialect)

        def process(value):
            if self.asdecimal and \
                    isinstance(value, decimal.Decimal):

                if value.adjusted() < -6:
                    return processors.to_float(value)

            if super_process:
                return super_process(value)
            else:
                return value
        return process

class SybaseExecutionContext_pyodbc(SybaseExecutionContext):
    def set_ddl_autocommit(self, connection, value):
        if value:
            connection.autocommit = True
        else:
            connection.autocommit = False

class SybaseDialect_pyodbc(PyODBCConnector, SybaseDialect):
    execution_ctx_cls = SybaseExecutionContext_pyodbc

    colspecs = {
        sqltypes.Numeric:_SybNumeric_pyodbc,
    }

dialect = SybaseDialect_pyodbc
