from flask import render_template, url_for, flash, redirect, request, Blueprint, session
from flask_login import login_user, current_user, logout_user, login_required
from Bookflix.users.forms import (RegistrationForm, LoginForm)
from Bookflix.models import User, Card
from Bookflix import bcrypt, db

users = Blueprint('users', __name__)



@users.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name=form.name.data, email=form.email.data, password=hashed_password, accountType=form.userType.data)
        card = Card(owner=user, number=form.number.data, security_number=form.securityNum.data, expiration_date=form.expDate.data)
        db.session.add(user)
        db.session.add(card)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)

@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    flash("primero"+str(current_user.is_authenticated), 'danger')
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data, force=True)
            flash("segundo"+str(current_user.is_authenticated), 'danger')
            next_page = request.args.get('next')
            return redirect(url_for('users.debug'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route("/debug")
def debug():
    return render_template('debug.html', current_user=current_user)