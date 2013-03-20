"""
urls.py

URL dispatch route mappings and error handlers

"""
from flask import render_template

from application import app
from application import views


## URL dispatch rules
# App Engine warm up handler
# See http://code.google.com/appengine/docs/python/config/appconfig.html#Warming_Requests
app.add_url_rule('/_ah/warmup', 'warmup', view_func=views.warmup)

# Home page
app.add_url_rule('/',                 'home', view_func=views.index, methods=['GET', 'POST'])
app.add_url_rule('/index',            'home', view_func=views.index, methods=['GET', 'POST'])
app.add_url_rule('/index/<int:page>', 'home', view_func=views.index, methods=['GET', 'POST'])

# Login
app.add_url_rule('/login', 'login', view_func=views.login, methods=['GET', 'POST'])

# Logout
app.add_url_rule('/logout', 'logout', view_func=views.logout, methods=['GET', 'POST'])

# User
app.add_url_rule('/user/<nickname>', 'view user', view_func=views.user)

# Edit user
app.add_url_rule('/edit', 'admin_only', view_func=views.admin_only)

# Edit an example
app.add_url_rule('/examples/<int:example_id>/edit', 'edit_example', view_func=views.edit_example, methods=['GET', 'POST'])

# Delete an example
app.add_url_rule('/examples/<int:example_id>/delete', view_func=views.delete_example, methods=['POST'])


## Error handlers
# Handle 404 errors
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Handle 500 errors
@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

