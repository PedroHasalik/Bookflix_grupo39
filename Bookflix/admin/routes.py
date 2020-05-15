from flask import render_template, request, Blueprint
from bookflix.decorators import roles_required
from bookflix.models import Book, Author, Genre, Publisher, News

admin = Blueprint('admin', __name__)


#        <a class="btn btn-outline-info" href="{{ url_for('admin.genres') }}">Generos</a>
#        <a class="btn btn-outline-info" href="{{ url_for('admin.authors') }}">Autores</a>
#        <a class="btn btn-outline-info" href="{{ url_for('admin.publishers') }}">Editoriales</a>
#        <a class="btn btn-outline-info" href="{{ url_for('admin.books') }}">Libros</a>
#        <a class="btn btn-outline-info" href="{{ url_for('admin.news') }}">Novedades</a>

@admin.route("/admin")
@admin_required()
def admin():
        return render_template('admin.html', title='Admin page')


#Listas de cosas de la base de datos.
@admin.route("/admin/genres")
@admin_required()
def genre_list():
        page = request.args.get('page', 1, type=int)
        items = Genre.query.all().paginate(page=page, per_page=10)
        return render_template('admin_list.html', title='Lista de Generos', listOf = 'genre', items=items)

@admin.route("/admin/authors")
@admin_required()
def author_list():
        page = request.args.get('page', 1, type=int)
        items = Author.query.all().paginate(page=page, per_page=10)
        return render_template('admin_list.html', title='Lista de Autores', listOf = 'author', items=items)

@admin.route("/admin/publishers")
@admin_required()
def publisher_list():
        page = request.args.get('page', 1, type=int)
        items = Publisher.query.all().paginate(page=page, per_page=10)
        return render_template('admin_list.html', title='Lista de Editoriales', listOf = 'publisher', items=items)

@admin.route("/admin/books")
@admin_required()
def book_list():
        page = request.args.get('page', 1, type=int)
        boitemsoks = Book.query.all().paginate(page=page, per_page=10)
        return render_template('admin_list.html', title='Lista de Libros', listOf = 'book', items=items)

@admin.route("/admin/news")
@admin_required()
def news_list():
        page = request.args.get('page', 1, type=int)
        items = news.query.all().paginate(page=page, per_page=10)
        return render_template('admin_list.html', title='Lista de Noticias', listOf = 'news', items=items))

#Crear las cosas de la base de datos.
@admin.route("/admin/new_genre")
@admin_required()
def new_genre():
        

#Editar las cosas de la base de datos.



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