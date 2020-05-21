from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField
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
    author= SelectField('Autor', default='', coerce=int) #Las opciones son 'none' y todos los autores, se crea en la ruta
    genre= SelectField('Genero', default='', coerce=int)#Las opciones son 'none' y todos los generos, se crea en la ruta
    publisher= SelectField('Editorial', default='', coerce=int)#Las opciones son 'none' y todas las editoriales , se crea en la ruta
    
    submit = SubmitField('Crear')

class NewsForm(FlaskForm):
    title = StringField('Título:', validators=[DataRequired()])
    content = TextAreaField('Contenido:', validators=[DataRequired()])

    submit = SubmitField('Subir novedad')