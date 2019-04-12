# -*- coding: utf-8 -*-
# @Time    : 2019/4/11 13:59
# @Author  : llc
# @File    : lexer.py
import re

from PyQt5.Qsci import QsciLexerCustom
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
        }

        self.__widgets = widget_list
        self.__properties = propertie_list
        self.__numbers = number_list

        self.__init_colors()
        self.__get_object_names()

    def description(self, style):
        if style == 0:
            return 'Default'
        elif style == 1:
            return 'Widgets'
        elif style == 2:
            return 'Properties'
        elif style == 3:
            return 'Numbers'

    def language(self):
        return "QSS"

    def __init_colors(self):
        # 字体颜色
        self.setColor(QColor(255, 255, 255), self.__styles["Default"])
        self.setColor(QColor(165, 197, 39), self.__styles["Widgets"])
        self.setColor(QColor(102, 217, 239), self.__styles["Properties"])
        self.setColor(QColor(174, 129, 255), self.__styles["Numbers"])
        # 背景颜色
        # for i in range(len(self.__styles)):
        #     self.setPaper(QColor(39, 40, 34), i)

    def __get_object_names(self):
        main_window = self.parent().parent()
        if main_window:
            self.__widgets.append(main_window.objectName())
            self.__append_object_names(main_window)

    def __append_object_names(self, widget):
        for child in widget.children():
            self.__widgets.append(child.objectName())
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
            else:
                # Style with the default style
                self.setStyling(token[1], self.__styles["Default"])
