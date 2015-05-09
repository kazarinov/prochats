# -*- coding: utf-8 -*-
import pymorphy2

pymorph = pymorphy2.MorphAnalyzer()


def normalize_word(word):
    return pymorph.parse(word).normal_form
