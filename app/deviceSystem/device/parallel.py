from app.deviceSystem.device import Device


class Parallel(Device):
    """
    :param device_type: 串、并、网口、
    :param device_id: 设备标识符
    """

    def __init__(self, device_type: str, device_id: str = None, parent=None):
        super(Parallel, self).__init__(device_type, device_id, parent)
        # 地址
        self.port = "D010"

    def setPort(self, port: str):
        self.port = port

    def setProperties(self, properties: dict):
        if isinstance(properties, dict):
            self.default_properties = properties
            self.loadSetting()

    def loadSetting(self):
        self.setName(self.default_properties["Device Name"])
        self.setPort(self.default_properties["Device Port"])

    def getInfo(self) -> dict:
        self.default_properties["Device Name"] = self.text()
        self.default_properties["Device Port"] = self.port

        return self.default_properties
