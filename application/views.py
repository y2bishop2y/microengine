"""
views.py

URL route handlers

Note that any handler params must match the URL route params.
For example the *say_hello* handler, handling the URL route '/hello/<username>',
  must be passed *username* as the argument.

"""
from google.appengine.api import users
from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError

from lib.flask import request, render_template, flash, url_for
from lib.flask_cache import Cache



from application import app, db, lm, oid, babel

from decorators import login_required, admin_required


# Flask-Cache (configured to use App Engine Memcache API)
cache = Cache(app)




@lm.user_loader
def load_user(id):
    return User.query.get(int(id))



@app.route('/', methods = ['GET', 'POST'])
@app.route('/index', methods = ['GET', 'POST'])
@app.route('/index/<int:page>', methods = ['GET', 'POST'])
@login_required
def index(page = 1):

    form = PostForm()

    if form.validate_on_submit():

        language = guessLanguage(form.post.data)
        if language == 'UNKNOWN' or len(lanaguage) >5:
            language = ''

        post = Post(body = form.post.data,
                    timestamp = datetime.utcnow(),
                    author = g.user,
                    language = language)

        db.session.add(post)
        db.session.commit()

        flash(gettext('Your post is now live!'))
        return redirect(url_for('index'))


    posts = g.user.followed_posts().paginate(page, POST_PER_PAGE, False)


    return render_template("index.html",
                           title = "Home",
                           form  = form,
                           posts = posts)



@app.route('/login', methods = ['GET', 'POST'])
@oid.loginhandler
def login():


    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))

    form = LoginForm()

    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data

        return oid.try_login(form.openid.data, ask_for = ['nickname', 'email'])



    return render_template('login.html',
                           title = 'Sign In',
                           form = form,
                           providers = app.config['OPENID_PROVIDERS'])



@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.before_request
def before_request():
    g.user = current_user

    if g.user.is_authenticated():
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()
        g.search_form = SearchForm()

    g.locale = get_locale()

@oid.after_login
def after_login(resp):

    if resp.email is None or resp.email == "":
        flash(gettext('Invalid login. Please try again.'))
        redirect(url_for('login'))


    user = User.query.filter_by(email = resp.email).first()

    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]

        nickname = User.make_valid_nickname(nickname)
        nickname = User.make_unique_nickname(nickname)
        user = User(nickname = nickname, email = resp.email, role = ROLE_USER)

        db.session.add(user)
        db.session.commit()

        # make the user follow him/herself
        db.session.add(user.follow(user))
        db.session.commit()

    remember_me = False

    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)

    login_user(user, remember = remember_me)
    return redirect(request.args.get('next') or url_for('index'))


@app.route('/user/<nickname>')
@app.route('/user/<nickname>/<int:page>')
@login_required
def user(nickname, page = 1):

    user = User.query.filter_by(nickname = nickname).first()

    if user == None:
        flash(gettext('User  %(nickname)s  not found.', nickname = nickname ))
        return redirect(url_for('index'))


    posts = user.posts.paginate(page, POST_PER_PAGE, False)
    return render_template('user.html',
                           user  = user,
                           posts = posts)


@app.route('/edit', methods = ['GET', 'POST'])
@login_required
def edit():

    form = EditForm(g.user.nickname)

    if form.validate_on_submit():
        g.user.nickname = form.nickname.data
        g.user.about_me = form.about_me.data

        db.session.add(g.user)
        db.session.commit()

        flash(gettext('Your changes have been saved.'))
        return redirect(url_for('edit'))

    else:
        form.nickname.data = g.user.nickname
        form.about_me.data = g.user.about_me

    return render_template('edit.html', form = form)



@app.errorhandler(404)
def internal_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()

    return render_template('500.html'), 500



@app.route('/follow/<nickname>')
def follow(nickname):

    user = User.query.filter_by(nickname = nickname).first()

    if user == None:
        flash(gettext('User %(nickname)s not found.', nickname = nickname ))
        return redirect(url_for('index'))

    if user == g.user:
        flash(gettext('You can\'t follow yourself'))
        return redirect(url_for('user', nickname = nickname))

    u = g.user.follow(user)
    if u is None:
        flash(gettext('Cannont follow %(nickname)s .', nickname = nickname))
        return redirect(url_for('user', nickname = nickname))

    db.session.add(u)
    db.session.commit()
    flash(gettext('You are now following %(nickname)s !', nickname = nickname))

    follower_notifaction(user, g.user)
    return redirect(url_for('user', nickname = nickname))


@app.route('/unfollow/<nickname>')
def unfollow(nickname):

    user = User.query.filter_by(nickname = nickname).first()

    if user == None:
        flash(gettext('User %(nickname)s not found', nickname = nickname))
        return redirect(url_for('index'))

    if user == g.user:
        flash(gettext('You can\'t unfollow yourself!'))
        return redirect(url_for('user', nickname = nickname))

    u = g.user.unfollow(user)

    if u is None:
        flash(gettext('Cannot unfollow %(nickname)s .', nickname = nickname))
        return redirect(url_for('user', nickname = nickname))

    db.session.add(u)
    db.session.commit()

    flash(gettext('You have stopped following %(nickname)s .', nickname = nickname))
    return redirect(url_for('user', nickname = nickname))


@app.route('/search', methods = ['POST'])
@login_required
def search():

    if not g.search_form.validate_on_submit():
        return redirect(url_for('index'))

    return redirect(url_for('search_results', query = g.search_form.search.data))

@app.route('/search_reulsts/<query>')
@login_required
def search_results(query):
    results = Post.query.whoosh_search(query, MAX_SEARCH_RESULTS).all()

    return render_template('search_results.html',
                           query = query,
                           results = results)


@babel.localeselector
def get_locale():
    # return request.accept_languages.best_match(LANGUAGES.keys())
    return 'es'



@app.route('/translate', methods = ['POST'])
@login_required
def translate():

    return jsonify({
    'text' : microsoft_translate(
        request.form['text'],
        request.form['sourceLang'],
        request.form['destLang']
    )
    })


@app.route('/delete/<int:id>')
@login_required
def delete(id):

    post = Post.query.get(id)

    if post == None:
        flash(gettext('Post not found'))

        return redirect(url_for('index'))


    if post.author.id != g.user.id:
        flash(gettext('You cannot delete this post.'))
        return redirect(url_for('index'))

    db.session.delete(post)
    db.session.commit()

    flash(gettext('Your post has been delete'))

    return redirect(url_for('index'))

