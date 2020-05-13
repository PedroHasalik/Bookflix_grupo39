from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class NewsForm(FlaskForm):
    title = StringField('Título:', validators=[DataRequired()])
    content = TextAreaField('Contenido:', validators=[DataRequired()])

    submit = SubmitField('Subir novedad')