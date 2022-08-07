from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGridLayout, QLabel, QCompleter, QGroupBox, QVBoxLayout
from PyQt5.QtWidgets import (QWidget)

from lib import VarComboBox, VarLineEdit, ColComboBox


class GaborGeneral(QWidget):
    def __init__(self, parent=None):
        super(GaborGeneral, self).__init__(parent)
        self.attributes: list = []
        self.default_properties = {
            "Center X": "0",
            "Center Y": "0",
            "Width": "100",
            "Height": "100",
            "Spatial": "0.033",
            "Contrast": "1",
            "Phase": "0",
            "Orientation": "0",
            "Back Color": "128,128,128",
            "SDx": "30",
            "SDy": "30",
            "Rotation": "0",
            "Transparency": "100%"
        }
        # up
        self.cx_pos = VarLineEdit()
        self.cy_pos = VarLineEdit()
        self._width = VarComboBox()
        self._height = VarComboBox()
        self.spatial = VarComboBox()
        self.contrast = VarComboBox()
        self.phase = VarComboBox()
        self.orientation = VarComboBox()
        self.back_color = ColComboBox()
        self.sdx = VarComboBox()
        self.sdy = VarComboBox()
        self.rotation = VarComboBox()
        self.transparency = VarComboBox()
        self.setUI()

    # 生成frame页面
    def setUI(self):
        self._width.addItems(["50", "100", "200", "250", "300"])
        self._width.setEditable(True)
        self._width.setCurrentText("100")
        self._height.addItems(["50", "100", "200", "250", "300"])
        self._height.setEditable(True)
        self._height.setCurrentText("100")
        self.spatial.addItems(["0.01", "0.02", "0.04", "0.06", "0.08"])
        self.spatial.setEditable(True)
        self.spatial.setCurrentText("0.033")
        self.contrast.addItems(["0", "1", "0.2", "0.4", "0.6", "0.8"])
        self.contrast.setEditable(True)
        self.contrast.setCurrentText("1")
        self.phase.addItems(["0", "45", "90", "135", "180"])
        self.phase.setEditable(True)
        self.phase.setItemData(0, "-180 to 180, degrees", Qt.ToolTipRole)
        self.orientation.addItems(["0", "45", "90", "135", "180"])
        self.orientation.setEditable(True)
        self.sdx.addItems(["30", "40", "60", "80"])
        self.sdx.setEditable(True)
        self.sdy.addItems(["30", "40", "60", "80"])
        self.sdy.setEditable(True)
        self.rotation.addItems(["0", "45", "90", "135", "180"])
        self.rotation.setEditable(True)
        self.rotation.setItemData(0,"0 to 180, degrees",Qt.ToolTipRole)
        self.transparency.addItems(["0%", "25%", "50%", "75%","100%"])
        self.transparency.setEditable(True)
        self.transparency.setCurrentText("100%")
        self.back_color.setCurrentText("128,128,128")
        self.back_color.setEditable(True)

        l1 = QLabel("Center X:")
        l2 = QLabel("Center Y:")
        l3 = QLabel("Width:")
        l4 = QLabel("Height:")
        l5 = QLabel("Spatial Frequency (cpp):")
        l6 = QLabel("Contrast:")
        l7 = QLabel("Phase (degrees):")
        l8 = QLabel("Orientation (degrees):")
        _21 = QLabel("SDx (pixels):")
        _22 = QLabel("SDy (pixels):")
        _23 = QLabel("Background Color:")
        _24 = QLabel("Rotation (degrees):")
        _25 = QLabel("Transparency:")

        l1.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l2.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l3.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l4.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l5.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l6.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l7.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l8.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        _21.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        _22.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        _23.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        _24.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        _25.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

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
        layout2.addWidget(self.spatial, 0, 1)
        layout2.addWidget(l6, 0, 2)
        layout2.addWidget(self.contrast, 0, 3)
        layout2.addWidget(l7, 1, 0)
        layout2.addWidget(self.phase, 1, 1)
        layout2.addWidget(l8, 1, 2)
        layout2.addWidget(self.orientation, 1, 3)

        layout2.addWidget(_23, 2, 0)
        layout2.addWidget(self.back_color, 2, 1)
        layout2.addWidget(_24, 2, 2)
        layout2.addWidget(self.rotation, 2, 3)

        layout2.addWidget(_21, 3, 0)
        layout2.addWidget(self.sdx, 3, 1)
        layout2.addWidget(_22, 3, 2)
        layout2.addWidget(self.sdy, 3, 3)
        layout2.addWidget(_25, 4, 0)
        layout2.addWidget(self.transparency, 4, 1)

        # self.setLayout(layout2)
        group2.setLayout(layout2)

        layout = QVBoxLayout()
        layout.addWidget(group1)
        layout.addWidget(group2)
        self.setLayout(layout)

    # 设置可选属性
    def setAttributes(self, attributes):
        self.attributes = attributes
        self.cx_pos.setCompleter(QCompleter(self.attributes))
        self.cy_pos.setCompleter(QCompleter(self.attributes))
        self._width.setCompleter(QCompleter(self.attributes))
        self._height.setCompleter(QCompleter(self.attributes))
        self.spatial.setCompleter(QCompleter(self.attributes))
        self.contrast.setCompleter(QCompleter(self.attributes))
        self.phase.setCompleter(QCompleter(self.attributes))
        self.orientation.setCompleter(QCompleter(self.attributes))
        self.back_color.setCompleter(QCompleter(self.attributes))
        self.rotation.setCompleter(QCompleter(self.attributes))
        self.sdx.setCompleter(QCompleter(self.attributes))
        self.sdy.setCompleter(QCompleter(self.attributes))
        self.transparency.setCompleter(QCompleter(self.attributes))

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
        self.default_properties['Center X'] = self.cx_pos.text()
        self.default_properties['Center Y'] = self.cy_pos.text()
        self.default_properties['Width'] = self._width.currentText()
        self.default_properties['Height'] = self._height.currentText()
        self.default_properties['Spatial'] = self.spatial.currentText()
        self.default_properties['Contrast'] = self.contrast.currentText()
        self.default_properties['Phase'] = self.phase.currentText()
        self.default_properties['Orientation'] = self.orientation.currentText()
        self.default_properties['Back Color'] = self.back_color.getRGB()
        self.default_properties['SDx'] = self.sdx.currentText()
        self.default_properties['SDy'] = self.sdy.currentText()
        self.default_properties['Rotation'] = self.rotation.currentText()
        self.default_properties['Transparency'] = self.transparency.currentText()

    def setProperties(self, properties: dict):
        if isinstance(properties, dict):
            self.default_properties = properties
            self.loadSetting()

    # 加载参数设置
    def loadSetting(self):
        self.cx_pos.setText(self.default_properties["Center X"])
        self.cy_pos.setText(self.default_properties["Center Y"])
        self._width.setCurrentText(self.default_properties["Width"])
        self._height.setCurrentText(self.default_properties["Height"])

        self.spatial.setCurrentText(self.default_properties["Spatial"])
        self.contrast.setCurrentText(self.default_properties["Contrast"])
        self.phase.setCurrentText(self.default_properties["Phase"])
        self.orientation.setCurrentText(self.default_properties["Orientation"])

        self.back_color.setCurrentText(self.default_properties["Back Color"])
        self.sdx.setCurrentText(self.default_properties['SDx'])
        self.sdy.setCurrentText(self.default_properties['SDy'])
        self.rotation.setCurrentText(self.default_properties["Rotation"])
        self.transparency.setCurrentText(self.default_properties["Transparency"])
