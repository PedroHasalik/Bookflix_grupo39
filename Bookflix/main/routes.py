from flask import render_template, request, Blueprint
from flask_login import login_required
from Bookflix.models import News

main = Blueprint('main', __name__)

@main.route('/home')
#@login_required
def home():
    news = News.query.order_by(News.date_posted.desc())
    return render_template('home.html', news=news)