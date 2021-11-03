"""
setting CSS style of GUI (Unfinished)
"""

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from .Ui_GUI import *

class setupCSS(Ui_SmartLearningSystemGUI):
    def __init__(self):
        #super(setupCSS,self).setupUi()
        self.setStyleSheet("background-color:#0E5746")

