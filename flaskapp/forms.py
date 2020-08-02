from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class PapyForm(FlaskForm):
    question = StringField('Pose une question à ton papi', validators=[DataRequired()])
    submit = SubmitField('Envoyer')
