import pytest
from parser import Parser

def test_parser_adresse():
    adresse = "Bonjour Grandpy, dis moi ce que tu sais à propos du 7 Cité Paradis, 75010 Paris"
    phrase_parsed = Parser()

    assert phrase_parsed.parse(adresse) == "7 cite paradis 75010 paris"

