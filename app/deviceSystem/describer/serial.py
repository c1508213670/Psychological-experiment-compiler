from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLineEdit, QFormLayout

from app.deviceSystem.describer.basis import Shower


class Serial(Shower):
    def __init__(self, parent=None):
        super(Serial, self).__init__(parent=parent)
        self.device_port = QLineEdit()
        self.device_port.textEdited.connect(self.showAddressTip)
        self.baud_rate = QLineEdit()
        self.data_bits = QLineEdit()
        self.setUI()

    def setUI(self):
        layout = QFormLayout()
        layout.setLabelAlignment(Qt.AlignLeft)
        layout.addRow("Device Type:", self.device_type)
        layout.addRow("Device Name:", self.device_name)
        layout.addRow("Device Port:", self.device_port)
        layout.addRow("Baud Rate:", self.baud_rate)
        layout.addRow("Data Bits:", self.data_bits)
        layout.addRow("", self.port_tip)
        self.setLayout(layout)

    def describe(self, info: dict):
        super().describe(info)
        self.device_port.setText(info.get("Device Port", "COM0"))
        self.baud_rate.setText(info.get("Baud Rate", "9600"))
        self.data_bits.setText(info.get("Data Bits", "8"))

    def getInfo(self):
        properties: dict = {
            "Device Type": self.device_type.text(),
            "Device Name": self.device_name.text(),
            "Device Port": self.device_port.text(),
            "Baud Rate": self.baud_rate.text(),
            "Data Bits": self.data_bits.text(),
        }
        return properties
