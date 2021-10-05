from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from GUI.Ui_GUI import *
from image_recognition.recognition_program import *
from googletrans import Translator
import cv2
import sys


# 建立類別來繼承 Ui_SmartLearningSystemGUI 介面程式
class MainWindow(QtWidgets.QMainWindow, Ui_SmartLearningSystemGUI):
    def __init__(self, parent=None):
        # 繼承Ui_Gui.py
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle('Hand Recognition')
        self.setWindowIcon(QtGui.QIcon('project_codes/GUI/GUI_icon.png'))

        # Label setting
        

        # Camera setting
        camera_array = ['Camera 0(Webcam)', 'Camera 1(External Camera)']
        self.camera_selector.addItems(camera_array)

        # Timer setting
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh)
        self.timer.start(10)

        # Button trigger setting
        self.confirm_btn.clicked.connect(self.add_btn_click)
        self.revise_btn.clicked.connect(self.revise_btn_click)
        self.clear_btn.clicked.connect(self.clear_btn_click)

        # Combobox trigger setting
        self.camera_selector.currentTextChanged.connect(self.camera_selector_changed)

        self.Recognition = RecognitionProgram()

    def add_btn_click(self):
        self.result_list.addItem(self.revise_textbox.text())
        self.revise_textbox.clear()
        
    def clear_btn_click(self):
        self.result_list.clear()
        self.revise_textbox.clear()

    def revise_btn_click(self):
        selected_items = self.result_list.selectedItems()
        for item in selected_items:
            item.setText(self.revise_textbox.text())
            self.revise_textbox.clear()

    def camera_selector_changed(self) :
        if self.camera_selector.currentIndex() == 0 :
            self.Recognition._selected_camera = 0
            self.Recognition.cap = cv2.VideoCapture(0)
        elif self.camera_selector.currentIndex() == 1 :
            self.Recognition._selected_camera = 1
            self.Recognition.cap = cv2.VideoCapture(1)       

    def refresh(self):
        frame = self.Recognition.output_img
        converted_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # for webcam debug
        # frame = cv2.flip(frame,1)

        # PyQt image format
        height, width = converted_frame.shape[:2]
        pyqt_img = QImage(converted_frame, width, height, QImage.Format_RGB888)
        pyqt_img = QPixmap.fromImage(pyqt_img)

        # Camera label changed to video frame
        self.camera_label.setPixmap(pyqt_img)
        self.camera_label.setScaledContents(True)

        # Finish recognition and add text to result list
        if self.Recognition.now_state == STATE.FinishRecognition:
            self.result_list.addItem(self.Recognition.text)

        # Lightness warning 
        if self.Recognition.state_lightness == STATE_LIGHTNESS.TooBright:
            self.warning_label.setStyleSheet("color:red")
            self.warning_label.setText('Warning:光線過亮')
        elif self.Recognition.state_lightness == STATE_LIGHTNESS.TooDim:
            self.warning_label.setStyleSheet("color:red")
            self.warning_label.setText('Warning:光線過暗')
        else:
            self.warning_label.setStyleSheet("color:blue")
            self.warning_label.setText('光線正常!')

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    win.Recognition.run_program()
