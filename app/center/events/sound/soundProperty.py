from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QTabWidget, QPushButton, QVBoxLayout, QHBoxLayout)

from app.func import Func
from .soundGeneral import SoundTab1
from app.center.events.__tools__ import DurationPage


class SoundProperty(QWidget):
    def __init__(self, parent=None):
        super(SoundProperty, self).__init__(parent)
        self.setWindowIcon(Func.getImageObject("common/icon.png", type=1))
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.tab = QTabWidget()

        self.general = SoundTab1()
        self.duration = DurationPage()
        self.tab.addTab(self.general, "General")
        self.tab.addTab(self.duration, "Duration")

        self.default_properties = {
            "General": self.general.default_properties,
            "Duration": self.duration.default_properties
        }
        # bottom
        self.ok_bt = QPushButton("OK")
        self.cancel_bt = QPushButton("Cancel")
        self.apply_bt = QPushButton("Apply")
        self.setUI()

    # 生成主界面
    def setUI(self):
        self.setWindowTitle("Sound property")
        self.resize(600, 800)
        below_layout = QHBoxLayout()
        below_layout.addStretch(10)
        below_layout.addWidget(self.ok_bt, 1)
        below_layout.addWidget(self.cancel_bt, 1)
        below_layout.addWidget(self.apply_bt, 1)
        below_layout.setContentsMargins(0, 0, 0, 0)
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tab, 6)
        # main_layout.addStretch(2)
        main_layout.addLayout(below_layout, 1)
        main_layout.setSpacing(0)
        self.setLayout(main_layout)

    def refresh(self):
        self.general.refresh()
        self.duration.refresh()

    def getProperties(self):
        properties = {
            **self.general.getProperties(),
            **self.duration.getProperties()
        }
        return properties

    def setAttributes(self, attributes):
        self.general.setAttributes(attributes)
        self.duration.setAttributes(attributes)

    def setProperties(self, properties: dict):
        self.general.setProperties(properties.get("General"))
        self.duration.setProperties(properties.get("Duration"))

    def updateInfo(self):
        self.general.updateInfo()
        self.duration.updateInfo()

    def loadSetting(self):
        self.general.loadSetting()
        self.duration.loadSetting()

    def getScreenId(self):
        return self.general.using_screen_id
