from app.deviceSystem.device import Device
from app.info import Info


class Quest(Device):
    def __init__(self, device_type: str = Info.DEV_QUEST, device_id: str = None, parent=None):
        super(Quest, self).__init__(device_type, device_id, parent)
        self.device_type = device_type

        self.quest_id: str = device_id
        self.guess_threshold = "0.5"
        self.std_dev = "0.25"
        self.desired_proportion = "0.75"
        self.steepness = "3.5"
        self.proportion = "0.01"
        self.chance_level = "0.05"
        self.method = "quantile"
        self.minimum = "0"
        self.maximum = "1"
        self.is_log10_transform = "Yes"
        self.grain = "0.01"
        self.range = "5"

    def getThreshold(self) -> str:
        return self.guess_threshold

    def setThreshold(self, threshold: str):
        self.guess_threshold = threshold

    def setSD(self, sd: str):
        self.std_dev = sd

    def setDesired(self, desired: str):
        self.desired_proportion = desired

    def setSteep(self, steepness: str):
        self.steepness = steepness

    def setProportion(self, proportion: str):
        self.proportion = proportion

    def setChanceLevel(self, chance_level: str):
        self.chance_level = chance_level

    def setMethod(self, method: str):
        self.method = method

    def setMaximum(self, maximum: str):
        self.maximum = maximum

    def setMinimum(self, minimum: str):
        self.minimum = minimum

    def setIsTransform(self, is_transform: str):
        self.is_log10_transform = is_transform

    def setGrain(self, grain: str):
        self.grain = grain

    def setRange(self, range: str):
        self.range = range

    def setProperties(self, properties: dict):
        if isinstance(properties, dict):
            self.default_properties = properties.copy()
            self.loadSetting()

    def loadSetting(self):
        self.setName(self.default_properties["Device Name"])
        self.guess_threshold = self.default_properties["Guess Threshold"]
        self.std_dev = self.default_properties["Std. Dev."]
        self.desired_proportion = self.default_properties["Desired Proportion"]
        self.steepness = self.default_properties["Steepness"]
        self.proportion = self.default_properties["Proportion"]
        self.chance_level = self.default_properties["Chance Level"]
        self.method = self.default_properties["Method"]
        self.minimum = self.default_properties["Minimum Test Value"]
        self.maximum = self.default_properties["Maximum Test Value"]
        self.is_log10_transform = self.default_properties["Is Log10 Transform"]
        self.grain = self.default_properties["Grain"]
        self.range = self.default_properties["Range"]

    def getInfo(self):
        self.default_properties.clear()
        self.default_properties["Device Type"] = self.device_type
        self.default_properties["Device Name"] = self.text()
        self.default_properties["Guess Threshold"] = self.guess_threshold
        self.default_properties["Std. Dev."] = self.std_dev
        self.default_properties["Desired Proportion"] = self.desired_proportion
        self.default_properties["Steepness"] = self.steepness
        self.default_properties["Proportion"] = self.proportion
        self.default_properties["Chance Level"] = self.chance_level
        self.default_properties["Method"] = self.method
        self.default_properties["Minimum Test Value"] = self.minimum
        self.default_properties["Maximum Test Value"] = self.maximum
        self.default_properties["Is Log10 Transform"] = self.is_log10_transform
        self.default_properties["Grain"] = self.grain
        self.default_properties["Range"] = self.range
        return self.default_properties
