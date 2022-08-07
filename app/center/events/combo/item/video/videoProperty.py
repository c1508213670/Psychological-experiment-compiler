from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QTabWidget, QHBoxLayout, QPushButton, QVBoxLayout

from app.func import Func
from .videoGeneral import VideoGeneral


class VideoProperty(QWidget):
    def __init__(self, parent=None):
        super(VideoProperty, self).__init__(parent)
        self.setWindowIcon(Func.getImageObject("common/icon.png", type=1))
        self.setWindowFlag(Qt.WindowStaysOnTopHint)

        self.tab = QTabWidget()
        self.below = QWidget()
        self.ok_bt = QPushButton("OK")
        self.cancel_bt = QPushButton("Cancel")
        self.apply_bt = QPushButton("Apply")
        self.general = VideoGeneral()

        self.default_properties = self.general.default_properties

        self.tab.addTab(self.general, "General")
        self.tab.setTabBarAutoHide(True)

        self.setButtons()
        self.setUI()

        # 生成主界面

    def setUI(self):
        self.setWindowTitle("Video property")
        self.resize(600, 800)
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tab, 6)
        main_layout.addWidget(self.below, 1)
        main_layout.setSpacing(0)
        self.setLayout(main_layout)

    def setButtons(self):
        below_layout = QHBoxLayout()
        below_layout.addStretch(10)
        below_layout.addWidget(self.ok_bt, 1)
        below_layout.addWidget(self.cancel_bt, 1)
        below_layout.addWidget(self.apply_bt, 1)
        below_layout.setContentsMargins(0, 0, 0, 0)
        self.below.setLayout(below_layout)

    def setAttributes(self, attributes):
        self.general.setAttributes(attributes)

    def updateInfo(self):
        self.general.updateInfo()

    def setPosition(self, x, y):
        self.general.setPosition(x, y)

    def setProperties(self, properties: dict):
        self.default_properties.update(properties)
        self.loadSetting()

    def loadSetting(self):
        self.general.loadSetting()
