#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import render_template, redirect, request, jsonify
from flaskapp import app
from flaskapp.forms import PapyForm
from geoloc import geoloc
from config import MAPBOX_API

import pdb

@app.route('/ajax/', methods=['GET', 'POST'])
def ajax():

    locate=""

    if request.form['Question']:
        question = request.form['Question']
        locate = geoloc(question)

    # breakpoint()


    return jsonify(locate)

@app.route('/')
@app.route('/index/')
def index():
    
    return render_template('index.html', MAPBOX_KEY = MAPBOX_API)
