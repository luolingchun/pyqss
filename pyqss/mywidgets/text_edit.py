# -*- coding: utf-8 -*-
# @Time    : 2019/3/22 14:23
# @Author  : llc
# @File    : text_edit.py
from PyQt5.QtGui import QTextCursor, QCursor
from PyQt5.QtWidgets import QTextEdit, QMenu
from PyQt5.QtCore import Qt


class NewTextEdit(QTextEdit):
    def __init__(self, *__args):
        super(NewTextEdit, self).__init__(*__args)

        # self.setContextMenuPolicy(Qt.CustomContextMenu)
        # self.customContextMenuRequested.connect(self.show_contextmenu)
        # self.textChanged.connect(self.show_contextmenu)

    def show_contextmenu(self):
        cursor = self.textCursor()
        self.contextmenu = QMenu(self)
        self.action_delete = self.contextmenu.addAction('删除')
        self.contextmenu.exec_()

    def get_word_cursor(self):
        cursor = self.textCursor()
        while cursor.movePosition(QTextCursor.Left, QTextCursor.KeepAnchor):
            if ' ' in cursor.selectedText():
                break
        return cursor.selectedText().strip()
