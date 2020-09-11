"""View functions mapped to route URLs"""

from flask import render_template, request
from flaskapp import app
from flaskapp.backend.API import Google, WikiMedia
from flaskapp.backend.messages import Message
from config import MAPBOX_API


@app.route("/ajax/", methods=["GET", "POST"])
def ajax():
    """Process data from the Ajax call"""
    google, wiki, message = Google(), WikiMedia(), Message()
    messages = []

    # check if the user ask an empty question:
    if request.form["Question"]:
        question = request.form["Question"]
        locate = google.geoloc(question)

        # check if the geoloc return a valid answer:
        if locate["status"]:
            infos_wiki = wiki.get_infos(locate["district"])
            messages.append(message.positive_address())

            # check if wikimedia return a valid answer:
            if infos_wiki["status"]:
                messages.append(message.positive_wiki())
                return {
                        "locate": locate["locate"],
                        "address": locate["address"],
                        "summary": infos_wiki["summary"],
                        "url": infos_wiki["url"],
                        "messages": messages,
                        "question": question,
                    }

            messages.append(message.negative_wiki())
            return {
                    "locate": locate["locate"],
                    "address": locate["address"],
                    "messages": messages,
                    "question": question,
                }

        messages.append(message.negative_address())
        return {"messages": messages, "question": question,}
    messages.append("Mais pose donc une question!!")
    return {"messages": messages, "question": "",}


@app.route("/")
@app.route("/index/")
def index():
    """To show the page of Grandpy_bot"""
    return render_template("index.html", MAPBOX_KEY=MAPBOX_API)
