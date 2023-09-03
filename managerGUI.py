from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from database import *
from threading import Thread
from bs4 import BeautifulSoup
from time import sleep
import sys, requests, math, subprocess, psutil, os, webbrowser
from pywinauto import Application, findwindows
from pywinauto.uia_defines import IUIA


LOG_URL = "https://www.leagueofgraphs.com/summoner/"
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}


class MyWindow(QWidget):
    def __init__(self):
        super(MyWindow, self).__init__()

        self.screen = QGuiApplication.primaryScreen()
        self.rect = self.screen.availableGeometry()
        # Get screen size
        self.screen_size = self.screen.size()
        # size of 'account manager' window
        self.acc_man_width = (self.convToRectWidth(965))
        self.acc_man_height = (self.convToRectHeight(120) + (len(dbHandler.get_accounts()) * (self.convToRectHeight(40))))
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
        self.champions_width = (self.convToRectWidth(965))
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
        self.accounts = {}
        # selected row tracker
        self.selected_pkID = 1
        # username belonging to selected selected_pkiD
        self.selected_username = ""
        # password belonging to selected selected_pkiD
        self.selected_password = ""
        # summoner name, region, username, password stored for checkbox action
        self.comboBoxRegion = ""
        self.QlineEditSumName = ""
        self.QlineEditUsername = ""
        self.QlineEditPassword = ""
        # initialize window
        self.setWindowIcon(QIcon("./account_man_icon_2.png"))
        self.setGeometry(self.xpos, self.ypos, self.acc_man_width, self.acc_man_height)
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
        self.update_accounts()
        self.fetch_account_data()
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
                self.collecting_data_label.move(self.convToRectWidth(845), self.convToRectHeight(75))
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
            self.acc_man_button.resize(self.convToRectWidth(180), self.convToRectHeight(40))
            self.acc_man_button.move(self.convToRectWidth(65), self.convToRectHeight(15))
            self.acc_man_button.setText("Account manager")
            self.acc_man_button.setFont(QFont('AnyStyle', self.font_size))
            self.acc_man_button.clicked.connect(self.acc_man_button_clicked)
            self.widgets["buttons"].append(self.acc_man_button)

    # Add account button and related buttons
        elif button == "add account":
            self.add_acc_button = QPushButton(self)
            self.add_acc_button.setCursor(QCursor(Qt.PointingHandCursor))
            self.add_acc_button.setStyleSheet(self.button_stylesheet)
            self.add_acc_button.resize(self.convToRectWidth(180), self.convToRectHeight(40))
            self.add_acc_button.move(self.convToRectWidth(255), self.convToRectHeight(15))
            self.add_acc_button.setText("Add new account")
            self.add_acc_button.setFont(QFont('AnyStyle', self.font_size))
            self.add_acc_button.clicked.connect(self.add_acc_button_clicked)
            self.widgets["buttons"].append(self.add_acc_button)

        elif button == "submit account":
            if self.current_window == "add account":
                self.subm_acc_button = QPushButton(self)
                self.subm_acc_button.setCursor(QCursor(Qt.PointingHandCursor))
                self.subm_acc_button.setStyleSheet(self.button_stylesheet)
                self.subm_acc_button.resize(self.convToRectWidth(170),self.convToRectHeight(40))
                self.subm_acc_button.move(self.convToRectWidth(130), self.convToRectHeight(335))
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
            self.login_button.move(self.convToRectWidth(445), self.convToRectHeight(15))
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
            self.info_button.move(self.convToRectWidth(555), self.convToRectHeight(15))
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
            self.edit_button.move(self.convToRectWidth(635), self.convToRectHeight(15))
            self.edit_button.resize(self.convToRectWidth(90), self.convToRectHeight(40))
            self.edit_button.setText("Edit")
            self.edit_button.setFont(QFont('AnyStyle', self.font_size))
            self.edit_button.clicked.connect(self.edit_button_clicked)
            self.widgets["buttons"].append(self.edit_button)

    # Delete button    
        elif button == "delete":
            self.delete_button = QPushButton(self)
            self.delete_button.setCursor(QCursor(Qt.PointingHandCursor))
            self.delete_button.setStyleSheet(self.button_stylesheet)
            self.delete_button.move(self.convToRectWidth(735), self.convToRectHeight(15))
            self.delete_button.resize(self.convToRectWidth(100), self.convToRectHeight(40))
            self.delete_button.setText("Delete")
            self.delete_button.setFont(QFont('AnyStyle', self.font_size))
            self.delete_button.clicked.connect(self.delete_button_clicked)
            self.widgets["buttons"].append(self.delete_button)

    # Champions button and related buttons    
        elif button == "champions":
            self.champions_button = QPushButton(self)
            self.champions_button.setCursor(QCursor(Qt.PointingHandCursor))
            self.champions_button.setStyleSheet(self.button_stylesheet)
            self.champions_button.move(self.convToRectWidth(845), self.convToRectHeight(15))
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
        self.name_label.resize(self.convToRectWidth(180), self.convToRectHeight(40))
        self.name_label.setText("Name")
        self.name_label.setFont(QFont('AnyStyle', self.font_size))
        self.name_label.setStyleSheet(self.headers_stylesheet)
        self.widgets["labels"].append(self.name_label)
        
        self.rank_label = QLabel(self)
        self.rank_label.move(self.convToRectWidth(255), self.convToRectHeight(65))
        self.rank_label.resize(self.convToRectWidth(180), self.convToRectHeight(40))
        self.rank_label.setText("Rank")
        self.rank_label.setFont(QFont('AnyStyle', self.font_size))
        self.rank_label.setStyleSheet(self.headers_stylesheet)
        self.widgets["labels"].append(self.rank_label)

        self.region_label = QLabel(self)
        self.region_label.move(self.convToRectWidth(445), self.convToRectHeight(65))
        self.region_label.resize(self.convToRectWidth(100), self.convToRectHeight(40))
        self.region_label.setText("Region")
        self.region_label.setFont(QFont('AnyStyle', self.font_size))
        self.region_label.setStyleSheet(self.headers_stylesheet)
        self.widgets["labels"].append(self.region_label)
       
        self.level_label = QLabel(self)
        self.level_label.move(self.convToRectWidth(555), self.convToRectHeight(65))
        self.level_label.resize(self.convToRectWidth(70), self.convToRectHeight(40))
        self.level_label.setText("Level")
        self.level_label.setFont(QFont('AnyStyle', self.font_size))
        self.level_label.setStyleSheet(self.headers_stylesheet)
        self.widgets["labels"].append(self.level_label)        


    # list accounts in db
    def accountsList(self):
        id_move_x, id_move_y = self.convToRectWidth(15), self.convToRectHeight(65)
        name_move_x, name_move_y = self.convToRectWidth(65), self.convToRectHeight(65)
        rank_move_x, rank_move_y = self.convToRectWidth(255), self.convToRectHeight(65)
        region_move_x, region_move_y = self.convToRectWidth(445), self.convToRectHeight(65)
        level_move_x, level_move_y = self.convToRectWidth(555), self.convToRectHeight(65)
        opgg_button_move_x, opgg_button_move_y = self.convToRectWidth(735), self.convToRectHeight(65)
        account_button_move_x, account_button_move_y = self.convToRectWidth(845), self.convToRectHeight(65)

        for pkID, sumData in self.accounts.items():
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
            self.account_label.resize(self.convToRectWidth(180), self.convToRectHeight(40))
            self.account_label.setText(str(sumData.get("summoner_name")))
            self.account_label.setFont(QFont('AnyStyle', self.font_size))
            self.account_label.setStyleSheet(self.headers_stylesheet)
            self.widgets["labels"].append(self.account_label)

            self.account_label = QLabel(self)
            self.account_label.move(rank_move_x, rank_move_y + self.convToRectHeight(40))
            rank_move_y += self.convToRectHeight(40)
            self.account_label.resize(self.convToRectWidth(180), self.convToRectHeight(40))
            self.account_label.setText(str(sumData.get("rank")))
            self.account_label.setFont(QFont('AnyStyle', self.font_size))
            self.account_label.setStyleSheet(self.headers_stylesheet)
            self.widgets["labels"].append(self.account_label)

            self.account_label = QLabel(self)
            self.account_label.move(region_move_x, region_move_y + self.convToRectHeight(40))
            region_move_y += self.convToRectHeight(40)
            self.account_label.resize(self.convToRectWidth(100), self.convToRectHeight(40))
            self.account_label.setText(sumData.get("region"))
            self.account_label.setFont(QFont('AnyStyle', self.font_size))
            self.account_label.setStyleSheet(self.headers_stylesheet)
            self.widgets["labels"].append(self.account_label)

            self.account_label = QLabel(self)
            self.account_label.move(level_move_x, level_move_y + self.convToRectHeight(40))
            level_move_y += self.convToRectHeight(40)
            self.account_label.resize(self.convToRectWidth(70), self.convToRectHeight(40))
            self.account_label.setText(str(sumData.get("level")))
            self.account_label.setFont(QFont('AnyStyle', self.font_size))
            self.account_label.setStyleSheet(self.headers_stylesheet)
            self.widgets["labels"].append(self.account_label)

            self.opgg_button = QPushButton(self)
            self.opgg_button.setCursor(QCursor(Qt.PointingHandCursor))
            self.opgg_button.setStyleSheet(self.button_stylesheet)
            self.opgg_button.move(opgg_button_move_x, opgg_button_move_y + self.convToRectHeight(40))
            opgg_button_move_y += self.convToRectHeight(40)
            self.opgg_button.resize(self.convToRectWidth(100),self.convToRectHeight(40))
            self.opgg_button.setText("OP.GG")
            self.opgg_button.setObjectName(f"{sumData.get('region')},{sumData.get('summoner_name')}")
            self.opgg_button.setFont(QFont('AnyStyle', self.font_size))
            self.opgg_button.clicked.connect(self.opgg_button_clicked)
            self.widgets["buttons"].append(self.opgg_button)

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

    def opgg_button_clicked(self, sum_name):
        region = self.sender().objectName().split(",")[0]
        sum_name = self.sender().objectName().split(",")[1]
        webbrowser.open(f"https://www.op.gg/summoners/{region}/{sum_name}")

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

                self.accounts[pkID] = {
                    "summoner_name": sumName,
                    "region": region,
                    "username": username,
                    "password": password,
                    "level": "",
                    "rank": "",
                }

                self.fetch_account_data()

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

                self.accounts[pkID] = {
                    "summoner_name": sumName,
                    "region": region,
                    "username": username,
                    "password": password,
                    "level": "",
                    "rank": "",
                }

                self.fetch_account_data()

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

            del self.accounts[int(self.selected_pkID)]

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

    
    def update_accounts(self):
        if not self.accounts:
            for account in dbHandler.get_accounts():
                pkID, region, sumName, username, password = account
                self.accounts[pkID] = {
                    "summoner_name": sumName,
                    "region": region,
                    "username": username,
                    "password": password,
                    "level": "",
                    "rank": "",
                }

    
#-----------------------------------------------------------------------------------------------------
# Threading funcs
    # Fetch summoner data and append to self.summoner_data list
    def fetch_account_data(self):    
        self.collecting_data = True    
        threads = []  # List to hold all threads
        finished_threads = 0  # Counter for finished threads

        def callback():
            nonlocal finished_threads
            finished_threads += 1
            if finished_threads == len(threads):
                self.collecting_data = False
                self.updateWindow()


        for pkID, sumData in self.accounts.items():
            thread = Thread(target=self.scrape_account, args=(pkID, sumData, callback))
            thread.start()
            threads.append(thread)  # Add the thread to the list


    def scrape_account(self, pkID: int, sumData: dict, callback: callable) -> None:
        url = f"{LOG_URL}{str.lower(sumData.get('region'))}/{sumData.get('summoner_name')}"
        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.content, 'html.parser')
        level = int(soup.find("div", class_="bannerSubtitle").text.strip().split()[1])
        try:
            rank = soup.find("div", class_="leagueTier").text.strip()
        except:
            rank = "Unranked"
        if "Master" in rank or "Grandmaster" in rank or "Challenger" in rank:
            rank, lp, lp_string = rank.split()
            rank = f"{rank} - {lp} {lp_string}"
        elif "Diamond" in rank:
            rank, tier, lp, lp_string = rank.split()
            rank = f"{rank} {tier} - {lp} {lp_string}"
        elif rank != "Unranked":
            try:
                lp = soup.find("span", class_="leaguePoints").text.strip()
                rank = rank + " - " + lp + " LP"
            except:
                pass

        self.accounts[pkID]["level"] = level
        self.accounts[pkID]["rank"] = rank

        callback()


    # Login when pressing login
    def login_clicked(self):
        ready = False
        closed = False
        process_killed = False

        kill_processes = ["LeagueClient.exe", "LeagueClientUx.exe", "RiotClientServices.exe"]

        for process in kill_processes:
            if process in (p.name() for p in psutil.process_iter()):
                os.system(f"TASKKILL /F /IM {process}")
                process_killed = True

        if process_killed:
            sleep(6)
        
        try:
            subprocess.call(["C:\Riot Games\League of Legends\LeagueClient.exe"])
        except:
            subprocess.call(["E:\Riot Games\League of Legends\LeagueClient.exe"])

        while not ready:
            if not "RiotClientUx.exe" in (p.name() for p in psutil.process_iter()):
                sleep(0.25)
            else:
                sleep(3)
                ready = True

        windows = findwindows.find_elements(class_name="RCLIENT")

        window_handle = windows[0].handle

        app = Application(backend="uia").connect(handle=window_handle)

        main_window = app.window(handle=window_handle)

        chrome_render_widget_host_hwnd = main_window.child_window(class_name="Chrome_RenderWidgetHostHWND")

        username_field = chrome_render_widget_host_hwnd.child_window(control_type=IUIA().known_control_types['Edit'], auto_id="username")
        password_field = chrome_render_widget_host_hwnd.child_window(control_type=IUIA().known_control_types['Edit'], auto_id="password")
        
        username_field.wait("visible", timeout=15)
        password_field.wait("visible", timeout=15)

        password_field.set_text(self.selected_password)
        username_field.set_text(self.selected_username)
        
        sign_in_button = chrome_render_widget_host_hwnd.child_window(control_type=IUIA().known_control_types['Button'], title="Sign in")
        sign_in_button.click_input()


        while not closed:
            if not "LeagueClientUx.exe" in (p.name() for p in psutil.process_iter()):
                sleep(1)
            else:
                if "RiotClientUx.exe" in (p.name() for p in psutil.process_iter()):
                    try:
                        os.system("TASKKILL /F /IM RiotClientUX.exe")
                        closed = True
                    except:
                        closed = True
                else:
                    closed = True
                
#------------------------------------------------------------------------------------------------------
#Set geometry func
    def set_geometry(self):
    # Geometry for 'Account Manager'
        if self.current_window == "account manager":
            self.xpos, self.ypos, self.width, self.height = self.geometry().getRect() 
            self.setGeometry(
                self.xpos,
                self.ypos,
                self.acc_man_width,
                self.convToRectHeight(120) + (len(dbHandler.get_accounts()) * self.convToRectHeight(40))
            )
    # Geometry for 'Add Account'
        elif self.current_window == "add account":
            self.xpos, self.ypos, self.width, self.height = self.geometry().getRect()   
            self.setGeometry(self.xpos, self.ypos, self.add_acc_width, self.add_acc_height)
    # Geometry for 'Info'
        elif self.current_window == "info":
            self.xpos, self.ypos, self.width, self.height = self.geometry().getRect() 
            self.setGeometry(self.xpos, self.ypos, self.info_width, self.info_height)
    # Geometry for 'Edit'
        elif self.current_window == "edit":
            self.xpos, self.ypos, self.width, self.height = self.geometry().getRect() 
            self.setGeometry(self.xpos, self.ypos, self.edit_width, self.edit_height)
    # Geometry for 'Champions'
        elif self.current_window == "champions":
            self.xpos, self.ypos, self.width, self.height = self.geometry().getRect() 
            self.setGeometry(self.xpos, self.ypos, self.champions_width, self.champions_height)

#------------------------------------------------------------------------------------------------------
# Scaling of sizes/positioning for different screen resolutions

    #Scaling of widths for different solutions
    def convToRectWidth(self, value):
        if str(self.screen_size) == "PyQt5.QtCore.QSize(2560, 1440)":
            new_value = (value / 2560)
            end_value = (int(self.rect.width()) * new_value)
            return math.ceil(end_value)

        elif str(self.screen_size) == "PyQt5.QtCore.QSize(1920, 1080)":
            self.font_size = 10
            new_value = (value / 2560)
            end_value = (int(self.rect.width()) * new_value)
            end_end_value = (end_value * 1.5)
            return math.ceil(end_end_value)
            
    #Scaling of heights for different solutions
    def convToRectHeight(self, value):
        if str(self.screen_size) == "PyQt5.QtCore.QSize(2560, 1440)":
            new_value = (value / 1400)
            end_value = (int(self.rect.height()) * new_value)
            return math.ceil(end_value)

        elif str(self.screen_size) == "PyQt5.QtCore.QSize(1920, 1080)":
            self.font_size = 10
            new_value = (value / 1400)
            end_value = (int(self.rect.height()) * new_value)
            end_end_value = (end_value * 1.5)
            return math.ceil(end_end_value)

    #Scaling of start width position for window
    def convToRectXpos(self, value):
        if str(self.screen_size) == "PyQt5.QtCore.QSize(2560, 1440)":
            new_value = (value / 2560)
            end_value = (int(self.rect.width()) * new_value)
            return math.ceil(end_value)

        elif str(self.screen_size) == "PyQt5.QtCore.QSize(1920, 1080)":            
            new_value = (value / 2560)
            end_value = (int(self.rect.width()) * new_value)
            return math.ceil(end_value)

    #Scaling of start height position for window
    def convToRectYpos(self, value):
        if str(self.screen_size) == "PyQt5.QtCore.QSize(2560, 1440)":
            new_value = (value / 1400)
            end_value = (int(self.rect.height()) * new_value)
            return math.ceil(end_value)        

        elif str(self.screen_size) == "PyQt5.QtCore.QSize(1920, 1080)":
            new_value = (value / 1400)
            end_value = (int(self.rect.height()) * new_value)
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