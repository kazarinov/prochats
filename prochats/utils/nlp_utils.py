# -*- coding: utf-8 -*-
from nltk.stem.snowball import RussianStemmer

stemmer = RussianStemmer()


def normalize_word(word):
    return stemmer.stem(word)