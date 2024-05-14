# 테스크 메니져 서버 기준 폴더를 뷰어로 보여주는 목적
# 해당 테스크 최초폴더생성및 버전관리
# wip 버전 업로드및 pup 버전
import outsourcing_pipline.log
import importlib
#importlib.reload(outsourcing_pipline.log)
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2 import __version__
from maya.app.general import mayaMixin
import pymel.core as pm
import maya.cmds as cmds
from outsourcing_pipline.config import INHOUSETOOLS_ICON_PATH
importlib.reload( outsourcing_pipline.config)
import os
import re

# 로그
log = outsourcing_pipline.log.get_logger('taskManager 00')
log.info(' 마야에서 로그가 프린트 되는지 체크 ')

def img_path(img):
    return os.path.join(INHOUSETOOLS_ICON_PATH, img)

class TaskManagerWindow(mayaMixin.MayaQWidgetBaseMixin,QMainWindow):
    # 윈도우 오브젝트의 이름
    WINDOW_NAME = 'task_manager_window_a'
    OPTIONVAR_TASKMANAGER_A='optionvar_task_manager_a'
    def __init__(self):
        super(TaskManagerWindow, self).__init__()
        log.info('taskmanager 시작합니다.')
        if pm.window(self.WINDOW_NAME, q=True, ex=True):
            pm.deleteUI(self.WINDOW_NAME, window=True)
        self.setObjectName(self.WINDOW_NAME)
        self.setWindowTitle(self.WINDOW_NAME)
        self.setGeometry(200, 200, 1000, 800)
        log.info(f'창 로고 {img_path("vive_initial_logo.png")}')
        self.setWindowIcon(QIcon(img_path('vive_initial_logo.png')))
        self.ui()
        self.get_optionvar_a()
        log.info(f' 이전 저장했던 옵션이 있는지 체크 ')

    def ui(self):
        log.info('task manager ui 시작합니다.')
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        frameAppBanner = QFrame()
        frameAppBanner.setStyleSheet('''
                                            color: #ddd;
                                            background-color: #000;
                                            padding: 10px 5px;
                                            ''')
        frameAppBanner.setGeometry(10,10,500,100)
        frameAppBanner.setFixedHeight(100)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed))
        window_layout = QVBoxLayout(self.centralWidget())
        window_layout.setContentsMargins(0, 0, 0, 0)
        window_layout.setSpacing(0)
        window_layout.setAlignment(Qt.AlignTop)
        main_widget.setLayout(window_layout)
        window_layout.addWidget(frameAppBanner)
        # --------- B a n n e r
        # 메인 레이아웃 : QHBoxLayout
        frameAppBannermain_layout = QHBoxLayout(frameAppBanner)
        frameAppBannermain_layout.setContentsMargins(10, 0, 0, 0)
        frameAppBannermain_layout.setSpacing(10)
        frameAppBannermain_layout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        # window_layout.addLayout(frameAppBanner)

        # 앱의 이름과 제작사 이름
        frameAppBannerapp_layout = QVBoxLayout()
        frameAppBannerapp_layout.setSpacing(0)
        frameAppBannerapp_layout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        frameAppBannermain_layout.addLayout(frameAppBannerapp_layout)

        # 앱 이름
        frameAppBannertitle_label = QLabel(u"Task Manager")
        frameAppBannertitle_label.setStyleSheet('''
                                font-size: 14pt;
                                font-family: Nanum Gothic, Malgun Gothic, sans-serif;
                                font-weight: bold;
                                padding: 0px;
                            ''')
        frameAppBannerapp_layout.addWidget(frameAppBannertitle_label)

        # 제작사 이름
        frameAppBannersub_title_label = QLabel('<b>VIVE</b> STUDIOS')
        frameAppBannersub_title_label.setStyleSheet('''
                                font-size: 9pt;
                                padding: 0px;
                            ''')
        frameAppBannerapp_layout.addWidget(frameAppBannersub_title_label)

        # 스페이서
        frameAppBannermain_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding))

        # 여기까지 이미지 Asset 로더 Vive studios
        # 콤보박스
        # 중앙 기능 버튼 레이아웃
        ####################################################################################################
        search_filter_layout = QHBoxLayout()
        search_filter_layout.setContentsMargins(0, 0, 0, 0)
        search_filter_layout.setSpacing(6)
        window_layout.addLayout(search_filter_layout)

        # 드라이브 콤보박스
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

        # 프로젝트 콤보박스
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

        # asset type 콤보박스
        self.searchStepTypeComboBox = QComboBox()
        self.searchStepTypeComboBox.setStyleSheet('''
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
        self.searchStepTypeComboBox.addItem("Step-type")
        self.searchStepTypeComboBox.setMaxVisibleItems(12)
        self.searchStepTypeComboBox.currentIndexChanged.connect(self.searchStepTypeComboBox_change)
        self.searchStepTypeComboBox.addItem("mm")
        self.searchStepTypeComboBox.addItem("ani")
        self.searchStepTypeComboBox.addItem("lit")
        self.searchStepTypeComboBox.addItem("fx")
        #search_filter_layout.addWidget(self.searchStepTypeComboBox)
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
        ##################################################
        # 좌측 필터
        ##################################################
        task_filter_widget = QWidget()
        self.splitter.addWidget(task_filter_widget)

        task_filter_widget_layout = QVBoxLayout(task_filter_widget)
        task_filter_widget_layout.setContentsMargins(0, 0, 10, 0)
        task_filter_widget_layout.setSpacing(10)

        ##################################################
        # 상단 메뉴바
        ##################################################
        task_top_layout = QHBoxLayout()
        task_filter_widget_layout.addLayout(task_top_layout)
        task_top_layout.setContentsMargins(0, 0, 0, 0)
        task_top_layout.setSpacing(5)

        ####################################################################################################
        # 중앙 태스크 리스트
        ####################################################################################################
        self.task_frame = QFrame()
        self.splitter.addWidget(self.task_frame)
        task_layout = QVBoxLayout(self.task_frame)
        task_layout.setContentsMargins(10, 0, 10, 0)
        task_layout.setSpacing(5)

        ####################################################################################################
        # 작업파일 레이아웃
        ####################################################################################################
        self.work_frame = QFrame()
        self.work_frame.setEnabled(False)
        self.splitter.addWidget(self.work_frame)
        work_layout = QVBoxLayout(self.work_frame)
        work_layout.setContentsMargins(10, 0, 0, 0)
        work_layout.setSpacing(3)

        ##################################################
        # 애셋, 샷 엔티티 선택 라디오버튼
        ##################################################
        self.main_entity_grp = QGroupBox('메인 엔티티')
        self.main_entity_grp.setFixedHeight(90)
        task_filter_widget_layout.addWidget(self.main_entity_grp)

        main_entity_grp_layout = QHBoxLayout(self.main_entity_grp)
        main_entity_grp_layout.setContentsMargins(10, 10, 10, 10)
        main_entity_grp_layout.setSpacing(10)
        main_entity_grp_layout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        # 버튼 그룹
        self.main_entity_btn_grp = QButtonGroup()
        self.main_entity_btn_grp.buttonReleased.connect(self.on_entity_selection_changed)
        # 애셋 라디오 버튼
        self.asset_entity_radio = QRadioButton('애셋')
        main_entity_grp_layout.addWidget(self.asset_entity_radio)
        # 스페이서
        main_entity_grp_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Fixed))
        # 샷 라디오 버튼
        self.shot_entity_radio = QRadioButton('샷')
        main_entity_grp_layout.addWidget(self.shot_entity_radio)

        # 버튼 그룹에 애셋, 샷 라디오 버튼 등록
        #self.main_entity_btn_grp.setId(self.asset_entity_radio, 0)
        #self.main_entity_btn_grp.setId(self.shot_entity_radio, 1)
        self.main_entity_btn_grp.addButton(self.asset_entity_radio,0)
        self.main_entity_btn_grp.addButton(self.shot_entity_radio,1)

        ####################################################################################################
        # 파이프라인 스텝
        ####################################################################################################
        # 태스크 필터들이 들어갈 레이아웃
        self.task_filter_layout = QVBoxLayout(task_filter_widget)
        task_filter_widget_layout.addLayout(self.task_filter_layout)
        self.task_filter_layout.setContentsMargins(0, 0, 0, 0)
        self.task_filter_layout.setSpacing(10)

        self.step_filter_grp = QGroupBox('파이프라인 스텝')
        self.task_filter_layout.addWidget(self.step_filter_grp)

        self.step_filter_grp_layout = QVBoxLayout(self.step_filter_grp)
        self.step_filter_grp_layout.setContentsMargins(10, 10, 10, 10)
        self.step_filter_grp_layout.setSpacing(1)
        self.step_filter_grp_layout.setAlignment(Qt.AlignTop)

        # 전체 선택 / 해제 체크박스
        self.step_cb = QCheckBox('전체')
        self.step_filter_grp_layout.addWidget(self.step_cb)
        self.step_cb.stateChanged.connect(self.step_cb_changed)
        #cb.is_master = True
        #cb.toggled.connect(partial(self.set_all_checkbox_checked, self.step_filter_grp_layout))

        # separator
        sep = QFrame()
        self.step_filter_grp_layout.addWidget(sep)
        sep.setFrameShape(QFrame.HLine)
        sep.setFrameShadow(QFrame.Sunken)
        sep.setFixedHeight(12)

        self.cb_mod = QCheckBox('mod')
        self.step_filter_grp_layout.addWidget(self.cb_mod)

        #cb.setIcon(QIcon(img_path('step/step_modeling.png')))
        #cb.sg_step = ShotgridPipelineStep.MODELING
        #cb.setObjectName(f'{self.FILTER_PREFIX}__steps__mod')
        #cb.toggled.connect(self.on_filter_checkbox_toggled)

        self.cb_lkd = QCheckBox('lkd')
        self.step_filter_grp_layout.addWidget(self.cb_lkd)
        #cb.setIcon(QIcon(img_path('step/step_lookdev.png')))
        #cb.sg_step = ShotgridPipelineStep.LOOKDEV
        #cb.setObjectName(f'{self.FILTER_PREFIX}__steps__lkd')
        #cb.toggled.connect(self.on_filter_checkbox_toggled)

        self.cb_rig = QCheckBox('rig')
        self.step_filter_grp_layout.addWidget(self.cb_rig)
        #cb.setIcon(QIcon(img_path('step/step_rigging.png')))
        #cb.sg_step = ShotgridPipelineStep.RIGGING
        #cb.setObjectName(f'{self.FILTER_PREFIX}__steps__rig')
        #cb.toggled.connect(self.on_filter_checkbox_toggled)

        self.cb_cfx = QCheckBox('cfx')
        self.step_filter_grp_layout.addWidget(self.cb_cfx)
        #cb.setIcon(QIcon(img_path('step/step_cfx.png')))
        #cb.sg_step = ShotgridPipelineStep.CFX_ASSET
        #cb.setObjectName(f'{self.FILTER_PREFIX}__steps__cfx')
        #cb.toggled.connect(self.on_filter_checkbox_toggled)

        step_code = 'mm'
        self.cb_mm = QCheckBox(step_code)
        self.step_filter_grp_layout.addWidget(self.cb_mm)
        #cb.setIcon(QIcon(img_path('step/step_matchmove.png')))
        #cb.sg_step = ShotgridPipelineStep.MATCHMOVE
        #cb.setObjectName(f'{self.FILTER_PREFIX}__steps__{step_code}')
        #cb.toggled.connect(self.on_filter_checkbox_toggled)

        step_code = 'ani'
        self.cb_ani = QCheckBox(step_code)
        self.step_filter_grp_layout.addWidget(self.cb_ani)
        #cb.setIcon(QIcon(img_path('step/step_animation.png')))
        #cb.sg_step = ShotgridPipelineStep.ANIMATION
        #cb.setObjectName(f'{self.FILTER_PREFIX}__steps__{step_code}')
        #cb.toggled.connect(self.on_filter_checkbox_toggled)

        step_code = 'lit'
        self.cb_lit = QCheckBox(step_code)
        self.step_filter_grp_layout.addWidget(self.cb_lit)
        #cb.setIcon(QIcon(img_path('step/step_lighting.png')))
        #cb.sg_step = ShotgridPipelineStep.LIGHTING
        #cb.setObjectName(f'{self.FILTER_PREFIX}__steps__{step_code}')
        #cb.toggled.connect(self.on_filter_checkbox_toggled)

        step_code = 'fx'
        self.cb_fx = QCheckBox(step_code)
        self.step_filter_grp_layout.addWidget(self.cb_fx)
        #cb.setIcon(QIcon(img_path('step/step_fx.png')))
        #cb.sg_step = ShotgridPipelineStep.FX
        #cb.setObjectName(f'{self.FILTER_PREFIX}__steps__{step_code}')
        #cb.toggled.connect(self.on_filter_checkbox_toggled)

        step_code = 'comp'
        self.cb_comp = QCheckBox(step_code)
        self.step_filter_grp_layout.addWidget(self.cb_comp)
        #cb.setIcon(QIcon(img_path('step/step_composition.png')))
        #cb.sg_step = ShotgridPipelineStep.COMPOSITION
        #cb.setObjectName(f'{self.FILTER_PREFIX}__steps__{step_code}')
        #cb.toggled.connect(self.on_filter_checkbox_toggled)

        # step list
        self.step_filter_list = []
        self.step_filter_list.append(self.cb_mod)
        self.step_filter_list.append(self.cb_lkd)
        self.step_filter_list.append(self.cb_rig)
        self.step_filter_list.append(self.cb_cfx)
        self.step_filter_list.append(self.cb_mm)
        self.step_filter_list.append(self.cb_ani)
        self.step_filter_list.append(self.cb_lit)
        self.step_filter_list.append(self.cb_fx)
        self.step_filter_list.append(self.cb_comp)
        ##################################################
        # 메인 태스크 리스트 위젯
        ##################################################
        search_pushbutton=QPushButton('옵션 기억 및 서치')
        task_layout.addWidget(search_pushbutton)
        search_pushbutton.setStyleSheet("""
                                        font-size: 13pt; 
                                        color: black;                               
                                        border: 1px solid orange;
                                        background-color: orange;                                
                                        border-radius: 8px;
                                        padding: 5px 10px;
                                        font-weight:bold;
                                        """)

        search_pushbutton.clicked.connect(self.search_pushbutton_clicked)
        
        self.task_list_widget = QTableWidget()
        self.task_list_widget.setEnabled(False)
        #self.task_list_widget.itemSelectionChanged.connect(self.on_task_list_selection_changed)
        #self.task_list_widget.itemDoubleClicked.connect(self.on_task_list_item_double_clicked)
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

        layout.addWidget(QLabel('WIPs'))
        layout.addItem(QSpacerItem(5, 0))

        self.wip_path_field = QLineEdit()
        layout.addWidget(self.wip_path_field)
        self.wip_path_field.setFixedHeight(20)

        # wip 경로 복사하기 버튼
        btn = QPushButton('C')
        layout.addWidget(btn)
        btn.setFixedSize(20, 20)
        #btn.clicked.connect(partial(self.copy_path_to_clipboard, self.wip_path_field))

        # wip 경로 열기 버튼
        btn = QPushButton('O')
        layout.addWidget(btn)
        btn.setFixedSize(20, 20)
        #btn.clicked.connect(partial(self.open_work_path, '', mode='wip'))

        # wip 파일 리스트
        self.wip_list_widget = QListWidget()
        work_layout.addWidget(self.wip_list_widget)
        #self.wip_list_widget.itemSelectionChanged.connect(self.on_wip_list_selection_changed)
        #self.wip_list_widget.doubleClicked.connect(self.on_wip_list_double_clicked)

        ##################################################
        # 스페이서
        ##################################################
        work_layout.addItem(QSpacerItem(0, 30))

        ##################################################
        # pub 작업 파일 리스트
        ##################################################
        # pub 경로 필드
        layout = QHBoxLayout()
        work_layout.addLayout(layout)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(1)
        layout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        # pub 타이틀
        layout.addWidget(QLabel('PUBs'))
        layout.addItem(QSpacerItem(5, 0))

        self.pub_path_field = QLineEdit()
        layout.addWidget(self.pub_path_field)
        self.pub_path_field.setFixedHeight(20)

        # pub 경로 복사하기 버튼
        btn = QPushButton('C')
        layout.addWidget(btn)
        btn.setFixedSize(20, 20)
        # btn.clicked.connect(partial(self.copy_path_to_clipboard, self.pub_path_field))

        # pub 경로 열기 버튼
        btn = QPushButton('O')
        layout.addWidget(btn)
        btn.setFixedSize(20, 20)
        # btn.clicked.connect(partial(self.open_work_path, '', mode='pub'))

        # pub 씬 파일 리스트 위젯
        self.pub_list_widget = QListWidget()
        work_layout.addWidget(self.pub_list_widget)
        # self.pub_list_widget.itemSelectionChanged.connect(self.on_pub_list_selection_changed)
        # self.pub_list_widget.doubleClicked.connect(self.on_pub_list_double_clicked)

        ####################################################################################################
        # 애셋 타입 필터
        ####################################################################################################
        self.asset_type_filter_grp = QGroupBox('애셋타입')
        self.task_filter_layout.addWidget(self.asset_type_filter_grp)

        #if self.is_shot_entity():
        #    self.asset_type_filter_grp.setVisible(False)

        self.asset_type_filter_grp_layout = QVBoxLayout(self.asset_type_filter_grp)
        self.asset_type_filter_grp_layout.setContentsMargins(10, 10, 10, 10)
        self.asset_type_filter_grp_layout.setSpacing(1)
        self.asset_type_filter_grp_layout.setAlignment(Qt.AlignTop)

        # 전체 선택 / 해제 체크박스
        self.asset_cb = QCheckBox('전체')
        self.asset_type_filter_grp_layout.addWidget(self.asset_cb)
        self.asset_cb.stateChanged.connect(self.asset_cb_changed)
        #cb.is_master = True
        #cb.toggled.connect(partial(self.set_all_checkbox_checked, self.asset_type_filter_grp_layout))

        # separator
        sep = QFrame()
        self.asset_type_filter_grp_layout.addWidget(sep)
        sep.setFrameShape(QFrame.HLine)
        sep.setFrameShadow(QFrame.Sunken)
        sep.setFixedHeight(12)
        self.asset_cb_list=[]
        for atype in ['character', 'prop', 'vehicle', 'env', 'crowd', 'location', 'fx']:
            cb = QCheckBox(atype)
            self.asset_type_filter_grp_layout.addWidget(cb)
            self.asset_cb_list.append(cb)
            #cb.setObjectName(f'{self.FILTER_PREFIX}__asset_types__{atype}')
            #cb.toggled.connect(self.on_filter_checkbox_toggled)

        ####################################################################################################
        # 시퀀스 필터
        ####################################################################################################
        self.sequence_filter_grp = QGroupBox('시퀀스')
        self.task_filter_layout.addWidget(self.sequence_filter_grp)

        #if self.is_asset_entity():
        #    self.sequence_filter_grp.setVisible(False)

        self.sequence_filter_grp_layout = QVBoxLayout(self.sequence_filter_grp)
        self.sequence_filter_grp_layout.setContentsMargins(10, 10, 10, 10)
        self.sequence_filter_grp_layout.setSpacing(1)
        self.sequence_filter_grp_layout.setAlignment(Qt.AlignTop)

        # 전체 선택 / 해제 체크박스
        self.sequence_cb = QCheckBox('전체')
        self.sequence_filter_grp_layout.addWidget(self.sequence_cb)
        self.sequence_cb.stateChanged.connect(self.sequence_cb_changed)
        self.sequence_filter_list=[]
        # separator
        sep = QFrame()
        self.sequence_filter_grp_layout.addWidget(sep)
        sep.setFrameShape(QFrame.HLine)
        sep.setFrameShadow(QFrame.Sunken)
        sep.setFixedHeight(12)

    def searchDriveComboBox_change(self):
        # option var  = 가 있으면 처리를 한다.
        # 선택한 콤보박스를 로그를 남겨보자.
        selected_item = self.searchDriveComboBox.currentText()
        log.info(f' 선택한 아이템 : {selected_item}')
        # 프로젝트를 추가해보자.
        vfx_folder = os.path.join(selected_item, 'vfx')
        if os.path.exists(vfx_folder):
            subfolders = [f for f in os.listdir(vfx_folder) if os.path.isdir(os.path.join(vfx_folder, f))]
            print(subfolders)
            if subfolders:
                for i in subfolders:
                    self.searchProjectComboBox.addItem(i)
        # 프로젝트 추가 완료
    def searchProjectComboBox_change(self):
        selected_item = self.searchProjectComboBox.currentText()
        log.info( f'Project : {selected_item}')
        # 엔티티 변경이 되었다면 테스크리스트에 내용을 추가한다.
        #self.init_task_list()
    pass

    def searchStepTypeComboBox_change(self):
        pass

    def sequence_cb_changed(self,state):
        if state==2:
            for i in self.sequence_filter_list:
                i.setChecked(True)
        else:
            for i in self.sequence_filter_list:
                i.setChecked(False)

    def asset_cb_changed(self,state):
        if state==2:
            for i in self.asset_cb_list:
                i.setChecked(True)
        else:
            for i in self.asset_cb_list:
                i.setChecked(False)
    def step_cb_changed(self,state):
        if state ==2:
            self.cb_mod.setChecked(True)
            self.cb_lkd.setChecked(True)
            self.cb_rig.setChecked(True)
            self.cb_cfx.setChecked(True)
            self.cb_mm.setChecked(True)
            self.cb_ani.setChecked(True)
            self.cb_lit.setChecked(True)
            self.cb_fx.setChecked(True)
            self.cb_comp.setChecked(True)
        else:
            self.cb_mod.setChecked(False)
            self.cb_lkd.setChecked(False)
            self.cb_rig.setChecked(False)
            self.cb_cfx.setChecked(False)
            self.cb_mm.setChecked(False)
            self.cb_ani.setChecked(False)
            self.cb_lit.setChecked(False)
            self.cb_fx.setChecked(False)
            self.cb_comp.setChecked(False)

    def on_entity_selection_changed(self):
        sel = self.get_main_entity()
        print(sel)
        if sel == 0:
            self.cb_mod.setVisible(True)
            self.cb_lkd.setVisible(True)
            self.cb_rig.setVisible(True)
            self.cb_mm.setVisible(False)
            self.cb_ani.setVisible(False)
            self.cb_lit.setVisible(False)
            self.cb_fx.setVisible(False)
            self.cb_comp.setVisible(False)
            self.asset_type_filter_grp.setVisible(True)
            self.sequence_filter_grp.setVisible(False)
            # check
            self.cb_rig.setChecked(True)
        elif sel == 1:
            self.cb_mod.setVisible(False)
            self.cb_lkd.setVisible(False)
            self.cb_rig.setVisible(False)
            self.cb_mm.setVisible(True)
            self.cb_ani.setVisible(True)
            self.cb_lit.setVisible(True)
            self.cb_fx.setVisible(True)
            self.cb_comp.setVisible(True)
            self.asset_type_filter_grp.setVisible(False)
            self.sequence_filter_grp.setVisible(True)
            # check
            self.cb_ani.setChecked(True)
        else:
            self.cb_mod.setVisible(True)
            self.cb_lkd.setVisible(True)
            self.cb_rig.setVisible(True)
            self.cb_mm.setVisible(True)
            self.cb_ani.setVisible(True)
            self.cb_lit.setVisible(True)
            self.cb_fx.setVisible(True)
            self.cb_comp.setVisible(True)
            self.asset_type_filter_grp.setVisible(True)
            self.sequence_filter_grp.setVisible(True)
        if sel ==1:
            # shot 이니깐 시컨스 넣어준다.
            # 1 현재 드라이브
            selected_drive_item = self.searchDriveComboBox.currentText()
            log.info(f' 선택한 drive 아이템 : {selected_drive_item}')
            # 2 현재 프로젝트
            selected_project_item = self.searchProjectComboBox.currentText()
            log.info(f' 선택한  Project 아이템: {selected_project_item}')
            # 드라이브랑 프로젝트가 있으면 시컨스 리스트를 얻는다.
            if (selected_drive_item!='-drive-') and (selected_project_item!='-project-'):
                log.info(f' drive {selected_drive_item} project {selected_project_item}')
                sequence_path = os.path.join(selected_drive_item,'vfx',selected_project_item,'shot')
                log.info(f' sequence {sequence_path} ')
                # 폴더 내 시컨스폴더만 가져온다.
                # 주어진 경로의 모든 항목을 가져옴.
                items = os.listdir(sequence_path)
                episode_list=[]
                for item in items:
                    # 전체 경로 생성
                    pattern = r'e\d{3}'
                    if re.match(pattern,item):
                        full_path = os.path.join(sequence_path,item)
                        if os.path.isdir(full_path):
                            print(full_path)
                            episode_list.append(item)
                # 기존에 시컨스아이템 있으면 삭제하기
                for i in self.sequence_filter_list:
                    i.deleteLater()
                self.sequence_filter_list=[]
                for i in episode_list:
                    cb = QCheckBox(i)
                    self.sequence_filter_grp_layout.addWidget(cb)
                    self.sequence_filter_list.append(cb)
                # 옵션바가 있어서 마지막으로 저장한 에피소드 체크하기

        # 엔티티 변경이 되었다면 테스크리스트에 내용을 추가한다.
        #self.init_task_list()
        #self.get_optionvar_a()
        pass

    def get_main_entity(self):
        if self.asset_entity_radio.isChecked():
            sel = 0
        # 샷이 선택되었을 경우
        elif self.shot_entity_radio.isChecked():
            sel = 1
        # 아무 것도 선택되지 않았을 경우(물론 이런 상황이 없어야 한다)
        else:
            sel = -1
        return sel
    def get_step_filter(self):
        selected_mainentity_item = self.get_main_entity()
        checklist=['mod','lkd','rig','cfx']
        if selected_mainentity_item == 1:
            checklist = ['cfx','mm','ani','lit','fx','comp']
        check_checkbox=[]
        for i in self.step_filter_list:
            if i.isChecked():
                if i.text() in checklist:
                    check_checkbox.append(i)
        return check_checkbox


    def init_task_list(self):
        # 모든값이 정삭정으로 있는지 체크
        str_set_option = ''
        check_option_drive = False
        check_option_project = False
        check_option_main_entity = False
        check_option_step = False
        check_option_asset_sequence = False
        # 이 명령이 떨어지면
        # 1 현재 드라이브
        selected_drive_item = self.searchDriveComboBox.currentText()
        log.info(f' 선택한 drive 아이템 : {selected_drive_item}')
        # 2 현재 프로젝트
        selected_project_item = self.searchProjectComboBox.currentText()
        log.info(f' 선택한  Project 아이템: {selected_project_item}')
        # 3 현재 메인 엔티티
        selected_mainentity_item = self.get_main_entity()
        str_selected_mainentity = 'asset'
        if selected_mainentity_item == 1:
            str_selected_mainentity = 'shot'
        elif selected_mainentity_item == -1:
            str_selected_mainentity = 'none'
        else:
            pass
        log.info(f' 선택한  MainEntity 아이템: {str_selected_mainentity}')
        # 4 현재 파이프라인스탭
        selected_step_list = self.get_step_filter()
        str_step_list = []
        for i in selected_step_list:
            str_step_list.append(i.text())
        log.info(f' 선택한  setep list: {str_step_list}')
        # 5 현재 애셋타입및 시컨스 있는지 체크후
        asset_sequence_list=[]
        if selected_mainentity_item == 1:
            for i in self.sequence_filter_list:
                if i.isChecked():
                    asset_sequence_list.append(i.text())
        elif selected_mainentity_item == -1:
            pass
        else:
            for i in self.asset_cb_list:
                if i.isChecked():
                    asset_sequence_list.append(i.text())
        log.info(f' 선택한  asset sequence list: {asset_sequence_list}')
        # 해당 테이블 리스트에 값을 넣어준다.
        # 12345 중에 단 한개라도 없으면 패스
        if selected_drive_item != '-drive-':
            check_option_drive = True
            str_set_option = str_set_option + selected_drive_item
        if selected_project_item != '-project-':
            check_option_project = True
            str_set_option = str_set_option + ',' + selected_project_item
        if selected_mainentity_item != -1:
            check_option_main_entity = True
            str_set_option = str_set_option + ',' + str(selected_mainentity_item)
        for i in selected_step_list:
            check_option_step = True
            str_set_option = str_set_option + ',' + i.text()
        if selected_mainentity_item == 1:
            for i in self.sequence_filter_list:
                if i.isChecked():
                    check_option_asset_sequence = True
                    str_set_option = str_set_option + ',' + i.text()
        elif selected_mainentity_item == -1:
            pass
        else:
            for i in self.asset_cb_list:
                if i.isChecked():
                    check_option_asset_sequence = True
                    str_set_option = str_set_option + ',' + i.text()

        if check_option_drive and check_option_project and check_option_main_entity and check_option_step and check_option_asset_sequence:
            cmds.optionVar(sv=(self.OPTIONVAR_TASKMANAGER_A, ''))
            self.set_optionvar_a(str_set_option)


    def set_optionvar_a(self,optionA):
        cmds.optionVar(sv=(self.OPTIONVAR_TASKMANAGER_A,optionA))


    def get_optionvar_a(self):
        return_dic={}
        get_string = ( cmds.optionVar(q=self.OPTIONVAR_TASKMANAGER_A) )
        if len(get_string) > 4:
            get_list=(get_string.split(','))
            self.searchDriveComboBox.setCurrentText(get_list[0])
            return_dic['drive']=get_list[0]
            self.searchProjectComboBox.setCurrentText(get_list[1])
            return_dic['project'] = get_list[1]
            if int(get_list[2]) == 0:
                self.asset_entity_radio.setChecked(True)
                return_dic['main_entity'] = 'asset'
            else:
                self.shot_entity_radio.setChecked(True)
                return_dic['main_entity'] = 'shot'
            self.on_entity_selection_changed()
            step_list = []
            for i in get_list[3:]:
                if i in ['mod','lkd','rig','cfx','mm','ani','lit','fx','comp']:
                    for j in self.step_filter_list:
                        # log.info(f' 선택 된 스텝{j.text()} {i}')
                        if j.text() == i:
                            j.setChecked(True)
                            step_list.append(i)
            return_dic['step'] = step_list
            asset_list = []
            for i in get_list[3:]:
                if i in ['character', 'prop', 'vehicle', 'env', 'crowd', 'location', 'fx']:
                    for j in self.asset_cb_list:
                        if j.text() == i:
                            j.setChecked(True)
                            asset_list.append(i)
            return_dic['asset'] = asset_list
            sequence_list = []
            for i in get_list[3:]:
                for j in self.sequence_filter_list:
                    if j.text() == i:
                        j.setChecked(True)
                        sequence_list.append(i)
            return_dic['sequence'] = sequence_list
        return return_dic

    def get_shot_code(self,path_a):
        # sequence path 를 주면 샷 폴더 패치를 반환한다.
        pattenrn1=r"e\d+_s\d+_c\d+"
        pattenrn2=r"e\d+_s\d+_\d+"
        return_list = []
        items = os.listdir(path_a)
        for item in items:
            # check folder
            if os.path.isdir(os.path.join(path_a,item)):
                if re.match(pattenrn1,item) or re.match(pattenrn2,item):
                    return_list.append(item)
        return return_list

    def search_pushbutton_clicked(self):
        self.init_task_list()
        get_dic = self.get_optionvar_a()
        log.info(f'테이블 위젯 시작')
        log.info(f'해드 만들기')
        project_path = os.path.join(get_dic['drive'],'vfx',get_dic['project'])
        main_entity_path = os.path.join(project_path,get_dic['main_entity'])
        log.info(f'project path {project_path}')
        log.info(f'entity path {main_entity_path}')
        for i in get_dic['sequence']:
            sequence_a = os.path.join(main_entity_path,i)
            log.info(f'sequence path {sequence_a}')
            for j in self.get_shot_code(sequence_a):
                log.info(f'샷 패치 {j}')
        HEADER_LABELS_ASSET = ['Type', 'Code', 'Name', 'Task']
        HEADER_LABELS_SHOT = ['Sequence', 'Scene', 'Shot', 'Task']
        self.task_list_widget.setColumnCount(5)
        self.task_list_widget.setHorizontalHeaderLabels(HEADER_LABELS_SHOT)
        pass
def show_window():
    global TaskManagerWindow

    try:
        TaskManagerWindow.close()
        TaskManagerWindow.deleteLater()
    except:
        pass

    taskmanagerwin = TaskManagerWindow()
    taskmanagerwin.show()
