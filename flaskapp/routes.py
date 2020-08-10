#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import render_template, redirect, request, jsonify
from flaskapp import app
from flaskapp.forms import PapyForm
from geoloc import geoloc

import pdb

@app.route('/ajax/', methods=['GET', 'POST'])
def ajax():

    locate=""

    if request.form['Question']:
        question = request.form['Question']
        locate = geoloc(question)

    return jsonify(locate)

@app.route('/', methods=['GET', 'POST'])
@app.route('/index/', methods=['GET', 'POST'])
def index():
 
    return render_template('index.html')
