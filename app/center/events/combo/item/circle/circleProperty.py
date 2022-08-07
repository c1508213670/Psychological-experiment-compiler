from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QTabWidget, QHBoxLayout

from app.func import Func
from .circleGeneral import CircleGeneral


class CircleProperty(QWidget):
    def __init__(self, parent=None):
        super(CircleProperty, self).__init__(parent=parent)
        self.setWindowIcon(Func.getImageObject("common/icon.png", type=1))
        self.setWindowFlag(Qt.WindowStaysOnTopHint)

        self.tab = QTabWidget()
        self.below = QWidget()

        self.general = CircleGeneral()
        self.default_properties = self.general.default_properties
        self.tab.addTab(self.general, "General")
        self.tab.setTabBarAutoHide(True)

        self.ok_bt = QPushButton("OK")
        self.cancel_bt = QPushButton("Cancel")
        self.apply_bt = QPushButton("Apply")
        self.setButtons()

        self.setUI()

    # 生成主界面
    def setUI(self):
        self.setWindowTitle("Property")
        self.resize(600, 800)
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tab, 6)
        main_layout.addWidget(self.below, 1)
        main_layout.setSpacing(0)
        self.setLayout(main_layout)

    # 生成下方三个按钮
    def setButtons(self):
        below_layout = QHBoxLayout()
        below_layout.addStretch(10)
        below_layout.addWidget(self.ok_bt, 1)
        below_layout.addWidget(self.cancel_bt, 1)
        below_layout.addWidget(self.apply_bt, 1)
        below_layout.setContentsMargins(0, 0, 0, 0)
        self.below.setLayout(below_layout)

    def updateInfo(self):
        self.general.updateInfo()

    def setAttributes(self, attributes):
        self.general.setAttributes(attributes)

    def setPosition(self, x, y):
        self.general.setPosition(x, y)

    def setWh(self, w, h):
        self.general.setWh(w, h)

    def setItemColor(self, color):
        self.general.setItemColor(color)

    def setLineColor(self, color):
        self.general.setLineColor(color)

    def setLineWidth(self, width):
        self.general.setLineWidth(width)

    def setProperties(self, properties: dict):
        self.default_properties.update(properties)
        self.loadSetting()

    def loadSetting(self):
        self.general.loadSetting()
