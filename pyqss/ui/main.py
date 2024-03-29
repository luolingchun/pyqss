# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_QssWindow(object):
    def setupUi(self, QssWindow):
        QssWindow.setObjectName("QssWindow")
        QssWindow.resize(665, 497)
        QssWindow.setMouseTracking(True)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon/images/icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        QssWindow.setWindowIcon(icon)
        self.QssWidget = QtWidgets.QWidget(QssWindow)
        self.QssWidget.setMouseTracking(True)
        self.QssWidget.setObjectName("QssWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.QssWidget)
        self.verticalLayout.setContentsMargins(4, 4, 4, 4)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget_top = QtWidgets.QWidget(self.QssWidget)
        self.widget_top.setMaximumSize(QtCore.QSize(16777215, 48))
        self.widget_top.setMouseTracking(True)
        self.widget_top.setObjectName("widget_top")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget_top)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.labelIcon = QtWidgets.QLabel(self.widget_top)
        self.labelIcon.setMouseTracking(True)
        self.labelIcon.setAlignment(QtCore.Qt.AlignCenter)
        self.labelIcon.setObjectName("labelIcon")
        self.horizontalLayout.addWidget(self.labelIcon)
        self.btnOpen = QtWidgets.QPushButton(self.widget_top)
        self.btnOpen.setMouseTracking(True)
        self.btnOpen.setObjectName("btnOpen")
        self.horizontalLayout.addWidget(self.btnOpen)
        self.btnSave = QtWidgets.QPushButton(self.widget_top)
        self.btnSave.setMouseTracking(True)
        self.btnSave.setObjectName("btnSave")
        self.horizontalLayout.addWidget(self.btnSave)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.labelTitle = QtWidgets.QLabel(self.widget_top)
        self.labelTitle.setMouseTracking(True)
        self.labelTitle.setObjectName("labelTitle")
        self.horizontalLayout.addWidget(self.labelTitle)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.btnAttach = QtWidgets.QPushButton(self.widget_top)
        self.btnAttach.setMouseTracking(True)
        self.btnAttach.setCheckable(True)
        self.btnAttach.setChecked(True)
        self.btnAttach.setObjectName("btnAttach")
        self.horizontalLayout.addWidget(self.btnAttach)
        self.btnMin = QtWidgets.QPushButton(self.widget_top)
        self.btnMin.setMouseTracking(True)
        self.btnMin.setObjectName("btnMin")
        self.horizontalLayout.addWidget(self.btnMin)
        self.btnClose = QtWidgets.QPushButton(self.widget_top)
        self.btnClose.setMouseTracking(True)
        self.btnClose.setObjectName("btnClose")
        self.horizontalLayout.addWidget(self.btnClose)
        self.verticalLayout.addWidget(self.widget_top)
        self.editor = QssEditor(self.QssWidget)
        self.editor.setMouseTracking(True)
        self.editor.setObjectName("editor")
        self.verticalLayout.addWidget(self.editor)
        QssWindow.setCentralWidget(self.QssWidget)

        self.retranslateUi(QssWindow)
        QtCore.QMetaObject.connectSlotsByName(QssWindow)

    def retranslateUi(self, QssWindow):
        _translate = QtCore.QCoreApplication.translate
        QssWindow.setWindowTitle(_translate("QssWindow", "MainWindow"))
        self.labelIcon.setText(_translate("QssWindow", "Q"))
        self.btnOpen.setText(_translate("QssWindow", "open"))
        self.btnSave.setText(_translate("QssWindow", "save"))
        self.labelTitle.setText(_translate("QssWindow", "QSS Editor"))
        self.btnAttach.setText(_translate("QssWindow", "~"))
        self.btnMin.setText(_translate("QssWindow", "0"))
        self.btnClose.setText(_translate("QssWindow", "r"))
from pyqss.sci.editor import QssEditor
from . import images_rc
