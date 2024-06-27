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

class MOD_ChangeWidget(QWidget):
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

        self.import_file_button = QPushButton('Change')
        self.import_file_button.clicked.connect(self.get_file)
        sub_layout.addWidget(self.import_file_button)

    def open_folder(self):
        path = self.main_path
        if os.path.isdir(path):
            os.startfile(path)
        else:
            print(f' None Folder ')

    def find_skin_clusters_in_geo_group(self):
        # 1. 리깅 파일 안에 있는 geo 그룹 찾기
        geo_group = None
        all_groups = cmds.ls(type='transform')
        for group in all_groups:
            if group == 'old_geo':  # 'geo' 그룹을 찾음
                geo_group = group
                break

        if not geo_group:
            cmds.warning("Cannot find 'geo' group in the scene.")
            return

        # 2. geo 그룹 내 하위 객체 검색
        child_objects = cmds.listRelatives(geo_group, ad=True, type='transform', fullPath=True) or []
        skin_clusters_dict = {}

        for obj in child_objects:
            # 3. 각 객체에서 skincluster 있는지 확인
            skin_cluster = cmds.ls(cmds.listHistory(obj), type='skinCluster')
            if skin_cluster:
                # 4. skincluster가 있으면 매쉬-조인트 리스트를 딕셔너리에 추가
                mesh_node = cmds.listRelatives(obj, shapes=True, fullPath=False)[0]
                joints = cmds.skinCluster(skin_cluster[0], query=True, inf=True)
                skin_clusters_dict[mesh_node] = joints

        # 5. 최종적으로 딕셔너리 반환
        return skin_clusters_dict

    def get_file(self):
        # change 하는 부분
        # geo 폴더가 있는지 확인 없으면 끝
        if pm.objExists('geo') == False:
            return
        # 스크립트 실행
        s_geo = 'geo'
        s_oldgeo = 'old_geo'
        s_prefix = 'old'
        if cmds.objExists(s_geo):
            print('check01')
            cmds.rename(s_geo, s_oldgeo)
            for i in cmds.listRelatives(s_oldgeo):
                selected_object = cmds.ls(i, dag=True, type='transform')
                print(selected_object)
                if not selected_object:
                    cmds.warning("선택한 오브젝트를 찾을 수 없습니다.")
                for node in selected_object:
                    new_name = s_prefix + '_' + node
                    cmds.rename(node, new_name)
            result = self.find_skin_clusters_in_geo_group()
            print(result)  # 딕셔너리 출력 혹은 다른 작업 수행
        filename = self.version_combobox.currentText()

        if os.path.isdir(self.main_path):
            print(self.main_path,filename)
            if self.asset == 'abc':
                cmds.AbcImport(os.path.join(self.main_path,filename))
                delete_parent = None
                if cmds.objExists(s_geo):
                    delete_parent = cmds.listRelatives(s_geo, parent=True, fullPath=False)
                    new_parent = cmds.listRelatives(s_oldgeo, parent=True, fullPath=False)
                    cmds.parent(s_geo, new_parent[0])
                    for shape_name, joint_list in result.items():
                        new_shape_name = shape_name.replace('old_', '')

                        # 선택된 객체들의 이름
                        source_object = shape_name
                        destination_object = new_shape_name
                        destination_skin_cluster = cmds.skinCluster(joint_list, new_shape_name, toSelectedBones=True, bindMethod=0,
                                                        normalizeWeights=1)[0]

                        # 스킨 클러스터 노드 가져오기
                        source_skin_cluster = cmds.ls(cmds.listHistory(source_object), type='skinCluster')[0]
                        # source_skin_cluster = cmds.skinCluster(source_object, query=True, ignoreFuture=True)
                        # source_skin_cluster = cmds.listConnections(source_object, type='skinCluster')
                        # destination_skin_cluster = cmds.listConnections(destination_object, type='skinCluster')

                        if not source_skin_cluster:
                            cmds.warning(f"No skinCluster found for {source_object}. Aborting copySkinWeights.")
                            cmds.error("Source skinCluster not found.")
                            raise RuntimeError("Source skinCluster not found.")

                        if not destination_skin_cluster:
                            cmds.warning(f"No skinCluster found for {destination_object}. Aborting copySkinWeights.")
                            cmds.error("Destination skinCluster not found.")
                            raise RuntimeError("Destination skinCluster not found.")

                        # 스킨 가중치 복사
                        cmds.select(clear=True)
                        cmds.select(source_object, add=True)
                        cmds.select(destination_object, add=True)
                        print(source_object,destination_object,source_skin_cluster,destination_skin_cluster)
                        cmds.copySkinWeights(
                            sourceSkin=source_skin_cluster,
                            destinationSkin=destination_skin_cluster,
                            noMirror=True,
                            surfaceAssociation='closestPoint',
                            influenceAssociation=('oneToOne', 'oneToOne', 'oneToOne')
                        )
                    if delete_parent:
                        cmds.delete(delete_parent)
                    #cmds.delete(s_oldgeo)
        #
        """
        path = self.main_path
        filename = self.version_combobox.currentText()
        file_path = os.path.join(path, filename)
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
        """


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



    def find_model_button_run(self):
        print('-**-')
        self.list_layout_item_remove(self.mod_change_scroll_layout)
        searchDrive_item = self.searchDriveComboBox.currentText()
        searchProject_item = self.searchProjectComboBox.currentText()
        searchAsset_item = self.searchAssetTypeComboBox.currentText()
        selected_item = self.task_list_widget.selectedItems()
        if selected_item == []:
            print(f'None Selected Rig Task Item')
            return False
        mod_abc_path = ''
        if len(selected_item) == 4:
            row = selected_item[0].row()
            code_item = self.task_list_widget.item(row, 2)
            print(f'item name :::: {code_item.text()}')
            mod_abc_path = os.path.join(searchDrive_item, 'vfx', searchProject_item, 'asset',
                                        searchAsset_item, code_item.text(), 'mod',
                                        'pub', 'data', 'abc', 'versions')
            mod_abc_path = mod_abc_path.replace('/','\\')
        print(mod_abc_path)
        if os.path.exists(mod_abc_path):
            print(mod_abc_path)
            items = os.listdir(mod_abc_path)
            pattern = re.compile(r"(.*?)_v(\d{3}).abc")
            highest_v = -1
            highest_file = None
            versions = []
            for i in os.listdir(mod_abc_path):
                mach = pattern.match(i)
                if mach:
                    versions.append(i)
                    version = int(mach.group(2))
                    if version > highest_v:
                        highest_v = version
                        highest_file = i
            print(highest_file)
            add_item = MOD_ChangeWidget('abc', mod_abc_path, versions, highest_file, parent=self)
            self.mod_change_scroll_layout.addWidget(add_item)
        mod_version_path = ''
        if len(selected_item) == 4:
            row = selected_item[0].row()
            code_item = self.task_list_widget.item(row, 2)
            print(f'item name :::: {code_item.text()}')
            mod_version_path = os.path.join(searchDrive_item, 'vfx', searchProject_item, 'asset',
                                        searchAsset_item, code_item.text(), 'mod',
                                        'pub', 'scenes', 'versions')
            mod_version_path = mod_version_path.replace('/','\\')
        print(mod_version_path)
        if os.path.exists(mod_version_path):
            print(mod_version_path)
            items = os.listdir(mod_version_path)
            pattern = re.compile(r"(.*?)_v(\d{3}).mb")
            highest_v = -1
            highest_file = None
            versions = []
            for i in os.listdir(mod_version_path):
                mach = pattern.match(i)
                if mach:
                    versions.append(i)
                    version = int(mach.group(2))
                    if version > highest_v:
                        highest_v = version
                        highest_file = i
            print(highest_file)
            add_item = MOD_ChangeWidget('mod', mod_version_path, versions, highest_file, parent=self)
            self.mod_change_scroll_layout.addWidget(add_item)

    def check_run01(self):
        print('temp01')
        # get seleted task item name
        selected_item = self.task_list_widget.selectedItems()
        if selected_item == []:
            print(f'None Selected Rig Task Item')
            return False
        if len(selected_item) == 4:
            row = selected_item[0].row()
            code_item = self.task_list_widget.item(row, 3)
            print(code_item.text())
        if pm.objExists(code_item.text()):
            return True
        else:
            return False

    def check_run02(self):
        if pm.objExists('geo'):
            return True
        else:
            return False
    def check_run03(self):
        if pm.objExists('rig'):
            return True
        else:
            return False
    def check_run04(self):
        check = False
        for i in pm.ls(type='transform') and pm.ls(type='shape'):
            if i.find('|')!=-1:
                check = True
                print(f'씬 안에 중복된 이름이 발견됨 : {i}')
        if check == True:
            return False
        else:
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