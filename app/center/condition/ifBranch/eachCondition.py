from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QComboBox, QFrame, QHBoxLayout, QCompleter

from lib import VarComboBox, VarLineEdit
from ..addDeleteButton import AddDeleteButton


class EachCondition(QFrame):
    placeholder_width = 100

    def __init__(self, parent=None):
        super(EachCondition, self).__init__(parent)

        self.vars: list = []

        self.default_properties: dict = {
            "Op": "and",
            "Var": "",
            "Compare": "=",
            "Var Value": ""
        }

        self.op = VarComboBox()
        self.op.addItems(('and', 'or', 'xor', 'nor', 'nand', 'xnor'))
        self.op.setFixedWidth(EachCondition.placeholder_width)

        self.var = VarComboBox()
        self.var.setEditable(True)
        self.var.setInsertPolicy(QComboBox.NoInsert)

        self.compare = VarComboBox()
        self.compare.addItems(("=", ">", ">=", "<", "<=", "≠"))
        self.compare.setFixedWidth(EachCondition.placeholder_width)

        self.var_value = VarLineEdit()

        self.add_bt = AddDeleteButton(button_type='add')
        self.del_bt = AddDeleteButton(button_type='delete')

    def addVar(self, var_choice: list):
        cVarStr = self.var.currentText()

        self.vars = var_choice
        self.var.addItems(var_choice)

        self.var.setCurrentText(cVarStr)

    def getLayout(self):
        layout = QHBoxLayout()
        layout.addWidget(self.op, 1, Qt.AlignVCenter)
        layout.addWidget(self.var, 4, Qt.AlignVCenter)
        layout.addWidget(self.compare, 1, Qt.AlignVCenter)
        layout.addWidget(self.var_value, 4, Qt.AlignVCenter)
        layout.addWidget(self.add_bt, 1, Qt.AlignVCenter)
        layout.addWidget(self.del_bt, 1, Qt.AlignVCenter)
        return layout

    def getInfo(self):
        self.default_properties.clear()
        if isinstance(self.op, QComboBox):
            self.default_properties["Op"] = self.op.currentText()
        else:
            self.default_properties["Op"] = ""
        self.default_properties["Var"] = self.var.currentText()
        self.default_properties["Compare"] = self.compare.currentText()
        self.default_properties["Var Value"] = self.var_value.text()
        return self.default_properties

    def loadSetting(self):
        if isinstance(self.op, QComboBox):
            self.op.setCurrentText(self.default_properties.get("Op", "and"))
        self.var.setCurrentText(self.default_properties.get("Var", ""))

        self.compare.setCurrentText(self.default_properties.get("Compare", ">"))
        self.var_value.setText(self.default_properties.get("Var Value", ""))

    def setProperties(self, properties: dict):
        if properties:
            self.default_properties = properties.copy()
            self.loadSetting()

    def setAttributes(self, attributes: list):

        self.addVar(attributes)
        self.var.setCompleter(QCompleter(attributes))
        self.var_value.setCompleter(QCompleter(attributes))

    def getCondition(self) -> str:
        """
        e.g. and ([var] == "var value")
        :return:
        """
        return f"{self.default_properties.get('Op', '')} ({self.default_properties.get('Var', '')}" \
               f"{self.default_properties.get('Compare', '=')}{self.default_properties.get('Var Value')})"
