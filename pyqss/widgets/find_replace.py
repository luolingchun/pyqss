# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/12/13 17:55
from PyQt5.QtWidgets import QWidget

from pyqss.ui.find_replace import Ui_widget


class FRWidget(QWidget, Ui_widget):
    def __init__(self, parent=None):
        super(FRWidget, self).__init__(parent)
        self.setupUi(self)

        self.setMinimumHeight(60)

    def mouseMoveEvent(self, event):
        pass
