# -*- coding: utf-8 -*-
# @Time    : 2019/4/12 10:20
# @Author  : llc
# @File    : frameless_window.py

from PyQt5.Qsci import QsciScintilla
from PyQt5.QtCore import Qt, QPoint, pyqtSignal
from PyQt5.QtGui import QPainter, QEnterEvent, QPen, QColor
from PyQt5.QtWidgets import QDialog, QStyleOption, QStyle


class FramelessWindow(QDialog):
    resized = pyqtSignal()

    def __init__(self):
        super(FramelessWindow, self).__init__()
        self.margin = 4
        self._top_drag = False
        self._bottom_drag = False
        self._left_drag = False
        self._right_drag = False
        self._bottom_left_drag = False
        self._bottom_right_drag = False
        self._top_left_drag = False
        self._top_right_drag = False
        self._start_point = None
        self._move_flag = False
        self.setMouseTracking(True)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.Dialog |
                            Qt.FramelessWindowHint |
                            Qt.WindowSystemMenuHint |
                            Qt.WindowMinMaxButtonsHint)

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
            self._move_flag = True
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
        elif event.buttons() == Qt.LeftButton and self._start_point and self._move_flag:
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
        super(FramelessWindow, self).resizeEvent(event)
        self._get_rect()
        self.resized.emit()

    def _get_rect(self):
        width, height = self.width(), self.height()
        margin = self.margin * 2
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
        super(FramelessWindow, self).leaveEvent(event)
        self.setCursor(Qt.ArrowCursor)

    def paintEvent(self, event):
        """无边框透明后圆角问题"""
        super(FramelessWindow, self).paintEvent(event)
        opt = QStyleOption()
        opt.initFrom(self)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(QColor(0, 0, 0, 1), 2 * self.margin))
        painter.drawRect(self.rect())
        self.style().drawPrimitive(QStyle.PE_Widget, opt, painter, self)

    def eventFilter(self, obj, event):
        if isinstance(obj, QsciScintilla) and isinstance(event, QEnterEvent):
            self.setCursor(Qt.ArrowCursor)

        return QDialog.eventFilter(self, obj, event)
