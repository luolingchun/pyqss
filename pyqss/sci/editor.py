# -*- coding: utf-8 -*-
# @Time    : 2019/4/11 14:01
# @Author  : llc
# @File    : editor.py

from PyQt5.Qsci import QsciScintilla, QsciLexerCSS, QsciAPIs
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor, QPalette, QFontMetrics
from .lexer import QsciLexerQSS


class TextEdit(QsciScintilla):
    def __init__(self,parent=None):
        super(TextEdit, self).__init__(parent)
        # 行尾字符
        self.setEolMode(QsciScintilla.EolUnix)
        # self.setEolVisibility(True)

        # 文字环绕
        self.setWrapMode(QsciScintilla.WrapWord)
        self.setWrapVisualFlags(QsciScintilla.WrapFlagByText)
        self.setWrapIndentMode(QsciScintilla.WrapIndentSame)

        # 边缘标记
        self.setEdgeMode(QsciScintilla.EdgeBackground)
        self.setEdgeColumn(50)
        edge_color = QColor("#ff00ff00")
        self.setEdgeColor(edge_color)

        # 缩进
        self.setTabWidth(4)
        self.setTabIndents(True)
        self.setAutoIndent(True)
        self.setBackspaceUnindents(True)
        self.setIndentationGuides(True)  # 显示缩进虚线

        # 闪烁的光标指示器
        self.setCaretWidth(2)  # 光标宽度
        self.setCaretLineVisible(True)  # 高亮显示选中的行
        self.setCaretForegroundColor(Qt.white)  # 闪烁光标颜色
        self.setCaretLineBackgroundColor(QColor(62, 61, 50))  # 选中行背景色

        # 自动补全
        self.setAutoCompletionCaseSensitivity(False)  # 不区分大小写
        self.setAutoCompletionReplaceWord(False)  # 不替换光标右侧的单词
        self.setAutoCompletionSource(QsciScintilla.AcsDocument)
        self.setAutoCompletionThreshold(1)  # 输入1个字符立即显示

        # 左侧栏
        self.setMarginType(0, QsciScintilla.NumberMargin)  # 行号
        self.setMarginLineNumbers(0, True)
        self.setMarginsForegroundColor(QColor(163, 163, 163))  # 前景色
        self.setMarginsBackgroundColor(QColor(39, 40, 34))  # 背景色
        self.setMarginWidth(0, "00000")
        self.setMarginSensitivity(0, True)

        # 滚动条
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 隐藏横向滚动条

        # 语法分析器
        lexer = QsciLexerQSS(self)
        self.setLexer(lexer)

        # 自动折叠
        # self.setMarginType(1, QsciScintilla.SymbolMargin)
        # self.setMarginLineNumbers(1, False)
        # self.setMarginWidth(1, 15)
        # self.setMarginSensitivity(1, True)

        # 括号匹配
        self.setBraceMatching(QsciScintilla.SloppyBraceMatch)  # 括号匹配
        self.setMatchedBraceBackgroundColor(QColor(58, 109, 160))  # 括号匹配背景色

        # 选择
        self.setSelectionBackgroundColor(QColor(110, 109, 98))  # 选中文字背景色

        # 其它
        # self.zoomTo(4)  # 缩放因子
        self.setUtf8(True)

        # 信号
        # self.SCN_ZOOM.connect(lambda :print(self.font().pointSize()))
