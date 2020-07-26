import pytest
from parser import parser

def test_parser():
    phrase = "Salut Grandpy, raconte moi à propos d'Openclassrooms."
    phrase_parsed = parser(phrase)
    
    assert phrase_parsed == "openclassrooms"
