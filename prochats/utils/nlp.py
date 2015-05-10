# -*- coding: utf-8 -*-
import pymorphy2
from stop_words import get_stop_words


pymorph = pymorphy2.MorphAnalyzer()
stop_words = get_stop_words('russian')


def normalize_word(word, types=None):
    if not types:
        types = ['NOUN']

    tags = pymorph.parse(word)
    if tags:
        tag = tags[0]
        norm_word = tag.normal_form
        if len(word) <= 1 or norm_word in stop_words or tag.tag.POS not in types:
            return None
        else:
            return norm_word
    else:
        return word
