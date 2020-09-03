"""View functions mapped to route URLs"""

from flask import render_template, request, jsonify
from flaskapp import app
from flaskapp.backend.API import Google, WikiMedia
from flaskapp.backend.messages import Message
from config import MAPBOX_API


@app.route("/ajax/", methods=["GET", "POST"])
def ajax():
    """Process data from the Ajax call"""
    google, wiki, message = Google(), WikiMedia(), Message()
    messages = []

    if request.form["Question"]:
        question = request.form["Question"]
        locate = google.geoloc(question)

        if google.loc_data["status"]:
            infos_wiki = wiki.get_infos(locate["district"])
            messages.append(message.positive_address())

            if wiki.wiki_data["status"]:
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

            messages.append(message.negative_wiki())
            return jsonify(
                {
                    "locate": locate["locate"],
                    "address": locate["address"],
                    "messages": messages,
                    "question": question,
                }
            )
        messages.append(message.negative_address())
        return jsonify({"messages": messages, "question": question,})
    messages.append("Mais pose donc une question!!")
    return jsonify({"messages": messages, "question": "",})


@app.route("/")
@app.route("/index/")
def index():
    """To return """
    return render_template("index.html", MAPBOX_KEY=MAPBOX_API)
