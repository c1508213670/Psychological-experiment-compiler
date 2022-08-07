from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QGroupBox, QGridLayout, QFormLayout, QVBoxLayout, QCompleter, QSizePolicy

from lib import ColComboBox, VarLineEdit, VarComboBox


class DotGeneral(QWidget):
    def __init__(self, parent=None):
        super(DotGeneral, self).__init__(parent)

        self.default_properties = {
            "Center X": "0",
            "Center Y": "0",
            "Width": "100",
            "Height": "100",
            "Is Oval": "yes",
            "Dot Num": "50",
            "Dot Type": "0",
            "Dot Size": "1",
            "Move Direction": "0",
            "Speed": "20",
            "Coherence": "100",
            "Dot Color": "0,0,0",

            "Fill Color": "0,0,0,0",
            "Border Color": "0,0,0,0",
            "Border Width": "0",
        }

        self.cx_pos = VarLineEdit("0")
        self.cy_pos = VarLineEdit("0")

        self._width = VarLineEdit("200")
        self._height = VarLineEdit("200")

        self.is_oval = VarComboBox()
        self.is_oval.addItems(("yes", "no"))

        self.dot_num = VarLineEdit("50")
        self.dot_type = VarComboBox()
        self.dot_type.addItems(("0", "1", "2", "3", "4"))
        self.dot_size = VarLineEdit("5")

        self.move_direction = VarLineEdit("0")
        self.move_direction.setRegularExpress(VarLineEdit.Float)
        self.move_direction.setToolTip("0 to 180 degrees")
        self.speed = VarLineEdit("20")
        self.speed.setRegularExpress(VarLineEdit.Float)

        self.dot_color = ColComboBox()
        self.dot_color.setCurrentText("0,0,0")

        self.coherence = VarLineEdit("100")
        self.coherence.setRegularExpress(VarLineEdit.Float)
        # down

        self.fill_color = ColComboBox()
        self.fill_color.addTransparent()
        self.border_color = ColComboBox()
        self.border_color.addTransparent()
        self.border_width = VarLineEdit("0")
        self.border_width.setRegularExpress(VarLineEdit.Integer)

        self.setUI()

    def setUI(self):
        l00 = QLabel("Center X:")
        l01 = QLabel("Center Y:")
        l10 = QLabel("Width:")
        l11 = QLabel("Height:")
        l20 = QLabel("Is Oval:")
        l21 = QLabel("Dot Num.:")
        l30 = QLabel("Dot Type:")
        l31 = QLabel("Dot Size:")
        l40 = QLabel("Direction (degrees):")
        l41 = QLabel("Speed (pixes/s):")
        l50 = QLabel("Dot Color:")
        l51 = QLabel("Coherence (%):")

        l6 = QLabel("Fill Color:")
        l7 = QLabel("Border Color:")
        l8 = QLabel("Border Width:")

        l00.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l01.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l10.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l11.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l20.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l21.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l30.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l31.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l40.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l41.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l50.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l51.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        l6.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l7.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l8.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

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
        layout1.addWidget(self.is_oval, 2, 1)
        layout1.addWidget(l21, 2, 2)
        layout1.addWidget(self.dot_num, 2, 3)
        layout1.addWidget(l30, 3, 0)
        layout1.addWidget(self.dot_type, 3, 1)
        layout1.addWidget(l31, 3, 2)
        layout1.addWidget(self.dot_size, 3, 3)
        layout1.addWidget(l40, 4, 0)
        layout1.addWidget(self.move_direction, 4, 1)
        layout1.addWidget(l41, 4, 2)
        layout1.addWidget(self.speed, 4, 3)
        layout1.addWidget(l50, 5, 0)
        layout1.addWidget(self.dot_color, 5, 1)
        layout1.addWidget(l51, 5, 2)
        layout1.addWidget(self.coherence, 5, 3)

        group1.setLayout(layout1)

        # group2 = QGroupBox("Fill && Frame")
        # layout2 = QFormLayout()
        # layout2.setRowWrapPolicy(QFormLayout.DontWrapRows)
        # layout2.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
        # layout2.setLabelAlignment(Qt.AlignLeft)
        #
        # self.fill_color.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)
        # self.border_color.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)
        #
        # layout2.addRow(l6, self.fill_color)
        # layout2.addRow(l7, self.border_color)
        # layout2.addRow(l8, self.border_width)
        # group2.setLayout(layout2)

        layout = QVBoxLayout()
        layout.addWidget(group1)
        # layout.addWidget(group2)
        self.setLayout(layout)

    # 设置可选属性
    def setAttributes(self, attributes):
        self.cx_pos.setCompleter(QCompleter(attributes))
        self.cy_pos.setCompleter(QCompleter(attributes))
        self._width.setCompleter(QCompleter(attributes))
        self._height.setCompleter(QCompleter(attributes))
        self.dot_num.setCompleter(QCompleter(attributes))
        self.dot_size.setCompleter(QCompleter(attributes))
        self.move_direction.setCompleter(QCompleter(attributes))
        self.speed.setCompleter(QCompleter(attributes))
        self.dot_color.setCompleter(QCompleter(attributes))
        self.coherence.setCompleter(QCompleter(attributes))
        # self.fill_color.setCompleter(QCompleter(attributes))
        # self.border_color.setCompleter(QCompleter(attributes))
        # self.border_width.setCompleter(QCompleter(attributes))

    def updateInfo(self):
        self.default_properties['Center X'] = self.cx_pos.text()
        self.default_properties['Center Y'] = self.cy_pos.text()
        self.default_properties["Width"] = self._width.text()
        self.default_properties["Height"] = self._height.text()
        self.default_properties["Is Oval"] = self.is_oval.currentText()
        self.default_properties["Dot Num"] = self.dot_num.text()
        self.default_properties["Dot Type"] = self.dot_type.currentText()
        self.default_properties["Dot Size"] = self.dot_size.text()
        self.default_properties['Move Direction'] = self.move_direction.text()
        self.default_properties['Speed'] = self.speed.text()
        self.default_properties['Dot Color'] = self.dot_color.getRGB()
        self.default_properties['Coherence'] = self.coherence.text()

        # self.default_properties['Fill Color'] = self.fill_color.getRGB()
        # self.default_properties["Border Color"] = self.border_color.getRGB()
        # self.default_properties["Border Width"] = self.border_width.text()

    def setProperties(self, properties: dict):
        self.default_properties.update(properties)
        self.loadSetting()

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

    # def setFillColor(self, rgb: str):
    #     if not self.fill_color.currentText().startswith("["):
    #         self.fill_color.setCurrentText(rgb)
    #
    # def setBorderColor(self, rgb: str):
    #     if not self.border_color.currentText().startswith("["):
    #         self.border_color.setCurrentText(rgb)
    #
    # def setBorderWidth(self, width: str):
    #     if not self.border_width.text().startswith("["):
    #         self.border_width.setText(width)

    # 加载参数设置
    def loadSetting(self):
        self.cx_pos.setText(self.default_properties["Center X"])
        self.cy_pos.setText(self.default_properties["Center Y"])
        self._width.setText(self.default_properties["Width"])
        self._height.setText(self.default_properties["Height"])

        self.is_oval.setCurrentText(self.default_properties["Is Oval"])
        self.dot_num.setText(self.default_properties["Dot Num"])
        self.dot_type.setCurrentText(self.default_properties["Dot Type"])
        self.dot_size.setText(self.default_properties["Dot Size"])
        self.move_direction.setText(self.default_properties["Move Direction"])
        self.speed.setText(self.default_properties["Speed"])

        self.dot_color.setCurrentText(self.default_properties["Dot Color"])
        self.coherence.setText(self.default_properties["Coherence"])

        # self.fill_color.setCurrentText(self.default_properties["Fill Color"])
        # self.border_color.setCurrentText(self.default_properties["Border Color"])
        # self.border_width.setText(self.default_properties["Border Width"])
