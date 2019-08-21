# -*- coding: utf-8 -*-
# @Time    : 2019/4/11 14:01
# @Author  : llc
# @File    : editor.py

from PyQt5.Qsci import QsciScintilla
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

from .lexer import QsciLexerQSS


class TextEdit(QsciScintilla):
    def __init__(self, parent=None, custom_widget=None):
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
        self.setAutoCompletionCaseSensitivity(False)  # 不区分大小写,好像没用
        self.setAutoCompletionReplaceWord(False)  # 不替换光标右侧的单词
        self.setAutoCompletionSource(QsciScintilla.AcsAll)
        self.setAutoCompletionThreshold(1)  # 输入1个字符立即显示
        # self.setAutoCompletionUseSingle(QsciScintilla.AcusAlways) #当只有一个时自动填充

        # 左侧栏
        self.setMarginLineNumbers(0, True)  # 行号
        self.setMarginWidth(1, 0)  # 第二列不显示
        self.setFolding(QsciScintilla.PlainFoldStyle, 2)  # 折叠
        self.setMarginWidth(2, 12)
        self.setFoldMarginColors(QColor(39, 40, 34), QColor(39, 40, 34))
        self.setMarginWidth(0, "00000")
        self.setMarginSensitivity(0, True)
        self.setMarginsForegroundColor(QColor(163, 163, 163))  # 前景色
        self.setMarginsBackgroundColor(QColor(39, 40, 34))  # 背景色

        # 滚动条
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 隐藏横向滚动条

        # 语法分析器
        self.lexer = QsciLexerQSS(self, custom_widget)
        self.setLexer(self.lexer)

        # 括号匹配
        self.setBraceMatching(QsciScintilla.SloppyBraceMatch)  # 括号匹配
        self.setMatchedBraceBackgroundColor(QColor(58, 109, 160))  # 括号匹配背景色

        # 选择
        self.selectionToEol()
        self.resetSelectionForegroundColor()  # 选中文字，文字不变成白色
        self.setSelectionBackgroundColor(QColor(110, 109, 98))  # 选中文字背景色

        # 缩放
        # self.zoomTo(4)  # 缩放因子
        self.margin_width = self.marginWidth(0)
        # self.SCN_ZOOM.connect(self.set_width)

        # 行数变化
        self.linesChanged.connect(self.onLinesChanged)

        # 其它
        self.setUtf8(True)
        self.setEdgeMode(QsciScintilla.EDGE_NONE)  # 行字数超过50时什么也不做，默认背景标记为绿色

    def onLinesChanged(self):
        self.setMarginWidth(0, self.fontMetrics().width(str(self.lines())) + 18)

    # def set_width(self):
    #     self.setMarginWidth(0, self.SendScintilla(self.SCI_GETZOOM) + self.marginWidth(0) + 18)

    # def keyPressEvent(self, event):
    #     if event.modifiers()==Qt.ControlModifier and event.key() == Qt.Key_Slash:  # 斜线 /
    #         # 快捷键 ctrl+/
    #         print(111111111111111111)
    #     else:
    #         super(TextEdit, self).keyPressEvent(event)