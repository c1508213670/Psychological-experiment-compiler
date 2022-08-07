from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGridLayout, QLabel, QCompleter, QGroupBox, QVBoxLayout
from PyQt5.QtWidgets import QWidget

from lib import VarComboBox, VarLineEdit


class SnowGeneral(QWidget):
    def __init__(self, parent=None):
        super(SnowGeneral, self).__init__(parent)
        self.attributes = []
        self.type = type
        self.default_properties = {
            "Center X": "0",
            "Center Y": "0",
            "Width": "100",
            "Height": "100",
            "Scale": "1",
            "Rotation": "0",
            "Transparency": "0"
        }
        # up
        self.cx_pos = VarLineEdit()
        self.cy_pos = VarLineEdit()
        self._width = VarComboBox()
        self._height = VarComboBox()
        self.scale = VarComboBox()
        self.rotation = VarComboBox()
        self.transparency = VarComboBox()
        self.setUI()

    # 生成frame页面
    def setUI(self):
        self._width.addItems(["0", "25", "50", "75", "100"])
        self._width.setEditable(True)
        self._width.setCurrentText("100")
        self._height.addItems(["0", "25", "50", "75", "100"])
        self._height.setEditable(True)
        self._height.setCurrentText("100")
        self.rotation.addItems(["0", "45", "90", "135", "180"])
        self.rotation.setEditable(True)
        self.scale.addItems(["1", "2", "4", "6", "8"])
        self.scale.setEditable(True)
        self.scale.setCurrentText("8")
        self.transparency.addItems(["0%", "25%", "50%", "75%", "100%"])
        self.transparency.setEditable(True)
        self.transparency.setCurrentText("100%")

        l1 = QLabel("Center X:")
        l2 = QLabel("Center Y:")
        l3 = QLabel("Width:")
        l4 = QLabel("Height:")
        l5 = QLabel("Scale:")
        l6 = QLabel("Rotation (degrees):")
        l7 = QLabel("Transparency:")

        l1.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l2.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l3.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l4.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l5.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l6.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l7.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        group1 = QGroupBox("Geometry")
        layout1 = QGridLayout()
        layout1.addWidget(l1, 0, 0)
        layout1.addWidget(self.cx_pos, 0, 1)
        layout1.addWidget(l2, 0, 2)
        layout1.addWidget(self.cy_pos, 0, 3)
        layout1.addWidget(l3, 1, 0)
        layout1.addWidget(self._width, 1, 1)
        layout1.addWidget(l4, 1, 2)
        layout1.addWidget(self._height, 1, 3)

        group1.setLayout(layout1)

        group2 = QGroupBox("Effects")
        layout2 = QGridLayout()
        layout2.addWidget(l5, 0, 0)
        layout2.addWidget(self.scale, 0, 1)
        layout2.addWidget(l6, 0, 2)
        layout2.addWidget(self.rotation, 0, 3)
        layout2.addWidget(l7, 1, 0)
        layout2.addWidget(self.transparency, 1, 1)

        # self.setLayout(layout2)
        group2.setLayout(layout2)

        layout = QVBoxLayout()
        layout.addWidget(group1)
        layout.addWidget(group2)
        self.setLayout(layout)
    # 设置可选属性
    def setAttributes(self, attributes):
        self.cx_pos.setCompleter(QCompleter(attributes))
        self.cy_pos.setCompleter(QCompleter(attributes))
        self._width.setCompleter(QCompleter(attributes))
        self._height.setCompleter(QCompleter(attributes))
        self.scale.setCompleter(QCompleter(attributes))
        self.rotation.setCompleter(QCompleter(attributes))
        self.transparency.setCompleter(QCompleter(attributes))

    def setPosition(self, x, y):
        if not self.cx_pos.text().startswith("["):
            self.cx_pos.setText(str(int(x)))
        if not self.cy_pos.text().startswith("["):
            self.cy_pos.setText(str(int(y)))

    def setWh(self, w, h):
        if not self._width.currentText().startswith("["):
            self._width.setCurrentText(str(int(w)))
        if not self._height.currentText().startswith("["):
            self._height.setCurrentText(str(int(h)))

    def updateInfo(self):
        self.default_properties.clear()
        self.default_properties['Center X'] = self.cx_pos.text()
        self.default_properties['Center Y'] = self.cy_pos.text()
        self.default_properties['Width'] = self._width.currentText()
        self.default_properties['Height'] = self._height.currentText()
        self.default_properties['Scale'] = self.scale.currentText()
        self.default_properties['Rotation'] = self.rotation.currentText()
        self.default_properties['Transparency'] = self.transparency.currentText()

    def setProperties(self, properties: dict):
        self.default_properties.update(properties)
        self.loadSetting()

    # 加载参数设置
    def loadSetting(self):
        self.cx_pos.setText(self.default_properties["Center X"])
        self.cy_pos.setText(self.default_properties["Center Y"])
        self._width.setCurrentText(self.default_properties["Width"])
        self._height.setCurrentText(self.default_properties["Height"])
        self.scale.setCurrentText(self.default_properties["Scale"])
        self.rotation.setCurrentText(self.default_properties["Rotation"])
        self.transparency.setCurrentText(self.default_properties["Transparency"])
