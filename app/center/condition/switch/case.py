from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QComboBox, QGridLayout, QLabel, QGroupBox, QCompleter

from lib import VarComboBox
from ..addDeleteButton import AddDeleteButton
from ..childWidget import ChildWidget


class Case(QGroupBox):
    """
    {
        "case value" : "",
        "stim type": "Image",
        "event name": "",
        "pro window": {}
    }
    """
    add = pyqtSignal()
    delCase = pyqtSignal(int)
    addCase = pyqtSignal(int)

    def __init__(self, title: str = "", parent=None):
        super(Case, self).__init__(title, parent)

        self.index = 0
        for c in title[::-1]:
            if c.isdigit():
                self.index = int(c)
                break

        # case
        self.values = VarComboBox(True)
        self.values.setInsertPolicy(QComboBox.NoInsert)

        # icon choose
        self.icon_choose = ChildWidget()

        self.default_properties: dict = self.icon_choose.default_properties
        self.default_properties["Case Value"] = ""

        self.add_bt = AddDeleteButton(self, "add")
        self.add_bt.clicked.connect(lambda: self.addCase.emit(self.index))
        self.del_bt = AddDeleteButton(self, "delete")
        self.del_bt.clicked.connect(lambda: self.delCase.emit(self.index))
        self.setUI()

    def setUI(self):
        grid_layout = QGridLayout()
        tip = QLabel("Value:")
        tip.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        if self.index:
            grid_layout.addWidget(tip, 0, 0, 1, 1)
            grid_layout.addWidget(self.values, 0, 1, 1, 5)
        grid_layout.addWidget(self.icon_choose, 1, 0, 3, 5)
        grid_layout.addWidget(self.add_bt, 4, 1, 1, 1)
        grid_layout.addWidget(self.del_bt, 4, 3, 1, 1)
        self.setLayout(grid_layout)

        self.setMaximumHeight(300)

    def refresh(self):
        self.icon_choose.refresh()

    def setNotAdd(self, no=True):
        self.add_bt.setEnabled(not no)

    def setNotDel(self, no=True):
        self.del_bt.setEnabled(not no)

    def updateInfo(self):
        self.icon_choose.updateInfo()
        self.default_properties["Case Value"] = self.values.currentText()

    def getInfo(self):
        self.updateInfo()
        return self.default_properties

    # 导入参数
    def setProperties(self, properties: dict):
        case_value = properties.get("Case Value", "")
        self.values.setCurrentText(case_value)
        # properties.pop("Case Value", "")
        self.icon_choose.setProperties(properties)

    def loadSetting(self):
        self.values.setCurrentText(self.default_properties.get("Case Value"))
        self.icon_choose.loadSetting()

    # 以便在其之前插入新的case
    def changeTitle(self, new_title: str):
        self.setTitle(new_title)
        for c in new_title:
            if c.isdigit():
                self.index = int(c)
                break

    def updateIndex(self, step: int = 1):
        self.index += step
        self.setTitle(f"Case {self.index}")

    def setAttributes(self, attributes: list):
        cCaseValueStr = self.values.currentText()
        self.values.addItems(attributes)
        self.values.setCompleter(QCompleter(attributes))
        self.values.setCurrentText(cCaseValueStr)

    def getCase(self) -> dict:
        return {
            "Case Value": self.default_properties.get("Case Value", ""),
            **self.icon_choose.getProperties(),
        }

    def getSubWid(self):
        return self.icon_choose.current_sub_wid
