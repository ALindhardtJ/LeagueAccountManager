from utilities.scaling_utils import ScalingUtils
from PyQt5.QtWidgets import QCheckBox
from utilities import obj_names
from PyQt5.QtWidgets import QLineEdit



class CheckBoxes:
    def __init__(self, parent) -> None:
        self.parent = parent
        self.check_box_actions = CheckBoxActions(parent=parent)
        self.__created_check_boxes = {}
    
    def get_check_box(self, object_name):
        if object_name in self.__created_check_boxes:
            return self.__created_check_boxes[object_name]
        else:
            return None

    def add_check_box(self, check_box: QCheckBox, object_name: str) -> None:
        self.__created_check_boxes[object_name] = check_box

    @property
    def created_check_boxes(self) -> dict:
        return self.__created_check_boxes


    def add_account_password(self) -> dict:
        show_widget = True
        object_name = obj_names.CheckBoxNames.ADD_ACCOUNT_PASSWORD.value
        if self.get_check_box(object_name=object_name):
            self.get_check_box(object_name=object_name).setChecked(False)
        else:
            pass_check_box = QCheckBox(self.parent)
            pass_check_box.setObjectName(object_name)
            pass_check_box.setText("Show Password")
            pass_check_box.stateChanged.connect(self.check_box_actions.add_account_password_clicked)
            pass_check_box.move(ScalingUtils.width(15), ScalingUtils.height(345))
            self.add_check_box(pass_check_box, object_name)
        return {"object_name":object_name, "show":show_widget}


    def edit_account_password(self) -> dict:
        show_widget = True
        object_name = obj_names.CheckBoxNames.EDIT_ACCOUNT_PASSWORD.value
        if self.get_check_box(object_name=object_name):
            self.get_check_box(object_name=object_name).setChecked(False)
        else:
            pass_check_box = QCheckBox(self.parent)
            pass_check_box.setObjectName(object_name)
            pass_check_box.setText("Show Password")
            pass_check_box.stateChanged.connect(self.check_box_actions.edit_account_password_clicked)
            pass_check_box.move(ScalingUtils.width(15), ScalingUtils.height(345))
            self.add_check_box(pass_check_box, object_name)
        return {"object_name":object_name, "show":show_widget}   

    
    def info_account_password(self) -> dict:
        show_widget = True
        object_name = obj_names.CheckBoxNames.INFO_ACCOUNT_PASSWORD.value
        if self.get_check_box(object_name=object_name):
            self.get_check_box(object_name=object_name).setChecked(False)
        else:
            pass_check_box = QCheckBox(self.parent)
            pass_check_box.setObjectName(object_name)
            pass_check_box.setText("Show Password")
            pass_check_box.stateChanged.connect(self.check_box_actions.info_account_password_clicked)
            pass_check_box.move(ScalingUtils.width(15), ScalingUtils.height(270))
            self.add_check_box(pass_check_box, object_name)
        return {"object_name":object_name, "show":show_widget}



class CheckBoxActions:
    def __init__(self, parent) -> None:
        self.parent = parent


    def add_account_password_clicked(self):
        line_edit = self.parent.line_edits.get_line_edit(obj_names.LineEditNames.ADD_ACCOUNT_PASSWORD.value)
        if line_edit.echoMode() == QLineEdit.Normal:
            line_edit.setEchoMode(QLineEdit.Password)
        else:
            line_edit.setEchoMode(QLineEdit.Normal)


    def edit_account_password_clicked(self):
        line_edit = self.parent.line_edits.get_line_edit(obj_names.LineEditNames.EDIT_ACCOUNT_PASSWORD.value)
        if line_edit.echoMode() == QLineEdit.Normal:
            line_edit.setEchoMode(QLineEdit.Password)
        else:
            line_edit.setEchoMode(QLineEdit.Normal)


    def info_account_password_clicked(self): 
        line_edit = self.parent.line_edits.get_line_edit(obj_names.LineEditNames.INFO_PASSWORD.value)
        if line_edit.echoMode() == QLineEdit.Normal:
            line_edit.setEchoMode(QLineEdit.Password)
        else:
            line_edit.setEchoMode(QLineEdit.Normal)