from flask import render_template, request, Blueprint, redirect, url_for
from flask_login import login_required, current_user
from Bookflix.decorators import full_login_required 
from Bookflix.models import News, User, Profile, Book
from Bookflix.main.forms import SearchForm

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
    results = Book.query.filter(Book.title.contains(query)).all()
    return render_template('search_results.html', results=results, query=query)

@main.route('/book/<id>')
@full_login_required()
def book(id):
    theBook = Book.query.get_or_404(id)
    return render_template('book.html', book=theBook)






