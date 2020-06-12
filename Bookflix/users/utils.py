import os
import secrets
from PIL import Image
from flask import url_for, current_app
from Bookflix.models import NavigationHistoryEntry
from flask_login import current_user
from Bookflix import db

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