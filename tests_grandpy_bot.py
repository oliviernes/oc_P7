import json
import pytest
from flaskapp.backend.parser import Parser
from flaskapp.backend.API import Google

def test_parser_adresse():
    adresse = "Bonjour Grandpy, dis moi ce que tu sais à propos du 7 Cité Paradis, 75010 Paris"
    phrase_parsed = Parser()

    assert phrase_parsed.parse(adresse) == "7 cite paradis 75010 paris"

def test_parser_empty_string():
    adresse = ""
    phrase_parsed = Parser()

    assert phrase_parsed.parse(adresse) == ""

def test_parser_STOP_WORDS_only():
    adresse = "a abord absolument afin ah ai aie ailleurs ainsi ait allaient"
    phrase_parsed = Parser()

    assert phrase_parsed.parse(adresse) == ""

class TestAPI:
    """Test the API response management."""

    def test_geoloc_return(self, mocker):
        result = {
            "results" :[
                    {
                        'place_id' : "ChIJxfB-lhRu5kcRfK7MP5oTfH8",
                        'geometry' : {
                                        'location' : {'lat': 48.8747265, 'lng': 2.3505517}
                                    }
                    }
                ],
        }

        mocker.patch('flaskapp.backend.API.Get_json.get_json', return_value = result)

        goggle = Google()

        assert goggle.geoloc('openclassrooms') == { 'locate': {'lat': 48.8747265, 'lng': 2.3505517}, 'place_id': "ChIJxfB-lhRu5kcRfK7MP5oTfH8" }
