import pytest
from parser import Parser

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
