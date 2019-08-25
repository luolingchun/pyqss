# -*- coding: utf-8 -*-
# @Time    : 2019/3/22 9:53
# @Author  : llc
# @File    : __init__.py
import os
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QKeySequence, QIcon
from PyQt5.QtWidgets import QGridLayout, QWidget, QHBoxLayout, QPushButton, QSpacerItem, QSizePolicy, QFileDialog, \
    QShortcut, QLabel
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
        self.setup_ui()

        # 加载样式
        qss = open(os.path.join(os.path.dirname(__file__), 'qss/default.qss'), 'r').read()
        self.setStyleSheet(qss)

    def setup_ui(self):
        self.setObjectName('QSSDialog')
        self.grid_layout = QGridLayout(self)
        self.grid_layout.setSpacing(0)
        self.grid_layout.setContentsMargins(self.margin, self.margin, self.margin, self.margin)
        # 标题组件
        self.title_widget = QWidget(self)
        self.title_widget.setMouseTracking(True)
        self.title_widget.setObjectName('BackWidget')

        self.hl = QHBoxLayout(self.title_widget)
        self.hl.setContentsMargins(0, 0, 0, 0)
        self.hl.setSpacing(0)
        self.label_icon = QLabel('Q', self.title_widget)
        self.label_icon.setMouseTracking(True)
        self.label_icon.setParent(self)
        self.label_icon.setObjectName('LabelIcon')
        self.label_icon.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.hl.addWidget(self.label_icon)
        self.pushButton_open = QPushButton('打开', self.title_widget)
        self.pushButton_open.setMouseTracking(True)
        self.pushButton_open.setObjectName('open')
        self.hl.addWidget(self.pushButton_open)
        self.pushButton_save = QPushButton('保存', self.title_widget)
        self.pushButton_save.setMouseTracking(True)
        self.pushButton_save.setObjectName('save')
        self.hl.addWidget(self.pushButton_save)
        s_item = QSpacerItem(214, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.hl.addItem(s_item)
        self.label_title = QLabel(self.title_widget)
        self.label_title.setMouseTracking(True)
        self.label_title.setObjectName('Title')
        self.title = 'QSS编辑器'
        self.label_title.setText(self.title)
        self.hl.addWidget(self.label_title)
        s_item = QSpacerItem(214, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.hl.addItem(s_item)
        font = QFont('Webdings')
        self.pushButton_min = QPushButton('0', self.title_widget)
        self.pushButton_min.setMouseTracking(True)
        self.pushButton_min.setObjectName('min')
        self.pushButton_min.clicked.connect(self.showMinimized)
        self.pushButton_min.setFont(font)
        self.hl.addWidget(self.pushButton_min)
        self.pushButton_close = QPushButton('r', self.title_widget)
        self.pushButton_close.setMouseTracking(True)
        self.pushButton_close.setObjectName('close')
        self.pushButton_close.clicked.connect(self.close)
        self.pushButton_close.setFont(font)
        self.hl.addWidget(self.pushButton_close)
        self.grid_layout.addWidget(self.title_widget, 0, 0, 1, 1)
        # QScintilla
        self.text_edit = TextEdit(self, self.custom_widget)
        self.text_edit.setMouseTracking(True)
        self.text_edit.installEventFilter(self)
        self.text_edit.setObjectName('TextEdit')
        self.text_edit.lexer.add_object_names()  # 将ObjectName添加API中
        self.text_edit.textChanged.connect(self.text_edit_textChanged)
        self.grid_layout.addWidget(self.text_edit, 1, 0, 1, 1)
        # 槽函数
        self.pushButton_open.clicked.connect(self.pushButton_open_clicked)
        self.pushButton_save.clicked.connect(self.pushButton_save_clicked)

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
