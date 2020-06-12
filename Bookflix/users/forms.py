from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, RadioField
from wtforms.fields.html5 import DateField  
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from Bookflix.models import User


class RegistrationForm(FlaskForm):
    name = StringField('Name',validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',validators=[DataRequired(), Email()])
    number = IntegerField('CardNumber', validators=[DataRequired()])
    expDate = DateField('ExpDate' ,format='%Y-%m-%d' ,validators=[DataRequired()])
    securityNum =  IntegerField( 'SecurityNumber' , validators=[DataRequired()])                                           
    password = PasswordField('Password', validators=[DataRequired()])
    userType =  RadioField('UserType', choices=[('Premium','Premium'),('Normal','Normal')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('La direccion de mail esta en uso. Por favor seleccione otra.')

class LoginForm(FlaskForm):
    email = StringField('email',validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    name = StringField('Name',validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',validators=[DataRequired(), Email()])
    number = IntegerField('CardNumber', validators=[DataRequired()])
    expDate = DateField('ExpDate' ,format='%Y-%m-%d' ,validators=[DataRequired()])
    securityNum =  IntegerField( 'SecurityNumber' , validators=[DataRequired()])                                           
    password = PasswordField('Password', validators=[DataRequired()])
    userType =  RadioField('UserType', choices=[('Premium','Premium'),('Normal','Normal')])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')

class ProfileRegistrationForm(FlaskForm):
    name = StringField('Name',validators=[DataRequired(), Length(min=2, max=20)])
    picture = FileField('Upload Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Create')

class ProfileUpdateForm(FlaskForm):
    name = StringField('Name',validators=[DataRequired(), Length(min=2, max=20)])
    picture = FileField('Upload Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')


    