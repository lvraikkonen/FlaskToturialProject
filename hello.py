#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask
from flask import request
# 动态生成url
from flask import url_for
from flask import render_template

app = Flask(__name__)


@app.route('/')
def index():
    user_agent = request.headers.get('User-Agent')
    return "<h1>Index Page</h1>Hello World!\n<p>Your browser is %s</p>" % user_agent


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


@app.route('/post/<int:post_id>')
def show_post(post_id):
    return "Post %d" % post_id


@app.route('/sum/<int:x>/<int:y>')
def sum_param(x, y):
    return "%d + %d = %d" % (x, y, x+y)


@app.route('/hello/')
@app.route('/hello/<user_name>')
def hello(user_name = None):
    return render_template('hello_user.html', name=user_name)


with app.test_request_context():
    print url_for('index')
    print url_for('login')
    print url_for('login', next='/')
    print url_for('show_post', post_id=123)
    print url_for('sum_param', x=1, y=2)

print app.url_map


if __name__ == '__main__':
    app.run(debug=True)
