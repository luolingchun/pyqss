# -*- coding: utf-8 -*-
# @Time    : 2019/3/22 9:53
# @Author  : llc
# @File    : __init__.py
import os

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QKeySequence, QIcon, QPixmap, QImage, QPainter, QFont, QColor
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QSpacerItem, QSizePolicy, QFileDialog, \
    QShortcut, QLabel, QVBoxLayout, QGridLayout, QLineEdit

from pyqss.tr import init_language
from pyqss.widgets.frameless_window import FramelessWindow
from pyqss.sci.editor import QssEditor

__version__ = '0.9.1'


class Qss(FramelessWindow):
    def __init__(self, custom_widget=None, language='zh'):
        super(Qss, self).__init__()
        self.custom_widget = custom_widget
        # 初始化语言
        self.tr = init_language(language)

        self.resize(600, 400)

        self.qss_file = None
        self.qss_name = 'unknown'
        self.title = self.tr("QSS Editor")
        self.setWindowTitle(self.title)
        self.setup_ui()
        self.set_icon()

        self.label_title = self.findChild(QLabel, "Title")
        self.editor = self.findChild(QssEditor, "QssEditor")

        self.editor.add_apis(self.custom_widget)

        # 加载样式
        with open(os.path.join(os.path.dirname(__file__), 'qss/default.qss'), 'r') as f:
            self.setStyleSheet(f.read())

        # 获取焦点
        self.editor.setFocus()

        # 查找替换
        QShortcut(QKeySequence("Ctrl+F"), self, self.find_replace)

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
        pushButton_open = QPushButton(self.tr('open'), title_widget)
        pushButton_open.setMouseTracking(True)
        pushButton_open.setObjectName('btn_open')
        thl.addWidget(pushButton_open)
        pushButton_save = QPushButton(self.tr('save'), title_widget)
        pushButton_save.setMouseTracking(True)
        pushButton_save.setObjectName('btn_save')
        thl.addWidget(pushButton_save)
        s_item = QSpacerItem(214, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        thl.addItem(s_item)
        label_title = QLabel(self.title, title_widget)
        label_title.setMouseTracking(True)
        label_title.setObjectName('Title')
        thl.addWidget(label_title)
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
        editor = QssEditor(self)
        editor.setMouseTracking(True)
        editor.installEventFilter(self)
        editor.setObjectName('QssEditor')
        editor.textChanged.connect(self.text_edit_textChanged)
        vl.addWidget(editor)
        # 槽函数
        pushButton_open.clicked.connect(self.pushButton_open_clicked)
        pushButton_save.clicked.connect(self.pushButton_save_clicked)
        # 快捷键
        shortcut_save = QShortcut(QKeySequence.Save, self)
        shortcut_save.activated.connect(self.shortcut_save_activated)

    def find_replace(self):
        print('find')
        widget = QWidget(self)
        widget.setGeometry(self.width(), 40)
        widget.setObjectName("FindReplace")
        gridLayout = QGridLayout(widget)
        gridLayout.setContentsMargins(0, 0, 0, 0)
        lineEdit_find = QLineEdit(widget)
        lineEdit_find.setObjectName("lineEdit_find")
        gridLayout.addWidget(lineEdit_find, 0, 0, 1, 1)
        label_pre = QLabel('f', widget)
        label_pre.setObjectName("label_pre")
        gridLayout.addWidget(label_pre, 0, 1, 1, 1)
        label_next = QLabel('g', widget)
        label_next.setObjectName("label_2")
        gridLayout.addWidget(label_next, 0, 2, 1, 1)
        find_close = QPushButton(widget)
        find_close.setObjectName("find_close")
        gridLayout.addWidget(find_close, 0, 3, 1, 1)
        lineEdit_replace = QLineEdit(widget)
        lineEdit_replace.setObjectName("lineEdit_replace")
        gridLayout.addWidget(lineEdit_replace, 1, 0, 1, 1)
        label_find = QLabel(widget)
        label_find.setObjectName("label_find")
        gridLayout.addWidget(label_find, 1, 1, 1, 1)
        label_replace = QLabel(widget)
        label_replace.setObjectName("label_4")
        gridLayout.addWidget(label_replace, 1, 2, 1, 1)

    def text_edit_textChanged(self):
        text = self.editor.text()
        # self.setStyleSheet(text)
        self.label_title.setText(self.title + "-" + self.qss_name + '*')
        if hasattr(self.custom_widget, 'setStyleSheet'):
            self.custom_widget.setStyleSheet(text)

    def pushButton_open_clicked(self):
        qss_file, ext = QFileDialog.getOpenFileName(self, '打开qss', '', '*.qss')
        if qss_file:
            with open(qss_file, 'r') as f:
                self.editor.clear()
                self.editor.append(f.read())
            self.qss_file = qss_file
            self.qss_name = str(os.path.basename(qss_file).split('.')[0])
            self.label_title.setText(self.title + '-' + self.qss_name)

    def pushButton_save_clicked(self):
        if self.qss_file:
            self.shortcut_save_activated()
            return
        qss_file, ext = QFileDialog.getSaveFileName(self, '保存qss', self.qss_name, '*.qss')
        if qss_file:
            with open(qss_file, 'w') as f:
                f.write(self.editor.text())
            self.qss_file = qss_file
            self.qss_name = str(os.path.basename(qss_file).split('.')[0])
            self.label_title.setText(self.title + '-' + str(os.path.basename(qss_file).split('.')[0]))
            return True
        return False

    def shortcut_save_activated(self):
        if not self.qss_file:
            if self.pushButton_save_clicked():
                self.label_title.setText(self.label_title.text().strip('*'))
        else:
            with open(self.qss_file, 'w') as f:
                f.write(self.editor.text())
            self.label_title.setText(self.label_title.text().strip('*'))

    def set_icon(self):
        image = QImage(QSize(128, 128), QImage.Format_ARGB32)
        text_painter = QPainter()
        text_painter.begin(image)
        text_painter.setRenderHint(QPainter.Antialiasing, True)
        text_painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
        font = QFont()
        font.setFamily('Microsoft Yahei')
        font.setPointSize(100)
        text_painter.setFont(font)
        text_painter.setPen(QColor(0, 128, 0))
        text_painter.drawText(10, 106, 'Q')
        text_painter.end()
        p = QPixmap.fromImage(image)
        self.setWindowIcon(QIcon(p))

    def closeEvent(self, event):
        if self.qss_file:
            self.shortcut_save_activated()
        event.accept()


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    from pyqss import Qss

    app = QApplication(sys.argv)
    qss = Qss()
    qss.show()
    app.exec_()
