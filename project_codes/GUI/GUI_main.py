from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from .Ui_GUI import *
from . import languages

from image_recognition.recognition_program import *
from image_recognition import text_to_speech
from word_transtale import selector_TranslateOrWord
from googletrans import Translator

import cv2
import sys
import numpy
import pymysql

# Database setting
DB_IP = '172.105.205.179'
DB_USER = 'root'
DB_PASSWORD = 'mitlab123456'
DB_PORT = 3306
DB_DATABASE = 'WordDB'


# 建立類別來繼承 Ui_SmartLearningSystemGUI 介面程式
class MainWindow(QtWidgets.QMainWindow, Ui_SmartLearningSystemGUI):
    def __init__(self, parent=None):
        # 繼承Ui_Gui.py
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle('Smart Learning System v1.0')
        self.setWindowIcon(QtGui.QIcon('project_codes/GUI/GUI_icon.png'))
        self.connectToDB()

        # Recognition program
        self.Recognition = RecognitionProgram()
        self.frame = self.Recognition.output_img
        self.contrast, self.brightness = 1, 0
        self.translate_mode = 0  # 0 = sentence mode , 1 = vocabulary mode

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
        self.result_box.textChanged.connect(self.google_translate)
        self.translated_box.setReadOnly(True)

        # Button trigger setting
        self.confirm_btn.clicked.connect(self.add_btn_click)
        self.clear_btn.clicked.connect(self.clear_btn_click)
        self.exit_btn.clicked.connect(sys.exit)

        # translate trigger setting
        self.sentenceMode_btn.clicked.connect(self.translated_mode_changed)
        self.vocabularyMode_btn.clicked.connect(self.translated_mode_changed)

        # Combobox trigger setting
        self.camera_selector.currentTextChanged.connect(
            self.camera_selector_changed)
        self.language_selector.currentTextChanged.connect(
            self.languages_selector_changed)

        # Scorllbar trigger setting
        self.brightness_scrollbar.valueChanged.connect(
            self.frame_contrast_brightness_check)
        self.contrast_scrollbar.valueChanged.connect(
            self.frame_contrast_brightness_check)


    # confirm to add word to database
    def add_btn_click(self):
        self.insertSentenceToDB()

    # clear all box
    def clear_btn_click(self):
        self.result_box.clear()
        self.translated_box.clear()

    def translated_mode_changed(self):
        result = selector_TranslateOrWord.selector_TranslateOrWord(self.result_box.toPlainText())
        print('result:',result)
        if self.sentenceMode_btn.isChecked():
            self.translate_mode = 0
        elif self.vocabularyMode_btn.isChecked():
            self.translate_mode = 1

    # translate english text to translated language(too many request the translate function will be disable)
    def google_translate(self):
        self.triggerCount = self.triggerCount + 1
        if self.triggerCount >= 3 or self.FinishFlag == True:
            self.triggerCount = 0
            text = self.result_box.toPlainText()
            self.translated_box.clear()
            try:
                if text == "":
                    result = ""
                else:
                    print('googletrans triggered')
                    result = self.translator.translate(
                        text, dest=self.lang, timeout=3).text
                self.translated_box.setText(result)
            except:
                pass

    # change camera to the choosen one
    def camera_selector_changed(self):
        index = self.camera_selector.currentIndex()
        self.Recognition.cap.release()
        if index == 0:
            self.Recognition.cap = cv2.VideoCapture(0)
        else:
            self.Recognition.cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)

    # change to the translated langauge
    def languages_selector_changed(self):
        index = self.language_selector.currentIndex()
        self.lang = self.languages_key_array[index]
        self.google_translate()

    # GUI camera frame check
    def frame_check(self):
        self.frame = cv2.convertScaleAbs(
            self.Recognition.output_img, alpha=self.contrast, beta=self.brightness)
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
        self.average_gray_value = np.mean(self.frame)
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


# ----------------------------------------------------------------------------------------------------------

    # Connect to Mysql database
    def connectToDB(self):
        try:
            self.db = pymysql.connect(
                host=DB_IP, port=DB_PORT, user=DB_USER, password=DB_PASSWORD, database=DB_DATABASE)
            print('Connect to database success!')
        except:
            print('Conncet to database failed!')


    # Insert data to Mysql database
    def insertSentenceToDB(self):
        try :
            cursor = self.db.cursor()
            data = self.result_box.toPlainText(), self.translated_box.toPlainText()
            mysql = "INSERT  INTO  SentenceTable (sentence,translation) VALUE ('%s','%s')" % data
            cursor.execute(mysql)
            self.db.commit()
            print('Insert data to database success!\n')
        except:
            print('Insert data to database failed')
