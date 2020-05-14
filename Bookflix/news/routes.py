from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import News
from flaskblog.news.forms import NewsForm

news = Blueprint('news', __name__)

#Estas rutas solo podrán ser utilizadas por el administrador.

@news.route('/news/create_new', methods=['GET', 'POST'])
@login_required #(Admin)
def new_new():
    form = NewsForm()
    if form.validate_on_submit():
        new = News(title=form.title.data, content=form.content.data)
        db.session.add(new)
        db.session.commit()
        flash('La novedad ha sido creada.', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_new.html', title= 'Nueva novedad', form=form, legend='Nueva novedad')

@news.route("/news/<int:new_id>")
def new(new_id):
    new = News.query.get_or_404(new_id)
    return render_template ('new.html', title=new.title, new=new)

@news.route("/new/<int:new_id>/update",  methods=['GET', 'POST'])
@login_required
def update_new(new_id):
    new = News.query.get_or_404(new_id)
    if new.author != current_user:
        abort(403) #Hay que cambiar esto; lógica: si no sos admin no podés.
    
    form = NewsForm()
    if form.validate_on_submit():
        new.title = form.title.data
        new.content = form.content.data
        new.image_file = form.picture.data
        db.session.commit()
        flash('Novedad modificada.', 'success')
        return redirect(url_for('news.new', new_id=new.id))
    elif request.method == 'GET':
        form.title.data = new.title
        form.content.data = new.content

    return render_template('create_new.html', title='Update new', form=form, legend='Update new')


@news.route("/new/<int:new_id>/delete",  methods=['POST'])
@login_required
def delete_new(new_id):
    new = News.query.get_or_404(new_id)
    if new.author != current_user:
        abort(403)
    db.session.delete(new)
    db.session.commit()
    flash('Novedad eliminada', 'success')
    return redirect (url_for('main.home'))

