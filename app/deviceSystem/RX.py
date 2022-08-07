import re

from PyQt5.QtCore import QSize, pyqtSignal, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QListWidget, QVBoxLayout, QHBoxLayout, QListView, QFrame, \
    QPushButton, QInputDialog, QLineEdit, QMessageBox

from app.deviceSystem.describer.control import Describer
from app.deviceSystem.device.control import DeviceHome, Device
from app.func import Func
from app.defi import *
from app.info import Info


class RX(QWidget):
    """
    :param device_type: 0-输入、1-输出设备、2-quest、3-tracker
    """
    deviceNameChanged = pyqtSignal(str, str)
    deviceOK = pyqtSignal()

    def __init__(self, device_type: int = 0, parent=None):
        super(RX, self).__init__(parent)
        self.setWindowModality(Qt.ApplicationModal)

        # 上方待选择设备
        self.device_bar = QListWidget()
        self.device_bar.setViewMode(QListView.IconMode)
        self.device_bar.setSortingEnabled(True)
        self.device_bar.setAcceptDrops(False)
        self.device_bar.setAutoFillBackground(True)
        self.device_bar.setWrapping(False)
        self.device_bar.setSpacing(10)
        self.device_bar.setFrameStyle(QFrame.NoFrame)
        self.device_bar.setIconSize(QSize(40, 40))

        # 设备类型
        self.device_type = device_type
        # 设备信息
        self.default_properties: dict = {}

        # 已选择设备
        self.device_home = DeviceHome()
        self.device_home.itemDoubleClicked.connect(self.rename)
        self.device_home.deviceChanged.connect(self.changeItem)
        self.device_home.deviceDeleted.connect(self.changeItem)

        # 展示区
        self.describer = Describer()

        self.device_home.default_properties = self.default_properties
        self.describer.default_properties = self.default_properties

        # device_list是写死的
        if device_type == OUTPUT_DEVICE:
            # default device
            self.device_home.createDevice(DEV_SCREEN)
            Info.OUTPUT_DEVICE_INFO = self.default_properties
            self.devices = (DEV_SERIAL_PORT, DEV_PARALLEL_PORT, DEV_NETWORK_PORT, DEV_SCREEN, DEV_SOUND)
            self.setWindowTitle("Output Devices")
        elif device_type == INPUT_DEVICE:
            # default devices
            self.device_home.createDevice(DEV_MOUSE)
            self.device_home.createDevice(DEV_KEYBOARD)
            Info.INPUT_DEVICE_INFO = self.default_properties
            self.devices = (DEV_MOUSE, DEV_KEYBOARD, DEV_RESPONSE_BOX, DEV_GAMEPAD, DEV_EYE_ACTION)
            self.setWindowTitle("Input Devices")
        elif device_type == QUEST_DEVICE:
            Info.QUEST_DEVICE_INFO = self.default_properties
            self.devices = (DEV_QUEST,)
            self.setWindowTitle("Quest Devices")
        elif device_type == TRACKER_DEVICE:
            Info.TRACKER_DEVICE_INFO = self.default_properties
            self.devices = (DEV_TRACKER,)
            self.setWindowTitle("Tracker Devices")
        self.setWindowIcon(QIcon(Func.getImage("common/icon.png")))
        for device in self.devices:
            self.device_bar.addItem(Device(device))

        self.ok()

        # 按键区
        self.ok_bt = QPushButton("OK")
        self.ok_bt.clicked.connect(self.ok)
        self.cancel_bt = QPushButton("Cancel")
        self.cancel_bt.clicked.connect(self.cancel)
        self.apply_bt = QPushButton("Apply")
        self.apply_bt.clicked.connect(self.apply)
        self.setUI()

    def setUI(self):
        layout = QVBoxLayout()

        layout1 = QHBoxLayout()
        layout1.addWidget(self.device_home, 1)
        layout1.addWidget(self.describer, 1)

        layout2 = QHBoxLayout()
        layout2.addStretch(5)
        layout2.addWidget(self.ok_bt)
        layout2.addWidget(self.cancel_bt)
        layout2.addWidget(self.apply_bt)

        layout.addWidget(self.device_bar, 1)
        layout.addLayout(layout1, 3)
        layout.addLayout(layout2, 1)
        self.setLayout(layout)

    def ok(self):
        self.apply()
        self.close()

    def cancel(self):
        self.device_home.loadSetting()
        self.repaint()

    def apply(self):
        self.getInfo()
        self.deviceOK.emit()

        if self.device_type == OUTPUT_DEVICE and self.device_home.currentItem() and DEV_SCREEN == self.device_home.currentItem().device_type:
            for wid, cWidget in Info.WID_WIDGET.items():
                if wid.split('.')[0] in [COMBO, TEXT, IMAGE, VIDEO, SOUND]:
                    if cWidget.isVisible():
                        cWidget.refresh()
                        break

    def changeItem(self, device_id: str, info: dict):
        self.describer.describe(device_id, info)

    def rename(self, item: Device):
        name: str = item.text()
        item_name: str = name.lower()

        new_name, ok = QInputDialog.getText(self, "Change Device Name", "Device Name:", QLineEdit.Normal, item.text())
        if ok and new_name != '' and re.fullmatch(r"[A-Za-z][\d\sA-Za-z_]+", new_name):
            new_name: str
            if new_name.lower() in self.device_home.device_list and item_name != new_name.lower():
                QMessageBox.warning(self, f"{new_name} is invalid!", "Device name must be unique and without spaces",
                                    QMessageBox.Ok)
            else:
                self.device_home.changeCurrentName(item_name, new_name)
                self.describer.changeName(item_name, new_name)
                self.deviceNameChanged.emit(item.getDeviceId(), new_name)

    # 参数导出, 记录到Info
    def getInfo(self):
        # get device information from GUI
        self.describer.updateInfo()
        # update device information
        self.device_home.updateDeviceInfo()
        return self.default_properties.copy()

    # 参数导入
    def setProperties(self, properties: dict):
        self.default_properties.clear()
        self.default_properties.update(properties)
        self.loadSetting()
        self.deviceOK.emit()

    def loadSetting(self):
        self.device_home.loadSetting()

    def refresh(self):
        self.describer.updateSimpleInfo()

    def show(self) -> None:
        self.refresh()
        super().show()
