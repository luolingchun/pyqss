# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/12/13 14:11

from ui.main import Ui_QssWindow
from .frameless_window import FramelessWindow


class QssWindow(FramelessWindow, Ui_QssWindow):
    def __init__(self, parent=None):
        super(QssWindow, self).__init__(parent)
        # 初始化界面
        self.setupUi(self)
