import requests
from parser import Parser
from config import GEOCODE_URL, GOOGLE_API

import pdb

def geoloc(question):

    parsing = Parser()
    question_parsed = parsing.parse(question)

    GOO = str(GOOGLE_API)

    payload = {
        'address': question_parsed,
        'key': GOOGLE_API
    }

    req = requests.get(GEOCODE_URL, params=payload)
    response = req.json()

    locate = response['results'][0]['geometry']['location']
    
    return locate
