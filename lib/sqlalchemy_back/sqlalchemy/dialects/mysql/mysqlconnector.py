# mysql/mysqlconnector.py
# Copyright (C) 2005-2012 the SQLAlchemy authors and contributors <see AUTHORS file>
#
# This module is part of SQLAlchemy and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

"""Support for the MySQL database via the MySQL Connector/Python adapter.

MySQL Connector/Python is available at:

    https://launchpad.net/myconnpy

Connecting
-----------

Connect string format::

    mysql+mysqlconnector://<user>:<password>@<host>[:<port>]/<dbname>

"""

from lib.sqlalchemy.dialects.mysql.base import (MySQLDialect,
    MySQLExecutionContext, MySQLCompiler, MySQLIdentifierPreparer,
    BIT)

from lib.sqlalchemy import util


class MySQLExecutionContext_mysqlconnector(MySQLExecutionContext):

    def get_lastrowid(self):
        return self.cursor.lastrowid


class MySQLCompiler_mysqlconnector(MySQLCompiler):
    def visit_mod(self, binary, **kw):
        return self.process(binary.left) + " %% " + self.process(binary.right)

    def post_process_text(self, text):
        return text.replace('%', '%%')

class MySQLIdentifierPreparer_mysqlconnector(MySQLIdentifierPreparer):

    def _escape_identifier(self, value):
        value = value.replace(self.escape_quote, self.escape_to_quote)
        return value.replace("%", "%%")

class _myconnpyBIT(BIT):
    def result_processor(self, dialect, coltype):
        """MySQL-connector already converts mysql bits, so."""

        return None

class MySQLDialect_mysqlconnector(MySQLDialect):
    driver = 'mysqlconnector'
    supports_unicode_statements = True
    supports_unicode_binds = True
    supports_sane_rowcount = True
    supports_sane_multi_rowcount = True

    supports_native_decimal = True

    default_paramstyle = 'format'
    execution_ctx_cls = MySQLExecutionContext_mysqlconnector
    statement_compiler = MySQLCompiler_mysqlconnector

    preparer = MySQLIdentifierPreparer_mysqlconnector

    colspecs = util.update_copy(
        MySQLDialect.colspecs,
        {
            BIT: _myconnpyBIT,
        }
    )

    @classmethod
    def dbapi(cls):
        from lib.sqlalchemy.dialects.mysql import connector
        return connector

    def create_connect_args(self, url):
        opts = url.translate_connect_args(username='user')
        opts.update(url.query)

        util.coerce_kw_type(opts, 'buffered', bool)
        util.coerce_kw_type(opts, 'raise_on_warnings', bool)
        opts['buffered'] = True
        opts['raise_on_warnings'] = True

        # FOUND_ROWS must be set in ClientFlag to enable
        # supports_sane_rowcount.
        if self.dbapi is not None:
            try:
                from lib.sqlalchemy.dialects.mysql.connector.constants import ClientFlag
                client_flags = opts.get('client_flags', ClientFlag.get_default())
                client_flags |= ClientFlag.FOUND_ROWS
                opts['client_flags'] = client_flags
            except:
                pass
        return [[], opts]

    def _get_server_version_info(self, connection):
        dbapi_con = connection.connection
        version = dbapi_con.get_server_version()
        return tuple(version)

    def _detect_charset(self, connection):
        return connection.connection.charset

    def _extract_error_code(self, exception):
        return exception.errno

    def is_disconnect(self, e, connection, cursor):
        errnos = (2006, 2013, 2014, 2045, 2055, 2048)
        exceptions = (self.dbapi.OperationalError,self.dbapi.InterfaceError)
        if isinstance(e, exceptions):
            return e.errno in errnos
        else:
            return False

    def _compat_fetchall(self, rp, charset=None):
        return rp.fetchall()

    def _compat_fetchone(self, rp, charset=None):
        return rp.fetchone()

dialect = MySQLDialect_mysqlconnector
