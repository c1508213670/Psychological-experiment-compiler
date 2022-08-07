from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLineEdit, QFormLayout

from app.deviceSystem.describer.basis import Shower


class Parallel(Shower):
    def __init__(self, parent=None):
        super(Parallel, self).__init__(parent=parent)
        self.device_port = QLineEdit()
        self.device_port.setToolTip("For UBW32 device, input port address here with the format of 'UBW:address'")
        self.device_port.textEdited.connect(self.showAddressTip)
        self.setUI()

    def setUI(self):
        layout = QFormLayout()
        layout.setLabelAlignment(Qt.AlignLeft)
        layout.addRow("Device Type:", self.device_type)
        layout.addRow("Device Name:", self.device_name)
        layout.addRow("Device Port:", self.device_port)
        layout.addRow("", self.port_tip)
        self.setLayout(layout)

    def describe(self, info: dict):
        super().describe(info)
        self.device_port.setText(info.get("Device Port", "D010"))

    def getInfo(self):
        properties: dict = {
            "Device Type": self.device_type.text(),
            "Device Name": self.device_name.text(),
            "Device Port": self.device_port.text(),
        }
        return properties
