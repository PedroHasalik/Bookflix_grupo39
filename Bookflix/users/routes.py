from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from Bookflix.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm)
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
    form = LoginForm()
    #if current_user.is_authenticated:
    #    return redirect(url_for('main.home'))
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            #return redirect(next_page) if next_page else redirect(url_for('main.home'))
            return redirect(url_for('users.account'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    card=Card.query.filter_by(owner=current_user).first()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        current_user.name = form.name.data
        current_user.email = form.email.data
        current_user.password= hashed_password
        current_user.accountType= form.userType.data
        card.number= form.number.data
        card.security_number = form.securityNum.data
        card.expiration_date = form.expDate.data 
        db.session.commit()
        flash('Los datos de la cuenta se guardaron!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.name.data = current_user.name
        form.email.data = current_user.email
        form.password.data = current_user.password
        form.number.data = card.number
        form.userType.data = current_user.accountType
        form.securityNum.data = card.security_number
        form.expDate.data = card.expiration_date
    return render_template('update_user.html', title='Account', form=form)

@users.route("/debug")
def debug():
    return render_template('debug.html', current_user=current_user)