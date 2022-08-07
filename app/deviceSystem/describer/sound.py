from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QLineEdit, QFormLayout, QVBoxLayout

from app.deviceSystem.describer.basis import Shower


class Sound(Shower):
    def __init__(self, parent=None):
        super(Sound, self).__init__(parent=parent)
        self.device_index = QLineEdit()
        self.sampling_rate = QLineEdit("auto")

        self.device_index.setValidator(QRegExpValidator(QRegExp(r"\d+|auto")))
        self.sampling_rate.setValidator(QRegExpValidator(QRegExp(r"\d+|auto")))

        self.index_tip.setHtml("About Device Index:"
                               "<br><br>Either \"auto\" (default to the optimized sound device index) or an integer that represents the sound device, as returned by PsychPortAudio('GetDevices') in MATLAB."
                               )
        self.setUI()

    def setUI(self):
        layout = QFormLayout()
        layout.setLabelAlignment(Qt.AlignLeft)
        layout.addRow("Device Type:", self.device_type)
        layout.addRow("Device Name:", self.device_name)
        layout.addRow("Device Index:", self.device_index)
        layout.addRow("Sampling Rate (Hz):", self.sampling_rate)

        vLayout = QVBoxLayout()
        vLayout.addLayout(layout)
        vLayout.addWidget(self.port_tip)
        vLayout.addWidget(self.index_tip)

        self.setLayout(vLayout)

    def describe(self, info: dict):
        super().describe(info)
        self.device_index.setText(info.get("Device Index", "0"))
        self.sampling_rate.setText(info.get("Sampling Rate", "auto"))

    def getInfo(self):
        properties: dict = {
            "Device Type": self.device_type.text(),
            "Device Name": self.device_name.text(),
            "Device Index": self.device_index.text(),
            "Sampling Rate": self.sampling_rate.text(),
        }
        return properties
