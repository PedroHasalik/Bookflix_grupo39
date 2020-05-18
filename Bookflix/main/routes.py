from flask import render_template, request, Blueprint
from Bookflix.decorators import full_login_required 
from Bookflix.models import News

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
@full_login_required()
def home():
    news = News.query.order_by(News.date_posted.desc())
    return render_template('home.html', news=news)