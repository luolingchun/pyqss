# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/3/18 17:00
import json
import os

cwd = os.path.dirname(__file__)


def init_language(language):
    tr_json = os.path.join(cwd, 'i18n', f'{language}.json')
    if not os.path.exists(tr_json):
        tr_json = os.path.join(cwd, 'i18n', 'zh.json')
    with open(tr_json, 'r', encoding='utf-8') as f:
        words = json.load(f)

    def tr(word):
        tr_word = words.get(word)
        if tr_word:
            return tr_word
        else:
            return word

    return tr
