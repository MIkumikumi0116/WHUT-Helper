# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'f:\Code\WHUT-Helper\Message_Window_UI.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Message_Window_UI(object):
    def setupUi(self, Message_Window_UI):
        Message_Window_UI.setObjectName("Message_Window_UI")
        Message_Window_UI.resize(450, 270)
        self.Central_Widget = QtWidgets.QWidget(Message_Window_UI)
        self.Central_Widget.setObjectName("Central_Widget")
        self.Central_Widget_Layout = QtWidgets.QVBoxLayout(self.Central_Widget)
        self.Central_Widget_Layout.setObjectName("Central_Widget_Layout")
        self.Massage_Panel = QtWidgets.QWidget(self.Central_Widget)
        self.Massage_Panel.setObjectName("Massage_Panel")
        self.Massage_Panel_Layout = QtWidgets.QVBoxLayout(self.Massage_Panel)
        self.Massage_Panel_Layout.setObjectName("Massage_Panel_Layout")
        self.Close_Button_Layout = QtWidgets.QHBoxLayout()
        self.Close_Button_Layout.setObjectName("Close_Button_Layout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.Close_Button_Layout.addItem(spacerItem)
        self.Close_Button = QtWidgets.QPushButton(self.Massage_Panel)
        self.Close_Button.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/all_images/res/Exit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Close_Button.setIcon(icon)
        self.Close_Button.setObjectName("Close_Button")
        self.Close_Button_Layout.addWidget(self.Close_Button)
        self.Massage_Panel_Layout.addLayout(self.Close_Button_Layout)
        self.Massage_Layout = QtWidgets.QHBoxLayout()
        self.Massage_Layout.setObjectName("Massage_Layout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.Massage_Layout.addItem(spacerItem1)
        self.Massage_Label = QtWidgets.QLabel(self.Massage_Panel)
        self.Massage_Label.setObjectName("Massage_Label")
        self.Massage_Layout.addWidget(self.Massage_Label)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.Massage_Layout.addItem(spacerItem2)
        self.Massage_Panel_Layout.addLayout(self.Massage_Layout)
        self.Confirm_Layout = QtWidgets.QHBoxLayout()
        self.Confirm_Layout.setObjectName("Confirm_Layout")
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.Confirm_Layout.addItem(spacerItem3)
        self.Confirm_Button = QtWidgets.QPushButton(self.Massage_Panel)
        self.Confirm_Button.setObjectName("Confirm_Button")
        self.Confirm_Layout.addWidget(self.Confirm_Button)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.Confirm_Layout.addItem(spacerItem4)
        self.Massage_Panel_Layout.addLayout(self.Confirm_Layout)
        self.Central_Widget_Layout.addWidget(self.Massage_Panel)
        Message_Window_UI.setCentralWidget(self.Central_Widget)

        self.retranslateUi(Message_Window_UI)
        QtCore.QMetaObject.connectSlotsByName(Message_Window_UI)

    def retranslateUi(self, Message_Window_UI):
        _translate = QtCore.QCoreApplication.translate
        Message_Window_UI.setWindowTitle(_translate("Message_Window_UI", "消息"))
        self.Massage_Label.setText(_translate("Message_Window_UI", "       "))
        self.Confirm_Button.setText(_translate("Message_Window_UI", "OKK"))
import All_Res_rc
