# -*- coding: utf-8 -*-
# @Time    : 2019/4/11 14:01
# @Author  : llc
# @File    : editor.py

from PyQt5.Qsci import QsciScintilla, QsciAPIs
from PyQt5.QtCore import Qt, QUrl, pyqtSignal
from PyQt5.QtGui import QColor, QKeySequence
from PyQt5.QtWidgets import QShortcut, QApplication

from .commenter import toggle_commenting
from .lexer import QsciLexerQSS
from .keywords import *


class QssEditor(QsciScintilla):
    opened = pyqtSignal(str)

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
        self.setEdgeColor(QColor("#ff00ff00"))

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

        # 左侧栏-行号
        self.setMarginLineNumbers(0, QsciScintilla.NumberMargin)
        self.setMarginWidth(0, "00000")
        self.setMarginsForegroundColor(QColor(163, 163, 163))  # 前景色
        self.setMarginsBackgroundColor(QColor(43, 43, 43))  # 背景色
        # 左侧栏-符号
        self.setMarginLineNumbers(1, QsciScintilla.SymbolMargin)
        self.setMarginWidth(1, 0)
        self.setMarginSensitivity(1, True)
        # self.marginClicked.connect(self.marginClickedFunc)
        # 左侧栏-折叠
        self.setFolding(QsciScintilla.PlainFoldStyle, 2)  # 折叠
        self.setMarginWidth(2, "00")
        self.setFoldMarginColors(QColor(43, 43, 43), QColor(43, 43, 43))

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

        # self.textChanged.connect(self.textChangedFunc)
        #
        # self.markerDefine(create_image(QColor(0, 128, 0)), 0)

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
        elif key == Qt.Key_BraceLeft:
            # 自动添加右括号
            self.insert("}")
        elif key == Qt.Key_ParenLeft:
            # 自动添加右括号
            self.insert(")")
        elif key == Qt.Key_Backspace:
            line, index = self.getCursorPosition()
            line_text = self.text(line)
            # print(line_text)
            if line_text[index - 1:index + 1].strip() == "{}":
                self.setSelection(line, index - 1, line, index + 1)
                self.removeSelectedText()
                return
        elif key == Qt.Key_Return:
            # 括号自动缩进
            line, index = self.getCursorPosition()
            line_text = self.text(line)
            # print(line_text)
            if line_text[index - 1::].strip() == "{}":
                super(QssEditor, self).keyPressEvent(event)
                self.insert("\n")
                self.indent(line + 1)
                self.setCursorPosition(line + 1, 1)
                return
            elif line_text[index - 1::].strip() == "{":
                super(QssEditor, self).keyPressEvent(event)
                self.indent(line + 1)
                self.setCursorPosition(line + 1, 1)
                return
        super(QssEditor, self).keyPressEvent(event)

    def dragEnterEvent(self, event):
        data = event.mimeData()
        if data.hasUrls():
            url = QUrl(data.text())
            if url.isLocalFile() and url.path().endswith(".qss"):
                event.accept()
            else:
                event.ignore()
        else:
            event.ignore()

    def dropEvent(self, event):
        data = event.mimeData()
        if data.hasUrls():
            url = QUrl(data.text())
            if url.isLocalFile() and url.path().endswith(".qss"):
                event.accept()
                qss_file = url.path().lstrip('/')
                with open(url.path().lstrip('/'), 'r') as f:
                    qss_text = f.read()
                self.setText(qss_text)
                self.opened.emit(qss_file)
            else:
                event.ignore()
        else:
            event.ignore()
