from PyQt5.QtGui import QGuiApplication
from math import ceil

class ScalingUtils:
    @staticmethod
    def get_screen_size():
        screen = QGuiApplication.primaryScreen()
        return screen.size()

    @staticmethod
    def get_rect():
        screen = QGuiApplication.primaryScreen()
        return screen.availableGeometry()

    @staticmethod
    def get_font_size():
        if str(ScalingUtils.get_screen_size()) == "PyQt5.QtCore.QSize(2560, 1440)":
            font_size = 13
            return font_size
        elif str(ScalingUtils.get_screen_size()) == "PyQt5.QtCore.QSize(1920, 1080)":
            font_size = 10
            return font_size

    @staticmethod
    def width(value):
        if str(ScalingUtils.get_screen_size()) == "PyQt5.QtCore.QSize(2560, 1440)":
            new_value = (value / 2560)
            end_value = (int(ScalingUtils.get_rect().width()) * new_value)
            return ceil(end_value)
        elif str(ScalingUtils.get_screen_size()) == "PyQt5.QtCore.QSize(1920, 1080)":
            new_value = (value / 2560)
            end_value = (int(ScalingUtils.get_rect().width()) * new_value)
            end_end_value = (end_value * 1.5)
            return ceil(end_end_value)

    @staticmethod
    def height(value):
        if str(ScalingUtils.get_screen_size()) == "PyQt5.QtCore.QSize(2560, 1440)":
            new_value = (value / 1400)
            end_value = (int(ScalingUtils.get_rect().height()) * new_value)
            return ceil(end_value)

        elif str(ScalingUtils.get_screen_size()) == "PyQt5.QtCore.QSize(1920, 1080)":
            new_value = (value / 1400)
            end_value = (int(ScalingUtils.get_rect().height()) * new_value)
            end_end_value = (end_value * 1.5)
            return ceil(end_end_value)

    @staticmethod
    def x_pos(value):
        if str(ScalingUtils.get_screen_size()) == "PyQt5.QtCore.QSize(2560, 1440)":
            new_value = (value / 2560)
            end_value = (int(ScalingUtils.get_rect().width()) * new_value)
            return ceil(end_value)

        elif str(ScalingUtils.get_screen_size()) == "PyQt5.QtCore.QSize(1920, 1080)":            
            new_value = (value / 2560)
            end_value = (int(ScalingUtils.get_rect().width()) * new_value)
            return ceil(end_value)

    @staticmethod
    def y_pos(value):
        if str(ScalingUtils.get_screen_size()) == "PyQt5.QtCore.QSize(2560, 1440)":
            new_value = (value / 1400)
            end_value = (int(ScalingUtils.get_rect().height()) * new_value)
            return ceil(end_value)        

        elif str(ScalingUtils.get_screen_size()) == "PyQt5.QtCore.QSize(1920, 1080)":
            new_value = (value / 1400)
            end_value = (int(ScalingUtils.get_rect().height()) * new_value)
            return ceil(end_value)