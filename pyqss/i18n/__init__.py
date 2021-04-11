# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2021/4/11 13:27
import json
import os

_here = os.path.dirname(__file__)


def init_tr(language):
    tr_json = os.path.join(_here, f'{language}.json')
    if not os.path.exists(tr_json):
        tr_json = os.path.join(_here, 'zh.json')
    with open(tr_json, 'r', encoding='utf-8') as f:
        words = json.load(f)

    def tr(word):
        tr_word = words.get(word)
        if tr_word:
            return tr_word
        else:
            return word

    return tr
