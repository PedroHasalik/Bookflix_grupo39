from flask import current_app, session
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
    date_created= db.Column(db.DateTime, nullable = False, default=datetime.utcnow)

    card=db.relationship('Card', backref='owner', lazy = True)
    profiles=db.relationship('Profile', backref='owner', lazy = True )

    def current_profile(self):
        return Profile.query.get(session['_current_profile_id'])


class Profile(db.Model):
    id=db.Column(db.Integer, primary_key = True)
    owner_id= db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

    name=db.Column(db.String(50),unique=True, nullable = False)
    image_file = db.Column(db.String(20), nullable = False, default='default.png')
    navigationHistory = db.relationship('NavigationHistoryEntry', lazy = True, backref='owner')
    favourites=db.relationship('Book', secondary = 'profile_favorites' ) #libros favoritos
    doneReading=db.relationship('Book', secondary = 'profile_done_reading') #libros leidos
    reviews=db.relationship('Review', backref='writer',lazy = True)

    def markAsRead(self, theBook):
        if not (theBook in self.doneReading):
            self.doneReading.append(theBook)
            db.session.commit()
    
    def unread(self, theBook):
        if (theBook in self.doneReading):
            self.doneReading.remove(theBook)
            db.session.commit()

class NavigationHistoryEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'), nullable = False)
    item_id = db.Column(db.Integer, nullable = False) #id del libro o capitulo a guardar en el historial
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    entryType = db.Column(db.String, nullable = False) #Book o Chapter
    entryName = db.Column(db.String, nullable = False) #El nombre del libro o el numero y nombre del capitulo

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

    def full_name(self):
        fullName = self.name+' '+self.surname
        return fullName

class Genre(db.Model):
    id=db.Column(db.Integer, primary_key = True)
    name=db.Column(db.String(20), nullable = False)

    books = db.relationship('Book', backref='theGenre', lazy = True)

    def full_name(self):
        return self.name

class Publisher(db.Model):
    id=db.Column(db.Integer, primary_key = True)
    name=db.Column(db.String(20), nullable = False)

    books = db.relationship('Book', backref='thePublisher', lazy = True)

    def full_name(self):
        return self.name

class Book(db.Model):
    id=db.Column(db.Integer, primary_key = True)

    author_id= db.Column(db.Integer, db.ForeignKey('author.id'), nullable = True)
    genre_id= db.Column(db.Integer, db.ForeignKey('genre.id'), nullable = True)
    publisher_id= db.Column(db.Integer, db.ForeignKey('publisher.id'), nullable = True)

    title= db.Column(db.String, nullable = False)
    image_file= db.Column(db.String(20), nullable = False, default='default.png')
    isbn= db.Column(db.String, nullable = False)
    public = db.Column(db.Boolean, nullable = False, default=False)


    reviews=db.relationship('Review',lazy = True, backref='book')
    chapters=db.relationship('Chapter', lazy = True, backref='book')

    def full_name(self):
        return self.title

class Chapter(db.Model):
    id=db.Column(db.Integer, primary_key = True)
    book_id= db.Column(db.Integer, db.ForeignKey('book.id',  ondelete='CASCADE'), nullable = False,)

    chapterNumber = db.Column(db.Integer, nullable = False)
    chapterTitle = db.Column(db.String)
    pdf_file = db.Column(db.String, nullable = False)

    def full_name(self):
        return ('Capitulo '+str(self.chapterNumber)+' - '+self.chapterTitle)


class Review(db.Model):
    id=db.Column(db.Integer, primary_key = True)
    writer_id= db.Column(db.Integer, db.ForeignKey('profile.id',  ondelete='CASCADE'), nullable = False)
    book_id= db.Column(db.Integer, db.ForeignKey('book.id',  ondelete='CASCADE'), nullable = False)

    score=db.Column(db.Integer, nullable= False)
    text=db.Column(db.Text, nullable= True)


class News(db.Model):
    id =db.Column(db.Integer, primary_key=True)
    
    title = db.Column(db.String(40), nullable= False)
    content = db.Column(db.String(140), nullable= False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    book_id = db.Column(db.Integer, nullable=True) #si la novedad es un trailer, book_id es la id del book para el cual es trailer. Sino, book_id es 0

    def full_name(self):
        return self.title



#MANY-TO-MANY RELATIONSHIP HELPERS

class ProfileFavorites(db.Model):
    __tablename__= 'profile_favorites'
    id = db.Column(db.Integer(), primary_key=True)
    profile_id = db.Column(db.Integer(), db.ForeignKey('profile.id', ondelete='CASCADE'))
    book_id = db.Column(db.Integer(), db.ForeignKey('book.id', ondelete='CASCADE'))

class ProfileDoneReading(db.Model):
    __tablename__= 'profile_done_reading'
    id = db.Column(db.Integer(), primary_key=True)
    profile_id = db.Column(db.Integer(), db.ForeignKey('profile.id', ondelete='CASCADE'))
    book_id = db.Column(db.Integer(), db.ForeignKey('book.id', ondelete='CASCADE'))





