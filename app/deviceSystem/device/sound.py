from app.deviceSystem.device import Device


class Sound(Device):
    """
    :param device_type: 串、并、网口、
    :param device_id: 设备标识符
    """
    index = 0

    def __init__(self, device_type: str, device_id: str = None, parent=None):
        super(Sound, self).__init__(device_type, device_id, parent)
        # 地址
        # self.device_index = str(Sound.index)
        self.device_index = "auto"
        Sound.index += 1
        # sound
        self.sampling_rate: str = "auto"

    def getPort(self) -> str:
        return self.device_index

    def setPort(self, port: str):
        self.device_index = port.split(".")[-1]

    def setSamplingRate(self, sampling_rate: str):
        self.sampling_rate = sampling_rate

    def setProperties(self, properties: dict):
        if isinstance(properties, dict):
            self.default_properties = properties
            self.loadSetting()

    def loadSetting(self):
        self.setName(self.default_properties["Device Name"])
        self.setPort(self.default_properties["Device Index"])
        self.setSamplingRate(self.default_properties.get("Sampling Rate", "auto"))

    def getInfo(self) -> dict:
        self.default_properties["Device Name"] = self.text()
        self.default_properties["Device Index"] = self.device_index
        self.default_properties["Sampling Rate"] = self.sampling_rate

        return self.default_properties
