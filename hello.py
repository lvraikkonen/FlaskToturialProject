#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask
from flask import request
from flask_script import Manager, Shell
# 动态生成url
from flask import url_for, session, redirect, flash
from flask import render_template

from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
import os

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY'] = 'DontTellAnyone'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64))
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)

manager.add_command("shell", Shell(make_context=make_shell_context))

class NameForm(FlaskForm):
    name = StringField("What's your name?", validators=[DataRequired()])
    submit = SubmitField('Submit')


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


@app.route('/hello_somebody', methods=['GET', 'POST'])
def hello_somebody():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            session['known'] = False
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('hello_somebody'))
    return render_template('userform_index.html', form=form, name=session.get('name'), known=session.get('known', False))


@app.route('/sum/<int:x>/<int:y>')
def sum_param(x, y):
    return "%d + %d = %d" % (x, y, x+y)


@app.route('/hello/')
@app.route('/hello/<user_name>')
def hello(user_name=None):
    if user_name is None:
        user_name = 'Stranger'
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


#with app.test_request_context():
#    print url_for('index')
#    print url_for('login')
#    print url_for('login', next='/')
#    print url_for('show_post', post_id=123)
#    print url_for('sum_param', x=1, y=2)
#    print url_for('hello', user_name='Claus')
#
#print app.url_map


if __name__ == '__main__':
    app.run()
