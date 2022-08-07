from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QGroupBox, QGridLayout, QFormLayout, QVBoxLayout, QCompleter, QSizePolicy

from lib import ColComboBox, VarLineEdit, VarComboBox


class ArcGeneral(QWidget):
    def __init__(self, parent=None):
        super(ArcGeneral, self).__init__(parent)

        self.default_properties = {
            "Center X": "0",
            "Center Y": "0",
            "Width": "200",
            "Height": "200",
            "Angle Start": "0",
            "Angle Length": "270",
            "Border Color": "0,0,0",
            "Border Width": '1',
            "Fill Color": "0,0,0,0"
        }

        self.cx_pos = VarLineEdit("0")
        self.cy_pos = VarLineEdit("0")

        self._width = VarLineEdit("200")
        self._height = VarLineEdit("200")

        self.angle_start = VarComboBox()
        self.angle_start.addItems(("0", "90", "180", "270", "360"))
        self.angle_start.setEditable(True)
        self.angle_length = VarComboBox()
        self.angle_length.addItems(("0", "90", "180", "270", "360"))
        self.angle_length.setCurrentText("270")
        self.angle_length.setEditable(True)

        # down
        self.border_color = ColComboBox()
        self.border_color.setCurrentText("0,0,0")
        self.border_width = VarLineEdit("1")
        self.fill_color = ColComboBox()
        self.fill_color.addTransparent()
        self.setUI()

    def setUI(self):
        l00 = QLabel("Center X:")
        l01 = QLabel("Center Y:")
        l10 = QLabel("Width:")
        l11 = QLabel("Height:")
        l20 = QLabel("Start Angle (degrees):")
        l21 = QLabel("Angle Length (degrees):")
        l2 = QLabel("Border Color:")
        l3 = QLabel("Border Width:")
        l4 = QLabel("Fill Color:")

        l00.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l01.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l10.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l11.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l20.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l21.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        group1 = QGroupBox("Geometry")
        layout1 = QGridLayout()

        layout1.addWidget(l00, 0, 0)
        layout1.addWidget(self.cx_pos, 0, 1)
        layout1.addWidget(l01, 0, 2)
        layout1.addWidget(self.cy_pos, 0, 3)
        layout1.addWidget(l10, 1, 0)
        layout1.addWidget(self._width, 1, 1)
        layout1.addWidget(l11, 1, 2)
        layout1.addWidget(self._height, 1, 3)
        layout1.addWidget(l20, 2, 0)
        layout1.addWidget(self.angle_start, 2, 1)
        layout1.addWidget(l21, 2, 2)
        layout1.addWidget(self.angle_length, 2, 3)

        group1.setLayout(layout1)

        group2 = QGroupBox("Fill && Borderline")

        layout2 = QFormLayout()

        layout2.setRowWrapPolicy(QFormLayout.DontWrapRows)
        layout2.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
        layout2.setLabelAlignment(Qt.AlignLeft)

        self.border_color.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)
        self.fill_color.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)

        layout2.addRow(l2, self.border_color)
        layout2.addRow(l3, self.border_width)
        layout2.addRow(l4, self.fill_color)

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
        self.border_width.setCompleter(QCompleter(attributes))

    def updateInfo(self):
        self.default_properties['Center X'] = self.cx_pos.text()
        self.default_properties['Center Y'] = self.cy_pos.text()
        self.default_properties["Width"] = self._width.text()
        self.default_properties["Height"] = self._height.text()
        self.default_properties["Angle Start"] = self.angle_start.currentText()
        self.default_properties["Angle Length"] = self.angle_length.currentText()

        self.default_properties['Border Width'] = self.border_width.text()
        self.default_properties['Border Color'] = self.border_color.getRGB()
        self.default_properties['Fill Color'] = self.fill_color.getRGB()

    def setPosition(self, x, y):
        if not self.cx_pos.text().startswith("["):
            self.cx_pos.setText(str(int(x)))
        if not self.cy_pos.text().startswith("["):
            self.cy_pos.setText(str(int(y)))

    def setWh(self, w, h):
        if not self._width.text().startswith("["):
            self._width.setText(str(int(w)))
        if not self._height.text().startswith("["):
            self._height.setText(str(int(h)))
        # partial update the default_properties
        self.default_properties["Width"] = self._width.text()
        self.default_properties["Height"] = self._height.text()

    def setItemColor(self, rgb: str):
        if not self.fill_color.currentText().startswith("["):
            self.fill_color.setCurrentText(rgb)

    def setBorderColor(self, rgb: str):
        if not self.border_color.currentText().startswith("["):
            self.border_color.setCurrentText(rgb)

    def setBorderWidth(self, width: str):
        if not self.border_width.text().startswith("["):
            self.border_width.setText(width)

    # 加载参数设置
    def loadSetting(self):
        self.cx_pos.setText(self.default_properties["Center X"])
        self.cy_pos.setText(self.default_properties["Center Y"])
        self._width.setText(self.default_properties["Width"])
        self._height.setText(self.default_properties["Height"])
        self.angle_start.setCurrentText(self.default_properties["Angle Start"])
        self.angle_length.setCurrentText(self.default_properties["Angle Length"])

        self.border_color.setCurrentText(self.default_properties["Border Color"])
        self.border_width.setText(self.default_properties["Border Width"])
        self.fill_color.setCurrentText(self.default_properties["Fill Color"])
