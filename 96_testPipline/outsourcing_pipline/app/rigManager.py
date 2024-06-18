# rigging
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

class CheckWorkDialog(QWidget):
    def __init__(self, string_name, script_run, parent=None):
        super().__init__(parent)
        self.check = False
        self.parent = parent
        self.string_name = string_name
        self.script_run = script_run
        self.ui()

    def ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        self.QPush_Button =QPushButton(self.string_name)
        self.QPush_Button.setEnabled(True)
        self.QPush_Button.clicked.connect(self.q_push_button)
        main_layout.addWidget(self.QPush_Button)

    def q_push_button(self):
        check_a = self.script_run()
        if check_a:
            self.set_underline()
            self.set_text_color(Qt.green)
        else:
            self.set_text_color(Qt.red)

    def reset_underline(self):
        # self.check = True
        font = self.QPush_Button.font()
        font.setStrikeOut(False)
        self.QPush_Button.setFont(font)
        self.set_text_color(Qt.white)

    def set_underline(self):
        print('set')
        font = self.QPush_Button.font()
        # font.setUnderline(True)
        font.setStrikeOut(True)
        self.QPush_Button.setFont(font)

    def set_text_color(self, color):
        palette = self.QPush_Button.palette()
        new_palette = QPalette(palette)
        new_palette.setColor(QPalette.ButtonText, color)
        self.QPush_Button.setPalette(new_palette)


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


class RigManagerWindow(mayaMixin.MayaQWidgetBaseMixin, QMainWindow):
    WINDOW_NAME = 'rig_manager_window_a'
    OPTIONVAR_TASKMANAGER_A = 'optionvar_rig_manager_a'

    def __init__(self):
        super(RigManagerWindow, self).__init__()
        if pm.window(self.WINDOW_NAME, q=True, ex=True):
            pm.deleteUI(self.WINDOW_NAME, window=True)
        self.setObjectName(self.WINDOW_NAME)
        self.setWindowTitle(self.WINDOW_NAME)
        self.setGeometry(200, 200, 1700, 800)
        self.ui()

    def ui(self):
        print('rig manager ui start.')
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
        frameAppBannertitle_label = QLabel(u"Rigging Manager")
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
        script_work_label = QLabel('script work')
        script_work_label.setStyleSheet('font-size: 10pt;')
        right_script_layout.addWidget(script_work_label)
        right_script_layout.addItem(QSpacerItem(5, 0))

    def check_run01(self):
        print('temp01')
        return False
    def check_run02(self):
        print('temp02')
        return True
    def check_run03(self):
        print('temp03')
        return False
    def check_run04(self):
        print('temp04')
        return True
    def check_run05(self):
        print('temp05')
        for index in range(self.check_work_scroll_layout.count()):
            dialog = self.check_work_scroll_layout.itemAt(index).widget()
            dialog.QPush_Button.click()  # Simulate the button click

    def check_work_reset_run(self):
        print('reset')
        for index in range(self.check_work_scroll_layout.count()):
            dialog = self.check_work_scroll_layout.itemAt(index).widget()
            dialog.reset_underline()

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
        vfx_folder = os.path.join(selected_drive_item, 'vfx', selected_project_item, 'asset')
        if os.path.exists(vfx_folder):
            subfolders = ['character', 'prop', 'vehicle', 'env', 'crowd', 'location', 'fx']
            if subfolders:
                self.searchAssetTypeComboBox.clear()
                self.searchAssetTypeComboBox.addItem('-AssetType-')
                for i in subfolders:
                    self.searchAssetTypeComboBox.addItem(i)
    def searchAssetTypeComboBox_change(self):
        # 변경이되면 rig task에 프린트한다.
        # 현재 상태 프린트
        searchDrive_item = self.searchDriveComboBox.currentText()
        searchProject_item = self.searchProjectComboBox.currentText()
        searchAsset_item = self.searchAssetTypeComboBox.currentText()
        if searchAsset_item not in ['-AssetType-', '']:
            asset_path = os.path.join(searchDrive_item, 'vfx', searchProject_item, 'asset', searchAsset_item)
            # print(searchDrive_item, searchProject_item, searchAsset_item)
            # print(asset_path)
            header_labels_asset = ['Type', 'Code', 'Name', 'Task']
            self.task_list_widget.setColumnCount(4)
            row_num = 0
            self.task_list_widget.clearContents()
            self.task_list_widget.setHorizontalHeaderLabels(header_labels_asset)

            rig_task = []
            for item in os.listdir(asset_path):
                item_path = os.path.join(asset_path, item)
                # print(f'asset_path:{asset_path} {item} {}')
                if os.path.isdir(item_path):
                    print('character : ', item_path)
                    rig_task.append(item)

            low_max = len(rig_task)
            self.task_list_widget.setRowCount(low_max)

            for item in rig_task:
                type_item = QTableWidgetItem(f'{searchAsset_item}')
                code_item = QTableWidgetItem(f'{item}')
                shot_item = QTableWidgetItem(f'{item}')
                task_item = QTableWidgetItem(f'rig')
                type_item.setFlags(type_item.flags() ^ Qt.ItemIsEditable)
                code_item.setFlags(code_item.flags() ^ Qt.ItemIsEditable)
                shot_item.setFlags(shot_item.flags() ^ Qt.ItemIsEditable)
                task_item.setFlags(task_item.flags() ^ Qt.ItemIsEditable)
                self.task_list_widget.setItem(row_num, 0, type_item)
                self.task_list_widget.setItem(row_num, 1, code_item)
                self.task_list_widget.setItem(row_num, 2, shot_item)
                self.task_list_widget.setItem(row_num, 3, task_item)
                row_num = row_num + 1

            pass
    def copy_path_to_clipboard_wip(self):
        pass
    def open_work_path_wip(self):
        pass
    def on_task_list_selection_changed(self):
        selected_item = self.task_list_widget.selectedItems()
        if selected_item:
            rows = set()
            for item in selected_item:
                rows.add(item.row())
            for row in rows:
                for column in range(self.task_list_widget.columnCount()):
                    item = self.task_list_widget.item(row, column)
                    item.setSelected(True)
    def on_task_list_item_double_clicked(self):
        selected_item = self.task_list_widget.selectedItems()
        if len(selected_item) == 4:
            # log.info(f'{selected_item}')
            # 선택한 아이템의 작업 path 를 가져온다.
            current_dpe = self.current_drive_project_entity()
            row = selected_item[0].row()
            code_item = self.task_list_widget.item(row, 1)
            print(f' get table item {row} {current_dpe} {code_item.text()}')
            wip_path = os.path.join(current_dpe['drive'], 'vfx', current_dpe['project'], 'asset',current_dpe['asset'],
                                    code_item.text(), 'rig', 'wip', 'scenes')
            print(wip_path)
            self.wip_path_field.setText(wip_path)
            self.wip_list_widget.clear()
            self.set_path_field(self.wip_list_widget, wip_path, r"(.*?)_v(\d{3})_w(\d{2}).mb")


    def current_drive_project_entity(self):
        searchDrive_item = self.searchDriveComboBox.currentText()
        searchProject_item = self.searchProjectComboBox.currentText()
        searchAsset_item = self.searchAssetTypeComboBox.currentText()
        return_dic = {}
        return_dic['drive'] = searchDrive_item
        return_dic['project'] = searchProject_item
        return_dic['asset'] = searchAsset_item
        return return_dic

    def set_path_field(self, field_a, path_a, pattern_a):
        # field and path and pattern 주면 맞는지 확인하고 리스트에 넣는다.
        # wip_list_widget , pub_list_widget
        if os.path.isdir(path_a):
            items = os.listdir(path_a)
            #field_a.clear()
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

    def on_wip_list_double_clicked(self, item):
        wip_file_path = self.wip_path_field.text()
        # wip_select_file = self.wip_list_widget.selected
        print(f'{wip_file_path} {item.text()}')
        file_name = os.path.join(wip_file_path, item.text())
        # 바로 오픈하지 않고 열겠습니까? 필요해보임
        if os.path.isfile(file_name):
            cmds.file(file_name, force=True, open=True, prompt=False, ignoreVersion=True, type='mayaBinary')
        pass

    def wip_show_context_menu(self, position):
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
            # action = QAction(" Selected -> Upload PUB File  ", self)
            # action.triggered.connect(self.wip_right_pub_upload)
            # menu.addAction(action)
        menu.exec_(self.wip_list_widget.mapToGlobal(position))

    def wip_right_wip_copy_path(self):
        print(f'  wip folder path copy')
        self.copy_path_to_clipboard_wip()
    def copy_path_to_clipboard_wip(self):
        print(f' wip path field')
        field_a = self.wip_path_field
        path = field_a.text()
        print(f'{path}')
        self.copy_path_to_clipboard(path)

    def copy_path_to_clipboard_pub(self):
        print(f' pub path field')
        field_a = self.pub_path_field
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

    def wip_right_open_folder(self):
        print(f' wip folder open')
        self.open_work_path_wip()

    def open_work_path_wip(self):
        field_a = self.wip_path_field
        path = field_a.text()
        self.open_work_path_a(path)

    def open_work_path_a(self, text_a):
        path = text_a
        if os.path.isdir(path):
            os.startfile(path)
        else:
            print(f' None Folder ')

    def wip_right_file_open(self):
        print(f' file open - wip right button')
        self.file_open(self.wip_path_field, self.wip_list_widget)

    def file_open(self, ptah_field, list_widget):
        # wip 과 pub 아이템( 씬 ) 파일 열기
        file_path = ptah_field.text()
        select_file = list_widget.selectedItems()
        file_name = os.path.join(file_path, select_file[0].text())
        # 바로 오픈하지 않고 열겠습니까? 필요해보임
        if os.path.isfile(file_name):
            cmds.file(file_name, force=True, open=True, prompt=False, ignoreVersion=True, type='mayaBinary')

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
            self.wip_list_widget.clear()
            self.set_path_field(self.wip_list_widget, self.wip_path_field.text(), r"(.*?)_v(\d{3})_w(\d{2}).mb")
        pass


def show_window():
    global RigManagerWindow

    try:
        RigManagerWindow.close()
        RigManagerWindow.deleteLater()
    except:
        pass

    rigmanagerwin = RigManagerWindow()
    rigmanagerwin.show()
show_window()