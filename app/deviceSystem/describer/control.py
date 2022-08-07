from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QStackedWidget, QGridLayout

from app.deviceSystem.describer import *
from app.deviceSystem.describer.basis import Shower
from app.info import Info


class DefaultShow(QWidget):
    def __init__(self, parent=None):
        super(DefaultShow, self).__init__(parent)
        self.label = QLabel("Device information will appear here.")
        self.label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        layout = QGridLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)


class Describer(QStackedWidget):
    def __init__(self, parent=None):
        super(Describer, self).__init__(parent)
        self.face = DefaultShow()
        self.addWidget(self.face)
        self.id_widget: dict = {
            # device_id: device_describer
        }
        self.default_properties = {

        }

    def describe(self, device_id: str, device_info: dict):
        if device_info == {}:
            self.removeWidget(self.id_widget.get(device_id))
            self.id_widget.pop(device_id)
            Shower.id_2_name.pop(device_id)
        else:
            if device_id in self.id_widget.keys():
                self.setCurrentWidget(self.id_widget.get(device_id))
            else:
                if device_id.startswith(Info.DEV_SCREEN):
                    d = Screen()
                elif device_id.startswith(Info.DEV_SOUND):
                    d = Sound()
                elif device_id.startswith(Info.DEV_NETWORK_PORT):
                    d = Net()
                elif device_id.startswith(Info.DEV_PARALLEL_PORT):
                    d = Parallel()
                elif device_id.startswith(Info.DEV_SERIAL_PORT):
                    d = Serial()
                elif device_id.startswith(Info.DEV_QUEST):
                    d = Quest()
                elif device_id.startswith(Info.DEV_TRACKER):
                    d = Tracker()
                elif device_id.startswith(Info.DEV_EYE_ACTION):
                    d = Action()
                elif device_id.startswith(Info.DEV_KEYBOARD):
                    d = Keyboard()
                elif device_id.startswith(Info.DEV_MOUSE):
                    d = Mouse()
                elif device_id.startswith(Info.DEV_RESPONSE_BOX):
                    d = ResponseBox()
                elif device_id.startswith(Info.DEV_GAMEPAD):
                    d = GamePad()
                device_info["Device Id"] = device_id
                d.describe(device_info)
                self.addWidget(d)
                self.setCurrentWidget(d)
                self.id_widget[device_id] = d

    def cancel(self, device_id: str):
        self.removeWidget(self.id_widget.get(device_id))

    def changeName(self, old_name: str, new_name: str):
        if self.currentIndex():
            self.currentWidget().changeName(new_name)

    def updateInfo(self):
        self.default_properties.clear()
        for k, v in self.id_widget.items():
            self.default_properties[k] = v.getInfo()

    def getInfo(self):
        self.updateInfo()
        return self.default_properties

    def updateSimpleInfo(self):
        for k, v in self.id_widget.items():
            if k.startswith(Info.DEV_TRACKER):
                v.updateExternalDeviceInformation()
            elif k.startswith(Info.DEV_EYE_ACTION):
                v.updateExternalDeviceInformation()
