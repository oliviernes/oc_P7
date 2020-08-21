#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unidecode
import re
import pdb

from config import EXTRA_WORDS, STOP_WORDS


class Parser:
    """Class which allow to parse sentences"""

    def __init__(self):
        self.erase_words = EXTRA_WORDS + STOP_WORDS

    def parse(self, phrase):
        """Parse a phrase"""
        phrase_no_accents = unidecode.unidecode(phrase)
        phrase_lower = phrase_no_accents.lower()
        phrase_alphanum = re.sub("[^A-Za-z0-9-]+", " ", phrase_lower)
        phrase_sliced = phrase_alphanum.split()
        words = [word for word in phrase_sliced if word not in self.erase_words]
        search_words = " ".join(words)
        return search_words
