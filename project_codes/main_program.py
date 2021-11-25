from GUI.GUI_main import MainWindow
from PyQt5.QtWidgets import *
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    win.Recognition.run_program()
    sys.exit(app.exec_())
