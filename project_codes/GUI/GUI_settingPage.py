from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from .Ui_settingPage import *
from . import languages
import cv2
import pymysql
import json
import os


# Path Configuration
currentPath = os.path.dirname(__file__) # GUI
dirPath = os.path.split(currentPath)[0] # ../ => project_code

ENV_FILE = './.env'
CONNECTION_TIMEOUT = 100

class SettingPage(QDialog,Ui_settingPage):
    """
    Ui_settingPage
    """
    def __init__(self,mainWindow,userID,userPassword):
        super(SettingPage,self).__init__()
        self.setupUi(self)
        self.mainWindow = mainWindow
        self.userID = userID
        self.userPassword = userPassword
        print('userID:'+self.userID+'\n'+'userPassword:'+self.userPassword)
        self.setWindowTitle("Setting")
        self.setFixedSize(self.size())
        self.setWindowIcon(QIcon("./project_codes/GUI/images/setting_icon.png"))

        # Button default setting
        self.init_btn.clicked.connect(self.initialize)
        self.init_btn.setIcon(QIcon('./project_codes/GUI/images/init_icon.png'))
        self.syncDB_btn.clicked.connect(lambda:self.syncronize(0))
        self.syncDB_btn.setIcon(QIcon('./project_codes/GUI/images/upstream_icon.png'))
        self.syncLocal_btn.clicked.connect(lambda:self.syncronize(1))
        self.syncLocal_btn.setIcon(QIcon('./project_codes/GUI/images/downstream_icon.png'))

        # Frame default setting
        self.cap = cv2.VideoCapture(0)
        self.contrast,self.brightness=1,0
        self.frameFlip = False
        self.frameMode = 0

        # Camera default setting
        camera_array = ['Camera 0(Webcam)', 'Camera 1(External Camera)']
        self.camera_selector.addItems(camera_array)

        # Language default setting(index 15 means Chinese Traditional(zh-tw))
        self.languages_key_array, self.languages_value_array = languages.langaugeData()
        self.language_selector.addItems(self.languages_value_array)
        self.language_selector.setCurrentIndex(15)
        self.lang = 'zh-tw'

        # Constrast and brightness scrollbar default setting
        self.brightness_scrollbar.setValue(0)
        self.brightness_scrollbar.setMinimum(-100)
        self.brightness_scrollbar.setMaximum(100)
        self.contrast_scrollbar.setValue(100)
        self.contrast_scrollbar.setMinimum(0)
        self.contrast_scrollbar.setMaximum(300)

        # RadioButtin clicked event default setting
        self.frameDefault_btn.clicked.connect(self.updateFrameMode)
        self.frameHorizontal_btn.clicked.connect(self.updateFrameMode)
        self.frameVertical_btn.clicked.connect(self.updateFrameMode)
        self.frameInverse_btn.clicked.connect(self.updateFrameMode)

        # Scorllbar scroll event default setting
        self.brightness_scrollbar.valueChanged.connect(
            self.updateContrastAndBrightness)
        self.contrast_scrollbar.valueChanged.connect(
            self.updateContrastAndBrightness)

        # Combobox clicked event default setting
        self.camera_selector.currentTextChanged.connect(
            self.updateCamera)
        self.language_selector.currentTextChanged.connect(
            self.updateLanguage)

    def initialize(self):
        """
        Initialize all setting configuration
        """
        self.mainWindow.connectionLabel.setText("Connection:Initializing")
        self.mainWindow.connectionLabel.setStyleSheet('color:black')
        self.mainWindow.translate_btn.setEnabled(True)
        self.mainWindow.result_box.clear()
        self.mainWindow.translate_box.clear()
        self.mainWindow.historyMenu.clear()
        self.mainWindow.historyAction.clear()
        self.mainWindow.historyDict.clear()
        self.mainWindow.historyIndex = 0
        self.frameFlip = False
        self.contrast , self.brightness = 1 , 0
        self.camera_selector.setCurrentIndex(0)
        self.language_selector.setCurrentIndex(15)
        self.lang = 'zh-tw'
        self.brightness_scrollbar.setValue(0)
        self.contrast_scrollbar.setValue(100)
        self.frameDefault_btn.setChecked(True)

    def updateFrameMode(self):
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

    def updateCamera(self):
        """
        change camera to the choosen one
        """
        index = self.camera_selector.currentIndex()
        self.mainWindow.frame_thread.Recognition.cap.release()
        if index == 0:
            self.mainWindow.frame_thread.Recognition.cap = cv2.VideoCapture(0)
        else:
            self.mainWindow.frame_thread.Recognition.cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
        self.mainWindow.frame_thread.start()

    def updateLanguage(self):
        """
        change to the new translate langauge and update the translation
        """
        index = self.language_selector.currentIndex()
        self.lang = self.languages_key_array[index]
        self.mainWindow.translate()

    def updateContrastAndBrightness(self):
        """
        update frame brightness, frame contrast and setting labelshow 
        """
        self.contrast = float(self.contrast_scrollbar.value() / 100)
        self.brightness = self.brightness_scrollbar.value()
        self.contrast_label.setText('對比(' + str(self.contrast) + '):')
        self.brightness_label.setText('亮度(' + str(self.brightness) + '):')

    def syncronize(self,syncMode):
        # syncMode = 0 (pull database data to local)
        # syncMode = 1 (push local data to database)
        databaseFile = open(file=ENV_FILE,mode='r')
        databaseData = json.loads(databaseFile.read())
        self.syncDB_thread = sync_Thread(databaseData,self.userID,syncMode)
        self.syncDB_thread.start()
    

class sync_Thread(QThread):
    """
    syncronize thread
    """
    def __init__(self,loginData,userID,syncMode):
        super().__init__()
        self.loginData = loginData
        self.userID = userID
        self.syncMode = syncMode
        self.localFile = os.path.join(dirPath,'localDictionary.txt')

    def run(self):
        self.connectToDB()
        if self.syncMode:
            # Push
            print('Push')
            localData = self.getWordFromLocal()
            self.writeDataToDB(localData)
        else:
            # pull
            print('Pull')
            databaseData = self.getWordFromDB()
            self.writeDataToLocal(databaseData)

    def connectToDB(self):
        """
        connect to database
        """
        try:
            self.db = pymysql.connect(host=self.loginData['DB_HOST'],
                                        port=self.loginData['DB_PORT'],
                                        user=self.loginData['DB_USER'],
                                        password=self.loginData['DB_PASSWORD'],
                                        database=self.loginData['DB_DATABASE'],
                                        connect_timeout=CONNECTION_TIMEOUT)
            self.cursor = self.db.cursor()
        except:
            print('conncect to daatabase failed')
            self.exit()

    def getWordFromDB(self):
        """
        get words form database
        """
        userWord = []
        sql = "SELECT user_word FROM User_Word WHERE user_id = '{}';".format(self.userID)
        self.cursor.execute(sql)
        sqlData = self.cursor.fetchall()
        for word in sqlData:
            userWord.append(word[0])
        return sorted(userWord)

    def getWordFromLocal(self):
        """
        get words from local file
        """
        localWord = []
        with open(file=self.localFile,mode='r') as file:
            jsonData = json.loads(file.read()) # Output should be a list
            file.close()
        for index in range(len(jsonData)):
            localWord.append(jsonData[index]['word'])
        return sorted(localWord)
            
    def writeDataToLocal(self,databaseData):
        """
        write database data to local file
        """
        fileData = open(file=self.localFile,mode='r').read()
        fileDataJSON = json.loads(fileData)
        with open(file=self.localFile,mode='r+') as file:
            # Step 1. Delete all word in local
            for _ in range(len(fileDataJSON)):
                del fileDataJSON[0]

            # Step 2. Add database data to local
            for word in databaseData:
                wordDict = {"word":word}
                fileDataJSON.append(wordDict)
            json.dump(fileDataJSON,file,ensure_ascii=False)

    def writeDataToDB(self,localData):
        """
        Write local data to database
        """
        # Step 1. Delete all word of user_id
        sql = "DELETE FROM User_Word WHERE user_id = '{}';".format(self.userID)
        self.cursor.execute(sql)

        # Step 2. Insert all word of local
        for word in localData:
            sql = "INSERT INTO User_Word (user_id,user_word) VALUES ('{}','{}');".format(self.userID,word)
            print(sql)
            self.cursor.execute(sql)
        self.db.commit()
