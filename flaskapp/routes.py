"""View functions mapped to route URLs"""

from flask import render_template, request, make_response
from flaskapp import app
from flaskapp.backend.api import Google, WikiMedia
from flaskapp.backend.parser import Parser
from flaskapp.backend.messages import Message
from config import MAPBOX_API
# from config import GOOGLE_API


@app.route("/ajax/", methods=["POST"])
def ajax():
    """Process data from the Ajax call"""
    google, wiki, message = Google(), WikiMedia(), Message()
    messages = []

    # check if the user ask an empty question:
    if request.form["Question"]:
        question = request.form["Question"]
        parsing = Parser()
        question_parsed = parsing.parse(question)
        locate = google.geoloc(question_parsed)

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
                    }

            messages.append(message.negative_wiki())
            return {
                    "locate": locate["locate"],
                    "address": locate["address"],
                    "messages": messages,
                }

        messages.append(message.negative_address())
        return {"messages": messages}
    messages.append("Mais pose donc une question!!")
    return {"messages": messages}


@app.route("/")
@app.route("/index/")
def index():
    """To show the page of Grandpy_bot"""
    resp = make_response(render_template("index.html", MAPBOX_KEY=MAPBOX_API))
    resp.headers['Content-Security-Policy'] = "default-src 'self' data: ; \
    style-src 'self' 'unsafe-inline' \
    https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css \
    https://api.mapbox.com/mapbox-gl-js/v1.11.1/mapbox-gl.css \
    http://localhost:5000/static/css/styles.css ;\
    worker-src 'self' https://api.mapbox.com/mapbox-gl-js/v1.11.1/mapbox-gl.js blob: ;\
    connect-src 'self' data: 'unsafe-inline' 'unsafe-eval' *; \
    script-src-elem 'self' 'unsafe-inline'\
    https://api.mapbox.com/mapbox-gl-js/v1.11.1/mapbox-gl.css\
    https://api.mapbox.com/mapbox-gl-js/v1.11.1/mapbox-gl.js ;"

    return resp
    """To switch to Google Map JS"""
    # return render_template("index.html", GOOGLE_KEY=GOOGLE_API)