#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import render_template, redirect, request, jsonify
from flaskapp import app
from flaskapp.forms import PapyForm
from config import MAPBOX_API
from flaskapp.backend.API import Google, WikiMedia

import pdb


@app.route("/ajax/", methods=["GET", "POST"])
def ajax():

    locate = ""

    google = Google()
    wiki = WikiMedia()

    if request.form["Question"]:
        question = request.form["Question"]
        locate = google.geoloc(question)
        infos_wiki = wiki.get_infos(locate["district"])

    # breakpoint()

    return jsonify(
        {
            "locate": locate["locate"],
            "address": locate["address"],
            "summary": infos_wiki["summary"],
            "url": infos_wiki["url"],
        }
    )


@app.route("/")
@app.route("/index/")
def index():

    return render_template("index.html", MAPBOX_KEY=MAPBOX_API)
