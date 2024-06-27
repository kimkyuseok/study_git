import os
import re
import pyperclip
import shutil
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from maya.app.general import mayaMixin
import pymel.core as pm
import maya.cmds as cmds


class AddWipVersionDialog(QDialog):
    def __init__(self, text_a, test_b=None, test_c=None, parent=None):
        super().__init__(parent)
        self.textA = text_a
        self.setWindowTitle('Wip Version Add')
        self.setFixedSize(400, 300)
        layout = QVBoxLayout()
        # a
        self.label_a = QLabel('v000 version add : (ex 999)', self)
        layout.addWidget(self.label_a)
        self.lineEdit_a = QLineEdit(self)
        layout.addWidget(self.lineEdit_a)
        if test_b:
            self.lineEdit_a.setText(test_b)
        # b
        self.label_b = QLabel('w00 version add : (ex 99)', self)
        layout.addWidget(self.label_b)
        self.lineEdit_b = QLineEdit(self)
        layout.addWidget(self.lineEdit_b)
        if test_c:
            self.lineEdit_b.setText(test_c)
        # c
        self.label_c = QLabel(' version  : ', self)
        layout.addWidget(self.label_c)
        self.lineEdit_c = QLineEdit(self)
        layout.addWidget(self.lineEdit_c)
        # ok
        self.button = QPushButton('check', self)
        self.button.clicked.connect(self.accept)
        layout.addWidget(self.button)
        #
        self.lineEdit_a.textChanged.connect(self.update_result)
        self.lineEdit_b.textChanged.connect(self.update_result)
        self.setLayout(layout)
        self.update_result()

    def update_result(self):
        text1 = self.textA
        text2 = self.lineEdit_a.text()
        text3 = self.lineEdit_b.text()
        #
        self.lineEdit_c.setText(f'{text1}_v{text2}_w{text3}.mb')

    def get_number(self):
        return self.lineEdit_c.text()


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
        # main layout
        #####################
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(5)
        main_layout.setAlignment(Qt.AlignTop)
        window_layout.addLayout(main_layout)
        #####################
        # splitter
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
        cache_exprot_label = QLabel('CFX Cache EXPORT')
        cache_exprot_label.setStyleSheet('font-size: 10pt;')
        task_top_layout.addWidget(cache_exprot_label)
        task_top_layout.addItem(QSpacerItem(5, 0))
        #################################################
        cfx_export_widget = QWidget()
        cfx_export_layout = QVBoxLayout(cfx_export_widget)
        cfx_export_layout.setContentsMargins(0, 0, 0, 0)
        cfx_export_layout.setSpacing(5)
        task_top_layout.addWidget(cfx_export_widget)
        self.cfx_export_scroll = QScrollArea(cfx_export_widget)
        self.cfx_export_scroll.setWidget(QWidget())
        self.cfx_export_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.cfx_export_scroll.setFrameShape(QScrollArea.Box)
        self.cfx_export_scroll.setFrameShadow(QScrollArea.Sunken)
        self.cfx_export_scroll.setWidgetResizable(True)
        self.cfx_export_scroll_layout = QVBoxLayout(self.cfx_export_scroll.widget())
        self.cfx_export_scroll_layout.setAlignment(Qt.AlignTop)
        self.cfx_export_scroll_layout.setSpacing(0)
        self.save_yeti_find_btn = QPushButton('file save (and) yetti find')
        self.save_yeti_find_btn.clicked.connect(self.filesave_yettifind)
        self.save_yeti_find_btn.setFixedHeight(40)
        cfx_export_layout.addWidget(self.save_yeti_find_btn)
        cfx_export_layout.addWidget(self.cfx_export_scroll)

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

        #################################################
        ani_cache_widget = QWidget()
        ani_cache_layout = QVBoxLayout(ani_cache_widget)
        ani_cache_layout.setContentsMargins(0, 0, 0, 0)
        ani_cache_layout.setSpacing(5)
        layout.addWidget(ani_cache_widget)
        self.ani_cache_scroll = QScrollArea(ani_cache_widget)
        self.ani_cache_scroll.setWidget(QWidget())
        self.ani_cache_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.ani_cache_scroll.setFrameShape(QScrollArea.Box)
        self.ani_cache_scroll.setFrameShadow(QScrollArea.Sunken)
        self.ani_cache_scroll.setWidgetResizable(True)
        self.ani_cache_scroll_layout = QVBoxLayout(self.ani_cache_scroll.widget())
        self.ani_cache_scroll_layout.setAlignment(Qt.AlignTop)
        self.ani_cache_scroll_layout.setSpacing(0)
        self.get_ani_cache_btn = QPushButton('get animation cache')
        self.get_ani_cache_btn.clicked.connect(self.get_ani_cache_btn_run)
        self.get_ani_cache_btn.setFixedHeight(40)
        ani_cache_layout.addWidget(self.get_ani_cache_btn)
        ani_cache_layout.addWidget(self.ani_cache_scroll)
        #################################################
        cfx_label = QLabel('CFX SET IMPORT')
        cfx_label.setStyleSheet('font-size: 10pt;')
        layout.addWidget(cfx_label)
        layout.addItem(QSpacerItem(5, 0))
        #################################################
        cfx_setting_widget = QWidget()
        cfx_setting_layout = QVBoxLayout(cfx_setting_widget)
        cfx_setting_layout.setContentsMargins(0, 0, 0, 0)
        cfx_setting_layout.setSpacing(5)
        layout.addWidget(cfx_setting_widget)
        self.cfx_setting_scroll = QScrollArea(cfx_setting_widget)
        self.cfx_setting_scroll.setWidget(QWidget())
        self.cfx_setting_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.cfx_setting_scroll.setFrameShape(QScrollArea.Box)
        self.cfx_setting_scroll.setFrameShadow(QScrollArea.Sunken)
        self.cfx_setting_scroll.setWidgetResizable(True)
        self.cfx_setting_scroll_layout = QVBoxLayout(self.cfx_setting_scroll.widget())
        self.cfx_setting_scroll_layout.setAlignment(Qt.AlignTop)
        self.cfx_setting_scroll_layout.setSpacing(0)
        # self.get_cfx_setting_btn = QPushButton('')
        # self.get_cfx_setting_btn.clicked.connect(self.import_btn_connect)
        # self.get_cfx_setting_btn.setFixedHeight(40)
        # cfx_setting_layout.addWidget(self.get_cfx_setting_btn)
        cfx_setting_layout.addWidget(self.cfx_setting_scroll)


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
        selected_item = self.searchDriveComboBox.currentText()
        print(f' select drive : {selected_item}')
        vfx_folder = os.path.join(selected_item, 'vfx')
        if os.path.exists(vfx_folder):
            subfolders = [f for f in os.listdir(vfx_folder) if os.path.isdir(os.path.join(vfx_folder, f))]
            print(subfolders)
            if subfolders:
                self.searchProjectComboBox.clear()
                self.searchProjectComboBox.addItem('-project-')
                for i in subfolders:
                    self.searchProjectComboBox.addItem(i)
        pass

    def searchProjectComboBox_change(self):
        print('project - searchProjectComboBox_change')
        selected_drive_item = self.searchDriveComboBox.currentText()
        selected_project_item = self.searchProjectComboBox.currentText()
        print(f' select project : {selected_project_item}')
        vfx_folder = os.path.join(selected_drive_item, 'vfx', selected_project_item, 'shot')
        if os.path.exists(vfx_folder):
            subfolders = [f for f in os.listdir(vfx_folder) if os.path.isdir(os.path.join(vfx_folder, f))]
            print(subfolders)
            if subfolders:
                self.searchSequenceTypeComboBox.clear()
                self.searchSequenceTypeComboBox.addItem('-sequence-')
                for i in subfolders:
                    self.searchSequenceTypeComboBox.addItem(i)
        pass

    def searchSequenceTypeComboBox_change(self):
        print('Sequence - searchSequenceTypeComboBox_change')
        selected_drive_item = self.searchDriveComboBox.currentText()
        selected_project_item = self.searchProjectComboBox.currentText()
        selected_sequence_item = self.searchSequenceTypeComboBox.currentText()
        print(f' select project : {selected_sequence_item}')
        vfx_folder = os.path.join(selected_drive_item, 'vfx', selected_project_item, 'shot', selected_sequence_item)
        if os.path.exists(vfx_folder):
            subfolders = [f for f in os.listdir(vfx_folder) if os.path.isdir(os.path.join(vfx_folder, f))]
            if subfolders:
                self.searchTaskTypeComboBox.clear()
                self.searchTaskTypeComboBox.addItem('- cut task -')
                for i in subfolders:
                    if os.path.exists(os.path.join(vfx_folder, i, 'ani')):
                        self.searchTaskTypeComboBox.addItem(i)
        pass

    def searchTaskTypeComboBox_change(self):
        print('CutTask - searchTaskTypeComboBox_change')
        wip_path = None
        s_drive_i = self.searchDriveComboBox.currentText()
        s_project_i = self.searchProjectComboBox.currentText()
        s_sequence_i = self.searchSequenceTypeComboBox.currentText()
        s_task_i = self.searchTaskTypeComboBox.currentText()
        wip_path = os.path.join(s_drive_i, 'vfx', s_project_i, 'shot', s_sequence_i,
                                s_task_i, 'cfx', 'wip', 'scenes')
        wip_path = wip_path.replace(':/', ':\\')
        self.wip_path_field.setText(wip_path)
        self.wip_list_widget.clear()
        self.set_path_field(self.wip_list_widget, wip_path, r"(.*?)_v(\d{3})_w(\d{2}).mb")
        pass

    def copy_path_to_clipboard_wip(self):
        print('wip path copy - copy_path_to_clipboard_wip')
        pass

    def open_work_path_wip(self):
        print('wip file path open - open_work_path_wip')
        field_a = self.wip_path_field
        path = field_a.text()
        self.open_work_path_a(path)
        pass

    def on_wip_list_double_clicked(self, item):
        wip_file_path = self.wip_path_field.text()
        # wip_select_file = self.wip_list_widget.selected
        print(f'{wip_file_path} {item.text()}')
        file_name = os.path.join(wip_file_path, item.text())
        if os.path.isfile(file_name):
            cmds.file(file_name, force=True, open=True, prompt=False, ignoreVersion=True, type='mayaBinary')
        pass

    def wip_show_context_menu(self, position):
        print('mouse right button  - wip_show_context_menu')
        # right menu
        menu = QMenu()
        checkStart = False
        if self.wip_list_widget.count() == 1:
            item = self.wip_list_widget.item(0)
            if item.text()[0] == 'N':
                checkStart = True
        elif self.wip_list_widget.count() == 0:
            checkStart = True
        else:
            pass
        if checkStart:
            action = QAction(" Fist Working Environment Setup ", self)
            action.triggered.connect(self.wip_right_fist_working_setup)
            menu.addAction(action)
            menu.addSeparator()

        action = QAction(" wip copy folder path", self)
        action.triggered.connect(self.wip_right_wip_copy_path)
        menu.addAction(action)

        action = QAction(" wip folder open", self)
        action.triggered.connect(self.wip_right_open_folder)
        menu.addAction(action)
        menu.addSeparator()

        if self.wip_list_widget.selectedItems():
            action = QAction(" file open ", self)
            action.triggered.connect(self.wip_right_file_open)
            menu.addAction(action)

            action = QAction(" copy  & +1 add version", self)
            action.triggered.connect(self.wip_right_add_version)
            menu.addAction(action)
            menu.addSeparator()
        menu.exec_(self.wip_list_widget.mapToGlobal(position))
        pass

    def create_empty_file(self, directroy, filename):
        if not os.path.exists(directroy):
            os.makedirs(directroy)
        file_path = os.path.join(directroy, filename)
        with open(file_path,'w') as file:
            pass

    def create_directoryi(self,path):
        print(path)
        if not os.path.exists(path):
            os.makedirs(path)

    def wip_right_fist_working_setup(self):
        print(f' 최초작업시작 cfx')
        s_task_i = self.searchTaskTypeComboBox.currentText()
        get_wip_path = self.wip_path_field.text()
        self.create_directoryi(get_wip_path)
        new_file_name = f'{s_task_i}_cfx_v001_w01.mb'
        self.create_empty_file(get_wip_path,new_file_name)
        self.set_path_field(self.wip_list_widget, get_wip_path, r"(.*?)_v(\d{3})_w(\d{2}).mb")
        # 파일열지 물어보기?

    def set_path_field(self, field_a, path_a, pattern_a):
        # field and path and pattern
        # wip_list_widget , pub_list_widget
        if os.path.isdir(path_a):
            items = os.listdir(path_a)
            field_a.clear()
            for item in items:
                if re.match(pattern_a, item):
                    print(f'{item}')
                    add_item = QListWidgetItem(item)
                    field_a.addItem(add_item)
            if len(items) == 0:
                add_item = QListWidgetItem('None Data')
                field_a.addItem(add_item)
        else:
            field_a.clear()
            add_item = QListWidgetItem('None Folder')
            field_a.addItem(add_item)

    def copy_path_to_clipboard_wip(self):
        print(f' wip path field')
        field_a = self.wip_path_field
        path = field_a.text()
        print(f'{path}')
        self.copy_path_to_clipboard(path)

    def copy_path_to_clipboard(self, text_a):
        path = text_a
        if path == '':
            return
        if not os.path.isdir(path):
            os.makedirs(path)
        pyperclip.copy(path)

    def open_work_path_a(self, text_a):
        path = text_a
        if os.path.isdir(path):
            os.startfile(path)
        else:
            print(f' None Folder ')

    def wip_right_wip_copy_path(self):
        print(f'  wip folder path copy')
        self.copy_path_to_clipboard_wip()

    def wip_right_open_folder(self):
        print(f' wip folder open')
        self.open_work_path_wip()

    def wip_right_file_open(self):
        print(f' file open - wip right button')
        self.file_open(self.wip_path_field,self.wip_list_widget)

    def wip_right_add_version(self):
        print(f'  wip right add version')
        folder_path = self.wip_path_field.text()
        items = self.wip_list_widget.selectedItems()
        wip_path = items[0].text()
        print(f"{wip_path.split('_v' ,1)}")
        text_a = wip_path.split('_v',1)[0]
        text_b = wip_path.split('_v',1)[1].split('_w',1)[0]
        text_c = wip_path.split('_v', 1)[1].split('_w', 1)[1]
        text_c = text_c.replace('.mb','')
        text_c = f'{(int(text_c) + 1):02d}'
        dialog = AddWipVersionDialog(text_a, text_b, text_c, self)
        old_path = os.path.join(folder_path,wip_path)
        if dialog.exec_():
            num_str_list = dialog.get_number()
            new_path = os.path.join(folder_path,num_str_list)
            print(f' copy . :{old_path} -> {new_path}')
            shutil.copy(old_path,new_path)
            self.set_path_field(self.wip_list_widget, self.wip_path_field.text(), r"(.*?)_v(\d{3})_w(\d{2}).mb")
        pass
    def get_ani_cache_btn_run(self):
        print(' get element ')
        self.list_layout_item_remove(self.ani_cache_scroll_layout)
        self.list_layout_item_remove(self.cfx_setting_scroll_layout)
        s_drive_i = self.searchDriveComboBox.currentText()
        s_project_i = self.searchProjectComboBox.currentText()
        s_sequence_i = self.searchSequenceTypeComboBox.currentText()
        s_task_i = self.searchTaskTypeComboBox.currentText()
        main_path = os.path.join(s_drive_i, 'vfx', s_project_i, 'shot', s_sequence_i, s_task_i)
        mm_cam_path = os.path.join(main_path, 'mm', 'pub', 'cam', 'versions')
        if os.path.exists(mm_cam_path):
            items = os.listdir(mm_cam_path)
            pattern = re.compile(r"(.*?)_v(\d{3}).abc")
            highest_v = -1
            highest_file = None
            versions = []
            for i in os.listdir(mm_cam_path):
                mach = pattern.match(i)
                if mach:
                    versions.append(i)
                    version = int(mach.group(2))
                    if version > highest_v:
                        highest_v = version
                        highest_file = i
            print(highest_file)
            add_item = CFX_ImportWidget('cam', mm_cam_path, versions, highest_file, parent=self)
            self.ani_cache_scroll_layout.addWidget(add_item)
        ani_pub_cache_abc_path = os.path.join(main_path, 'ani', 'pub', 'cache', 'abc', 'versions')
        if os.path.exists(ani_pub_cache_abc_path):
            pattern = re.compile(r"(.*?)_v(\d{3}).abc")
            dic_ani_versions = {}
            dic_ani_versions_h = {}
            for i in os.listdir(ani_pub_cache_abc_path):
                mach = pattern.match(i)
                if mach:
                    print(mach)
                    print(mach.group(1))
                    if mach.group(1) not in dic_ani_versions:
                        dic_ani_versions[mach.group(1)] = []
                    if mach:
                        dic_ani_versions[mach.group(1)].append(i)
            for i in dic_ani_versions:
                highest_v = -1
                highest_file = None
                for j in dic_ani_versions[i]:
                    mach = pattern.match(j)
                    if mach:
                        version = int(mach.group(2))
                        if version > highest_v:
                            highest_v = version
                            highest_file = j
                dic_ani_versions_h[i] = highest_file
            for i in dic_ani_versions:
                add_item = CFX_ImportWidget(i, ani_pub_cache_abc_path,
                                            dic_ani_versions[i], dic_ani_versions_h[i], parent=self)
                self.ani_cache_scroll_layout.addWidget(add_item)
            for i in dic_ani_versions:
                if i.find('__')!=-1:
                    split_a = i.split('__')
                    if split_a[0] == 'character':
                        folder_path = os.path.join(s_drive_i, 'vfx', s_project_i, 'asset', 'character',
                                                  split_a[2], 'cfx', 'pub', 'data')
                        asset_path = os.path.join(folder_path, 'yeti_cfx_grp.mb')
                        if os.path.exists(asset_path):
                            add_item = CFX_ImportWidget(f'cfx Set:{split_a[2]}', folder_path,
                                                        ['yeti_cfx_grp.mb'], 'yeti_cfx_grp.mb', parent=self)
                            self.cfx_setting_scroll_layout.addWidget(add_item)

    def filesave_yettifind(self):
        self.list_layout_item_remove(self.cfx_export_scroll_layout)
        s_drive_i = self.searchDriveComboBox.currentText()
        s_project_i = self.searchProjectComboBox.currentText()
        s_sequence_i = self.searchSequenceTypeComboBox.currentText()
        s_task_i = self.searchTaskTypeComboBox.currentText()
        main_path = os.path.join(s_drive_i, 'vfx', s_project_i, 'shot', s_sequence_i, s_task_i)
        cfx_path = os.path.join(main_path, 'cfx', 'pub', 'cache', 'yeti')
        self.create_directoryi(cfx_path)
        yeti_shape = pm.ls(type='pgYetiMaya')
        pattern = re.compile(r"(.*?)__v(\d{3})")
        for i in yeti_shape:
            new_path = ''

            yeti_node = pm.PyNode(i).getParent()
            file_name = f'{yeti_node.name()}.%04d.fur'
            ch_name = yeti_node.name().rsplit('_',2)[0]
            print('yeti shape')
            if os.path.exists(cfx_path):
                print(f'yeti path {cfx_path}')
                for i in os.listdir(cfx_path):
                    mach = pattern.match(i)
                    if mach != None:
                        print(mach.group(1), int(mach.group(2)))
                        if mach:
                            print(mach.group(1),int(mach.group(2)))
                            new_path = os.path.join(cfx_path,
                                                    f"{mach.group(1).split('__')[0]}__cfx__v{int(mach.group(2))+1:03d}",
                                                    yeti_node.name())
                        else:
                            new_path = os.path.join(cfx_path,
                                                    f"{mach.group(1).split('__')[0]}__cfx__v{1:03d}",
                                                    yeti_node.name())
            if len(os.listdir(cfx_path)) == 0:
                new_path = os.path.join(cfx_path,
                                        f"{ch_name}__cfx__v{1:03d}",
                                        yeti_node.name())
            print(f'test :  {new_path}')
            if new_path != '':
                print(file_name)
                #self.create_directoryi(new_path)
                add_item = CFX_ExportWidget(yeti_node.name(), new_path, file_name, parent=self)
                self.cfx_export_scroll_layout.addWidget(add_item)

    def file_open(self, ptah_field, list_widget):
        # wip 과 pub 아이템( 씬 ) 파일 열기
        file_path = ptah_field.text()
        select_file = list_widget.selectedItems()
        file_name = os.path.join(file_path, select_file[0].text())
        # 바로 오픈하지 않고 열겠습니까? 필요해보임
        if os.path.isfile(file_name):
            cmds.file(file_name, force=True, open=True, prompt=False, ignoreVersion=True, type='mayaBinary')


    def list_layout_item_remove(self,list_layout_a):
        countlayoutitem = list_layout_a.count()
        #print(countlayoutitem)
        for i in reversed(range(countlayoutitem)):
            item = list_layout_a.itemAt(i)
            if isinstance(item, QSpacerItem):
                list_layout_a.removeItem(item)
            elif item.widget() is not None:
                widget = item.widget()
                list_layout_a.removeWidget(widget)
                widget.deleteLater()


class CFX_ExportWidget(QWidget):
    def __init__(self, asset, main_path, file_name, parent=None):
        super().__init__(parent)
        self.asset = asset
        self.main_path = main_path
        self.file_name = file_name
        self.parent = parent
        self.ui()

    def ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        display_name = self.asset
        self.asset_code_label = QLabel(display_name)
        main_layout.addWidget(self.asset_code_label)
        self.cache_file_path = QLineEdit()
        self.cache_file_path.setText(self.main_path)
        main_layout.addWidget(self.cache_file_path)
        self.cache_file_name = QLineEdit()
        self.cache_file_name.setText(self.file_name)
        main_layout.addWidget(self.cache_file_name)
        ##################################################
        cache_exprt_button_layout = QHBoxLayout()
        main_layout.addLayout(cache_exprt_button_layout)
        cache_exprt_button_layout.setContentsMargins(0, 0, 0, 0)
        cache_exprt_button_layout.setSpacing(5)
        #
        cache_open_folder_button = QPushButton(' OPEN Folder')
        cache_exprt_button_layout.addWidget(cache_open_folder_button)
        cache_open_folder_button.clicked.connect(self.open_folder)
        #
        cache_export_button = QPushButton(' Yetti Cache Export START ')
        cache_exprt_button_layout.addWidget(cache_export_button)
        cache_export_button.clicked.connect(self.cache_export_button_run)

    def open_folder(self):
        path = self.main_path
        if os.path.isdir(path):
            os.startfile(path)
        else:
            print(f' None Folder ')
            if os.path.isdir(path.split('yeti')[0]+'yeti'):
                os.startfile(path.split('yeti')[0]+'yeti')

    def cache_export_button_run(self):
        start_frame = cmds.playbackOptions(q=True, min=True)
        end_frame = cmds.playbackOptions(q=True, max=True)
        file_path = self.cache_file_path.text()
        if os.path.exists(file_path):
            pass
        else:
            os.makedirs(file_path)
        file_name = self.cache_file_name.text()
        full_path = os.path.join(file_path,file_name)
        full_path = full_path.replace('\\','/')
        yeti_node = self.asset
        cmd = (f'pgYetiCommand -writeCache "{full_path}" -range {start_frame} {end_frame} '
               f'-samples 3 -updateViewport false  -generatePreview false {yeti_node}')
        print(cmd)
        pm.mel.eval(cmd)
        rename_a = cmds.file(q=True, sceneName=1)
        cmds.file(rename=rename_a)
        cmds.file(save=True, type='mayaBinary')



class CFX_ImportWidget(QWidget):
    def __init__(self, asset, main_path, versions, current, parent=None):
        super().__init__(parent)
        self.asset = asset
        self.main_path = main_path
        self.versions = versions
        self.current = current
        self.parent = parent
        self.ui()

    def ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        display_name = self.asset
        self.asset_code_label = QLabel(display_name)
        main_layout.addWidget(self.asset_code_label)

        self.version_combobox = QComboBox()
        self.version_combobox.addItem("-versions-")
        for i in self.versions:
            self.version_combobox.addItem(i)
        self.version_combobox.setCurrentText(self.current)
        main_layout.addWidget(self.version_combobox)

        sub_layout = QHBoxLayout()
        main_layout.addLayout(sub_layout)
        self.open_folder_button = QPushButton('Open Folder')
        self.open_folder_button.clicked.connect(self.open_folder)
        sub_layout.addWidget(self.open_folder_button)

        self.import_file_button = QPushButton('GET')
        self.import_file_button.clicked.connect(self.get_file)
        sub_layout.addWidget(self.import_file_button)

    def open_folder(self):
        path = self.main_path
        if os.path.isdir(path):
            os.startfile(path)
        else:
            print(f' None Folder ')

    def get_file(self):
        path = self.main_path
        filename = self.version_combobox.currentText()
        file_path = os.path.join(path,filename)
        if self.asset.find('__') != -1:
            split_a = self.asset.split('__')
            if split_a[0] == 'character':
                cmds.file(file_path, i=True, namespace=split_a[1])
        elif self.asset.find('cfx Set:') != -1:
            split_a = self.asset.split(':')
            if split_a[0] == 'cfx Set':
                print('cfx Set')
                cmds.file(file_path, i=True)
                dic_blendshape = {'crow': ['crowBody', 'crowBody_scalp_mesh'],
                                  'rat': ['rat_body_mesh', 'rat_body_scalp_mesh']}
                if split_a[1] in dic_blendshape:
                    chache_bs = cmds.ls(f'*:{dic_blendshape[split_a[1]][0]}', type='transform')
                    if len(chache_bs) == 1:
                        bs_node = cmds.blendShape(chache_bs[0], dic_blendshape[split_a[1]][1], name='cfx_bs')[0]
                        cmds.setAttr(bs_node + '.' + dic_blendshape[split_a[1]][0], 1)
                        cmds.parent('cfx',chache_bs[0].split(':',1)[0]+':geo')

        elif os.path.exists(file_path):
            cmds.file(file_path, i=True)
        else:
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
show_window()