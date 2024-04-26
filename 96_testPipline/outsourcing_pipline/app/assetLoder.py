# 마야에서 로그를 불러올수 있는지 체크
import outsourcing_pipline.log
import importlib
#importlib.reload(outsourcing_pipline.log)
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2 import __version__
from maya.app.general import mayaMixin
import pymel.core as pm
from outsourcing_pipline.config import INHOUSETOOLS_ICON_PATH
importlib.reload( outsourcing_pipline.config)
import os
# 로그
log = outsourcing_pipline.log.get_logger('asset_loader')
log.info(' 마야에서 로그가 프린트 되는지 체크 ')


def img_path(img):
    return os.path.join(INHOUSETOOLS_ICON_PATH, img)
class AssetLoaderWindow(mayaMixin.MayaQWidgetBaseMixin,QMainWindow):
    WINDOW_NAME = 'vive_asset_loader_window_a'
    def __init__(self):
        super(AssetLoaderWindow, self).__init__()
        log.info('어셋로더 Class 시작합니다.')
        if pm.window(self.WINDOW_NAME, q=True, ex=True):
            pm.deleteUI(self.WINDOW_NAME, window=True)
        self.setObjectName(self.WINDOW_NAME)
        self.setWindowTitle(self.WINDOW_NAME)
        self.setGeometry(200, 200, 1000, 800)
        log.info(f'창로고 {img_path("vive_initial_logo.png")}')
        self.setWindowIcon(QIcon(img_path('vive_initial_logo.png')))
        self.ui()
        pass

    def ui(self):
        log.info('어셋로더 ui 시작합니다.')
        log.info(f'{INHOUSETOOLS_ICON_PATH}')
        #log.info(f'{INHOUSETOOLS_DRIVE_SERVER}')
        #print (self.img_path('abcd.jpg'))
        # 이미지를 넣을려고했는데 -경훈td-님은 환경설정을 잡았다.  환경설정 추가

        #Qframe QVBoxLayout
        # 메인 위젯 생성
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
        #frameAppBanner.setFixedWidth(1500)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed))

        window_layout = QVBoxLayout(self.centralWidget())
        window_layout.setContentsMargins(0, 0, 0, 0)
        window_layout.setSpacing(0)
        window_layout.setAlignment(Qt.AlignTop)

        main_widget.setLayout(window_layout)
        window_layout.addWidget(frameAppBanner)

        # 메인 레이아웃 : QHBoxLayout
        frameAppBannermain_layout = QHBoxLayout(frameAppBanner)
        frameAppBannermain_layout.setContentsMargins(10, 0, 0, 0)
        frameAppBannermain_layout.setSpacing(10)
        frameAppBannermain_layout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        #window_layout.addLayout(frameAppBanner)

        # 앱의 이름과 제작사 이름
        frameAppBannerapp_layout = QVBoxLayout()
        frameAppBannerapp_layout.setSpacing(0)
        frameAppBannerapp_layout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        frameAppBannermain_layout.addLayout(frameAppBannerapp_layout)

        # 앱 이름
        frameAppBannertitle_label = QLabel(u"Asset 로더 ")
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
        self.searchAssetTypeComboBox.addItem("Asset-type")
        self.searchAssetTypeComboBox.setMaxVisibleItems(12)
        self.searchAssetTypeComboBox.currentIndexChanged.connect(self.searchAssetTypeComboBox_change)
        search_filter_layout.addWidget(self.searchAssetTypeComboBox)

        # 스플리터 생성
        ####################################################################################################
        self.splitter = QSplitter()
        self.splitter.setSizes([8,2])
        self.splitter.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        #self.splitter.splitterMoved.connect(self.on_splitter_moved)
        window_layout.addWidget(self.splitter)

        # 애셋 리스트 그룹
        ####################################################################################################
        self.asset_list_scroll = QScrollArea()
        self.asset_list_scroll.setWidget(QWidget())
        self.asset_list_scroll.setWidgetResizable(True)
        self.asset_list_scroll.setFrameShape(QFrame.Panel)
        self.asset_list_scroll.setFrameShadow(QFrame.Sunken)
        self.asset_list_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.splitter.addWidget(self.asset_list_scroll )

        self.asset_list_layout = FlowLayout(self.asset_list_scroll.widget())
        self.asset_list_layout.setSpacing(20)

        # 애셋 임포트 현황
        ####################################################################################################
        status_widget = QWidget()
        status_layout = QVBoxLayout(status_widget)
        status_layout.setContentsMargins(0, 0, 0, 0)
        status_layout.setSpacing(5)

        lbl = QLabel('선택한 애셋')
        lbl.setAlignment(Qt.AlignCenter)
        lbl.setFixedHeight(30)
        lbl.setStyleSheet('color:#c8c8c8;background-color:black')
        status_layout.addWidget(lbl)
        self.splitter.addWidget(status_widget)

        #-------------------
        self.asset_selection_scroll = QScrollArea(status_widget)
        self.asset_selection_scroll.setWidget(QWidget())
        self.asset_selection_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.asset_selection_scroll.setFrameShape(QScrollArea.Box)
        self.asset_selection_scroll.setFrameShadow(QScrollArea.Sunken)
        self.asset_selection_scroll.setWidgetResizable(True)

        self.asset_selection_scroll_layout = QVBoxLayout(self.asset_selection_scroll.widget())
        self.asset_selection_scroll_layout.setAlignment(Qt.AlignTop)
        self.asset_selection_scroll_layout.setSpacing(0)

        self.import_btn = QPushButton('선택한 애셋 불러오기')
        self.import_btn.clicked.connect( self.import_btn_connect)
        self.import_btn.setFixedHeight(40)
        #self.import_btn.setIcon(QIcon(img_path('download_white.png')))
        #self.import_btn.setIconSize(QSize(15, 15))

        status_layout.addWidget(self.asset_selection_scroll)
        status_layout.addWidget(self.import_btn)

    def import_btn_connect(self):
        pass

    def asset_list_layout_item_remove(self):
        countlayoutitem = self.asset_list_layout.count()
        print (countlayoutitem)
        for i in reversed(range(countlayoutitem)):
            item = self.asset_list_layout.itemAt(i)
            if isinstance(item, QSpacerItem):
                self.asset_list_layout.removeItem(item)
            elif item.widget() is not None:
                widget = item.widget()
                self.asset_list_layout.removeWidget(widget)
                widget.deleteLater()



        #print ('a')

    def searchDriveComboBox_change(self):
        # option var  = 가 있으면 처리를 한다.
        # 선택한 콤보박스를 로그를 남겨보자.
        selected_item=self.searchDriveComboBox.currentText()
        log.info(f' 선택한 아이템 : {selected_item}')
        # 프로젝트를 추가해보자.
        vfx_folder=os.path.join(selected_item,'vfx')
        if os.path.exists(vfx_folder):
            subfolders = [f for f in os.listdir(vfx_folder) if os.path.isdir(os.path.join(vfx_folder,f))]
            print (subfolders)
            if subfolders:
                for i in subfolders:
                    self.searchProjectComboBox.addItem(i)
        #프로젝트 추가 완료
        pass

    def searchProjectComboBox_change(self):
        # 현재 선택한 프로젝트 log info
        selected_dirve_item = self.searchDriveComboBox.currentText()
        selected_project_item = self.searchProjectComboBox.currentText()
        log.info(f' 선택한 drive : {selected_dirve_item}')
        log.info(f' 선택한 프로젝트 : {selected_project_item}')
        if selected_dirve_item and selected_project_item:
            vfx_folder = os.path.join(selected_dirve_item, 'vfx', selected_project_item,'asset')
            if os.path.exists(vfx_folder):
                subfolders = [f for f in os.listdir(vfx_folder) if os.path.isdir(os.path.join(vfx_folder, f))]
                print(subfolders)
                if subfolders:
                    for i in subfolders:
                        if i in ['.mayaSwatches','assetName']:
                            pass
                        else:
                            self.searchAssetTypeComboBox.addItem(i)
    def searchAssetTypeComboBox_change(self):
        selected_dirve_item = self.searchDriveComboBox.currentText()
        selected_project_item = self.searchProjectComboBox.currentText()
        selected_asset_item = self.searchAssetTypeComboBox.currentText()
        log.info(f' 선택한 drive : {selected_dirve_item}')
        log.info(f' 선택한 프로젝트 : {selected_project_item}')
        log.info(f' 선택한 프로젝트 : {selected_asset_item}')
        if selected_dirve_item and selected_project_item and selected_asset_item:
            if selected_asset_item=='Asset-type':
                self.asset_list_layout_item_remove()
                return
            vfx_folder = os.path.join(selected_dirve_item,
                    'vfx', selected_project_item,
                    'asset', selected_asset_item)
            if os.path.exists(vfx_folder):
                subfolders = [f for f in os.listdir(vfx_folder) if os.path.isdir(os.path.join(vfx_folder, f))]
                print(subfolders)
                self.asset_list_layout_item_remove()
                for i in subfolders:
                    item = AssetIconWidget(i, parent=self)
                    self.asset_list_layout.addWidget(item)
            print (self.asset_list_layout.count)
        pass
class FlowLayout(QLayout):
    def __init__(self, parent=None):
        super(FlowLayout, self).__init__(parent)
        self.margin = 9
        self.space_x = 9
        self.space_y = 9
        self.itemList = []

    def __del__(self):
        item = self.takeAt(0)
        while item:
            item = self.takeAt(0)

    def setSpacing(self, space):
        super().setSpacing(space)
        super().setContentsMargins(space, space, space, space)
        self.space_x = space
        self.space_y = space
        self.margin = space

    def addItem(self, item):
        self.itemList.append(item)

    def count(self):
        return len(self.itemList)

    def itemAt(self, index):
        if 0 <= index < len(self.itemList):
            return self.itemList[index]

    def takeAt(self, index):
        if 0 <= index < len(self.itemList):
            return self.itemList.pop(index)

    def expandingDirections(self):
        return Qt.Orientations(Qt.Orientation(0))

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        height = self.do_layout(QRect(0, 0, width, 0))
        return height

    def setGeometry(self, rect):
        super(FlowLayout, self).setGeometry(rect)
        self.do_layout(rect)

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        size = QSize()

        for item in self.itemList:
            size = size.expandedTo(item.minimumSize())

        size += QSize(self.contentsMargins().top() + self.contentsMargins().bottom(),
                      self.contentsMargins().left() + self.contentsMargins().right())
        return size

    def do_layout(self, rect):
        x = rect.x() + self.contentsMargins().left()
        y = rect.y() + self.contentsMargins().top()
        line_height = 0

        for item in self.itemList:
            next_x = x + item.sizeHint().width() + self.space_x
            if next_x - self.space_x > rect.right() - self.contentsMargins().right() and line_height > 0:
                x = rect.x() + self.contentsMargins().left()
                y = y + line_height + self.space_y
                next_x = x + item.sizeHint().width() + self.space_x
                line_height = 0

            item.setGeometry(QRect(QPoint(x, y), item.sizeHint()))

            x = next_x
            line_height = max(line_height, item.sizeHint().height())

        return y + line_height - rect.y() + self.contentsMargins().bottom()

class AssetIconWidget(QWidget):

    LABEL_COMMON_HEIGHT = 25

    def __init__(self, asset, icon_size=250, parent=None):
        """
        :param vive.model.Asset asset:
        :param int icon_size: 썸네일 아이콘의 사이즈. 기본값은 100이다.
        :param AssetLoaderWindow parent:
        """
        super().__init__(parent)
        self.asset = asset
        self.icon_size = icon_size
        self.parent = parent
        self.ui()
        self.init_thumbnail(clear=True)
    def ui(self):
        # 위젯의 전체 사이즈를 맞춘다.
        self.setFixedWidth(self.icon_size)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        # 애셋코드
        display_name = self.asset
        self.asset_code_label = QLabel(display_name)
        main_layout.addWidget(self.asset_code_label)
        self.asset_code_label.setAlignment(Qt.AlignCenter)
        self.asset_code_label.setStyleSheet("""
                    QLabel {
                        background-color: #222;
                    }
                """)



    def init_thumbnail(self, clear=False):
        if not clear and os.path.isfile(self.asset.thumbnail_file):
            icon_file = self.asset.thumbnail_file
        else:
            icon_file = img_path('no_image_300_300.png')

def show_window():
    global AssetLoaderWindow

    try:
        AssetLoaderWindow.close()
        AssetLoaderWindow.deleteLater()
    except:
        pass

    assetloaderwin = AssetLoaderWindow()
    assetloaderwin.show()
