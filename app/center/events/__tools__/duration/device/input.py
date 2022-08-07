from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QListWidgetItem

from app.func import Func
from app.info import Info


class InputDevice(QListWidgetItem):
    def __init__(self, device_id: str, device_name: str, parent=None):
        super(InputDevice, self).__init__(device_name, parent)

        self.device_name = device_name
        self.device_id = device_id
        self.device_type = device_id.split(".")[0]
        self.setIcon(QIcon(Func.getImage(f"devices/{self.device_type}_device.png")))

        self.default_properties = {
            "Device Id": self.device_id,
            "Device Name": self.device_name,
            "Device Type": self.device_type,
            "Allowable": "",
            "Correct": "",
            "RT Window": "",
            "End Action": "",
            "Right": "",
            "Wrong": "",
            "No Resp": "",
            "Output Device": "",
            "Start": "",
            "End": "",
            "Mean": "",
            "Is Oval": "No",
        }

        if self.device_type == Info.DEV_KEYBOARD:
            self.allowable = "{any}"
        elif self.device_type == Info.DEV_MOUSE:
            self.allowable = "123"
        elif self.device_type == Info.DEV_RESPONSE_BOX:
            self.allowable = "12345678"
        elif self.device_type == Info.DEV_EYE_ACTION:
            self.allowable = "3456789"
        elif self.device_type == Info.DEV_GAMEPAD:
            self.allowable = "12345678"
        else:
            self.allowable = ""
        self.correct = ""
        self.rt_window = "(Same as duration)"
        self.end_action = "Terminate"
        self.right = ""
        self.wrong = ""
        self.no_resp = ""
        self.output_device = ""
        self.start = ""
        self.end = ""
        self.mean = ""
        self.is_oval = "No"

    def getDeviceId(self):
        return self.device_id

    def getDeviceName(self):
        return self.device_name

    def setDeviceName(self, new_name: str):
        self.device_name = new_name
        self.setText(new_name)

    def getInfo(self) -> dict:
        self.default_properties["Allowable"] = self.allowable
        self.default_properties["Correct"] = self.correct
        self.default_properties["RT Window"] = self.rt_window
        self.default_properties["End Action"] = self.end_action

        self.default_properties["Device Name"] = self.device_name
        self.default_properties["Device Type"] = self.device_type
        self.default_properties["Right"] = self.right
        self.default_properties["Wrong"] = self.wrong
        self.default_properties["No Resp"] = self.no_resp
        self.default_properties["Output Device"] = self.output_device

        self.default_properties["Start"] = self.start
        self.default_properties["End"] = self.end
        self.default_properties["Is Oval"] = self.is_oval
        return self.default_properties

    def setProperties(self, device_info: dict):
        self.default_properties = device_info.copy()
        self.loadSetting()

    def loadSetting(self):
        self.device_id = self.default_properties.get("Device Id")
        self.device_name = self.default_properties.get("Device Name")
        self.device_type = self.default_properties.get("Device Type")

        self.allowable = self.default_properties["Allowable"]
        self.correct = self.default_properties["Correct"]
        self.rt_window = self.default_properties["RT Window"]
        self.end_action = self.default_properties["End Action"]

        self.device_name = self.default_properties["Device Name"]
        self.right = self.default_properties["Right"]
        self.wrong = self.default_properties["Wrong"]
        self.no_resp = self.default_properties["No Resp"]
        self.output_device = self.default_properties["Output Device"]

        self.start = self.default_properties["Start"]
        self.end = self.default_properties["End"]
        self.mean = self.default_properties["Mean"]
        self.is_oval = self.default_properties["Is Oval"]

    def __str__(self):
        return f"{self.device_name}, {self.device_id}"
