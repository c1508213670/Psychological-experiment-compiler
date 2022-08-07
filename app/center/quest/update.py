from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel, QPushButton, QLineEdit, QVBoxLayout, QHBoxLayout, QGridLayout, QCompleter, QComboBox

from app.func import Func
from lib import VarComboBox, TabItemWidget


class QuestUpdate(TabItemWidget):
    def __init__(self, widget_id: str, widget_name: str):
        super(QuestUpdate, self).__init__(widget_id, widget_name)

        self.tip1 = QLineEdit()
        self.tip2 = QLineEdit()
        self.tip1.setReadOnly(True)
        self.tip2.setReadOnly(True)

        self.default_properties = {
            "Is Correct": "1",
            "Quest Name": "",
        }
        self.response_variable = VarComboBox()
        self.response_variable.addItems(["1", "0"])
        self.response_variable.setEditable(True)

        self.quest_info = Func.getDeviceInfo("quest")

        if len(self.quest_info) > 1:
            self.quest_info.update({'quest_rand': 'quest_rand'})

        self.quest_name = QComboBox()
        self.quest_name.currentTextChanged.connect(self.changeQuestId)

        self.using_quest_id = ""

        self.bt_ok = QPushButton("OK")
        self.bt_ok.clicked.connect(self.ok)
        self.bt_cancel = QPushButton("Cancel")
        self.bt_cancel.clicked.connect(self.cancel)
        self.bt_apply = QPushButton("Apply")
        self.bt_apply.clicked.connect(self.apply)
        self.setUI()

        self.setAttributes(Func.getWidgetAttributes(self.widget_id))

    def changeQuestId(self, quest_name):
        for k, v in self.quest_info.items():
            if v == quest_name:
                self.using_quest_id = k
                break

    def setUI(self):
        self.setWindowTitle("Update")
        self.resize(500, 750)
        self.tip1.setStyleSheet("border-width:0;border-style:outset;background-color:transparent;")
        self.tip1.setText("Updating Quest")
        self.tip1.setFont(QFont("Times", 20, QFont.Bold))
        self.tip2.setStyleSheet("border-width:0;border-style:outset;background-color:transparent;")
        self.tip2.setText("Update the Quest test value based on a previous response")

        layout1 = QGridLayout()
        layout1.addWidget(self.tip1, 0, 0, 1, 4)
        layout1.addWidget(self.tip2, 1, 0, 1, 4)
        layout1.addWidget(QLabel("Was the Response Correct?"), 2, 0, 1, 1)
        layout1.addWidget(self.response_variable, 2, 1, 1, 1)
        layout1.addWidget(QLabel("Quest Name:"), 3, 0, 1, 1)
        layout1.addWidget(self.quest_name, 3, 1, 1, 1)

        layout2 = QHBoxLayout()
        layout2.addStretch(10)
        layout2.addWidget(self.bt_ok)
        layout2.addWidget(self.bt_cancel)
        layout2.addWidget(self.bt_apply)

        layout = QVBoxLayout()
        layout.addLayout(layout1)
        layout.addStretch(10)
        layout.addLayout(layout2)
        self.setLayout(layout)

    def ok(self):
        self.apply()
        self.close()
        self.tabClosed.emit(self.widget_id)

    def cancel(self):
        self.loadSetting()

    def refresh(self):
        self.quest_info = Func.getDeviceInfo("quest")
        if len(self.quest_info) > 1:
            self.quest_info.update({'quest_rand':'quest_rand'})

        quest_id = self.using_quest_id
        self.quest_name.clear()
        self.quest_name.addItems(self.quest_info.values())
        quest_name = self.quest_info.get(quest_id)

        if quest_name:
            self.quest_name.setCurrentText(quest_name)
            self.using_quest_id = quest_id

        attributes = Func.getWidgetAttributes(self.widget_id)
        self.setAttributes(attributes)
        self.updateInfo()

    def apply(self):
        self.updateInfo()
        self.propertiesChanged.emit(self.widget_id)

    def setAttributes(self, attributes):
        attributes = [f"[{attribute}]" for attribute in attributes]
        self.response_variable.setCompleter(QCompleter(attributes))

    def updateInfo(self):
        self.default_properties["Is Correct"] = self.response_variable.currentText()
        self.default_properties["Quest Name"] = self.quest_name.currentText()

    def setProperties(self, properties: dict):
        self.default_properties.update(properties)
        self.loadSetting()

    def loadSetting(self):
        self.response_variable.setCurrentText(self.default_properties["Is Correct"])
        self.quest_name.setCurrentText(self.default_properties["Quest Name"])

    def getProperties(self) -> dict:
        """
        get this widget's properties to show it in Properties Window.
        @return: a dict of properties
        """
        self.refresh()
        return self.default_properties

    def store(self):
        """
        return necessary data for restoring this widget.
        @return:
        """
        return self.default_properties

    def restore(self, properties: dict):
        self.setProperties(properties)

    def clone(self, new_widget_id: str, new_widget_name):
        clone_widget = QuestUpdate(new_widget_id, new_widget_name)
        clone_widget.setProperties(self.default_properties.copy())
        return clone_widget

    def getResponseVariable(self) -> str:
        return self.response_variable.currentText()

    def getQuestName(self) -> str:
        return self.quest_name.currentText()
