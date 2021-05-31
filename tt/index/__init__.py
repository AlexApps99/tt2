import flask
from flask import Blueprint, render_template, redirect
import flask_login
from flask_login import login_required
from wtforms import BooleanField, PasswordField
from wtforms.fields.html5 import EmailField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, Email
from ..db import get_user

idx_page = Blueprint("index", __name__, template_folder="templates")


@idx_page.route('/')
def show():
    return render_template("base.html", n="Mapman")


@idx_page.route("/")
def hello_world():
    return render_template("error.html", n="Hello, World!")


class LoginForm(FlaskForm):
    email = EmailField('email', validators=[DataRequired(), Email()])
    password = PasswordField(
        'password',
        validators=[DataRequired(), Length(8, 100)]
    )
    remember_me = BooleanField('remember_me')


# use flash to put an error for wrong shiz
@idx_page.route("/login", methods=('GET', 'POST'))
def login():
    form = LoginForm()
    if form.validate_on_submit():
        u = get_user(form.email.data, form.password.data)
        if u is not None:
            flask_login.login_user(u, remember=form.remember_me.data)
            # TODO potential security risk right here
            next = flask.request.args.get('next')
            return redirect(next or '/')
    return render_template("login.html", form=form)


@idx_page.route("/logout")
@login_required
def logout():
    flask_login.logout_user()
    return redirect('/')


@idx_page.errorhandler(404)
def george_not_found(e):
    return render_template('error.html', n=404), 404
