from flask import render_template, request, Blueprint, flash, redirect, url_for
from Bookflix import db
from Bookflix.decorators import full_login_required, admin_required
from Bookflix.models import Book, Author, Genre, Publisher, News
from Bookflix.admin.forms import GenreForm, AuthorForm, PublisherForm, BookForm, NewsForm

admin = Blueprint('admin', __name__)


#        <a class="btn btn-outline-info" href="{{ url_for('admin.genres') }}">Generos</a>
#        <a class="btn btn-outline-info" href="{{ url_for('admin.authors') }}">Autores</a>
#        <a class="btn btn-outline-info" href="{{ url_for('admin.publishers') }}">Editoriales</a>
#        <a class="btn btn-outline-info" href="{{ url_for('admin.books') }}">Libros</a>
#        <a class="btn btn-outline-info" href="{{ url_for('admin.news') }}">Novedades</a>

@admin.route("/admin")
@admin_required()
def admin_dashboard():
        return render_template('admin/admin.html', title='Admin page')


#LISTAR las cosas de la base de datos.
@admin.route("/admin/genres")
@admin_required()
def genre_list():
        page = request.args.get('page', 1, type=int)
        items = Genre.query.paginate(page=page, per_page=10)
        return render_template('admin/admin_list.html', title='Lista de Generos', listOf = 'genre', items=items)

@admin.route("/admin/authors")
@admin_required()
def author_list():
        page = request.args.get('page', 1, type=int)
        items = Author.query.paginate(page=page, per_page=10)
        return render_template('admin/admin_list.html', title='Lista de Autores', listOf = 'author', items=items)

@admin.route("/admin/publishers")
@admin_required()
def publisher_list():
        page = request.args.get('page', 1, type=int)
        items = Publisher.query.paginate(page=page, per_page=10)
        return render_template('admin/admin_list.html', title='Lista de Editoriales', listOf = 'publisher', items=items)

@admin.route("/admin/books")
@admin_required()
def book_list():
        page = request.args.get('page', 1, type=int)
        items = Book.query.paginate(page=page, per_page=10)
        return render_template('admin/admin_list.html', title='Lista de Libros', listOf = 'book', items=items)

@admin.route("/admin/news")
@admin_required()
def news_list():
        page = request.args.get('page', 1, type=int)
        items = News.query.paginate(page=page, per_page=10)
        return render_template('admin/admin_list.html', title='Lista de Noticias', listOf = 'news', items=items)

#CREAR las cosas de la base de datos.
@admin.route("/admin/new_genre", methods=['GET', 'POST'])
@admin_required()
def new_genre():
        form = GenreForm()
        if form.validate_on_submit():
                genre = Genre(name=form.name.data)
                db.session.add(genre)
                db.session.commit()
                flash('Genre added successfully', 'success')
                return redirect(url_for('admin.genre_list'))
        return render_template('admin/new_genre.html', form=form, legend='Nuevo Genero', title='Nuevo Genero')

@admin.route("/admin/new_author", methods=['GET', 'POST'])
@admin_required()
def new_author():
        form = AuthorForm()
        if form.validate_on_submit():
                author = Author(name=form.name.data, surname=form.surname.data)
                db.session.add(author)
                db.session.commit()
                flash('Author added successfully', 'success')
                return redirect(url_for('admin.author_list'))
        return render_template('admin/new_author.html', form=form, legend='Nuevo Autor', title='Nuevo Autor')

@admin.route("/admin/new_publisher", methods=['GET', 'POST'])
@admin_required()
def new_publisher():
        form = PublisherForm()
        if form.validate_on_submit():
                publisher = Publisher(name=form.name.data)
                db.session.add(publisher)
                db.session.commit()
                flash('Publisher added successfully', 'success')
                return redirect(url_for('admin.publisher_list'))
        return render_template('admin/new_publisher.html', form=form, legend='Nueva Editorial', title='Nueva Editorial')

@admin.route("/admin/new_book", methods=['GET', 'POST'])
@admin_required()
def new_book():
        form = BookForm()
        #i have to put it to 0 because I'm coercing the field to be integer and a None just gets fucked up. 
        #Next sprint: go back to this being None, find away to bypass the coerce=int thing
        authorChoices = ([(0, 'None')]+ [(each.id, each.full_name()) for each in Author.query.all()]) 
        genreChoices = ([(0, 'None')]+ [(each.id, each.full_name()) for each in Genre.query.all()])
        publisherChoices = ([(0, 'None')]+ [(each.id, each.full_name()) for each in Publisher.query.all()])
        form.author.choices = authorChoices
        form.genre.choices = genreChoices
        form.publisher.choices = publisherChoices
        if form.validate_on_submit():
                if (form.author.data == 0):
                        theAuthor = None
                else:
                        theAuthor = Author.query.get(form.author.data)

                if (form.genre.data == 0):
                        theGenre = None
                else:
                        theGenre = Genre.query.get(form.genre.data)

                if (form.publisher.data == 0):
                        thePublisher = None
                else:
                        thePublisher = Publisher.query.get(form.publisher.data)

                book = Book(title=form.title.data, isbn = form.isbn.data, theAuthor = theAuthor, theGenre = theGenre, thePublisher = thePublisher)
                db.session.add(book)
                db.session.commit()
                flash('Book added successfully', 'success')
                return redirect(url_for('admin.book_list'))
        return render_template('admin/new_book.html', form=form, legend='Nuevo Libro', title='Nuevo Libro')

@admin.route('/admin/new_news', methods=['GET', 'POST'])
@admin_required()
def new_news():
    form = NewsForm()
    if form.validate_on_submit():
        news = News(title=form.title.data, content=form.content.data)
        db.session.add(news)
        db.session.commit()
        flash('La novedad ha sido creada.', 'success')
        return redirect(url_for('admin.news_list'))
    return render_template('admin/new_news.html', title= 'Nueva novedad', form=form, legend='Nueva novedad')

#EDITAR las cosas de la base de datos.
@admin.route("/admin/genre/edit/<int:id>", methods=['GET', 'POST'])
@admin_required()
def edit_genre(id):
        genre = Genre.query.get_or_404(id)
        form = GenreForm()
        if form.validate_on_submit():
                genre.name = form.name.data
                db.session.commit()
                flash('Genre successfully updated!', 'success')
                return redirect(url_for('admin.genre_list'))
        elif request.method == 'GET':
                form.name.data = genre.name
        return render_template('admin/new_genre.html', form=form, legend='Editar Genero', title=genre.name)

@admin.route("/admin/author/edit/<int:id>", methods=['GET', 'POST'])
@admin_required()
def edit_author(id):
        author = Author.query.get_or_404(id)
        form = AuthorForm()
        if form.validate_on_submit():
                author.name = form.name.data
                author.surname = form.surname.data
                db.session.commit()
                flash('author successfully updated!', 'success')
                return redirect(url_for('admin.author_list'))
        elif request.method == 'GET':
                form.name.data = author.name
                form.surname.data = author.surname
        return render_template('admin/new_author.html', form=form, legend='Editar Autor', title=author.name)

@admin.route("/admin/publisher/edit/<int:id>", methods=['GET', 'POST'])
@admin_required()
def edit_publisher(id):
        publisher = Publisher.query.get_or_404(id)
        form = PublisherForm()
        if form.validate_on_submit():
                publisher.name = form.name.data
                db.session.commit()
                flash('publisher successfully updated!', 'success')
                return redirect(url_for('admin.publisher_list'))
        elif request.method == 'GET':
                form.name.data = publisher.name
        return render_template('admin/new_publisher.html', form=form, legend='Editar Editorial', title=publisher.name)

@admin.route("/admin/book/edit/<int:id>", methods=['GET', 'POST'])
@admin_required()
def edit_book(id):
        book = Book.query.get_or_404(id)
        form = BookForm()
        authorChoices = ([(0, 'None')]+ [(each.id, each.full_name()) for each in Author.query.all()])
        genreChoices = ([(0, 'None')]+ [(each.id, each.full_name()) for each in Genre.query.all()])
        publisherChoices = ([(0, 'None')]+ [(each.id, each.full_name()) for each in Publisher.query.all()])
        form.author.choices = authorChoices
        form.genre.choices = genreChoices
        form.publisher.choices = publisherChoices
        if form.validate_on_submit():
                book.title = form.title.data
                book.isbn = form.isbn.data

                if (form.author.data == 0):
                        book.theAuthor = None
                else:
                        book.theAuthor = Author.query.get(form.author.data)

                if (form.genre.data == 0):
                        book.theGenre = None
                else:
                        book.theGenre = Genre.query.get(form.genre.data)

                if (form.publisher.data == 0):
                        book.thePublisher = None
                else:
                        book.thePublisher = Publisher.query.get(form.publisher.data)

                db.session.commit()
                flash('book successfully updated!', 'success')
                return redirect(url_for('admin.book_list'))
        elif request.method == 'GET':
                form.title.data = book.title
                form.isbn.data = book.isbn
                
                if (book.theAuthor):
                        form.author.data = book.theAuthor.id
                else:
                        form.author.data = 0
                
                if (book.theGenre):                       
                        form.genre.data = book.theGenre.id
                else:
                        form.genre.data = 0

                if (book.thePublisher):
                        form.publisher.data = book.thePublisher.id
                else:
                        form.publisher.data = 0

        return render_template('admin/new_book.html', form=form, legend='Editar Genero', title=book.title)

@admin.route("/admin/news/edit/<int:id>",  methods=['GET', 'POST'])
@admin_required()
def edit_news(id):
    news = News.query.get_or_404(id)
    form = NewsForm()
    if form.validate_on_submit():
        news.title = form.title.data
        news.content = form.content.data
        db.session.commit()
        flash('Novedad modificada.', 'success')
        return redirect(url_for('admin.news_list'))
    elif request.method == 'GET':
        form.title.data = news.title
        form.content.data = news.content

    return render_template('admin/new_news.html', title='Editar Novedad', form=form, legend='Editar Novedad')

#BORRAR las cosas de la base de datos

@admin.route("/admin/genre/delete/<int:id>")
@admin_required()
def delete_genre(id):
        genre = Genre.query.get_or_404(id)
        db.session.delete(genre)
        db.session.commit()
        flash('Genre successfully deleted!', 'success')
        return redirect(url_for('admin.genre_list'))

@admin.route("/admin/author/delete/<int:id>")
@admin_required()
def delete_author(id):
        author = Author.query.get_or_404(id)
        db.session.delete(author)
        db.session.commit()
        flash('Author successfully deleted!', 'success')
        return redirect(url_for('admin.author_list'))

@admin.route("/admin/publisher/delete/<int:id>")
@admin_required()
def delete_publisher(id):
        publisher = Publisher.query.get_or_404(id)
        db.session.delete(publisher)
        db.session.commit()
        flash('Publisher successfully deleted!', 'success')
        return redirect(url_for('admin.publisher_list'))

@admin.route("/admin/book/delete/<int:id>")
@admin_required()
def delete_book(id):
        book = Book.query.get_or_404(id)
        db.session.delete(book)
        db.session.commit()
        flash('Book successfully deleted!', 'success')
        return redirect(url_for('admin.book_list'))

@admin.route("/admin/news/delete/<int:id>")
@admin_required()
def delete_news(id):
        news = News.query.get_or_404(id)
        db.session.delete(news)
        db.session.commit()
        flash('News successfully deleted!', 'success')
        return redirect(url_for('admin.news_list'))

#Everything below this is commented out
'''
@news.route("/new/<int:new_id>/delete",  methods=['POST'])
@admin_required()
def delete_new(new_id):
    new = News.query.get_or_404(new_id)
    if new.author != current_user:
        abort(403)
    db.session.delete(new)
    db.session.commit()
    flash('Novedad eliminada', 'success')
    return redirect (url_for('main.home'))

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