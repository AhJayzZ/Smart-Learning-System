from genericpath import isfile
from os import path
from re import S
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from .Ui_GUI import *
from . import languages

from image_recognition.recognition_program import *
from image_recognition import text_to_speech
from word_transtale import selector_TranslateOrWord

import numpy
import cv2
import sys,os
import pymysql
import time

# Database setting
DB_IP = '172.105.205.179'
DB_USER = 'root'
DB_PASSWORD = 'mitlab123456'
DB_PORT = 3306
DB_DATABASE = 'WordDB'

class MainWindow(QtWidgets.QMainWindow, Ui_SmartLearningSystemGUI):
    """
    建立類別來繼承 Ui_SmartLearningSystemGUI 介面程式
    """
    def __init__(self, parent=None):
        # 繼承Ui_Gui.py
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle('Smart Learning System v1.0')
        self.setWindowIcon(QIcon('./project_codes/GUI/images/GUI_icon.png'))
        self.sound_btn.setIcon(QIcon('./project_codes/GUI/images/sound_icon.png'))
        self.translate_btn.setIcon(QIcon('./project_codes/GUI/images/translate_icon.png'))
        self.connectDB_thread = connectDB_Thread()
        self.connectDB_thread.start()

        # Recognition program
        self.contrast,self.brightness=1,0
        self.average_gray_value = 0
        self.frameFlip = False
        self.Recognition = RecognitionProgram()
        self.frame_thread = frame_Thread(self.Recognition)
        self.frame_thread.frame_callback.connect(self.frame_refresh)
        self.frame_thread.start()
        

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
        self.translateTimer = QTimer(self)
        self.translateTimer.timeout.connect(self.translate)
        self.previousResult = ""

        # Result & translate box default setting
        self.result_box.textChanged.connect(self.translateTimeCount)
        self.translate_box.setReadOnly(True)

        # Button trigger default setting
        self.init_btn.clicked.connect(self.initialize)
        self.add_btn.clicked.connect(self.insertDataToDB)
        self.translate_btn.clicked.connect(self.translate)
        self.translate_btn.clicked.connect(self.playSound)
        self.sound_btn.clicked.connect(self.playSound)
        self.back_btn.clicked.connect(sys.exit) # Back to login page(unfinished)

        # RadioButtin trigger default setting
        self.frameDefault_btn.clicked.connect(self.frameMode_check)
        self.frameHorizontal_btn.clicked.connect(self.frameMode_check)
        self.frameVertical_btn.clicked.connect(self.frameMode_check)
        self.frameInverse_btn.clicked.connect(self.frameMode_check)

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

        # Menubar trigger default setting
        self.settingAction = QAction(parent=self,text='設定',triggered=self.settingAction_triggered)
        self.guideAction = QAction(parent=self,text='使用手冊',triggered=self.guideAction_triggered)
        self.openWordFileAction = QAction(parent=self,text='打開單字本',triggered=self.openWordFileAction_triggered)
        self.menubar.addAction(self.settingAction)
        self.menubar.addAction(self.guideAction)
        self.menubar.addAction(self.openWordFileAction)
        
        self.historyDict={}
        self.historyAction = []
        self.historyIndex = 0
        self.historyMenu = QMenu(parent=self,title='翻譯紀錄')
        self.menubar.addMenu(self.historyMenu)
        
    
# -----------------------------------------Window event--------------------------------------------
    def closeEvent(self,event):
        """
        PyQt window close event
        """
        reply = QMessageBox(icon=QMessageBox.Warning,
                            windowIcon=QIcon('./project_codes/GUI/images/exit_icon.png'),
                            windowTitle='離開程式',
                            text='是否離開本程式?',
                            standardButtons=(QMessageBox.Yes|QMessageBox.No)).exec_()

        if reply == QMessageBox.Yes:
            event.accept()
            sys.exit()
        else:
            event.ignore()
    
# -----------------------------------------Widgets function-----------------------------------------

    def initialize(self):
        """
        Initialize all setting configuration
        """
        self.frame_thread.Recognition.cap = cv2.VideoCapture(0)
        self.camera_selector.setCurrentIndex(0)
        self.result_box.clear()
        self.translate_box.clear()
        self.contrast , self.brightness = 1 , 0
        self.brightness_scrollbar.setValue(0)
        self.contrast_scrollbar.setValue(100)
        self.language_selector.setCurrentIndex(15)
        self.lang = 'zh-tw'
        self.frameDefault_btn.setChecked(True)

    def insertDataToDB(self):
        """
        Insert data to Mysql database
        """
        try :
            if self.sentenceOrWord == 0: # Sentence
                data = self.result_box.toPlainText(), self.translation_output
            else:                       # Word
                data = self.result_box.toPlainText(), self.translation_output['defination']
                
            cursor = self.connectDB_thread.db.cursor()
            mysql = "INSERT  INTO  SentenceTable (sentence,translation) VALUE ('%s','%s')" % data
            cursor.execute(mysql)
            self.connectDB_thread.db.commit()
            print('Insert data to database success!')
        except:
            print('Insert data to database failed!')

    def playSound(self):
        """
        play .mp3 file of result_box text
        """
        self.input_text = self.result_box.toPlainText()
        self.gTTS_thread = gTTS_Thread(self.input_text).start()
        self.gTTS_thread.start()

    def set_output_format(self):
        """
        setting output data format
        """
        self.sentenceOrWord = self.translation_thread.sentenceOrWord
        self.translation_output = self.translation_thread.translation_output

        if self.sentenceOrWord == 0: # Sentence
            self.translate_box.setText(self.translation_output)
        else :                       # Word
            try:
                output_format = '定義:\n' + self.translation_output['defination'] + '\n\n' + \
                                '音標:\n' + self.translation_output['eng_pr'] + ',' + self.translation_output['ame_pr'] + '\n\n' + \
                                '時態:\n' + self.translation_output['tenses']
                self.translate_box.setText(output_format)
            except:
                try :
                    self.translate_box.setText('定義:\n' + self.translation_output['defination'])
                except:
                    self.translate_box.setText('Find Nothing,please try again!') 
        self.addTranslateHistory() 
                    
    def translate(self):
        """
        translate function, wordOrSentence = 0(Sentence),1(Word)
        if wordOrSentence = 0,use googletrans,
        if wordOrSentence = 1,use webscraper to catch data from website
        """
        self.input_text = self.result_box.toPlainText()
        if self.input_text == "":
            self.result_box.clear()
            self.translate_box.clear()
        else:
            if self.previousResult != self.input_text:
                self.translation_thread = translation_Thread(self.input_text,self.lang)
                self.translation_thread.translation_finished.connect(self.set_output_format)
                self.translation_thread.start()
            
        self.previousResult = self.input_text

    def addTranslateHistory(self):
        """
        add the  action of translate history into menubar
        """
        print(self.historyIndex)
        self.translateTimer.stop()
        self.historyDict[self.input_text] = self.translate_box.toPlainText()
        if self.historyIndex < 10:
            self.historyAction.append(QAction(parent=self,text=self.input_text,triggered=self.historyAction_triggerred))
            self.historyMenu.addAction(self.historyAction[self.historyIndex])
        else:
            self.historyAction[self.historyIndex % 10].setText(self.input_text)
        self.historyIndex = self.historyIndex + 1
        
    def translateTimeCount(self):
        """
        triggered counting for translation function
        """
        self.translateTimer.start(3000)

    def camera_selector_changed(self):
        """
        change camera to the choosen one
        """
        index = self.camera_selector.currentIndex()
        self.frame_thread.Recognition.cap.release()
        if index == 0:
            self.frame_thread.Recognition.cap = cv2.VideoCapture(0)
        else:
            self.frame_thread.Recognition.cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
        self.frame_thread.start()

    def languages_selector_changed(self):
        """
        change to the new translate langauge and update the translation
        """
        index = self.language_selector.currentIndex()
        self.lang = self.languages_key_array[index]
        self.translate()

    # GUI camera frame check
    def frameMode_check(self):
        """
        change GUI frame  if frame flip or frame be lighten
        """
        self.frameFlip = True
        if self.frameHorizontal_btn.isChecked():
            self.frameMode = 1
        elif self.frameVertical_btn.isChecked():
            self.frameMode = 0
        elif self.frameInverse_btn.isChecked():
            self.frameMode = -1
        else:
            self.frameFlip = False

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
        self.average_gray_value = numpy.mean(self.frame_thread.frame)
        if self.average_gray_value > self.frame_thread.Recognition.MAX_AVERAGE_GRAY_VALUE:
            self.warning_label.setStyleSheet("color:red")
            self.warning_label.setText('光線狀態:光線過亮')
        elif self.average_gray_value < self.frame_thread.Recognition.MIN_AVERAGE_GRAY_VALUE:
            self.warning_label.setStyleSheet("color:red")
            self.warning_label.setText('光線狀態:光線過暗')
        else:
            self.warning_label.setStyleSheet("color:blue")
            self.warning_label.setText('光線狀態:正常!')

    def frame_refresh(self):
        """
        refresh frame and check frame flip and brightness
        """
        self.frame_thread.frame = cv2.convertScaleAbs(self.frame_thread.Recognition._input_img,alpha=self.contrast,beta=self.brightness)
        self.frame_thread.Recognition.output_img = self.frame_thread.frame

        # frame checking(flip,lightness)
        if self.frameFlip :
            self.frame_thread.frame = cv2.flip(self.frame_thread.frame, self.frameMode)

        self.lightness_check()

        # PyQt image format
        converted_frame = cv2.cvtColor(self.frame_thread.frame, cv2.COLOR_BGR2RGB)
        height, width = converted_frame.shape[:2]
        pyqt_img = QImage(converted_frame, width, height, QImage.Format_RGB888)
        pyqt_img = QPixmap.fromImage(pyqt_img)
        self.camera_label.setPixmap(pyqt_img)
        self.camera_label.setScaledContents(True)

        # Show now state
        self.state_label.setText('現在狀態:' + str(self.frame_thread.Recognition.now_state))

        # Finish recognition
        if self.frame_thread.Recognition.now_state == STATE.FinishRecognition:
            if self.FinishFlag == False:
                self.FinishFlag = True
                print('Recognition text : ', self.frame_thread.Recognition.text)
                self.result_box.setText(self.frame_thread.Recognition.text)
                self.translate()
                self.playSound()
                cv2.imshow('Cropped Frame', self.frame_thread.Recognition.crop_img)
        else:
            self.FinishFlag = False

# -----------------------------------------Menubar-----------------------------------------

    def settingAction_triggered(self):
        """
        settingAction triggered
        """
        print('settingAction_triggered')

    def guideAction_triggered(self):
        """
        open user guide message box
        """
        self.guideText = open(file='./project_codes/GUI/guide.txt',mode='r',encoding='utf-8')
        QMessageBox(icon=QMessageBox.Information,
                    windowIcon=QIcon('./project_codes/GUI/images/guide_icon.png'),
                    windowTitle='使用說明',
                    text=self.guideText.read()).exec()
        self.guideText.close()

    def historyAction_triggerred(self):
        """
        setting result_box and translate_box to translate history 
        """        
        actionText = self.sender().text()
        self.result_box.setText(actionText)
        self.translate_box.setText(self.historyDict[actionText])
    
    def openWordFileAction_triggered(self):
        """
        Open local word dictionary,if file not exist,create one
        """
        self.fileOpen_thread = localFileOpen_Thread()
        self.fileOpen_thread.start()

# -----------------------------------------Threading-----------------------------------------

class frame_Thread(QThread):
    """
    frame updating threading
    """
    frame_callback = pyqtSignal(int)
    def __init__(self,Recognition,parent=None):
        super().__init__(parent)
        self.Recognition = Recognition
        self.frame = self.Recognition._input_img

    def run(self):
        while self.Recognition.cap.isOpened():
            self.frame = self.Recognition._input_img
            self.frame_callback.emit(1)
            time.sleep(0.01)
            
class gTTS_Thread(QThread):
    """
    google Text To Speech threading
    """
    def __init__(self,input_text,parent=None):
        super().__init__(parent)
        self.input_text = input_text
        
    def run(self):
        text_to_speech.TextToSpeech(self.input_text)

class translation_Thread(QThread):
    """
    translate funtion threading
    """
    translation_finished = pyqtSignal(int)
    def __init__(self,input_text,translated_lang,parent=None):
        super().__init__(parent)
        self.input_text = input_text
        self.translated_lang = translated_lang
        self.sentenceOrWord ,self.translation_output = -1,""

    def run(self):
        self.sentenceOrWord = selector_TranslateOrWord.check_if_one_word(self.input_text)
        self.translation_output = selector_TranslateOrWord.selector_TranslateOrWord(self.input_text,src='en',dest=self.translated_lang)
        self.translation_finished.emit(1)


class connectDB_Thread(QThread):
    """
    connect to database threading
    """
    def __init__(self,parent=None):
        super().__init__(parent)
        self.currentPath = os.path.dirname(__file__)
        self.dirPath = os.path.split(self.currentPath)[0]    
        self.filePath = os.path.join(self.dirPath,'localDict.txt')

    def run(self):
        try:
            self.db = pymysql.connect(
                host=DB_IP, port=DB_PORT, user=DB_USER, password=DB_PASSWORD, database=DB_DATABASE)
            print('Connect to database success!')
        except:
            print('Conncet to database failed!')

    
class localFileOpen_Thread(QThread):
    """
    local word file open threading
    """
    def __init__(self,parent=None):
        super().__init__(parent)
        self.currentPath = os.path.dirname(__file__)
        self.dirPath = os.path.split(self.currentPath)[0]    
        self.filePath = os.path.join(self.dirPath,'localDict.txt')

    def run(self):
        if not os.path.exists(self.filePath):
            open(self.filePath,'w')
               
        try :
            os.system(self.filePath)
        except:
            print('Open file error!')

