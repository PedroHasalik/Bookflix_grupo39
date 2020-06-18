from flask import render_template, request, Blueprint, redirect, url_for, flash
from flask_login import login_required, current_user
from Bookflix.decorators import full_login_required 
from Bookflix.models import News, User, Profile, Book, Publisher, Genre, Author, Chapter
from Bookflix.main.forms import SearchForm
from Bookflix.users.utils import saveBookHistory

main = Blueprint('main', __name__)


@main.route('/home')
@full_login_required()
def home():
    page = request.args.get('page', 1, type=int)
    news = News.query.paginate(page=page, per_page=10)
    return render_template('home.html', title='Home', news=news)

@main.route('/profiles')
@login_required
def profiles():
    profiles = Profile.query.filter_by(owner=current_user).all()
    return render_template('bookflix_profiles.html', profiles=profiles)

@main.route("/news/<int:news_id>")
@full_login_required()
def news(news_id):
    news = News.query.get_or_404(news_id)
    return render_template ('news.html', title=news.title, news=news)

@main.route('/search', methods=['GET', 'POST'])
@full_login_required()
def search():
    form = SearchForm()
    if request.method == 'POST' and form.validate_on_submit():
        return redirect(url_for('main.search_results', query=form.search.data))
    return render_template('search.html', legend="Nueva Búsqueda", form=form)

@main.route('/search_results/<query>')
@full_login_required()
def search_results(query):
    results = Book.query.filter((Book.title.contains(query)) | (Book.thePublisher.has(Publisher.name.contains(query))) | (Book.theGenre.has(Genre.name.contains(query))) | (Book.theAuthor.has(Author.name.contains(query))) ).filter_by(public = True).all()
    return render_template('search_results.html', results=results, query=query)

@main.route('/book/<id>')
@full_login_required()
def book(id):
    theBook = Book.query.get_or_404(id)
    if (current_user.accountType != 'Admin' and theBook.public == False):
        flash('Este libro todavia no esta disponible.', 'info')
        return redirect(url_for('main.home'))
    saveBookHistory(name=theBook.full_name(),entryType='Book', id=id)
    return render_template('book.html', book=theBook)

@main.route('/chapter/<chapter_id>')
@full_login_required()
def chapter(chapter_id):
    theChapter = Chapter.query.get_or_404(chapter_id)
    theBook = Book.query.get_or_404(theChapter.book_id)
    theName = theBook.full_name() + ' - ' + theChapter.full_name()
    if (current_user.accountType != 'Admin' and theBook.public == False):
        flash('Este libro todavia no esta disponible.', 'info')
        return redirect(url_for('main.home'))
    saveBookHistory(name=theName, entryType='Chapter', id=chapter_id)
    return render_template('chapter.html', book=theBook, chapter=theChapter)






