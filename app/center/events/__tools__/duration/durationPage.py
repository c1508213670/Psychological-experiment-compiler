from PyQt5.QtWidgets import QWidget, QVBoxLayout, QCompleter, QFormLayout

from app.center.events.__tools__.duration.RM import inputDevicesDur, outputDevicesDur
from lib import VarComboBox


class DurationPage(QWidget):
    def __init__(self, parent=None):
        super(DurationPage, self).__init__(parent=parent)
        self.duration = VarComboBox()
        self.duration.addItems(("1000", "2000", "3000", "4000", "100~500", "(Infinite)"))
        self.duration.setEditable(True)
        self.duration.setReg(r"\(Infinite\)|\d+|\d+~\d+")
        self.up = outputDevicesDur()
        self.down = inputDevicesDur()
        self.up.deviceChanged.connect(self.down.updateExternalInfo)
        self.default_properties = {
            "Duration": "1000",
            "Output Devices": self.up.default_properties,
            "Input Devices": self.down.default_properties
        }
        self.setUI()

    def setUI(self):
        layout0 = QFormLayout()
        layout0.addRow("Duration (ms):", self.duration)

        layout = QVBoxLayout()
        layout.addLayout(layout0, 0)
        layout.addWidget(self.down, 1)
        layout.addWidget(self.up, 1)
        self.setLayout(layout)

    def refresh(self):
        self.up.refresh()
        self.down.refresh()

    def setAttributes(self, attributes: list):
        self.duration.setCompleter(QCompleter(attributes))
        self.up.setAttributes(attributes)
        self.down.setAttributes(attributes)

    def updateInfo(self):
        """
        update info.
        :return:
        """
        self.default_properties["Duration"] = self.duration.currentText()
        self.up.updateInfo()
        self.down.updateInfo()
        return self.default_properties

    def getProperties(self):
        return {"Duration": self.duration.currentText()}

    # 设置参数
    def setProperties(self, properties: dict):
        self.default_properties["Duration"] = properties["Duration"]
        self.up.setProperties(properties["Output Devices"])
        self.down.setProperties(properties["Input Devices"])
        self.loadSetting()

    # 加载参数设置
    def loadSetting(self):
        self.duration.setCurrentText(self.default_properties["Duration"])
        self.up.loadSetting()
        self.down.loadSetting()
