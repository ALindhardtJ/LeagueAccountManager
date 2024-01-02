import sys
import utilities.utils 
from PyQt5.QtWidgets import QApplication
from lol_account_manager_gui import LolAccountManagerApp



def run_app():
    app = QApplication(sys.argv)
    app.setStyleSheet(utilities.utils.STYLESHEET)
    win = LolAccountManagerApp()
    win.show()
    sys.exit(app.exec_())



if __name__ == "__main__":
    run_app()                                               