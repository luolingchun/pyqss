# -*- coding: utf-8 -*-
# @Time    : 2019/3/22 9:53
# @Author  : llc
# @File    : __init__.py
import os
from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QFont, QFontMetrics, QKeySequence, QPainter, QIcon, QEnterEvent
from PyQt5.QtWidgets import QGridLayout, QWidget, QHBoxLayout, QPushButton, QSpacerItem, QSizePolicy, QTextEdit, \
    QFileDialog, QShortcut, QLabel, QDialog, QStyle, QStyleOption
from pyqss import resource_rc

__version__ = '1.0.0'
_PATH = os.path.dirname(__file__)


class Qss(QDialog):
    def __init__(self, custom_widget=None):
        super(Qss, self).__init__()
        self.custom_widget = custom_widget
        self.setWindowTitle('QSS编辑器')
        self.resize(800, 600)

        self._top_drag = False
        self._bottom_drag = False
        self._left_drag = False
        self._right_drag = False
        self._bottom_left_drag = False
        self._bottom_right_drag = False
        self._top_left_drag = False
        self._top_right_drag = False
        self._start_point = None
        self.setMouseTracking(True)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.Dialog |
                            Qt.FramelessWindowHint |
                            Qt.WindowSystemMenuHint |
                            Qt.WindowMinMaxButtonsHint)
        self.qss_file = ''
        self._margin = 3
        self._setup_ui()

        # 设置图标
        self.setWindowIcon(QIcon(':/icon/1.png'))
        # 加载样式
        self.setStyleSheet(open(os.path.join(_PATH, 'default.qss'), 'r').read())

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
        metrics = QFontMetrics(self.text_edit.font())
        # 设置tab键为4个空格
        self.text_edit.setTabStopDistance(4 * metrics.width(' '))
        self.text_edit.textChanged.connect(self.text_edit_textChanged)
        grid_layout.addWidget(self.text_edit, 1, 0, 1, 1)
        # 槽函数
        pushButton_open.clicked.connect(self.pushButton_open_clicked)
        pushButton_save.clicked.connect(self.pushButton_save_clicked)

        self.shortcut_save = QShortcut(QKeySequence.Save, self)
        self.shortcut_save.activated.connect(self.shortcut_save_activated)

    def text_edit_textChanged(self):
        _str = self.text_edit.toPlainText()
        self.label_title.setText(self.label_title.text().strip('*') + '*')
        if not hasattr(self.custom_widget, 'setStyleSheet'):
            return
        self.custom_widget.setStyleSheet(_str)

    def pushButton_open_clicked(self):
        qss, ext = QFileDialog.getOpenFileName(self, '打开qss', '', '*.qss')
        if qss:
            with open(qss, 'r') as f:
                self.text_edit.setPlainText(f.read())
            self.qss_file = qss
            self.label_title.setText(self.title + '-' + os.path.basename(qss).split('.')[0])

    def pushButton_save_clicked(self):
        if self.qss_file:
            self.shortcut_save_activated()
            return
        qss, ext = QFileDialog.getSaveFileName(self, '保存qss', '', '*.qss')
        if qss:
            with open(qss, 'w') as f:
                f.write(self.text_edit.toPlainText())
            self.qss_file = qss
            self.label_title.setText(self.title + '-' + os.path.basename(qss).split('.')[0])

    def shortcut_save_activated(self):
        if not self.qss_file:
            self.pushButton_save_clicked()
            self.label_title.setText(self.label_title.text().strip('*'))
        else:
            with open(self.qss_file, 'w') as f:
                f.write(self.text_edit.toPlainText())
            self.label_title.setText(self.label_title.text().strip('*'))

    def mousePressEvent(self, event):
        self._start_point = event.globalPos()
        self._pos = self.pos()
        self._width = self.width()
        self._height = self.height()
        if (event.button() == Qt.LeftButton) and (event.pos() in self._t_rect):
            # 上
            self._top_drag = True
        elif (event.button() == Qt.LeftButton) and (event.pos() in self._b_rect):
            # 下
            self._bottom_drag = True
        elif (event.button() == Qt.LeftButton) and (event.pos() in self._l_rect):
            # 左
            self._left_drag = True
            event.accept()
        elif (event.button() == Qt.LeftButton) and (event.pos() in self._r_rect):
            # 右
            self._right_drag = True
            event.accept()
        elif (event.button() == Qt.LeftButton) and (event.pos() in self._bl_rect):
            # 左下
            self._bottom_left_drag = True
            event.accept()
        elif (event.button() == Qt.LeftButton) and (event.pos() in self._br_rect):
            # 右下
            self._bottom_right_drag = True
            event.accept()
        elif (event.button() == Qt.LeftButton) and (event.pos() in self._tl_rect):
            # 左上
            self._top_left_drag = True
            event.accept()
        elif (event.button() == Qt.LeftButton) and (event.pos() in self._tr_rect):
            # 右上
            self._top_right_drag = True
            event.accept()
        elif event.button() == Qt.LeftButton:
            # 移动
            event.accept()

    def mouseMoveEvent(self, event):
        if event.pos() in self._t_rect:
            # 上
            self.setCursor(Qt.SizeVerCursor)
        elif event.pos() in self._b_rect:
            # 下
            self.setCursor(Qt.SizeVerCursor)
        elif event.pos() in self._l_rect:
            # 左
            self.setCursor(Qt.SizeHorCursor)
        elif event.pos() in self._r_rect:
            # 右
            self.setCursor(Qt.SizeHorCursor)
        elif event.pos() in self._bl_rect:
            # 左下
            self.setCursor(Qt.SizeBDiagCursor)
        elif event.pos() in self._br_rect:
            # 右下
            self.setCursor(Qt.SizeFDiagCursor)
        elif event.pos() in self._tl_rect:
            # 左上
            self.setCursor(Qt.SizeFDiagCursor)
        elif event.pos() in self._tr_rect:
            # 右上
            self.setCursor(Qt.SizeBDiagCursor)
        else:
            self.setCursor(Qt.ArrowCursor)

        if not self._start_point:
            return
        elif Qt.LeftButton and self._top_drag:
            # 上
            diff_y = event.globalPos().y() - self._start_point.y()
            if diff_y > 0 and self.height() == self.minimumHeight():
                return
            self.setGeometry(self.pos().x(), self._pos.y() + diff_y, self.width(), self._height - diff_y)
            event.accept()
        elif Qt.LeftButton and self._bottom_drag:
            # 下
            self.resize(self.width(), event.pos().y())
            event.accept()
        elif Qt.LeftButton and self._left_drag:
            # 左
            diff_x = event.globalPos().x() - self._start_point.x()
            if diff_x > 0 and self.width() == self.minimumWidth():
                return
            self.setGeometry(self._pos.x() + diff_x, self.pos().y(), self._width - diff_x, self.height())
            event.accept()
        elif Qt.LeftButton and self._right_drag:
            # 右
            self.resize(event.pos().x(), self.height())
            event.accept()
        elif Qt.LeftButton and self._bottom_left_drag:
            # 左下
            diff_x = event.globalPos().x() - self._start_point.x()
            diff_y = event.globalPos().y() - self._start_point.y()
            if diff_x > 0 and self.width() == self.minimumWidth():
                return
            if diff_y < 0 and self.height() == self.minimumHeight():
                return
            self.setGeometry(self._pos.x() + diff_x, self.pos().y(), self._width - diff_x, self._height + diff_y)
            event.accept()
        elif Qt.LeftButton and self._bottom_right_drag:
            # 右下
            self.resize(event.pos().x(), event.pos().y())
            event.accept()
        elif Qt.LeftButton and self._top_left_drag:
            # 左上
            diff_x = event.globalPos().x() - self._start_point.x()
            diff_y = event.globalPos().y() - self._start_point.y()
            if diff_x > 0 and self.width() == self.minimumWidth():
                return
            if diff_y < 0 and self.height() == self.minimumHeight():
                return
            self.setGeometry(self._pos.x() + diff_x, self._pos.y() + diff_y, self._width - diff_x,
                             self._height - diff_y)
            event.accept()
        elif Qt.LeftButton and self._top_right_drag:
            # 右上
            diff_x = event.globalPos().x() - self._start_point.x()
            diff_y = event.globalPos().y() - self._start_point.y()
            if diff_x > 0 and self.width() == self.minimumWidth():
                return
            if diff_y < 0 and self.height() == self.minimumHeight():
                return
            self.setGeometry(self.pos().x(), self._pos.y() + diff_y, self._width + diff_x,
                             self._height - diff_y)
            event.accept()
        elif event.buttons() == Qt.LeftButton and self._start_point:
            # 移动
            diff_x = event.globalPos() - self._start_point
            self.move(self._pos + diff_x)
            self._get_rect()
            event.accept()

    def mouseReleaseEvent(self, event):
        self._top_drag = False
        self._bottom_drag = False
        self._left_drag = False
        self._right_drag = False
        self._bottom_left_drag = False
        self._bottom_right_drag = False
        self._top_left_drag = False
        self._top_right_drag = False
        self._start_point = None
        event.accept()

    def resizeEvent(self, event):
        super(Qss, self).resizeEvent(event)
        self._get_rect()

    def _get_rect(self):
        width, height = self.width(), self.height()
        margin = self._margin * 2
        self._t_rect = [QPoint(x, y) for x in range(margin, width - margin) for y in range(0, margin)]
        self._b_rect = [QPoint(x, y) for x in range(margin, width - margin) for y in
                        range(height - margin, height)]
        self._l_rect = [QPoint(x, y) for x in range(0, margin) for y in range(margin, height - margin)]
        self._r_rect = [QPoint(x, y) for x in range(width - margin, width) for y in
                        range(margin, height - margin)]
        self._bl_rect = [QPoint(x, y) for x in range(0, margin) for y in range(height - margin, height)]
        self._br_rect = [QPoint(x, y) for x in range(width - margin, width) for y in
                         range(height - margin, height)]
        self._tl_rect = [QPoint(x, y) for x in range(0, margin) for y in range(0, margin)]
        self._tr_rect = [QPoint(x, y) for x in range(width - margin, width) for y in range(0, margin)]

    def leaveEvent(self, event):
        super(Qss, self).leaveEvent(event)
        self.setCursor(Qt.ArrowCursor)

    def paintEvent(self, event):
        super(Qss, self).paintEvent(event)
        opt = QStyleOption()
        opt.initFrom(self)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, painter, self)

    def eventFilter(self, obj, event):
        if obj == self.text_edit and isinstance(event, QEnterEvent):
            self.setCursor(Qt.ArrowCursor)

        return QDialog.eventFilter(self, obj, event)


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    from pyqss import Qss

    app = QApplication(sys.argv)
    qss = Qss()
    qss.setStyleSheet(open('default.qss', 'r').read())
    qss.show()
    app.exec_()
