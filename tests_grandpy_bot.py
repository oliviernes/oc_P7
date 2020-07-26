import pytest

def test_parser():
    phrase = "Salut Grandpy, raconte moi à propos d'Openclassrooms."
    phrase_parse = parser(phrase)
    
    assert phrase_parse == "openclassrooms"
