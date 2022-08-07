from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFormLayout, QGroupBox, QGridLayout, QLabel, QCompleter
from PyQt5.QtWidgets import QWidget, QVBoxLayout

from lib import ColComboBox, VarLineEdit


class LineGeneral(QWidget):
    def __init__(self, parent=None):
        super(LineGeneral, self).__init__(parent=parent)
        self.attributes = []
        self.pLabels = []

        self.default_properties = {
            "X1": "0",
            "Y1": "0",
            "X2": "0",
            "Y2": "0",
            "Border Color": "0,0,0",
            "Border Width": '1',
        }
        # up
        self.x_pos1 = VarLineEdit()
        self.y_pos1 = VarLineEdit()
        self.x_pos2 = VarLineEdit()
        self.y_pos2 = VarLineEdit()

        # down
        self.border_color = ColComboBox()
        self.border_color.setCurrentText("0,0,0")
        self.border_width = VarLineEdit()
        self.border_width.setRegularExpress(r"\d+")
        self.border_width.setText("2")
        self.setUI()

    # 生成frame页面
    def setUI(self):
        l00 = QLabel("X1:")
        l01 = QLabel("Y1:")
        l10 = QLabel("X2:")
        l11 = QLabel("Y2:")

        l00.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l01.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l10.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l11.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        group1 = QGroupBox("Geometry")
        layout1 = QGridLayout()

        layout1.addWidget(l00, 0, 0)
        layout1.addWidget(self.x_pos1, 0, 1)
        layout1.addWidget(l01, 0, 2)
        layout1.addWidget(self.y_pos1, 0, 3)
        layout1.addWidget(l10, 1, 0)
        layout1.addWidget(self.x_pos2, 1, 1)
        layout1.addWidget(l11, 1, 2)
        layout1.addWidget(self.y_pos2, 1, 3)

        group1.setLayout(layout1)

        group2 = QGroupBox("Borderline")
        layout2 = QFormLayout()
        layout2.addRow("Border Color:", self.border_color)
        layout2.addRow("Border Width:", self.border_width)
        layout2.setLabelAlignment(Qt.AlignRight)

        layout2.setVerticalSpacing(20)
        group2.setLayout(layout2)

        layout = QVBoxLayout()
        layout.addWidget(group1)
        layout.addWidget(group2)
        self.setLayout(layout)

    # 设置可选属性
    def setAttributes(self, attributes):
        self.x_pos1.setCompleter(QCompleter(attributes))
        self.y_pos1.setCompleter(QCompleter(attributes))
        self.x_pos2.setCompleter(QCompleter(attributes))
        self.y_pos2.setCompleter(QCompleter(attributes))
        self.border_width.setCompleter(QCompleter(attributes))

    def setPosition(self, x1, y1, x2, y2):
        if not self.x_pos1.text().startswith("["):
            self.x_pos1.setText(str(int(x1)))

        if not self.y_pos1.text().startswith("["):
            self.y_pos1.setText(str(int(y1)))

        if not self.x_pos2.text().startswith("["):
            self.x_pos2.setText(str(int(x2)))

        if not self.y_pos2.text().startswith("["):
            self.y_pos2.setText(str(int(y2)))

    def updateInfo(self):
        self.default_properties.clear()
        self.default_properties['X1'] = self.x_pos1.text()
        self.default_properties['Y1'] = self.y_pos1.text()

        self.default_properties['X2'] = self.x_pos2.text()
        self.default_properties['Y2'] = self.y_pos2.text()

        self.default_properties['Border Color'] = self.border_color.getRGB()
        self.default_properties['Border Width'] = self.border_width.text()

    def setProperties(self, properties: dict):
        self.default_properties.update(properties)
        print(properties)
        self.loadSetting()

    def setLineColor(self, rgb: str):
        if not self.border_color.currentText().startswith("["):
            self.border_color.setCurrentText(rgb)

    def setLineWidth(self, width: str):
        if not self.border_width.text().startswith("["):
            self.border_width.setText(width)

    # 加载参数设置
    def loadSetting(self):
        self.x_pos1.setText(self.default_properties["X1"])
        self.y_pos1.setText(self.default_properties["Y1"])

        self.x_pos2.setText(self.default_properties["X2"])
        self.y_pos2.setText(self.default_properties["Y2"])

        self.border_color.setCurrentText(self.default_properties["Border Color"])
        self.border_width.setText(self.default_properties["Border Width"])
