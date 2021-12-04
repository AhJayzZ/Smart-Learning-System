# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\AhJayzZ\Desktop\NTUST\Project\Smart-Learning-System\project_codes\GUI\loginPage.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_loginPage(object):
    def setupUi(self, loginPage):
        loginPage.setObjectName("loginPage")
        loginPage.resize(741, 259)
        self.loginButton = QtWidgets.QPushButton(loginPage)
        self.loginButton.setGeometry(QtCore.QRect(400, 140, 151, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.loginButton.setFont(font)
        self.loginButton.setObjectName("loginButton")
        self.exitButton = QtWidgets.QPushButton(loginPage)
        self.exitButton.setGeometry(QtCore.QRect(570, 200, 151, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.exitButton.setFont(font)
        self.exitButton.setObjectName("exitButton")
        self.reviewWebsiteButton = QtWidgets.QPushButton(loginPage)
        self.reviewWebsiteButton.setGeometry(QtCore.QRect(570, 140, 151, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.reviewWebsiteButton.setFont(font)
        self.reviewWebsiteButton.setObjectName("reviewWebsiteButton")
        self.titleLabel = QtWidgets.QLabel(loginPage)
        self.titleLabel.setGeometry(QtCore.QRect(10, 10, 721, 91))
        font = QtGui.QFont()
        font.setFamily("Tw Cen MT Condensed Extra Bold")
        font.setPointSize(30)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.titleLabel.setFont(font)
        self.titleLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.titleLabel.setObjectName("titleLabel")
        self.guideButton = QtWidgets.QPushButton(loginPage)
        self.guideButton.setGeometry(QtCore.QRect(400, 200, 151, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.guideButton.setFont(font)
        self.guideButton.setObjectName("guideButton")
        self.groupBox = QtWidgets.QGroupBox(loginPage)
        self.groupBox.setGeometry(QtCore.QRect(20, 140, 361, 101))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.groupBox.setFont(font)
        self.groupBox.setAutoFillBackground(False)
        self.groupBox.setStyleSheet("")
        self.groupBox.setTitle("")
        self.groupBox.setFlat(False)
        self.groupBox.setObjectName("groupBox")
        self.accountTextbox = QtWidgets.QLineEdit(self.groupBox)
        self.accountTextbox.setGeometry(QtCore.QRect(80, 10, 271, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.accountTextbox.setFont(font)
        self.accountTextbox.setCursorPosition(0)
        self.accountTextbox.setObjectName("accountTextbox")
        self.passwordTextbox = QtWidgets.QLineEdit(self.groupBox)
        self.passwordTextbox.setGeometry(QtCore.QRect(80, 60, 271, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.passwordTextbox.setFont(font)
        self.passwordTextbox.setFrame(True)
        self.passwordTextbox.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passwordTextbox.setClearButtonEnabled(False)
        self.passwordTextbox.setObjectName("passwordTextbox")
        self.accountLabel = QtWidgets.QLabel(self.groupBox)
        self.accountLabel.setGeometry(QtCore.QRect(10, 10, 61, 25))
        font = QtGui.QFont()
        font.setFamily("華康新儷粗黑")
        font.setPointSize(15)
        font.setBold(False)
        font.setWeight(50)
        self.accountLabel.setFont(font)
        self.accountLabel.setObjectName("accountLabel")
        self.passwordLabel = QtWidgets.QLabel(self.groupBox)
        self.passwordLabel.setGeometry(QtCore.QRect(10, 60, 61, 25))
        font = QtGui.QFont()
        font.setFamily("華康儷粗黑")
        font.setPointSize(15)
        font.setBold(False)
        font.setWeight(50)
        self.passwordLabel.setFont(font)
        self.passwordLabel.setObjectName("passwordLabel")
        self.groupBox.raise_()
        self.loginButton.raise_()
        self.exitButton.raise_()
        self.reviewWebsiteButton.raise_()
        self.titleLabel.raise_()
        self.guideButton.raise_()

        self.retranslateUi(loginPage)
        QtCore.QMetaObject.connectSlotsByName(loginPage)

    def retranslateUi(self, loginPage):
        _translate = QtCore.QCoreApplication.translate
        loginPage.setWindowTitle(_translate("loginPage", "Dialog"))
        self.loginButton.setText(_translate("loginPage", "登入"))
        self.exitButton.setText(_translate("loginPage", "離開"))
        self.reviewWebsiteButton.setText(_translate("loginPage", "複習網頁"))
        self.titleLabel.setText(_translate("loginPage", "Smart  Learning  System"))
        self.guideButton.setText(_translate("loginPage", "使用說明"))
        self.accountLabel.setText(_translate("loginPage", "帳號:"))
        self.passwordLabel.setText(_translate("loginPage", "密碼:"))