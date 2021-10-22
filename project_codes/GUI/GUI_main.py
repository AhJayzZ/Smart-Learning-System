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

        # FinishFlag setting(Avoid duplicated translation)
        self.FinishFlag = False

        # Constrast and brightness scrollbar default setting
        self.brightness_scrollbar.setValue(0)
        self.brightness_scrollbar.setMinimum(-100)
        self.brightness_scrollbar.setMaximum(100)
        self.contrast_scrollbar.setValue(100)
        self.contrast_scrollbar.setMinimum(0)
        self.contrast_scrollbar.setMaximum(300)

        # Camera default setting
        camera_array = ['Camera 0(Webcam)', 'Camera 1(External Camera)']
        self.camera_selector.addItems(camera_array)

        # Language default setting(index 15 means Chinese Traditional)
        self.languages_key_array, self.languages_value_array = languages.langauge_data()
        self.language_selector.addItems(self.languages_value_array)
        self.language_selector.setCurrentIndex(15)
        self.lang = 'zh-tw'
        
        # Timer default setting
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh)
        self.timer.start(10)

        # result & translate box default setting
        self.translate_box.setReadOnly(True)

        # Button trigger default setting
        self.add_btn.clicked.connect(self.add_btn_click)
        self.translate_btn.clicked.connect(self.translate)
        self.clear_btn.clicked.connect(self.clear_btn_click)
        self.exit_btn.clicked.connect(sys.exit)

        # Combobox trigger default setting
        self.camera_selector.currentTextChanged.connect(
            self.camera_selector_changed)
        self.language_selector.currentTextChanged.connect(
            self.languages_selector_changed)

        # Scorllbar trigger default setting
        self.brightness_scrollbar.valueChanged.connect(
            self.frame_contrast_brightness_check)
        self.contrast_scrollbar.valueChanged.connect(
            self.frame_contrast_brightness_check)

    
    def add_btn_click(self):
        """
        # add word or sentence to database
        """
        self.insertDataToDB()

    def clear_btn_click(self):
        """
        clear all box
        """
        self.result_box.clear()
        self.translate_box.clear()


    def translate(self):
        """
        translate function, wordOrSentence = 0(Sentence),1(Word)
        if wordOrSentence = 0,use googletrans,
        if wordOrSentence = 1,use webscraper to catch data from website
        """
        input_text = self.result_box.toPlainText()
        if input_text == "":
            pass
        else:
            sentenceOrWord = selector_TranslateOrWord.check_if_one_word(input_text)
            output_translation = selector_TranslateOrWord.selector_TranslateOrWord(input_text,src='en',dest=self.lang)
            text_to_speech.TextToSpeech(input_text)
            if sentenceOrWord == 0:
                print('sentence')
                self.translate_box.setText(output_translation)
            else :
                print('word')
                output_format = '定義:\n' + output_translation['defination'] + '\n\n' + \
                                '音標:\n' + output_translation['eng_pr'] + ',' + output_translation['ame_pr'] + '\n\n' + \
                                '時態:\n' + output_translation['tenses']
                try:
                    self.translate_box.setText(output_format)
                except:
                    self.translate_box.setText(output_translation['defination'])
            
    def camera_selector_changed(self):
        """
        change camera to the choosen one
        """
        index = self.camera_selector.currentIndex()
        self.Recognition.cap.release()
        if index == 0:
            self.Recognition.cap = cv2.VideoCapture(0)
        else:
            self.Recognition.cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)

    
    def languages_selector_changed(self):
        """
        change to the new translate langauge and update the translation
        """
        index = self.language_selector.currentIndex()
        self.lang = self.languages_key_array[index]
        self.translate()

    # GUI camera frame check
    def frame_check(self):
        """
        change GUI frame  if frame flip or frame be lighten
        """
        self.frame = cv2.convertScaleAbs(
            self.Recognition.output_img, alpha=self.contrast, beta=self.brightness)
        if self.frameHorizontal_btn.isChecked():
            self.frame = cv2.flip(self.frame, 1)
        elif self.frameVertical_btn.isChecked():
            self.frame = cv2.flip(self.frame, 0)
        elif self.frameInverse_btn.isChecked():
            self.frame = cv2.flip(self.frame, -1)

    def frame_contrast_brightness_check(self):
        """
        update frame brightness, frame contrast and setting labelshow 
        """
        self.contrast = self.contrast_scrollbar.value() / 100
        self.brightness = self.brightness_scrollbar.value()
        self.contrast_label.setText('對比(' + str(self.contrast) + '):')
        self.brightness_label.setText('亮度(' + str(self.brightness) + '):')

    def lightness_check(self):
        """
        check and update frame brightness status
        """
        self.average_gray_value = numpy.mean(self.frame)
        if self.average_gray_value > self.Recognition.MAX_AVERAGE_GRAY_VALUE:
            self.warning_label.setStyleSheet("color:red")
            self.warning_label.setText('光線狀態:光線過亮')
        elif self.average_gray_value < self.Recognition.MIN_AVERAGE_GRAY_VALUE:
            self.warning_label.setStyleSheet("color:red")
            self.warning_label.setText('光線狀態:光線過暗')
        else:
            self.warning_label.setStyleSheet("color:blue")
            self.warning_label.setText('光線狀態:正常!')

    def refresh(self):
        """
        refresh every 10ms trigger by clock
        """
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
                self.result_box.setText(self.Recognition.text)
                self.translate()
                cv2.imshow('Cropped Frame', self.Recognition.crop_img)
        else:
            self.FinishFlag = False

# ----------------------------------------------------------------------------------------------------------

    def connectToDB(self):
        """
        Connect to Mysql database
        """
        try:
            self.db = pymysql.connect(
                host=DB_IP, port=DB_PORT, user=DB_USER, password=DB_PASSWORD, database=DB_DATABASE)
            print('Connect to database success!')
        except:
            print('Conncet to database failed!')


    # Insert data to Mysql database
    def insertDataToDB(self):
        try :
            cursor = self.db.cursor()
            data = self.result_box.toPlainText(), self.translate_box.toPlainText()
            mysql = "INSERT  INTO  SentenceTable (sentence,translation) VALUE ('%s','%s')" % data
            cursor.execute(mysql)
            self.db.commit()
            print('Insert data to database success!')
        except:
            print('Insert data to database failed!')
