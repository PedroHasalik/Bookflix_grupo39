from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, SelectField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, ValidationError
from Bookflix.models import Genre, Publisher, Book

#CREATE FORMS
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

    picture = FileField('Imagen:', validators=[FileAllowed(['jpg', 'png'])])

    submit = SubmitField('Subir novedad')

#UPDATE FORMS

class GenreUpdateForm(FlaskForm):
    name = StringField('Nombre', validators= [ DataRequired()])
    current_id = IntegerField()
    submit = SubmitField('Confirmar')

    def validate_name(self, name):
        genre = Genre.query.get(self.current_id.data)
        if (genre.name != name.data):
            genre2 = Genre.query.filter_by(name=name.data).first()
            if (genre2):
                raise ValidationError('Ya existe otro genero con ese nombre.')

class PublisherUpdateForm(FlaskForm):
    name = StringField('Nombre', validators= [ DataRequired()])
    current_id = IntegerField()
    submit = SubmitField('Confirmar')

    def validate_name(self, name):
        publisher = Publisher.query.get(self.current_id.data)
        if (publisher.name != name.data):
            publisher2 = Publisher.query.filter_by(name=name.data).first()
            if publisher2:
                raise ValidationError('Ya existe una editorial con ese nombre.')

class BookUpdateForm(FlaskForm):
    title = StringField('Titulo', validators= [ DataRequired()])
    current_id = IntegerField()
    isbn = StringField('ISBN', validators= [ DataRequired()])
    author= SelectField('Autor', default='', coerce=int) #Las opciones son 'none' y todos los autores, se crea en la ruta
    genre= SelectField('Genero', default='', coerce=int)#Las opciones son 'none' y todos los generos, se crea en la ruta
    publisher= SelectField('Editorial', default='', coerce=int)#Las opciones son 'none' y todas las editoriales , se crea en la ruta
    
    def validate_isbn(self, isbn):
        book = Book.query.get(self.current_id.data)
        if (book.isbn != isbn.data):
            book2 = Book.query.filter_by(isbn=isbn.data).first()
            if book2:
                raise ValidationError('Ya existe un libro con ese ISBN.')
    submit = SubmitField('Confirmar')

class ConfirmDeleteForm(FlaskForm):
    submit = SubmitField('ELIMINAR')