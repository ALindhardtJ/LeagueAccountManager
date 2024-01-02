from utilities.scaling_utils import ScalingUtils
from PyQt5.QtWidgets import QLineEdit, QCompleter
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QStringListModel, Qt
from database import dbHandler
import copy
from utilities import obj_names



class LineEdits:
    def __init__(self, parent):
        self.parent = parent
        self.line_edit_actions = LineEditActions(parent=parent)
        self.__created_line_edits = {}  # Dictionary to store created line_edits

    def get_line_edit(self, object_name: str):
        if object_name in self.__created_line_edits:
            return self.__created_line_edits[object_name]
        else:
            return None

    def add_line_edit(self, line_edit: QLineEdit, object_name: str) -> None:
        self.__created_line_edits[object_name] = line_edit

    @property
    def created_line_edits(self) -> dict:
        return self.__created_line_edits


    def add_account_summoner_name(self) -> dict:
        show_widget = True
        object_name = obj_names.LineEditNames.ADD_ACCOUNT_SUMMONER_NAME.value
        if self.get_line_edit(object_name=object_name):
            self.get_line_edit(object_name=object_name).clear()
        else:
            summoner_name = QLineEdit(self.parent)
            summoner_name.setObjectName(object_name)
            summoner_name.setPlaceholderText("Summoner name")
            summoner_name.move(ScalingUtils.width(130), ScalingUtils.height(155))
            summoner_name.resize(ScalingUtils.width(170), ScalingUtils.height(40))
            summoner_name.setFont(QFont('AnyStyle', ScalingUtils.get_font_size()))
            self.add_line_edit(summoner_name, object_name)
        return {"object_name":object_name, "show":show_widget}


    def add_account_tagline(self) -> dict:
        show_widget = True
        object_name = obj_names.LineEditNames.ADD_ACCOUNT_TAGLINE.value
        if self.get_line_edit(object_name=object_name):
            self.get_line_edit(object_name=object_name).clear()
        else:
            tagline = QLineEdit(self.parent)
            tagline.setObjectName(object_name)
            tagline.setPlaceholderText("Tagline - leave out '#'")
            tagline.setFont(QFont('AnyStyle', ScalingUtils.get_font_size()))
            tagline.move(ScalingUtils.width(130), ScalingUtils.height(215))
            tagline.resize(ScalingUtils.width(170), ScalingUtils.height(40))
            self.add_line_edit(tagline, object_name)
        return {"object_name":object_name, "show":show_widget}


    def add_account_username(self) -> dict:
        show_widget = True
        object_name = obj_names.LineEditNames.ADD_ACCOUNT_USERNAME.value
        if self.get_line_edit(object_name=object_name):
            self.get_line_edit(object_name=object_name).clear()
        else:
            username = QLineEdit(self.parent)
            username.setObjectName(object_name)
            username.setPlaceholderText("Username")
            username.setFont(QFont('AnyStyle', ScalingUtils.get_font_size()))
            username.move(ScalingUtils.width(130), ScalingUtils.height(275))
            username.resize(ScalingUtils.width(170), ScalingUtils.height(40))
            self.add_line_edit(username, object_name)
        return {"object_name":object_name, "show":show_widget}


    def add_account_password(self) -> dict:
        show_widget = True
        object_name = obj_names.LineEditNames.ADD_ACCOUNT_PASSWORD.value
        if self.get_line_edit(object_name=object_name):
            self.get_line_edit(object_name=object_name).clear()
        else:
            password = QLineEdit(self.parent)
            password.setObjectName(object_name)
            password.setEchoMode(QLineEdit.Password)
            password.setPlaceholderText("Password")
            password.setFont(QFont('AnyStyle', ScalingUtils.get_font_size()))
            password.move(ScalingUtils.width(130), ScalingUtils.height(335))
            password.resize(ScalingUtils.width(170), ScalingUtils.height(40))
            self.add_line_edit(password, object_name)
        return {"object_name":object_name, "show":show_widget}


    def edit_account_summoner_name(self) -> dict:
        show_widget = True
        object_name = obj_names.LineEditNames.EDIT_ACCOUNT_SUMMONER_NAME.value
        if self.get_line_edit(object_name=object_name):
            self.get_line_edit(object_name=object_name).setText(self.parent.account_manager.selected_account.summoner_name)
        else:
            summoner_name = QLineEdit(self.parent)
            summoner_name.setObjectName(object_name)
            summoner_name.setText(self.parent.account_manager.selected_account.summoner_name)
            summoner_name.move(ScalingUtils.width(130), ScalingUtils.height(155))
            summoner_name.resize(ScalingUtils.width(170), ScalingUtils.height(40))
            summoner_name.setFont(QFont('AnyStyle', ScalingUtils.get_font_size()))
            self.add_line_edit(summoner_name, object_name)
        return {"object_name":object_name, "show":show_widget}
    
    
    def edit_account_tagline(self) -> dict:
        show_widget = True
        object_name = obj_names.LineEditNames.EDIT_ACCOUNT_TAGLINE.value
        if self.get_line_edit(object_name=object_name):
            self.get_line_edit(object_name=object_name).setText(self.parent.account_manager.selected_account.tagline)
        else:
            tagline = QLineEdit(self.parent)
            tagline.setObjectName(object_name)
            tagline.setText(self.parent.account_manager.selected_account.tagline)
            tagline.setFont(QFont('AnyStyle', ScalingUtils.get_font_size()))
            tagline.move(ScalingUtils.width(130), ScalingUtils.height(215))
            tagline.resize(ScalingUtils.width(170), ScalingUtils.height(40))
            self.add_line_edit(tagline, object_name)
        return {"object_name":object_name, "show":show_widget}


    def edit_account_username(self) -> dict:
        show_widget = True
        object_name = obj_names.LineEditNames.EDIT_ACCOUNT_USERNAME.value
        if self.get_line_edit(object_name=object_name):
            self.get_line_edit(object_name=object_name).setText(self.parent.account_manager.selected_account.username)
        else:
            username = QLineEdit(self.parent)
            username.setObjectName(object_name)
            username.setText(self.parent.account_manager.selected_account.username)
            username.move(ScalingUtils.width(130), ScalingUtils.height(275))
            username.resize(ScalingUtils.width(170), ScalingUtils.height(40))
            username.setFont(QFont('AnyStyle', ScalingUtils.get_font_size()))
            self.add_line_edit(username, object_name)
        return {"object_name":object_name, "show":show_widget}


    def edit_account_password(self) -> dict:
        show_widget = True
        object_name = obj_names.LineEditNames.EDIT_ACCOUNT_PASSWORD.value
        if self.get_line_edit(object_name=object_name):
            self.get_line_edit(object_name=object_name).setText(self.parent.account_manager.selected_account.password)
        else:
            password = QLineEdit(self.parent)
            password.setObjectName(object_name)
            password.setEchoMode(QLineEdit.Password)
            password.setText(self.parent.account_manager.selected_account.password)
            password.setFont(QFont('AnyStyle', ScalingUtils.get_font_size()))
            password.move(ScalingUtils.width(130), ScalingUtils.height(335))
            password.resize(ScalingUtils.width(170), ScalingUtils.height(40))
            self.add_line_edit(password, object_name)
        return {"object_name":object_name, "show":show_widget}


    def info_summoner_name(self) -> dict:
        show_widget = True
        object_name = obj_names.LineEditNames.INFO_SUMMONER_NAME.value
        if self.get_line_edit(object_name=object_name):
            self.get_line_edit(object_name=object_name).setText(self.parent.account_manager.selected_account.summoner_name)
        else:
            line_edit_tagline = QLineEdit(self.parent)
            line_edit_tagline.setText(self.parent.account_manager.selected_account.summoner_name)
            line_edit_tagline.setObjectName(object_name)
            line_edit_tagline.setReadOnly(True)
            line_edit_tagline.setFont(QFont('AnyStyle', ScalingUtils.get_font_size()))
            line_edit_tagline.move(ScalingUtils.width(125), ScalingUtils.height(77))
            line_edit_tagline.resize(ScalingUtils.width(170), ScalingUtils.height(40))
            self.add_line_edit(line_edit_tagline, object_name)
        return {"object_name":object_name, "show":show_widget}
    

    def info_tagline(self) -> dict:
        show_widget = True
        object_name = obj_names.LineEditNames.INFO_TAGLINE.value
        if self.get_line_edit(object_name=object_name):
            self.get_line_edit(object_name=object_name).setText(self.parent.account_manager.selected_account.tagline)
        else:
            line_edit_tagline = QLineEdit(self.parent)
            line_edit_tagline.setText(self.parent.account_manager.selected_account.tagline)
            line_edit_tagline.setObjectName(object_name)
            line_edit_tagline.setReadOnly(True)
            line_edit_tagline.setFont(QFont('AnyStyle', ScalingUtils.get_font_size()))
            line_edit_tagline.move(ScalingUtils.width(125), ScalingUtils.height(137))
            line_edit_tagline.resize(ScalingUtils.width(170), ScalingUtils.height(40))
            self.add_line_edit(line_edit_tagline, object_name)
        return {"object_name":object_name, "show":show_widget}


    def info_username(self) -> dict:
        show_widget = True
        object_name = obj_names.LineEditNames.INFO_USERNAME.value
        if self.get_line_edit(object_name=object_name):
            self.get_line_edit(object_name=object_name).setText(self.parent.account_manager.selected_account.username)
        else:
            line_edit_username = QLineEdit(self.parent)
            line_edit_username.setText(self.parent.account_manager.selected_account.username)
            line_edit_username.setObjectName(object_name)
            line_edit_username.setReadOnly(True)
            line_edit_username.setFont(QFont('AnyStyle', ScalingUtils.get_font_size()))
            line_edit_username.move(ScalingUtils.width(125), ScalingUtils.height(197))
            line_edit_username.resize(ScalingUtils.width(170), ScalingUtils.height(40))
            self.add_line_edit(line_edit_username, object_name)
        return {"object_name":object_name, "show":show_widget}


    def info_password(self) -> dict:
        show_widget = True
        object_name = obj_names.LineEditNames.INFO_PASSWORD.value
        if self.get_line_edit(object_name=object_name):
            self.get_line_edit(object_name=object_name).setText(self.parent.account_manager.selected_account.password)
        else:
            line_edit_password = QLineEdit(self.parent)
            line_edit_password.setText(self.parent.account_manager.selected_account.password)
            line_edit_password.setObjectName(object_name)
            line_edit_password.setReadOnly(True)
            line_edit_password.setEchoMode(QLineEdit.Password)
            line_edit_password.setFont(QFont('AnyStyle', ScalingUtils.get_font_size()))
            line_edit_password.move(ScalingUtils.width(125), ScalingUtils.height(257))
            line_edit_password.resize(ScalingUtils.width(170), ScalingUtils.height(40))
            self.add_line_edit(line_edit_password, object_name)
        return {"object_name":object_name, "show":show_widget}


    def champions_search(self) -> dict:
        show_widget = True
        object_name = obj_names.LineEditNames.CHAMPIONS_SEARCH.value
        if self.get_line_edit(object_name=object_name):
            pass
        else:
            search_suggestions = dbHandler.get_champions_names()
            model = QStringListModel(search_suggestions)
            completer = QCompleter()
            completer.setModel(model)
            completer.setCaseSensitivity(Qt.CaseInsensitive)
            champion_search = QLineEdit(self.parent)
            champion_search.setObjectName(object_name)
            champion_search.setCompleter(completer)
            champion_search.setPlaceholderText("Search for a champion")
            champion_search.setFont(QFont('AnyStyle', ScalingUtils.get_font_size()))
            champion_search.move(ScalingUtils.width(325), ScalingUtils.height(65))
            champion_search.resize(ScalingUtils.width(180), ScalingUtils.height(40))
            champion_search.returnPressed.connect(self.line_edit_actions.on_enter_pressed)
            self.add_line_edit(champion_search, object_name)
        return {"object_name":object_name, "show":show_widget}



class LineEditActions:
    def __init__(self, parent):
        self.parent = parent

    def on_enter_pressed(self):
        champion = self.parent.line_edits.get_line_edit(obj_names.LineEditNames.CHAMPIONS_SEARCH.value).text()
        accounts = dbHandler.get_accounts_by_champion(champion_name=champion)
        account_ids = [account[0] for account in accounts]
        self.parent.account_manager.filter_accounts(account_ids)
        self.parent.refresh_gui_account_manager()
        self.parent.buttons.get_button(obj_names.ButtonNames.REMOVE_ACCOUNT_FILTER.value).show()