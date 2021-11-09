# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\AhJayzZ\Desktop\NTUST\Project\Smart-Learning-System\project_codes\GUI\GUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SmartLearningSystemGUI(object):
    def setupUi(self, SmartLearningSystemGUI):
        SmartLearningSystemGUI.setObjectName("SmartLearningSystemGUI")
        SmartLearningSystemGUI.resize(1370, 1006)
        SmartLearningSystemGUI.setStyleSheet("color:black")
        self.centralwidget = QtWidgets.QWidget(SmartLearningSystemGUI)
        self.centralwidget.setObjectName("centralwidget")
        self.brightness_label = QtWidgets.QLabel(self.centralwidget)
        self.brightness_label.setGeometry(QtCore.QRect(870, 780, 141, 41))
        font = QtGui.QFont()
        font.setFamily("標楷體")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.brightness_label.setFont(font)
        self.brightness_label.setObjectName("brightness_label")
        self.camera_label = QtWidgets.QLabel(self.centralwidget)
        self.camera_label.setGeometry(QtCore.QRect(10, 10, 821, 711))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(20)
        self.camera_label.setFont(font)
        self.camera_label.setFrameShape(QtWidgets.QFrame.Panel)
        self.camera_label.setFrameShadow(QtWidgets.QFrame.Plain)
        self.camera_label.setScaledContents(False)
        self.camera_label.setAlignment(QtCore.Qt.AlignCenter)
        self.camera_label.setObjectName("camera_label")
        self.contrast_label = QtWidgets.QLabel(self.centralwidget)
        self.contrast_label.setGeometry(QtCore.QRect(870, 730, 151, 41))
        font = QtGui.QFont()
        font.setFamily("標楷體")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.contrast_label.setFont(font)
        self.contrast_label.setObjectName("contrast_label")
        self.translate_box = QtWidgets.QTextEdit(self.centralwidget)
        self.translate_box.setEnabled(True)
        self.translate_box.setGeometry(QtCore.QRect(840, 410, 521, 310))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.translate_box.setFont(font)
        self.translate_box.setObjectName("translate_box")
        self.translate_label = QtWidgets.QLabel(self.centralwidget)
        self.translate_label.setGeometry(QtCore.QRect(840, 360, 151, 41))
        font = QtGui.QFont()
        font.setFamily("標楷體")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.translate_label.setFont(font)
        self.translate_label.setObjectName("translate_label")
        self.result_label = QtWidgets.QLabel(self.centralwidget)
        self.result_label.setGeometry(QtCore.QRect(840, 0, 161, 41))
        font = QtGui.QFont()
        font.setFamily("標楷體")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.result_label.setFont(font)
        self.result_label.setObjectName("result_label")
        self.back_btn = QtWidgets.QPushButton(self.centralwidget)
        self.back_btn.setGeometry(QtCore.QRect(870, 900, 441, 50))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.back_btn.setFont(font)
        self.back_btn.setObjectName("back_btn")
        self.result_box = QtWidgets.QTextEdit(self.centralwidget)
        self.result_box.setGeometry(QtCore.QRect(840, 40, 521, 310))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.result_box.setFont(font)
        self.result_box.setObjectName("result_box")
        self.camera_select_label = QtWidgets.QLabel(self.centralwidget)
        self.camera_select_label.setGeometry(QtCore.QRect(10, 740, 81, 41))
        font = QtGui.QFont()
        font.setFamily("標楷體")
        font.setPointSize(20)
        self.camera_select_label.setFont(font)
        self.camera_select_label.setObjectName("camera_select_label")
        self.translate_btn = QtWidgets.QPushButton(self.centralwidget)
        self.translate_btn.setGeometry(QtCore.QRect(1060, 360, 100, 40))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.translate_btn.setFont(font)
        self.translate_btn.setObjectName("translate_btn")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 800, 191, 151))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.frameShow_layout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.frameShow_layout.setContentsMargins(0, 0, 0, 0)
        self.frameShow_layout.setObjectName("frameShow_layout")
        self.frameshow_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("標楷體")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.frameshow_label.setFont(font)
        self.frameshow_label.setObjectName("frameshow_label")
        self.frameShow_layout.addWidget(self.frameshow_label)
        self.frameDefault_btn = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("標楷體")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.frameDefault_btn.setFont(font)
        self.frameDefault_btn.setChecked(True)
        self.frameDefault_btn.setObjectName("frameDefault_btn")
        self.frameShow_layout.addWidget(self.frameDefault_btn)
        self.frameHorizontal_btn = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("標楷體")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.frameHorizontal_btn.setFont(font)
        self.frameHorizontal_btn.setObjectName("frameHorizontal_btn")
        self.frameShow_layout.addWidget(self.frameHorizontal_btn)
        self.frameVertical_btn = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("標楷體")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.frameVertical_btn.setFont(font)
        self.frameVertical_btn.setObjectName("frameVertical_btn")
        self.frameShow_layout.addWidget(self.frameVertical_btn)
        self.frameInverse_btn = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("標楷體")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.frameInverse_btn.setFont(font)
        self.frameInverse_btn.setObjectName("frameInverse_btn")
        self.frameShow_layout.addWidget(self.frameInverse_btn)
        self.contrast_scrollbar = QtWidgets.QSlider(self.centralwidget)
        self.contrast_scrollbar.setGeometry(QtCore.QRect(1040, 740, 160, 22))
        self.contrast_scrollbar.setOrientation(QtCore.Qt.Horizontal)
        self.contrast_scrollbar.setTickInterval(1)
        self.contrast_scrollbar.setObjectName("contrast_scrollbar")
        self.language_selector = QtWidgets.QComboBox(self.centralwidget)
        self.language_selector.setGeometry(QtCore.QRect(590, 740, 251, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.language_selector.setFont(font)
        self.language_selector.setEditable(False)
        self.language_selector.setCurrentText("")
        self.language_selector.setPlaceholderText("")
        self.language_selector.setObjectName("language_selector")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(10, 10, 821, 711))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.camera_selector = QtWidgets.QComboBox(self.centralwidget)
        self.camera_selector.setGeometry(QtCore.QRect(100, 740, 221, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.camera_selector.setFont(font)
        self.camera_selector.setEditable(False)
        self.camera_selector.setCurrentText("")
        self.camera_selector.setPlaceholderText("")
        self.camera_selector.setObjectName("camera_selector")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(210, 800, 631, 151))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.state_layout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.state_layout.setContentsMargins(0, 0, 0, 0)
        self.state_layout.setObjectName("state_layout")
        self.state_label = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.state_label.setFont(font)
        self.state_label.setAutoFillBackground(False)
        self.state_label.setObjectName("state_label")
        self.state_layout.addWidget(self.state_label)
        self.warning_label = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.warning_label.setFont(font)
        self.warning_label.setAutoFillBackground(False)
        self.warning_label.setObjectName("warning_label")
        self.state_layout.addWidget(self.warning_label)
        self.add_btn = QtWidgets.QPushButton(self.centralwidget)
        self.add_btn.setGeometry(QtCore.QRect(1170, 360, 191, 40))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.add_btn.setFont(font)
        self.add_btn.setObjectName("add_btn")
        self.sound_btn = QtWidgets.QPushButton(self.centralwidget)
        self.sound_btn.setGeometry(QtCore.QRect(950, 360, 100, 40))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.sound_btn.setFont(font)
        self.sound_btn.setObjectName("sound_btn")
        self.brightness_scrollbar = QtWidgets.QSlider(self.centralwidget)
        self.brightness_scrollbar.setGeometry(QtCore.QRect(1040, 790, 160, 22))
        self.brightness_scrollbar.setOrientation(QtCore.Qt.Horizontal)
        self.brightness_scrollbar.setTickPosition(QtWidgets.QSlider.NoTicks)
        self.brightness_scrollbar.setTickInterval(1)
        self.brightness_scrollbar.setObjectName("brightness_scrollbar")
        self.language_label = QtWidgets.QLabel(self.centralwidget)
        self.language_label.setGeometry(QtCore.QRect(360, 740, 221, 41))
        font = QtGui.QFont()
        font.setFamily("標楷體")
        font.setPointSize(20)
        self.language_label.setFont(font)
        self.language_label.setObjectName("language_label")
        self.init_btn = QtWidgets.QPushButton(self.centralwidget)
        self.init_btn.setGeometry(QtCore.QRect(870, 840, 441, 50))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.init_btn.setFont(font)
        self.init_btn.setObjectName("init_btn")
        self.tableWidget.raise_()
        self.brightness_label.raise_()
        self.camera_label.raise_()
        self.contrast_label.raise_()
        self.translate_box.raise_()
        self.translate_label.raise_()
        self.result_label.raise_()
        self.back_btn.raise_()
        self.result_box.raise_()
        self.camera_select_label.raise_()
        self.translate_btn.raise_()
        self.verticalLayoutWidget.raise_()
        self.contrast_scrollbar.raise_()
        self.language_selector.raise_()
        self.camera_selector.raise_()
        self.verticalLayoutWidget_2.raise_()
        self.add_btn.raise_()
        self.sound_btn.raise_()
        self.brightness_scrollbar.raise_()
        self.language_label.raise_()
        self.init_btn.raise_()
        SmartLearningSystemGUI.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(SmartLearningSystemGUI)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1370, 25))
        self.menubar.setObjectName("menubar")
        SmartLearningSystemGUI.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(SmartLearningSystemGUI)
        self.statusbar.setObjectName("statusbar")
        SmartLearningSystemGUI.setStatusBar(self.statusbar)

        self.retranslateUi(SmartLearningSystemGUI)
        self.language_selector.setCurrentIndex(-1)
        self.camera_selector.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(SmartLearningSystemGUI)

    def retranslateUi(self, SmartLearningSystemGUI):
        _translate = QtCore.QCoreApplication.translate
        SmartLearningSystemGUI.setWindowTitle(_translate("SmartLearningSystemGUI", "MainWindow"))
        self.brightness_label.setText(_translate("SmartLearningSystemGUI", " 亮度(0):"))
        self.camera_label.setText(_translate("SmartLearningSystemGUI", "ThisLabelWillBeChangedToVideoFrame"))
        self.contrast_label.setText(_translate("SmartLearningSystemGUI", " 對比(1.0):"))
        self.translate_label.setText(_translate("SmartLearningSystemGUI", "翻譯結果 "))
        self.result_label.setText(_translate("SmartLearningSystemGUI", "辨識結果 "))
        self.back_btn.setText(_translate("SmartLearningSystemGUI", " 返回主頁面"))
        self.camera_select_label.setText(_translate("SmartLearningSystemGUI", "鏡頭:"))
        self.translate_btn.setText(_translate("SmartLearningSystemGUI", " 翻譯"))
        self.frameshow_label.setText(_translate("SmartLearningSystemGUI", "顯示模式:"))
        self.frameDefault_btn.setText(_translate("SmartLearningSystemGUI", "影像正常顯示"))
        self.frameHorizontal_btn.setText(_translate("SmartLearningSystemGUI", "影像水平反轉"))
        self.frameVertical_btn.setText(_translate("SmartLearningSystemGUI", "影像垂直反轉"))
        self.frameInverse_btn.setText(_translate("SmartLearningSystemGUI", "影像水平垂直反轉"))
        self.state_label.setText(_translate("SmartLearningSystemGUI", "現在狀態:Initial"))
        self.warning_label.setText(_translate("SmartLearningSystemGUI", "光線狀態:正常"))
        self.add_btn.setText(_translate("SmartLearningSystemGUI", " 新增至單字本"))
        self.sound_btn.setText(_translate("SmartLearningSystemGUI", "  發音"))
        self.language_label.setText(_translate("SmartLearningSystemGUI", "句子翻譯語言:"))
        self.init_btn.setText(_translate("SmartLearningSystemGUI", " 設定初始化"))
