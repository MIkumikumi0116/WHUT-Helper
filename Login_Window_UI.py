# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'f:\Code\WHUT-Helper\Login_Window_UI.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Login_Window_UI(object):
    def setupUi(self, Login_Window_UI):
        Login_Window_UI.setObjectName("Login_Window_UI")
        Login_Window_UI.setEnabled(True)
        Login_Window_UI.resize(480, 320)
        self.Central_Widget = QtWidgets.QWidget(Login_Window_UI)
        self.Central_Widget.setObjectName("Central_Widget")
        self.Central_Widget_Layout = QtWidgets.QVBoxLayout(self.Central_Widget)
        self.Central_Widget_Layout.setObjectName("Central_Widget_Layout")
        self.Main_Panel = QtWidgets.QWidget(self.Central_Widget)
        self.Main_Panel.setObjectName("Main_Panel")
        self.Main_Panel_Layout = QtWidgets.QVBoxLayout(self.Main_Panel)
        self.Main_Panel_Layout.setObjectName("Main_Panel_Layout")
        self.Close_Button_Layout = QtWidgets.QHBoxLayout()
        self.Close_Button_Layout.setObjectName("Close_Button_Layout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.Close_Button_Layout.addItem(spacerItem)
        self.Close_Button = QtWidgets.QPushButton(self.Main_Panel)
        self.Close_Button.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/all_images/res/Exit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Close_Button.setIcon(icon)
        self.Close_Button.setObjectName("Close_Button")
        self.Close_Button_Layout.addWidget(self.Close_Button)
        self.Main_Panel_Layout.addLayout(self.Close_Button_Layout)
        self.Login_Panel = QtWidgets.QWidget(self.Main_Panel)
        self.Login_Panel.setObjectName("Login_Panel")
        self.Login_Panel_Layout = QtWidgets.QHBoxLayout(self.Login_Panel)
        self.Login_Panel_Layout.setObjectName("Login_Panel_Layout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.Login_Panel_Layout.addItem(spacerItem1)
        self.Login_Layout = QtWidgets.QVBoxLayout()
        self.Login_Layout.setObjectName("Login_Layout")
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.Login_Layout.addItem(spacerItem2)
        self.Name_Layout = QtWidgets.QHBoxLayout()
        self.Name_Layout.setObjectName("Name_Layout")
        self.Name_Label = QtWidgets.QLabel(self.Login_Panel)
        self.Name_Label.setObjectName("Name_Label")
        self.Name_Layout.addWidget(self.Name_Label)
        self.Name_LineEdit = QtWidgets.QLineEdit(self.Login_Panel)
        self.Name_LineEdit.setObjectName("Name_LineEdit")
        self.Name_Layout.addWidget(self.Name_LineEdit)
        self.Login_Layout.addLayout(self.Name_Layout)
        self.Password_Layout = QtWidgets.QHBoxLayout()
        self.Password_Layout.setObjectName("Password_Layout")
        self.Password_Label = QtWidgets.QLabel(self.Login_Panel)
        self.Password_Label.setObjectName("Password_Label")
        self.Password_Layout.addWidget(self.Password_Label)
        self.Password_LineEdit = QtWidgets.QLineEdit(self.Login_Panel)
        self.Password_LineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.Password_LineEdit.setObjectName("Password_LineEdit")
        self.Password_Layout.addWidget(self.Password_LineEdit)
        self.Login_Layout.addLayout(self.Password_Layout)
        self.Login_Button = QtWidgets.QPushButton(self.Login_Panel)
        self.Login_Button.setObjectName("Login_Button")
        self.Login_Layout.addWidget(self.Login_Button)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.Login_Layout.addItem(spacerItem3)
        self.Login_Panel_Layout.addLayout(self.Login_Layout)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.Login_Panel_Layout.addItem(spacerItem4)
        self.Main_Panel_Layout.addWidget(self.Login_Panel)
        self.Central_Widget_Layout.addWidget(self.Main_Panel)
        Login_Window_UI.setCentralWidget(self.Central_Widget)

        self.retranslateUi(Login_Window_UI)
        QtCore.QMetaObject.connectSlotsByName(Login_Window_UI)

    def retranslateUi(self, Login_Window_UI):
        _translate = QtCore.QCoreApplication.translate
        Login_Window_UI.setWindowTitle(_translate("Login_Window_UI", "登录"))
        self.Name_Label.setText(_translate("Login_Window_UI", "学号"))
        self.Password_Label.setText(_translate("Login_Window_UI", "密码"))
        self.Login_Button.setText(_translate("Login_Window_UI", "登录"))
        self.Login_Button.setShortcut(_translate("Login_Window_UI", "Return"))
import All_Res_rc
