from app.deviceSystem.device import Device
from app.info import Info


class Screen(Device):
    """
    :param device_type: 串、并、网口、
    :param device_id: 设备标识符
    """
    index = 0

    def __init__(self, device_type: str, device_id: str = None, parent=None):
        super(Screen, self).__init__(device_type, device_id, parent)
        # 地址
        self.device_index = str(Screen.index)
        # self.device_index = "auto"
        Screen.index += 1

        # screen 专属
        self.back_color = "255,255,255"
        self.sample = "0"
        self.resolution = "auto"
        self.refresh_rate = "auto"

        self.physic_size = "NaN"
        self.stim_distance = "NaN"
        self.gamma_filename = ""

    def getIndex(self) -> str:
        return self.device_index

    def getColor(self) -> str:
        if self.device_type == Info.DEV_SCREEN:
            return self.back_color
        return ""

    def getSample(self) -> str:
        return self.sample

    def getResolution(self) -> str:
        return self.resolution

    def getRefreshRate(self) -> str:
        return self.refresh_rate

    def getGammaFilename(self) -> str:
        return self.gamma_filename

    def setIndex(self, port: str):
        self.device_index = port.split(".")[-1]

    def setColor(self, color: str):
        self.back_color = color

    def setSample(self, sample: str):
        self.sample = sample

    def setResolution(self, resolution):
        self.resolution = resolution

    def setRefreshRate(self, refresh_rate):
        self.refresh_rate = refresh_rate

    def setPhysicSize(self, physic_size):
        self.physic_size = physic_size

    def setStimDistance(self, stim_distance):
        self.stim_distance = stim_distance

    def setGammaFilename(self, gamma_filename):
        self.gamma_filename = gamma_filename

    def setProperties(self, properties: dict):
        if isinstance(properties, dict):
            self.default_properties = properties
            self.loadSetting()

    def loadSetting(self):
        self.setName(self.default_properties["Device Name"])
        self.setIndex(self.default_properties["Device Index"])
        self.setColor(self.default_properties.get("Back Color", "255,255,255"))
        self.setSample(self.default_properties.get("Multi Sample", "0"))
        self.setResolution(self.default_properties.get("Resolution", "auto"))
        self.setRefreshRate(self.default_properties.get("Refresh Rate", "auto"))
        self.setPhysicSize(self.default_properties.get("Physic Size", ""))
        self.setStimDistance(self.default_properties.get("Viewing Distance", "auto"))
        self.setGammaFilename(self.default_properties.get("Gamma Filename", ""))

    def getInfo(self) -> dict:
        self.default_properties["Device Name"] = self.text()
        self.default_properties["Device Index"] = self.device_index
        self.default_properties["Back Color"] = self.back_color
        self.default_properties["Multi Sample"] = self.sample
        self.default_properties["Resolution"] = self.resolution
        self.default_properties["Refresh Rate"] = self.refresh_rate
        self.default_properties["Physic Size"] = self.physic_size
        self.default_properties["Viewing Distance"] = self.stim_distance
        self.default_properties["Gamma Filename"] = self.gamma_filename

        return self.default_properties
