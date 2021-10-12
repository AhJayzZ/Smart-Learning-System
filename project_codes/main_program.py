from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from GUI.Ui_GUI import *
from image_recognition.recognition_program import *

from image_recognition import text_to_speech
from googletrans import Translator
from GUI import languages
import cv2
import numpy
import sys

# 建立類別來繼承 Ui_SmartLearningSystemGUI 介面程式
class MainWindow(QtWidgets.QMainWindow, Ui_SmartLearningSystemGUI):
    def __init__(self, parent=None):
        # 繼承Ui_Gui.py
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle('Smart Learning System v1.0')
        self.setWindowIcon(QtGui.QIcon('project_codes/GUI/GUI_icon.png'))

        # Recognition program
        self.Recognition = RecognitionProgram()
        self.frame = self.Recognition.output_img
        self.contrast = 1
        self.brightness = 0

        # Finish Flag setting(Avoid duplicated translation)
        self.FinishFlag = False
        self.triggerCount = 0

        # Constrast and brightness scrollbar setting
        self.brightness_scrollbar.setValue(0)
        self.brightness_scrollbar.setMinimum(-100)
        self.brightness_scrollbar.setMaximum(100)
        self.contrast_scrollbar.setValue(100)
        self.contrast_scrollbar.setMinimum(0)
        self.contrast_scrollbar.setMaximum(300)

        # Camera setting
        camera_array = ['Camera 0(Webcam)', 'Camera 1(External Camera)']
        self.camera_selector.addItems(camera_array)

        # Language setting(index 15 means Chinese Traditional)
        self.lang = 'zh-tw'
        self.translator = Translator()
        self.languages_key_array, self.languages_value_array = languages.langauge_data()
        self.language_selector.addItems(self.languages_value_array)
        self.language_selector.setCurrentIndex(15)

        # Timer setting
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh)
        self.timer.start(10)

        # result & translated box setting
        self.result_box.textChanged.connect(self.translate)
        self.translated_box.setReadOnly(True)

        # Button trigger setting
        self.confirm_btn.clicked.connect(self.add_btn_click)
        self.clear_btn.clicked.connect(self.clear_btn_click)
        self.exit_btn.clicked.connect(sys.exit)

        # Combobox trigger setting
        self.camera_selector.currentTextChanged.connect(self.camera_selector_changed)
        self.language_selector.currentTextChanged.connect(self.languages_selector_changed)

        # Scorllbar trigger setting
        self.brightness_scrollbar.valueChanged.connect(self.frame_contrast_brightness_check)
        self.contrast_scrollbar.valueChanged.connect(self.frame_contrast_brightness_check)

    # add clear the box and set the box that revise_textbox typed
    def add_btn_click(self):
        self.result_box.setText(self.revise_textbox.text())
        self.revise_textbox.clear()

    # clear all box
    def clear_btn_click(self):
        self.result_box.clear()
        self.translated_box.clear()
        self.revise_textbox.clear()

    # translate english text to translated language(too many request the translate function will be disable)
    def translate(self):
        self.triggerCount = self.triggerCount + 1
        if self.triggerCount >= 5 or self.FinishFlag == True:
            self.triggerCount = 0
            text = self.result_box.toPlainText()
            self.translated_box.clear()
            self.revise_textbox.clear()
            try:
                if text == "":
                    result = ""
                else:
                    print('googletrans triggered')
                    result = self.translator.translate(text, dest=self.lang, timeout=3).text
                self.translated_box.setText(result)
            except:
                pass

    # change camera to the choosen one
    def camera_selector_changed(self):
        index = self.camera_selector.currentIndex()
        if index == 0:
            self.Recognition.cap = cv2.VideoCapture(0)
        else:
            self.Recognition.cap = cv2.VideoCapture(index,cv2.CAP_DSHOW)

    # change to the translated langauge
    def languages_selector_changed(self):
        index = self.language_selector.currentIndex()
        self.lang = self.languages_key_array[index]
        self.translate()

    # GUI camera frame check
    def frame_check(self):
        self.frame = cv2.convertScaleAbs(self.Recognition.output_img,alpha=self.contrast,beta=self.brightness)
        self.average_gray_value = numpy.mean(self.frame)
        if self.frameHorizontal_btn.isChecked():
            self.frame = cv2.flip(self.frame, 1)
        elif self.frameVertical_btn.isChecked():
            self.frame = cv2.flip(self.frame, 0)
        elif self.frameInverse_btn.isChecked():
            self.frame = cv2.flip(self.frame, -1)
    
    # setting contrast and brightness of frame
    def frame_contrast_brightness_check(self):
        self.contrast = self.contrast_scrollbar.value() / 100
        self.brightness = self.brightness_scrollbar.value()
        self.contrast_label.setText('對比(' + str(self.contrast) + '):')
        self.brightness_label.setText('亮度(' + str(self.brightness) + '):')

    # frame lightness check and update lightness state
    def lightness_check(self):
        if self.average_gray_value > self.Recognition.MAX_AVERAGE_GRAY_VALUE:
            self.warning_label.setStyleSheet("color:red")
            self.warning_label.setText('光線狀態:光線過亮')
        elif self.average_gray_value < self.Recognition.MIN_AVERAGE_GRAY_VALUE:
            self.warning_label.setStyleSheet("color:red")
            self.warning_label.setText('光線狀態:光線過暗')
        else:
            self.warning_label.setStyleSheet("color:blue")
            self.warning_label.setText('光線狀態:正常!')
        
    # insert recognition text to result box
    def text_to_result_box(self):
        self.result_box.setText(self.Recognition.text)

    def refresh(self):
        self.frame_check()
        self.lightness_check()

        # PyQt image format
        converted_frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
        height, width = converted_frame.shape[:2]
        pyqt_img = QImage(converted_frame, width, height, QImage.Format_RGB888)
        pyqt_img = QPixmap.fromImage(pyqt_img)
        self.camera_label.setPixmap(pyqt_img)
        self.camera_label.setScaledContents(True)

        # Show now state
        self.state_label.setText('現在狀態:' + str(self.Recognition.now_state))

        # Finish recognition
        if self.Recognition.now_state == STATE.FinishRecognition:
            if self.FinishFlag == False:
                self.FinishFlag = True
                print('Recognition text : ', self.Recognition.text)
                cv2.imshow('Cropped Frame', self.Recognition.crop_img)
                text_to_speech.TextToSpeech(self.Recognition.text)
                self.result_box.setText(self.Recognition.text)
        else:
            self.FinishFlag = False


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    win.Recognition.run_program()
    sys.exit(app.exec_())