from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QListWidget, QMenu, QListWidgetItem

from app.deviceSystem.device import *
from app.info import Info


class DeviceHome(QListWidget):
    deviceChanged = pyqtSignal(str, dict)
    deviceDeleted = pyqtSignal(str, dict)

    def __init__(self, parent=None):
        super(DeviceHome, self).__init__(parent)

        # 设备计数，生成设备id
        self.device_count = {
            # input device
            Info.DEV_MOUSE: 0,
            Info.DEV_KEYBOARD: 0,
            Info.DEV_RESPONSE_BOX: 0,
            Info.DEV_GAMEPAD: 0,
            Info.DEV_EYE_ACTION: 0,
            # simple_info device
            Info.DEV_SERIAL_PORT: 0,
            Info.DEV_PARALLEL_PORT: 0,
            Info.DEV_NETWORK_PORT: 0,
            Info.DEV_SCREEN: 0,
            Info.DEV_SOUND: 0,
            # quest
            Info.DEV_QUEST: 0,
            # tracker
            Info.DEV_TRACKER: 0,
        }

        # 存放当前选择设备名，避免重复，只通过create\delete操作
        self.device_list = []

        # 记录属性
        self.default_properties = {
            # device_id : device_info
        }

        self.currentItemChanged.connect(self.changeDevice)

        # 拖动的图标
        self.dragItem = None
        # self.setViewMode(QListView.IconMode)
        self.setAcceptDrops(True)
        self.setSortingEnabled(True)
        self.setWrapping(False)
        self.createContextMenu()

    def dropEvent(self, e):
        source = e.source()
        device_type = source.currentItem().getType()
        self.createDevice(device_type)

    def dragEnterEvent(self, e):
        source = e.source()
        if source != self:
            e.setDropAction(Qt.MoveAction)
        e.accept()

    def createContextMenu(self):
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showContextMenu)
        self.contextMenu = QMenu(self)
        self.rename_action = self.contextMenu.addAction("rename")
        self.rename_action.triggered.connect(lambda: self.itemDoubleClicked.emit(self.currentItem()))

        self.delete_action = self.contextMenu.addAction("delete")
        self.delete_action.triggered.connect(lambda: self.deleteDevice(index=-1))
        self.clear_action = self.contextMenu.addAction("clear all")
        self.clear_action.triggered.connect(self.clearAll)

    def clearAll(self):
        """
        everything rollback
        :return:
        """
        for i in range(self.count() - 1, -1, -1):
            self.deleteDevice(i)
        for k in self.device_count.keys():
            self.device_count[k] = 0

    def showContextMenu(self, pos):
        if self.count():
            item = self.itemAt(pos)
            if item:
                self.contextMenu.exec_(QCursor.pos())  # 在鼠标位置显示

    def changeDevice(self, item: Device, item_1: Device):
        """
        :param item: to this item
        :param item_1: from this item
        :return:
        """
        if item is not None:
            self.deviceChanged.emit(item.getDeviceId(), item.getInfo())

    def updateDeviceInfo(self):
        for i in range(self.count()):
            item: Device = self.item(i)
            device_id = item.getDeviceId()
            item.setProperties(self.default_properties[device_id])

    def setProperties(self, properties: dict):
        self.default_properties = properties.copy()
        self.loadSetting()

    # 以default_properties导入
    def loadSetting(self):
        # 从properties添加
        self.clearAll()
        for k, v in self.default_properties.items():
            v: dict
            device_id = k
            device_type = v.get("Device Type")
            device_name = v.get("Device Name")
            self.createDevice(device_type, device_id, device_name, device_info=v)
            # load count of devices
            self.device_count[device_type] += 1

    def createDeviceId(self, device_type):
        """
        生成设备标识符
        :param device_type:
        :return:
        """
        current_id = self.device_count[device_type]
        self.device_count[device_type] = current_id + 1
        return f"{device_type}.{current_id}"

    def deleteDevice(self, index: int = -1):
        """
        删除设备
        :param index: 设备索引，默认当前选中
        :return:
        """
        if index == -1:
            index = self.currentRow()
        # 被删掉的设备
        del_device: Device = self.takeItem(index)
        device_name: str = del_device.getName()
        self.device_list.remove(device_name.lower())
        self.deviceDeleted.emit(del_device.getDeviceId(), {})

    def createDevice(self, device_type, device_id=None, device_name=None, device_info=None):
        """
        添加设备到已选列表
        :param device_info: 设备信息
        :param device_name:
        :param device_id: 设备标识符
        :param device_type: 设备类型
        :return:
        """
        if device_id is None:
            device_id = self.createDeviceId(device_type)

        # 新建设备对象
        if device_type == Info.DEV_SOUND:
            device = Sound(device_type, device_id)
        elif device_type == Info.DEV_SCREEN:
            device = Screen(device_type, device_id)
        elif device_type == Info.DEV_NETWORK_PORT:
            device = Net(device_type, device_id)
        elif device_type == Info.DEV_PARALLEL_PORT:
            device = Parallel(device_type, device_id)
        elif device_type == Info.DEV_SERIAL_PORT:
            device = Serial(device_type, device_id)
        elif device_type == Info.DEV_QUEST:
            device = Quest(device_type, device_id)
        elif device_type == Info.DEV_TRACKER:
            device = Tracker(device_type, device_id)
        elif device_type == Info.DEV_EYE_ACTION:
            device = Action(device_type, device_id)
        elif device_type == Info.DEV_GAMEPAD:
            device = GamePad(device_type, device_id)
        elif device_type == Info.DEV_MOUSE:
            device = Mouse(device_type, device_id)
        elif device_type == Info.DEV_KEYBOARD:
            device = Keyboard(device_type, device_id)
        elif device_type == Info.DEV_RESPONSE_BOX:
            device = ResponseBox(device_type, device_id)
        else:
            device = Device(device_type, device_id)

        if device_name is None:
            device_name = device_id.replace(".", "_")
        self.device_list.append(device_name.lower())
        device.setName(device_name)

        # 载入信息
        if device_info is not None:
            device.setProperties(device_info)
        self.addItem(device)
        self.setCurrentItem(device)

    def changeCurrentName(self, old_name: str, new_name: str):
        self.currentItem().setText(new_name)
        self.device_list.remove(old_name)
        self.device_list.append(new_name)

    def checkDeviceName(self, new_name: str):
        if new_name.lower() in self.device_list or new_name == "" or "." in new_name:
            return False
        return True
