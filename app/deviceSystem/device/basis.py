from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QListWidgetItem

from app.func import Func


class Device(QListWidgetItem):
    def __init__(self, device_type: str, device_id: str = None, parent=None):
        super(Device, self).__init__(device_type, parent)
        # 设备类型
        self.device_type = device_type
        self.device_id = device_id
        # 设置图标
        self.setIcon(QIcon(Func.getImage("devices/{}_device.png".format(self.device_type))))
        self.setText(self.device_type.capitalize())

        self.default_properties = {
            "Device Type": self.device_type,
            "Device Name": self.text(),
        }

    def getType(self) -> str:
        return self.device_type

    def getDeviceId(self) -> str:
        return self.device_id

    def getName(self) -> str:
        return self.text()

    def setName(self, name: str):
        self.setText(name)

    def setProperties(self, properties: dict):
        if properties:
            self.default_properties.update(properties)

    def loadSetting(self):
        pass
