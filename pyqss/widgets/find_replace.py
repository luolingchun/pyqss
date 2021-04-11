# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/12/13 17:55
from PyQt5.QtWidgets import QWidget

from pyqss.ui.find_replace import Ui_widget


class FRWidget(QWidget, Ui_widget):
    def __init__(self, tr, parent=None):
        super(FRWidget, self).__init__(parent)
        # 初始化语言
        self.tr = tr
        self.setupUi(self)

        self.setMinimumHeight(60)

    def retranslateUi(self, a):
        self.btnPre.setToolTip(self.tr("pre"))
        self.btnPre.setText(self.tr("h"))
        self.btnNext.setToolTip(self.tr("next"))
        self.btnNext.setText(self.tr("i"))
        self.btnReplace.setToolTip(self.tr("replace"))
        self.btnReplace.setText(self.tr("P"))
        self.btnReplaceAll.setToolTip(self.tr("replace all"))
        self.btnReplaceAll.setText(self.tr("R"))

    def mouseMoveEvent(self, event):
        pass
