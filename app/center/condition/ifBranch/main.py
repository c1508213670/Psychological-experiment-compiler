from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QGroupBox, QPushButton, QVBoxLayout, QHBoxLayout

from app.func import Func
from lib import TabItemWidget
from ..childWidget import ChildWidget
from ..ifBranch.condition import ConditionArea


class IfBranch(TabItemWidget):
    """
    {
        "Condition": "",
        "Yes": "",
        "No": ""
    }

    """
    itemAdded = pyqtSignal(str, str, str)
    itemDeleted = pyqtSignal(int, str)
    itemNameChanged = pyqtSignal(str, str)

    def __init__(self, widget_id: str, widget_name: str):
        super(IfBranch, self).__init__(widget_id, widget_name)

        # 条件
        self.condition_area = ConditionArea()
        # 事件
        self.true_icon_choose = ChildWidget()
        self.true_icon_choose.itemAdded.connect(lambda a, b: self.itemAdded.emit(self.widget_id, a, b))
        self.true_icon_choose.itemDeleted.connect(lambda a: self.itemDeleted.emit(3, a))
        self.true_icon_choose.itemNameChanged.connect(lambda a, b: self.itemNameChanged.emit(a, b))

        self.false_icon_choose = ChildWidget()
        self.false_icon_choose.itemAdded.connect(lambda a, b: self.itemAdded.emit(self.widget_id, a, b))
        self.false_icon_choose.itemDeleted.connect(lambda a: self.itemDeleted.emit(3, a))
        self.false_icon_choose.itemNameChanged.connect(lambda a, b: self.itemNameChanged.emit(a, b))

        self.default_properties = {
            "Condition": self.condition_area.default_properties,
            "Yes": self.true_icon_choose.default_properties,
            "No": self.false_icon_choose.default_properties
        }

        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.ok)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.cancel)
        self.apply_button = QPushButton("Apply")
        self.apply_button.clicked.connect(self.apply)
        self.setUI()

    def setUI(self):
        condition_group = QGroupBox("Condition")
        layout1 = QVBoxLayout()
        layout1.addWidget(self.condition_area)
        condition_group.setLayout(layout1)

        true_group = QGroupBox("If True")
        layout2 = QVBoxLayout()
        layout2.addWidget(self.true_icon_choose)
        true_group.setLayout(layout2)

        false_group = QGroupBox("If False")
        layout3 = QVBoxLayout()
        layout3.addWidget(self.false_icon_choose)
        false_group.setLayout(layout3)

        buttons_layout = QHBoxLayout()

        buttons_layout.addStretch(1)
        buttons_layout.addWidget(self.ok_button)
        buttons_layout.addWidget(self.cancel_button)
        buttons_layout.addWidget(self.apply_button)
        buttons_layout.setContentsMargins(0, 0, 0, 0)

        layout = QVBoxLayout()
        layout.addWidget(condition_group, 1)
        tf_layout = QHBoxLayout()
        tf_layout.addWidget(true_group)
        tf_layout.addWidget(false_group)
        layout.addLayout(tf_layout, 20)
        layout.addLayout(buttons_layout, 1)
        self.setLayout(layout)

    def refresh(self):
        self.true_icon_choose.refresh()
        self.false_icon_choose.refresh()
        self.setAttributes(Func.getWidgetAttributes(self.widget_id))

    def updateInfo(self):
        self.condition_area.updateInfo()
        self.true_icon_choose.updateInfo()
        self.false_icon_choose.updateInfo()

    def getProperties(self):
        self.refresh()
        return self.default_properties

    def ok(self):
        self.apply()
        self.close()
        self.tabClosed.emit(self.widget_id)

    def cancel(self):
        self.loadSetting()

    def apply(self):
        self.updateInfo()
        self.propertiesChanged.emit(self.widget_id)
        attributes = Func.getWidgetAttributes(self.widget_id)
        self.setAttributes(attributes)

    def setProperties(self, properties: dict):
        self.condition_area.setProperties(properties.get("Condition"))
        self.true_icon_choose.setProperties(properties.get("Yes"))
        self.false_icon_choose.setProperties(properties.get("No"))
        # self.loadSetting()

    def restore(self, properties: dict):
        self.setProperties(properties)

    def store(self):
        self.updateInfo()
        return self.default_properties

    def loadSetting(self):
        self.condition_area.loadSetting()
        self.true_icon_choose.loadSetting()
        self.false_icon_choose.loadSetting()

    def clone(self, new_widget_id: str, new_widget_name: str):
        self.updateInfo()
        clone_widget = IfBranch(new_widget_id, new_widget_name)
        clone_widget.setProperties(self.default_properties.copy())
        return clone_widget

    # 设置可选参数
    def setAttributes(self, attributes):
        format_attributes = ["[{}]".format(attribute) for attribute in attributes]
        self.condition_area.setAttributes(format_attributes)
        self.true_icon_choose.setAttributes(format_attributes)
        self.false_icon_choose.setAttributes(format_attributes)

    def getUsingDeviceCount(self) -> int:
        return self.true_icon_choose.getUsingDeviceCount() + self.false_icon_choose.getUsingDeviceCount()

    def getCondition(self) -> str:
        """
        返回判断条件
        :return:
        """
        return self.condition_area.getCondition()

    def getTrueWidgetInfo(self) -> dict:
        """
        获取信息，包括Event name等
        :return:
        """
        return self.true_icon_choose.getProperties()

    def getTrueWidget(self):
        return self.true_icon_choose.getWidget()

    def getFalseWidgetInfo(self) -> dict:
        return self.false_icon_choose.getProperties()

    def getFalseWidget(self):
        return self.false_icon_choose.getWidget()

    def getSubWidgetId(self):
        return self.true_icon_choose.current_sub_wid, self.false_icon_choose.current_sub_wid
