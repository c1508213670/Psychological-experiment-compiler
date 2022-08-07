from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLineEdit, QFormLayout, QVBoxLayout

from app.deviceSystem.describer.basis import Shower


class ResponseBox(Shower):
    def __init__(self, parent=None):
        super(ResponseBox, self).__init__(parent=parent)
        self.device_index = QLineEdit()
        self.device_index.textEdited.connect(self.showAddressTip)
        self.device_index.setToolTip("The serial port address corresponding to the Cedrus response pad")
        self.index_tip.setHtml("About Device Port:"
                               "<br><br>Currently, only response pads from Cedrus are supported. "
                               "Input \"auto\" for the default serial port name."
                               "<br><br><b>Windows:</b> 'COM2', etc."
                               "<br><br><b>Mac OS: </b> '/dev/cu.usbserial-FTDI125ZX9', etc."
                               "<br><br><b>Linux: </b> '/dev/ttyS0', etc."
                               )
        self.setUI()

    def setUI(self):
        layout = QFormLayout()
        layout.setLabelAlignment(Qt.AlignLeft)
        layout.addRow("Device Type:", self.device_type)
        layout.addRow("Device Name:", self.device_name)
        layout.addRow("Device Port:", self.device_index)

        vLayout = QVBoxLayout()
        vLayout.addLayout(layout)
        vLayout.addWidget(self.port_tip)
        vLayout.addWidget(self.index_tip)

        self.setLayout(vLayout)

    def describe(self, info: dict):
        self.device_index.setText(info.get("Device Index", "0"))
        super().describe(info)

    def getInfo(self):
        properties: dict = {
            "Device Type": self.device_type.text(),
            "Device Name": self.device_name.text(),
            "Device Index": self.device_index.text(),
        }
        return properties
