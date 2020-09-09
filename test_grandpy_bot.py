from flaskapp import app
import json
import pytest
import requests
from flask import request
from flaskapp.backend.parser import Parser
from flaskapp.backend.API import Google, WikiMedia, GetJson
from flaskapp.backend.messages import Message


class TestParser:

    def test_parser_adresse(self):
        adresse = (
            "Bonjour Grandpy, dis moi ce que tu sais à propos du 7 Cité"
            " Paradis, 75010 Paris"
        )
        phrase_parsed = Parser()

        assert phrase_parsed.parse(adresse) == "7 cite paradis 75010 paris"


    def test_parser_empty_string(self):
        adresse = ""
        phrase_parsed = Parser()

        assert phrase_parsed.parse(adresse) == ""


    def test_parser_STOP_WORDS_only(self):
        adresse = "a abord absolument afin ah ai aie ailleurs ainsi ait allaient"
        phrase_parsed = Parser()

        assert phrase_parsed.parse(adresse) == ""


    def test_parser_apostrophe(self):
        adresse = "Bonjour Grandpy, dis moi ce que tu sais à propos" " d'Openclassrooms"
        phrase_parsed = Parser()

        assert phrase_parsed.parse(adresse) == "openclassrooms"


class TestAPI:
    """Test the API response management."""

    def test_geoloc_return_OK(self, mocker):
        results = {
            "results": [
                {
                    "geometry": {"location": {"lat": 48.8747265, "lng": 2.3505517}},
                    "formatted_address": "7 Cité Paradis, 75010 Paris," " France",
                    "address_components": [
                        {
                            "long_name": "7",
                            "short_name": "7",
                            "types": ["street_number"],
                        },
                        {
                            "long_name": "Cité Paradis",
                            "short_name": "Cité Paradis",
                            "types": ["route"],
                        },
                        {
                            "long_name": "Paris",
                            "short_name": "Paris",
                            "types": ["locality", "political"],
                        },
                        {
                            "long_name": "Arrondissement de Paris",
                            "short_name": "Arrondissement de Paris",
                            "types": ["administrative_area_level_2", "political"],
                        },
                        {
                            "long_name": "Île-de-France",
                            "short_name": "IDF",
                            "types": ["administrative_area_level_1", "political"],
                        },
                        {
                            "long_name": "France",
                            "short_name": "FR",
                            "types": ["country", "political"],
                        },
                        {
                            "long_name": "75010",
                            "short_name": "75010",
                            "types": ["postal_code"],
                        },
                    ],
                }
            ],
            "status": "OK",
        }

        mocker.patch("flaskapp.backend.API.GetJson.get_json", return_value=results)

        goggle = Google()

        assert goggle.geoloc("openclassrooms") == {
            "locate": {"lat": 48.8747265, "lng": 2.3505517},
            "address": "7 Cité Paradis, 75010 Paris, France",
            "district": "Cité Paradis",
            "status": True,
        }

    def test_geoloc_bad_result(self, mocker):
        results = {"results": [{"bad result": "no valid data",}], "status": "OK"}

        mocker.patch("flaskapp.backend.API.GetJson.get_json", return_value=results)

        goggle = Google()
        goggle.geoloc("bad_answer")

        assert goggle.loc_data == {
            "status": False,
            "error": {
                "KeyError": "'geometry'",
                "response": {
                    "results": [{"bad result": "no valid data",}],
                    "status": "OK",
                },
            },
        }

    def test_get_infos_request(self, mocker):
        wiki = WikiMedia()

        titles = [
            "Cité Paradis",
            "OpenClassrooms",
            "Vanessa Paradis",
            "Baden-Baden",
            "Cité de Carcassonne",
            "Saison 10 de Camping Paradis",
            "Paradis (homonymie)",
            "Rue d'Hauteville",
            "Paradis",
            "Liste des voies du 10e arrondissement de Paris",
        ]

        summary = (
            "La cité Paradis est une voie publique située dans"
            " le 10e arrondissement de Paris.\n\n\n== Situation et accès"
            " ==\nLa cité Paradis est une voie publique située dans le 10e "
            "arrondissement de Paris. Elle est en forme de té, une branche"
            " débouche au 43, rue de Paradis, la deuxième au 57, rue "
            "d'Hauteville et la troisième en impasse."
        )
        url = "https://fr.wikipedia.org/wiki/Cit%C3%A9_Paradis"

        class Page:
            """Class to mock Mediawiki.page response"""

            def __init__(self):
                self.url = url

        mocker.patch("flaskapp.backend.API.MediaWiki.search", return_value=titles)
        mocker.patch("flaskapp.backend.API.MediaWiki.page", return_value=Page())
        mocker.patch("flaskapp.backend.API.MediaWiki.summary", return_value=summary)
        mocker.patch("flaskapp.backend.API.MediaWiki.page.url", return_value=url)

        assert wiki.get_infos("Cité Paradis") == {
            "summary": "La cité Paradis est une voie publique située"
            " dans le 10e arrondissement de Paris.\n\n\n\nLa cité Paradis"
            " est une voie publique située dans le 10e arrondissement de "
            "Paris. Elle est en forme de té, une branche débouche au 43, "
            "rue de Paradis, la deuxième au 57, rue d'Hauteville et la "
            "troisième en impasse.",
            "url": "https://fr.wikipedia.org/wiki/Cit%C3%A9_Paradis",
            "status": True,
        }

    def test_get_infos_no_titles(self, mocker):
        wiki = WikiMedia()

        titles = []

        mocker.patch("flaskapp.backend.API.MediaWiki.search", return_value=titles)

        assert wiki.get_infos("whatever") == {
            "summary": "",
            "url": "",
            "status": False,
        }

    def test_get_json(self, mocker):

        payload = {
            "key": "any_key",
            "address": "openclassrooms",
        }

        GEOCODE_URL = "https://maps.googleapis.com/maps/api/geocode/json"

        class Requests:
            """Class to mock Requests.get response"""

            def json(self):
                return {
                        "results": [
                                    {
                                    "address_components": [
                                        {
                                        "long_name": "10",
                                    "short_name": "10",
                                    "types": [
                                        "street_number"
                                    ]
                                    },
                                    ],
                                  }
                                ],
                        "status": "OK" 
                        }

            def raise_for_status(self):
                return "nothing"

        response = Requests()
        
        get = GetJson(GEOCODE_URL, payload)

        mocker.patch("flaskapp.backend.API.requests.get", return_value=response) 

        assert get.get_json() == response.json()

class TestMessages:
    def test_positive_adresse(self, mocker):

        message = Message()

        mocker.patch(
            "flaskapp.backend.messages.rand",
            return_value="Mais t'ai-je déjà raconté"
            " l'histoire de ce quartier qui m'a vu en "
            "culottes courtes ?",
        )

        assert (
            message.positive_address() == "Mais t'ai-je déjà raconté "
            "l'histoire de ce quartier qui m'a vu en culottes courtes ?"
        )

    def test_negative_adresse(self, mocker):

        message = Message()

        mocker.patch(
            "flaskapp.backend.messages.rand",
            return_value="Je ne comprend pas ta question. " "Parle moi mieux que ça!",
        )

        assert (
            message.negative_address() == "Je ne comprend pas ta "
            "question. Parle moi mieux que ça!"
        )


@pytest.fixture
def client():
    client = app.test_client()
    return client

def test_ajax_no_response_from_Google_API(client, mocker):


    mocker.patch(
        "flaskapp.backend.API.Google.geoloc", return_value={"status": False}
    )


    mocker.patch(
        "flaskapp.backend.messages.rand",
        return_value="Je ne comprend pas ta question. " "Parle moi mieux que ça!",
    )

    response = client.post("/ajax/?Question=azertgdsds", data = { 'Question': 'azertgdsds'} )

    data = json.loads(response.data)
    
    assert (response.status_code == 200)
    assert data == {"messages": ["Je ne comprend pas ta question. Parle moi mieux que ça!"], "question": "azertgdsds",}

def test_ajax_no_question(client, mocker):


    mocker.patch(
        "flaskapp.backend.messages.rand",
        return_value="Je ne comprend pas ta question. " "Parle moi mieux que ça!",
    )

    response = client.post("/ajax/?Question=", data = { 'Question': ''} )

    data = json.loads(response.data)
    
    assert (response.status_code == 200)
    assert data == {"messages": ["Mais pose donc une question!!"], "question": "",}


def test_ajax_response_from_Google_API_but_not_Wikipedia(client, mocker):


    mocker.patch(
        "flaskapp.backend.API.Google.geoloc", return_value={"locate": {
                                'lat': 48.8975156, 'lng': 2.3833993},
                                "district": 'Quai de la Charente',
                                "address": '10 Quai de la Charente, 75019 Paris, France',
                                "status": True,
                                }
    )

    mocker.patch(
        "flaskapp.backend.API.WikiMedia.get_infos", return_value={"summary": "", "url": "", "status": False}
    )

    mocker.patch(
        "flaskapp.backend.messages.Message.positive_address", return_value = "Bien sûr mon poussin ! La voici: ",
    )

    mocker.patch(
        "flaskapp.backend.messages.Message.negative_wiki", return_value = "Ça ne me dit rien du tout!!",
    )

    response = client.post("/ajax/?Question=openclassrooms", data = { 'Question': 'openclassrooms'} )

    data = json.loads(response.data)
    
    assert (response.status_code == 200)
    assert data ==  {
                    "locate": {'lat': 48.8975156, 'lng': 2.3833993},
                    "address": '10 Quai de la Charente, 75019 Paris, France',
                    "messages": ["Bien sûr mon poussin ! La voici: ", "Ça ne me dit rien du tout!!"],
                    "question": "openclassrooms",
                }

def test_ajax_response_from_Google_API_and_Wikipedia(client, mocker):

    mocker.patch(
        "flaskapp.backend.API.Google.geoloc", return_value={"locate": {
                                'lat': 48.8975156, 'lng': 2.3833993},
                                "district": 'Quai de la Charente',
                                "address": '10 Quai de la Charente, 75019 Paris, France',
                                "status": True,
                                }
    )

    mocker.patch(
        "flaskapp.backend.API.WikiMedia.get_infos",
        return_value={
                    "summary": "Un résumé de wikipedia", 
                    "url": "https://fr.wikipedia.org/wiki/OpenClassrooms", 
                    "status": True
                    }
    )

    mocker.patch(
        "flaskapp.backend.messages.Message.positive_address", return_value = "Bien sûr mon poussin ! La voici: ",
    )

    mocker.patch(
        "flaskapp.backend.messages.Message.positive_wiki", return_value = "J'y suis allé quand j'étais jeune, il y a 60 ans!:",
    )


    response = client.post("/ajax/?Question=openclassrooms", data = { 'Question': 'openclassrooms'} )

    data = json.loads(response.data)
    
    assert (response.status_code == 200)
    assert data ==  {
                    "locate": {'lat': 48.8975156, 'lng': 2.3833993},
                    "address": '10 Quai de la Charente, 75019 Paris, France',
                    "messages": ["Bien sûr mon poussin ! La voici: ", "J'y suis allé quand j'étais jeune, il y a 60 ans!:"],
                    "question": "openclassrooms",
                    "summary": "Un résumé de wikipedia", 
                    "url": "https://fr.wikipedia.org/wiki/OpenClassrooms",
                }