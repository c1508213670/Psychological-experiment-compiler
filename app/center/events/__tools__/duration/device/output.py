from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QListWidgetItem

from app.func import Func


# 重写上方输出设备list widget的item
class OutputDevice(QListWidgetItem):
    def __init__(self, device_id: str, device_name: str, parent=None):
        super(OutputDevice, self).__init__(device_name, parent)

        self.device_name = device_name
        self.device_id = device_id
        self.device_type = device_id.split(".")[0]
        self.setIcon(QIcon(Func.getImage(f"devices/{self.device_type}_device.png")))

        self.default_properties = {
            "Device Id": self.device_id,
            "Device Name": self.device_name,
            "Device Type": self.device_type,
            "Value Or Msg": "",
            "Pulse Duration": ""
        }

        self.value_or_msg = ""
        self.pulse_duration = "End of Duration"

    def getDeviceId(self):
        return self.device_id

    def getDeviceName(self):
        return self.device_name

    def setDeviceName(self, new_name: str):
        self.device_name = new_name
        self.setText(new_name)

    def getInfo(self) -> dict:
        self.default_properties["Device Id"] = self.device_id
        self.default_properties["Device Name"] = self.device_name
        self.default_properties["Device Type"] = self.device_type
        self.default_properties["Value Or Msg"] = self.value_or_msg
        self.default_properties["Pulse Duration"] = self.pulse_duration
        return self.default_properties

    def setProperties(self, device_info: dict):
        self.default_properties.update(device_info)
        self.loadSetting()

    def loadSetting(self):
        self.device_id = self.default_properties.get("Device Id", self.device_id)
        self.device_name = self.default_properties.get("Device Name", self.device_name)
        self.device_type = self.default_properties.get("Device Type", self.device_type)
        self.value_or_msg = self.default_properties["Value Or Msg"]
        self.pulse_duration = self.default_properties["Pulse Duration"]
