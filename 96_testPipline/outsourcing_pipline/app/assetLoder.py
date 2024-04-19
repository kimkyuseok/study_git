# 마야에서 로그를 불러올수 있는지 체크
import outsourcing_pipline.log
#import importlib
#importlib.reload(outsourcing_pipline.log)
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2 import __version__
from maya.app.general import mayaMixin
import pymel.core as pm
# 로그
log = outsourcing_pipline.log.get_logger('asset_loader')
log.info(' 마야에서 로그가 프린트 되는지 체크 ')


class AssetLoaderWindow(mayaMixin.MayaQWidgetBaseMixin,QMainWindow):
    WINDOW_NAME = 'vive_asset_loader_window'
    def __init__(self):
        super(AssetLoaderWindow, self).__init__()
        log.info('어셋로더 Class 시작합니다.')
        if pm.window(self.WINDOW_NAME, q=True, ex=True):
            pm.deleteUI(self.WINDOW_NAME, window=True)
        self.setObjectName(self.WINDOW_NAME)
        self.setWindowTitle(self.WINDOW_NAME)
        self.setGeometry(200, 200, 1000, 800)
        self.ui()
        pass

    def ui(self):
        log.info('어셋로더 ui 시작합니다.')
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
