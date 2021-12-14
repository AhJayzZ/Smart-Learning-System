from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from .GUI_mainPage import MainWindow
from .Ui_loginPage import *
from datetime import date
from datetime import datetime
import sys,os
import json
import webbrowser
import pymysql

# Path Configuration
currentPath = os.path.dirname(__file__) # GUI
dirPath = os.path.split(currentPath)[0] # ../ => project_code
localFileName = "localDictionary.txt"

ENV_FILE = './.env'
CONNECTION_TIMEOUT = 10

class LoginPage(QDialog,Ui_loginPage):
    """
    Ui_LoginPage
    """
    def __init__(self):
        super(LoginPage,self).__init__()
        self.setupUi(self)
        self.show()
        self.setWindowTitle("Login")
        self.setFixedSize(self.size())
        self.setWindowIcon(QIcon("./project_codes/GUI/images/login_icon.png"))
        self.setStyleSheet("background-color:#4D9358")

        self.loginButton.clicked.connect(self.openMainPage)
        self.registerButton.clicked.connect(self.openRegisterWebsite)
        self.reviewWebsiteButton.clicked.connect(self.openReviewWebsite)
        self.exitButton.clicked.connect(sys.exit)

        # Style
        textboxStyle = "color:black;background-color:white;"
        buttonStyle = "QPushButton {background-color:#FFC43D;border-radius:20px;}\
                        QPushButton:pressed{background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1 ,stop: 0 #BDD5EA, stop: 1 #9CAEA9)}"
        self.accountTextbox.setStyleSheet(textboxStyle)
        self.passwordTextbox.setStyleSheet(textboxStyle)
        self.loginButton.setStyleSheet(buttonStyle)
        self.reviewWebsiteButton.setStyleSheet(buttonStyle)
        self.registerButton.setStyleSheet(buttonStyle)
        self.exitButton.setStyleSheet(buttonStyle)
        self.accountTextbox.setFocus()

    def openMainPage(self):
        """
        open main page
        """
        with open(file=ENV_FILE,mode='r') as file:
            loginData = json.loads(file.read())
        self.userID = self.accountTextbox.text()
        self.userPassword = self.passwordTextbox.text()
        self.connect_thread = connectDB_Thread(loginData,self.userID,self.userPassword)
        self.connect_thread.conncectFailed.connect(self.connectFailedMsg)
        self.connect_thread.loginFinish.connect(self.loginMsg)
        self.connect_thread.start()

    def openRegisterWebsite(self):
        """
        open register webiste
        """
        with open(file=ENV_FILE,mode='r') as file:
            direction = 'accounts/register/'
            fileContent = json.loads(file.read())
            webbrowser.open("http://{}:{}/{}".format(fileContent["WEBSITE_HOST"],
                                                    fileContent["WEBSITE_PORT"],
                                                    direction))
        
    def openReviewWebsite(self):
        """
        open review website
        """
        with open(file=ENV_FILE,mode='r') as file:
            direction = 'accounts/login/'
            fileContent = json.loads(file.read())
            webbrowser.open("http://{}:{}/{}".format(fileContent["WEBSITE_HOST"],
                                                    fileContent["WEBSITE_PORT"],
                                                    direction))

    def connectFailedMsg(self):
        """
        connect failed message
        """
        QMessageBox(icon=QMessageBox.Critical,
                    text='無法連線到資料庫，可能是連線問題或是資料庫維護中',
                    windowIcon=self.style().standardIcon(QStyle.SP_MessageBoxCritical),
                    windowTitle='連線錯誤').exec()

    def loginMsg(self):
        """
        login message
        """
        if self.connect_thread.userExist == True:
            print('loginTime:'+self.connect_thread.loginTime)
            self.hide()
            self.mainWindow = MainWindow(self)
        else:
            QMessageBox(icon=QMessageBox.Critical,
                        windowIcon=self.style().standardIcon(QStyle.SP_MessageBoxCritical),
                        text='帳號或密碼不存在，請重新確認帳號密碼或註冊會員',
                        windowTitle='帳號密碼不存在').exec()
    


class connectDB_Thread(QThread):
    """
    connect to database thread
    """
    conncectFailed = pyqtSignal(int)
    loginFinish = pyqtSignal(int)
    def __init__(self,loginData,userID,userPassword):
        super().__init__()
        self.loginData = loginData
        self.userID = userID
        self.userPassword = userPassword

    def run(self):
        self.db = self.connectToDB(self.loginData)
        if self.db:
            self.cursor = self.db.cursor()
            self.userExist = self.checkUserExist(self.userID,self.userPassword)
            self.loginFinish.emit(1)

    def connectToDB(self,loginData):
        """
        connect to database
        """
        try:
            return pymysql.connect(host=loginData['DB_HOST'],
                                        port=loginData['DB_PORT'],
                                        user=loginData['DB_USER'],
                                        password=loginData['DB_PASSWORD'],
                                        database=loginData['DB_DATABASE'],
                                        connect_timeout=CONNECTION_TIMEOUT)
        except:
            self.conncectFailed.emit(1)
    
    def checkUserExist(self,name,password):
        """
        check user is in database or not
        """
        sql = "SELECT user_name FROM user_account;"
        self.cursor.execute(sql)
        userNameData = self.cursor.fetchall()
        sql = "SELECT user_password FROM user_account;"
        self.cursor.execute(sql)
        userPasswordData = self.cursor.fetchall()

        for userIndex in range(len(userNameData)):
            if (name == userNameData[userIndex][0] and 
                password == userPasswordData[userIndex][0]):
                self.updateLoginTime()
                return True
        return False

    def updateLoginTime(self):
        """
        update database user login time
        """
        self.loginTime= date.today().strftime("%d/%m/%Y ") + datetime.now().strftime("%H:%M:%S")
        sql = "UPDATE user_account SET last_login_time='{}' WHERE user_name='{}';".format(self.loginTime,self.userID)
        self.cursor.execute(sql)
        self.db.commit()