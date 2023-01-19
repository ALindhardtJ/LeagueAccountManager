from itertools import zip_longest
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from database import *
from threading import Thread
from bs4 import BeautifulSoup
from pynput.keyboard import Key, Controller
from time import sleep
import sys, requests, math, subprocess, psutil, os

app = QApplication(sys.argv)
screen = app.primaryScreen()
rect = screen.availableGeometry()
rect.width()
rect.height()


class MyWindow(QWidget):
    def __init__(self):
        super(MyWindow, self).__init__()
        # Get screen size
        self.screen_size = screen.size()
        # size of 'account manager' window
        self.acc_man_width = (self.convToRectWidth(1024))
        self.acc_man_height = (self.convToRectHeight(700))
        # size of 'add account' window
        self.add_acc_width = (self.convToRectWidth(328))
        self.add_acc_height = (self.convToRectHeight(385))
        # size of 'info' window
        self.info_width = (self.convToRectWidth(328))
        self.info_height = (self.convToRectHeight(220))
        # size of 'edit' window
        self.edit_width = (self.convToRectWidth(328))
        self.edit_height = (self.convToRectHeight(385))
        # size of 'champions' window
        self.champions_width = (self.convToRectWidth(1010))
        self.champions_height = (self.convToRectHeight(700))
        # starting x,y pos for window
        self.xpos = (self.convToRectXpos(800))
        self.ypos = (self.convToRectYpos(300))
        # text color
        self.text_color = "color: #519aba;"     
        # font size
        self.font_size = 13   
        # headers stylesheet
        self.headers_stylesheet = "border: 1px solid grey;"
        # QLineEdit stylesheet
        self.QLineEdit_stylesheet = "border: 1px solid grey;"
        # define current window
        self.current_window = "account manager"
        # bool to check password checkbox
        self.isPasswordCheckBoxChecked = False
        # collecting data check
        self.collecting_data = True
        # loading summoner data check
        self.loading_all_summoner_data = True
        # first run check
        self.isFirstRun = True
        # Dict of all widgets
        self.widgets = {
            "buttons": [],
            "images": [],
            "comboBox": [],
            "lineEdits": [],
            "checkBoxes": [],
            "labels": [],
        }
        # list of accounts stored
        self.accounts = []
        # list of fetched summoner data
        self.summoner_data = []
        # selected row tracker
        self.selected_pkID = 1
        # username belonging to selected selected_pkiD
        self.selected_username = ""
        # password belonging to selected selected_pkiD
        self.selected_password = ""
        # region, summoner name, username, password stored for checkbox action
        self.comboBoxRegion = ""
        self.QlineEditSumName = ""
        self.QlineEditUsername = ""
        self.QlineEditPassword = ""
        # initialize window
        self.setWindowIcon(QIcon("./account_man_icon_2.png"))
        self.setGeometry(self.xpos, self.ypos, self.acc_man_width, self.acc_man_height)
        self.setFixedWidth(self.acc_man_width)
        self.setFixedHeight(self.acc_man_height)
        self.setStyleSheet("background-color: #1a1b26; color: #519aba;")
        # buttons shared stylesheet
        self.button_stylesheet = """
                            QPushButton {
                                background-color: #252630;
                                color: #519aba;
                            }
                            QPushButton::checked {
                                background-color: #5f32e6;
                                color: #d2d2d2
                            }
                            QPushButton::pressed {
                                background-color: #5f32e6;
                            }
                            QPushButton:hover {
                                color: #d2d2d2;
                            }
                            """
        self.setWindowTitle("League Account Manager")
        # GUI init
        self.GUI()

#------------------------------------------------------------------------------------------------------
#Defining user interfaces of different windows
    def GUI(self):
        if self.current_window == "account manager":
            # logo
            self.make_logo()
            # 'account manager' button
            self.buttons("account manager")
            # 'add account' button
            self.buttons("add account")
            # 'login' button
            self.buttons("login")
            # 'delete' button
            self.buttons("delete")
            # 'info' button
            self.buttons("info")
            # 'edit' button definition
            self.buttons("edit")
            # 'champs register/check/delete' button definition
            self.buttons("champions")
            # 'headers for accounts list'
            self.headers()
            # 'accounts list'
            self.accountsList()
            # 'collecting data' label
            self.makeLabel("collecting data")


        elif self.current_window == "add account":
            # logo
            self.make_logo()
            # 'account manager' button
            self.buttons("account manager")
            # 'region' label
            self.makeLabel("region")
            # 'region' comboBox
            self.combo_boxes("region")
            # text fields
            self.line_edits("summoner_name")
            self.line_edits("username")
            self.line_edits("password")
            self.makeCheckBox("password")
            # 'submit account' button
            self.buttons("submit account")


        elif self.current_window == "info":
            # logo
            self.make_logo()
            # 'account manager' button
            self.buttons("account manager")
            # QLineEdits
            self.line_edits("username")
            self.line_edits("password")
            # 'checkbox for password'
            self.makeCheckBox("password")
            # 'label for username'
            self.makeLabel("info")


        elif self.current_window == "edit":
            # logo
            self.make_logo()
            # 'account manager' button
            self.buttons("account manager")
            # 'region' label
            self.makeLabel("region")
            # 'region' comboBox
            self.combo_boxes("region")
            # text fields
            self.line_edits("summoner_name")
            self.line_edits("username")
            self.line_edits("password")
            self.makeCheckBox("password")
            # 'submit account' button
            self.buttons("submit account")


        elif self.current_window == "champions":
            # logo
            self.make_logo()
            # 'account manager' button
            self.buttons("account manager")
            # 'under development QLineEdit'
            self.makeLabel("under_development")


#------------------------------------------------------------------------------------------------------
# Defining decsriptions of different widgets

    #Delete pop-up box
    def pop_up_box(self, whatfor):
        if whatfor == "delete":
            msg = QMessageBox(self)
            msg.setText("'Delete' button only works while not still collecting account data")
            x = msg.exec_()

    #logo description'
    def make_logo(self):
        self.logo = QLabel(self)
        self.image = QPixmap("./account_man_icon_2.png")
        self.image2 = self.image.scaledToHeight(self.convToRectWidth(40))
        self.logo.setPixmap(self.image2)
        self.logo.move(self.convToRectWidth(10), self.convToRectHeight(10))
        self.widgets["images"].append(self.logo)

    #Label description
    def makeLabel(self, whatfor):
        if whatfor == "region":
            self.region_label = QLabel(self)
            self.region_label.setText("Choose a Region")
            self.region_label.move(self.convToRectWidth(20), self.convToRectHeight(107))
            self.widgets["labels"].append(self.region_label)
        
        elif whatfor == "info":
            self.username_label = QLabel(self)
            self.username_label.setText("Username")
            self.username_label.move(self.convToRectWidth(50), self.convToRectHeight(110))
            self.widgets["labels"].append(self.username_label)

        elif whatfor == "under_development":
            self.username_label = QLabel(self)
            self.username_label.setText("Under development")
            self.username_label.move(self.convToRectWidth(50), self.convToRectHeight(110))
            self.widgets["labels"].append(self.username_label)

        elif whatfor == "collecting data":
            if self.collecting_data:
                self.collecting_data_label = QLabel(self)
                self.collecting_data_label.setText("Collecting account data")
                self.collecting_data_label.move(self.convToRectWidth(895), self.convToRectHeight(75))
                self.collecting_data_label.setStyleSheet("color: orange")
                self.widgets["labels"].append(self.collecting_data_label)
            else:
                pass

    #Checkbox desription
    def makeCheckBox(self, checkBox):
        if self.current_window == "add account":
            if checkBox == "password":
                if not self.isPasswordCheckBoxChecked:
                    self.passCheckBox = QCheckBox(self)
                    self.passCheckBox.setText("Show Password")
                    self.passCheckBox.stateChanged.connect(self.checkBox)
                    self.passCheckBox.move(self.convToRectWidth(15), self.convToRectHeight(285))
                    self.widgets["checkBoxes"].append(self.passCheckBox)       
                else:     
                    self.passCheckBox = QCheckBox(self)
                    self.passCheckBox.setChecked(True)
                    self.passCheckBox.setText("Show Password")
                    self.passCheckBox.stateChanged.connect(self.checkBox)
                    self.passCheckBox.move(self.convToRectWidth(15), self.convToRectHeight(285))
                    self.widgets["checkBoxes"].append(self.passCheckBox)   

        elif self.current_window == "edit":
            if checkBox == "password":
                if not self.isPasswordCheckBoxChecked:
                    self.passCheckBox = QCheckBox(self)
                    self.passCheckBox.setText("Show Password")
                    self.passCheckBox.stateChanged.connect(self.checkBox)
                    self.passCheckBox.move(self.convToRectWidth(15), self.convToRectHeight(285))
                    self.widgets["checkBoxes"].append(self.passCheckBox)       
                else:     
                    self.passCheckBox = QCheckBox(self)
                    self.passCheckBox.setChecked(True)
                    self.passCheckBox.setText("Show Password")
                    self.passCheckBox.stateChanged.connect(self.checkBox)
                    self.passCheckBox.move(self.convToRectWidth(15), self.convToRectHeight(285))
                    self.widgets["checkBoxes"].append(self.passCheckBox)      
        
        elif self.current_window == "info":
            if checkBox == "password":
                if not self.isPasswordCheckBoxChecked:
                    self.passCheckBox = QCheckBox(self)
                    self.passCheckBox.setText("Show Password")
                    self.passCheckBox.stateChanged.connect(self.checkBox)
                    self.passCheckBox.move(self.convToRectWidth(15), self.convToRectHeight(167))
                    self.widgets["checkBoxes"].append(self.passCheckBox)       
                else:     
                    self.passCheckBox = QCheckBox(self)
                    self.passCheckBox.setChecked(True)
                    self.passCheckBox.setText("Show Password")
                    self.passCheckBox.stateChanged.connect(self.checkBox)
                    self.passCheckBox.move(self.convToRectWidth(15), self.convToRectHeight(167))
                    self.widgets["checkBoxes"].append(self.passCheckBox) 


    #Button describtions
    def buttons(self, button):
    # Account manager button and releted buttons
        if button == "account manager":
            self.acc_man_button = QPushButton(self)
            self.acc_man_button.setCursor(QCursor(Qt.PointingHandCursor))
            self.acc_man_button.setStyleSheet(self.button_stylesheet)
            self.acc_man_button.resize(self.convToRectWidth(160), self.convToRectHeight(40))
            self.acc_man_button.move(self.convToRectWidth(65), self.convToRectHeight(15))
            self.acc_man_button.setText("Account Manager")
            self.acc_man_button.setFont(QFont('AnyStyle', self.font_size))
            self.acc_man_button.clicked.connect(self.acc_man_button_clicked)
            self.widgets["buttons"].append(self.acc_man_button)

    # Add account button and related buttons
        elif button == "add account":
            self.add_acc_button = QPushButton(self)
            self.add_acc_button.setCursor(QCursor(Qt.PointingHandCursor))
            self.add_acc_button.setStyleSheet(self.button_stylesheet)
            self.add_acc_button.move(self.convToRectWidth(235), self.convToRectHeight(15))
            self.add_acc_button.resize(self.convToRectWidth(150), self.convToRectHeight(40))
            self.add_acc_button.setText("Add Account")
            self.add_acc_button.setFont(QFont('AnyStyle', self.font_size))
            self.add_acc_button.clicked.connect(self.add_acc_button_clicked)
            self.widgets["buttons"].append(self.add_acc_button)

        elif button == "submit account":
            if self.current_window == "add account":
                self.subm_acc_button = QPushButton(self)
                self.subm_acc_button.setCursor(QCursor(Qt.PointingHandCursor))
                self.subm_acc_button.setStyleSheet(self.button_stylesheet)
                self.subm_acc_button.move(self.convToRectWidth(130), self.convToRectHeight(335))
                self.subm_acc_button.resize(self.convToRectWidth(170),self.convToRectHeight(40))
                self.subm_acc_button.setText("Submit Account")
                self.subm_acc_button.setFont(QFont('AnyStyle', self.font_size))
                self.subm_acc_button.clicked.connect(self.subm_acc_button_clicked)
                self.widgets["buttons"].append(self.subm_acc_button)

            elif self.current_window == "edit":
                self.subm_acc_button = QPushButton(self)
                self.subm_acc_button.setCursor(QCursor(Qt.PointingHandCursor))
                self.subm_acc_button.setStyleSheet(self.button_stylesheet)
                self.subm_acc_button.move(self.convToRectWidth(130), self.convToRectHeight(335))
                self.subm_acc_button.resize(self.convToRectWidth(170),self.convToRectHeight(40))
                self.subm_acc_button.setText("Edit Account")
                self.subm_acc_button.setFont(QFont('AnyStyle', self.font_size))
                self.subm_acc_button.clicked.connect(self.subm_acc_button_clicked)
                self.widgets["buttons"].append(self.subm_acc_button)

    # Login button
        elif button == "login":
            self.login_button = QPushButton(self)
            self.login_button.setCursor(QCursor(Qt.PointingHandCursor))
            self.login_button.setStyleSheet(self.button_stylesheet)
            self.login_button.move(self.convToRectWidth(395), self.convToRectHeight(15))
            self.login_button.resize(self.convToRectWidth(100), self.convToRectHeight(40))
            self.login_button.setText("Login")
            self.login_button.setFont(QFont('AnyStyle', self.font_size))
            self.login_button.clicked.connect(self.login_button_clicked)
            self.widgets["buttons"].append(self.login_button)

    # Info button    
        elif button == "info":
            self.info_button = QPushButton(self)
            self.info_button.setCursor(QCursor(Qt.PointingHandCursor))
            self.info_button.setStyleSheet(self.button_stylesheet)
            self.info_button.move(self.convToRectWidth(505), self.convToRectHeight(15))
            self.info_button.resize(self.convToRectWidth(70),self.convToRectHeight(40))
            self.info_button.setText("Info")
            self.info_button.setFont(QFont('AnyStyle', self.font_size))
            self.info_button.clicked.connect(self.info_button_clicked)
            self.widgets["buttons"].append(self.info_button)

    # Edit button 
        elif button == "edit":
            self.edit_button = QPushButton(self)
            self.edit_button.setCursor(QCursor(Qt.PointingHandCursor))
            self.edit_button.setStyleSheet(self.button_stylesheet)
            self.edit_button.move(self.convToRectWidth(585), self.convToRectHeight(15))
            self.edit_button.resize(self.convToRectWidth(130), self.convToRectHeight(40))
            self.edit_button.setText("Edit")
            self.edit_button.setFont(QFont('AnyStyle', self.font_size))
            self.edit_button.clicked.connect(self.edit_button_clicked)
            self.widgets["buttons"].append(self.edit_button)

    # Delete button    
        elif button == "delete":
            self.delete_button = QPushButton(self)
            self.delete_button.setCursor(QCursor(Qt.PointingHandCursor))
            self.delete_button.setStyleSheet(self.button_stylesheet)
            self.delete_button.move(self.convToRectWidth(725), self.convToRectHeight(15))
            self.delete_button.resize(self.convToRectWidth(160), self.convToRectHeight(40))
            self.delete_button.setText("Delete")
            self.delete_button.setFont(QFont('AnyStyle', self.font_size))
            self.delete_button.clicked.connect(self.delete_button_clicked)
            self.widgets["buttons"].append(self.delete_button)

    # Champions button and related buttons    
        elif button == "champions":
            self.champions_button = QPushButton(self)
            self.champions_button.setCursor(QCursor(Qt.PointingHandCursor))
            self.champions_button.setStyleSheet(self.button_stylesheet)
            self.champions_button.move(self.convToRectWidth(900), self.convToRectHeight(15))
            self.champions_button.resize(self.convToRectWidth(110),self.convToRectHeight(40))
            self.champions_button.setText("Champions")
            self.champions_button.setFont(QFont('AnyStyle', self.font_size))
            self.champions_button.clicked.connect(self.champions_button_clicked)
            self.widgets["buttons"].append(self.champions_button)


    # Combo box descriptions 
    def combo_boxes(self, comboBox):
    # ComboBox for choosing region in 'add account'
        if self.current_window == "add account":
            if comboBox == "region":
                self.region_comboBox = QComboBox(self)
                self.region_comboBox.setCursor(QCursor(Qt.PointingHandCursor))
                regions = ["BR", "EUNE", "EUW", "JP", "KR", "LAN", "LAS", "NA", "OCE", "RU", "TR"]

                for region in regions:
                    self.region_comboBox.addItem(region)

                if self.comboBoxRegion == "":
                    self.region_comboBox.move(self.convToRectWidth(130), self.convToRectHeight(95))
                    self.region_comboBox.resize(self.convToRectWidth(170), self.convToRectHeight(40))
                    self.region_comboBox.setFont(QFont('AnyStyle', self.font_size))
                    self.widgets["comboBox"].append(self.region_comboBox)
                else:
                    self.region_comboBox.setCurrentText(self.comboBoxRegion)
                    self.region_comboBox.move(self.convToRectWidth(130), self.convToRectHeight(95))
                    self.region_comboBox.resize(self.convToRectWidth(170), self.convToRectHeight(40))
                    self.region_comboBox.setFont(QFont('AnyStyle', self.font_size))
                    self.widgets["comboBox"].append(self.region_comboBox)

        elif self.current_window == "edit":
            if comboBox == "region":
                self.region_comboBox = QComboBox(self)
                self.region_comboBox.setCursor(QCursor(Qt.PointingHandCursor))
                regions = ["Region","BR", "EUNE", "EUW", "JP", "KR", "LAN", "LAS", "NA", "OCE", "RU", "TR"]

                for region in regions:
                    self.region_comboBox.addItem(region)

                if self.comboBoxRegion == "":
                    self.region_comboBox.move(self.convToRectWidth(130), self.convToRectHeight(95))
                    self.region_comboBox.resize(self.convToRectWidth(170), self.convToRectHeight(40))
                    self.region_comboBox.setFont(QFont('AnyStyle', self.font_size))
                    self.widgets["comboBox"].append(self.region_comboBox)
                else:
                    self.region_comboBox.setCurrentText(self.comboBoxRegion)
                    self.region_comboBox.move(self.convToRectWidth(130), self.convToRectHeight(95))
                    self.region_comboBox.resize(self.convToRectWidth(170), self.convToRectHeight(40))
                    self.region_comboBox.setFont(QFont('AnyStyle', self.font_size))
                    self.widgets["comboBox"].append(self.region_comboBox)

    # Line edit descriptions
    def line_edits(self, lineEdit):
    # Line edits for 'Add account'
        if self.current_window == "add account":
            if lineEdit == "summoner_name":
                self.summoner_name = QLineEdit(self)
                self.summoner_name.setStyleSheet(self.QLineEdit_stylesheet)
                self.summoner_name.setPlaceholderText("Summoner name")
                if not self.QlineEditSumName == "":
                    self.summoner_name.setText(self.QlineEditSumName)
                self.summoner_name.move(self.convToRectWidth(130), self.convToRectHeight(155))
                self.summoner_name.resize(self.convToRectWidth(170), self.convToRectHeight(40))
                self.summoner_name.setFont(QFont('AnyStyle', self.font_size))
                self.widgets["lineEdits"].append(self.summoner_name)

            elif lineEdit == "username":
                self.username = QLineEdit(self)
                self.username.setStyleSheet(self.QLineEdit_stylesheet)
                self.username.setPlaceholderText("Username")
                if not self.QlineEditUsername == "":
                    self.username.setText(self.QlineEditUsername)
                self.username.move(self.convToRectWidth(130), self.convToRectHeight(215))
                self.username.resize(self.convToRectWidth(170), self.convToRectHeight(40))
                self.username.setFont(QFont('AnyStyle', self.font_size))
                self.widgets["lineEdits"].append(self.username)

            elif lineEdit == "password":
                if not self.isPasswordCheckBoxChecked:
                    self.password = QLineEdit(self)
                    self.password.setStyleSheet(self.QLineEdit_stylesheet)
                    self.password.setEchoMode(QLineEdit.Password)
                    self.password.setPlaceholderText("Password")
                    if not self.QlineEditPassword == "":
                        self.password.setText(self.QlineEditPassword)
                    self.password.move(self.convToRectWidth(130), self.convToRectHeight(275))
                    self.password.resize(self.convToRectWidth(170), self.convToRectHeight(40))
                    self.password.setFont(QFont('AnyStyle', self.font_size))
                    self.widgets["lineEdits"].append(self.password)
                else:
                    self.password = QLineEdit(self)
                    self.password.setStyleSheet(self.QLineEdit_stylesheet)
                    self.password.setText(self.QlineEditPassword)
                    self.password.setPlaceholderText("Password")
                    if not self.QlineEditPassword == "":
                        self.password.setText(self.QlineEditPassword)
                    self.password.move(self.convToRectWidth(130), self.convToRectHeight(275))
                    self.password.resize(self.convToRectWidth(170), self.convToRectHeight(40))
                    self.password.setFont(QFont('AnyStyle', self.font_size))
                    self.widgets["lineEdits"].append(self.password)

        elif self.current_window == "edit":
            if lineEdit == "summoner_name":
                self.summoner_name = QLineEdit(self)
                self.summoner_name.setStyleSheet(self.QLineEdit_stylesheet)
                self.summoner_name.setPlaceholderText("Summoner name")
                if not self.QlineEditSumName == "":
                    self.summoner_name.setText(self.QlineEditSumName)
                self.summoner_name.move(self.convToRectWidth(130), self.convToRectHeight(155))
                self.summoner_name.resize(self.convToRectWidth(170), self.convToRectHeight(40))
                self.summoner_name.setFont(QFont('AnyStyle', self.font_size))
                self.widgets["lineEdits"].append(self.summoner_name)

            elif lineEdit == "username":
                self.username = QLineEdit(self)
                self.username.setStyleSheet(self.QLineEdit_stylesheet)
                self.username.setPlaceholderText("Username")
                if not self.QlineEditUsername == "":
                    self.username.setText(self.QlineEditUsername)
                self.username.move(self.convToRectWidth(130), self.convToRectHeight(215))
                self.username.resize(self.convToRectWidth(170), self.convToRectHeight(40))
                self.username.setFont(QFont('AnyStyle', self.font_size))
                self.widgets["lineEdits"].append(self.username)

            elif lineEdit == "password":
                if not self.isPasswordCheckBoxChecked:
                    self.password = QLineEdit(self)
                    self.password.setStyleSheet(self.QLineEdit_stylesheet)
                    self.password.setEchoMode(QLineEdit.Password)
                    self.password.setPlaceholderText("Password")
                    if not self.QlineEditPassword == "":
                        self.password.setText(self.QlineEditPassword)
                    self.password.move(self.convToRectWidth(130), self.convToRectHeight(275))
                    self.password.resize(self.convToRectWidth(170), self.convToRectHeight(40))
                    self.password.setFont(QFont('AnyStyle', self.font_size))
                    self.widgets["lineEdits"].append(self.password)
                else:
                    self.password = QLineEdit(self)
                    self.password.setStyleSheet(self.QLineEdit_stylesheet)
                    self.password.setText(self.QlineEditPassword)
                    self.password.setPlaceholderText("Password")
                    if not self.QlineEditPassword == "":
                        self.password.setText(self.QlineEditPassword)
                    self.password.move(self.convToRectWidth(130), self.convToRectHeight(275))
                    self.password.resize(self.convToRectWidth(170), self.convToRectHeight(40))
                    self.password.setFont(QFont('AnyStyle', self.font_size))
                    self.widgets["lineEdits"].append(self.password)


        elif self.current_window == "info":
            pkID, region, sumName, username, password = dbHandler.get_account(self.selected_pkID)

            if lineEdit == "username":
                self.username = QLineEdit(self)
                self.username.setStyleSheet(self.QLineEdit_stylesheet)
                if not self.QlineEditUsername == "":
                    self.username.setText(self.QlineEditUsername)
                else:
                    self.username.setText(username)
                self.username.move(self.convToRectWidth(130), self.convToRectHeight(97))
                self.username.resize(self.convToRectWidth(170), self.convToRectHeight(40))
                self.username.setFont(QFont('AnyStyle', self.font_size))
                self.widgets["lineEdits"].append(self.username)

            elif lineEdit == "password":
                if not self.isPasswordCheckBoxChecked:
                    self.password = QLineEdit(self)
                    self.password.setStyleSheet(self.QLineEdit_stylesheet)
                    self.password.setEchoMode(QLineEdit.Password)
                    if not self.QlineEditPassword == "":
                        self.password.setText(self.QlineEditPassword)
                    else:
                        self.password.setText(password)
                    self.password.move(self.convToRectWidth(130), self.convToRectHeight(157))
                    self.password.resize(self.convToRectWidth(170), self.convToRectHeight(40))
                    self.password.setFont(QFont('AnyStyle', self.font_size))
                    self.widgets["lineEdits"].append(self.password)
                else:
                    self.password = QLineEdit(self)
                    self.password.setStyleSheet(self.QLineEdit_stylesheet)
                    self.password.setText(self.QlineEditPassword)
                    self.password.setPlaceholderText("Password")
                    if not self.QlineEditPassword == "":
                        self.password.setText(self.QlineEditPassword)
                    else:
                        self.password.setText(password)
                    self.password.move(self.convToRectWidth(130), self.convToRectHeight(157))
                    self.password.resize(self.convToRectWidth(170), self.convToRectHeight(40))
                    self.password.setFont(QFont('AnyStyle', self.font_size))
                    self.widgets["lineEdits"].append(self.password)


    # Headers for 'account manager'
    def headers(self):
        self.id_label = QLabel(self)
        self.id_label.move(self.convToRectWidth(15), self.convToRectHeight(65))
        self.id_label.resize(self.convToRectWidth(40), self.convToRectHeight(40))
        self.id_label.setText("ID")
        self.id_label.setFont(QFont('AnyStyle', self.font_size))
        self.id_label.setStyleSheet(self.headers_stylesheet)
        self.widgets["labels"].append(self.id_label)

        self.name_label = QLabel(self)
        self.name_label.move(self.convToRectWidth(65), self.convToRectHeight(65))
        self.name_label.resize(self.convToRectWidth(160), self.convToRectHeight(40))
        self.name_label.setText("Name")
        self.name_label.setFont(QFont('AnyStyle', self.font_size))
        self.name_label.setStyleSheet(self.headers_stylesheet)
        self.widgets["labels"].append(self.name_label)
        
        self.rank_label = QLabel(self)
        self.rank_label.move(self.convToRectWidth(235), self.convToRectHeight(65))
        self.rank_label.resize(self.convToRectWidth(150), self.convToRectHeight(40))
        self.rank_label.setText("Rank")
        self.rank_label.setFont(QFont('AnyStyle', self.font_size))
        self.rank_label.setStyleSheet(self.headers_stylesheet)
        self.widgets["labels"].append(self.rank_label)

        self.region_label = QLabel(self)
        self.region_label.move(self.convToRectWidth(395), self.convToRectHeight(65))
        self.region_label.resize(self.convToRectWidth(100), self.convToRectHeight(40))
        self.region_label.setText("Region")
        self.region_label.setFont(QFont('AnyStyle', self.font_size))
        self.region_label.setStyleSheet(self.headers_stylesheet)
        self.widgets["labels"].append(self.region_label)
       
        self.level_label = QLabel(self)
        self.level_label.move(self.convToRectWidth(505), self.convToRectHeight(65))
        self.level_label.resize(self.convToRectWidth(70), self.convToRectHeight(40))
        self.level_label.setText("Level")
        self.level_label.setFont(QFont('AnyStyle', self.font_size))
        self.level_label.setStyleSheet(self.headers_stylesheet)
        self.widgets["labels"].append(self.level_label)        

        self.thirtyDays_label = QLabel(self)
        self.thirtyDays_label.move(self.convToRectWidth(585), self.convToRectHeight(65))
        self.thirtyDays_label.resize(self.convToRectWidth(130), self.convToRectHeight(40))
        self.thirtyDays_label.setText("Last 30 Days")
        self.thirtyDays_label.setFont(QFont('AnyStyle', self.font_size)) 
        self.thirtyDays_label.setStyleSheet(self.headers_stylesheet) 
        self.widgets["labels"].append(self.thirtyDays_label)       

        self.hoursPlayed_label = QLabel(self)
        self.hoursPlayed_label.move(self.convToRectWidth(725), self.convToRectHeight(65))
        self.hoursPlayed_label.resize(self.convToRectWidth(160), self.convToRectHeight(40))
        self.hoursPlayed_label.setText("Hours Played Total")
        self.hoursPlayed_label.setFont(QFont('AnyStyle', self.font_size))
        self.hoursPlayed_label.setStyleSheet(self.headers_stylesheet)
        self.widgets["labels"].append(self.hoursPlayed_label)

    # list accounts in db
    def accountsList(self):
        rows = 0
        id_move_x, id_move_y = self.convToRectWidth(15), self.convToRectHeight(65)
        name_move_x, name_move_y = self.convToRectWidth(65), self.convToRectHeight(65)
        rank_move_x, rank_move_y = self.convToRectWidth(235), self.convToRectHeight(65)
        region_move_x, region_move_y = self.convToRectWidth(395), self.convToRectHeight(65)
        level_move_x, level_move_y = self.convToRectWidth(505), self.convToRectHeight(65)
        lastThirty_move_x, lastThirty_move_y = self.convToRectWidth(585), self.convToRectHeight(65)
        hoursTotal_move_x, hoursTotal_move_y = self.convToRectWidth(725), self.convToRectHeight(65)
        account_button_move_x, account_button_move_y = self.convToRectWidth(900), self.convToRectHeight(65)

        if self.isFirstRun:
            accounts = dbHandler.get_accounts()
            self.accounts = accounts
            thread = Thread(target=self.fetch_account_data, args=(self.accounts, "all",))
            thread.start()
            upWindow = Thread(target=self.updateWindowThread)
            upWindow.start()
            for account in self.accounts:
                pkID, region, sumName, username, password = account

                self.account_label = QLabel(self)
                self.account_label.move(id_move_x, id_move_y + self.convToRectHeight(40))
                id_move_y += self.convToRectHeight(40)
                self.account_label.resize(self.convToRectWidth(40), self.convToRectHeight(40))
                self.account_label.setText(str(pkID))
                self.account_label.setFont(QFont('AnyStyle', self.font_size))
                self.account_label.setStyleSheet(self.headers_stylesheet)
                self.widgets["labels"].append(self.account_label)

                self.account_label = QLabel(self)
                self.account_label.move(name_move_x, name_move_y + self.convToRectHeight(40))
                name_move_y += self.convToRectHeight(40)
                self.account_label.resize(self.convToRectWidth(160), self.convToRectHeight(40))
                self.account_label.setText(str(sumName))
                self.account_label.setFont(QFont('AnyStyle', self.font_size))
                self.account_label.setStyleSheet(self.headers_stylesheet)
                self.widgets["labels"].append(self.account_label)

                self.account_label = QLabel(self)
                self.account_label.move(rank_move_x, rank_move_y + self.convToRectHeight(40))
                rank_move_y += self.convToRectHeight(40)
                self.account_label.resize(self.convToRectWidth(150), self.convToRectHeight(40))
                # self.account_label.setText(str(self.summoner_data[(len(self.summoner_data)-1)][1]))
                self.account_label.setFont(QFont('AnyStyle', self.font_size))
                self.account_label.setStyleSheet(self.headers_stylesheet)
                self.widgets["labels"].append(self.account_label)

                self.account_label = QLabel(self)
                self.account_label.move(region_move_x, region_move_y + self.convToRectHeight(40))
                region_move_y += self.convToRectHeight(40)
                self.account_label.resize(self.convToRectWidth(100), self.convToRectHeight(40))
                self.account_label.setText(str(region))
                self.account_label.setFont(QFont('AnyStyle', self.font_size))
                self.account_label.setStyleSheet(self.headers_stylesheet)
                self.widgets["labels"].append(self.account_label)

                self.account_label = QLabel(self)
                self.account_label.move(level_move_x, level_move_y + self.convToRectHeight(40))
                level_move_y += self.convToRectHeight(40)
                self.account_label.resize(self.convToRectWidth(70), self.convToRectHeight(40))
                # self.account_label.setText(str(self.summoner_data[(len(self.summoner_data)-1)][0]))
                self.account_label.setFont(QFont('AnyStyle', self.font_size))
                self.account_label.setStyleSheet(self.headers_stylesheet)
                self.widgets["labels"].append(self.account_label)

                self.account_label = QLabel(self)
                self.account_label.move(lastThirty_move_x, lastThirty_move_y + self.convToRectHeight(40))
                lastThirty_move_y += self.convToRectHeight(40)
                self.account_label.resize(self.convToRectWidth(130), self.convToRectHeight(40))
                # self.account_label.setText(str(self.summoner_data[(len(self.summoner_data)-1)][2]) + " Games")
                self.account_label.setFont(QFont('AnyStyle', self.font_size))
                self.account_label.setStyleSheet(self.headers_stylesheet)
                self.widgets["labels"].append(self.account_label)

                self.account_label = QLabel(self)
                self.account_label.move(hoursTotal_move_x, hoursTotal_move_y + self.convToRectHeight(40))
                hoursTotal_move_y += self.convToRectHeight(40)
                self.account_label.resize(self.convToRectWidth(160), self.convToRectHeight(40))
                # self.account_label.setText(str(self.summoner_data[(len(self.summoner_data)-1)][3]))
                self.account_label.setFont(QFont('AnyStyle', self.font_size))
                self.account_label.setStyleSheet(self.headers_stylesheet)
                self.widgets["labels"].append(self.account_label)

                self.account_button = QPushButton(self)
                self.account_button.setCursor(QCursor(Qt.PointingHandCursor))
                self.account_button.setStyleSheet(self.button_stylesheet)
                self.account_button.setCheckable(True)
                self.account_button.move(account_button_move_x, account_button_move_y + self.convToRectHeight(40))
                account_button_move_y += self.convToRectHeight(40)
                self.account_button.resize(self.convToRectWidth(110),self.convToRectHeight(40))
                self.account_button.setText("Select")
                self.account_button.setObjectName(str(pkID))
                self.account_button.setFont(QFont('AnyStyle', self.font_size))
                self.account_button.clicked.connect(self.select_button_clicked)
                self.widgets["buttons"].append(self.account_button)

            self.isFirstRun = False
        
        else:
            for account, data in zip_longest(self.accounts, self.summoner_data):
                rows += 1
                pkID, region, sumName, username, password = account
                try:
                    level, rank, gamesThirty, hours = data
                except:
                    level = ""
                    rank = ""
                    gamesThirty = ""
                    hours = ""
        

                self.account_label = QLabel(self)
                self.account_label.move(id_move_x, id_move_y + self.convToRectHeight(40))
                id_move_y += self.convToRectHeight(40)
                self.account_label.resize(self.convToRectWidth(40), self.convToRectHeight(40))
                self.account_label.setText(str(pkID))
                self.account_label.setFont(QFont('AnyStyle', self.font_size))
                self.account_label.setStyleSheet(self.headers_stylesheet)
                self.widgets["labels"].append(self.account_label)

                self.account_label = QLabel(self)
                self.account_label.move(name_move_x, name_move_y + self.convToRectHeight(40))
                name_move_y += self.convToRectHeight(40)
                self.account_label.resize(self.convToRectWidth(160), self.convToRectHeight(40))
                self.account_label.setText(str(sumName))
                self.account_label.setFont(QFont('AnyStyle', self.font_size))
                self.account_label.setStyleSheet(self.headers_stylesheet)
                self.widgets["labels"].append(self.account_label)

                self.account_label = QLabel(self)
                self.account_label.move(rank_move_x, rank_move_y + self.convToRectHeight(40))
                rank_move_y += self.convToRectHeight(40)
                self.account_label.resize(self.convToRectWidth(150), self.convToRectHeight(40))
                self.account_label.setText(str(rank))
                self.account_label.setFont(QFont('AnyStyle', self.font_size))
                self.account_label.setStyleSheet(self.headers_stylesheet)
                self.widgets["labels"].append(self.account_label)

                self.account_label = QLabel(self)
                self.account_label.move(region_move_x, region_move_y + self.convToRectHeight(40))
                region_move_y += self.convToRectHeight(40)
                self.account_label.resize(self.convToRectWidth(100), self.convToRectHeight(40))
                self.account_label.setText(str(region))
                self.account_label.setFont(QFont('AnyStyle', self.font_size))
                self.account_label.setStyleSheet(self.headers_stylesheet)
                self.widgets["labels"].append(self.account_label)

                self.account_label = QLabel(self)
                self.account_label.move(level_move_x, level_move_y + self.convToRectHeight(40))
                level_move_y += self.convToRectHeight(40)
                self.account_label.resize(self.convToRectWidth(70), self.convToRectHeight(40))
                self.account_label.setText(str(level))
                self.account_label.setFont(QFont('AnyStyle', self.font_size))
                self.account_label.setStyleSheet(self.headers_stylesheet)
                self.widgets["labels"].append(self.account_label)

                self.account_label = QLabel(self)
                self.account_label.move(lastThirty_move_x, lastThirty_move_y + self.convToRectHeight(40))
                lastThirty_move_y += self.convToRectHeight(40)
                self.account_label.resize(self.convToRectWidth(130), self.convToRectHeight(40))
                self.account_label.setText(str(gamesThirty) + " Games")
                self.account_label.setFont(QFont('AnyStyle', self.font_size))
                self.account_label.setStyleSheet(self.headers_stylesheet)
                self.widgets["labels"].append(self.account_label)

                self.account_label = QLabel(self)
                self.account_label.move(hoursTotal_move_x, hoursTotal_move_y + self.convToRectHeight(40))
                hoursTotal_move_y += self.convToRectHeight(40)
                self.account_label.resize(self.convToRectWidth(160), self.convToRectHeight(40))
                self.account_label.setText(str(hours))
                self.account_label.setFont(QFont('AnyStyle', self.font_size))
                self.account_label.setStyleSheet(self.headers_stylesheet)
                self.widgets["labels"].append(self.account_label)

                self.account_button = QPushButton(self)
                self.account_button.setCursor(QCursor(Qt.PointingHandCursor))
                self.account_button.setStyleSheet(self.button_stylesheet)
                self.account_button.setCheckable(True)
                self.account_button.move(account_button_move_x, account_button_move_y + self.convToRectHeight(40))
                account_button_move_y += self.convToRectHeight(40)
                self.account_button.resize(self.convToRectWidth(110),self.convToRectHeight(40))
                self.account_button.setText("Select")
                self.account_button.setObjectName(str(pkID))
                self.account_button.setFont(QFont('AnyStyle', self.font_size))
                self.account_button.clicked.connect(self.select_button_clicked)
                self.widgets["buttons"].append(self.account_button)


#------------------------------------------------------------------------------------------------------
# Defining actions of widgets

    #Defining button actions
    # 'account manager' button and related buttons
    def acc_man_button_clicked(self):
        # 'account manager' button actions
        self.hide_widgets()
        self.isPasswordCheckBoxChecked = False
        self.current_window = "account manager"
        self.comboBoxRegion = ""
        self.QlineEditSumName = ""
        self.QlineEditUsername = ""
        self.QlineEditPassword = ""
        self.GUI()
        self.set_geometry()
        self.show_widgets()

    def select_button_clicked(self, pkID):
        # 'select' button actions
        pkID = self.sender()
        for value in self.widgets['buttons']:
            if value != pkID:
                value.setChecked(False)
        self.update()
        self.selected_pkID = pkID.objectName()

    # 'add account' button and related buttons
    def add_acc_button_clicked(self):
        # 'add account' button actions
        self.hide_widgets()
        self.isPasswordCheckBoxChecked = False
        self.current_window = "add account"
        self.GUI()
        self.set_geometry()
        self.show_widgets()
    
    def subm_acc_button_clicked(self):
        # 'submit account' button actions
        if self.current_window == "add account":
            self.hide_widgets()

            self.current_window = "account manager"
            self.collecting_data = True

            self.comboBoxRegion = ""
            self.QlineEditSumName = ""
            self.QlineEditUsername = ""
            self.QlineEditPassword = ""
            self.isPasswordCheckBoxChecked = False

            region = self.region_comboBox.currentText()
            summonername = self.summoner_name.text()
            username = self.username.text()
            password = self.password.text()

            
            if summonername != "" and username != "" and password != "":
                dbHandler.add_account(region, summonername, username, password)
                
                pkID, region, sumName, username, password = dbHandler.get_last_account()

                tempAccountList = [(pkID, region, sumName, username, password)]

                self.accounts.append((pkID, region, sumName, username, password))

                thread = Thread(target=self.fetch_account_data, args=(tempAccountList, "single",))
                thread.start()

                upWindow = Thread(target=self.updateWindowThread)
                upWindow.start()

            self.GUI()
            self.set_geometry()
            self.show_widgets()
        
        elif self.current_window == "edit":
            self.hide_widgets()

            self.current_window = "account manager"

            self.comboBoxRegion = ""
            self.QlineEditSumName = ""
            self.QlineEditUsername = ""
            self.QlineEditPassword = ""
            self.isPasswordCheckBoxChecked = False

            region = self.region_comboBox.currentText()
            summonername = self.summoner_name.text()
            username = self.username.text()
            password = self.password.text()


            if region != "Region":
                dbHandler.edit_account(edit=region, column="region", pkID=self.selected_pkID)
            if summonername != "":
                dbHandler.edit_account(edit=summonername, column="sumName", pkID=self.selected_pkID)
            if username != "":
                dbHandler.edit_account(edit=username, column="username", pkID=self.selected_pkID)
            if password != "":
                dbHandler.edit_account(edit=password, column="password", pkID=self.selected_pkID)

            if region != "Region" or summonername != "" or username != "" or password != "":
                pkID, region, sumName, username, password = dbHandler.get_account(self.selected_pkID)
                tempAccountList = [(pkID, region, sumName, username, password)]

                counter = 0
                for account in self.accounts:
                    if account[0] == pkID:
                        self.accounts[counter] = (pkID, region, sumName, username, password)
                        break
                    counter += 1

                thread = Thread(target=self.fetch_account_data, args=(tempAccountList, "single_edit",))
                thread.start()

            self.GUI()
            self.set_geometry()
            self.show_widgets()

    # 'login' button and related buttons
    def login_button_clicked(self):
        # 'login' button actions
        pkID, region, sumName, username, password = dbHandler.get_account(self.selected_pkID)
        self.selected_username = username
        self.selected_password = password
        login_thread = Thread(target=self.login_clicked)
        login_thread.start()

    # 'delete' button and related buttons
    def delete_button_clicked(self):
        # 'delete' button actions
        if self.collecting_data:
            self.pop_up_box("delete")

        else:
            self.hide_widgets()

            counter = 0
            for account in self.accounts:
                pkID, region, sumName, username, password = account
                if pkID == int(self.selected_pkID):
                    del self.summoner_data[counter]
                    del self.accounts[counter]
                    break
                counter += 1

            dbHandler.delete_account(self.selected_pkID)

            self.selected_pkID = 1
            self.GUI()
            self.set_geometry()
            self.show_widgets()

    # 'info' button and related buttons
    def info_button_clicked(self):
        # 'info' button actions
        self.hide_widgets()
        self.current_window = "info"
        self.GUI()
        self.set_geometry()
        self.show_widgets()

    # 'edit' button and related buttons
    def edit_button_clicked(self):
        # 'edit' button actions
        self.hide_widgets()
        self.current_window = "edit"
        self.GUI()
        self.set_geometry()
        self.show_widgets()

    # 'champions' button and related buttons
    def champions_button_clicked(self):
        # 'champions' button actions
        self.hide_widgets()
        self.current_window = "champions"
        self.GUI()
        self.set_geometry()
        self.show_widgets()


    # Checkbox actions
    def checkBox(self):
        if self.current_window == "add account":
            if not self.isPasswordCheckBoxChecked:
                self.isPasswordCheckBoxChecked = True
                self.comboBoxRegion = self.region_comboBox.currentText()
                self.QlineEditSumName = self.summoner_name.text()
                self.QlineEditUsername = self.username.text()
                self.QlineEditPassword = self.password.text()
                self.hide_widgets()
                self.GUI()
                self.set_geometry()
                self.show_widgets()
            else:
                self.isPasswordCheckBoxChecked = False
                self.comboBoxRegion = self.region_comboBox.currentText()
                self.QlineEditSumName = self.summoner_name.text()
                self.QlineEditUsername = self.username.text()
                self.QlineEditPassword = self.password.text()
                self.hide_widgets()
                self.GUI()
                self.set_geometry()
                self.show_widgets()

        elif self.current_window == "edit":
            if not self.isPasswordCheckBoxChecked:
                self.isPasswordCheckBoxChecked = True
                self.comboBoxRegion = self.region_comboBox.currentText()
                self.QlineEditSumName = self.summoner_name.text()
                self.QlineEditUsername = self.username.text()
                self.QlineEditPassword = self.password.text()
                self.hide_widgets()
                self.GUI()
                self.set_geometry()
                self.show_widgets()
            else:
                self.isPasswordCheckBoxChecked = False
                self.comboBoxRegion = self.region_comboBox.currentText()
                self.QlineEditSumName = self.summoner_name.text()
                self.QlineEditUsername = self.username.text()
                self.QlineEditPassword = self.password.text()
                self.hide_widgets()
                self.GUI()
                self.set_geometry()
                self.show_widgets()

        elif self.current_window == "info":
            if not self.isPasswordCheckBoxChecked:
                self.isPasswordCheckBoxChecked = True
                self.QlineEditUsername = self.username.text()
                self.QlineEditPassword = self.password.text()
                self.hide_widgets()
                self.GUI()
                self.set_geometry()
                self.show_widgets()
            else:
                self.isPasswordCheckBoxChecked = False
                self.QlineEditUsername = self.username.text()
                self.QlineEditPassword = self.password.text()
                self.hide_widgets()
                self.GUI()
                self.set_geometry()
                self.show_widgets()

#------------------------------------------------------------------------------------------------------
# Other funcs
    # Simulate press of account manager button
    def updateWindow(self):
        self.acc_man_button.click()
    
#-----------------------------------------------------------------------------------------------------
# Threading funcs
    # Fetch summoner data and append to self.summoner_data list
    def fetch_account_data(self, liste, what):
        if what == "all":
            for account in liste:
                try:
                    pkID, region, sumName, username, password = account

                    LOG_URL = "https://www.leagueofgraphs.com/summoner/"
                    WOL_URL = "https://wol.gg/stats/"
                    HEADERS = {'User-Agent': 'My User Agent 1.0'}

                    url = f"{LOG_URL}{str.lower(region)}/{sumName}/last-30-days"

                    response = requests.get(url, headers=HEADERS)

                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    level = int(str(str.split(soup.find(class_="bannerSubtitle").text.strip(), "-")[0])[5:])
                    rank = str(soup.find(class_="leagueTier").text.strip())
                    lp = soup.find(class_="leaguePoints").text.strip()
                    rank = rank + " - " + lp + " LP"
                    gamesThirty = int(soup.find(class_="summonerProfileQueuesTabs tabsContainer").find(class_="tabs-content").find("div", { "data-tab-id" : "championsData-all-queues" }).find(class_="pie-chart small").text.strip())
                    
                    url = f"{WOL_URL}{str.lower(region)}/{sumName}/"

                    response = requests.get(url, headers=HEADERS)

                    soup = BeautifulSoup(response.content, 'html.parser')

                    time_played_minutes = soup.find(id="time-minutes")
                    time_played_minutes = "".join(filter(str.isdigit, time_played_minutes.text.strip()))
                    minutes = int(time_played_minutes)
                    hours = round(minutes/60)
                    
                    self.summoner_data.append((level, rank, gamesThirty, hours))
                except:
                    self.summoner_data.append(("No data", "No data", "No data", "No data"))
        
        elif what == "single":
            done = False
            while not done:
                if not self.loading_all_summoner_data:
                    if len(self.accounts) != len(self.summoner_data): 
                        for account in liste:
                            try:
                                pkID, region, sumName, username, password = account

                                LOG_URL = "https://www.leagueofgraphs.com/summoner/"
                                WOL_URL = "https://wol.gg/stats/"
                                HEADERS = {'User-Agent': 'My User Agent 1.0'}

                                url = f"{LOG_URL}{str.lower(region)}/{sumName}/last-30-days"

                                response = requests.get(url, headers=HEADERS)

                                soup = BeautifulSoup(response.content, 'html.parser')
                                
                                level = int(str(str.split(soup.find(class_="bannerSubtitle").text.strip(), "-")[0])[5:])
                                rank = str(soup.find(class_="leagueTier").text.strip())
                                lp = soup.find(class_="leaguePoints").text.strip()
                                rank = rank + " - " + lp + " LP"
                                gamesThirty = int(soup.find(class_="summonerProfileQueuesTabs tabsContainer").find(class_="tabs-content").find("div", { "data-tab-id" : "championsData-all-queues" }).find(class_="pie-chart small").text.strip())
                                
                                url = f"{WOL_URL}{str.lower(region)}/{sumName}/"

                                response = requests.get(url, headers=HEADERS)


                                soup = BeautifulSoup(response.content, 'html.parser')

                                time_played_minutes = soup.find(id="time-minutes")
                                time_played_minutes = "".join(filter(str.isdigit, time_played_minutes.text.strip()))
                                minutes = int(time_played_minutes)
                                hours = round(minutes/60)
                                
                                self.summoner_data.append((level, rank, gamesThirty, hours))
                                done = True

                            except:
                                self.summoner_data.append(("No data", "No data", "No data", "No data"))
                                done = True
                    else:
                        done = True
                else:
                    sleep(1)

        elif what == "single_edit":
            done = False
            self.collecting_data = True
            while not done:
                if not self.loading_all_summoner_data:
                    if len(self.accounts) == len(self.summoner_data): 
                        for account in liste:
                            try:
                                pkID, region, sumName, username, password = account

                                LOG_URL = "https://www.leagueofgraphs.com/summoner/"
                                WOL_URL = "https://wol.gg/stats/"
                                HEADERS = {'User-Agent': 'My User Agent 1.0'}

                                url = f"{LOG_URL}{str.lower(region)}/{sumName}/last-30-days"

                                response = requests.get(url, headers=HEADERS)

                                soup = BeautifulSoup(response.content, 'html.parser')
                                
                                level = int(str(str.split(soup.find(class_="bannerSubtitle").text.strip(), "-")[0])[5:])
                                rank = str(soup.find(class_="leagueTier").text.strip())
                                lp = soup.find(class_="leaguePoints").text.strip()
                                rank = rank + " - " + lp + " LP"
                                gamesThirty = int(soup.find(class_="summonerProfileQueuesTabs tabsContainer").find(class_="tabs-content").find("div", { "data-tab-id" : "championsData-all-queues" }).find(class_="pie-chart small").text.strip())
                                
                                url = f"{WOL_URL}{str.lower(region)}/{sumName}/"

                                response = requests.get(url, headers=HEADERS)


                                soup = BeautifulSoup(response.content, 'html.parser')

                                time_played_minutes = soup.find(id="time-minutes")
                                time_played_minutes = "".join(filter(str.isdigit, time_played_minutes.text.strip()))
                                minutes = int(time_played_minutes)
                                hours = round(minutes/60)

                                summoner_data = (level, rank, gamesThirty, hours)

                                counter = 0
                                for account in self.accounts:
                                    if account[0] == pkID:
                                        self.summoner_data[counter] = summoner_data
                                        break
                                    counter += 1

                                done = True

                                done2 = False
                                while not done2:
                                    if self.current_window != "account manager":
                                        self.collecting_data = False
                                        self.loading_all_summoner_data = False
                                        done2 = True
                                    else:
                                        self.collecting_data = False
                                        self.loading_all_summoner_data = False
                                        self.updateWindow()
                                        done2 = True

                            except:
                                pkID, region, sumName, username, password = account
                                counter = 0
                                for account in self.accounts:
                                    if account[0] == pkID:
                                        self.summoner_data[counter] = ("No data", "No data", "No data", "No data")
                                        break
                                    counter += 1
                                done = True

                                done2 = False
                                while not done2:
                                    if self.current_window != "account manager":
                                        self.collecting_data = False
                                        self.loading_all_summoner_data = False
                                        done2 = True
                                    else:
                                        self.collecting_data = False
                                        self.loading_all_summoner_data = False
                                        self.updateWindow()
                                        done2 = True
                    else:
                        done = True
                else:
                    sleep(1)

    # Update window when all sum data has been fetched
    def updateWindowThread(self):
        done = False
        while not done:
            if len(self.accounts) != len(self.summoner_data):
                sleep(0.25)
            else:
                if self.current_window != "account manager":
                    self.collecting_data = False
                    self.loading_all_summoner_data = False
                    done = True
                else:
                    self.collecting_data = False
                    self.loading_all_summoner_data = False
                    self.updateWindow()
                    done = True

    # Login when pressing login
    def login_clicked(self):
        ready = False
        closed = False
        keyboard = Controller()

        if "LeagueClientUx.exe" in (p.name() for p in psutil.process_iter()):
            os.system("TASKKILL /F /IM LeagueClientUx.exe")
            sleep(9)
        try:
            subprocess.call(["C:\Riot Games\League of Legends\LeagueClient.exe"])
        except:
            subprocess.call(["E:\Riot Games\League of Legends\LeagueClient.exe"])

        while not ready:
            if "RiotClientUx.exe" in (p.name() for p in psutil.process_iter()):
                sleep(3)
                ready = True
            else:
                sleep(0.25)

        keyboard.type(self.selected_username)
        keyboard.press(Key.tab)
        keyboard.release(Key.tab)
        sleep(0.15)
        keyboard.type(self.selected_password)
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
        sleep(7)

        while not closed:
            if "LeagueClientUx.exe" in (p.name() for p in psutil.process_iter()):
                if "RiotClientUx.exe" in (p.name() for p in psutil.process_iter()):
                    try:
                        os.system("TASKKILL /F /IM RiotClientUX.exe")
                        closed = True
                    except:
                        closed = True
                else:
                    closed = True
            else:
                closed = True
                
#------------------------------------------------------------------------------------------------------
#Set geometry func
    def set_geometry(self):
    # Geometry for 'Account Manager'
        if self.current_window == "account manager":
            self.xpos, self.ypos, self.width, self.height = self.geometry().getRect() 
            self.setGeometry(self.xpos, self.ypos, self.acc_man_width, self.acc_man_height)
            self.setFixedWidth(self.acc_man_width)
            self.setFixedHeight(self.acc_man_height)
    # Geometry for 'Add Account'
        elif self.current_window == "add account":
            self.xpos, self.ypos, self.width, self.height = self.geometry().getRect()   
            self.setGeometry(self.xpos, self.ypos, self.add_acc_width, self.add_acc_height)
            self.setFixedWidth(self.add_acc_width)
            self.setFixedHeight(self.add_acc_height)
    # Geometry for 'Info'
        elif self.current_window == "info":
            self.xpos, self.ypos, self.width, self.height = self.geometry().getRect() 
            self.setGeometry(self.xpos, self.ypos, self.info_width, self.info_height)
            self.setFixedWidth(self.info_width)
            self.setFixedHeight(self.info_height)
    # Geometry for 'Edit'
        elif self.current_window == "edit":
            self.xpos, self.ypos, self.width, self.height = self.geometry().getRect() 
            self.setGeometry(self.xpos, self.ypos, self.edit_width, self.edit_height)
            self.setFixedWidth(self.edit_width)
            self.setFixedHeight(self.edit_height)
    # Geometry for 'Champions'
        elif self.current_window == "champions":
            self.xpos, self.ypos, self.width, self.height = self.geometry().getRect() 
            self.setGeometry(self.xpos, self.ypos, self.champions_width, self.champions_height)
            self.setFixedWidth(self.champions_width)
            self.setFixedHeight(self.champions_height)

#------------------------------------------------------------------------------------------------------
# Scaling of sizes/positioning for different screen resolutions

    #Scaling of widths for different solutions
    def convToRectWidth(self, value):
        if str(self.screen_size) == "PyQt5.QtCore.QSize(2560, 1440)":
            new_value = (value / 2560)
            end_value = (int(rect.width()) * new_value)
            return math.ceil(end_value)

        elif str(self.screen_size) == "PyQt5.QtCore.QSize(1920, 1080)":
            self.font_size = 10
            new_value = (value / 2560)
            end_value = (int(rect.width()) * new_value)
            end_end_value = (end_value * 1.5)
            return math.ceil(end_end_value)
            
    #Scaling of heights for different solutions
    def convToRectHeight(self, value):
        if str(self.screen_size) == "PyQt5.QtCore.QSize(2560, 1440)":
            new_value = (value / 1400)
            end_value = (int(rect.height()) * new_value)
            return math.ceil(end_value)

        elif str(self.screen_size) == "PyQt5.QtCore.QSize(1920, 1080)":
            self.font_size = 10
            new_value = (value / 1400)
            end_value = (int(rect.height()) * new_value)
            end_end_value = (end_value * 1.5)
            return math.ceil(end_end_value)

    #Scaling of start width position for window
    def convToRectXpos(self, value):
        if str(self.screen_size) == "PyQt5.QtCore.QSize(2560, 1440)":
            new_value = (value / 2560)
            end_value = (int(rect.width()) * new_value)
            return math.ceil(end_value)

        elif str(self.screen_size) == "PyQt5.QtCore.QSize(1920, 1080)":            
            new_value = (value / 2560)
            end_value = (int(rect.width()) * new_value)
            return math.ceil(end_value)

    #Scaling of start height position for window
    def convToRectYpos(self, value):
        if str(self.screen_size) == "PyQt5.QtCore.QSize(2560, 1440)":
            new_value = (value / 1400)
            end_value = (int(rect.height()) * new_value)
            return math.ceil(end_value)        

        elif str(self.screen_size) == "PyQt5.QtCore.QSize(1920, 1080)":
            new_value = (value / 1400)
            end_value = (int(rect.height()) * new_value)
            return math.ceil(end_value)

#------------------------------------------------------------------------------------------------------
# Clear widgets func
    def hide_widgets(self):
        for widget in self.widgets:
            if self.widgets[widget] != []:
                for i in range(-1, len(self.widgets[widget])): 
                    self.widgets[widget][i].hide() 
            for i in range(0, len(self.widgets[widget])):
                self.widgets[widget].pop()
# Show widgets func
    def show_widgets(self):
        for widget in self.widgets:
            if self.widgets[widget] != []:
                for i in range(-1, len(self.widgets[widget])): 
                    self.widgets[widget][i].show()

#------------------------------------------------------------------------------------------------------
#Main func to run program
def window():
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())