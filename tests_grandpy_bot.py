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
        results = {
            "results": [
                {
                    "geometry": {"location": {"lat": 48.8747265, "lng": 2.3505517}},
                    "formatted_address": "7 Cité Paradis, 75010 Paris, France",
                    "address_components": [{'long_name': '7', 'short_name': '7', 'types': ['street_number']}, {'long_name': 'Cité Paradis', 'short_name': 'Cité Paradis', 'types': ['route']}, {'long_name': 'Paris', 'short_name': 'Paris', 'types': ['locality', 'political']}, {'long_name': 'Arrondissement de Paris', 'short_name': 'Arrondissement de Paris', 'types': ['administrative_area_level_2', 'political']}, {'long_name': 'Île-de-France', 'short_name': 'IDF', 'types': ['administrative_area_level_1', 'political']}, {'long_name': 'France', 'short_name': 'FR', 'types': ['country', 'political']}, {'long_name': '75010', 'short_name': '75010', 'types': ['postal_code']}],
                }
            ],
            "status": "OK"
        }

        mocker.patch("flaskapp.backend.API.Get_json.get_json", return_value=results)

        goggle = Google()

        assert goggle.geoloc("openclassrooms") == {
            "locate": {"lat": 48.8747265, "lng": 2.3505517},
            "address": "7 Cité Paradis, 75010 Paris, France",
            "district": "Cité Paradis",
        }

    # def test_get_infos(self, mocker):
        
