# -*- coding: utf-8 -*-
# @Time    : 2019/4/11 14:01
# @Author  : llc
# @File    : editor.py

from PyQt5.Qsci import QsciScintilla, QsciAPIs
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QColor, QKeySequence
from PyQt5.QtWidgets import QShortcut, QApplication

from .commenter import toggle_commenting
from .lexer import QsciLexerQSS
from .keywords import *


class QssEditor(QsciScintilla):
    def __init__(self, parent=None):
        super(QssEditor, self).__init__(parent=parent)

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
        self.lexer = QsciLexerQSS(self)
        self.setLexer(self.lexer)
        # API
        self.api = QsciAPIs(self.lexer)
        self.api_list = API_LIST
        for p in PROPERTY_LIST:
            self.api_list.extend(p.split('-'))

        # 括号匹配
        self.setBraceMatching(QsciScintilla.SloppyBraceMatch)  # 括号匹配
        self.setMatchedBraceBackgroundColor(QColor(58, 109, 160))  # 括号匹配背景色

        # 选择
        self.selectionToEol()
        self.resetSelectionForegroundColor()  # 选中文字，文字不变成白色
        self.setSelectionBackgroundColor(QColor(33, 66, 131))  # 选中文字背景色

        # 缩放
        # self.zoomTo(4)  # 缩放因子
        self.margin_width = self.marginWidth(0)
        # self.SCN_ZOOM.connect(self.set_width)

        # 行数变化
        self.linesChanged.connect(self.onLinesChanged)

        # # 多光标支持
        self.SendScintilla(QsciScintilla.SCI_SETMULTIPLESELECTION, True)
        self.SendScintilla(QsciScintilla.SCI_SETMULTIPASTE, 1)
        self.SendScintilla(QsciScintilla.SCI_SETADDITIONALSELECTIONTYPING, True)

        # 其它
        self.setUtf8(True)
        self.setEdgeMode(QsciScintilla.EDGE_NONE)  # 行字数超过50时什么也不做，默认背景标记为绿色

        QShortcut(QKeySequence("Ctrl+0"), self, self.test)

    def test(self):
        print('test')

    def onLinesChanged(self):
        self.setMarginWidth(0, self.fontMetrics().width(str(self.lines())) + 18)

    def add_apis(self, custom_widget):
        """添加api，用于自动补全"""
        if custom_widget:
            if custom_widget.objectName():
                self.lexer.widgets.append(custom_widget.objectName())
                self.api_list.append(custom_widget.objectName())
            self.get_object_names(custom_widget)

        # 初始化api
        for api in self.api_list:
            self.api.add(api)
        self.api.prepare()

    def get_object_names(self, widget):
        """遍历widget及其后代，获得objectName，用于自动补全"""
        for child in widget.children():
            if child.objectName():
                self.lexer.widgets.append(child.objectName())
                self.api_list.append(child.objectName())
            self.get_object_names(child)

    def keyPressEvent(self, event):
        key = event.key()
        key_modifiers = QApplication.keyboardModifiers()
        if key == Qt.Key_Slash and key_modifiers == Qt.ControlModifier:
            # 注释快捷键，Ctrl+/
            toggle_commenting(self)
            return
        # elif key == Qt.Key_Return:
        # 括号缩进,TODO
        # pos = self.getCursorPosition()
        # pos_text = self.wordCharacters()
        # print(pos_text)
        # super(QssEditor, self).keyPressEvent(event)
        # if pos_text and pos_text[-2:] == '{}':
        #     self.insert("\n")
        #     self.insert('	')
        #     self.setCursorPosition(pos[0], pos[1] + 2)
        # return
        super(QssEditor, self).keyPressEvent(event)
