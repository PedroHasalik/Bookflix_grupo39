from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from Bookflix.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm, ProfileRegistrationForm, ProfileUpdateForm)
from Bookflix.models import User, Card, Profile
from Bookflix import bcrypt, db
from Bookflix.users.utils import save_picture
from Bookflix.decorators import full_login_required

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

@users.route('/', methods=['GET', 'POST'])
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
            return redirect(url_for('main.profiles'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('users.login'))


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
        return redirect(url_for('main.home'))
    elif request.method == 'GET':
        form.name.data = current_user.name
        form.email.data = current_user.email
        form.password.data = current_user.password
        form.number.data = card.number
        form.userType.data = current_user.accountType
        form.securityNum.data = card.security_number
        form.expDate.data = card.expiration_date
    return render_template('update_user.html', title='Account', form=form)

@users.route("/register_profile", methods=['GET', 'POST'])
@login_required
def register_profile():
    form = ProfileRegistrationForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
        else:
            picture_file = "default.png"
        profile =Profile (owner=current_user, name=form.name.data, image_file=picture_file)
        db.session.add(profile)
        db.session.commit()
        return redirect(url_for('main.profiles'))
    return render_template('register_profile.html', form=form, profile =  current_user.current_profile(), title= 'Crear perfil', legend= 'Crear perfil')

@users.route("/update_profile", methods=['GET', 'POST'])
@full_login_required()
def update_profile():
    form = ProfileUpdateForm()
    if form.validate_on_submit():
        current_user.current_profile().name = form.name.data
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
        else:
            picture_file = "default.png"
        current_user.current_profile().image_file = picture_file
        db.session.commit()
        flash('Los datos de la cuenta se guardaron!', 'success')
        return redirect(url_for('main.home'))
    elif request.method == 'GET':
        form.name.data = current_user.current_profile().name
    return render_template('update_profile.html', form=form, profile =  current_user.current_profile(), title= 'Editar perfil', legend= 'Editar perfil')

@users.route("/set_profile/<int:id>")
@login_required
def set_profile(id):
    profile=Profile.query.get_or_404(id)
    if(profile.owner == current_user):
        current_user.current_profile_id = id
    db.session.commit()
    return redirect (url_for("main.home"))


@users.route("/debug")
def debug():
    return render_template('debug.html', current_user=current_user)