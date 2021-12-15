from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from .GUI_settingPage import SettingPage
from .Ui_mainPage import *

from image_recognition.recognition_program import *
from image_recognition import text_to_speech
from word_transtale import selector_TranslateOrWord

import requests
import numpy
import cv2
import sys
import os
import time
import json


# Path Configuration
currentPath = os.path.dirname(__file__)  # GUI
dirPath = os.path.split(currentPath)[0]  # ../ => project_code
localFile = os.path.join(dirPath,"localDictionary.txt")
guideFile = os.path.join(currentPath,'guide.txt')

class MainWindow(QMainWindow, Ui_SmartLearningSystemGUI):
    """
    Ui_SmartLearningSystemGUI 
    """
    def __init__(self, loginPage):
        # 繼承Ui_Gui.py
        super(MainWindow, self).__init__()
        self.loginPage = loginPage
        self.userID = self.loginPage.userID
        self.userPassword = self.loginPage.userPassword
        self.settingPage = SettingPage(mainWindow=self,
                                       userID=self.userID,
                                       userPassword=self.userPassword)
        self.setupUi(self)
        self.setWindowTitle('Smart Learning System')
        self.setFixedSize(self.size())
        self.setWindowIcon(QIcon('./project_codes/GUI/images/GUI_icon.png'))
        self.expand_btn.setIcon(QIcon('./project_codes/GUI/images/rightexpand_icon.png'))
        self.sound_btn.setIcon(QIcon('./project_codes/GUI/images/sound_icon.png'))
        self.translate_btn.setIcon(QIcon('./project_codes/GUI/images/translate_icon.png'))
        self.add_btn.setIcon(QIcon('./project_codes/GUI/images/add_icon.png'))
        self.back_btn.setIcon(QIcon('./project_codes/GUI/images/back_icon.png'))
        self.clear_btn.setIcon(QIcon('./project_codes/GUI/images/clear_icon.png'))
        self.removeWord_btn.setIcon(QIcon('./project_codes/GUI/images/remove_icon.png'))

        # Recognition program
        self.FinishFlag = False
        self.Recognition = RecognitionProgram()
        self.frame_thread = frame_Thread(self)
        self.frame_thread.frame_callback.connect(self.frameRefresh)
        self.frame_thread.start()

        # Timer default setting
        self.connectionCheck_thread = connectCheck_Thread(self)
        self.connectionTimer = QTimer(
            self, timeout=self.connectionCheck).start(1000)
        self.translateTimer = QTimer(self, timeout=self.translate)
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
        self.expand_btn.clicked.connect(self.expandPage)
        self.removeWord_btn.clicked.connect(self.wordRemove)
        self.back_btn.clicked.connect(self.backToLoginPage)

        # List widget default setting
        self.wordList.currentItemChanged.connect(self.wordListSelected)

        # Menubar trigger default setting
        self.settingAction = QAction(
            parent=self, text='設定', triggered=self.settingAction_triggered)
        self.guideAction = QAction(
            parent=self, text='使用手冊', triggered=self.guideAction_triggered)
        self.openWordFileAction = QAction(
            parent=self, text='打開單字本', triggered=self.openWordFileAction_triggered)
        self.menubar.addAction(self.settingAction)
        self.menubar.addAction(self.guideAction)
        self.menubar.addAction(self.openWordFileAction)

        # Translate history default setting
        self.historyDict = {}
        self.historyAction = []
        self.historyIndex, self.historyIndexMaximum = 0, 10
        self.historyMenu = QMenu(parent=self, title='翻譯紀錄')
        self.menubar.addMenu(self.historyMenu)

        # Widget style default setting
        self.expandFlag = False
        button_style = "QPushButton {background-color:#FFC43D;border-radius:20px;}\
                        QPushButton:pressed{background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1 ,stop: 0 #BDD5EA, stop: 1 #9CAEA9)}"
        textbox_style = "border-image:url(./project_codes/GUI/images/textbox.jpg) 0 0 0 0 stretch stretch;"
        self.setStyleSheet("background-color:#4D9358")
        self.wordList.setStyleSheet("background-color:white")
        self.add_btn.setStyleSheet(button_style)
        self.back_btn.setStyleSheet(button_style)
        self.translate_btn.setStyleSheet(button_style)
        self.sound_btn.setStyleSheet(button_style)
        self.clear_btn.setStyleSheet(button_style)
        self.expand_btn.setStyleSheet(button_style)
        self.removeWord_btn.setStyleSheet(button_style)
        self.translate_box.setStyleSheet(textbox_style)
        self.result_box.setStyleSheet(textbox_style)
        
        # Run program
        self.show()
        self.loadWordList()
        self.Recognition.run_program()

# -----------------------------------------Window event--------------------------------------------

    def closeEvent(self, event):
        """
        PyQt window close event
        """
        reply = QMessageBox(icon=QMessageBox.Warning,
                            windowIcon=QIcon(
                                './project_codes/GUI/images/exit_icon.png'),
                            windowTitle='離開程式',
                            text='是否離開本程式?',
                            standardButtons=(QMessageBox.Yes | QMessageBox.No)).exec_()

        if reply == QMessageBox.Yes:
            event.accept()
            sys.exit()
        else:
            event.ignore()

    def backToLoginPage(self):
        """
        back to login page
        """
        self.Recognition.cap.release()
        self.hide()
        self.loginPage.show()

# -----------------------------------------Functions-----------------------------------------

    def connectionCheck(self):
        """
        check network connection
        """
        self.connectionCheck_thread.start()

    def clear(self):
        """
        clear result and translate box
        """
        self.inputText = ""
        self.translate_box.clear()
        self.result_box.clear()
    
    def enableWidget(self):
        """
        avoid process preemption
        """
        if self.translation_thread.isFinished() and self.gTTS_thread.isFinished():
            self.sound_btn.setEnabled(True)
            self.translate_btn.setEnabled(True)
            self.add_btn.setEnabled(True)
            self.wordList.setEnabled(True)

    def addToDictionary(self):
        """
        add translate data to localDictionary
        """
        if not os.path.exists(localFile):
           with open(file=localFile, mode='w', encoding='utf-8') as file:
               file.write("[]")
        try:
            self.inputText = self.result_box.toPlainText()
            if self.inputText != "":
                with open(file=localFile,mode='r+',encoding='utf-8') as file:
                    fileContent = json.loads(file.read())
                    wordDuplicated = False
                    for index in range(len(fileContent)):
                        if self.inputText == fileContent[index]["word"]:
                            wordDuplicated = True
                            break
                    if not wordDuplicated:
                        file.seek(0)
                        self.wordList.addItem(self.inputText)
                        fileContent.append({"word": self.inputText})
                        json.dump(fileContent,file,ensure_ascii=False)
        except:
            QMessageBox(icon=QMessageBox.Critical,
                        windowIcon=self.style().standardIcon(QStyle.SP_MessageBoxCritical),
                        text='載入本地單字本失敗，請檢查檔案中的JSON的格式並修復',
                        windowTitle='檔案錯誤').exec()

    def playSound(self):
        """
        play .mp3 file of result_box text
        """
        self.inputText = self.result_box.toPlainText()
        self.gTTS_thread = gTTS_Thread(self.inputText)
        self.gTTS_thread.gTTS_finish.connect(self.enableWidget)
        self.gTTS_thread.start()

    def setOutputFormat(self):
        """
        setting output data format
        """
        self.sentenceOrWord = self.translation_thread.sentenceOrWord
        self.translationOutput = self.translation_thread.translation_output
        if self.sentenceOrWord == 0:  # Sentence
            self.translate_box.setText(self.translationOutput)
        else:                       # Word
            try: 
                outputFormat = '\n'.join(['【定義】\n' + str(self.translationOutput['defination']) + '\n' ,
                                        '【音標】\n' + str(self.translationOutput['eng_pr']) + '\n' + str(self.translationOutput['ame_pr']) + '\n ',
                                        '【時態】\n' + str(self.translationOutput['tenses']) + '\n',
                                        '【英文定義】\n' + str(self.translationOutput['def_eng'])])
                self.translate_box.setText(outputFormat)
            except:
                    self.translate_box.setText('Find nothing,please try again!')
        self.addTranslateHistory(self.inputText)

    def translate(self):
        """
        translate function, wordOrSentence = 0(Sentence),1(Word)
        if wordOrSentence = 0,use googletrans,
        if wordOrSentence = 1,use webscraper to catch data from website
        """
        self.inputText = self.result_box.toPlainText()
        if self.inputText == "":
            self.result_box.clear()
            self.translate_box.clear()
        else:
            if (self.previousResult != self.inputText) or (self.previousLang != self.settingPage.lang):
                self.translation_thread = translation_Thread(self.inputText, self.settingPage.lang)
                self.translation_thread.translation_finished.connect(self.setOutputFormat)
                self.translation_thread.translation_finished.connect(self.enableWidget)
                self.translation_thread.start()

                # Avoid process preemption
                self.sound_btn.setEnabled(False)
                self.translate_btn.setEnabled(False)
                self.add_btn.setEnabled(False)
                self.wordList.setEnabled(False)
        self.previousLang = self.settingPage.lang
        self.previousResult = self.inputText

    def addTranslateHistory(self,word):
        """
        add the  action of translate history into menubar
        """
        self.translateTimer.stop()
        self.historyDict[word] = self.translate_box.toPlainText()
        if self.historyIndex < self.historyIndexMaximum:
            self.historyAction.append(QAction(
                parent=self, text=word, triggered=self.historyAction_triggerred))
            self.historyMenu.addAction(self.historyAction[self.historyIndex])
        else:
            self.historyAction[self.historyIndex %
                               self.historyIndexMaximum].setText(word)
        self.historyIndex = self.historyIndex + 1

    def translateTimeCount(self):
        """
        triggered counting for translation function
        """
        self.translateTimer.start(3000)

    def lightnessCheck(self):
        """
        check and update frame brightness status
        """
        self.averageGrayValue = numpy.mean(self.frame_thread.Recognition.average_gray_value)
        if self.averageGrayValue > self.frame_thread.Recognition.MAX_AVERAGE_GRAY_VALUE:
            self.warning_label.setStyleSheet("color:red")
            self.warning_label.setText('光線:過亮')
        elif self.averageGrayValue < self.frame_thread.Recognition.MIN_AVERAGE_GRAY_VALUE:
            self.warning_label.setStyleSheet("color:red")
            self.warning_label.setText('光線:過暗')
        else:
            self.warning_label.setStyleSheet("color:black")
            self.warning_label.setText('光線:正常')

    def imageToPixmap(self,image):
        """
        convert frame to pyqt image format
        """
        convertedFrame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        height, width = convertedFrame.shape[:2]
        return QPixmap.fromImage(QImage(convertedFrame, width, height, QImage.Format_RGB888))

    def frameRefresh(self):
        """
        refresh frame and update state,also check lightness
        """
        # Lightness check
        self.lightnessCheck()

        # Frame update
        self.camera_label.setPixmap(self.imageToPixmap(self.frame_thread.frame))

        # Show state
        self.state_label.setText('辨識狀態:' + str(self.frame_thread.Recognition.now_state))
        
        # Finish recognition
        if self.frame_thread.Recognition.has_recognited_text():
            if self.FinishFlag == False:
                self.frame_thread.Recognition.ack_had_got_recognited_text()
                self.FinishFlag = True

                self.inputText = self.frame_thread.Recognition.text
                self.result_box.setText(self.inputText)
                self.translate()
                self.playSound()
        else:
            self.FinishFlag = False

# -----------------------------------------Word List--------------------------------------------
    def expandPage(self):
        """
        expand main page
        """
        EXPAND_SIZE = 320
        if self.expandFlag == False:
            self.expandFlag = True
            self.setFixedSize(self.width()+EXPAND_SIZE,self.height())
            self.expand_btn.setIcon(QIcon('./project_codes/GUI/images/leftexpand_icon.png'))
        else:
            self.expandFlag = False  
            self.setFixedSize(self.width()-EXPAND_SIZE,self.height())
            self.expand_btn.setIcon(QIcon('./project_codes/GUI/images/rightexpand_icon.png'))

    def loadWordList(self):
        """
        load local dictionary to wordlist
        """
        self.wordList.clear()
        with open(file=localFile,mode='r') as file:
            try:
                for word in json.loads(file.read()):
                    self.wordList.addItem(word["word"])
            except:
                print("load local file error")
                pass
    
    def wordRemove(self):
        """
        remove word from local dictionary and wordlist
        """
        wordSelected = self.wordList.currentItem()
        if not wordSelected: return
        else:
            itemIndex = self.wordList.row(wordSelected) 
            with open(file=localFile,mode='r',encoding='utf-8') as file:
                fileContent = json.load(file)
            with open(file=localFile,mode='w',encoding='utf-8') as file:
                if wordSelected.text() in fileContent[itemIndex].values():
                    self.wordList.takeItem(itemIndex)
                    del fileContent[itemIndex]
                    json.dump(fileContent,file,ensure_ascii=False) 

    def wordListSelected(self):
        """
        set word to result box when wordlist selection changed
        """
        if self.wordList.currentItem():
            self.result_box.setText(self.wordList.currentItem().text())
            self.translate()
            self.playSound()

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
        with open(file=guideFile, mode='r', encoding='utf-8') as file:
            QMessageBox(icon=QMessageBox.Information,
                        windowIcon=QIcon('./project_codes/GUI/images/guide_icon.png'),
                        windowTitle='使用說明',
                        text=file.read()).exec()

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

    def __init__(self, mainWindow):
        super().__init__()
        self.mainWindow = mainWindow
        self.Recognition = mainWindow.Recognition
        self.mainWindow.camera_label.setScaledContents(True)

    def run(self):
        while self.Recognition.cap.isOpened():
            self.frame = self.Recognition.output_img
            self.contrast = self.mainWindow.settingPage.contrast
            self.brightness = self.mainWindow.settingPage.brightness
            self.frameFlip = self.mainWindow.settingPage.frameFlip
            self.frameMode = self.mainWindow.settingPage.frameMode
            if self.frameFlip:
                self.frame = cv2.flip(src=self.frame, flipCode=self.frameMode)
            self.frame = cv2.convertScaleAbs(
                src=self.frame, alpha=self.contrast, beta=self.brightness)
            self.frame_callback.emit(1)
            time.sleep(0.01)


class gTTS_Thread(QThread):
    """
    google Text To Speech threading
    """
    gTTS_finish = pyqtSignal(int)

    def __init__(self, inputText):
        super().__init__()
        self.inputText = inputText

    def run(self):
        text_to_speech.TextToSpeech(self.inputText)
        self.gTTS_finish.emit(1)


class translation_Thread(QThread):
    """
    translate funtion threading
    """
    translation_finished = pyqtSignal(int)

    def __init__(self, inputText, translated_lang):
        super().__init__()
        self.inputText = inputText
        self.translated_lang = translated_lang
        self.sentenceOrWord, self.translation_output = -1, ""

    def run(self):
        self.sentenceOrWord = selector_TranslateOrWord.check_if_one_word(
            self.inputText)
        self.translation_output = selector_TranslateOrWord.selector_TranslateOrWord(
            self.inputText, src='en', dest=self.translated_lang)
        self.translation_finished.emit(1)


class localFileOpen_Thread(QThread):
    """
    local word file open threading
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.filePath = localFile

    def run(self):
        if not os.path.exists(self.filePath):
           with open(self.filePath, 'w', encoding='utf-8') as file:
               file.write("[]")

        try:
            os.system(self.filePath)
        except:
            QMessageBox(icon=QMessageBox.Critical,
                        text='open local dictionary file error',
                        windowTitle='File Error').exec()


class connectCheck_Thread(QThread):
    """
    connection check thread
    """
    def __init__(self, mainWindow):
        super().__init__(parent=None)
        self.url = 'http://www.google.com'
        self.mainWindow = mainWindow

    def run(self):
        try:
            requests.get(url=self.url, timeout=1)
            self.mainWindow.connectionLabel.setStyleSheet('color:blue')
            self.mainWindow.connectionLabel.setText('連線狀態: 成功')
        except:
            self.mainWindow.connectionLabel.setStyleSheet('color:red')
            self.mainWindow.connectionLabel.setText('連線狀態: 失敗')
