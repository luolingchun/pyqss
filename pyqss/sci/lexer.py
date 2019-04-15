# -*- coding: utf-8 -*-
# @Time    : 2019/4/11 13:59
# @Author  : llc
# @File    : lexer.py
import re

from PyQt5.Qsci import QsciLexerCustom, QsciAPIs, QsciScintilla
from PyQt5.QtGui import QColor, QFont
from .apis import *


class QsciLexerQSS(QsciLexerCustom):
    def __init__(self, parent=None):
        super(QsciLexerQSS, self).__init__(parent)

        self.setDefaultColor(QColor(248, 248, 248))  # 默认前景色
        self.setDefaultPaper(QColor(39, 40, 34))  # 默认背景色
        self.setDefaultFont(QFont("Consolas", 12))  # 默认字体

        # 样式
        self.__styles = {
            "Default": 0,
            "Widgets": 1,
            "Properties": 2,
            "Numbers": 3,
            'Colors': 4,
        }

        self.__widgets = widgets
        self.__properties = properties
        self.__numbers = numbers
        self.__colors = colors

        self.__init_colors()

        # api
        self.__apis = self.__widgets + properties + colors + sub_controls
        self.__api = QsciAPIs(self)

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

    def language(self):
        return "QSS"

    def __init_colors(self):
        # 字体颜色
        self.setColor(QColor(255, 255, 255), self.__styles["Default"])
        self.setColor(QColor(165, 197, 39), self.__styles["Widgets"])
        self.setColor(QColor(102, 217, 239), self.__styles["Properties"])
        self.setColor(QColor(174, 129, 255), self.__styles["Numbers"])
        self.setColor(QColor(104, 232, 104), self.__styles["Colors"])
        # 背景颜色
        # for i in range(len(self.__styles)):
        #     self.setPaper(QColor(39, 40, 34), i)

    def add_object_names(self):
        main_window = self.parent().parent()
        if main_window:
            if main_window.objectName():
                self.__widgets.append(main_window.objectName())
                self.__apis.append(main_window.objectName())
            self.__append_object_names(main_window)
        # 初始化api
        for _api in self.__apis:
            self.__api.add(_api)
        self.__api.prepare()

    def __append_object_names(self, widget):
        for child in widget.children():
            if child.objectName():
                self.__widgets.append(child.objectName())
                self.__apis.append(child.objectName())
            self.__append_object_names(child)

    def styleText(self, start, end):
        self.startStyling(start)
        splitter = re.compile(r"\s+|\d|\w+-\w+|\w+|\W")
        text = self.parent().text()[start:end]
        tokens = [(token, len(bytearray(token, "utf-8"))) for token in splitter.findall(text)]
        # print(tokens)
        for i, token in enumerate(tokens):
            if token[0] in self.__widgets:
                self.setStyling(token[1], self.__styles["Widgets"])
            elif token[0] in self.__properties:
                self.setStyling(token[1], self.__styles["Properties"])
            elif token[0] in self.__numbers:
                self.setStyling(token[1], self.__styles["Numbers"])
            elif token[0] in self.__colors:
                self.setStyling(token[1], self.__styles["Colors"])
            else:
                self.setStyling(token[1], self.__styles["Default"])

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
