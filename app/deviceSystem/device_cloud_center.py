from app.defi import *
from app.deviceSystem.RX import RX
from app.deviceSystem.describer import Tracker, Action


class DeviceCloudCenter:
    def __init__(self):
        self.input = RX(0)
        self.output = RX(1)
        self.quest = RX(2)
        self.tracker = RX(3)

        # now we just handle this one.
        self.output.deviceOK.connect(self.updateSimpleInfo)
        self.tracker.deviceOK.connect(self.updateSimpleInfo)

        # share the properties of all kinds of device
        self.input_properties = self.input.default_properties
        self.output_properties = self.output.default_properties
        self.quest_properties = self.quest.default_properties
        self.tracker_properties = self.tracker.default_properties

        self.simple_info = {
            # now we just have screen information
            # device_id: device_name
            "screen.0": "screen_0",
            # "sound.0": "sound_0",
            # "tracker.0”: ""tracker_0"
        }
        # now only tracker need such information.
        Tracker.simple_info = self.simple_info
        Action.simple_info = self.simple_info

    def updateSimpleInfo(self, device_types: tuple = (DEV_SCREEN, DEV_SOUND, DEV_TRACKER)):
        """
        now we just update screen information.
        :param device_types:
        :return:
        """
        self.simple_info.clear()
        for k, v in self.output_properties.items():
            for device_type in device_types:
                if k.startswith(device_type):
                    self.simple_info[k] = v.get("Device Name", "")

        for k, v in self.tracker_properties.items():
            for device_type in device_types:
                if k.startswith(device_type):
                    self.simple_info[k] = v.get("Device Name", "")

    def getDeviceName(self, device_type: str) -> list:
        """
        you can get any one type's name you want
        :param device_type: screen or sound
        :return: device_name
        """
        device: list = []

        for k, v in self.output_properties.items():
            if k.startswith(device_type):
                device.append(v.get("Device Name", ""))
        return device
