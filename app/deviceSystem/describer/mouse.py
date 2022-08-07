from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QLineEdit, QFormLayout, QCheckBox, QVBoxLayout

from app.deviceSystem.describer.basis import Shower


class Mouse(Shower):
    def __init__(self, parent=None):
        super(Mouse, self).__init__(parent=parent)
        self.mouse_index = QLineEdit()
        self.mouse_index.setValidator(QRegExpValidator(QRegExp(r"-1|\d+|auto")))
        self.setUI()

    def setUI(self):
        layout = QFormLayout()
        layout.setLabelAlignment(Qt.AlignLeft)
        layout.addRow("Device Type:", self.device_type)
        layout.addRow("Device Name:", self.device_name)
        layout.addRow("Device Index:", self.mouse_index)
        layout.addRow("Is Kb Queue:", self.is_kb_queue)

        v_layout = QVBoxLayout()
        v_layout.addLayout(layout)
        v_layout.addWidget(self.port_tip)
        v_layout.addWidget(self.index_tip)

        self.setLayout(v_layout)

    def describe(self, info: dict):
        super().describe(info)
        self.mouse_index.setText(info.get("Device Index", "auto"))
        kb_queue = info.get("Is KB Queue", 0)
        if kb_queue == 2:
            if Mouse.kb_id == self.device_id or Mouse.kb_id == "":
                Mouse.kb_id = self.device_id
                self.is_kb_queue.setCheckState(kb_queue)
            else:
                self.is_kb_queue.setCheckState(0)
        else:
            self.is_kb_queue.setCheckState(0)

        order_num = int(info.get("Device Id").split(".")[1]) + 1

        if order_num == 1:
            gpOrderStr = 'first'
        elif order_num == 2:
            gpOrderStr = 'second'
        else:
            gpOrderStr = f"{order_num}th"

        self.index_tip.setHtml("About Device Index:"
                               # f"<br><br>Either “auto” (default to the {gpOrderStr} value returned by GetMouseIndices in MATLAB) or an integer that represents the mouse."
                               f'<br><br>Either "auto" (default to the {gpOrderStr} value returned by GetMouseIndices in MATLAB) or an integer that represents the mouse.'
                               # f"<br><br><b>auto:</b> will use the {gpOrderStr} value in mouse indices for this mouse (returned by GetMouseIndices in MATLAB)"
                               )

    def getInfo(self):
        properties: dict = {
            "Device Type": self.device_type.text(),
            "Device Name": self.device_name.text(),
            "Device Index": self.mouse_index.text(),
            "Is KB Queue": self.is_kb_queue.checkState(),
        }
        return properties
