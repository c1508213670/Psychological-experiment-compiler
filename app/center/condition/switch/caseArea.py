from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QGridLayout, QWidget, QScrollArea

from app.center.condition.switch.case import Case


class CaseArea(QScrollArea):
    """
    {
        "case 1": ...,
        "case 2": ...,
        ...
        "Default": ...
        }
    """
    MAX_CASE_COUNT = 9
    MIN_CASE_COUNT = 3

    itemAdded = pyqtSignal(str, str)
    itemDeleted = pyqtSignal(str)
    itemNameChanged = pyqtSignal(str, str)

    def __init__(self, parent=None):
        super(CaseArea, self).__init__(parent)

        self.attributes: list = []

        self.case_default = Case(title='Otherwise')

        self.case_list: list = [Case(title='Case 1'), Case(title='Case 2'), self.case_default]
        self.case_list[0].addCase.connect(self.insertCase)
        self.case_list[1].addCase.connect(self.insertCase)
        self.case_list[0].delCase.connect(self.delCase)
        self.case_list[1].delCase.connect(self.delCase)

        self.default_properties: dict = {
            "Otherwise": self.case_default.default_properties,
            "Case 1": self.case_list[0].default_properties,
            "Case 2": self.case_list[1].default_properties,
        }
        for c in self.case_list:
            c.icon_choose.itemAdded.connect(self.itemAdded)
            c.icon_choose.itemDeleted.connect(self.itemDeleted)
            c.icon_choose.itemNameChanged.connect(self.itemDeleted)

        self.setUI()

    def setUI(self):
        self.layout = QGridLayout()
        self.layout.addWidget(self.case_list[0], 0, 0)
        self.layout.addWidget(self.case_list[1], 0, 1)
        self.layout.addWidget(self.case_default, 0, 2)
        self.whiteboard = QWidget()
        self.whiteboard.setLayout(self.layout)
        self.setWidget(self.whiteboard)
        self.setWidgetResizable(True)

    def refresh(self):
        for case in self.case_list:
            case.refresh()

    def insertCase(self, index):
        # 更新case的index
        for case in self.case_list[index:-1]:
            case.updateIndex(1)
            self.layout.removeWidget(case)

        self.layout.removeWidget(self.case_default)
        new_case = Case(f"Case {index + 1}")
        new_case.setAttributes(self.attributes)
        new_case.addCase.connect(self.insertCase)
        new_case.delCase.connect(self.delCase)

        new_case.icon_choose.itemAdded.connect(self.itemAdded)
        new_case.icon_choose.itemDeleted.connect(self.itemDeleted)
        new_case.icon_choose.itemNameChanged.connect(self.itemNameChanged)

        self.case_list.insert(index, new_case)
        for case in self.case_list[index:-1]:
            self.addCase(case)
        cnt = len(self.case_list)
        self.layout.addWidget(self.case_default, (cnt - 1) // 3, (cnt - 1) % 3)
        self.noAdd(cnt >= CaseArea.MAX_CASE_COUNT)
        self.noDel(cnt <= CaseArea.MIN_CASE_COUNT)
        self.update()
        self.repaint()

    def delCase(self, index):
        del_case: Case = self.case_list.pop(index - 1)
        self.layout.removeWidget(del_case)
        del_case.hide()
        for case in self.case_list[index - 1:-1]:
            case.updateIndex(-1)
            self.layout.removeWidget(case)
        self.layout.removeWidget(self.case_default)
        for case in self.case_list[index - 1:-1]:
            self.addCase(case)
        cnt = len(self.case_list)
        self.layout.addWidget(self.case_default, (cnt - 1) // 3, (cnt - 1) % 3)
        self.noAdd(cnt >= CaseArea.MAX_CASE_COUNT)
        self.noDel(cnt <= CaseArea.MIN_CASE_COUNT)
        self.update()
        self.repaint()

        del_widget_id = del_case.icon_choose.current_sub_wid
        if del_widget_id != "":
            # send to wid_node to delete the widget from node
            self.itemDeleted.emit(del_widget_id)

    def addCase(self, case: Case):
        index = case.index
        row = (index - 1) // 3
        col = (index - 1) % 3
        self.layout.addWidget(case, row, col)

    def noAdd(self, no=True):
        for case in self.case_list:
            case.setNotAdd(no)

    def noDel(self, no=True):
        """
        :param no: T=
        :return:
        """
        for case in self.case_list:
            case.setNotDel(no)

    def updateInfo(self):
        self.default_properties.clear()
        for case in self.case_list:
            self.default_properties[case.title()] = case.getInfo()

    def setProperties(self, properties: dict):
        self.default_properties.update(properties)
        self.loadSetting()

    def loadSetting(self):
        old_cnt = len(self.default_properties)
        new_cnt = len(self.case_list)
        if old_cnt > new_cnt:
            for i in range(old_cnt - new_cnt):
                self.insertCase(new_cnt + i - 1)
        else:
            for i in range(new_cnt - old_cnt):
                self.delCase(old_cnt - 1)

        for case in self.case_list:
            # cCaseKey = case.title()
            # if "Otherwise" == cCaseKey:
            #     cCaseKey = "Default"
            cCaseInfo = self.default_properties.get(case.title(), {})
            case.setProperties(cCaseInfo)

    def setAttributes(self, attributes: list):
        self.attributes = attributes
        for case in self.case_list:
            case.setAttributes(self.attributes)

    def getUsingDeviceCount(self) -> int:
        cnt = 0
        for case in self.case_list:
            cnt += case.icon_choose.getUsingDeviceCount()
        return cnt
