from flask import render_template, request, Blueprint
from flask_login import login_required, current_user
from Bookflix.decorators import full_login_required 
from Bookflix.models import News, User

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
@login_required
def home():
    news = News.query.order_by(News.date_posted.desc())
    return render_template('home.html', news=news)

@main.route('/profiles')
@login_required
def profiles():
    profiles = current_user.profiles
    return render_template('bookflix_profiles.html', profiles=profiles, user=current_user)