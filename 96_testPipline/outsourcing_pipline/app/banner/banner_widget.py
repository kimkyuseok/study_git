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
from banner_model import *


class _AbstractBannerWidget(QtWidgets.QWidget):

    def __init__(self, after_script=None):
        super().__init__()
        self.ui()

    def ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.main_layout.setAlignment(Qt.AlignTop)

    def add_banner_class(self, BannerClass, *args, **kwargs):
        banner_class_A = BannerClass(*args, **kwargs)
        self.main_layout.addWidget(banner_class_A)


# 앱스트랙트 베너 위젯에 베너 클레스 추가
class showWidget_addItem(_AbstractBannerWidget):
    def __init__(self):
        super().__init__()
        self.add_banner_class(banner_modelingTool)
