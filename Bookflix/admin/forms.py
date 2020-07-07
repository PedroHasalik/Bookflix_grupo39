from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms.fields.html5 import DateField
from wtforms import StringField, SubmitField, SelectField, TextAreaField, IntegerField, BooleanField
from wtforms.validators import DataRequired, ValidationError
from Bookflix.models import Genre, Publisher, Book, Chapter

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
    image_file = FileField('Imagen', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    
    def validate_isbn(self, isbn):
        book = Book.query.filter_by(isbn=isbn.data).first()
        if book:
            raise ValidationError('Ya existe un libro con ese ISBN.')
    submit = SubmitField('Confirmar')

class ChapterForm(FlaskForm):
    number = IntegerField('Numero', validators= [ DataRequired()])
    title = StringField('Titulo')
    book_id = IntegerField( validators= [ DataRequired()])
    pdf_file = FileField('Archivo PDF', validators=[DataRequired(), FileAllowed(['pdf'])])

    submit = SubmitField('Confirmar')

    def validate_number(self, number):
        chapter = Chapter.query.filter((Chapter.book_id == self.book_id.data) & (Chapter.chapterNumber == number.data)).first()
        if chapter:
            raise ValidationError('Ya existe un capitulo con ese numero en este libro.')

class NewsForm(FlaskForm):
    title = StringField('Título:', validators=[DataRequired()])
    content = TextAreaField('Contenido:', validators=[DataRequired()])

    picture = FileField('Imagen:', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])

    book = SelectField('Es trailer de:', default='', coerce=int) #Las opciones son 'none' y todos los libros, se crea en la ruta

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
    image_file = FileField('Imagen', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    public =  BooleanField('¿Visible para los usuarios?')
    
    def validate_isbn(self, isbn):
        book = Book.query.get(self.current_id.data)
        if (book.isbn != isbn.data):
            book2 = Book.query.filter_by(isbn=isbn.data).first()
            if book2:
                raise ValidationError('Ya existe un libro con ese ISBN.')
    submit = SubmitField('Confirmar')

class ChapterUpdateForm(FlaskForm):
    number = IntegerField('Numero', validators= [ DataRequired()])
    current_id = IntegerField()
    title = StringField('Titulo')
    book_id = IntegerField()
    pdf_file = FileField('Archivo PDF', validators=[FileAllowed(['pdf'])])

    submit = SubmitField('Confirmar')

    def validate_number(self, number):
        chapter = Chapter.query.get(self.current_id.data)
        if (chapter.chapterNumber != number.data):
            chapter2 = Chapter.query.filter((Chapter.book_id == self.book_id.data) & (Chapter.chapterNumber == number.data)).first()
            if chapter2:
                raise ValidationError('Ya existe un capitulo con ese numero en este libro.')

class ConfirmDeleteForm(FlaskForm):
    submit = SubmitField('ELIMINAR')

class StatDateForm(FlaskForm):
    fromDate = DateField('DESDE' ,format='%Y-%m-%d' ,validators=[DataRequired()])
    toDate = DateField('HASTA' ,format='%Y-%m-%d' ,validators=[DataRequired()])
    estadisticaDe = SelectField('Estadistica de', choices=[('admin.admin_stats_book', 'Libros leidos'), ('admin.admin_stats_accounts', 'Cuentas Creadas')])

    submit = SubmitField('Ver estadisticas')

    def validate_toDate(self, toDate):
        fromDate = self.fromDate
        if (toDate.data < fromDate.data):
            raise ValidationError("La fecha 'DESDE' tiene que ser antes o igual que la fecha 'HASTA'.")