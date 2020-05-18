from flask import render_template, request, Blueprint
from bookflix.decorators import roles_required
from bookflix.models import Book, Author, Genre, Publisher, News
from bookflix.admin.forms import GenreForm, AuthorForm, PublisherForm, BookForm

admin = Blueprint('admin', __name__)


#        <a class="btn btn-outline-info" href="{{ url_for('admin.genres') }}">Generos</a>
#        <a class="btn btn-outline-info" href="{{ url_for('admin.authors') }}">Autores</a>
#        <a class="btn btn-outline-info" href="{{ url_for('admin.publishers') }}">Editoriales</a>
#        <a class="btn btn-outline-info" href="{{ url_for('admin.books') }}">Libros</a>
#        <a class="btn btn-outline-info" href="{{ url_for('admin.news') }}">Novedades</a>

@admin.route("/admin")
@admin_required()
def admin():
        return render_template('admin/admin.html', title='Admin page')


#LISTAR las cosas de la base de datos.
@admin.route("/admin/genres")
@admin_required()
def genre_list():
        page = request.args.get('page', 1, type=int)
        items = Genre.query.all().paginate(page=page, per_page=10)
        return render_template('admin/admin_list.html', title='Lista de Generos', listOf = 'genre', items=items)

@admin.route("/admin/authors")
@admin_required()
def author_list():
        page = request.args.get('page', 1, type=int)
        items = Author.query.all().paginate(page=page, per_page=10)
        return render_template('admin/admin_list.html', title='Lista de Autores', listOf = 'author', items=items)

@admin.route("/admin/publishers")
@admin_required()
def publisher_list():
        page = request.args.get('page', 1, type=int)
        items = Publisher.query.all().paginate(page=page, per_page=10)
        return render_template('admin/admin_list.html', title='Lista de Editoriales', listOf = 'publisher', items=items)

@admin.route("/admin/books")
@admin_required()
def book_list():
        page = request.args.get('page', 1, type=int)
        boitemsoks = Book.query.all().paginate(page=page, per_page=10)
        return render_template('admin/admin_list.html', title='Lista de Libros', listOf = 'book', items=items)

@admin.route("/admin/news")
@admin_required()
def news_list():
        page = request.args.get('page', 1, type=int)
        items = news.query.all().paginate(page=page, per_page=10)
        return render_template('admin/admin_list.html', title='Lista de Noticias', listOf = 'news', items=items))

#CREAR las cosas de la base de datos.
@admin.route("/admin/new_genre")
@admin_required()
def new_genre():
        form = GenreForm()
        if form.validate_on_submit():
                genre = Genre(name=form.name.data)
                db.session.add(genre)
                db.session.commit()
                flash('Genre added successfully', 'success')
                return redirect(url_for('admin.genre_list'))
        return render_template('admin/genre_new.html', form=form, legend='Nuevo Genero', title='Nuevo Genero')

@admin.route("/admin/new_author")
@admin_required()
def new_author():
        form = AuthorForm()
        if form.validate_on_submit():
                author = Author(name=form.name.data, surname=form.surname.data)
                db.session.add(author)
                db.session.commit()
                flash('Author added successfully', 'success')
                return redirect(url_for('admin.author_list'))
        return render_template('admin/author_new.html', form=form, legend='Nuevo Autor', title='Nuevo Autor')

@admin.route("/admin/new_publisher")
@admin_required()
def new_publisher():
        form = PublisherForm()
        if form.validate_on_submit():
                publisher = Publisher(name=form.name.data)
                db.session.add(publisher)
                db.session.commit()
                flash('Publisher added successfully', 'success')
                return redirect(url_for('admin.publisher_list'))
        return render_template('admin/publisher_new.html', form=form, legend='Nueva Editorial', title='Nueva Editorial')

@admin.route("/admin/new_book")
@admin_required()
def new_book():
        form = BookForm()
        if form.validate_on_submit():
                theAuthor = Author.query.get(form.author.data)
                theGenre = Genre.query.get(form.genre.data)
                thePublisher = Publisher.query.get(form.publisher.data)
                book = Book(name=form.name.data, author = theAuthor, genre = theGenre, publisher = thePublisher)
                db.session.add(book)
                db.session.commit()
                flash('Book added successfully', 'success')
                return redirect(url_for('admin.book_list'))
        return render_template('admin/book_new.html', form=form, legend='Nuevo Libro', title='Nuevo Libro')
        

#EDITAR las cosas de la base de datos.


#Everything below this is commented out
'''
@admin.route("/admin/genres")
@admin_required()
def genre_list():
        page = request.args.get('page', 1, type=int)
        genres = Genre.query.all().paginate(page=page, per_page=10)
        return render_template('genrelist.html', title='Lista de Generos')


@admin.route("/admin/authors")
@admin_required()
def author_list():
        page = request.args.get('page', 1, type=int)
        authors = Author.query.all().paginate(page=page, per_page=10)
        return render_template('authorlist.html', title='Lista de Autores')

@admin.route("/admin/publishers")
@admin_required()
def publisher_list():
        page = request.args.get('page', 1, type=int)
        publishers = Publisher.query.all().paginate(page=page, per_page=10)
        return render_template('publisherlist.html', title='Lista de Editoriales')

@admin.route("/admin/books")
@admin_required()
def book_list():
        page = request.args.get('page', 1, type=int)
        books = Book.query.all().paginate(page=page, per_page=10)
        return render_template('booklist.html', title='Lista de Libros')

@admin.route("/admin/news")
@admin_required()
def news_list():
        page = request.args.get('page', 1, type=int)
        news = news.query.all().paginate(page=page, per_page=10)
        return render_template('newslist.html', title='Lista de Noticias')
'''