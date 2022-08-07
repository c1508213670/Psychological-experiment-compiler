from PyQt5.QtWidgets import QWidget, QFormLayout, QComboBox

from app.func import Func
from lib import VarComboBox


# slider专属页面
class ComboGeneral(QWidget):
    def __init__(self, parent=None):
        super(ComboGeneral, self).__init__(parent)

        # 当前页面属性
        self.default_properties = {
            "Clear After": "Yes",
            "Screen Name": "screen_0"
        }

        self.clear_after = VarComboBox()
        self.clear_after.addItems(("clear_0", "notClear_1", "doNothing_2"))

        self.using_screen_id: str = "screen.0"
        self.screen_name = QComboBox()
        self.screen_info = Func.getDeviceInfo("screen")
        self.screen_name.addItems(self.screen_info.values())
        self.screen_name.currentTextChanged.connect(self.changeScreen)

        self.setUI()

    def setUI(self):
        layout = QFormLayout()
        layout.addRow("Screen Name:", self.screen_name)
        layout.addRow("Don't Clear After:", self.clear_after)

        self.setLayout(layout)

    def refresh(self):
        self.screen_info = Func.getDeviceInfo("screen")
        screen_id = self.using_screen_id
        self.screen_name.clear()
        self.screen_name.addItems(self.screen_info.values())
        screen_name = self.screen_info.get(screen_id)
        if screen_name:
            self.screen_name.setCurrentText(screen_name)
            self.using_screen_id = screen_id

    def setAttributes(self, attributes: list):
        pass

    def changeScreen(self, screen):
        for k, v in self.screen_info.items():
            if v == screen:
                self.using_screen_id = k
                break

    def updateInfo(self):
        self.default_properties["Clear After"] = self.clear_after.currentText()
        self.default_properties["Screen Name"] = self.screen_name.currentText()

    def getProperties(self):
        self.updateInfo()
        return self.default_properties

    def setProperties(self, properties: dict):
        self.default_properties.update(properties)
        self.loadSetting()

    def loadSetting(self):
        self.clear_after.setCurrentText(self.default_properties["Clear After"])
        self.screen_name.setCurrentText(self.default_properties["Screen Name"])
