# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/3/15 17:42


if __name__ == '__main__':
    from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton

    app = QApplication([])
    window = QMainWindow()
    pushbutton = QPushButton('test', parent=window)
    pushbutton.setObjectName('PPPP')
    pushbutton.move(20, 20)
    window.show()

    from pyqss import Qss

    qss = Qss(window)
    qss.show()

    app.exec_()
