import re

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QWidget, QLabel, QTextEdit, QFrame, QCheckBox

from app.defi import *


class Shower(QWidget):
    id_2_name = {

    }
    kb_id = ""

    def __init__(self, parent=None):
        super(Shower, self).__init__(parent)
        self.device_id = ""

        self.device_type = QLabel("Unselected")
        self.device_name = QLabel("Unselected")

        self.is_kb_queue = QCheckBox()
        self.is_kb_queue.stateChanged.connect(self.changeState)

        # you can show tips here!
        self.index_tip = QTextEdit("")
        self.index_tip.viewport().setAutoFillBackground(False)
        self.index_tip.setReadOnly(True)
        self.index_tip.setFrameShape(QFrame.NoFrame)
        self.index_tip.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.index_tip.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.port_tip = QLabel()

        self.timer = QTimer()
        self.timer.timeout.connect(self.port_tip.clear)

    def describe(self, info: dict):
        self.device_id = info.get("Device Id")
        device_type = info.get("Device Type", "ERROR")
        device_name = info.get("Device Name", "ERROR")
        self.device_type.setText(device_type)
        self.device_name.setText(device_name)

        Shower.id_2_name[self.device_id] = device_name

    def showAddressTip(self, port: str):
        """
        端口有效性提示
        :param port:
        :return:
        """
        flag, tip = self.checkPort(port)
        if flag is False:
            self.port_tip.setText(tip)
        else:
            self.port_tip.clear()

    def showTip(self, text):
        self.port_tip.setText(f"<font color='#ff0000' face='Sans'>{text} has been selected!<br> Only one device is allowed to be queued.</font>")
        self.timer.start(3000)

    def checkPort(self, port: str):
        flag: bool = True
        tip = ""
        device_type: str = self.device_type.text()
        if device_type == DEV_SCREEN:
            if not port.isdigit() or int(port) > 10:
                flag = False
                tip = "Screen index should be in [0 to 10]"

        elif device_type == DEV_NETWORK_PORT:
            port_list = port.split(".")
            if len(port_list) == 4:
                for i in port_list:
                    if i.isdigit():
                        if int(i) < 0 or int(i) > 255:
                            flag = False
                    else:
                        flag = False
            else:
                flag = False

            if flag is False:
                tip = "Invalid IP address"

        elif device_type == DEV_SERIAL_PORT:

            if port.startswith("COM") and port[3:].isdigit():
                # window
                pass
            elif port.startswith("/dev/cu.usbserial-"):
                # mac ox
                pass
            elif port.startswith("/dev/ttyS") and port[9:].isdigit():
                # linux
                pass
            elif port.startswith("auto"):
                pass
            else:
                flag = False
                tip = "Invalid serial address"

        elif device_type == DEV_RESPONSE_BOX:
            if port.startswith("COM") and port[3:].isdigit():
                # window
                pass
            elif port.startswith("/dev/cu.usbserial-"):
                # mac ox
                pass
            elif port.startswith("/dev/ttyS") and port[9:].isdigit():
                # linux
                pass
            elif port.startswith("auto"):
                pass
            else:
                flag = False
                tip = "Invalid Cedrus port address"

        elif device_type == DEV_PARALLEL_PORT:
            # Check whether a current_text string holds just a hexadecimal number
            if re.match(r'(\A[0-9a-fA-F]+\Z)|(^UBW:.+)', port) is None:
                flag = False
                tip = "<font color='#ff0000' face='Sans'>Should either be a hexadecimal or a string starts with 'UBW:' <br> (UBW denotes the UBW32 device) and followed by the port address</font>"

        elif device_type == DEV_SOUND:
            flag = port.isdigit()
            if flag is False:
                tip = "Should be a digit"

        return flag, tip

    def changeName(self, new_name: str):
        self.device_name.setText(new_name)
        Shower.id_2_name[self.device_id] = new_name

    def getDeviceId(self):
        return self.device_id

    def changeState(self, state):
        if Shower.kb_id == "" or Shower.kb_id == self.device_id or Shower.id_2_name.get(Shower.kb_id) is None:
            self.is_kb_queue.setCheckState(state)
            self.port_tip.clear()
            if state == 0:
                Shower.kb_id = ""
            else:
                Shower.kb_id = self.device_id
        else:
            self.showTip(f"{Shower.id_2_name.get(Shower.kb_id, '')}")
            self.is_kb_queue.setCheckState(0)
