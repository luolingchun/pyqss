# -*- coding: utf-8 -*-
# @Time    : 2019/3/22 9:53
# @Author  : llc
# @File    : __init__.py
import os

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QKeySequence
from PyQt5.QtWidgets import QGridLayout, QWidget, QHBoxLayout, QPushButton, QSpacerItem, QSizePolicy, QFileDialog, \
    QShortcut, QLabel, QVBoxLayout

from pyqss.ui.frameless_window import FramelessWindow
from pyqss.sci.editor import TextEdit

__version__ = '0.0.3'


class Qss(FramelessWindow):
    def __init__(self, custom_widget=None):
        super(Qss, self).__init__()
        self.custom_widget = custom_widget
        self.setWindowTitle('QSS编辑器')
        self.resize(800, 600)

        self.qss_file = ''
        self.title = 'QSS编辑器'
        self.setup_ui()

        # 加载样式
        with open(os.path.join(os.path.dirname(__file__), 'qss/default.qss'), 'r') as f:
            self.setStyleSheet(f.read())

    def setup_ui(self):
        widget = QWidget(self)
        widget.setObjectName('BackWidget')
        widget.setMouseTracking(True)
        hl = QHBoxLayout(self)
        hl.addWidget(widget)
        hl.setContentsMargins(self.margin, self.margin, self.margin, self.margin)
        vl = QVBoxLayout(widget)
        vl.setSpacing(0)
        vl.setContentsMargins(0, 0, 0, 0)
        # 标题组件
        title_widget = QWidget(widget)
        title_widget.setMouseTracking(True)

        thl = QHBoxLayout(title_widget)
        thl.setContentsMargins(0, 0, 0, 0)
        thl.setSpacing(0)
        label_icon = QLabel('Q', title_widget)
        label_icon.setMouseTracking(True)
        label_icon.setObjectName('LabelIcon')
        label_icon.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        thl.addWidget(label_icon)
        pushButton_open = QPushButton('打开', title_widget)
        pushButton_open.setMouseTracking(True)
        pushButton_open.setObjectName('btn_open')
        thl.addWidget(pushButton_open)
        pushButton_save = QPushButton('保存', title_widget)
        pushButton_save.setMouseTracking(True)
        pushButton_save.setObjectName('btn_save')
        thl.addWidget(pushButton_save)
        s_item = QSpacerItem(214, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        thl.addItem(s_item)
        self.label_title = QLabel(self.title, title_widget)
        self.label_title.setMouseTracking(True)
        self.label_title.setObjectName('Title')
        thl.addWidget(self.label_title)
        s_item = QSpacerItem(214, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        thl.addItem(s_item)
        pushButton_min = QPushButton('0', title_widget)
        pushButton_min.setMouseTracking(True)
        pushButton_min.setObjectName('btn_min')
        pushButton_min.clicked.connect(self.showMinimized)
        thl.addWidget(pushButton_min)
        pushButton_close = QPushButton('r', title_widget)
        pushButton_close.setMouseTracking(True)
        pushButton_close.setObjectName('btn_close')
        pushButton_close.clicked.connect(self.close)
        thl.addWidget(pushButton_close)
        vl.addWidget(title_widget)
        # QScintilla
        self.text_edit = TextEdit()
        self.text_edit.setMouseTracking(True)
        self.text_edit.installEventFilter(self)
        self.text_edit.setObjectName('TextEdit')
        self.text_edit.lexer.add_object_names(self.custom_widget)  # 将ObjectName添加API中
        self.text_edit.textChanged.connect(self.text_edit_textChanged)
        vl.addWidget(self.text_edit)
        # 槽函数
        pushButton_open.clicked.connect(self.pushButton_open_clicked)
        pushButton_save.clicked.connect(self.pushButton_save_clicked)
        # 快捷键
        self.shortcut_save = QShortcut(QKeySequence.Save, self)
        self.shortcut_save.activated.connect(self.shortcut_save_activated)

    def text_edit_textChanged(self):
        _str = self.text_edit.text()
        # self.setStyleSheet(_str)
        self.label_title.setText(self.label_title.text().strip('*') + '*')
        if not hasattr(self.custom_widget, 'setStyleSheet'):
            return
        self.custom_widget.setStyleSheet(_str)

    def pushButton_open_clicked(self):
        qss, ext = QFileDialog.getOpenFileName(self, '打开qss', '', '*.qss')
        if qss:
            with open(qss, 'r') as f:
                self.text_edit.clear()
                self.text_edit.append(f.read())
            self.qss_file = qss
            self.label_title.setText(self.title + '-' + str(os.path.basename(qss).split('.')[0]))

    def pushButton_save_clicked(self):
        if self.qss_file:
            self.shortcut_save_activated()
            return
        qss, ext = QFileDialog.getSaveFileName(self, '保存qss', '', '*.qss')
        if qss:
            with open(qss, 'w') as f:
                f.write(self.text_edit.text())
            self.qss_file = qss
            self.label_title.setText(self.title + '-' + str(os.path.basename(qss).split('.')[0]))
            return True
        return False

    def shortcut_save_activated(self):
        if not self.qss_file:
            if self.pushButton_save_clicked():
                self.label_title.setText(self.label_title.text().strip('*'))
        else:
            with open(self.qss_file, 'w') as f:
                f.write(self.text_edit.text())
            self.label_title.setText(self.label_title.text().strip('*'))


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    from pyqss import Qss

    app = QApplication(sys.argv)
    qss = Qss()
    qss.show()
    app.exec_()
