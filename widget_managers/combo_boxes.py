from PyQt5.QtWidgets import QComboBox
from PyQt5.QtGui import QCursor, QFont
from PyQt5.QtCore import Qt
from utilities.scaling_utils import ScalingUtils
from utilities import obj_names, utils



class ComboBoxes:
    def __init__(self, parent) -> None:
        self.parent = parent
        self.__created_combo_boxes = {}
    

    def get_combo_box(self, object_name):
        if object_name in self.__created_combo_boxes:
            return self.__created_combo_boxes[object_name]
        else:
            return None

    def add_combo_box(self, combo_box: QComboBox, object_name: str) -> None:
        self.__created_combo_boxes[object_name] = combo_box

    @property
    def created_combo_boxes(self) -> dict:
        return self.__created_combo_boxes


    def add_account_region(self) -> dict:
        show_widget = True
        object_name = obj_names.ComboBoxNames.ADD_ACCOUNT_REGION.value
        if self.get_combo_box(object_name=object_name):
            pass
            # self.get_combo_box(object_name=object_name).setCurrentIndex(0)
        else:
            add_account_region_combo_box = QComboBox(self.parent)
            add_account_region_combo_box.setObjectName(object_name)
            add_account_region_combo_box.setCursor(QCursor(Qt.PointingHandCursor))
            add_account_region_combo_box.setFont(QFont('AnyStyle', ScalingUtils.get_font_size()))
            add_account_region_combo_box.move(ScalingUtils.width(130), ScalingUtils.height(95))
            add_account_region_combo_box.resize(ScalingUtils.width(170), ScalingUtils.height(40))
            for region in utils.REGIONS:
                add_account_region_combo_box.addItem(region)
            self.add_combo_box(add_account_region_combo_box, object_name)
        return {"object_name":object_name, "show":show_widget}


    def edit_account_region(self) -> dict:
        show_widget = True
        object_name = obj_names.ComboBoxNames.EDIT_ACCOUNT_REGION.value
        index = utils.REGIONS.index(self.parent.account_manager.selected_account.region)
        if self.get_combo_box(object_name=object_name):
            self.get_combo_box(object_name=object_name).setCurrentIndex(index)
        else:
            edit_account_region_combo_box = QComboBox(self.parent)
            edit_account_region_combo_box.setObjectName(object_name)
            edit_account_region_combo_box.setCursor(QCursor(Qt.PointingHandCursor))
            edit_account_region_combo_box.setFont(QFont('AnyStyle', ScalingUtils.get_font_size()))
            edit_account_region_combo_box.move(ScalingUtils.width(130), ScalingUtils.height(95))
            edit_account_region_combo_box.resize(ScalingUtils.width(170), ScalingUtils.height(40))
            for region in utils.REGIONS:
                edit_account_region_combo_box.addItem(region)
            edit_account_region_combo_box.setCurrentIndex(index)
            self.add_combo_box(edit_account_region_combo_box, object_name)
        return {"object_name":object_name, "show":show_widget}