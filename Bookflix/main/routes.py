from flask import render_template, request, Blueprint
from flask_login import login_required, current_user
from Bookflix.decorators import full_login_required 
from Bookflix.models import News, User, Profile

main = Blueprint('main', __name__)


@main.route('/home')
@login_required
def home():
    news = News.query.order_by(News.date_posted.desc())
    return render_template('home.html', news=news)

@main.route('/profiles')
@login_required
def profiles():
    profiles = Profile.query.filter_by(owner=current_user).all()
    return render_template('bookflix_profiles.html', profiles=profiles)