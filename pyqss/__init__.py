# -*- coding: utf-8 -*-
# @Time    : 2019/3/22 9:53
# @Author  : llc
# @File    : __init__.py.py

__version__ = '0.0.1'

from PyQt5.QtWidgets import QMainWindow, QGridLayout, QWidget, QHBoxLayout, QPushButton, QSpacerItem, QSizePolicy, \
    QCompleter
from .mywidgets.text_edit import NewTextEdit
from .config import completer_str_list


class Qss(QMainWindow):
    def __init__(self, custom_window=None):
        super(Qss, self).__init__()
        self.custom_window = custom_window

        self.setup_ui()
        self.setWindowTitle('QSS编辑器')

        self.text_edit.textChanged.connect(self.text_edit_textChanged)

    def text_edit_textChanged(self):
        self.custom_window.setStyleSheet(self.text_edit.toPlainText())

    def setup_ui(self):
        self.central_widget = QWidget(self)
        self.grid_layout = QGridLayout(self.central_widget)
        self.widget = QWidget(self.central_widget)
        self.hl = QHBoxLayout(self.widget)
        self.pushButton_new = QPushButton('新建', self.widget)
        self.hl.addWidget(self.pushButton_new)
        self.pushButton_open = QPushButton('打开', self.widget)
        self.hl.addWidget(self.pushButton_open)
        self.pushButton_save = QPushButton('保存', self.widget)
        self.hl.addWidget(self.pushButton_save)
        self.hls = QSpacerItem(214, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.hl.addItem(self.hls)
        self.grid_layout.addWidget(self.widget, 0, 0, 1, 1)
        self.text_edit = NewTextEdit(self.central_widget)
        self.grid_layout.addWidget(self.text_edit, 1, 0, 1, 1)
        self.setCentralWidget(self.central_widget)


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    qss = Qss()
    qss.show()
    app.exec_()
