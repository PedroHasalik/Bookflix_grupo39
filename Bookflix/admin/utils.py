import os
import secrets
from PIL import Image
from flask import url_for, current_app



def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/news_pics', picture_fn)

    output_size = (500, 500)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    form_picture.save(picture_path)

    return picture_fn

def save_book_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/book_pics', picture_fn)

    #output_size = (125, 125)
    #i = Image.open(form_picture)
    #i.thumbnail(output_size)
    #i.save(picture_path)

    form_picture.save(picture_path)

    return picture_fn

def save_chapter(form_pdf, filename):
    _, f_ext = os.path.splitext(form_pdf.filename)
    pdf_fn = filename + f_ext
    pdf_path = os.path.join(current_app.root_path, 'static/chapter_pdfs', pdf_fn)

    form_pdf.save(pdf_path)

    return pdf_fn