from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class GenreForm(FlaskForm):
    name = StringField('Title', validators= [ DataRequired()])
    submit = SubmitField('Crear')

class AuthorForm(FlaskForm):
    name = StringField('Title', validators= [ DataRequired()])
    submit = SubmitField('Crear')

class PublisherForm(FlaskForm):
    name = StringField('Title', validators= [ DataRequired()])
    submit = SubmitField('Crear')

class BookForm(FlaskForm):
    title = StringField('Title', validators= [ DataRequired()])
    submit = SubmitField('Crear')