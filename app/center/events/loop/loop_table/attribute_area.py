from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QGroupBox, QFormLayout, QLineEdit, QLabel


class AttributeArea(QGroupBox):
    nameChanged = pyqtSignal(QGroupBox)

    def __init__(self, name: str = "", value: str = ""):
        super(AttributeArea, self).__init__(None)
        # widget
        self.tip_label = QLabel()
        self.tip_label.setFixedHeight(18)
        self.tip_label.hide()
        self.name_line_edit = QLineEdit(name)
        self.name_line_edit.textEdited.connect(lambda text: self.nameChanged.emit(self))
        self.value_line_edit = QLineEdit(value)
        self.name_line_edit.setMinimumWidth(150)
        self.value_line_edit.setMinimumWidth(150)

        # layout
        layout = QFormLayout()
        layout.addRow(self.tip_label)
        layout.addRow("Variable Name: ", self.name_line_edit)
        layout.addRow("Default Value: ", self.value_line_edit)

        self.setLayout(layout)

    def name(self):
        """
        return its name
        """
        return self.name_line_edit.text()

    def value(self):
        """
        return its value
        """
        return self.value_line_edit.text()

    def __str__(self):
        return f"name: {self.name()}\tvalue: {self.value()}"

    def setNameChangeable(self, changeable: bool):
        """
        set value can be changed or not
        """
        self.name_line_edit.setEnabled(changeable)

    def setValueChangeable(self, changeable: bool):
        """
        set value can be changed or not
        """
        if changeable:
            self.value_line_edit.setText("")
            self.value_line_edit.setEnabled(True)
        else:
            self.value_line_edit.setText("You are not allowed to change the default variable")
            self.value_line_edit.setEnabled(False)

    def showTip(self, tip: str):
        self.tip_label.setText(f"""<span style="color: red; font-size:12px">
                                    {tip}
                                    </span>""")
        self.tip_label.show()
        self.name_line_edit.setStyleSheet("border: 1px solid rgb(199,84,80);color:rgb(199,84,80);")

    def hideTip(self):
        self.tip_label.hide()
        self.name_line_edit.setStyleSheet("border: 1px solid rgb(198,198,198);color:black;")
