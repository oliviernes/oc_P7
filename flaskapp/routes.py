#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import render_template, redirect
from flaskapp import app
from flaskapp.forms import PapyForm
from geoloc import geoloc

import pdb

@app.route('/', methods=['GET', 'POST'])
@app.route('/index/', methods=['GET', 'POST'])
def index():
    form = PapyForm()
    form.validate_on_submit()
    locate=""
    if form.question.data:
        question = form.question.data
        locate = geoloc(question)
 
    return render_template('index.html', locate = locate, form = form)
