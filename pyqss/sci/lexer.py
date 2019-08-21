# -*- coding: utf-8 -*-
# @Time    : 2019/4/11 13:59
# @Author  : llc
# @File    : lexer.py
import re

from PyQt5.Qsci import QsciLexerCustom, QsciAPIs, QsciScintilla
from PyQt5.QtGui import QColor, QFont
from .apis import *


class QsciLexerQSS(QsciLexerCustom):
    def __init__(self, parent=None, custom_widget=None):
        super(QsciLexerQSS, self).__init__(parent)
        self.custom_widget = custom_widget
        self.setDefaultColor(QColor(248, 248, 248))  # 默认前景色
        self.setDefaultPaper(QColor(39, 40, 34))  # 默认背景色
        self.setDefaultFont(QFont("Consolas", 12))  # 默认字体

        # 样式
        self._styles = {
            "Default": 0,
            "Widgets": 1,
            "Properties": 2,
            "Numbers": 3,
            'Colors': 4,
            'Annotation': 5,
        }

        self._widgets = widgets
        self._properties = properties
        self._numbers = numbers
        self._colors = colors

        self._init_colors()

        # api
        self._apis = self._widgets + properties + pseudo_states + colors + sub_controls
        self._api = QsciAPIs(self)

    def description(self, style):
        if style == 0:
            return 'Default'
        elif style == 1:
            return 'Widgets'
        elif style == 2:
            return 'Properties'
        elif style == 3:
            return 'Numbers'
        elif style == 4:
            return 'Colors'
        elif style == 5:
            return 'Annotation'

    def language(self):
        return "QSS"

    def _init_colors(self):
        # 字体颜色
        self.setColor(QColor(255, 255, 255), self._styles["Default"])
        self.setColor(QColor(165, 197, 39), self._styles["Widgets"])
        self.setColor(QColor(102, 217, 239), self._styles["Properties"])
        self.setColor(QColor(174, 129, 255), self._styles["Numbers"])
        self.setColor(QColor(104, 232, 104), self._styles["Colors"])
        self.setColor(QColor(117, 113, 94), self._styles["Annotation"])
        # 背景颜色
        # for i in range(len(self._styles)):
        #     self.setPaper(QColor(39, 40, 34), i)

    def add_object_names(self):
        main_window = self.custom_widget
        if main_window:
            if main_window.objectName():
                self._widgets.append(main_window.objectName())
                self._apis.append(main_window.objectName())
            self.__append_object_names(main_window)
        # 初始化api
        for _api in self._apis:
            self._api.add(_api)
        self._api.prepare()

    def __append_object_names(self, widget):
        for child in widget.children():
            if child.objectName():
                self._widgets.append(child.objectName())
                self._apis.append(child.objectName())
            self.__append_object_names(child)

    def styleText(self, start, end):
        self.startStyling(start)
        splitter = re.compile(r"\/\*.*\*\/|s+|\d|\w+-\w+-\w+-\w+-\w+|\w+-\w+-\w+-\w+|\w+-\w+-\w+|\w+-\w+|\w+|\W")
        text = self.parent().text()[start:end]
        tokens = [(token, len(bytearray(token, "utf-8"))) for token in splitter.findall(text)]
        # print(tokens)
        for i, token in enumerate(tokens):
            if token[0] in self._widgets:
                self.setStyling(token[1], self._styles["Widgets"])
            elif token[0] in self._properties:
                self.setStyling(token[1], self._styles["Properties"])
            elif token[0] in self._numbers:
                self.setStyling(token[1], self._styles["Numbers"])
            elif token[0] in self._colors:
                self.setStyling(token[1], self._styles["Colors"])
            elif token[0].startswith('/*') or token[0].endswith('*/'):
                self.setStyling(token[1], self._styles["Annotation"])
            else:
                self.setStyling(token[1], self._styles["Default"])

        # 折叠
        lines = self.parent().text().splitlines()
        editor = self.parent()
        fold_level = 0
        editor.SendScintilla(QsciScintilla.SCI_SETFOLDLEVEL, 0, QsciScintilla.SC_FOLDLEVELHEADERFLAG)
        for line_number, line in enumerate(lines):
            # Add folding points as needed
            open_count = line.count('{')
            close_count = line.count('}')
            if close_count > 0:
                # Set the line's folding level first, so that the closing curly brace is added to the fold
                editor.SendScintilla(QsciScintilla.SCI_SETFOLDLEVEL, line_number + 1,
                                     fold_level | QsciScintilla.SC_FOLDLEVELHEADERFLAG)
                # Adjust the folding level
                fold_level += open_count
                fold_level -= close_count
            else:
                # Adjust the folding level first
                fold_level += open_count
                fold_level -= close_count
                if fold_level <= 0:
                    fold_level = 0
                # Set the line's adjusted folding level
                editor.SendScintilla(QsciScintilla.SCI_SETFOLDLEVEL, line_number + 1,
                                     fold_level | QsciScintilla.SC_FOLDLEVELHEADERFLAG)
            # print(fold_level)
        # Reset the fold level of the last line
        editor.SendScintilla(QsciScintilla.SCI_SETFOLDLEVEL, len(lines) - 1, 0)
