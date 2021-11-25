from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

#from GUI_CSS import *
from .GUI_settingPage import *
from .Ui_GUI import *

from image_recognition.recognition_program import *
from image_recognition import text_to_speech
from word_transtale import selector_TranslateOrWord

import numpy
import cv2
import sys,os
import pymysql
import time

# Path Configuration
currentPath = os.path.dirname(__file__) # GUI
dirPath = os.path.split(currentPath)[0] # ../ => project_code
    
class MainWindow(QMainWindow, Ui_SmartLearningSystemGUI):
    """
    Ui_SmartLearningSystemGUI 
    """
    def __init__(self):
        # 繼承Ui_Gui.py
        super(MainWindow, self).__init__()
        self.settingPage = SettingWindow(mainWindow=self)
        #setupCSS.__init__(self) #still unfinished
        self.setupUi(self)
        self.setWindowTitle('Smart Learning System v1.0')
        self.setWindowIcon(QIcon('./project_codes/GUI/images/GUI_icon.png'))

        self.sound_btn.setIcon(QIcon('./project_codes/GUI/images/sound_icon.png'))
        self.translate_btn.setIcon(QIcon('./project_codes/GUI/images/translate_icon.png'))
        self.add_btn.setIcon(QIcon('./project_codes/GUI/images/add_icon.png'))
        self.back_btn.setIcon(QIcon('./project_codes/GUI/images/back_icon.png'))
        self.clear_btn.setIcon(QIcon('./project_codes/GUI/images/clear_icon.png')) 
        self.clear_btn.setFlat(True)

        self.connectDB_thread = connectDB_Thread()  
        self.connectDB_thread.start()

        # Recognition program
        self.FinishFlag = False
        self.Recognition = RecognitionProgram()
        self.frame_thread = frame_Thread(self.Recognition)
        self.frame_thread.frame_callback.connect(self.frame_refresh)
        self.frame_thread.start()
        
        # Translte timer default setting
        self.translateTimer = QTimer(self,timeout=self.translate)
        self.previousResult = ""
        self.previousLang = ""

        # Result and translate box default setting
        self.result_box.textChanged.connect(self.translateTimeCount)
        self.translate_box.setReadOnly(True)

        # Button clicked event default setting
        self.clear_btn.clicked.connect(self.clear)
        self.add_btn.clicked.connect(self.addToDictionary)
        self.translate_btn.clicked.connect(self.translate)
        self.translate_btn.clicked.connect(self.playSound)
        self.sound_btn.clicked.connect(self.playSound)
        self.back_btn.clicked.connect(sys.exit) # Back to login page(unfinished)

        # Menubar trigger default setting
        self.settingAction = QAction(parent=self,text='設定',triggered=self.settingAction_triggered)
        self.guideAction = QAction(parent=self,text='使用手冊',triggered=self.guideAction_triggered)
        self.openWordFileAction = QAction(parent=self,text='打開單字本',triggered=self.openWordFileAction_triggered)
        self.menubar.addAction(self.settingAction)
        self.menubar.addAction(self.guideAction)
        self.menubar.addAction(self.openWordFileAction)
        
        # Translate history default setting
        self.historyDict={}
        self.historyAction = []
        self.historyIndex,self.historyIndexMaximum = 0, 10
        self.historyMenu = QMenu(parent=self,title='翻譯紀錄')
        self.menubar.addMenu(self.historyMenu)

        # CSS Style default setting
        button_style = "QPushButton {background-color:#FFB01F;border-radius:20px;}\
                        QPushButton:pressed{background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1 ,stop: 0 #BDD5EA, stop: 1 #F7F7FF)}"
        textbox_style = "border-image:url(./project_codes/GUI/images/textbox.jpg) 0 0 0 0 stretch stretch;"
        self.setStyleSheet("background-color:#4D9358")
        self.add_btn.setStyleSheet(button_style)
        self.back_btn.setStyleSheet(button_style)
        self.translate_btn.setStyleSheet(button_style)
        self.sound_btn.setStyleSheet(button_style)
        self.translate_box.setStyleSheet(textbox_style)
        self.result_box.setStyleSheet(textbox_style)
        
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

    def clear(self):
        """
        clear result and translate box
        """
        self.translate_box.clear()
        self.result_box.clear()

    def addToDictionary(self):
        """
        add translate data to localDictionary
        """
        currentPath = os.path.dirname(__file__)
        dirPath = os.path.split(currentPath)[0]    
        filePath = os.path.join(dirPath,'localDictionary.txt')
        if not os.path.exists(filePath):
            open(filePath,'w',encoding='utf-8')
        try:
            with open(filePath,'a',encoding='utf-8') as file:   
                if self.sentenceOrWord == 0:
                    lines = [self.input_text,',',self.translation_output,'\n']
                else :
                    lines = [self.input_text,',',self.translation_output['defination'],'\n']
                file.writelines(lines)
                file.close()
        except:
            print('add to localDictionary failed')

    # def insertDataToDB(self):
    #     """
    #     Insert data to Mysql database
    #     """
    #     try :
    #         if self.sentenceOrWord == 0: # Sentence
    #             data = self.result_box.toPlainText(), self.translation_output
    #         else:                       # Word
    #             data = self.result_box.toPlainText(), self.translation_output['defination']
                
    #         cursor = self.connectDB_thread.db.cursor()
    #         mysql = "INSERT  INTO  SentenceTable (sentence,translation) VALUE ('%s','%s')" % data
    #         cursor.execute(mysql)
    #         self.connectDB_thread.db.commit()
    #         print('Insert data to database success!')
    #     except:
    #         print('Insert data to database failed!')

    def playSound(self):
        """
        play .mp3 file of result_box text
        """
        self.input_text = self.result_box.toPlainText()
        self.gTTS_thread = gTTS_Thread(self.input_text)
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
            if self.previousResult != self.input_text or self.previousLang != self.settingPage.lang:
                self.translation_thread = translation_Thread(self.input_text,self.settingPage.lang)
                self.translation_thread.translation_finished.connect(self.set_output_format)
                self.translation_thread.start()

                # Avoid translate history preemption
                self.translate_btn.setEnabled(False)
                self.add_btn.setEnabled(False)
        self.previousLang = self.settingPage.lang
        self.previousResult = self.input_text

    def addTranslateHistory(self):
        """
        add the  action of translate history into menubar
        """
        self.translateTimer.stop()
        self.historyDict[self.input_text] = self.translate_box.toPlainText()
        if self.historyIndex < self.historyIndexMaximum:
            self.historyAction.append(QAction(parent=self,text=self.input_text,triggered=self.historyAction_triggerred))
            self.historyMenu.addAction(self.historyAction[self.historyIndex])
        else:
            self.historyAction[self.historyIndex % self.historyIndexMaximum].setText(self.input_text)
        self.historyIndex = self.historyIndex + 1
        # Avoid translate history preemption 
        self.translate_btn.setEnabled(True)
        self.add_btn.setEnabled(True)

    def translateTimeCount(self):
        """
        triggered counting for translation function
        """
        self.translateTimer.start(3000)

    def lightness_check(self):
        """
        check and update frame brightness status
        """
        self.average_gray_value = numpy.mean(self.frame_thread.frame)
        if self.average_gray_value > self.frame_thread.Recognition.MAX_AVERAGE_GRAY_VALUE:
            self.warning_label.setStyleSheet("color:red")
            self.warning_label.setText('光線狀態:過亮')
        elif self.average_gray_value < self.frame_thread.Recognition.MIN_AVERAGE_GRAY_VALUE:
            self.warning_label.setStyleSheet("color:red")
            self.warning_label.setText('光線狀態:過暗')
        else:
            self.warning_label.setStyleSheet("color:blue")
            self.warning_label.setText('光線狀態:正常!')

    def frame_refresh(self):
        """
        refresh frame and check frame flip and brightness
        """
        self.frame_thread.frame = cv2.convertScaleAbs(src=self.frame_thread.Recognition._input_img,
                                                        alpha=self.settingPage.contrast,
                                                        beta=self.settingPage.brightness)

        self.frame_thread.Recognition.output_img = cv2.flip(self.frame_thread.frame,1)

        # frame checking(flip,lightness)
        if self.settingPage.frameFlip:
            self.frame_thread.frame = cv2.flip(src=self.frame_thread.frame, flipCode=self.settingPage.frameMode)
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
                self.result_box.setText(self.frame_thread.Recognition.text)
                self.translate()
                self.playSound()
                print('Recognition text : ', self.frame_thread.Recognition.text)
                cv2.imshow('Cropped Frame', self.frame_thread.Recognition.crop_img)
        else:
            self.FinishFlag = False

# -----------------------------------------Menubar-----------------------------------------

    def settingAction_triggered(self):
        """
        open setting page 
        """
        self.settingPage.show()

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
        set result_box and translate_box to translate history record
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
        self.filePath = os.path.join(dirPath,'localDictionary.txt')

    def run(self):
        if not os.path.exists(self.filePath):
            open(self.filePath,'w',encoding='utf-8')
               
        try :
            os.system(self.filePath)
        except:
            print('Open file error!')