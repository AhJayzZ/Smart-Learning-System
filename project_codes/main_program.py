import re
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from GUI.Ui_GUI import *
from image_recognition.recognition_program import *

from googletrans import Translator
from GUI.languages import langauge_data
import cv2
import sys


# 建立類別來繼承 Ui_SmartLearningSystemGUI 介面程式
class MainWindow(QtWidgets.QMainWindow, Ui_SmartLearningSystemGUI):
    def __init__(self, parent=None):
        # 繼承Ui_Gui.py
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle('Hand Recognition')
        self.setWindowIcon(QtGui.QIcon('project_codes/GUI/GUI_icon.png'))
        
        # Recognition program
        self.Recognition = RecognitionProgram()
        
        # Finish Flag setting(Avoid duplicated operation)
        self.FinishFlag = False
        
        # Camera setting
        camera_array = ['Camera 0(Webcam)', 'Camera 1(External Camera)']
        self.camera_selector.addItems(camera_array)

        # Language setting(index 15 means Chinese Traditional)
        self.lang = 'zh-tw'
        self.languages_key_array,self.languages_value_array = langauge_data()
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

    # add clear the box and set the box that revise_textbox typed
    def add_btn_click(self):
        self.result_box.setText(self.revise_textbox.text())
        self.revise_textbox.clear()
        
    # clear all box
    def clear_btn_click(self):
        self.result_box.clear()
        self.translated_box.clear()
        self.revise_textbox.clear()

    # translate english text to translated language(too many request the translate function will disable)
    def translate(self):
        translator = Translator()
        text = self.result_box.toPlainText()
        try :
            result = translator.translate(text,dest=self.lang).text
            self.translated_box.setText(result)
        except :
            self.result_box.clear()
            self.translated_box.clear()

    # change camera to the choosen one 
    def camera_selector_changed(self):
        index = self.camera_selector.currentIndex()
        if index == 0 :
            self.Recognition.cap = cv2.VideoCapture(0)
        else :
            self.Recognition.cap = cv2.VideoCapture(index,cv2.CAP_DSHOW)       

    # change to the translated langauge
    def languages_selector_changed(self):
        index = self.language_selector.currentIndex()
        self.lang = self.languages_key_array[index]
        self.translate()

    # flip the camera frame
    def frame_flip(self):
        print(self.frameDefault_btn.checked)

    # insert recognition text to result box
    def text_to_result_box(self):
        self.result_box.setText(self.Recognition.text)

    def refresh(self):
        frame = self.Recognition.output_img
        if self.frameHorizontal_btn.isChecked() :
            frame = cv2.flip(frame,1)
        elif self.frameVertical_btn.isChecked() :
            frame = cv2.flip(frame,0)
        elif self.frameInverse_btn.isChecked() :
            frame = cv2.flip(frame,-1)

        converted_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # PyQt image format
        height, width = converted_frame.shape[:2]
        pyqt_img = QImage(converted_frame, width, height, QImage.Format_RGB888)
        pyqt_img = QPixmap.fromImage(pyqt_img)

        # Camera label changed to video frame
        self.camera_label.setPixmap(pyqt_img)
        self.camera_label.setScaledContents(True)

        # Show now state
        self.state_label.setText('現在狀態:' + str(self.Recognition.now_state))

        # Finish recognition and add text to result list
        if self.Recognition.now_state == STATE.FinishRecognition :
            if self.FinishFlag == False:
                self.FinishFlag = True
                print('Recognition text : ',self.Recognition.text)
                self.result_box.setText(self.Recognition.text)
        else :
            self.FinishFlag = False

        # Lightness warning 
        if self.Recognition.state_lightness == STATE_LIGHTNESS.TooBright:
            self.warning_label.setStyleSheet("color:red")
            self.warning_label.setText('光線狀態:光線過亮')
        elif self.Recognition.state_lightness == STATE_LIGHTNESS.TooDim:
            self.warning_label.setStyleSheet("color:red")
            self.warning_label.setText('光線狀態:光線過暗') 
        else:
            self.warning_label.setStyleSheet("color:blue")
            self.warning_label.setText('光線狀態:正常!')

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    win.Recognition.run_program()
    sys.exit(app.exec_())
