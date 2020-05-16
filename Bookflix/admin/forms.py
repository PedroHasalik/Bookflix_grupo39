from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
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
    submit = SubmitField('Crear')