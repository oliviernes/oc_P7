#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import render_template, redirect, request, jsonify
from flaskapp import app
from flaskapp.forms import PapyForm
from config import MAPBOX_API
from flaskapp.backend.API import Google, WikiMedia
from flaskapp.backend.messages import Message

import pdb


@app.route("/ajax/", methods=["GET", "POST"])
def ajax():

    google = Google()
    wiki = WikiMedia()
    message = Message()
    messages = []

    if request.form["Question"]:
        question = request.form["Question"]
        locate = google.geoloc(question)

        if google.loc_data['status']:
            infos_wiki = wiki.get_infos(locate["district"])
            messages.append(message.positive_address())
            if wiki.wiki_data['status']:
                messages.append(message.positive_wiki())
                return jsonify(
                    {
                        "locate": locate["locate"],
                        "address": locate["address"],
                        "summary": infos_wiki["summary"],
                        "url": infos_wiki["url"],
                        "messages": messages,
                        "question": question,
                    }
                )
            else:
                messages.append(message.negative_wiki())
                return jsonify(
                    {
                        "locate": locate["locate"],
                        "address": locate["address"],
                        "messages": messages,
                        "question": question,
                    }
                )
        else:
            messages.append(message.negative_addresse())
            return jsonify({ "messages": messages, "question": question,})
    else:
        messages.append("Mais pose donc une question!!")
        return jsonify({ "messages": messages, "question": "",} )


@app.route("/")
@app.route("/index/")
def index():

    return render_template("index.html", MAPBOX_KEY=MAPBOX_API)
