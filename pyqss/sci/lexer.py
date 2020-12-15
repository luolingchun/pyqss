# -*- coding: utf-8 -*-
# @Time    : 2019/4/11 13:59
# @Author  : llc
# @File    : lexer.py
import re

from PyQt5.Qsci import QsciLexerCustom, QsciScintillaBase
from PyQt5.QtGui import QColor, QFont

from .keywords import *

BACKGROUND_COLOR = QColor(20, 20, 20)


class QsciLexerQSS(QsciLexerCustom):
    flags = {
        "String": False,
        "Comment": False,
    }
    styles = {
        "Default": 0,
        "Widget": 1,
        "Property": 2,
        "Number": 3,
        'Color': 4,
        'Comment': 5,
        "String": 6,
    }

    def __init__(self, parent=None):
        super(QsciLexerQSS, self).__init__(parent)
        self.setDefaultColor(QColor(248, 248, 248))  # 默认前景色
        self.setDefaultPaper(BACKGROUND_COLOR)  # 默认背景色
        self.setDefaultFont(QFont("Consolas", 12))  # 默认字体

        # 字体颜色
        self.setColor(QColor(255, 255, 255), self.styles["Default"])
        self.setColor(QColor(165, 197, 39), self.styles["Widget"])
        self.setColor(QColor(102, 217, 239), self.styles["Property"])
        self.setColor(QColor(174, 129, 255), self.styles["Number"])
        self.setColor(QColor(104, 232, 104), self.styles["Color"])
        self.setColor(QColor(117, 113, 94), self.styles["Comment"])
        self.setColor(QColor(230, 219, 116), self.styles["String"])

        self.widgets = WIDGET_LIST

    def description(self, style):
        if style == 0:
            return 'Default'
        elif style == 1:
            return 'Widget'
        elif style == 2:
            return 'Property'
        elif style == 3:
            return 'Number'
        elif style == 4:
            return 'Color'
        elif style == 5:
            return 'Comment'
        elif style == 6:
            return 'String'

    def language(self):
        return "QSS"

    def styleText(self, start, end):
        editor = self.parent()
        for k in self.flags.keys():
            self.flags[k] = False

        self.startStyling(start)
        splitter = re.compile(
            r"({\.|\.}|#|\'|\"\"\"|\n|\".*\"|\d|\w+-\w+-\w+-\w+-\w+|\w+-\w+-\w+-\w+|\w+-\w+-\w+|\w+-\w+|\w+|\W)")
        text = editor.text()[start:end]
        tokens = [(token, len(bytearray(token, "utf-8"))) for token in splitter.findall(text)]
        if start != 0:
            previous_style = editor.SendScintilla(QsciScintillaBase.SCI_GETSTYLEAT, start - 1)
            if previous_style == self.styles["Comment"]:
                self.flags["Comment"] = True
            # Initialize token variables
        previous_token_text = ""
        token_text = ""
        # next_token_text = ""
        for i, token in enumerate(tokens):
            # Save previous token
            if token_text != "":
                previous_token_text = token_text
            # Set the current and next token information
            token_text = token[0]
            next_token_text = ""
            if len(tokens) > i + 1:
                next_token_text = tokens[i + 1][0]
            token_length = token[1]

            # comment
            if self.flags["Comment"]:
                self.setStyling(token_length, self.styles["Comment"])
                if previous_token_text.strip() == "*" and token_text.strip() == "/":
                    self.flags["Comment"] = False
                continue
            else:
                if token_text == "/" and next_token_text == "*":
                    self.setStyling(token_length, self.styles["Comment"])
                    self.flags["Comment"] = True
                    continue

            # Sprecial token styling
            if token_text in self.widgets or token_text in PSEUDO_STATE_LIST or token_text in SUB_CONTROL_LIST:
                self.setStyling(token_length, self.styles["Widget"])
            elif token_text in PROPERTY_LIST:
                self.setStyling(token_length, self.styles["Property"])
            elif token_text.isdigit():
                self.setStyling(token_length, self.styles["Number"])
            elif token_text in COLOR_LIST or token_text in PROPERTY_TYPE_LIST:
                self.setStyling(token_length, self.styles["Color"])
            elif token_text.startswith('"') and token_text.endswith('"'):
                self.setStyling(token_length, self.styles["String"])
            else:
                # Style with the default style
                self.setStyling(token_length, self.styles["Default"])

        # Folding
        lines = editor.text().splitlines()
        # Initialize the folding variables
        fold_level = 0
        # folding = False
        # Folding loop
        for line_number, line in enumerate(lines):
            # Add folding points as needed
            open_count = line.count('{')
            close_count = line.count('}')
            if open_count > 0:
                # Set the line's folding level first, so that the closing curly brace is added to the fold
                editor.SendScintilla(QsciScintillaBase.SCI_SETFOLDLEVEL, line_number,
                                     fold_level | QsciScintillaBase.SC_FOLDLEVELHEADERFLAG)
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
                editor.SendScintilla(QsciScintillaBase.SCI_SETFOLDLEVEL, line_number,
                                     fold_level | QsciScintillaBase.SC_FOLDLEVELHEADERFLAG)
            # print(fold_level)
        # Reset the fold level of the last line
        editor.SendScintilla(QsciScintillaBase.SCI_SETFOLDLEVEL, len(lines), 0)
