# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/12/13 14:11
from pyqss.ui.main import Ui_QssWindow
from pyqss.widgets.frameless_window import FramelessWindow


class QssWindow(FramelessWindow, Ui_QssWindow):
    def __init__(self):
        super(QssWindow, self).__init__()
        # 初始化界面
        self.setupUi(self)

    def retranslateUi(self, a):
        self.labelIcon.setText(self.tr("Q"))
        self.btnOpen.setText(self.tr("open"))
        self.btnSave.setText(self.tr("save"))
        self.labelTitle.setText(self.tr("QSS Editor"))
        self.btnAttach.setText(self.tr("~"))
        self.btnMin.setText(self.tr("0"))
        self.btnClose.setText(self.tr("r"))
