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

# 로그
log = outsourcing_pipline.log.get_logger('taskManager 00')
log.info(' 마야에서 로그가 프린트 되는지 체크 ')

def img_path(img):
    return os.path.join(INHOUSETOOLS_ICON_PATH, img)

class TaskManagerWindow(mayaMixin.MayaQWidgetBaseMixin,QMainWindow):
    # 윈도우 오브젝트의 이름
    WINDOW_NAME = 'task_manager_window_a'
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
        task_filter_widget_layout.addWidget(self.main_entity_grp)

        main_entity_grp_layout = QHBoxLayout(self.main_entity_grp)
        main_entity_grp_layout.setContentsMargins(10, 10, 10, 10)
        main_entity_grp_layout.setSpacing(10)
        main_entity_grp_layout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        # 버튼 그룹
        self.main_entity_btn_grp = QButtonGroup()
        #self.main_entity_btn_grp.buttonReleased.connect(self.on_entity_selection_changed)
        # 애셋 라디오 버튼
        self.asset_entity_radio = QRadioButton('애셋')
        main_entity_grp_layout.addWidget(self.asset_entity_radio)
        # 스페이서
        main_entity_grp_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Fixed))
        # 샷 라디오 버튼
        self.shot_entity_radio = QRadioButton('샷')
        main_entity_grp_layout.addWidget(self.shot_entity_radio)
        """
        # 버튼 그룹에 애셋, 샷 라디오 버튼 등록
        self.main_entity_btn_grp.setId(self.asset_entity_radio, 0)
        self.main_entity_btn_grp.setId(self.shot_entity_radio, 1)
        self.main_entity_btn_grp.addButton(self.asset_entity_radio)
        self.main_entity_btn_grp.addButton(self.shot_entity_radio)
        """
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
        cb = QCheckBox('전체')
        self.step_filter_grp_layout.addWidget(cb)
        #cb.is_master = True
        #cb.toggled.connect(partial(self.set_all_checkbox_checked, self.step_filter_grp_layout))

        # separator
        sep = QFrame()
        self.step_filter_grp_layout.addWidget(sep)
        sep.setFrameShape(QFrame.HLine)
        sep.setFrameShadow(QFrame.Sunken)
        sep.setFixedHeight(12)

        cb = QCheckBox('mod')
        self.step_filter_grp_layout.addWidget(cb)
        #cb.setIcon(QIcon(img_path('step/step_modeling.png')))
        #cb.sg_step = ShotgridPipelineStep.MODELING
        #cb.setObjectName(f'{self.FILTER_PREFIX}__steps__mod')
        #cb.toggled.connect(self.on_filter_checkbox_toggled)

        cb = QCheckBox('lkd')
        self.step_filter_grp_layout.addWidget(cb)
        #cb.setIcon(QIcon(img_path('step/step_lookdev.png')))
        #cb.sg_step = ShotgridPipelineStep.LOOKDEV
        #cb.setObjectName(f'{self.FILTER_PREFIX}__steps__lkd')
        #cb.toggled.connect(self.on_filter_checkbox_toggled)

        cb = QCheckBox('rig')
        self.step_filter_grp_layout.addWidget(cb)
        #cb.setIcon(QIcon(img_path('step/step_rigging.png')))
        #cb.sg_step = ShotgridPipelineStep.RIGGING
        #cb.setObjectName(f'{self.FILTER_PREFIX}__steps__rig')
        #cb.toggled.connect(self.on_filter_checkbox_toggled)

        cb = QCheckBox('cfx')
        self.step_filter_grp_layout.addWidget(cb)
        #cb.setIcon(QIcon(img_path('step/step_cfx.png')))
        #cb.sg_step = ShotgridPipelineStep.CFX_ASSET
        #cb.setObjectName(f'{self.FILTER_PREFIX}__steps__cfx')
        #cb.toggled.connect(self.on_filter_checkbox_toggled)

        step_code = 'mm'
        cb = QCheckBox(step_code)
        self.step_filter_grp_layout.addWidget(cb)
        #cb.setIcon(QIcon(img_path('step/step_matchmove.png')))
        #cb.sg_step = ShotgridPipelineStep.MATCHMOVE
        #cb.setObjectName(f'{self.FILTER_PREFIX}__steps__{step_code}')
        #cb.toggled.connect(self.on_filter_checkbox_toggled)

        step_code = 'ani'
        cb = QCheckBox(step_code)
        self.step_filter_grp_layout.addWidget(cb)
        #cb.setIcon(QIcon(img_path('step/step_animation.png')))
        #cb.sg_step = ShotgridPipelineStep.ANIMATION
        #cb.setObjectName(f'{self.FILTER_PREFIX}__steps__{step_code}')
        #cb.toggled.connect(self.on_filter_checkbox_toggled)

        step_code = 'lit'
        cb = QCheckBox(step_code)
        self.step_filter_grp_layout.addWidget(cb)
        #cb.setIcon(QIcon(img_path('step/step_lighting.png')))
        #cb.sg_step = ShotgridPipelineStep.LIGHTING
        #cb.setObjectName(f'{self.FILTER_PREFIX}__steps__{step_code}')
        #cb.toggled.connect(self.on_filter_checkbox_toggled)

        step_code = 'fx'
        cb = QCheckBox(step_code)
        self.step_filter_grp_layout.addWidget(cb)
        #cb.setIcon(QIcon(img_path('step/step_fx.png')))
        #cb.sg_step = ShotgridPipelineStep.FX
        #cb.setObjectName(f'{self.FILTER_PREFIX}__steps__{step_code}')
        #cb.toggled.connect(self.on_filter_checkbox_toggled)

        step_code = 'comp'
        cb = QCheckBox(step_code)
        self.step_filter_grp_layout.addWidget(cb)
        #cb.setIcon(QIcon(img_path('step/step_composition.png')))
        #cb.sg_step = ShotgridPipelineStep.COMPOSITION
        #cb.setObjectName(f'{self.FILTER_PREFIX}__steps__{step_code}')
        #cb.toggled.connect(self.on_filter_checkbox_toggled)

        ##################################################
        # 메인 태스크 리스트 위젯
        ##################################################
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
        cb = QCheckBox('전체')
        self.asset_type_filter_grp_layout.addWidget(cb)
        #cb.is_master = True
        #cb.toggled.connect(partial(self.set_all_checkbox_checked, self.asset_type_filter_grp_layout))

        # separator
        sep = QFrame()
        self.asset_type_filter_grp_layout.addWidget(sep)
        sep.setFrameShape(QFrame.HLine)
        sep.setFrameShadow(QFrame.Sunken)
        sep.setFixedHeight(12)

        for atype in ['character', 'prop', 'vehicle', 'env', 'crowd', 'location', 'fx']:
            cb = QCheckBox(atype)
            self.asset_type_filter_grp_layout.addWidget(cb)
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
        cb = QCheckBox('전체')
        self.sequence_filter_grp_layout.addWidget(cb)
        #cb.is_master = True
        #cb.toggled.connect(partial(self.set_all_checkbox_checked, self.sequence_filter_grp_layout))

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
        pass
    def searchStepTypeComboBox_change(self):
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
