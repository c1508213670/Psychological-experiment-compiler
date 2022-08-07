from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QComboBox, QFormLayout, QCompleter

from app.info import Info
from lib import VarLineEdit, VarComboBox


class TriggerInfo(QWidget):

    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)

        self.value = VarLineEdit()
        self.pulse_dur = VarComboBox()
        self.pulse_dur.setEditable(True)
        self.pulse_dur.setInsertPolicy(QComboBox.NoInsert)
        self.pulse_dur.addItems(["End of Duration", "10", "20", "30", "40", "50"])

        self.pulse_dur.setReg(r"\d+|End of Duration")

        self.device_name = ""
        self.device_type = ""

        self.setUI()

    def setUI(self):
        layout = QFormLayout()
        layout.addRow("Value or Msg:", self.value)
        layout.addRow("Pulse Dur:", self.pulse_dur)
        layout.setLabelAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.setVerticalSpacing(40)
        # 左、上、右、下
        layout.setContentsMargins(10, 20, 10, 0)
        self.setLayout(layout)

    def describe(self, info: dict):
        value = info.get("Value Or Msg")
        self.value.setText(value)

        self.device_name = info.get("Device Name")
        self.device_type = info.get("Device Type")

        pul_dur = info.get("Pulse Duration")
        self.pulse_dur.setEnabled(self.device_type == Info.DEV_PARALLEL_PORT)
        self.pulse_dur.setCurrentText(pul_dur)

    def setAttributes(self, attributes):
        self.value.setCompleter(QCompleter(attributes))
        self.pulse_dur.setCompleter(QCompleter(attributes))

    def getInfo(self):
        info = {
            "Device Name": self.device_name,
            "Device Type": self.device_type,
            "Value Or Msg": self.value.text(),
            "Pulse Duration": self.pulse_dur.currentText(),
        }
        return info
