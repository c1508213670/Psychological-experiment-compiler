from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QTabWidget, QHBoxLayout, QPushButton, QVBoxLayout

from app.func import Func
from .videoGeneral import VideoTab1
from app.center.events.__tools__ import DurationPage
from app.center.events.__tools__ import FramePage


class VideoProperty(QWidget):
    def __init__(self, parent=None):
        super(VideoProperty, self).__init__(parent)
        self.setWindowIcon(Func.getImageObject("common/icon.png", type=1))
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.tab = QTabWidget()

        self.ok_bt = QPushButton("OK")
        self.cancel_bt = QPushButton("Cancel")
        self.apply_bt = QPushButton("Apply")
        self.general = VideoTab1()
        self.frame = FramePage()
        self.duration = DurationPage()

        self.default_properties = {
            "General": self.general.default_properties,
            "Frame": self.frame.default_properties,
            "Duration": self.duration.default_properties
        }

        self.tab.addTab(self.general, "General")
        self.tab.addTab(self.frame, "Frame")
        self.tab.addTab(self.duration, "Duration")
        self.setUI()

    def setUI(self):
        self.setWindowTitle("Video property")
        self.resize(600, 800)
        below_layout = QHBoxLayout()
        below_layout.addStretch(10)
        below_layout.addWidget(self.ok_bt, 1)
        below_layout.addWidget(self.cancel_bt, 1)
        below_layout.addWidget(self.apply_bt, 1)
        below_layout.setContentsMargins(0, 0, 0, 0)
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tab, 6)
        main_layout.addLayout(below_layout, 1)
        main_layout.setSpacing(0)

        self.setLayout(main_layout)

    def refresh(self):
        self.general.refresh()
        self.duration.refresh()

    def setAttributes(self, attributes):
        self.general.setAttributes(attributes)
        self.frame.setAttributes(attributes)
        self.duration.setAttributes(attributes)

    def updateInfo(self):
        self.general.updateInfo()
        self.frame.updateInfo()
        self.duration.updateInfo()

    def getProperties(self):
        properties = {
            **self.general.getProperties(),
            **self.frame.getProperties(),
            **self.duration.getProperties()
        }
        return properties

    def setProperties(self, properties: dict):
        self.general.setProperties(properties.get("General"))
        self.frame.setProperties(properties.get("Frame"))
        self.duration.setProperties(properties.get("Duration"))

    def loadSetting(self):
        self.general.loadSetting()
        self.frame.loadSetting()
        self.duration.loadSetting()

    def getScreenId(self):
        return self.general.using_screen_id
