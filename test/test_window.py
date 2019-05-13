# -*- coding: utf-8 -*-
# @Time    : 2019/3/22 9:53
# @Author  : llc
# @File    : test_window.py
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from PyQt5.QtWidgets import QGridLayout, QWidget, QHBoxLayout, QPushButton, QSpacerItem, QSizePolicy, \
    QTextEdit, QLabel, QDialog


class TestWindow(QDialog):
    def __init__(self, custom_widget=None):
        super(TestWindow, self).__init__()
        self.custom_widget = custom_widget
        self.setWindowTitle('QSS编辑器')
        self.resize(800, 600)

        self.setWindowFlags(Qt.Window |
                            Qt.FramelessWindowHint |
                            Qt.WindowSystemMenuHint |
                            Qt.WindowMinMaxButtonsHint |
                            Qt.WindowCloseButtonHint)
        self._margin = 0

        self._setup_ui()

    def _setup_ui(self):
        self.setObjectName('QSSDialog')
        grid_layout = QGridLayout(self)
        grid_layout.setSpacing(0)
        grid_layout.setContentsMargins(self._margin, self._margin, self._margin, self._margin)
        # 标题组件
        title_widget = QWidget()
        title_widget.setMouseTracking(True)
        title_widget.setObjectName('BackWidget')
        hl = QHBoxLayout(title_widget)
        hl.setContentsMargins(0, 0, 0, 0)
        hl.setSpacing(0)
        label_icon = QLabel('Q')
        label_icon.setObjectName('LabelIcon')
        label_icon.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        hl.addWidget(label_icon)
        pushButton_open = QPushButton('打开', title_widget)
        pushButton_open.setMouseTracking(True)
        pushButton_open.setObjectName('open')
        hl.addWidget(pushButton_open)
        pushButton_save = QPushButton('保存', title_widget)
        pushButton_save.setMouseTracking(True)
        pushButton_save.setObjectName('save')
        hl.addWidget(pushButton_save)
        s_item = QSpacerItem(214, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        hl.addItem(s_item)
        self.label_title = QLabel(self)
        self.label_title.setMouseTracking(True)
        self.label_title.setObjectName('Title')
        self.title = 'QSS编辑器'
        self.label_title.setText(self.title)
        hl.addWidget(self.label_title)
        s_item = QSpacerItem(214, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        hl.addItem(s_item)
        font = QFont('Webdings')
        pushButton_min = QPushButton('0', title_widget)
        pushButton_min.setMouseTracking(True)
        pushButton_min.setObjectName('min')
        pushButton_min.clicked.connect(self.showMinimized)
        pushButton_min.setFont(font)
        hl.addWidget(pushButton_min)
        pushButton_close = QPushButton('r', title_widget)
        pushButton_close.setMouseTracking(True)
        pushButton_close.setObjectName('close')
        pushButton_close.clicked.connect(self.close)
        pushButton_close.setFont(font)
        hl.addWidget(pushButton_close)
        grid_layout.addWidget(title_widget, 0, 0, 1, 1)
        # 多行文本组件
        self.text_edit = QTextEdit(self)
        self.text_edit.setMouseTracking(True)
        self.text_edit.installEventFilter(self)
        self.text_edit.setObjectName('TextEdit')
        grid_layout.addWidget(self.text_edit, 1, 0, 1, 1)


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    from pyqss import Qss

    app = QApplication(sys.argv)
    test_window = TestWindow()
    test_window.show()
    # 将主窗口注册到Qss中
    qss = Qss(test_window)
    qss.show()

    app.exec_()
