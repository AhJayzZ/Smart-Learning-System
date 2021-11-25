
from GUI.GUI_loginPage import LoginPage
from PyQt5.QtWidgets import QApplication
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    initialPage = LoginPage()
    sys.exit(app.exec_())