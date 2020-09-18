import pytest
from flaskapp.backend.api import Google, WikiMedia, GetJson

class TestApi:
    """Test the api response management."""

    def test_geoloc_return_OK(self, mocker):
        results = {
            "results": [
                {
                    "geometry": {"location": {
                                            "lat": 48.8747265,
                                            "lng": 2.3505517
                                            }
                                 },
                    "formatted_address": "7 Cité Paradis, 75010 Paris,"
                    " France",
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
                            "types": ["administrative_area_level_2",
                                      "political"],
                        },
                        {
                            "long_name": "Île-de-France",
                            "short_name": "IDF",
                            "types": ["administrative_area_level_1",
                                      "political"],
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

        mocker.patch(
                    "flaskapp.backend.api.GetJson.get_json",
                    return_value=results
                    )

        goggle = Google()

        assert goggle.geoloc("openclassrooms") == {
            "locate": {"lat": 48.8747265, "lng": 2.3505517},
            "address": "7 Cité Paradis, 75010 Paris, France",
            "district": "Cité Paradis",
            "status": True,
        }

    def test_geoloc_zero_results(self, mocker):
        results = {"results": [], "status": "ZERO_RESULTS"}

        mocker.patch(
                    "flaskapp.backend.api.GetJson.get_json",
                    return_value=results
                    )

        goggle = Google()

        assert goggle.geoloc("zero_results") == {"status": False}

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

        mocker.patch(
                    "flaskapp.backend.api.MediaWiki.search",
                    return_value=titles
                    )
        mocker.patch(
                    "flaskapp.backend.api.MediaWiki.page",
                    return_value=Page()
                    )
        mocker.patch(
                    "flaskapp.backend.api.MediaWiki.summary",
                    return_value=summary
                    )
        mocker.patch(
                    "flaskapp.backend.api.MediaWiki.page.url",
                    return_value=url
                    )

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

        mocker.patch(
                    "flaskapp.backend.api.MediaWiki.search",
                    return_value=titles
                    )

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
                                    "types": ["street_number"],
                                },
                            ],
                        }
                    ],
                    "status": "OK",
                }

            def raise_for_status(self):
                return "nothing"

        response = Requests()

        get = GetJson(GEOCODE_URL, payload)

        mocker.patch(
                    "flaskapp.backend.api.requests.get",
                    return_value=response
                    )

        assert get.get_json() == response.json()
