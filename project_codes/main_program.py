from GUI.GUI_main import *
import sys

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    win.Recognition.run_program()
    sys.exit(app.exec_())