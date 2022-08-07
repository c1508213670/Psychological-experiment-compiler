import re

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QScrollArea, QFormLayout, QHBoxLayout, QLabel, QPushButton, \
    QVBoxLayout

from lib import MessageBox, Dialog
from .attribute_area import AttributeArea


class AttributeDialog(Dialog):
    # when user add some attributes, emit signal (col)
    attributesAdded = pyqtSignal(int)
    # when user change attributes, emit signal (col, attribute_name, attribute_value)
    attributesChanged = pyqtSignal(int, str, str)

    def __init__(self, exist_attribute: dict):
        super(AttributeDialog, self).__init__(None)
        # data
        # bind through pointer
        self.exist_attribute = exist_attribute
        self.attribute_areas = []
        # if change == True, it means that change attribute
        self.change = False
        self.col = -1
        # title
        self.setWindowTitle("Add Variable(s)")
        self.setModal(True)
        # scroll area > container > some attribute areas
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        container = QWidget()
        # form layout to set attribute ares
        self.layout = QFormLayout()
        self.layout.addRow(QLabel("Set variable and default value."))
        self.addAttribute()
        container.setLayout(self.layout)
        scroll_area.setWidget(container)
        # buttons
        ok_button = QPushButton("Ok")
        ok_button.clicked.connect(self.ok)
        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.addAttribute)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.cancel)
        # buttons' layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(ok_button)
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(cancel_button)
        button_layout.setAlignment(Qt.AlignRight)
        button_layout.setSpacing(10)
        # vertical layout to set scroll area and buttons
        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(scroll_area)
        vertical_layout.addLayout(button_layout)
        self.setLayout(vertical_layout)

    def updateExistAttributes(self,newAttributes: dict):
        self.exist_attribute = newAttributes


    def addAttribute(self, checked=False, name="", value=""):
        """
        add new attribute area into widget
        """
        attribute_area = AttributeArea(name, value)
        attribute_area.nameChanged.connect(self.handleAttributeNameChanged)
        self.layout.insertRow(self.layout.rowCount(), attribute_area)
        self.attribute_areas.append(attribute_area)

    def ok(self):
        """
        click ok, and we check data
        """
        if not self.change:
            # add attribute
            new_attributes = set()
            for attribute_area in self.attribute_areas:
                name = attribute_area.name()
                if name:
                    if name in self.exist_attribute:
                        MessageBox.information(self, "warning", f"Variable {name} already exists.")
                        return
                    elif name in new_attributes:
                        MessageBox.information(self, "warning", f"Duplicate variable {name}.")
                        return
                    elif not re.match(r"^[a-zA-Z][a-zA-Z0-9_]*$", name):
                        MessageBox.information(self, "warning",
                                               "Name must start with a letter and contain only letters, numbers, and _.")
                        return
                    new_attributes.add(name)
            self.attributesAdded.emit(self.col)
        else:
            # change attribute
            attribute_area = self.attribute_areas[0]
            name = attribute_area.name()
            value = attribute_area.value()
            if name == "Repetitions" and not re.match(r"^\+?[1-9][0-9]*$", value):
                # if Repetitions, value must be positive number
                MessageBox.information(self, "warning", "Only positive number is enabled.")
                return
            self.attributesChanged.emit(self.col, name, value)
        self.close()

    def cancel(self):
        self.close()

    def showWindow(self, type: int, col: int = -1, attribute_name: str = "", attribute_value: str = ""):
        """
        add single or many
        type 0: single
             1: many
        """
        # hide or show add button
        self.add_button.hide()
        self.setMinimumHeight(180)
        self.setMinimumWidth(400)
        self.setWindowTitle("Add Variable")
        if type:
            self.setMinimumHeight(500)
            self.add_button.show()
            self.setWindowTitle("Add Variables")
        # clear attribute areas existed
        while self.layout.rowCount():
            self.layout.removeRow(0)
        # clear attribute_areas
        self.attribute_areas.clear()
        # add new one
        self.addAttribute(name=attribute_name, value=attribute_value)
        # if attribute != empty, it means that user want to change attribute
        # however, we don't allow user to change timeline' default value and repetitions's value must be positive num
        self.change = False
        if attribute_name:
            self.change = True
            self.setWindowTitle("Change Variable")
        self.col = col
        if self.col != -1:
            if attribute_name == "Timeline":
                self.attribute_areas[0].setNameChangeable(False)
                self.attribute_areas[0].setValueChangeable(False)
            if attribute_name == "Timeline" or attribute_name == "Repetitions":
                self.attribute_areas[0].setNameChangeable(False)
        self.show()

    def getAttributes(self) -> list:
        """
        return attributes and default values
        """
        attributes = []
        for attribute_area in self.attribute_areas:
            name = attribute_area.name()
            if name:
                # we ignore empty name
                value = attribute_area.value()
                attributes.append((name, value))
        return attributes

    def handleAttributeNameChanged(self, attribute_area: AttributeArea):
        """
        check validity of attribute's name on time.
        """
        # only pattern now
        name = attribute_area.name()
        if name and not re.match(r"^[a-zA-Z][a-zA-Z0-9_]*$", name):
            attribute_area.showTip("Variable name must start with a letter and contain only letters, numbers, _")
        else:
            attribute_area.hideTip()
