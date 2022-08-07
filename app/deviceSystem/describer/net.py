from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLineEdit, QFormLayout, QCheckBox

from app.deviceSystem.describer.basis import Shower


class Net(Shower):
    def __init__(self, parent=None):
        super(Net, self).__init__(parent=parent)
        self.device_ip_address = QLineEdit()
        self.device_ip_address.textEdited.connect(self.showAddressTip)
        self.device_ip_port = QLineEdit()
        self.is_client = QCheckBox()
        self.is_client.stateChanged.connect(self.changeClient)
        self.setUI()

    def setUI(self):
        layout = QFormLayout()
        layout.setLabelAlignment(Qt.AlignLeft)
        layout.addRow("Device Type:", self.device_type)
        layout.addRow("Device Name:", self.device_name)
        layout.addRow("IP Address:", self.device_ip_address)
        layout.addRow("IP Port:", self.device_ip_port)
        layout.addRow("Is Client:", self.is_client)
        layout.addRow("", self.port_tip)
        self.setLayout(layout)

    def describe(self, info: dict):
        super().describe(info)
        self.device_ip_address.setText(info.get("IP Address", "127.0.0.1"))
        self.device_ip_port.setText(info.get("IP Port", "25576"))
        self.is_client.setChecked(info.get("Is Client", "Yes") == "1")

    def changeClient(self, state):
        pass

    def getInfo(self):
        properties: dict = {
            "Device Type": self.device_type.text(),
            "Device Name": self.device_name.text(),
            "IP Address": self.device_ip_address.text(),
            "IP Port": self.device_ip_port.text(),
            "Is Client": self.is_client.checkState(),
        }
        return properties
