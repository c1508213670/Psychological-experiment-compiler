from app.deviceSystem.device.basis import Device
from app.info import Info


class Action(Device):
    def __init__(self, device_type: str = Info.DEV_EYE_ACTION, device_id: str = "", parent=None):
        super(Action, self).__init__(device_type, device_id, parent)
        self.tracker_name = ""

    def getInfo(self):
        self.default_properties.clear()
        self.default_properties["Device Name"] = self.text()
        self.default_properties["Device Type"] = self.device_type
        self.default_properties["Tracker Name"] = self.tracker_name

        return self.default_properties

    def setProperties(self, properties: dict):
        if properties:
            self.default_properties = properties.copy()
            self.loadSetting()

    def loadSetting(self):
        self.device_type = self.default_properties.get("Device Type")
        self.setName(self.default_properties.get("Device Name"))
        self.tracker_name = self.default_properties.get("Tracker Name")
