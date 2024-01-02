import win32clipboard
from PyQt5.QtGui import QGuiApplication, QIcon
from PyQt5.QtWidgets import QWidget

from widget_managers import buttons, labels, check_boxes, combo_boxes, line_edits
from my_lcu_driver import MyLcuDriver
from account_manager import account_manager
from utilities import obj_names, utils
from utilities.scaling_utils import ScalingUtils
from configuration_files import configuration_values


class LolAccountManagerApp(QWidget):
    def __init__(self):
        super(LolAccountManagerApp, self).__init__()

        self.screen = QGuiApplication.primaryScreen()
        self.rect = self.screen.availableGeometry()
        self.screen_size = self.screen.size()

        self.setWindowIcon(QIcon(str(utils.APP_ICON_FILE)))
        self.setWindowTitle("League Account Manager")
        self.setGeometry(ScalingUtils.x_pos(800), ScalingUtils.y_pos(200), 0, 0)

        self.buttons = buttons.Buttons(parent=self)
        self.labels = labels.Labels(parent=self)
        self.check_boxes = check_boxes.CheckBoxes(parent=self)
        self.combo_boxes = combo_boxes.ComboBoxes(parent=self)
        self.line_edits = line_edits.LineEdits(parent=self)

        self.account_manager = account_manager.AccountManager(parent=self)
        self.account_manager.update_accounts_from_db()
        if configuration_values.collect_data_on_startup:
            self.account_manager.fetch_account_data()

        self.lcu_driver = MyLcuDriver(parent=self)
        self.lcu_driver.start()

        self.GUI_account_manager()

#--------------------------------------------------------------------------------------------------------------------#
#Defining user interfaces of different windows

    def GUI_account_manager(self):
        print(len(self.children()))

        widgets = {
            "labels": [],
            "buttons": [],
            "line_edits": [],
            "combo_boxes": [],
            "check_boxes": [],
        }


        widgets["labels"].append(self.labels.lol_account_manager_logo())
        widgets["labels"].append(self.labels.account_id())
        widgets["labels"].append(self.labels.name())
        widgets["labels"].append(self.labels.rank())
        widgets["labels"].append(self.labels.header_region())
        widgets["labels"].append(self.labels.games_played())
        widgets["labels"].append(self.labels.winrate())

        generated_labels, generated_buttons = self.generate_account_specific_widgets()
        widgets["labels"] += generated_labels
        widgets["buttons"] += generated_buttons

        widgets["buttons"].append(self.buttons.account_manager_button())
        widgets["buttons"].append(self.buttons.add_new_account())
        widgets["buttons"].append(self.buttons.remove_account_filter())
        widgets["buttons"].append(self.buttons.login())
        widgets["buttons"].append(self.buttons.delete())
        widgets["buttons"].append(self.buttons.info())
        widgets["buttons"].append(self.buttons.edit())
        widgets["buttons"].append(self.buttons.skins_champions())
        widgets["buttons"].append(self.buttons.collect_account_data())
        widgets["buttons"].append(self.buttons.app_configurations())

        widgets["line_edits"].append(self.line_edits.champions_search())

        self.show_hide_widgets(active_widgets=widgets)
        self.set_geometry_account_manager()


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - # 

    def GUI_add_account(self):
        print(len(self.children()))

        widgets = {
            "labels": [],
            "buttons": [],
            "line_edits": [],
            "combo_boxes": [],
            "check_boxes": [],
        }

        widgets["labels"].append(self.labels.lol_account_manager_logo())
        widgets["labels"].append(self.labels.add_edit_region())
        widgets["labels"].append(self.labels.add_edit_summoner_name())
        widgets["labels"].append(self.labels.add_edit_tagline())
        widgets["labels"].append(self.labels.add_edit_username())

        widgets["buttons"].append(self.buttons.account_manager_button())
        widgets["buttons"].append(self.buttons.submit_new_account())

        widgets["line_edits"].append(self.line_edits.add_account_summoner_name())
        widgets["line_edits"].append(self.line_edits.add_account_tagline())
        widgets["line_edits"].append(self.line_edits.add_account_username())
        widgets["line_edits"].append(self.line_edits.add_account_password())

        widgets["check_boxes"].append(self.check_boxes.add_account_password())

        widgets["combo_boxes"].append(self.combo_boxes.add_account_region())

        self.show_hide_widgets(active_widgets=widgets)
        self.set_geometry_add_account()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - # 
    
    def GUI_app_configurations(self):
        print(len(self.children()))

        widgets = {
            "labels": [],
            "buttons": [],
            "line_edits": [],
            "combo_boxes": [],
            "check_boxes": [],
        }

        widgets["labels"].append(self.labels.lol_account_manager_logo())
        widgets["buttons"].append(self.buttons.account_manager_button())
        widgets["buttons"].append(self.buttons.automatic_queue_accept())
        widgets["buttons"].append(self.buttons.collect_data_on_startup())
        self.show_hide_widgets(active_widgets=widgets)
        self.set_geometry_app_configurations()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - # 

    def GUI_info(self):
        print(len(self.children()))

        widgets = {
            "labels": [],
            "buttons": [],
            "line_edits": [],
            "combo_boxes": [],
            "check_boxes": [],
        }

        widgets["labels"].append(self.labels.lol_account_manager_logo())
        widgets["labels"].append(self.labels.info_summoner_name())
        widgets["labels"].append(self.labels.info_tagline())
        widgets["labels"].append(self.labels.info_username())
        widgets["labels"].append(self.labels.copy_summoner_name())
        widgets["labels"].append(self.labels.copy_tagline())
        widgets["labels"].append(self.labels.copy_username())
        widgets["labels"].append(self.labels.copy_password())

        widgets["buttons"].append(self.buttons.account_manager_button())

        widgets["line_edits"].append(self.line_edits.info_summoner_name())
        widgets["line_edits"].append(self.line_edits.info_tagline())
        widgets["line_edits"].append(self.line_edits.info_username())
        widgets["line_edits"].append(self.line_edits.info_password())

        widgets["check_boxes"].append(self.check_boxes.info_account_password())

        self.show_hide_widgets(active_widgets=widgets)
        self.set_geometry_info()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - # 

    def GUI_edit(self):
        print(len(self.children()))

        widgets = {
            "labels": [],
            "buttons": [],
            "line_edits": [],
            "combo_boxes": [],
            "check_boxes": [],
        }

        widgets["labels"].append(self.labels.lol_account_manager_logo())
        widgets["labels"].append(self.labels.add_edit_region())
        widgets["labels"].append(self.labels.add_edit_summoner_name())
        widgets["labels"].append(self.labels.add_edit_tagline())
        widgets["labels"].append(self.labels.add_edit_username())

        widgets["buttons"].append(self.buttons.account_manager_button())
        widgets["buttons"].append(self.buttons.submit_edited_account())

        widgets["line_edits"].append(self.line_edits.edit_account_summoner_name())
        widgets["line_edits"].append(self.line_edits.edit_account_tagline())
        widgets["line_edits"].append(self.line_edits.edit_account_username())
        widgets["line_edits"].append(self.line_edits.edit_account_password())

        widgets["check_boxes"].append(self.check_boxes.edit_account_password())

        widgets["combo_boxes"].append(self.combo_boxes.edit_account_region())

        self.show_hide_widgets(active_widgets=widgets)
        self.set_geometry_edit()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - # 

    def GUI_skins_champions(self):
        print(len(self.children()))

        widgets = {
            "labels": [],
            "buttons": [],
            "line_edits": [],
            "combo_boxes": [],
            "check_boxes": [],
        }

        
        self.set_geometry_skins_champions()


#--------------------------------------------------------------------------------------------------------------------#

    def generate_account_specific_widgets(self) -> None:
        increment = 40
        labels = []
        buttons = []
        
        for account in self.account_manager.accounts.values():
            labels += self.generate_account_specific_labels(
                account=account,
                increment=increment
            )
            buttons += self.generate_account_specific_buttons(
                account=account,
                increment=increment
            )
            increment += 40

        return labels, buttons

#--------------------------------------------------------------------------------------------------------------------#


    def generate_account_specific_labels(self, account: account_manager.Account, increment: int) -> list[dict]:
        labels = []
        labels.append(self.labels.actual_account_id(
            account=account,
            increment=increment
        ))
        labels.append(self.labels.actual_name(
            account=account,
            increment=increment
        ))
        labels.append(self.labels.actual_rank(
            account=account,
            increment=increment
        ))
        labels.append(self.labels.actual_region(
            account=account,
            increment=increment
        ))
        labels.append(self.labels.actual_games_played(
            account=account,
            increment=increment
        ))
        labels.append(self.labels.actual_winrate(
            account=account,
            increment=increment
        ))
        return labels

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - # 

    def generate_account_specific_buttons(self, account: account_manager.Account, increment: int) -> list[dict]:
        buttons = []
        buttons.append(self.buttons.opgg(
            account=account,
            increment=increment
        ))
        buttons.append(self.buttons.select_account(
            account=account,
            increment=increment
        ))
        return buttons

#--------------------------------------------------------------------------------------------------------------------#

    def refresh_gui_account_manager(self):
        if self.buttons.get_button(obj_names.ButtonNames.DELETE.value).isVisible():
            self.set_geometry_account_manager()
            self.buttons.get_button(obj_names.ButtonNames.ACCOUNT_MANAGER.value).click()

#--------------------------------------------------------------------------------------------------------------------#

    def set_system_clipboard_text(self, text: str) -> None:
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardText(text)
        win32clipboard.CloseClipboard()

#--------------------------------------------------------------------------------------------------------------------#
#Set geometry for different windows

    def set_geometry_account_manager(self):
        x, y, width, height = self.geometry().getRect()
        self.setGeometry(
            x,
            y,
            ScalingUtils.width(1035),
            ScalingUtils.height(170) + (len(self.account_manager.accounts) * ScalingUtils.height(40))
        )

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - # 

    def set_geometry_add_account(self):
        self.setGeometry(self.geometry().x(), self.geometry().y(), ScalingUtils.width(328), ScalingUtils.height(465))

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - # 

    def set_geometry_app_configurations(self):
        self.setGeometry(self.geometry().x(), self.geometry().y(), ScalingUtils.width(370), ScalingUtils.height(315))

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - # 

    def set_geometry_info(self):
        self.setGeometry(self.geometry().x(), self.geometry().y(), ScalingUtils.width(350), ScalingUtils.height(315))

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - # 

    def set_geometry_edit(self):
        self.setGeometry(self.geometry().x(), self.geometry().y(), ScalingUtils.width(328), ScalingUtils.height(460))

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - # 

    def set_geometry_skins_champions(self):
        self.setGeometry(self.geometry().x(), self.geometry().y(), ScalingUtils.width(1035), ScalingUtils.height(900))


#--------------------------------------------------------------------------------------------------------------------#

    def show_hide_widgets(self, active_widgets: dict):
        for widget_type, widget_dict in [("buttons", self.buttons.created_buttons),
                                        ("line_edits", self.line_edits.created_line_edits),
                                        ("check_boxes", self.check_boxes.created_check_boxes),
                                        ("combo_boxes", self.combo_boxes.created_combo_boxes),
                                        ("labels", self.labels.created_labels)]:
            for widget_name, widget in widget_dict.items():
                for active_widget_dict in active_widgets[widget_type]:
                    if active_widget_dict["object_name"] == widget_name:
                        widget.setVisible(active_widget_dict["show"])
                        break
                else:
                    widget.hide()
