from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class PapyForm(FlaskForm):
    question = StringField('Question', validators=[DataRequired()])
    submit = SubmitField('Envoyer')
