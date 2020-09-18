import pytest
from flaskapp.backend.parser import Parser


class TestParser:
    """Class testing the parser"""

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
        adresse = "a abord absolument afin ah ai aie ailleurs ainsi ait"
        phrase_parsed = Parser()

        assert phrase_parsed.parse(adresse) == ""

    def test_parser_apostrophe(self):
        adresse = "Bonjour Grandpy, dis moi ce que tu sais à propos" \
         " d'Openclassrooms"
        phrase_parsed = Parser()

        assert phrase_parsed.parse(adresse) == "openclassrooms"
