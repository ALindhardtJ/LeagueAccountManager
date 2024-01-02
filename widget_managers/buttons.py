import webbrowser, subprocess, psutil, os
from pywinauto.uia_defines import IUIA
from pywinauto import Application, findwindows
from time import sleep, time
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QFont, QCursor
from PyQt5.QtCore import Qt
from threading import Thread
from account_manager import account_manager
from utilities.scaling_utils import ScalingUtils
from database import dbHandler, AccountManagerDB
from utilities import obj_names
from configuration_files import configuration_values



class Buttons:
    def __init__(self, parent):
        self.parent = parent
        self.button_actions = ButtonActions(parent=parent)
        self.__created_buttons = {}  # Dictionary to store created buttons

    def get_button(self, object_name):
        if object_name in self.__created_buttons:
            return self.__created_buttons[object_name]
        else:
            return None

    def add_button(self, button: QPushButton, object_name: str) -> None:
        self.__created_buttons[object_name] = button

    @property
    def created_buttons(self) -> dict:
        return self.__created_buttons
    

    def account_manager_button(self) -> dict:
        show_widget = True
        object_name = obj_names.ButtonNames.ACCOUNT_MANAGER.value
        if self.get_button(object_name=object_name):
            pass
        else:
            account_manager_button = QPushButton(self.parent)
            account_manager_button.setObjectName(object_name)
            account_manager_button.setCursor(QCursor(Qt.PointingHandCursor))
            account_manager_button.setText("Account manager")
            account_manager_button.setFont(QFont('AnyStyle', ScalingUtils.get_font_size()))
            account_manager_button.resize(ScalingUtils.width(250), ScalingUtils.height(40))
            account_manager_button.move(ScalingUtils.width(65), ScalingUtils.height(15))
            account_manager_button.clicked.connect(self.button_actions.account_manager_button_clicked)
            self.add_button(
                button=account_manager_button,
                object_name=object_name
            )
        return {"object_name":object_name, "show":show_widget}
 

    def add_new_account(self) -> dict:
        show_widget = True
        object_name = obj_names.ButtonNames.ADD_NEW_ACCOUNT.value
        if self.get_button(object_name=object_name):
            pass
        else:
            add_new_account_button = QPushButton(self.parent)
            add_new_account_button.setObjectName(object_name)
            add_new_account_button.setCursor(QCursor(Qt.PointingHandCursor))
            add_new_account_button.setText("Add new account")
            add_new_account_button.setFont(QFont('AnyStyle', ScalingUtils.get_font_size()))
            add_new_account_button.resize(ScalingUtils.width(180), ScalingUtils.height(40))
            add_new_account_button.move(ScalingUtils.width(325), ScalingUtils.height(15))
            add_new_account_button.clicked.connect(self.button_actions.add_new_account_button_clicked)
            self.add_button(add_new_account_button, object_name)
        return {"object_name":object_name, "show":show_widget}


    def app_configurations(self) -> dict:
        show_widget = True
        object_name = obj_names.ButtonNames.APP_CONFIGURATIONS.value
        if self.get_button(object_name=object_name):
            pass
        else:
            app_configurations_button = QPushButton(self.parent)
            app_configurations_button.setObjectName(object_name)
            app_configurations_button.setCursor(QCursor(Qt.PointingHandCursor))
            app_configurations_button.setFont(QFont('AnyStyle', ScalingUtils.get_font_size()))
            app_configurations_button.setText("App configurations")
            app_configurations_button.move(ScalingUtils.width(805), (ScalingUtils.height(15)))
            app_configurations_button.resize(ScalingUtils.width(220),ScalingUtils.height(40))
            app_configurations_button.clicked.connect(self.button_actions.app_configurations_clicked)
            self.add_button(app_configurations_button, object_name)
        return {"object_name":object_name, "show":show_widget}
    

    def skins_champions(self) -> dict:
        show_widget = True
        object_name = obj_names.ButtonNames.SKINS_CHAMPIONS.value
        if self.get_button(object_name=object_name):
            pass
        else:
            skins_champions_button = QPushButton(self.parent)
            skins_champions_button.setObjectName(object_name)
            skins_champions_button.setCursor(QCursor(Qt.PointingHandCursor))
            skins_champions_button.setText("Account champions/skins")
            skins_champions_button.setFont(QFont('AnyStyle', ScalingUtils.get_font_size()))
            skins_champions_button.move(ScalingUtils.width(515), ScalingUtils.height(15))
            skins_champions_button.resize(ScalingUtils.width(280),ScalingUtils.height(40))
            skins_champions_button.clicked.connect(self.button_actions.skins_champions_button_clicked)
            self.add_button(skins_champions_button, object_name)
        return {"object_name":object_name, "show":show_widget}


    def delete(self) -> dict:
        show_widget = True
        object_name = obj_names.ButtonNames.DELETE.value
        if self.get_button(object_name=object_name):
            pass
        else:
            delete_button = QPushButton(self.parent)
            delete_button.setObjectName(object_name)
            delete_button.setCursor(QCursor(Qt.PointingHandCursor))
            delete_button.setText("Delete")
            delete_button.setFont(QFont('AnyStyle', ScalingUtils.get_font_size()))
            delete_button.move(ScalingUtils.width(515), ScalingUtils.height(65))
            delete_button.resize(ScalingUtils.width(87), ScalingUtils.height(40))
            delete_button.clicked.connect(self.button_actions.delete_button_clicked)
            self.add_button(delete_button, object_name)
        return {"object_name":object_name, "show":show_widget}


    def edit(self) -> dict:
        show_widget = True
        object_name = obj_names.ButtonNames.EDIT.value
        if self.get_button(object_name=object_name):
            pass
        else:
            edit_button = QPushButton(self.parent)
            edit_button.setObjectName(object_name)
            edit_button.setCursor(QCursor(Qt.PointingHandCursor))
            edit_button.setText("Edit")
            edit_button.setFont(QFont('AnyStyle', ScalingUtils.get_font_size()))
            edit_button.move(ScalingUtils.width(612), ScalingUtils.height(65))
            edit_button.resize(ScalingUtils.width(87), ScalingUtils.height(40))
            edit_button.clicked.connect(self.button_actions.edit_button_clicked)
            self.add_button(edit_button, object_name)
        return {"object_name":object_name, "show":show_widget}


    def info(self) -> dict:
        show_widget = True
        object_name = obj_names.ButtonNames.INFO.value
        if self.get_button(object_name=object_name):
            pass
        else:
            info_button = QPushButton(self.parent)
            info_button.setObjectName(object_name)
            info_button.setCursor(QCursor(Qt.PointingHandCursor))
            info_button.setText("Info")
            info_button.setFont(QFont('AnyStyle', ScalingUtils.get_font_size()))
            info_button.move(ScalingUtils.width(709), ScalingUtils.height(65))
            info_button.resize(ScalingUtils.width(87),ScalingUtils.height(40))
            info_button.clicked.connect(self.button_actions.info_button_clicked)
            self.add_button(info_button, object_name)
        return {"object_name":object_name, "show":show_widget}


 #MISSING FIX   
    def skins_champions_champions(self) -> dict:
        show_widget = True
        object_name = obj_names.ButtonNames.CHAMPIONS.value
        if self.get_button(object_name=object_name):
            pass
        else:
            champions_button = QPushButton(self.parent)
            champions_button.setObjectName(object_name)
            champions_button.setCheckable(True)
            champions_button.setChecked(self.parent.champions_button_checked)
            champions_button.setCursor(QCursor(Qt.PointingHandCursor))
            champions_button.setText("Champions")
            champions_button.setFont(QFont('AnyStyle', ScalingUtils.get_font_size()))
            champions_button.move(ScalingUtils.width(430), ScalingUtils.height(15))
            champions_button.resize(ScalingUtils.width(180),ScalingUtils.height(40))
            champions_button.clicked.connect(self.button_actions.champions_button_clicked)
            self.add_button(champions_button, object_name)
        return {"object_name":object_name, "show":show_widget}

#MISSING FIX
    def skins_champions_skins(self) -> dict:
        show_widget = True
        object_name = obj_names.ButtonNames.SKINS.value
        if self.get_button(object_name=object_name):
            pass
        else:  
            skins_button = QPushButton(self.parent)
            skins_button.setObjectName(object_name)
            skins_button.setCheckable(True)
            skins_button.setChecked(True)
            skins_button.setChecked(self.parent.skins_button_checked)
            skins_button.setCursor(QCursor(Qt.PointingHandCursor))
            skins_button.setText("Skins")
            skins_button.setFont(QFont('AnyStyle', ScalingUtils.get_font_size()))
            skins_button.move(ScalingUtils.width(615), ScalingUtils.height(15))
            skins_button.resize(ScalingUtils.width(120),ScalingUtils.height(40))
            skins_button.clicked.connect(self.button_actions.skins_button_clicked)
            self.add_button(skins_button, object_name)
        return {"object_name":object_name, "show":show_widget}

    
    def submit_new_account(self) -> dict:
        show_widget = True
        object_name = obj_names.ButtonNames.SUBMIT_NEW_ACCOUNT.value
        if self.get_button(object_name=object_name):
            pass
        else:
            submit_new_account_button = QPushButton(self.parent)
            submit_new_account_button.setObjectName(object_name)
            submit_new_account_button.setCursor(QCursor(Qt.PointingHandCursor))
            submit_new_account_button.setText("Submit Account")
            submit_new_account_button.setFont(QFont('AnyStyle', ScalingUtils.get_font_size()))
            submit_new_account_button.resize(ScalingUtils.width(170),ScalingUtils.height(40))
            submit_new_account_button.move(ScalingUtils.width(130), ScalingUtils.height(405))
            submit_new_account_button.clicked.connect(self.button_actions.submit_new_account_button_clicked)
            self.add_button(submit_new_account_button, object_name)
        return {"object_name":object_name, "show":show_widget}


    def submit_edited_account(self) -> dict:
        show_widget = True
        object_name = obj_names.ButtonNames.SUBMIT_EDITED_ACCOUNT.value
        if self.get_button(object_name=object_name):
            pass
        else:
            submit_edited_account_button = QPushButton(self.parent)
            submit_edited_account_button.setObjectName(object_name)
            submit_edited_account_button.setCursor(QCursor(Qt.PointingHandCursor))
            submit_edited_account_button.setText("Edit Account")
            submit_edited_account_button.setFont(QFont('AnyStyle', ScalingUtils.get_font_size()))
            submit_edited_account_button.resize(ScalingUtils.width(170),ScalingUtils.height(40))
            submit_edited_account_button.move(ScalingUtils.width(130), ScalingUtils.height(405))
            submit_edited_account_button.clicked.connect(self.button_actions.submit_edited_account_button_clicked)
            self.add_button(submit_edited_account_button, object_name)
        return {"object_name":object_name, "show":show_widget}


    def login(self) -> dict:
        show_widget = True
        object_name = obj_names.ButtonNames.LOGIN.value
        if self.get_button(object_name=object_name):
            pass
        else:
            login_button = QPushButton(self.parent)
            login_button.setCheckable(True)
            login_button.setObjectName(object_name)
            login_button.setCursor(QCursor(Qt.PointingHandCursor))
            login_button.setText("Login")
            login_button.setFont(QFont('AnyStyle', ScalingUtils.get_font_size()))
            login_button.move(ScalingUtils.width(915), ScalingUtils.height(65))
            login_button.resize(ScalingUtils.width(110), ScalingUtils.height(40))
            login_button.clicked.connect(self.button_actions.login_button_clicked)
            self.add_button(login_button, object_name)
        return {"object_name":object_name, "show":show_widget}


    def collect_account_data(self) -> dict:
        show_widget = True
        object_name = obj_names.ButtonNames.COLLECT_ACCOUNT_DATA.value
        if self.get_button(object_name=object_name):
            pass
        else:
            refresh_data_button = QPushButton(self.parent)
            refresh_data_button.setCheckable(True)
            refresh_data_button.setChecked(self.parent.account_manager.collecting_data)
            refresh_data_button.setObjectName(object_name)
            refresh_data_button.setCursor(QCursor(Qt.PointingHandCursor))
            if not configuration_values.collect_data_on_startup:
                refresh_data_button.setText("Refresh all account data")
            else:
                refresh_data_button.setText("Collecting account data")
            refresh_data_button.setFont(QFont('AnyStyle', ScalingUtils.get_font_size()))
            refresh_data_button.move(ScalingUtils.width(805), ScalingUtils.height(110))
            refresh_data_button.resize(ScalingUtils.width(220),ScalingUtils.height(40))
            refresh_data_button.clicked.connect(self.button_actions.collect_account_data_button_clicked)
            refresh_data_button.setVisible(show_widget)
            self.add_button(refresh_data_button, object_name)
        return {"object_name":object_name, "show":show_widget}


    def opgg(self, account: account_manager.Account, increment: int) -> dict:
        show_widget = True
        object_name = f"{obj_names.ButtonNames.OPGG.value}_{str(account.account_id)}"
        if self.get_button(object_name=object_name):
            self.get_button(object_name=object_name).move(
                ScalingUtils.width(805), (ScalingUtils.height(115) + ScalingUtils.height(increment))
            )
        else:
            opgg_button = QPushButton(self.parent)
            opgg_button.setObjectName(object_name)
            opgg_button.setCursor(QCursor(Qt.PointingHandCursor))
            opgg_button.setText("OP.GG")
            opgg_button.setFont(QFont('AnyStyle', ScalingUtils.get_font_size()))
            opgg_button.move(ScalingUtils.width(805), (ScalingUtils.height(115) + ScalingUtils.height(increment)))
            opgg_button.resize(ScalingUtils.width(100),ScalingUtils.height(40))
            opgg_button.clicked.connect(lambda: self.button_actions.opgg_button_clicked(account))
            self.add_button(opgg_button, object_name)
        return {"object_name":object_name, "show":show_widget}
    
    
    def select_account(self, account: account_manager.Account, increment: int) -> dict:
        show_widget = True
        object_name = f"{obj_names.ButtonNames.SELECT_ACCOUNT.value}_{str(account.account_id)}"
        if self.get_button(object_name=object_name):
            self.get_button(object_name=object_name).move(
                ScalingUtils.width(915), (ScalingUtils.height(115) + ScalingUtils.height(increment))
            )
        else:
            account_button = QPushButton(self.parent)
            account_button.setObjectName(object_name)
            account_button.setCursor(QCursor(Qt.PointingHandCursor))
            account_button.setCheckable(True)
            account_button.setText("Select")
            account_button.setFont(QFont('AnyStyle', ScalingUtils.get_font_size()))

            if self.parent.account_manager.is_selected_account(account):
                account_button.setChecked(True)

            account_button.move(ScalingUtils.width(915), (ScalingUtils.height(115) + ScalingUtils.height(increment)))
            account_button.resize(ScalingUtils.width(110),ScalingUtils.height(40))
            account_button.clicked.connect(lambda: self.button_actions.select_button_clicked(account, account_button))
            self.add_button(account_button, object_name)
        return {"object_name":object_name, "show":show_widget}


    def automatic_queue_accept(self) -> dict:
        show_widget = True
        object_name = obj_names.ButtonNames.AUTOMATIC_QUEUE_ACCEPT.value
        if self.get_button(object_name=object_name):
            pass
        else:
            automatic_queue_accept_button = QPushButton(self.parent)
            automatic_queue_accept_button.setObjectName(object_name)
            automatic_queue_accept_button.setCursor(QCursor(Qt.PointingHandCursor))
            automatic_queue_accept_button.setCheckable(True)
            automatic_queue_accept_button.setFont(QFont('AnyStyle', ScalingUtils.get_font_size()))
            automatic_queue_accept_button.setText("Automatic queue accept")
            automatic_queue_accept_button.setChecked(configuration_values.automatic_queue_accept)
            automatic_queue_accept_button.move(ScalingUtils.width(65), (ScalingUtils.height(130)))
            automatic_queue_accept_button.resize(ScalingUtils.width(250),ScalingUtils.height(40))
            automatic_queue_accept_button.clicked.connect(self.button_actions.automatic_queue_accept_button_clicked)
            self.add_button(automatic_queue_accept_button, object_name)
        return {"object_name":object_name, "show":show_widget}
    

    def collect_data_on_startup(self) -> dict:
        show_widget = True
        object_name = obj_names.ButtonNames.COLLECT_DATA_ON_STARTUP.value
        if self.get_button(object_name=object_name):
            pass
        else:
            collect_data_on_startup_button = QPushButton(self.parent)
            collect_data_on_startup_button.setObjectName(object_name)
            collect_data_on_startup_button.setCursor(QCursor(Qt.PointingHandCursor))
            collect_data_on_startup_button.setCheckable(True)
            collect_data_on_startup_button.setFont(QFont('AnyStyle', ScalingUtils.get_font_size()))
            collect_data_on_startup_button.setText("Collect account data on startup")
            collect_data_on_startup_button.setChecked(configuration_values.collect_data_on_startup)
            collect_data_on_startup_button.move(ScalingUtils.width(65), (ScalingUtils.height(230)))
            collect_data_on_startup_button.resize(ScalingUtils.width(250),ScalingUtils.height(40))
            collect_data_on_startup_button.clicked.connect(self.button_actions.collect_data_on_startup_clicked)
            self.add_button(collect_data_on_startup_button, object_name)
        return {"object_name":object_name, "show":show_widget}


    def remove_account_filter(self) -> dict:
        show_widget = self.parent.account_manager.accounts_filtered
        object_name = obj_names.ButtonNames.REMOVE_ACCOUNT_FILTER.value
        if self.get_button(object_name=object_name):
            pass
        else:
            remove_account_filter_button = QPushButton(self.parent)
            remove_account_filter_button.setObjectName(object_name)
            remove_account_filter_button.setCursor(QCursor(Qt.PointingHandCursor))
            remove_account_filter_button.setText("Remove filter")
            remove_account_filter_button.setFont(QFont('AnyStyle', ScalingUtils.get_font_size()))
            remove_account_filter_button.move(ScalingUtils.width(65), ScalingUtils.height(65))
            remove_account_filter_button.resize(ScalingUtils.width(250),ScalingUtils.height(40))
            remove_account_filter_button.clicked.connect(self.button_actions.remove_account_filter_button_clicked)
            self.add_button(remove_account_filter_button, object_name)
        return {"object_name":object_name, "show":show_widget}



class ButtonActions():
    def __init__(self, parent):
        self.parent = parent

    def account_manager_button_clicked(self):
        self.parent.GUI_account_manager()
        
    def add_new_account_button_clicked(self):
        self.parent.GUI_add_account()

    def app_configurations_clicked(self):
        self.parent.GUI_app_configurations()

    def skins_champions_button_clicked(self):
        pass
        # self.parent.GUI_skins_champions()


    def delete_button_clicked(self):
        if self.parent.account_manager.selected_account is not None:
            dbHandler.delete_account(account_id=self.parent.account_manager.selected_account.account_id)
            self.parent.account_manager.delete_selected_account()
            self.parent.GUI_account_manager()
                

    def edit_button_clicked(self):
        if self.parent.account_manager.selected_account is not None:
            self.parent.GUI_edit()
            

    def info_button_clicked(self):
        if self.parent.account_manager.selected_account is not None:
            self.parent.GUI_info()

        
    def submit_new_account_button_clicked(self):
        region = self.parent.combo_boxes.get_combo_box(obj_names.ComboBoxNames.ADD_ACCOUNT_REGION.value).currentText()
        summoner_name = self.parent.line_edits.get_line_edit(obj_names.LineEditNames.ADD_ACCOUNT_SUMMONER_NAME.value).text()
        tagline = self.parent.line_edits.get_line_edit(obj_names.LineEditNames.ADD_ACCOUNT_TAGLINE.value).text()
        username = self.parent.line_edits.get_line_edit(obj_names.LineEditNames.ADD_ACCOUNT_USERNAME.value).text()
        password = self.parent.line_edits.get_line_edit(obj_names.LineEditNames.ADD_ACCOUNT_PASSWORD.value).text()

        if summoner_name != "" and tagline != "" and username != "" and password != "":
            account_id, region, tagline, summoner_name, username, password = dbHandler.add_account(
                region=region,
                tagline=tagline,
                summoner_name=summoner_name,
                username=username,
                password=password
            )
            account = self.parent.account_manager.create_account(
                account_id = account_id,
                summoner_name = summoner_name,
                region = region,
                tagline = tagline,
                username = username,
                password = password
            )
            self.parent.account_manager.fetch_account_data(account)
            self.parent.GUI_account_manager()
        
        
    def submit_edited_account_button_clicked(self):
        region = self.parent.combo_boxes.get_combo_box(obj_names.ComboBoxNames.EDIT_ACCOUNT_REGION.value).currentText()
        tagline = self.parent.line_edits.get_line_edit(obj_names.LineEditNames.EDIT_ACCOUNT_TAGLINE.value).text()
        summoner_name = self.parent.line_edits.get_line_edit(obj_names.LineEditNames.EDIT_ACCOUNT_SUMMONER_NAME.value).text()
        username = self.parent.line_edits.get_line_edit(obj_names.LineEditNames.EDIT_ACCOUNT_USERNAME.value).text()
        password = self.parent.line_edits.get_line_edit(obj_names.LineEditNames.EDIT_ACCOUNT_PASSWORD.value).text()

        dbHandler.edit_account(
            account_id=self.parent.account_manager.selected_account.account_id,
            region=region,
            tagline=tagline,
            summoner_name=summoner_name,
            username=username,
            password=password
        )
        self.parent.account_manager.edit_selected_account(
            region=region,
            tagline=tagline,
            summoner_name=summoner_name,
            username=username,
            password=password
        )
        self.parent.account_manager.fetch_account_data(self.parent.account_manager.selected_account)
        self.parent.GUI_account_manager()


#MISSING FIX
    def champions_button_clicked(self):
        if not self.parent.champions_button_checked:
            self.parent.champions_button_checked = not self.parent.champions_button_checked
            self.parent.skins_button_checked = not self.parent.skins_button_checked
            self.parent.button_skins.setChecked(self.parent.skins_button_checked)
            self.parent.button_champions.setChecked(self.parent.champions_button_checked)

            self.parent.GUI_skins_champions()
            
        else:
            self.parent.button_champions.setChecked(self.parent.champions_button_checked)

#MISSING FIX
    def skins_button_clicked(self):
        if not self.parent.skins_button_checked:
            self.parent.skins_button_checked = not self.parent.skins_button_checked
            self.parent.champions_button_checked = not self.parent.champions_button_checked
            self.parent.button_champions.setChecked(self.parent.champions_button_checked)
            self.parent.button_skins.setChecked(self.parent.skins_button_checked)

            self.parent.GUI_skins_champions()
            
        else:
            self.parent.button_skins.setChecked(self.parent.skins_button_checked)


#MISSING FIX
    def remove_account_filter_button_clicked(self):
        self.parent.account_manager.update_accounts_from_db()
        self.parent.line_edits.get_line_edit(obj_names.LineEditNames.CHAMPIONS_SEARCH.value).clear()
        self.parent.buttons.get_button(obj_names.ButtonNames.REMOVE_ACCOUNT_FILTER.value).hide()
        self.parent.refresh_gui_account_manager()


    def collect_account_data_button_clicked(self):
        self.parent.account_manager.fetch_account_data()


    def opgg_button_clicked(self, account: account_manager.Account):
        url = f"https://www.op.gg/summoners/{account.region}/{account.summoner_name}-{account.tagline}"
        webbrowser.open(url)


    def select_button_clicked(self, account: account_manager.Account, button: QPushButton):
        self.parent.account_manager.set_selected_account(account)
        for created_button in self.parent.buttons.created_buttons.values():
            if created_button.isCheckable():
                if created_button != button:
                    if created_button != self.parent.buttons.get_button(obj_names.ButtonNames.AUTOMATIC_QUEUE_ACCEPT.value):
                        created_button.setChecked(False)
        if not button.isChecked():
            button.setChecked(True)


    def automatic_queue_accept_button_clicked(self):
        configuration_values.toggle_automatic_queue_accept()


    def collect_data_on_startup_clicked(self):
        configuration_values.toggle_collect_data_on_startup()


    def login_button_clicked(self):
        if self.parent.account_manager.selected_account is not None:
            self.parent.buttons.get_button(obj_names.ButtonNames.LOGIN.value).setDisabled(True)
            login_thread = Thread(target=self.login_process)
            login_thread.start()
            champions_owned_update_thread = Thread(target=self.champions_owned_update, args=(login_thread,))
            champions_owned_update_thread.start()
            skins_owned_update_thread = Thread(target=self.skins_owned_update, args=(login_thread,))
            skins_owned_update_thread.start()

    def login_process(self):
        ready = False
        closed = False
        processes_killed = False
        kill_processes = ["RiotClientServices.exe", "LeagueClientUx.exe", "LeagueClient.exe"]

        for process_name in kill_processes:
            try:
                subprocess.call(["TASKKILL", "/F", "/IM", process_name])
                processes_killed = True
            except subprocess.CalledProcessError as e:
                pass
        if processes_killed:
            sleep(6)

        try:
            subprocess.call(["C:\Riot Games\League of Legends\LeagueClient.exe"])
        except:
            subprocess.call(["E:\Riot Games\League of Legends\LeagueClient.exe"])

        window_handle = None
        timeout = 20  # Timeout in seconds
        start_time = time()

        while not ready and (time() - start_time) < timeout:
            windows = findwindows.find_elements(class_name="RCLIENT")
            if windows:
                window_handle = windows[0].handle
                app = Application(backend="uia").connect(handle=window_handle)
                main_window = app.window(handle=window_handle)
                chrome_render_widget_host_hwnd = main_window.child_window(class_name="Chrome_RenderWidgetHostHWND")
                ready = True
            else:
                sleep(0.25)

        if window_handle:
            username_field = chrome_render_widget_host_hwnd.child_window(control_type=IUIA().known_control_types['Edit'], auto_id="username")
            password_field = chrome_render_widget_host_hwnd.child_window(control_type=IUIA().known_control_types['Edit'], auto_id="password")
            username_field.wait("visible", timeout=15)
            password_field.wait("visible", timeout=15)

            username_field.set_text(self.parent.account_manager.selected_account.username)
            password_field.set_text(self.parent.account_manager.selected_account.password)

            sign_in_button = chrome_render_widget_host_hwnd.child_window(control_type=IUIA().known_control_types['Button'], title="Sign in")
            sign_in_button.click()

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

        self.parent.buttons.get_button(obj_names.ButtonNames.LOGIN.value).setEnabled(True)
        self.parent.buttons.get_button(obj_names.ButtonNames.LOGIN.value).setChecked(False)

    def champions_owned_update(self, process: Thread):
        time_slept = 0
        while process.is_alive() and time_slept < 120:
            sleep(1)
            time_slept += 1

        time_waited = 0
        while not (self.parent.lcu_driver.account_data_fetched and self.parent.lcu_driver.champions_imported) and time_waited < 60:
            sleep(1)
            time_waited += 1
        if self.parent.lcu_driver.account_data_fetched and self.parent.lcu_driver.champions_imported:
            dbHandler2 = AccountManagerDB()
            dbHandler2.assign_champions_to_account(
                summoner_name = self.parent.lcu_driver.summoner_name,
                tagline=self.parent.lcu_driver.summoner_tagline,
                champion_list = self.parent.lcu_driver.owned_champions_list
            )
        else:
            print("Not ready for db interaction FROM CHAMPIONS")
            print(f"{self.parent.lcu_driver.account_data_fetched=}")
            print(f"{self.parent.lcu_driver.champions_imported=}")
            pass

    def skins_owned_update(self, process: Thread):
        time_slept = 0
        while process.is_alive() and time_slept < 120:
            sleep(1)
            time_slept += 1

        time_waited = 0
        while not (self.parent.lcu_driver.account_data_fetched and self.parent.lcu_driver.skins_imported) and time_waited < 60:
            sleep(1)
            time_waited += 1
        if self.parent.lcu_driver.account_data_fetched and self.parent.lcu_driver.skins_imported:
            dbHandler3 = AccountManagerDB()
            dbHandler3.assign_skins_to_account(
                summoner_name=self.parent.lcu_driver.summoner_name,
                tagline=self.parent.lcu_driver.summoner_tagline,
                skin_list=self.parent.lcu_driver.owned_skins_list
            )

        else:
            print("Not ready for db interaction FROM SKINS")
            print(f"{self.parent.lcu_driver.account_data_fetched=}")
            print(f"{self.parent.lcu_driver.skins_imported=}")
            pass