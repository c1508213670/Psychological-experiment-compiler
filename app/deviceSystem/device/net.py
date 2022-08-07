from app.deviceSystem.device import Device


class Net(Device):
    """
    :param device_type: 网口、
    :param device_id: 设备标识符
    """

    def __init__(self, device_type: str, device_id: str = None, parent=None):
        super(Net, self).__init__(device_type, device_id, parent)
        # 地址
        self.ip_address = "127.0.0.1"
        # net
        self.ip_port: str = "25576"

        self.is_client = 1

    def getPort(self) -> str:
        return self.ip_address

    def setIPAddress(self, port: str):
        self.ip_address = port

    def setClient(self, client: int):
        self.is_client = client

    def setIpPort(self, ip_port: str):
        self.ip_port = ip_port

    def setProperties(self, properties: dict):
        if isinstance(properties, dict):
            self.default_properties = properties
            self.loadSetting()

    def loadSetting(self):
        self.setName(self.default_properties["Device Name"])
        self.setIPAddress(self.default_properties["IP Address"])
        self.setIpPort(self.default_properties.get("IP Port", "25576"))
        self.setClient(self.default_properties.get("Is Client", 1))

    def getInfo(self) -> dict:
        self.default_properties["Device Name"] = self.text()
        self.default_properties["IP Address"] = self.ip_address
        self.default_properties["IP Port"] = self.ip_port
        self.default_properties["Is Client"] = self.is_client

        return self.default_properties
