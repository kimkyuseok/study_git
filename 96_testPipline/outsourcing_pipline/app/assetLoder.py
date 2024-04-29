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
import maya.cmds as cmds
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
        self.selected_assets = {}
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

    def delete_selected_item(self,item):
        """선택한 애셋을 삭제했을 때 처리해야할 내용"""
        element = False
        for selected in self.selected_assets:
            if item == self.selected_assets[selected]['item']:
                element = selected
                break
        if element:
            del self.selected_assets[element]
            item.close()
            item.deleteLater()

    def append_asset(self, asset):
        """
        :param Asset asset:
        """
        selected_dirve_item = self.searchDriveComboBox.currentText()
        selected_project_item = self.searchProjectComboBox.currentText()
        selected_asset_item = self.searchAssetTypeComboBox.currentText()
        log.info(f' 선택된 드라이브 프로젝트 어셋타입 {selected_dirve_item} {selected_project_item} {selected_asset_item}')
        # 프로젝트 경로에 파일이 있으면 콤보박스에 추가
        projectComboPath = os.path.join(selected_dirve_item, 'vfx', selected_project_item, 'asset', selected_asset_item)
        rig_pub_mb_file = os.path.join(projectComboPath, asset, 'rig', 'pub', 'scenes', asset + '_rig.mb')
        mod_pub_mb_file = os.path.join(projectComboPath, asset, 'mod', 'pub', 'scenes', asset + '_mod.mb')
        lkd_pub_mb_file = os.path.join(projectComboPath, asset, 'lkd', 'pub', 'scenes', asset + '_default_shd.mb')

        # mod, lkd, rig 파일이 모두 없다면 등록할 수 없다.
        exists = False
        if os.path.isfile(rig_pub_mb_file):
            exists = True
        if os.path.isfile(mod_pub_mb_file):
            exists = True
        if os.path.isfile(lkd_pub_mb_file):
            exists = True
        if not exists:
            return


        # 애셋 선택 현황 사전에 해당 애셋이 등록되어있는지 확인하고,
        # 있다면 해당 애셋의 임포트 수량을 +1 시킨다.
        if asset in self.selected_assets:
            log.info(f' {asset} 선택한 어셋 리스트에 있음 ')
            item = self.selected_assets[asset]['item']
            #item.add_number()
        else:
            # AssetSelectionStatusItem 클래스 타입 인스턴스를 생성한다.
            item = _SelectedAssetItem(asset=asset, parent=self)
            # 아이템을 레이아웃에 추가한다.
            self.asset_selection_scroll_layout.addWidget(item)

            self.selected_assets[asset] = {
                'item': item,
                'asset': asset,
            }
    def import_btn_connect(self):
        log.info(f' asset 불러오기')
        selected = []

        # 어셋 현황에 있는 위젯을 분석한다.
        for i in range(self.asset_selection_scroll_layout.count()):
            sel = self.asset_selection_scroll_layout.itemAt(i).widget()
            print (sel.get_asset())
            selected.append({
                'asset': sel.get_asset(),
                'namespace': sel.get_namespace(),
                'file_type': sel.get_file_type(),
                'import_mode': sel.get_import_mode(),
                'number': sel.get_number(),
            })
        # 처리한 위젯을 리스트에서 제거한다.
        for i in reversed(range(self.asset_selection_scroll_layout.count())):
            w = self.asset_selection_scroll_layout.itemAt(i).widget()
            w.setParent(None)
        log.info(f' 선택한 어셋 리스트??? {selected}')
        for sel in selected:
            asset = sel['asset']
            log.debug(f'asset : {asset}')
            selected_dirve_item = self.searchDriveComboBox.currentText()
            selected_project_item = self.searchProjectComboBox.currentText()
            selected_asset_item = self.searchAssetTypeComboBox.currentText()
            log.info(f' 선택된 드라이브 프로젝트 어셋타입 {selected_dirve_item} {selected_project_item} {selected_asset_item}')
            # 프로젝트 경로에 파일이 있으면 콤보박스에 추가
            projectComboPath = os.path.join(selected_dirve_item, 'vfx', selected_project_item, 'asset',
                                            selected_asset_item)
            rig_pub_mb_file = os.path.join(projectComboPath, asset, 'rig', 'pub', 'scenes', asset + '_rig.mb')
            mod_pub_mb_file = os.path.join(projectComboPath, asset, 'mod', 'pub', 'scenes', asset + '_mod.mb')
            lkd_pub_mb_file = os.path.join(projectComboPath, asset, 'lkd', 'pub', 'scenes', asset + '_default_shd.mb')

            apath = os.path.join(projectComboPath, asset)
            log.info(f'apath : {apath}')
            for i in range(sel['number']):
                if sel['file_type'] == 'mod':
                    pub_file = mod_pub_mb_file
                elif sel['file_type'] == 'lkd':
                    pub_file = lkd_pub_mb_file
                else:
                    pub_file = rig_pub_mb_file

                log.info(f'pub_file : {pub_file}')
                if not os.path.isfile(pub_file):
                    log.error('pub_file does not exist.')
                    continue
                secne_reference = pm.ls(type='reference')
                count = {}
                count_key = sel['namespace']
                if count_key in count:
                    count[count_key] += 1
                else:
                    count[count_key] = 1
                for i in secne_reference:
                    log.info(f'레퍼런스이름  : {i}')
                    if i.find('UNKNOWN_REF_NODE') != -1:
                        pass
                    elif i.find('sharedReferenceNode') != -1:
                        pass
                    else:
                        top_group_name = pm.referenceQuery(i, nodes=1)[0].rsplit(':', 1)[1]
                        count_key = top_group_name
                        if count_key in count:
                            count[count_key] += 1
                        else:
                            count[count_key] = 1
                namespace000 = f"{sel['namespace']}{count[sel['namespace']]:03d}"
                log.info(f' new namespace  : {namespace000}')
                if sel['import_mode'] == 'REFERENCE_MODE':
                    nodes = cmds.file(
                        pub_file,
                        reference=True,
                        ignoreVersion=True,
                        namespace=namespace000,
                        prompt=False,
                        returnNewNodes=True
                    )
                else:
                    nodes = cmds.file(
                        pub_file,
                        i=True,
                        ignoreVersion=True,
                        namespace=sel['namespace'],
                        prompt=False,
                        returnNewNodes=True
                    )
        self.selected_assets = {}
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

        projectComboPath = os.path.join(selected_dirve_item, 'vfx', selected_project_item, 'asset', selected_asset_item)

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
                    asset=i
                    rig_pub_mb_file = os.path.join(projectComboPath, asset, 'rig', 'pub', 'scenes', asset + '_rig.mb')
                    mod_pub_mb_file = os.path.join(projectComboPath, asset, 'mod', 'pub', 'scenes', asset + '_mod.mb')
                    lkd_pub_mb_file = os.path.join(projectComboPath, asset, 'lkd', 'pub', 'scenes',
                                                   asset + '_default_shd.mb')

                    # mod, lkd, rig 파일이 모두 없다면 등록할 수 없다.
                    exists = False
                    if os.path.isfile(rig_pub_mb_file):
                        exists = True
                    if os.path.isfile(mod_pub_mb_file):
                        exists = True
                    if os.path.isfile(lkd_pub_mb_file):
                        exists = True
                    if exists==True:
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
        #self.asset_code_label.clacked.connect(self.printitem)
        main_layout.addWidget(self.asset_code_label)
        self.asset_code_label.setAlignment(Qt.AlignCenter)
        self.asset_code_label.setFixedHeight(50)
        self.asset_code_label.setStyleSheet("""
                    QLabel {
                        background-color: #222;
                    }
                """)
        self.asset_code_button = QPushButton('select asset')
        self.asset_code_button.clicked.connect(self.printitem)
        main_layout.addWidget(self.asset_code_button)


    def printitem(self):
        asset=self.asset_code_label.text()
        self.parent.append_asset(asset)
        print (self.asset_code_label.text())
        pass
    def init_thumbnail(self, clear=False):
        if not clear and os.path.isfile(self.asset.thumbnail_file):
            icon_file = self.asset.thumbnail_file
        else:
            icon_file = img_path('no_image_300_300.png')

class _SelectedAssetItem(QFrame):
    """어셋을 선택했을 때 우측 어셋 선택 현황 위젯에 추가될 리스트 아이템 클래스"""

    def __init__(self, asset, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.ui()
        self.set_asset(asset)

    def ui(self):
        self.setFrameShape(QFrame.Panel)
        self.setFrameShadow(QFrame.Raised)

        self.item_layout = QVBoxLayout(self)
        self.item_layout.setContentsMargins(10, 10, 10, 10)
        self.item_layout.setSpacing(5)

        # 어셋 코드, 임포트 방식, 네임스페이스용 폼레이아웃
        form_layout = QFormLayout()
        form_layout.setSpacing(3)
        self.item_layout.addLayout(form_layout)

        # 썸네일
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        layout.setAlignment(Qt.AlignBottom)
        form_layout.addRow(None, layout)

        # 삭제 버튼
        delete_button = QPushButton(' 목록에서 제거')
        delete_button.setFixedHeight(25)
        delete_button.clicked.connect(self.on_item_deleted)
        layout.addWidget(delete_button)

        # 어셋 코드
        self._asset_code_field = QLineEdit()
        #self._asset_code_field.setFixedHeight(25)
        self._asset_code_field.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        form_layout.addRow(QLabel('애셋코드'), self._asset_code_field)

        # 네임스페이스
        self._namespace_field = QLineEdit()
        self._namespace_field.setFixedHeight(25)
        self._namespace_field.setPlaceholderText('Namespace')
        form_layout.addRow(QLabel('네임스페이스'), self._namespace_field)

        # 불러올 파일
        self.file_type_combo = QComboBox()
        self.file_type_combo.setFixedWidth(100)
        self.file_type_combo.setFixedHeight(25)
        form_layout.addRow(QLabel('파일 타입'), self.file_type_combo)

        # 임포트 방식
        self._import_type_combo = QComboBox()
        self._import_type_combo.setFixedWidth(100)
        self._import_type_combo.setFixedHeight(25)
        self._import_type_combo.addItem('REFERENCE_MODE')
        self._import_type_combo.addItem('IMPORT_MODE')
        form_layout.addRow(QLabel('불러오기 방식'), self._import_type_combo)

        # 임포트 할 수량
        self._number_field = QSpinBox(self)
        form_layout.addRow(QLabel('개수'), self._number_field)
        self._number_field.setFixedWidth(100)
        self._number_field.setFixedHeight(25)
        self._number_field.setMinimum(0)
        self._number_field.setValue(1)
        #self._number_field.valueChanged.connect(self.set_number)
    def get_asset(self):
        return self.asset

    def get_namespace(self):
        return self._namespace_field.text()

    def get_file_type(self):
        return self.file_type_combo.currentText()

    def get_import_mode(self):
        return self._import_type_combo.currentText()

    def get_number(self):
        return self._number_field.value()
    def set_asset(self,asset):
        self.asset = asset
        log.info(f' asset set ')
        self._asset_code_field.setText(asset)
        self._namespace_field.setText(asset)

        selected_dirve_item = self.parent.searchDriveComboBox.currentText()
        selected_project_item = self.parent.searchProjectComboBox.currentText()
        selected_asset_item = self.parent.searchAssetTypeComboBox.currentText()
        log.info(f' 선택된 드라이브 프로젝트 어셋타입 {selected_dirve_item} {selected_project_item} {selected_asset_item}')
        # 프로젝트 경로에 파일이 있으면 콤보박스에 추가
        projectComboPath = os.path.join(selected_dirve_item,'vfx',selected_project_item,'asset',selected_asset_item)
        rig_pub_mb_file = os.path.join(projectComboPath,asset,'rig','pub','scenes',asset+'_rig.mb')
        mod_pub_mb_file = os.path.join(projectComboPath, asset, 'mod', 'pub', 'scenes', asset + '_mod.mb')
        lkd_pub_mb_file = os.path.join(projectComboPath, asset, 'lkd', 'pub', 'scenes', asset + '_default_shd.mb')

        if os.path.isfile(rig_pub_mb_file):
            log.info(f' rig pub file { rig_pub_mb_file }')
            self.file_type_combo.addItem('rig')
        else:
            log.info(f' rig pub file None : {rig_pub_mb_file}')

        if os.path.isfile(mod_pub_mb_file):
            log.info(f' rig pub file {mod_pub_mb_file}')
            self.file_type_combo.addItem('mod')
        else:
            log.info(f' rig pub file None : {mod_pub_mb_file}')

        if os.path.isfile(lkd_pub_mb_file):
            log.info(f' rig pub file {lkd_pub_mb_file}')
            self.file_type_combo.addItem('lkd')
        else:
            log.info(f' rig pub file None : {lkd_pub_mb_file}')
    def on_item_deleted(self):
        """현재 아이템을 삭제하는 메소드"""
        log.info(f'delete === {self._asset_code_field.text()} === item')
        self.parent.delete_selected_item(self)
    pass
def show_window():
    global AssetLoaderWindow

    try:
        AssetLoaderWindow.close()
        AssetLoaderWindow.deleteLater()
    except:
        pass

    assetloaderwin = AssetLoaderWindow()
    assetloaderwin.show()
