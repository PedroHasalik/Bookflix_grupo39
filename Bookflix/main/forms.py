from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,  TextAreaField, RadioField
from wtforms.validators import DataRequired

class SearchForm(FlaskForm):
  search = StringField('Búsqueda', [DataRequired()])
  submit = SubmitField('Buscar')

class ReviewForm(FlaskForm):
    text = TextAreaField('Texto', [DataRequired()])
    score =  RadioField('Puntaje', choices=[(1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5')] ,validators=[DataRequired()])
    submit = SubmitField('Publicar')