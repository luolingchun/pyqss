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

__version__ = '1.0'


class Qss(FramelessWindow):
    def __init__(self, custom_widget=None, language='zh'):
        super(Qss, self).__init__()
        self.custom_widget = custom_widget
        # 初始化语言
        self.tr = init_language(language)

        self.resize(600, 400)
        self.text_to_find = ''
        self.state_ = tuple()

        self.qss_file = None
        self.qss_name = 'unknown'
        self.title = self.tr("QSS Editor")
        self.setWindowTitle(self.title)
        self.setup_ui()
        self.set_icon()

        self.editor = self.findChild(QssEditor, "QssEditor")
        self.label_title = self.findChild(QLabel, "Title")
        self.fr_widget = self.findChild(QWidget, "FRWidget")
        self.lineEdit_find = self.fr_widget.findChild(QLineEdit, "LineEditFind")
        self.lineEdit_replace = self.fr_widget.findChild(QLineEdit, "LineEditReplace")
        self.btn_pre = self.fr_widget.findChild(QPushButton, "btn_pre")
        self.btn_next = self.fr_widget.findChild(QPushButton, "btn_next")
        self.btn_replace = self.fr_widget.findChild(QPushButton, "btn_replace")
        self.btn_replace_all = self.fr_widget.findChild(QPushButton, "btn_replace_all")

        self.editor.add_apis(self.custom_widget)

        # 加载样式
        with open(os.path.join(os.path.dirname(__file__), 'qss/default.qss'), 'r') as f:
            self.setStyleSheet(f.read())

        # 获取焦点
        self.editor.setFocus()

        # 查找替换
        QShortcut(QKeySequence("Ctrl+F"), self, self.find_replace)

        # 信号和槽
        self.lineEdit_find.textChanged.connect(self.lineEdit_find_textChanged)
        self.btn_pre.clicked.connect(lambda: self.findText(forward=False))
        self.btn_next.clicked.connect(lambda: self.findText(forward=True))
        self.btn_replace.clicked.connect(self.btn_replace_clicked)
        self.btn_replace_all.clicked.connect(self.btn_replace_all_clicked)

    def setup_ui(self):
        widget = QWidget(self)
        widget.setObjectName('TopWidget')
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

        # find and replace
        self.setup_fr_ui()

    def setup_fr_ui(self):
        """查找替换"""

        def rf_resize():
            widget.resize(self.width() - 32 * self.margin, 40)

        widget = QWidget(self)
        widget.installEventFilter(self)
        widget.setObjectName('FRWidget')
        widget.setGeometry(self.x() + 16 * self.margin, self.y() + 60,
                           self.width() - 32 * self.margin, 40)
        self.resized.connect(rf_resize)
        gridLayout = QGridLayout(widget)
        gridLayout.setContentsMargins(0, 0, 0, 0)
        lineEdit_find = QLineEdit(widget)
        lineEdit_find.setPlaceholderText(self.tr("find"))
        lineEdit_find.setObjectName("LineEditFind")
        gridLayout.addWidget(lineEdit_find, 0, 0, 1, 1)
        btn_pre = QPushButton('h', widget)
        btn_pre.setToolTip(self.tr("pre"))
        btn_pre.setObjectName("btn_pre")
        gridLayout.addWidget(btn_pre, 0, 1, 1, 1)
        btn_next = QPushButton('i', widget)
        btn_next.setToolTip(self.tr("next"))
        btn_next.setObjectName("btn_next")
        gridLayout.addWidget(btn_next, 0, 2, 1, 1)
        lineEdit_replace = QLineEdit(widget)
        lineEdit_replace.setPlaceholderText(self.tr("replace") + '...')
        lineEdit_replace.setObjectName("LineEditReplace")
        gridLayout.addWidget(lineEdit_replace, 1, 0, 1, 1)
        btn_replace = QPushButton("P", widget)
        btn_replace.setToolTip(self.tr("replace"))
        btn_replace.setObjectName("btn_replace")
        gridLayout.addWidget(btn_replace, 1, 1, 1, 1)
        btn_replace_all = QPushButton("R", widget)
        btn_replace_all.setToolTip(self.tr("replace all"))
        btn_replace_all.setObjectName("btn_replace_all")
        gridLayout.addWidget(btn_replace_all, 1, 2, 1, 1)

        widget.hide()

    def find_replace(self):
        if self.fr_widget.isHidden():
            self.fr_widget.show()
            self.fr_widget.findChild(QWidget, "LineEditFind").setFocus()
            self.lineEdit_find_textChanged(self.lineEdit_find.text())
        else:
            self.fr_widget.hide()
            self.editor.cancelFind()

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

    def lineEdit_find_textChanged(self, text):
        self.editor.findFirst(text, True, False, True, True)

    def findText(self, forward):
        text_to_find = self.lineEdit_find.text()

        if forward:
            line, index = self.editor.getSelection()[2:]
        else:
            line, index = self.editor.getSelection()[:2]

        state_ = (
            True, False,
            False, False,
            forward, line, index,
            False, False,
        )

        self.text_to_find = text_to_find
        self.state_ = state_
        self.editor.findFirst(text_to_find, *state_)

    def btn_replace_clicked(self):
        self.editor.beginUndoAction()
        selected_text = self.editor.selectedText()
        if selected_text == self.lineEdit_find.text():
            self.editor.replaceSelectedText(self.lineEdit_replace.text())
        self.editor.endUndoAction()

    def btn_replace_all_clicked(self):
        # TODO:不能撤销
        self.editor.beginUndoAction()
        text = self.editor.text()
        new_text = text.replace(self.lineEdit_find.text(), self.lineEdit_replace.text())
        self.editor.setText(new_text)
        self.editor.endUndoAction()

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
