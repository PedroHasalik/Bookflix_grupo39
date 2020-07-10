import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_login import current_user
from flask_mail import Message
from Bookflix import db, mail
from Bookflix.models import NavigationHistoryEntry

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

def saveBookHistory(name,entryType,id):
    entry = NavigationHistoryEntry(entryType=entryType, item_id=id, entryName=name, owner=current_user.current_profile())
    db.session.add(entry)
    db.session.commit()

def send_reset_email(user): # video 10
        token = user.get_reset_token()
        msg = Message('Password Reset Request', sender='noreply@demo.com', recipients = [user.email])
        msg.body = f'''A request has been filed to reset your password in our blog. If you didn't request a password reset, ignore this email.
To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}
This link will expire in 30 minutes.
'''
        mail.send(msg)