# Grandpy Bot 🤖 👴:

Grandpy Bot is a bot with whom you can interact in order to get information about an address, a place, a monument or whatever GrandPy is able to get information from. If Grandypy Bot manage to get an address, he will display a map with a marker accordingly to the GPS coordinates of the address. If he manage to get an address, Grandpy will try to get information from Wikipedia about the retrieved address and he will display it under the map. If Grandpy can't retrieve an adresse or information about the address, he will inform the user. The former questions asked by the user will be displayed by grandpy bot until the page is updated.

# Created with:

* python 3.7.4
* flask 1.1.2
* requests 2.24.0

# Heroku:

The `Procfile` provided allows to deploy the program on heroku.

# How to run the program:

You have to get a [MapBox API key](https://docs.mapbox.com/help/how-mapbox-works/access-tokens/) and  a [GoogleMap API key](https://developers.google.com/maps/documentation/geocoding/get-api-key)

Then, you have to store these keys as environment variables.

For linux local storage:

* fork the code
* cd oc_P7
* Create a virtual environement: virtualenv -p python3 .venv
* Activate the virtual environment: source .venv/bin/activate
* export GOOGLE_API_KEY="Your google api key"
* export MAPBOX_API_KEY="Your mapbox api key"

You also need to set the FLASK_APP environment variable berore running it:

* export FLASK_APP=grandpy_bot.py

* Then, you can run it: flask run

The website is accessible on http://127.0.0.1:5000/ with your web browser.

# Tests:

You can test the program with the following command:

* pytest tests_grandpy_bot.py

# Switching to Google Maps JS:

The code to switch to Google Maps JS is commented in ajax.js file to easily switch maps from Mapbox GL JS to Google Maps JS.