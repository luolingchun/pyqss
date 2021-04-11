# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/3/15 17:42
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel


class QTest(QMainWindow):
    def __init__(self):
        super(QTest, self).__init__()


if __name__ == '__main__':
    # 适配高分辨率
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication([])
    window = QTest()
    pushbutton = QPushButton('button', window)
    pushbutton.setObjectName('button')
    pushbutton.move(20, 20)
    label = QLabel("label", window)
    label.setObjectName('label')
    label.move(20, 80)
    window.show()
    window.resize(300, 400)

    from pyqss import Qss

    # qss = Qss(window, language='en')
    qss = Qss(window, language='zh')
    qss.show()

    app.exec_()
