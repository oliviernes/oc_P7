import pytest
from parser import parser

def test_parser_phrase():
    phrase = "Salut Grandpy, raconte moi à propos d'Openclassrooms."
    phrase_parsed = parser(phrase)
    
    assert phrase_parsed == "openclassrooms"

def test_parser_adresse():
    adresse = "Bonjour Grandpy, dis moi ce que tu sais à propos du 7 Cité Paradis, 75010 Paris"
    phrase_parsed = parser(adresse)

    assert phrase_parsed == "7 cite paradis 75010 paris"
