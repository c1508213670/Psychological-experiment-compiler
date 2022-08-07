from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QHBoxLayout, QPushButton, QVBoxLayout

from app.func import Func
from lib import TabItemWidget
from .case import Case
from .caseArea import CaseArea
from .condition import SwitchCondition


class Switch(TabItemWidget):
    """
    {
        "switch": ""
        "case": {}
    """
    itemAdded = pyqtSignal(str, str, str)
    itemDeleted = pyqtSignal(int, str)
    itemNameChanged = pyqtSignal(str, str)

    def __init__(self, widget_id: str, widget_name):
        super(Switch, self).__init__(widget_id, widget_name)
        #
        self.switch_area = SwitchCondition()
        self.case_area = CaseArea(self)

        self.case_area.itemAdded.connect(lambda a, b: self.itemAdded.emit(self.widget_id, a, b))
        self.case_area.itemDeleted.connect(lambda a: self.itemDeleted.emit(3, a))
        self.case_area.itemNameChanged.connect(lambda a, b: self.itemNameChanged.emit(a, b))

        self.default_properties: dict = {
            "Switch": self.switch_area.getProperties(),
            "Case": self.case_area.default_properties
        }

        self.ok_bt = QPushButton("OK")
        self.ok_bt.clicked.connect(self.ok)
        self.cancel_bt = QPushButton("Cancel")
        self.cancel_bt.clicked.connect(self.cancel)
        self.apply_bt = QPushButton("Apply")
        self.apply_bt.clicked.connect(self.apply)

        self.setUI()

    def setUI(self):
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch(1)
        buttons_layout.addWidget(self.ok_bt)
        buttons_layout.addWidget(self.cancel_bt)
        buttons_layout.addWidget(self.apply_bt)

        layout = QVBoxLayout()
        layout.addWidget(self.switch_area, 1)
        layout.addWidget(self.case_area, 20)
        layout.addLayout(buttons_layout, 1)
        self.setLayout(layout)

    def ok(self):
        self.apply()
        self.close()
        self.tabClosed.emit(self.widget_id)

    def cancel(self):
        self.loadSetting()

    def apply(self):
        self.updateInfo()
        self.propertiesChanged.emit(self.widget_id)

    def refresh(self):
        attributes = Func.getWidgetAttributes(self.widget_id)
        self.setAttributes(attributes)
        self.case_area.refresh()

    def updateInfo(self):
        self.case_area.updateInfo()
        self.default_properties["Switch"] = self.switch_area.getProperties()

    def getUsingDeviceCount(self) -> int:
        return self.case_area.getUsingDeviceCount()

    def getProperties(self):
        self.refresh()
        return self.default_properties

    def setProperties(self, properties: dict):
        self.case_area.setProperties(properties.get("Case"))
        self.switch_area.setProperties(properties.get("Switch"))
        self.default_properties["Switch"] = properties.get("Switch")

    def restore(self, properties: dict):
        self.setProperties(properties)

    def store(self):
        self.updateInfo()
        return self.default_properties

    def loadSetting(self):
        self.switch_area.setProperties(self.default_properties.get("Switch", ""))
        self.case_area.loadSetting()

    def clone(self, new_widget_id: str, new_widget_name: str):
        self.updateInfo()
        clone_widget = Switch(new_widget_id, new_widget_name)
        clone_widget.setProperties(self.default_properties.copy())
        return clone_widget

    def setAttributes(self, attributes: list):
        format_attributes = ["[{}]".format(attribute) for attribute in attributes]
        self.switch_area.setAttributes(format_attributes)
        self.case_area.setAttributes(format_attributes)

    def getSwitch(self) -> str:
        return self.default_properties.get("Switch", "")

    def getCasesInfo(self) -> list:
        """
        :return: [case1, case2, ...]
        case1: dict
        """
        return self.default_properties.get("Case", {})

    def getCases(self):
        return [case.getCase() for case in self.case_area.case_list]

    def getSubWidgetId(self):
        sub_wid = []
        for case in self.case_area.case_list:
            case: Case
            wid = case.getSubWid()
            if wid:
                sub_wid.append(wid)
        return sub_wid
