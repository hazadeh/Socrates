from flask import render_template, flash, redirect, url_for, request, session, g
from flask_login import current_user, login_user, logout_user
from app import app
from app.forms import LoginForm,  SearchForm
from app.models import Article
import json
import os


@app.route('/')
@app.route('/index')
def index():
    user = {'username': session['username']
            if 'username' in session else 'Guest'}
    return render_template('index.html', title='Socrates', user=user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    user = {'username': session['username']
            if 'username' in session else 'Guest'}
    form = LoginForm()
    if form.validate_on_submit():
        # this makes u and p 'azadeh' MUST BE UPDATED
        if form.username.data is None or form.username.data not in ['azadeh'] or form.username.data != form.password.data:
            flash('Invalid username or password')
            return redirect(url_for('login'))
        session['username'] = form.username.data
        session['state'] = '0'
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form, user=user)


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


@app.before_request
def before_request():
    if 'username' in session and session['username']:
        g.search_form = SearchForm()


@app.route('/reset')
def reset():
    user = {'username': session['username']}
    session['state'] = '0'
    session['seen'] = ''
    return render_template('search.html', title=('Search'), article=[], user=user, sysout="Let's start...\nQ1: Name a digital world issue that interests you and why it interests you?"
                                                                                          "\nYou can be as descriptive as you wish. "
                                                                                          "There is no word limit. You can provide suggestive words, write in note form, or write full sentences.s")

# @app.route('/upvote')
# def upvote():
#     request.args.get('id')
#     articles = json.loads(session['articles'])
#     sysout = session['sysout']
#     return render_template('search.html', title=('Search'), articles=articles, user=session['username'], sysout=sysout)


@app.route('/search')
def search():
    if 'username' not in session or session['username'] is None:
        redirect(url_for('login'))
    user = {'username': session['username']}

    submit = request.args.get('submit')

    if('seen' not in session or 'state' not in session):
        session['state'] = '0'
        session['seen'] = ''

    if submit == 'Refresh':
        user = {'username': session['username']}
        session['state'] = '0'
        session['seen'] = ''
        if os.path.exists(os.path.join(os.getcwd(), 'app/static/wordcloud.png')):
            os.remove(os.path.join(os.getcwd(), 'app/static/wordcloud.png'))

        return render_template('search.html', title=('Search'), article=[], user=user,
                               sysout="Let's start...\nQ1: Name a digital world issue that interests you and why it interests you?"
                                      "\nYou can be as descriptive as you wish. "
                                      "There is no word limit. You can provide suggestive words, write in note form, or write full sentences.")

    articles = []
    articlemodel = Article()

    state = session['state']
    if submit == 'Rephrase':
        state = str(int(session['state']) - 1)

    articles, state, sysout = articlemodel.search(query=g.search_form.q.data,
                                                  state=state, seen=session['seen'])

    session['state'] = state
    if state == 0:
        session['seen'] = ''
    elif int(state) % 2 == 0:  # for every other search (state is even), clear seen from session and append all current article ids
        seen = ''
        for artcl in articles:
            seen += '"' + artcl['id'] + '",'
        session['seen'] = session['seen'] + seen

    return render_template('search.html', title=('Search'), articles=articles, user=user, sysout=sysout, rephrase=(int(state) % 2 == 0))
