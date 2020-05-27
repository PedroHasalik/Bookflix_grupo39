from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, ValidationError
from Bookflix.models import Genre, Publisher, Book


class GenreForm(FlaskForm):
    name = StringField('Nombre', validators= [ DataRequired()])
    submit = SubmitField('Confirmar')

    def validate_name(self, name):
        genre = Genre.query.filter_by(name=name.data).first()
        if genre:
            raise ValidationError('Ya existe un genero con ese nombre.')

class AuthorForm(FlaskForm):
    name = StringField('Nombre', validators= [ DataRequired()])
    surname = StringField('Apellido', validators= [ DataRequired()])
    submit = SubmitField('Confirmar')

class PublisherForm(FlaskForm):
    name = StringField('Nombre', validators= [ DataRequired()])
    submit = SubmitField('Confirmar')

    def validate_name(self, name):
        publisher = Publisher.query.filter_by(name=name.data).first()
        if publisher:
            raise ValidationError('Ya existe una editorial con ese nombre.')

class BookForm(FlaskForm):
    title = StringField('Titulo', validators= [ DataRequired()])
    isbn = StringField('ISBN', validators= [ DataRequired()])
    author= SelectField('Autor', default='', coerce=int) #Las opciones son 'none' y todos los autores, se crea en la ruta
    genre= SelectField('Genero', default='', coerce=int)#Las opciones son 'none' y todos los generos, se crea en la ruta
    publisher= SelectField('Editorial', default='', coerce=int)#Las opciones son 'none' y todas las editoriales , se crea en la ruta
    
    def validate_isbn(self, isbn):
        book = Book.query.filter_by(isbn=isbn.data).first()
        if book:
            raise ValidationError('Ya existe un libro con ese ISBN.')
    submit = SubmitField('Confirmar')

class NewsForm(FlaskForm):
    title = StringField('Título:', validators=[DataRequired()])
    content = TextAreaField('Contenido:', validators=[DataRequired()])

    submit = SubmitField('Subir novedad')