# -*- coding: utf-8 -*-
import pymorphy2

pymorph = pymorphy2.MorphAnalyzer()


def normalize_word(word):
    tags = pymorph.parse(word)
    if tags:
        return tags[0].normal_form
    else:
        return word
