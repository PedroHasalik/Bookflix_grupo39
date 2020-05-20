from flask import current_app
from Bookflix import db, login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
        return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    email=db.Column(db.String(50),unique=True, nullable = False)
    password=db.Column(db.String(60), nullable = False)
    accountType=db.Column(db.String, nullable = False) #valores posibles: 'Admin', 'Premium', 'Normal'
    name=db.Column(db.String(60), nullable = False)
    current_profile_id=db.Column(db.Integer, nullable = True, default = None) #Es un id de Profile
    card=db.relationship('Card', backref='owner', lazy = True)
    profiles=db.relationship('Profile', backref='owner', lazy = True )

    def current_profile():
        return Profile.query.get(current_profile_id)


class Profile(db.Model):
    id=db.Column(db.Integer, primary_key = True)
    owner_id= db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    
    name=db.Column(db.String(50),unique=True, nullable = False)
    image_file = db.Column(db.String(20), nullable = False, default='default.jpg')

    #favourites=db.relationship('Book',lazy = True) VA A SER UN QUILOMBO IMPLEMENTAR ESTO. NOTA: probablemente se solucione implementandolo como many-to-many
    #pending=db.relationship('Book',lazy = True)
    #doneReading=db.relationship('Book',lazy = True)
    #reviews=db.relationship('Review', backref='writer',lazy = True)

class Card(db.Model):
    id=db.Column(db.Integer, primary_key = True)
    owner_id= db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    number = db.Column(db.Integer, nullable = False)
    security_number = db.Column(db.Integer, nullable = False)
    expiration_date = db.Column(db.DateTime, nullable = False)


class Author(db.Model):
    id=db.Column(db.Integer, primary_key = True)
    name=db.Column(db.String(20), nullable = False) #Nombre
    surname= db.Column(db.String(20)) #Apellido

    books = db.relationship('Book', backref='theAuthor', lazy = True)

    def name():
        fullName = name+' '+surname
        return fullName

class Genre(db.Model):
    id=db.Column(db.Integer, primary_key = True)
    name=db.Column(db.String(20), nullable = False)

    books = db.relationship('Book', backref='theGenre', lazy = True)

    def name():
        return name

class Publisher(db.Model):
    id=db.Column(db.Integer, primary_key = True)
    name=db.Column(db.String(20), nullable = False)

    books = db.relationship('Book', backref='thePublisher', lazy = True)

    def name():
        return name

class Book(db.Model):
    id=db.Column(db.Integer, primary_key = True)

    author_id= db.Column(db.Integer, db.ForeignKey('author.id'), nullable = True)
    genre_id= db.Column(db.Integer, db.ForeignKey('genre.id'), nullable = True)
    publisher_id= db.Column(db.Integer, db.ForeignKey('publisher.id'), nullable = True)

    title= db.Column(db.String, nullable = False)
    image_file= db.Column(db.String(20), nullable = False, default='default.jpg')


    #reviews=db.relationship('Review',lazy = True)
    chapters=db.relationship('Chapter', lazy = True, backref='book')

    def name():
        return title

class Chapter(db.Model):
    id=db.Column(db.Integer, primary_key = True)
    book_id= db.Column(db.Integer, db.ForeignKey('book.id'), nullable = False)

    chapterNumber = db.Column(db.Integer, nullable = False)
    chapterTitle = db.Column(db.String)
    pdf_file = db.Column(db.String, nullable = False)

'''
class Review(db.Model):
    id=db.Column(db.Integer, primary_key = True)
    author_id= db.Column(db.Integer, db.ForeignKey('profile.id'), nullable = False)
    book_id= db.Column(db.Integer, db.ForeignKey('book.id'), nullable = False)

    score=db.Column(db.Integer, nullable= False)
    text=db.Column(db.Text, nullable= True)
'''

class News(db.Model):
    id =db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40), nullable= False)
    content = db.Column(db.String(140), nullable= False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    image_file =  image_file = db.Column(db.String(20), nullable=False, default='default.jpg')

    def name():
        return title



