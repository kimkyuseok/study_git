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

"""
# Maya 메인 윈도우를 QtWidgets.QWidget으로 변환
def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)
"""

# 체크 리스트 클레스 변형 해서 매번 만드는 베너를 클레스 생성
# 어떠한 이름을 가질수 있는 베너 클레스 +_+
# 타이틀 과 회사 이름을 넣을수 있음!
# 상속과 뷰어로 사용 되므로 시그널 같은거 불필요
# 베너 클래스 정의


class BannerClass(QtWidgets.QFrame):
    # 시그널 필요없음
    # pyqtSignal(str, object)
    # error_button_clicked = Signal(str, list)
    # error_button_clicked = Signal(object, object)

    def __init__(self, tool_name, vendor_name=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__tool_name = tool_name
        self.__vendor_name = vendor_name
        self.ui()

    def ui(self):
        print(f" 불러오는지 테스트 : {self.__tool_name },{self.__vendor_name}")
        main_widget = QWidget(self)
        #self.setCentralWidget(main_widget)
        frameAppBanner = QFrame(self)
        frameAppBanner.setStyleSheet('''
                                                                    color: #ddd;
                                                                    background-color: #000;
                                                                    padding: 10px 5px;
                                                                    ''')
        frameAppBanner.setGeometry(10, 10, 500, 100)
        frameAppBanner.setFixedHeight(100)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed))
        window_layout = QVBoxLayout(main_widget)
        window_layout.setContentsMargins(0, 0, 0, 0)
        window_layout.setSpacing(0)
        window_layout.setAlignment(Qt.AlignTop)
        main_widget.setLayout(window_layout)
        window_layout.addWidget(frameAppBanner)
        # --------- B a n n e r
        # manin layout : QHBoxLayout
        frameAppBannermain_layout = QHBoxLayout(frameAppBanner)
        frameAppBannermain_layout.setContentsMargins(10, 0, 0, 0)
        frameAppBannermain_layout.setSpacing(10)
        frameAppBannermain_layout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        # window_layout.addLayout(frameAppBanner)
        # app & studios
        frameAppBannerapp_layout = QVBoxLayout()
        frameAppBannerapp_layout.setSpacing(0)
        frameAppBannerapp_layout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        frameAppBannermain_layout.addLayout(frameAppBannerapp_layout)
        # app
        frameAppBannertitle_label = QLabel(self.__tool_name)
        frameAppBannertitle_label.setStyleSheet('''
                                                        font-size: 14pt;
                                                        font-family: Nanum Gothic, Malgun Gothic, sans-serif;
                                                        font-weight: bold;
                                                        padding: 0px;
                                                    ''')
        frameAppBannerapp_layout.addWidget(frameAppBannertitle_label)
        # studios
        frameAppBannersub_title_label = QLabel(self.__vendor_name)
        frameAppBannersub_title_label.setStyleSheet('''
                                                        font-size: 9pt;
                                                        padding: 0px;
                                                    ''')
        frameAppBannerapp_layout.addWidget(frameAppBannersub_title_label)
        search_filter_layout = QHBoxLayout()
        search_filter_layout.setContentsMargins(0, 0, 0, 0)
        search_filter_layout.setSpacing(6)
        window_layout.addLayout(search_filter_layout)
        # 최종 레이아웃 설정
        self.setLayout(window_layout)

# 빈 베너에  내용물을 채워 넣었고!
class banner_modelingTool(BannerClass):

    def __init__(self):
        # 부모 클래스의 __init__ 메서드 호출
        super().__init__(
            tool_name='Modling Manager',
            vendor_name='<b>VIVE</b> STUDIOS',
        )

    # 앱스트랙트 베너 위젯


"""
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

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        main_layout.setAlignment(Qt.AlignTop)
        window_layout.addLayout(main_layout)

        main_layout.addWidget(self.banner_class)


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
"""