# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/3/15 17:42
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel

if __name__ == '__main__':

    # 适配高分辨率
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication([])
    window = QMainWindow()
    pushbutton = QPushButton('button', window)
    pushbutton.setObjectName('button')
    pushbutton.move(20, 20)
    label = QLabel("label", window)
    label.move(20, 80)
    window.show()
    window.resize(300, 400)

    from pyqss import Qss

    qss = Qss(window, language='en')
    qss.show()

    app.exec_()
