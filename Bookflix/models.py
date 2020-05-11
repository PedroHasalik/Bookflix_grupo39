from flask import current_app
from Bookflix import db, login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
        return Profile.query.get(int(user_id))

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email=db.Column(db.String(50),unique=True, nullable = False)
    password=db.Column(db.String(60), nullable = False)
    accountType=db.Column(db.String, nullable = False) #valores posibles: admin, premium, normal
    name=db.Column(db.String(60), nullable = False)
    card=db.relationship('Card', backref='owner', lazy = True)
    profiles=db.relationship('Profiles', backref='owner', lazy = True )


class Profile(db.Model,UserMixin):
    id=db.Column(db.Integer, primary_key = True)
    name=db.Column(db.String(50),unique=True, nullable = False)
    image_file = db.Column(db.String(20), nullable = False, default='default.jpg')
    favourites=db.relationship('Book',lazy = True)
    pending=db.relationship('Book',lazy = True)
    doneReading=db.relationship('Book',lazy = True)
    reviews=db.relationship('Review', backref='writer',lazy = True)

class Card(db.Model):
    id=db.Column(db.Integer, primary_key = True)
    number=db.Column(db.Integer, nullable= False)
    expDate=db.Column(db.DateTime, nullable = False)
    securityNum=db.Column(db.Integer, nullable= False)
    ownerName= db.Column(db.String, nullable= False)

class Book(db.Model):
    id=db.Column(db.Integer, primary_key = True)
    pdf_file= db.Column(db.String(20), nullable = False)
    image_file= db.Column(db.String(20), nullable = False)
    isTrending= db.Column(db.Boolean, nullable= False, default= False)
    author=db.relationship('Author',lazy = True)
    genre=db.relationship('Genre',lazy = True)
    reviews=db.relationship('Review',lazy = True)
    publisher=db.relationship('Publisher',lazy = True)

class Author(db.Model):
    id=db.Column(db.Integer, primary_key = True)
    name=db.Column(db.String(20), nullable = False)

class Genre(db.Model):
    id=db.Column(db.Integer, primary_key = True)
    name=db.Column(db.String(20), nullable = False)

class Publisher(db.Model):
    id=db.Column(db.Integer, primary_key = True)
    name=db.Column(db.String(20), nullable = False)

class Review(db.Model):
    id=db.Column(db.Integer, primary_key = True)
    score=db.Column(db.Integer, nullable= False)
    text=db.Column(db.Text, nullable= True)

