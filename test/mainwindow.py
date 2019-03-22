# -*- coding: utf-8 -*-
# @Time    : 2019/3/22 10:26
# @Author  : llc
# @File    : mainwindow.py

from PyQt5.QtWidgets import QMainWindow
try:
    from .ui import *
except:
    from ui import *


class Form(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Form, self).__init__()

        self.setupUi(self)


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    form = Form()
    form.show()

    # 加载QSS编辑器
    from pyqss import Qss

    qss = Qss(form)
    qss.show()


    app.exec_()
