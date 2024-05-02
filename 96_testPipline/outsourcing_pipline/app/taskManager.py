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

        # self.search_btn = QPushButton('test')
        # task_top_layout.addWidget(self.search_btn)
        # 스페이서
        #task_top_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Fixed))
        task_filter_widget_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Fixed, QSizePolicy.Expanding))

        # self.searchB_btn = QPushButton('testB')
        # task_top_layout.addWidget(self.searchB_btn)

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
