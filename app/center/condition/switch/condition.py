from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QComboBox, QFormLayout, QCompleter

from lib import VarComboBox


class SwitchCondition(QWidget):
    def __init__(self, parent=None):
        super(SwitchCondition, self).__init__(parent)

        self.switch_choice = VarComboBox()
        self.switch_choice.setEditable(True)
        self.switch_choice.setInsertPolicy(QComboBox.NoInsert)
        self.switch_choice.currentTextChanged.connect(self.changeSwitch)
        self.vars: list = []
        self.current_var = ""
        self.setUI()

    def setUI(self):
        layout = QFormLayout()
        layout.addRow("Switch:", self.switch_choice)
        layout.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)

    def addSwitchValue(self, var_choice: list):
        cSwitchChoiceStr = self.switch_choice.currentText()

        self.vars = var_choice
        self.switch_choice.addItems(var_choice)

        self.switch_choice.setCurrentText(cSwitchChoiceStr)

    def changeSwitch(self, new_var):
        self.current_var = new_var

    def getProperties(self):
        return self.current_var

    def setProperties(self, new_var: str):
        self.switch_choice.setCurrentText(new_var)

    def setAttributes(self, attributes: list):
        cSwitchChoiceStr = self.switch_choice.currentText()

        self.switch_choice.addItems(attributes)
        self.switch_choice.setCompleter(QCompleter(attributes))

        self.switch_choice.setCurrentText(cSwitchChoiceStr)
