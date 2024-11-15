import importlib
# importlib.reload(outsourcing_pipline.log)
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2 import __version__
from maya.app.general import mayaMixin
import pymel.core as pm
import maya.cmds as cmds
import os
import sys


# 체크리스트??
# 1 파일이름이 최상위 그룹인가.
# 2 중복된 파일이름이 있는가?

class ModelingManagerWindow(mayaMixin.MayaQWidgetBaseMixin, QMainWindow):
    WINDOW_NAME = 'vive_modeling_manager_window_a'

    def __init__(self):
        super(ModelingManagerWindow, self).__init__()
        log.info('모델링 메니져 시작합니다.')
        if pm.window(self.WINDOW_NAME, q=True, ex=True):
            pm.deleteUI(self.WINDOW_NAME, window=True)
        self.setObjectName(self.WINDOW_NAME)
        self.setWindowTitle(self.WINDOW_NAME)
        self.setGeometry(200, 200, 1000, 800)
        self.ui()

    def ui(self):
        print('modeling manager ui start.')
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        frameAppBanner = QFrame()
        frameAppBanner.setStyleSheet('''
                                                            color: #ddd;
                                                            background-color: #000;
                                                            padding: 10px 5px;
                                                            ''')
        frameAppBanner.setGeometry(10, 10, 500, 100)
        frameAppBanner.setFixedHeight(100)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed))
        window_layout = QVBoxLayout(self.centralWidget())
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
        frameAppBannertitle_label = QLabel(u"Modling Manager")
        frameAppBannertitle_label.setStyleSheet('''
                                                font-size: 14pt;
                                                font-family: Nanum Gothic, Malgun Gothic, sans-serif;
                                                font-weight: bold;
                                                padding: 0px;
                                            ''')
        frameAppBannerapp_layout.addWidget(frameAppBannertitle_label)
        # studios
        frameAppBannersub_title_label = QLabel('<b>VIVE</b> STUDIOS')
        frameAppBannersub_title_label.setStyleSheet('''
                                                font-size: 9pt;
                                                padding: 0px;
                                            ''')
        frameAppBannerapp_layout.addWidget(frameAppBannersub_title_label)
        search_filter_layout = QHBoxLayout()
        search_filter_layout.setContentsMargins(0, 0, 0, 0)
        search_filter_layout.setSpacing(6)
        window_layout.addLayout(search_filter_layout)

        # dirve combobox
        self.searchDriveComboBox = QComboBox()
        self.searchDriveComboBox.setStyleSheet('''
                                                        font-size: 14pt; 
                                                        color: black;                               
                                                        border: 1px solid orange;
                                                        background-color: orange;                                
                                                        border-radius: 8px;
                                                        padding: 5px 10px;
                                                        font-weight:bold;
                                                        '''
                                               "QComboBox::drop-down{width:30px;height:30px}"
                                               )
        self.searchDriveComboBox.addItem("-drive-")
        self.searchDriveComboBox.addItem("D:/")
        self.searchDriveComboBox.addItem("V:/")
        self.searchDriveComboBox.addItem("X:/")
        self.searchDriveComboBox.currentIndexChanged.connect(self.searchDriveComboBox_change)
        search_filter_layout.addWidget(self.searchDriveComboBox)
        # project combobox
        self.searchProjectComboBox = QComboBox()
        self.searchProjectComboBox.setStyleSheet('''
                                                                font-size: 14pt; 
                                                                color: black;                               
                                                                border: 1px solid orange;
                                                                background-color: orange;                                
                                                                border-radius: 8px;
                                                                padding: 5px 10px;
                                                                font-weight:bold;
                                                                '''
                                                 "QComboBox::drop-down{width:30px;height:30px}"
                                                 )
        self.searchProjectComboBox.addItem("-project-")
        self.searchProjectComboBox.currentIndexChanged.connect(self.searchProjectComboBox_change)
        search_filter_layout.addWidget(self.searchProjectComboBox)
        # asset combobox
        self.searchAssetTypeComboBox = QComboBox()
        self.searchAssetTypeComboBox.setStyleSheet('''
                                                                        font-size: 14pt; 
                                                                        color: black;                               
                                                                        border: 1px solid orange;
                                                                        background-color: orange;                                
                                                                        border-radius: 8px;
                                                                        padding: 5px 10px;
                                                                        font-weight:bold;
                                                                        '''
                                                   "QComboBox::drop-down{width:30px;height:30px}"
                                                   )
        self.searchAssetTypeComboBox.addItem("-AssetType-")
        self.searchAssetTypeComboBox.currentIndexChanged.connect(self.searchAssetTypeComboBox_change)
        search_filter_layout.addWidget(self.searchAssetTypeComboBox)

        #####################
        # main layout
        #####################
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(7)
        main_layout.setAlignment(Qt.AlignTop)
        window_layout.addLayout(main_layout)
        #####################
        # splitter
        #####################
        self.splitter = QSplitter()
        main_layout.addWidget(self.splitter)
        self.splitter.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.splitter.setOrientation(Qt.Horizontal)
        self.splitter.setSizes([350, 350, 350, 350])
        # self.splitter.splitterMoved.connect(self.on_splitter_moved)
        ####################################################################################################
        # left
        ####################################################################################################
        self.left_frame = QFrame()
        self.splitter.addWidget(self.left_frame)
        task_layout = QVBoxLayout(self.left_frame)
        task_layout.setContentsMargins(10, 0, 10, 0)
        task_layout.setSpacing(5)
        ####################################################################################################
        # mid left
        ####################################################################################################
        self.mid_left_frame = QFrame()
        self.mid_left_frame.setEnabled(True)
        self.splitter.addWidget(self.mid_left_frame)
        work_layout = QVBoxLayout(self.mid_left_frame)
        work_layout.setContentsMargins(10, 0, 0, 0)
        work_layout.setSpacing(3)

        ##################################################
        # mid right
        ##################################################
        mid_right_widget = QWidget()
        self.splitter.addWidget(mid_right_widget)
        task_filter_widget_layout = QVBoxLayout(mid_right_widget)
        task_filter_widget_layout.setContentsMargins(0, 0, 10, 0)
        task_filter_widget_layout.setSpacing(10)
        ##################################################
        # right
        ##################################################
        right_widget = QWidget()
        self.splitter.addWidget(right_widget)
        right_widget_layout = QVBoxLayout(right_widget)
        right_widget_layout.setContentsMargins(0, 0, 10, 0)
        right_widget_layout.setSpacing(10)

        ##################################################
        # left work
        ##################################################
        task_top_layout = QVBoxLayout()
        task_layout.addLayout(task_top_layout)
        task_top_layout.setContentsMargins(0, 0, 0, 0)
        task_top_layout.setSpacing(5)
        cache_exprot_label = QLabel('Rig Task')
        cache_exprot_label.setStyleSheet('font-size: 10pt;')
        task_top_layout.addWidget(cache_exprot_label)
        task_top_layout.addItem(QSpacerItem(5, 0))

        self.task_list_widget = QTableWidget()
        self.task_list_widget.setEnabled(True)
        self.task_list_widget.itemSelectionChanged.connect(self.on_task_list_selection_changed)
        self.task_list_widget.itemDoubleClicked.connect(self.on_task_list_item_double_clicked)
        # self.task_list_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        # self.task_list_widget.customContextMenuRequested.connect(self.task_list_context_menu)
        task_layout.addWidget(self.task_list_widget)

        ##################################################
        # wip 작업 파일 리스트
        ##################################################
        # wip 경로 필드
        layout = QHBoxLayout()
        work_layout.addLayout(layout)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(1)
        layout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        wips_label = QLabel('WIPs')
        wips_label.setStyleSheet('font-size: 10pt;')

        layout.addWidget(wips_label)
        layout.addItem(QSpacerItem(5, 0))

        self.wip_path_field = QLineEdit()
        layout.addWidget(self.wip_path_field)
        self.wip_path_field.setFixedHeight(30)

        # wip 경로 복사하기 버튼
        btn = QPushButton('C')
        # btn.setGeometry(0, 0, 80, 80)
        layout.addWidget(btn)
        btn.setFixedSize(30, 30)
        btn.clicked.connect(self.copy_path_to_clipboard_wip)

        # wip 경로 열기 버튼
        btn = QPushButton('O')
        layout.addWidget(btn)
        btn.setFixedSize(30, 30)
        btn.clicked.connect(self.open_work_path_wip)

        # wip 파일 리스트
        self.wip_list_widget = QListWidget()
        work_layout.addWidget(self.wip_list_widget)
        self.wip_list_widget.itemDoubleClicked.connect(self.on_wip_list_double_clicked)
        self.wip_list_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.wip_list_widget.customContextMenuRequested.connect(self.wip_show_context_menu)
        ################################
        # mid right work
        ################################
        mid_right_layout = QVBoxLayout()
        task_filter_widget_layout.addLayout(mid_right_layout)
        mid_right_layout.setContentsMargins(0, 0, 0, 0)
        mid_right_layout.setSpacing(5)
        check_work_label = QLabel('check work & change work')
        check_work_label.setStyleSheet('font-size: 10pt;')
        mid_right_layout.addWidget(check_work_label)
        mid_right_layout.addItem(QSpacerItem(5, 0))

        check_work_widget = QWidget()
        check_work_layout = QVBoxLayout(check_work_widget)
        check_work_layout.setContentsMargins(0, 0, 0, 0)
        check_work_layout.setSpacing(5)
        mid_right_layout.addWidget(check_work_widget)
        self.check_work_scroll = QScrollArea(check_work_widget)
        self.check_work_scroll.setWidget(QWidget())
        self.check_work_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.check_work_scroll.setFrameShape(QScrollArea.Box)
        self.check_work_scroll.setFrameShadow(QScrollArea.Sunken)
        self.check_work_scroll.setWidgetResizable(True)
        self.check_work_scroll_layout = QVBoxLayout(self.check_work_scroll.widget())
        self.check_work_scroll_layout.setAlignment(Qt.AlignTop)
        self.check_work_scroll_layout.setSpacing(0)
        check_work_layout.addWidget(self.check_work_scroll)
        check_work_run_button = QPushButton('Run _ Check')
        check_work_run_button.clicked.connect(self.check_run05)
        check_work_reset_button = QPushButton('Reset _ Check')
        check_work_reset_button.clicked.connect(self.check_work_reset_run)
        check_work_layout.addWidget(check_work_run_button)
        check_work_layout.addWidget(check_work_reset_button)

        self.check_buttonlist = []
        add_item = CheckWorkDialog('컨테이너 그룹 여부', self.check_run01, parent=self)
        self.check_work_scroll_layout.addWidget(add_item)
        self.check_buttonlist.append(add_item)
        add_item = CheckWorkDialog('geo 그룹 여부', self.check_run02, parent=self)
        self.check_work_scroll_layout.addWidget(add_item)
        self.check_buttonlist.append(add_item)
        add_item = CheckWorkDialog('rig 그룹 여부', self.check_run03, parent=self)
        self.check_work_scroll_layout.addWidget(add_item)
        self.check_buttonlist.append(add_item)
        add_item = CheckWorkDialog('중복 이름의 오브젝트 확인', self.check_run04, parent=self)
        self.check_work_scroll_layout.addWidget(add_item)
        self.check_buttonlist.append(add_item)

        ################################
        # right work
        ################################
        right_script_layout = QVBoxLayout()
        right_widget_layout.addLayout(right_script_layout)
        right_script_layout.setContentsMargins(0, 0, 0, 0)
        right_script_layout.setSpacing(5)
        script_work_label = QLabel('mod change work')
        script_work_label.setStyleSheet('font-size: 10pt;')
        right_script_layout.addWidget(script_work_label)
        right_script_layout.addItem(QSpacerItem(5, 0))

        mod_change_widget = QWidget()
        mod_change_layout = QVBoxLayout(mod_change_widget)
        mod_change_layout.setContentsMargins(0, 0, 0, 0)
        mod_change_layout.setSpacing(5)
        right_script_layout.addWidget(mod_change_widget)

        self.mod_change_scroll = QScrollArea(mod_change_widget)
        self.mod_change_scroll.setWidget(QWidget())
        self.mod_change_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.mod_change_scroll.setFrameShape(QScrollArea.Box)
        self.mod_change_scroll.setFrameShadow(QScrollArea.Sunken)
        self.mod_change_scroll.setWidgetResizable(True)
        self.mod_change_scroll_layout = QVBoxLayout(self.mod_change_scroll.widget())
        self.mod_change_scroll_layout.setAlignment(Qt.AlignTop)
        self.mod_change_scroll_layout.setSpacing(0)
        right_script_layout.addWidget(self.mod_change_scroll)
        find_model_run_button = QPushButton('Find Model Asset')
        find_model_run_button.clicked.connect(self.find_model_button_run)
        mod_change_layout.addWidget(find_model_run_button)

    def searchDriveComboBox_change(self):
        pass

    def searchProjectComboBox_change(self):
        pass

    def searchAssetTypeComboBox_change(self):
        pass

    def on_task_list_selection_changed(self):
        pass

    def on_task_list_item_double_clicked(self):
        pass

    def copy_path_to_clipboard_wip(self):
        pass

    def open_work_path_wip(self):
        pass

    def on_wip_list_double_clicked(self):
        pass

    def wip_show_context_menu(self):
        pass

    def check_run05(self):
        pass

    def check_work_reset_run(self):
        pass

    def check_run01(self):
        pass

    def check_run02(self):
        pass

    def check_run03(self):
        pass

    def check_run04(self):
        pass

    def find_model_button_run(self):
        pass


def show_window():
    global ModelingManagerWindow
    try:
        ModelingManagerWindow.close()
        ModelingManagerWindow.deleteLater()
    except:
        pass
    modelingmanagerwin = ModelingManagerWindow()
    modelingmanagerwin.show()


show_window()