#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unidecode
import re
import pdb

from config import EXTRA_WORDS, STOP_WORDS

def parser(phrase):
    """"Parse a phrase"""
    ERASE_WORDS = EXTRA_WORDS + STOP_WORDS
    
    phrase_no_accents = unidecode.unidecode(phrase)
    phrase_lower = phrase_no_accents.lower()
    phrase_alphanum = re.sub('[^A-Za-z0-9-]+', ' ', phrase_lower)
    phrase_sliced = phrase_alphanum.split()
    search_word = [word for word in phrase_sliced if word not in ERASE_WORDS]
    return search_word[0]
    
