from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired


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
    author= SelectField('Autor', default='') #Las opciones son 'none' y todos los autores, se crea en la ruta
    genre= SelectField('Genero', default='')#Las opciones son 'none' y todos los generos, se crea en la ruta
    publisher= SelectField('Editorial', default='')#Las opciones son 'none' y todas las editoriales , se crea en la ruta

    #author= SelectField('Autor', choices=([(None, 'None')]+ [(each.id, each.name()) for each in Author.query.all()]), default='') #Las opciones son 'none' y todos los autores
    #genre= SelectField('Genero', choices=([(None, 'None')]+ [(each.id, each.name()) for each in Genre.query.all()]), default='')
    #publisher= SelectField('Editorial', choices=([(None, 'None')]+ [(each.id, each.name()) for each in Publisher.query.all()]), default='')
    submit = SubmitField('Crear')