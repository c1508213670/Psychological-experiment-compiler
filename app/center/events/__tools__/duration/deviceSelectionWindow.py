from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QLabel, QListWidget, QPushButton, QListView, QGridLayout, QListWidgetItem

from app.func import Func
from app.info import Info
from lib import Dialog


class DeviceDialog(Dialog):
    deviceAdd = pyqtSignal(str, str)

    def __init__(self, io_type, parent=None):
        super(DeviceDialog, self).__init__(parent=parent)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.io_type = io_type

        self.tip = QLabel("Please choose device(s) from menu bar first!")
        self.tip.setAlignment(Qt.AlignCenter)
        self.devices_list = QListWidget()
        self.ok_bt = QPushButton("OK")
        self.cancel_bt = QPushButton("Cancel")
        self.ok_bt.clicked.connect(self.ok)
        self.cancel_bt.clicked.connect(self.close)
        self.setUI()

    def setUI(self):
        self.resize(500, 350)
        self.setWindowTitle("Choose Device(s)")
        self.devices_list.setViewMode(QListView.IconMode)
        self.devices_list.setSortingEnabled(True)
        self.devices_list.setAcceptDrops(False)
        self.devices_list.setAutoFillBackground(True)
        self.devices_list.setSpacing(20)

        layout = QGridLayout()
        layout.addWidget(self.devices_list, 0, 0, 1, 4)
        layout.addWidget(self.tip, 0, 0, 1, 4)
        layout.addWidget(self.ok_bt, 1, 2, 1, 1)
        layout.addWidget(self.cancel_bt, 1, 3, 1, 1)
        self.setLayout(layout)

    # 从菜单栏添加待选设备
    # devices: dict
    # 图片名与设备名相同
    def addDevices(self, devices: dict):
        self.tip.show()
        self.devices_list.clear()
        for k, v in devices.items():
            device_type = v.get("Device Type")
            if device_type == Info.DEV_SCREEN or device_type == Info.DEV_SOUND:
                continue
            device_name = v.get("Device Name")

            item = QListWidgetItem(device_name)
            item.setData(3, k)
            item.setIcon(QIcon(Func.getImage(f"devices/{device_type}_device.png")))
            self.devices_list.addItem(item)
            self.tip.hide()

    def ok(self):
        selected_device = self.devices_list.currentItem()
        if selected_device:
            device_id = selected_device.data(3)
            device_name = selected_device.text()
            self.deviceAdd.emit(device_id, device_name)
        self.close()

    def refresh(self):
        if self.io_type == 0:
            self.addDevices(Info.OUTPUT_DEVICE_INFO)
        else:
            self.addDevices(Info.INPUT_DEVICE_INFO)

    def show(self):
        self.refresh()
        return super().show()

    def getDeviceInfo(self):
        self.refresh()
        info = {}
        for i in self.devices_list.count():
            info[self.devices_list.item(i).data(3)] = self.devices_list.item(i).text()
        return info
