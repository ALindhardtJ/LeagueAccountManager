from account_manager import account_manager
from utilities.scaling_utils import ScalingUtils
from utilities import obj_names, utils
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QFont, QPixmap, QCursor
from PyQt5.QtCore import Qt, QTimer

class Labels:
    def __init__(self, parent) -> None:
        self.parent = parent
        self.label_actions = LabelActions(parent=parent)
        self.__created_labels = {}  # Dictionary to store created labels

        self.region_size_x, self.region_size_y = ScalingUtils.width(87), ScalingUtils.height(40)
        self.region_move_x = ScalingUtils.width(515)
        self.games_size_x, self.games_size_y = ScalingUtils.width(87), ScalingUtils.height(40)
        self.games_move_x = ScalingUtils.width(612)
        self.winrate_size_x, self.winrate_size_y = ScalingUtils.width(87), ScalingUtils.height(40)
        self.winrate_move_x = ScalingUtils.width(709)

    def get_label(self, object_name):
        if object_name in self.__created_labels:
            return self.__created_labels[object_name]
        else:
            return None
        
    def add_label(self, label: QLabel, object_name: str) -> None:
        self.__created_labels[object_name] = label

    @property
    def created_labels(self) -> dict:
        return self.__created_labels


    def lol_account_manager_logo(self) -> dict:
        show_widget = True
        object_name = obj_names.LabelNames.APPLICATION_LOGO.value
        if self.get_label(object_name=object_name):
            pass
        else:
            logo = QLabel(self.parent)
            logo.setObjectName(object_name)
            logo.setStyleSheet("border: 0px;")
            image = QPixmap(str(utils.APP_LOGO_FILE))
            image2 = image.scaledToHeight(ScalingUtils.width(40))
            logo.setPixmap(image2)
            logo.move(ScalingUtils.width(10), ScalingUtils.height(10))
            self.add_label(logo, object_name)
        return {"object_name":object_name, "show":show_widget}


    def account_id(self) -> dict:
        show_widget = True
        object_name = obj_names.LabelNames.ACCOUNT_ID.value
        if self.get_label(object_name=object_name):
            pass
        else:
            account_id_label = QLabel(self.parent)
            account_id_label.setObjectName(object_name)
            account_id_label.setText("ID")
            account_id_label.setFont(QFont('AnyStyle', ScalingUtils.get_font_size()))
            account_id_label.move(ScalingUtils.width(15), ScalingUtils.height(110))
            account_id_label.resize(ScalingUtils.width(40), ScalingUtils.height(40))
            self.add_label(account_id_label, object_name)
        return {"object_name":object_name, "show":show_widget}
    

    def name(self) -> dict:
        show_widget = True
        object_name = obj_names.LabelNames.NAME.value
        if self.get_label(object_name=object_name):
            pass
        else:
            name_label = QLabel(self.parent)
            name_label.setObjectName(object_name)
            name_label.setText("Ingame name + tagline")
            name_label.setFont(QFont('AnyStyle', ScalingUtils.get_font_size()))
            name_label.move(ScalingUtils.width(65), ScalingUtils.height(110))
            name_label.resize(ScalingUtils.width(250), ScalingUtils.height(40))
            self.add_label(name_label, object_name)
        return {"object_name":object_name, "show":show_widget}  


    def rank(self) -> dict:
        show_widget = True
        object_name = obj_names.LabelNames.RANK.value
        if self.get_label(object_name=object_name):
            pass
        else:
            rank_label = QLabel(self.parent)
            rank_label.setObjectName(object_name)
            rank_label.setText("Rank")
            rank_label.setFont(QFont('AnyStyle', ScalingUtils.get_font_size()))
            rank_label.move(ScalingUtils.width(325), ScalingUtils.height(110))
            rank_label.resize(ScalingUtils.width(180), ScalingUtils.height(40))
            self.add_label(rank_label, object_name)
        return {"object_name":object_name, "show":show_widget}


    def header_region(self) -> dict:
        show_widget = True
        object_name = obj_names.LabelNames.HEADER_REGION.value
        if self.get_label(object_name=object_name):
            pass
        else:
            header_region_label = QLabel(self.parent)
            header_region_label.setObjectName(object_name)
            header_region_label.setText("Region")
            header_region_label.setFont(QFont('AnyStyle', ScalingUtils.get_font_size()))
            header_region_label.move(self.region_move_x, ScalingUtils.height(110))
            header_region_label.resize(self.region_size_x, self.region_size_y)
            self.add_label(header_region_label, object_name)
        return {"object_name":object_name, "show":show_widget}


    def games_played(self) -> dict:
        show_widget = True
        object_name = obj_names.LabelNames.GAMES_PLAYED.value
        if self.get_label(object_name=object_name):
            pass
        else:
            games_label = QLabel(self.parent)
            games_label.setObjectName(object_name)
            games_label.setText("Games")
            games_label.setFont(QFont('AnyStyle', ScalingUtils.get_font_size()))
            games_label.move(self.games_move_x, ScalingUtils.height(110))
            games_label.resize(self.games_size_x, self.games_size_y)
            self.add_label(games_label, object_name)
        return {"object_name":object_name, "show":show_widget}


    def winrate(self) -> dict:
        show_widget = True
        object_name = obj_names.LabelNames.WINRATE.value
        if self.get_label(object_name=object_name):
            pass
        else:
            winrate_label = QLabel(self.parent)
            winrate_label.setObjectName(object_name)
            winrate_label.setText("Winrate")
            winrate_label.setFont(QFont('AnyStyle', ScalingUtils.get_font_size()))
            winrate_label.move(self.winrate_move_x, ScalingUtils.height(110))
            winrate_label.resize(self.winrate_size_x, self.winrate_size_y)
            self.add_label(winrate_label, object_name)
        return {"object_name":object_name, "show":show_widget}


    def add_edit_region(self) -> dict:
        show_widget = True
        object_name = obj_names.LabelNames.REGION.value
        if self.get_label(object_name=object_name):
            pass
        else:
            region_label = QLabel(self.parent)
            region_label.setObjectName(object_name)
            region_label.setStyleSheet("border: 0px;")
            region_label.setText("Choose a Region")
            region_label.move(ScalingUtils.width(25), ScalingUtils.height(107))
            self.add_label(region_label, object_name)
        return {"object_name":object_name, "show":show_widget}


    def add_edit_summoner_name(self) -> dict:
        show_widget = True
        object_name = obj_names.LabelNames.ADD_EDIT_SUMMONER_NAME.value
        if self.get_label(object_name=object_name):
            pass
        else:
            tagline_label = QLabel(self.parent)
            tagline_label.setObjectName(object_name)
            tagline_label.setStyleSheet("border: 0px;")
            tagline_label.setText("Summoner name")
            tagline_label.move(ScalingUtils.width(25), ScalingUtils.height(167))
            self.add_label(tagline_label, object_name)
        return {"object_name":object_name, "show":show_widget}
    

    def add_edit_tagline(self) -> dict:
        show_widget = True
        object_name = obj_names.LabelNames.ADD_EDIT_TAGLINE.value
        if self.get_label(object_name=object_name):
            pass
        else:
            tagline_label = QLabel(self.parent)
            tagline_label.setObjectName(object_name)
            tagline_label.setStyleSheet("border: 0px;")
            tagline_label.setText("Tagline")
            tagline_label.move(ScalingUtils.width(25), ScalingUtils.height(227))
            self.add_label(tagline_label, object_name)
        return {"object_name":object_name, "show":show_widget}


    def add_edit_username(self) -> dict:
        show_widget = True
        object_name = obj_names.LabelNames.ADD_EDIT_USERNAME.value
        if self.get_label(object_name=object_name):
            pass
        else:
            username_label = QLabel(self.parent)
            username_label.setObjectName(object_name)
            username_label.setStyleSheet("border: 0px;")
            username_label.setText("Username")
            username_label.move(ScalingUtils.width(25), ScalingUtils.height(287))
            self.add_label(username_label, object_name)
        return {"object_name":object_name, "show":show_widget}
    

    def info_summoner_name(self) -> dict:
        show_widget = True
        object_name = obj_names.LabelNames.INFO_SUMMONER_NAME.value
        if self.get_label(object_name=object_name):
            pass
        else:
            tagline_label = QLabel(self.parent)
            tagline_label.setObjectName(object_name)
            tagline_label.setStyleSheet("border: 0px;")
            tagline_label.setText("Summoner name")
            tagline_label.move(ScalingUtils.width(30), ScalingUtils.height(90))
            self.add_label(tagline_label, object_name)
        return {"object_name":object_name, "show":show_widget}
    

    def info_tagline(self) -> dict:
        show_widget = True
        object_name = obj_names.LabelNames.INFO_TAGLINE.value
        if self.get_label(object_name=object_name):
            pass
        else:
            tagline_label = QLabel(self.parent)
            tagline_label.setObjectName(object_name)
            tagline_label.setStyleSheet("border: 0px;")
            tagline_label.setText("Tagline")
            tagline_label.move(ScalingUtils.width(30), ScalingUtils.height(150))
            self.add_label(tagline_label, object_name)
        return {"object_name":object_name, "show":show_widget}


    def info_username(self) -> dict:
        show_widget = True
        object_name = obj_names.LabelNames.INFO_USERNAME.value
        if self.get_label(object_name=object_name):
            pass
        else:
            username_label = QLabel(self.parent)
            username_label.setObjectName(object_name)
            username_label.setStyleSheet("border: 0px;")
            username_label.setText("Username")
            username_label.move(ScalingUtils.width(30), ScalingUtils.height(210))
            self.add_label(username_label, object_name)
        return {"object_name":object_name, "show":show_widget}


    def under_development(self) -> dict:
        show_widget = True
        object_name = obj_names.LabelNames.UNDER_DEVELOPMENT.value
        if self.get_label(object_name=object_name):
            pass
        else:
            under_development_label = QLabel(self.parent)
            under_development_label.setObjectName(object_name)
            under_development_label.setText("Under development")
            under_development_label.move(ScalingUtils.width(50), ScalingUtils.height(110))
            self.add_label(under_development_label, object_name)
        return {"object_name":object_name, "show":show_widget}


    def actual_account_id(self, account: account_manager.Account, increment: int) -> dict:
        show_widget = True
        object_name = f"{obj_names.LabelNames.ACTUAL_ACCOUNT_ID.value}_{str(account.account_id)}"
        if self.get_label(object_name=object_name):
            self.get_label(object_name=object_name).setText(str(account.account_id))
            self.get_label(object_name=object_name).move(
                ScalingUtils.width(15), (ScalingUtils.height(115) + ScalingUtils.height(increment))
            )
        else:
            id_label = QLabel(self.parent)
            id_label.setObjectName(object_name)
            id_label.setText(str(account.account_id))
            id_label.setFont(QFont('AnyStyle', ScalingUtils.get_font_size()))
            id_label.move(ScalingUtils.width(15), (ScalingUtils.height(115) + ScalingUtils.height(increment)))
            id_label.resize(ScalingUtils.width(40), ScalingUtils.height(40))
            self.add_label(id_label, object_name)
        return {"object_name":object_name, "show":show_widget}


    def actual_name(self, account: account_manager.Account, increment: int) -> dict:
        show_widget = True
        object_name = f"{obj_names.LabelNames.ACTUAL_NAME.value}_{str(account.account_id)}"
        if self.get_label(object_name=object_name):
            self.get_label(object_name=object_name).setText(f"{account.summoner_name} #{account.tagline}")
            self.get_label(object_name=object_name).move(
                ScalingUtils.width(65), (ScalingUtils.height(115) + ScalingUtils.height(increment))
            )
        else:
            summoner_name_label = QLabel(self.parent)
            summoner_name_label.setObjectName(object_name)
            summoner_name_label.setText(f"{account.summoner_name} #{account.tagline}")
            summoner_name_label.setFont(QFont('AnyStyle', ScalingUtils.get_font_size()))
            summoner_name_label.move(ScalingUtils.width(65), (ScalingUtils.height(115) + ScalingUtils.height(increment)))
            summoner_name_label.resize(ScalingUtils.width(250), ScalingUtils.height(40))
            self.add_label(summoner_name_label, object_name)
        return {"object_name":object_name, "show":show_widget}


    def actual_rank(self, account: account_manager.Account, increment: int) -> dict:
        show_widget = True
        object_name = f"{obj_names.LabelNames.ACTUAL_RANK.value}_{str(account.account_id)}"
        if self.get_label(object_name=object_name):
            self.get_label(object_name=object_name).setText(account.rank)
            self.get_label(object_name=object_name).move(
                ScalingUtils.width(325), (ScalingUtils.height(115) + ScalingUtils.height(increment))
            )
        else:
            rank_label = QLabel(self.parent)
            rank_label.setObjectName(object_name)
            rank_label.setFont(QFont('AnyStyle', ScalingUtils.get_font_size()))
            rank_label.setText(account.rank)
            rank_label.move(ScalingUtils.width(325), (ScalingUtils.height(115) + ScalingUtils.height(increment)))
            rank_label.resize(ScalingUtils.width(180), ScalingUtils.height(40))
            self.add_label(rank_label, object_name)
        return {"object_name":object_name, "show":show_widget}


    def actual_region(self, account: account_manager.Account, increment: int) -> dict:
        show_widget = True
        object_name = f"{obj_names.LabelNames.ACTUAL_REGION.value}_{str(account.account_id)}"
        if self.get_label(object_name=object_name):
            self.get_label(object_name=object_name).setText(account.region)
            self.get_label(object_name=object_name).move(
                self.region_move_x, (ScalingUtils.height(115) + ScalingUtils.height(increment))
            )
        else:
            region_label = QLabel(self.parent)
            region_label.setObjectName(object_name)
            region_label.setText(account.region)
            region_label.setFont(QFont('AnyStyle', ScalingUtils.get_font_size()))
            region_label.move(self.region_move_x, (ScalingUtils.height(115) + ScalingUtils.height(increment)))
            region_label.resize(self.region_size_x, self.region_size_y)
            self.add_label(region_label, object_name)
        return {"object_name":object_name, "show":show_widget}


    def actual_games_played(self, account: account_manager.Account, increment: int) -> dict:
        show_widget = True
        object_name = f"{obj_names.LabelNames.ACTUAL_GAMES_PLAYED.value}_{str(account.account_id)}"
        if self.get_label(object_name=object_name):
            self.get_label(object_name=object_name).setText(account.games_played)
            self.get_label(object_name=object_name).move(
                self.games_move_x, (ScalingUtils.height(115) + ScalingUtils.height(increment))
            )
        else:
            games_label = QLabel(self.parent)
            games_label.setObjectName(object_name)
            games_label.setText(account.games_played)
            games_label.setFont(QFont('AnyStyle', ScalingUtils.get_font_size()))
            games_label.move(self.games_move_x, (ScalingUtils.height(115) + ScalingUtils.height(increment)))
            games_label.resize(self.games_size_x, self.games_size_y)
            self.add_label(games_label, object_name)
        return {"object_name":object_name, "show":show_widget}


    def actual_winrate(self, account: account_manager.Account, increment: int) -> dict:
        show_widget = True
        object_name = f"{obj_names.LabelNames.ACTUAL_WINRATE.value}_{str(account.account_id)}"
        if self.get_label(object_name=object_name):
            self.get_label(object_name=object_name).setText(account.winrate)
            self.get_label(object_name=object_name).move(
                self.winrate_move_x, (ScalingUtils.height(115) + ScalingUtils.height(increment))
            )
        else:
            winrate_label = QLabel(self.parent)
            winrate_label.setObjectName(object_name)
            winrate_label.setText(account.winrate)
            winrate_label.setFont(QFont('AnyStyle', ScalingUtils.get_font_size()))
            winrate_label.move(self.winrate_move_x, (ScalingUtils.height(115) + ScalingUtils.height(increment)))
            winrate_label.resize(self.winrate_size_x, self.winrate_size_y)
            self.add_label(winrate_label, object_name)
        return {"object_name":object_name, "show":show_widget}


    def copy_summoner_name(self) -> dict:
        show_widget = True
        object_name = obj_names.LabelNames.COPY_SUMMONER_NAME.value
        if self.get_label(object_name=object_name):
            pass
        else:
            logo = QLabel(self.parent)
            logo.setObjectName(object_name)
            logo.setCursor(QCursor(Qt.PointingHandCursor))
            logo.setStyleSheet("border: 0px;")
            image = QPixmap(str(utils.CLIPBOARD_LOGO_FILE))
            image2 = image.scaledToHeight(ScalingUtils.width(35))
            logo.setPixmap(image2)
            logo.move(ScalingUtils.width(305), ScalingUtils.height(80))
            logo.mousePressEvent = lambda event: self.label_actions.copy_label_clicked(event, logo)
            self.add_label(logo, object_name)
        return {"object_name":object_name, "show":show_widget}
    

    def copy_tagline(self) -> dict:
        show_widget = True
        object_name = obj_names.LabelNames.COPY_TAGLINE.value
        if self.get_label(object_name=object_name):
            pass
        else:
            logo = QLabel(self.parent)
            logo.setObjectName(object_name)
            logo.setCursor(QCursor(Qt.PointingHandCursor))
            logo.setStyleSheet("border: 0px;")
            image = QPixmap(str(utils.CLIPBOARD_LOGO_FILE))
            image2 = image.scaledToHeight(ScalingUtils.width(35))
            logo.setPixmap(image2)
            logo.move(ScalingUtils.width(305), ScalingUtils.height(140))
            logo.mousePressEvent = lambda event: self.label_actions.copy_label_clicked(event, logo)
            self.add_label(logo, object_name)
        return {"object_name":object_name, "show":show_widget}
    

    def copy_username(self) -> dict:
        show_widget = True
        object_name = obj_names.LabelNames.COPY_USERNAME.value
        if self.get_label(object_name=object_name):
            pass
        else:
            logo = QLabel(self.parent)
            logo.setObjectName(object_name)
            logo.setCursor(QCursor(Qt.PointingHandCursor))
            logo.setStyleSheet("border: 0px;")
            image = QPixmap(str(utils.CLIPBOARD_LOGO_FILE))
            image2 = image.scaledToHeight(ScalingUtils.width(35))
            logo.setPixmap(image2)
            logo.move(ScalingUtils.width(305), ScalingUtils.height(200))
            logo.mousePressEvent = lambda event: self.label_actions.copy_label_clicked(event, logo)
            self.add_label(logo, object_name)
        return {"object_name":object_name, "show":show_widget}
    

    def copy_password(self) -> dict:
        show_widget = True
        object_name = obj_names.LabelNames.COPY_PASSWORD.value
        if self.get_label(object_name=object_name):
            pass
        else:
            logo = QLabel(self.parent)
            logo.setObjectName(object_name)
            logo.setCursor(QCursor(Qt.PointingHandCursor))
            logo.setStyleSheet("border: 0px;")
            image = QPixmap(str(utils.CLIPBOARD_LOGO_FILE))
            image2 = image.scaledToHeight(ScalingUtils.width(35))
            logo.setPixmap(image2)
            logo.move(ScalingUtils.width(305), ScalingUtils.height(260))
            logo.mousePressEvent = lambda event: self.label_actions.copy_label_clicked(event, logo)
            self.add_label(logo, object_name)
        return {"object_name":object_name, "show":show_widget}



class LabelActions:
    def __init__(self, parent):
        self.parent = parent


    def copy_label_clicked(self, event, label: QLabel):
        if label.objectName() == obj_names.LabelNames.COPY_SUMMONER_NAME.value:
            self.parent.set_system_clipboard_text(self.parent.account_manager.selected_account.summoner_name)
            label.setStyleSheet("border: 1px solid grey;")
            QTimer.singleShot(150, lambda w=label: self.remove_border_style(w))

        elif label.objectName() == obj_names.LabelNames.COPY_TAGLINE.value:
            self.parent.set_system_clipboard_text(self.parent.account_manager.selected_account.tagline)
            label.setStyleSheet("border: 1px solid grey;")
            QTimer.singleShot(150, lambda w=label: self.remove_border_style(w))

        elif label.objectName() == obj_names.LabelNames.COPY_USERNAME.value:
            self.parent.set_system_clipboard_text(self.parent.account_manager.selected_account.username)
            label.setStyleSheet("border: 1px solid grey;")
            QTimer.singleShot(150, lambda w=label: self.remove_border_style(w))

        elif label.objectName() == obj_names.LabelNames.COPY_PASSWORD.value:
            self.parent.set_system_clipboard_text(self.parent.account_manager.selected_account.password)
            label.setStyleSheet("border: 1px solid grey;")
            QTimer.singleShot(150, lambda w=label: self.remove_border_style(w))
    
    def remove_border_style(self, label: QLabel):
        label.setStyleSheet("border: 0px;")