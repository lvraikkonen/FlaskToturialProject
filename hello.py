#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask
from flask import request
# 动态生成url
from flask import url_for
from flask import render_template

from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime

app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)


@app.route('/')
def index():
    user_agent = request.headers.get('User-Agent')
    return render_template('index.html', user_agent=user_agent, current_time=datetime.utcnow())


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return do_the_login()
    else:
        return show_the_login_form()


def do_the_login():
    return "Logging..."


def show_the_login_form():
    return "Showing login form..."


@app.route('/sum/<int:x>/<int:y>')
def sum_param(x, y):
    return "%d + %d = %d" % (x, y, x+y)


@app.route('/hello/')
@app.route('/hello/<user_name>')
def hello(user_name = None):
    return render_template('user.html', name=user_name)


@app.route('/post/<int:post_id>')
def show_post(post_id):
    return render_template('post.html', post_id=post_id)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


with app.test_request_context():
    print url_for('index')
    print url_for('login')
    print url_for('login', next='/')
    print url_for('show_post', post_id=123)
    print url_for('sum_param', x=1, y=2)
    print url_for('hello', user_name='Claus')

print app.url_map


if __name__ == '__main__':
    app.run()
