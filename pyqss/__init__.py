# -*- coding: utf-8 -*-
# @Time    : 2019/3/22 9:53
# @Author  : llc
# @File    : __init__.py
import os

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence, QEnterEvent
from PyQt5.QtWidgets import QFileDialog, QShortcut, QMainWindow

from pyqss.i18n import init_tr
from pyqss.widgets.find_replace import FRWidget
from pyqss.widgets.main import QssWindow


def read_qss(qss_file):
    with open(qss_file, 'r', encoding='utf8') as f:
        content = f.read()
    return content


def write_qss(qss_file, content):
    with open(qss_file, 'w', encoding='utf8') as f:
        f.write(content)


class Qss(QssWindow):
    def __init__(self, custom_widget=None, language='zh', theme='default'):
        # 初始化语言
        self.tr = init_tr(language)
        super(Qss, self).__init__()
        self.custom_widget = custom_widget
        # 设置窗口大小
        self.resize(600, 400)

        self.qss_file = None
        self.qss_name = 'unknown'
        self.title = self.tr("QSS Editor")
        self.setWindowTitle(self.title)
        self.labelTitle.setText(self.title)

        # 添加api
        self.editor.add_apis(self.custom_widget)

        # 获取焦点
        self.editor.setFocus()
        self.editor.installEventFilter(self)

        # 快捷键
        shortcut_save = QShortcut(QKeySequence.Save, self)
        shortcut_save.activated.connect(self.shortcut_save_activated)
        QShortcut(QKeySequence("Ctrl+F"), self, self.find_replace)

        # 信号和槽
        self.btnOpen.clicked.connect(self.btnOpen_clicked)
        self.btnSave.clicked.connect(self.btnSave_clicked)
        self.btnAttach.clicked.connect(self.btnAttach_clicked)
        self.btnMin.clicked.connect(self.showMinimized)
        self.btnClose.clicked.connect(self.close)

        self.editor.textChanged.connect(self.editor_text_changed)
        self.editor.opened.connect(self.open_qss)

        # 加载样式
        content = read_qss(os.path.join(os.path.dirname(__file__), f'theme/{theme}.qss'))
        self.setStyleSheet(content)

        # 初始化查找替换
        self.fr_widget = None
        self.init_fr_widget()

    def init_fr_widget(self):
        """查找替换控件"""
        self.fr_widget = FRWidget(self.tr, parent=self)
        self.fr_widget.hide()
        self.fr_widget.setGeometry(50, 50, self.width() - 100, 40)
        self.fr_widget.leFind.textChanged.connect(self.leFind_text_changed)
        self.fr_widget.btnPre.clicked.connect(lambda: self.find_text(forward=False))
        self.fr_widget.btnNext.clicked.connect(lambda: self.find_text(forward=True))
        self.fr_widget.btnReplace.clicked.connect(self.btnReplace_clicked)
        self.fr_widget.btnReplaceAll.clicked.connect(self.btnReplaceAll_clicked)

        self.resized.connect(self.resize_fr)

    def resize_fr(self):
        self.fr_widget.setGeometry(50, 50, self.width() - 100, 40)

    def find_replace(self):
        if self.fr_widget.isHidden():
            self.fr_widget.show()
            self.fr_widget.leFind.setFocus()
            self.leFind_text_changed(self.fr_widget.leFind.text())
        else:
            self.fr_widget.hide()
            self.editor.cancelFind()

    def editor_text_changed(self):
        text = self.editor.text()
        # self.setStyleSheet(text)
        self.labelTitle.setText(self.title + "-" + self.qss_name + '*')
        if hasattr(self.custom_widget, 'setStyleSheet'):
            self.custom_widget.setStyleSheet(text)

    def btnOpen_clicked(self):
        qss_file, ext = QFileDialog.getOpenFileName(self, '打开qss', '', '*.qss')
        if qss_file:
            self.open_qss(qss_file)

    def open_qss(self, qss_file):
        content = read_qss(qss_file)
        self.editor.clear()
        self.editor.append(content)
        self.qss_file = qss_file
        self.qss_name = str(os.path.basename(qss_file).split('.')[0])
        self.labelTitle.setText(self.title + '-' + self.qss_name)

    def btnSave_clicked(self):
        if self.qss_file:
            self.shortcut_save_activated()
            return
        qss_file, ext = QFileDialog.getSaveFileName(self, '保存qss', self.qss_name, '*.qss')
        if qss_file:
            write_qss(qss_file, self.editor.text())
            self.qss_file = qss_file
            self.qss_name = str(os.path.basename(qss_file).split('.')[0])
            self.labelTitle.setText(self.title + '-' + str(os.path.basename(qss_file).split('.')[0]))
            return True
        return False

    def shortcut_save_activated(self):
        if not self.qss_file:
            if self.btnSave_clicked():
                self.labelTitle.setText(self.labelTitle.text().strip('*'))
        else:
            write_qss(self.qss_file, self.editor.text())
            self.labelTitle.setText(self.labelTitle.text().strip('*'))

    def leFind_text_changed(self, text):
        self.editor.findFirst(text, True, False, True, True)

    def find_text(self, forward):
        text_to_find = self.fr_widget.leFind.text()

        c_line, c_index = self.editor.getCursorPosition()
        line_from, index_from, line_to, index_to = self.editor.getSelection()

        if forward:
            line = line_to
            index = index_to
        else:
            if (line_from, index_from) == (-1, -1):
                line = c_line
                index = c_index
            else:
                line = line_from
                index = index_from

        return self.editor.findFirst(text_to_find, False, False, False, True, forward, line, index)

    def btnReplace_clicked(self):
        if self.editor.hasSelectedText():
            row1, line1, row2, line2 = self.editor.getSelection()
            self.editor.setCursorPosition(row1, line1)
        self.find_text(True)
        self.editor.replace(self.fr_widget.leReplace.text())
        return True

    def btnReplaceAll_clicked(self):
        self.editor.beginUndoAction()
        text = self.editor.text()
        n = text.count(self.fr_widget.leFind.text(), False)
        for i in range(n):
            self.find_text(True)
            self.editor.replace(self.fr_widget.leReplace.text())
        self.editor.endUndoAction()

    def btnAttach_clicked(self, is_checked):
        if is_checked:
            self.move_custom_widget()

    def moveEvent(self, event):
        super(Qss, self).moveEvent(event)
        if self.btnAttach.isChecked():
            self.move_custom_widget()

    def move_custom_widget(self):
        if hasattr(self.custom_widget, "setGeometry"):
            if self.custom_widget.isMaximized() or self.custom_widget.isFullScreen():
                return
            self.custom_widget.setGeometry(self.x() - self.custom_widget.width() - 3,
                                           self.y(),
                                           self.custom_widget.width(),
                                           self.custom_widget.height())

    def eventFilter(self, obj, event):
        if obj.objectName() == 'editor' and isinstance(event, QEnterEvent):
            self.setCursor(Qt.ArrowCursor)

        return QMainWindow.eventFilter(self, obj, event)

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Escape:
            # 隐藏查找替换
            self.fr_widget.hide()
        super(Qss, self).keyPressEvent(event)

    def closeEvent(self, event):
        if self.qss_file:
            self.shortcut_save_activated()
        super(Qss, self).closeEvent(event)


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    from pyqss import Qss

    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    qss = Qss()
    qss.editor.add_apis(qss)
    qss.show()
    app.exec_()
