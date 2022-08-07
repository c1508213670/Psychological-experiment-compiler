from app.deviceSystem.device.basis import Device


class ResponseBox(Device):
    index = 0

    def __init__(self, device_type: str, device_id: str = None, parent=None):
        super(ResponseBox, self).__init__(device_type, device_id, parent)

        # self.device_index = str(ResponseBox.index)
        self.device_index = "auto"
        ResponseBox.index += 1

    def getInfo(self):
        self.default_properties.clear()
        self.default_properties["Device Name"] = self.text()
        self.default_properties["Device Type"] = self.device_type
        self.default_properties["Device Index"] = self.device_index
        return self.default_properties

    def setProperties(self, properties: dict):
        if properties:
            self.default_properties = properties.copy()
            self.loadSetting()

    def loadSetting(self):
        self.device_type = self.default_properties.get("Device Type")
        self.setName(self.default_properties.get("Device Name"))
        self.device_index = self.default_properties.get("Device Index")
