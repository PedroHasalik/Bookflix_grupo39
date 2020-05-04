from flask import current_app
from Bookflix import db, login_manager
from flask_login import UserMixin
from datetime import datetime

class User(db.Model)
    id=db.Column(db.Integer, primary_key = True)
    email=db.Column(db.String(50),unique=True, nullable = False)
    password=db.Column(db.String(60), nullable = False)
    premium=db.Column(db.Boolean, nullable = False)
    name=db.Column(db.String(60), nullable = False)
    card=db.Relationship('Card', backref='owner', lazy = True)
    profiles=db.Relationship('Profiles', backref='owner', lazy = True )

class Profile(db.Model,UserMixin)
    id=db.Column(db.Integer, primary_key = True)
    name=db.Column(db.String(50),unique=True, nullable = False)
    image_file = db.Column(db.String(20), nullable = False, default='default.jpg')
    favourites=db.Relationship('Book',lazy = True)
    pending=db.Relationship('Book',lazy = True)
    doneReading=db.Relationship('Book',lazy = True)
    reviews=db.Relationship('Review', backref='writer',lazy = True)

class Card(db.Model)
    id=db.Column(db.Integer, primary_key = True)
    number=db.Column(db.Integer, nullable= False)
    expDate=db.Column(db.DateTime, nullable = False)
    securityNum=db.Column(db.Integer(3), nullable= False)
    ownerName= db.Column(db.String, nullable= False)

class Book(db.model)
    id=db.Column(db.Integer, primary_key = True)
    pdf_file= db.Column(db.String(20), nullable = False)
    image_file= db.Column(db.String(20), nullable = False)
    isTrending= db.Column(db.Boolean, nullable= False, default= False)
    author=db.Relationship('Author',lazy = True)
    genre=db.Relationship('Genre',lazy = True)
    reviews=db.Relationship('Review',lazy = True)
    publisher=db.Relationship('Publisher',lazy = True)

class Author(db.model)
    id=db.Column(db.Integer, primary_key = True)
    name=db.Column(db.String(20), nullable = False)

class Genre(db.model)
    id=db.Column(db.Integer, primary_key = True)
    name=db.Column(db.String(20), nullable = False)

class Publisher(db.model)
    id=db.Column(db.Integer, primary_key = True)
    name=db.Column(db.String(20), nullable = False)

class Review(db.model)
    id=db.Column(db.Integer, primary_key = True)
    score=db.Column(db.Integer, nullable= False)
    text=db.Column(db.Text, nullable= True)

