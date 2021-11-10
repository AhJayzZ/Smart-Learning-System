from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from .Ui_settingPage import *
from . import languages
import cv2

class SettingWindow(QDialog,Ui_settingPage):
    """
    Ui_settingPage
    """
    def __init__(self,mainWindow=None):
        super(SettingWindow,self).__init__()
        self.setupUi(self)
        self.mainWindow = mainWindow
        self.setWindowTitle("Setting Page")
        self.setWindowIcon(QIcon("./project_codes/GUI/images/setting_icon.png"))

        # Button default setting
        self.init_btn.clicked.connect(self.initialize)
        self.init_btn.setIcon(QIcon('./project_codes/GUI/images/init_icon.png'))

        # Frame default setting
        self.cap = cv2.VideoCapture(0)
        self.contrast,self.brightness=1,0
        self.average_gray_value = 0
        self.frameFlip = False

        # Camera default setting
        camera_array = ['Camera 0(Webcam)', 'Camera 1(External Camera)']
        self.camera_selector.addItems(camera_array)

        # Language default setting(index 15 means Chinese Traditional(zh-tw))
        self.languages_key_array, self.languages_value_array = languages.langauge_data()
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
        self.frameDefault_btn.clicked.connect(self.frameMode_check)
        self.frameHorizontal_btn.clicked.connect(self.frameMode_check)
        self.frameVertical_btn.clicked.connect(self.frameMode_check)
        self.frameInverse_btn.clicked.connect(self.frameMode_check)

        # Scorllbar scroll event default setting
        self.brightness_scrollbar.valueChanged.connect(
            self.frame_contrast_brightness_check)
        self.contrast_scrollbar.valueChanged.connect(
            self.frame_contrast_brightness_check)

        # Combobox clicked event default setting
        self.camera_selector.currentTextChanged.connect(
            self.camera_selector_changed)
        self.language_selector.currentTextChanged.connect(
            self.languages_selector_changed)

    def initialize(self):
        """
        Initialize all setting configuration
        """
        self.mainWindow.translate_btn.setEnabled(True)
        self.mainWindow.result_box.clear()
        self.mainWindow.translate_box.clear()
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

    def camera_selector_changed(self):
        """
        change camera to the choosen one
        """
        index = self.camera_selector.currentIndex()
        self.mainWindow.frame_thread.Recognition.cap
        if index == 0:
            self.mainWindow.frame_thread.Recognition.cap = cv2.VideoCapture(0)
        else:
            self.mainWindow.frame_thread.Recognition.cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
        self.mainWindow.frame_thread.start()

    def languages_selector_changed(self):
        """
        change to the new translate langauge and update the translation
        """
        index = self.language_selector.currentIndex()
        self.lang = self.languages_key_array[index]
        self.mainWindow.translate()

    def frame_contrast_brightness_check(self):
        """
        update frame brightness, frame contrast and setting labelshow 
        """
        self.contrast = float(self.contrast_scrollbar.value() / 100)
        self.brightness = self.brightness_scrollbar.value()
        self.contrast_label.setText('對比(' + str(self.contrast) + '):')
        self.brightness_label.setText('亮度(' + str(self.brightness) + '):')