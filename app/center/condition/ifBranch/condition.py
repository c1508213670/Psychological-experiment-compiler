from PyQt5.QtWidgets import QFormLayout, QLabel, QWidget

from .eachCondition import EachCondition


class ConditionArea(QWidget):
    """
    properties:
    {
        "condition 0":  {
                            "op": "and",
                            "var": "",
                            "compare": ">",
                            "var value": ""
                            }
        "condition 1": ...
    }
    """
    MAX_CONDITION_COUNT = 6

    def __init__(self, parent=None):
        super(ConditionArea, self).__init__(parent)

        self.default_properties: dict = {
            "Condition 0": {
                "Op": "and",
                "Var": "",
                "Compare": ">",
                "var value": ""
            }
        }
        self.attributes: list = []

        self.default_condition = EachCondition()

        self.default_condition.op = QLabel()
        self.default_condition.op.setFixedWidth(100)
        self.default_condition.del_bt = QLabel()
        self.default_condition.del_bt.setFixedWidth(self.default_condition.add_bt.width())
        self.default_condition.add_bt.clicked.connect(self.addCondition)

        self.conditions = [self.default_condition]
        #
        self.form_layout = QFormLayout(self)
        self.form_layout.addRow(self.default_condition.getLayout())
        self.setLayout(self.form_layout)

    def addCondition(self):
        index = self.getButtonIndex(self.sender())
        if index != -1:

            new_condition = EachCondition()
            new_condition.setAttributes(self.attributes)
            new_condition.add_bt.clicked.connect(self.addCondition)
            new_condition.del_bt.clicked.connect(self.delCondition)

            self.form_layout.insertRow(index + 1, new_condition.getLayout())
            self.conditions.insert(index + 1, new_condition)
            if len(self.conditions) == ConditionArea.MAX_CONDITION_COUNT:
                for c in self.conditions:
                    c.add_bt.setDisabled(True)

    def delCondition(self):
        index = self.getButtonIndex(self.sender())
        if index != -1:
            self.conditions.pop(index)
            self.form_layout.removeRow(index)
            # 修改按钮状态
            if len(self.conditions) == ConditionArea.MAX_CONDITION_COUNT - 1:
                for c in self.conditions:
                    c.add_bt.setDisabled(False)

    def getButtonIndex(self, button):
        for i, v in enumerate(self.conditions):
            if button is v.add_bt or button is v.del_bt:
                return i
        return -1

    def updateInfo(self):
        self.default_properties.clear()
        for i, c in enumerate(self.conditions):
            self.default_properties[f"Condition {i}"] = c.getInfo()
        return self.default_properties

    def loadSetting(self):
        old_cnt = len(self.default_properties)
        new_cnt = len(self.conditions)
        if old_cnt > new_cnt:
            for i in range(old_cnt - new_cnt):
                a_condition = EachCondition()
                a_condition.add_bt.clicked.connect(self.addCondition)
                a_condition.del_bt.clicked.connect(self.delCondition)
                self.form_layout.addRow(a_condition.getLayout())
                self.conditions.append(a_condition)
        else:
            for i in range(new_cnt - 1, old_cnt - 1, -1):
                self.conditions.pop()
                self.form_layout.removeRow(i)

        for i, c in enumerate(self.conditions):
            c.setProperties(self.default_properties.get(f"Condition {i}", {}))


    def setProperties(self, properties: dict):
        self.default_properties.update(properties)
        self.loadSetting()

    def setAttributes(self, attributes: list):
        self.attributes = attributes
        for c in self.conditions:
            c.setAttributes(attributes)

    def getCondition(self) -> str:
        return "".join(condition.getCondition() for condition in self.conditions)
