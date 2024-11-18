import maya.cmds as cmds
import maya.OpenMayaUI as omui
from shiboken2 import wrapInstance
from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import os
import json
import re
import traceback
# Maya 메인 윈도우를 QtWidgets.QWidget으로 변환
from banner_widget import *
from banner_model import *

def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)

# 대화상자 위젯
class widgetsUI(QtWidgets.QDialog):
    def __init__(self, banner_class, app_name, parent=None):
        super().__init__(parent)  # 부모를 Maya 메인 윈도우로 설정
        self.banner_class = banner_class
        self.app_name = app_name
        self.ui()

    def ui(self):
        self.setWindowTitle(self.app_name)
        self.setMinimumWidth(500)
        self.setMinimumHeight(700)

        window_layout = QVBoxLayout(self)
        window_layout.setContentsMargins(0, 0, 0, 0)
        window_layout.setSpacing(0)
        window_layout.setAlignment(Qt.AlignTop)
        banner_class = self.banner_class()
        window_layout.addWidget(banner_class)


# 대화상자 표시 함수
def show_window():
    global widgetsUI
    try:
        widgetsUI.close()
    except:
        pass

    # Maya의 메인 윈도우를 부모로 설정하여 대화상자 띄우기
    parent = maya_main_window()
    widgetsui = widgetsUI(banner_class=showWidget_addItem, app_name='모델링 tool', parent=parent)
    widgetsui.show()


# 대화상자 열기
show_window()
