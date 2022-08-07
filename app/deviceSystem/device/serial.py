from app.deviceSystem.device import Device


class Serial(Device):
    """
    :param device_type: 串、并、网口、
    :param device_id: 设备标识符
    """

    def __init__(self, device_type: str, device_id: str = None, parent=None):
        super(Serial, self).__init__(device_type, device_id, parent)
        # 地址
        self.port = "COM1"
        # serial
        self.baud_rate: str = "9600"
        self.data_bits: str = "8"

    def getPort(self) -> str:
        return self.port

    def setPort(self, port: str):
        self.port = f"COM{port.split('.')[-1]}"

    def setBaud(self, baud: str):
        self.baud_rate = baud

    def setBits(self, bits: str):
        self.data_bits = bits

    def setProperties(self, properties: dict):
        if isinstance(properties, dict):
            self.default_properties = properties
            self.loadSetting()

    def loadSetting(self):
        self.setName(self.default_properties["Device Name"])
        self.setPort(self.default_properties["Device Port"])
        self.setBaud(self.default_properties.get("Baud Rate", "9600"))
        self.setBits(self.default_properties.get("Data Bits", "8"))

    def getInfo(self) -> dict:
        self.default_properties["Device Name"] = self.text()
        self.default_properties["Device Port"] = self.port
        self.default_properties["Baud Rate"] = self.baud_rate
        self.default_properties["Data Bits"] = self.data_bits

        return self.default_properties
