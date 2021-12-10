from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from .GUI_mainPage import MainWindow
from .Ui_loginPage import *
import sys

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
        self.guideButton.clicked.connect(self.openGuide)
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
        self.guideButton.setStyleSheet(buttonStyle)
        self.exitButton.setStyleSheet(buttonStyle)
        self.accountTextbox.setFocus()

    def openMainPage(self):
        """
        open main page
        """
        self.hide()
        self.userID = self.accountTextbox.text()
        self.userPassword = self.passwordTextbox.text()
        self.mainWindow = MainWindow(self)

    def openGuide(self):
        """
        open user guide
        """
        guideText = open(file='./project_codes/GUI/guide.txt',mode='r',encoding='utf-8')
        QMessageBox(icon=QMessageBox.Information,
                    windowIcon=QIcon('./project_codes/GUI/images/guide_icon.png'),
                    windowTitle='使用說明',
                    text=guideText.read()).exec()

    def openReviewWebsite(self):
        """
        open review website
        """
        print('Not finish yet')
