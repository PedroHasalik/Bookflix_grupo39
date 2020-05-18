from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
from bookflix.models import Author, Genre, Publisher


class GenreForm(FlaskForm):
    name = StringField('Nombre', validators= [ DataRequired()])
    submit = SubmitField('Crear')

class AuthorForm(FlaskForm):
    name = StringField('Nombre', validators= [ DataRequired()])
    surname = StringField('Apellido', validators= [ DataRequired()])
    submit = SubmitField('Crear')

class PublisherForm(FlaskForm):
    name = StringField('Nombre', validators= [ DataRequired()])
    submit = SubmitField('Crear')

class BookForm(FlaskForm):
    title = StringField('Titulo', validators= [ DataRequired()])
    author= SelectField('Autor', choices=([(None, 'None')]+ [(each.id, each.name()) for each in Author.query.all()]), default='') #Las opciones son 'none' y todos los autores
    genre= SelectField('Genero', choices=([(None, 'None')]+ [(each.id, each.name()) for each in Genre.query.all()]), default='')
    publisher= SelectField('Editorial', choices=([(None, 'None')]+ [(each.id, each.name()) for each in Publisher.query.all()]), default='')
    submit = SubmitField('Crear')