from GUI.GUI_main import MainWindow
from PyQt5.QtWidgets import *
import sys

app = QApplication(sys.argv)
win = MainWindow()

if __name__ == "__main__":
    win.show()
    win.Recognition.run_program()
    sys.exit(app.exec_())