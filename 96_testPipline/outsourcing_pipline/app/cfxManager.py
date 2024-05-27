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

class AddWipVersionDialog(QDialog):
    def __init__(self, text_a, test_b=None, test_c=None, parent=None):
        super().__init__(parent)
        self.textA = text_a
        self.setWindowTitle('Wip Version Add')
        self.setFixedSize(400, 300)
        layout = QVBoxLayout()
        # a
        self.label_a = QLabel('v000 버전 추가 : (ex 999)', self)
        layout.addWidget(self.label_a)
        self.lineEdit_a = QLineEdit(self)
        layout.addWidget(self.lineEdit_a)
        if test_b:
            self.lineEdit_a.setText(test_b)
        # b
        self.label_b = QLabel('w00 버전 추가 : (ex 99)', self)
        layout.addWidget(self.label_b)
        self.lineEdit_b = QLineEdit(self)
        layout.addWidget(self.lineEdit_b)
        if test_c:
            self.lineEdit_b.setText(test_c)
        # c
        self.label_c = QLabel(' 버전  : ', self)
        layout.addWidget(self.label_c)
        self.lineEdit_c = QLineEdit(self)
        layout.addWidget(self.lineEdit_c)
        # ok
        self.button = QPushButton('확인', self)
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
        # 오른쪽 메뉴 생성
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

    def set_path_field(self, field_a, path_a, pattern_a):
        # field and path and pattern 주면 맞는지 확인하고 리스트에 넣는다.
        # wip_list_widget , pub_list_widget
        if os.path.isdir(path_a):
            items = os.listdir(path_a)
            field_a.clear()
            for item in items:
                if re.match(pattern_a, item):
                    log.info(f'{item}')
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
            print(f' 복사합니다. :{old_path} -> {new_path}')
            shutil.copy(old_path,new_path)
            self.set_path_field(self.wip_list_widget, self.wip_path_field.text(), r"(.*?)_v(\d{3})_w(\d{2}).mb")
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
