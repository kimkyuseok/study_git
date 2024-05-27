import os
import re
import pyperclip
import shutil
# importlib.reload(outsourcing_pipline.log)
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from maya.app.general import mayaMixin
import pymel.core as pm
import maya.cmds as cmds


class CFXManagerWindow(mayaMixin.MayaQWidgetBaseMixin, QMainWindow):
    WINDOW_NAME = 'cfx_manager_window_a'
    OPTIONVAR_TASKMANAGER_A = 'optionvar_cfx_manager_a'

    def __init__(self):
        super(CFXManagerWindow, self).__init__()
        if pm.window(self.WINDOW_NAME, q=True, ex=True):
            pm.deleteUI(self.WINDOW_NAME, window=True)
        self.setObjectName(self.WINDOW_NAME)
        self.setWindowTitle(self.WINDOW_NAME)
        self.setGeometry(200, 200, 1700, 800)
        self.ui()

    def ui(self):
        print('task manager ui start.')
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
        frameAppBannertitle_label = QLabel(u"CFX Manager")
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
        #frameAppBannermain_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding))
        ####################################################################################################
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

        # squence combobox
        self.searchSequenceTypeComboBox = QComboBox()
        self.searchSequenceTypeComboBox.setStyleSheet('''
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
        self.searchSequenceTypeComboBox.addItem("-Sequence-")
        self.searchSequenceTypeComboBox.setMaxVisibleItems(12)
        self.searchSequenceTypeComboBox.currentIndexChanged.connect(self.searchSequenceTypeComboBox_change)
        search_filter_layout.addWidget(self.searchSequenceTypeComboBox)

        # task combobox
        self.searchTaskTypeComboBox = QComboBox()
        self.searchTaskTypeComboBox.setStyleSheet('''
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
        self.searchTaskTypeComboBox.addItem("-CutTask-")
        self.searchTaskTypeComboBox.setMaxVisibleItems(12)
        self.searchTaskTypeComboBox.currentIndexChanged.connect(self.searchTaskTypeComboBox_change)
        search_filter_layout.addWidget(self.searchTaskTypeComboBox)

        #####################
        # 메인 레이아웃
        #####################
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(5)
        main_layout.setAlignment(Qt.AlignTop)
        window_layout.addLayout(main_layout)
        #####################
        # 스플리터
        #####################
        self.splitter = QSplitter()
        main_layout.addWidget(self.splitter)
        self.splitter.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.splitter.setOrientation(Qt.Horizontal)
        # self.splitter.splitterMoved.connect(self.on_splitter_moved)

        ####################################################################################################
        # left
        ####################################################################################################
        self.work_frame = QFrame()
        self.work_frame.setEnabled(True)
        self.splitter.addWidget(self.work_frame)
        work_layout = QVBoxLayout(self.work_frame)
        work_layout.setContentsMargins(10, 0, 0, 0)
        work_layout.setSpacing(3)
        ####################################################################################################
        # mid
        ####################################################################################################
        self.task_frame = QFrame()
        self.splitter.addWidget(self.task_frame)
        task_layout = QVBoxLayout(self.task_frame)
        task_layout.setContentsMargins(10, 0, 10, 0)
        task_layout.setSpacing(5)
        ##################################################
        # right
        ##################################################
        task_filter_widget = QWidget()
        self.splitter.addWidget(task_filter_widget)
        task_filter_widget_layout = QVBoxLayout(task_filter_widget)
        task_filter_widget_layout.setContentsMargins(0, 0, 10, 0)
        task_filter_widget_layout.setSpacing(10)
        ##################################################
        # right work
        ##################################################
        task_top_layout = QVBoxLayout()
        task_filter_widget_layout.addLayout(task_top_layout)
        task_top_layout.setContentsMargins(0, 0, 0, 0)
        task_top_layout.setSpacing(5)
        cache_export_save_find_button = QPushButton(' File SAVE (and) Yetti FIND ')
        task_top_layout.addWidget(cache_export_save_find_button)
        task_top_layout.addItem(QSpacerItem(5, 0))

        cache_exprot_label = QLabel('CFX Cache EXPORT')
        cache_exprot_label.setStyleSheet('font-size: 10pt;')
        task_top_layout.addWidget(cache_exprot_label)
        task_top_layout.addItem(QSpacerItem(5, 0))

        cache_exprt_button_layout = QHBoxLayout()
        task_top_layout.addLayout(cache_exprt_button_layout)
        cache_exprt_button_layout.setContentsMargins(0, 0, 0, 0)
        cache_exprt_button_layout.setSpacing(5)
        #
        cache_export_button = QPushButton(' Yetti Cache Export START ')
        cache_exprt_button_layout.addWidget(cache_export_button)
        #
        cache_open_folder_button = QPushButton(' Yetti Cache Folder OPEN ')
        cache_exprt_button_layout.addWidget(cache_open_folder_button)


        ##################################################
        # mid work
        ##################################################
        layout = QVBoxLayout()
        task_layout.addLayout(layout)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(1)
        layout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        AniCache_label = QLabel('Ani Cache IMPORT')
        AniCache_label.setStyleSheet('font-size: 10pt;')
        layout.addWidget(AniCache_label)
        layout.addItem(QSpacerItem(5, 0))
        cfx_label = QLabel('CFX SET IMPORT')
        cfx_label.setStyleSheet('font-size: 10pt;')
        layout.addWidget(cfx_label)
        layout.addItem(QSpacerItem(5, 0))

        ##################################################
        # wip work
        ##################################################
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
        # wip path copy
        btn = QPushButton('C')
        # btn.setGeometry(0, 0, 80, 80)
        layout.addWidget(btn)
        btn.setFixedSize(30, 30)
        btn.clicked.connect(self.copy_path_to_clipboard_wip)
        # wip open folder
        btn = QPushButton('O')
        layout.addWidget(btn)
        btn.setFixedSize(30, 30)
        btn.clicked.connect(self.open_work_path_wip)
        # wip file list
        self.wip_list_widget = QListWidget()
        work_layout.addWidget(self.wip_list_widget)
        # self.wip_list_widget.itemSelectionChanged.connect(self.on_wip_list_selection_changed)
        # self.wip_list_widget.doubleClicked.connect(self.on_wip_list_double_clicked)
        self.wip_list_widget.itemDoubleClicked.connect(self.on_wip_list_double_clicked)
        self.wip_list_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.wip_list_widget.customContextMenuRequested.connect(self.wip_show_context_menu)

        self.splitter.setSizes([500, 450, 450])

    def searchDriveComboBox_change(self):
        print('dirve - searchDriveComboBox_change')
        pass

    def searchProjectComboBox_change(self):
        print('project - searchProjectComboBox_change')
        pass

    def searchSequenceTypeComboBox_change(self):
        print('Sequence - searchSequenceTypeComboBox_change')
        pass

    def searchTaskTypeComboBox_change(self):
        print('CutTask - searchTaskTypeComboBox_change')
        pass

    def copy_path_to_clipboard_wip(self):
        pass

    def open_work_path_wip(self):
        pass

    def on_wip_list_double_clicked(self):
        pass

    def wip_show_context_menu(self):
        pass


def show_window():
    global CFXManagerWindow

    try:
        CFXManagerWindow.close()
        CFXManagerWindow.deleteLater()
    except:
        pass

    cfxmanagerwin = CFXManagerWindow()
    cfxmanagerwin.show()
