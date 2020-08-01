from flask import render_template, redirect
from flaskapp import app
from flaskapp.forms import PapyForm

@app.route('/')
@app.route('/index/', methods=['GET', 'POST'])
def index():
    form = PapyForm()
    form.validate_on_submit()
    return render_template('index.html', form = form)
