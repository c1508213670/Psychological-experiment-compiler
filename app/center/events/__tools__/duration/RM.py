from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QPushButton, QGridLayout, QLabel, QGroupBox

from app.center.events.__tools__.duration.deviceSelectionWindow import DeviceDialog
from app.center.events.__tools__.duration.describer.control import Describer
from app.center.events.__tools__.duration.device.control import DeviceHome


class outputDevicesDur(QGroupBox):
    deviceChanged = pyqtSignal(list)

    def __init__(self, title: str = "Stimulus Trigger", parent=None):
        super(outputDevicesDur, self).__init__(title, parent)
        self.home = DeviceHome()
        self.add_bt = QPushButton("Add")
        self.del_bt = QPushButton("Delete")
        self.del_bt.setEnabled(True)

        self.describer = Describer(0)

        self.default_properties = {}
        self.home.default_properties = self.default_properties
        self.describer.default_properties = self.default_properties

        self.dialog = DeviceDialog(0)
        self.dialog.deviceAdd.connect(self.add)
        self.add_bt.clicked.connect(self.dialog.show)
        self.del_bt.clicked.connect(self.delete)
        self.home.deviceChanged.connect(self.describer.describe)

        self.attribs = []

        self.setUI()

    def setUI(self):
        layout = QGridLayout()
        layout.addWidget(QLabel("Output Devices"), 0, 0, 1, 2)
        layout.addWidget(QLabel("Trigger Info"), 0, 2, 1, 1)
        layout.addWidget(self.home, 1, 0, 2, 2)
        layout.addWidget(self.add_bt, 3, 0, 1, 1)
        layout.addWidget(self.del_bt, 3, 1, 1, 1)
        layout.addWidget(self.describer, 1, 2, 2, 2)
        layout.setVerticalSpacing(0)
        self.setLayout(layout)

    def refresh(self):
        self.home.refresh()
        self.describer.refresh()
        self.updateInfo()

    def setAttributes(self, attributes: list):
        self.attribs = attributes
        # self.describer.setAttributes(attributes)
        self.setAttributesForSubArea()

    def setAttributesForSubArea(self):
        self.describer.setAttributes(self.attribs)

    def setProperties(self, properties: dict):
        self.default_properties.update(properties)
        self.loadSetting()

    def loadSetting(self):
        self.home.loadSetting()

    def add(self, device_id, device_name):
        self.home.createDevice(device_id, device_name)
        self.del_bt.setEnabled(self.home.count() > 0)
        self.deviceChanged.emit(self.home.getDeviceList())

    def delete(self):
        self.home.deleteDevice()
        self.del_bt.setEnabled(self.home.count() > 0)
        self.deviceChanged.emit(self.home.getDeviceList())

    def updateInfo(self):
        self.describer.updateInfo()
        self.home.updateDeviceInfo()


class inputDevicesDur(QGroupBox):
    def __init__(self, title="Input Devices", parent=None):
        super(inputDevicesDur, self).__init__(title, parent)
        self.home = DeviceHome()
        self.add_bt = QPushButton("Add")
        self.del_bt = QPushButton("Delete")
        self.del_bt.setEnabled(True)

        self.default_properties: dict = {}
        self.home.default_properties = self.default_properties

        self.resp_info = Describer(1)
        self.resp_trigger = Describer(2)
        self.eye_action = Describer(3)

        self.dialog = DeviceDialog(1)
        self.dialog.deviceAdd.connect(self.add)
        self.add_bt.clicked.connect(self.dialog.show)
        self.del_bt.clicked.connect(self.delete)
        self.home.deviceChanged.connect(self.resp_info.describe)
        self.home.deviceChanged.connect(self.resp_trigger.describe)
        self.home.deviceChanged.connect(self.eye_action.describe)

        self.attribs = []
        self.setUI()

    def setUI(self):
        layout = QGridLayout()
        layout.addWidget(QLabel("Device(s)"), 0, 0, 1, 1)
        layout.addWidget(self.home, 1, 0, 3, 2)
        layout.addWidget(self.add_bt, 4, 0, 1, 1)
        layout.addWidget(self.del_bt, 4, 1, 1, 1)
        # layout.addWidget(self.in_tip1, 1, 2, 5, 2)
        layout.addWidget(self.resp_info, 0, 2, 5, 2)
        # layout.addWidget(self.in_tip2, 5, 0, 2, 4)
        layout.addWidget(self.resp_trigger, 5, 0, 2, 4)
        # layout.addWidget(self.in_tip3, 7, 0, 2, 4)
        layout.addWidget(self.eye_action, 7, 0, 2, 4)
        layout.setVerticalSpacing(0)
        self.setLayout(layout)

    def add(self, device_id, device_name):
        self.home.createDevice(device_id, device_name)
        self.setAttributesForSubArea()
        # self.resp_trigger.setAttributes(self.attribs)
        # self.eye_action.setAttributes(self.attribs)
        self.del_bt.setEnabled(self.home.count() > 0)

    def delete(self):
        self.home.deleteDevice()
        self.del_bt.setEnabled(self.home.count() > 0)

    def updateExternalInfo(self, output_device: list):
        self.resp_trigger.updateSimpleInfo(output_device)

    def updateInfo(self):
        info1 = self.resp_info.getInfo()
        info2 = self.resp_trigger.getInfo()
        info3 = self.eye_action.getInfo()

        self.default_properties.clear()
        for k in info1.keys():
            self.default_properties[k] = {**info1[k], **info2[k], **info3[k]}
        self.home.updateDeviceInfo()

    def refresh(self):
        self.home.refresh()
        self.resp_info.refresh()
        self.resp_trigger.refresh()
        self.eye_action.refresh()

    def setAttributes(self, attributes: list):
        self.attribs = attributes
        self.setAttributesForSubArea()
        # self.resp_info.setAttributes(attributes)
        # self.resp_trigger.setAttributes(attributes)
        # self.eye_action.setAttributes(attributes)

    def setAttributesForSubArea(self):
        self.resp_info.setAttributes(self.attribs)
        self.resp_trigger.setAttributes(self.attribs)
        self.eye_action.setAttributes(self.attribs)

    def setProperties(self, properties: dict):
        self.default_properties.update(properties)
        self.loadSetting()

    def loadSetting(self):
        self.home.loadSetting()
