from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QFormLayout, QGroupBox, QGridLayout, QWidget, QLabel, \
    QCompleter

from lib import VarComboBox, VarLineEdit, ColComboBox


class FramePage(QWidget):
    def __init__(self, parent=None):
        super(FramePage, self).__init__(parent=parent)
        self.default_properties = {
            "Center X": "50%",
            "Center Y": "50%",
            "Width": "100%",
            "Height": "100%",
            "Enable": "Yes",
            "Border Color": "255,255,255",
            "Border Width": "0",
            "Frame Fill Color": "255,255,255",
            "Frame Transparent": "100%"
        }
        # up
        self.x_pos = VarComboBox(True)
        self.x_pos.addItems(("50%", "0%", "25%", "75%", "100%"))
        self.x_pos.setReg((VarComboBox.Percentage, VarComboBox.Integer))
        self.y_pos = VarComboBox(True)
        self.y_pos.addItems(("50%", "0%", "25%", "75%", "100%"))
        self.y_pos.setReg((VarComboBox.Percentage, VarComboBox.Integer))
        self.width = VarComboBox(True)
        self.width.addItems(("100%", "75%", "50%", "25%"))
        self.width.setReg((VarComboBox.Percentage, VarComboBox.Integer))
        self.height = VarComboBox(True)
        self.height.addItems(("100%", "75%", "50%", "25%"))
        self.height.setReg((VarComboBox.Percentage, VarComboBox.Integer))
        # down
        self.enable = VarComboBox()
        self.enable.currentTextChanged.connect(self.operationAble)
        self.border_color = ColComboBox()
        self.border_width = VarLineEdit("0")
        self.border_width.setRegularExpress(VarComboBox.Integer)
        self.back_color = ColComboBox()
        self.transparent = VarLineEdit("100%")
        self.transparent.setRegularExpress(VarComboBox.Percentage)
        self.enable.addItems(("No", "Yes"))
        self.enable.setAcceptDrops(False)
        self.setUI()

    # 生成frame页面
    def setUI(self):
        l1 = QLabel("Center X:")
        l2 = QLabel("Center Y:")
        l3 = QLabel("Width:")
        l4 = QLabel("Height:")
        l45 = QLabel("Enable:")
        l5 = QLabel("Border Color:")
        l6 = QLabel("Border Width:")
        l7 = QLabel("Background Color:")
        l8 = QLabel("Transparency:")
        l1.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l2.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l3.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l4.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l45.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l5.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l6.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l7.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l8.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        group1 = QGroupBox("Geometry")
        layout1 = QGridLayout()
        layout1.addWidget(l1, 0, 0)
        layout1.addWidget(self.x_pos, 0, 1)
        layout1.addWidget(l2, 0, 2)
        layout1.addWidget(self.y_pos, 0, 3)

        layout1.addWidget(l3, 1, 0)
        layout1.addWidget(self.width, 1, 1)
        layout1.addWidget(l4, 1, 2)
        layout1.addWidget(self.height, 1, 3)
        group1.setLayout(layout1)

        group2 = QGroupBox("Border && Background")
        layout2 = QFormLayout()

        layout2.addRow(l45, self.enable)
        layout2.addRow(l5, self.border_color)
        layout2.addRow(l6, self.border_width)
        layout2.addRow(l7, self.back_color)
        layout2.addRow(l8, self.transparent)
        layout2.setVerticalSpacing(20)
        group2.setLayout(layout2)

        layout = QVBoxLayout()
        layout.addWidget(group1)
        layout.addWidget(group2)
        self.setLayout(layout)

    def operationAble(self, signal):
        self.border_color.setEnabled(signal == "Yes")
        self.border_width.setEnabled(signal == "Yes")
        self.back_color.setEnabled(signal == "Yes")
        self.transparent.setEnabled(signal == "Yes")

    # 设置可选属性
    def setAttributes(self, attributes):
        self.x_pos.setCompleter(QCompleter(attributes))
        self.y_pos.setCompleter(QCompleter(attributes))
        self.width.setCompleter(QCompleter(attributes))
        self.height.setCompleter(QCompleter(attributes))
        self.transparent.setCompleter(QCompleter(attributes))
        self.back_color.setCompleter(QCompleter(attributes))
        self.border_color.setCompleter(QCompleter(attributes))
        self.border_width.setCompleter(QCompleter(attributes))

    def updateInfo(self):
        x_pos = self.x_pos.currentText()
        y_pos = self.y_pos.currentText()
        width = self.width.currentText()
        height = self.height.currentText()
        if x_pos:
            self.default_properties["Center X"] = x_pos
        else:
            self.default_properties["Center X"] = "50%"
            self.x_pos.setCurrentText("50%")
        if y_pos:
            self.default_properties["Center Y"] = y_pos
        else:
            self.default_properties["Center Y"] = "50%"
            self.y_pos.setCurrentText("50%")
        if width:
            self.default_properties["Width"] = self.width.currentText()
        else:
            self.default_properties["Width"] = "100%"
            self.width.setCurrentText("100%")
        if height:
            self.default_properties["Height"] = self.height.currentText()
        else:
            self.default_properties["Height"] = "100%"
            self.height.setCurrentText("100%")

        self.default_properties["Enable"] = self.enable.currentText()
        self.default_properties["Border Color"] = self.border_color.getRGB()
        self.default_properties["Border Width"] = self.border_width.text()
        self.default_properties["Frame Fill Color"] = self.back_color.getRGB()
        self.default_properties["Frame Transparent"] = self.transparent.text()

    def getProperties(self):
        return self.default_properties

    def setProperties(self, properties: dict):
        self.default_properties.update(properties)
        self.loadSetting()

    # 加载参数设置
    def loadSetting(self):
        self.x_pos.setCurrentText(self.default_properties["Center X"])
        self.y_pos.setCurrentText(self.default_properties["Center Y"])
        self.width.setCurrentText(self.default_properties["Width"])
        self.height.setCurrentText(self.default_properties["Height"])
        self.enable.setCurrentText(self.default_properties["Enable"])
        self.border_color.setCurrentText(self.default_properties["Border Color"])
        self.border_width.setText(self.default_properties["Border Width"])
        self.back_color.setCurrentText(self.default_properties["Frame Fill Color"])
        self.transparent.setText(self.default_properties["Frame Transparent"])
