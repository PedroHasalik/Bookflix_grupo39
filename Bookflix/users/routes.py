from flask import render_template, url_for, flash, redirect, request, Blueprint
from Bookflix.users.forms import (RegistrationForm, LoginForm)

users = Blueprint('users', __name__)



@users.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html', title= 'Register')

@users.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html', title= 'Login')