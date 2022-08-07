import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QGroupBox, QGridLayout, QVBoxLayout, QFormLayout, QHBoxLayout, \
    QCompleter, QSizePolicy

from lib import VarLineEdit, ColComboBox


class Point:
    def __init__(self, x_l, y_l, x="0", y="0"):
        self.x_label = QLabel(x_l)
        self.y_label = QLabel(y_l)
        self.x_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.y_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.x = VarLineEdit(x)
        self.x.setRegularExpress(VarLineEdit.Integer)
        self.y = VarLineEdit(y)
        self.y.setRegularExpress(VarLineEdit.Integer)

    def getX(self):
        return self.x.text()

    def getY(self):
        return self.y.text()

    def set(self, x, y):
        self.x.setText(str(x))
        self.y.setText(str(y))

    def setAttributes(self, attributes):
        self.x.setCompleter(QCompleter(attributes))
        self.y.setCompleter(QCompleter(attributes))


class PolygonGeneral(QWidget):
    def __init__(self, parent=None):
        super(PolygonGeneral, self).__init__(parent)
        self.attributes = []
        self.default_properties = {
            "Center X": 0,
            "Center Y": 0,
            "Points": [],
            "Border Color": "0,0,0",
            "Border Width": '1',
            "Fill Color": "0,0,0,0"
        }

        # 圆心
        self.cx_pos: int = 0
        self.cy_pos: int = 0

        self.scene_w: int = 0
        self.scene_h: int = 0

        self.p1 = Point("X1:", "Y1:")
        self.p2 = Point("X2:", "Y2:")
        self.p3 = Point("X3:", "Y3:")

        self.points: list = [self.p1, self.p2, self.p3]

        self.add_bt = QPushButton("+")
        self.add_bt.clicked.connect(self.addPoint)
        self.del_bt = QPushButton("-")
        self.del_bt.clicked.connect(self.delPoint)
        self.del_bt.setEnabled(False)
        # down
        self.border_color = ColComboBox()
        self.border_color.setCurrentText("0,0,0")
        self.border_width = VarLineEdit("1")
        self.fill_color = ColComboBox()
        self.fill_color.addTransparent()
        self.setUI()

    def addPoint(self):
        point_index = len(self.points) + 1
        point = Point(f"X{point_index}:", f"Y{point_index}:")
        point.setAttributes(self.attributes)
        self.points.append(point)

        # 给顶点赋值
        for i, p in enumerate(self.points):
            p: Point
            new_x = str(self.cx_pos + int(100 * np.cos(np.pi / 2 - i * 2 * np.pi / point_index)))
            new_y = str(self.cy_pos + int(100 * np.sin(i * 2 * np.pi / point_index - np.pi / 2)))
            p.set(new_x, new_y)

        self.point_layout.addWidget(point.x_label, point_index, 0)
        self.point_layout.addWidget(point.x, point_index, 1)
        self.point_layout.addWidget(point.y_label, point_index, 2)
        self.point_layout.addWidget(point.y, point_index, 3)

        self.del_bt.setEnabled(point_index > 3)
        self.add_bt.setEnabled(point_index <= 20)

    def delPoint(self):
        point = self.points.pop(-1)
        point.x_label.deleteLater()
        point.y_label.deleteLater()
        point.x.deleteLater()
        point.y.deleteLater()

        n = len(self.points)
        for i, p in enumerate(self.points):
            p: Point
            new_x = str(self.cx_pos + int(100 * np.cos(np.pi / 2 - i * 2 * np.pi / n)))
            new_y = str(self.cy_pos + int(100 * np.sin(i * 2 * np.pi / n - np.pi / 2)))
            p.set(new_x, new_y)

        self.del_bt.setEnabled(n > 3)
        self.add_bt.setEnabled(n < 20)

    # 生成frame页面
    def setUI(self):
        l1 = QLabel("Border Color:")
        l2 = QLabel("Border Width:")
        l3 = QLabel("Fill Color:")
        l1.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l2.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l3.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        group1 = QGroupBox("Geometry")

        self.point_layout = QGridLayout()
        self.point_layout.addWidget(self.p1.x_label, 1, 0)
        self.point_layout.addWidget(self.p1.x, 1, 1)
        self.point_layout.addWidget(self.p1.y_label, 1, 2)
        self.point_layout.addWidget(self.p1.y, 1, 3)
        self.point_layout.addWidget(self.p2.x_label, 2, 0)
        self.point_layout.addWidget(self.p2.x, 2, 1)
        self.point_layout.addWidget(self.p2.y_label, 2, 2)
        self.point_layout.addWidget(self.p2.y, 2, 3)
        self.point_layout.addWidget(self.p3.x_label, 3, 0)
        self.point_layout.addWidget(self.p3.x, 3, 1)
        self.point_layout.addWidget(self.p3.y_label, 3, 2)
        self.point_layout.addWidget(self.p3.y, 3, 3)

        bt_layout = QHBoxLayout()
        bt_layout.addStretch(5)
        bt_layout.addWidget(self.add_bt)
        bt_layout.addWidget(self.del_bt)
        bt_layout.setAlignment(Qt.AlignBottom)

        up_layout = QVBoxLayout()
        up_layout.addLayout(self.point_layout, 10)
        up_layout.addLayout(bt_layout, 11)

        group1.setLayout(up_layout)

        group2 = QGroupBox("Fill && Borderline")
        layout2 = QFormLayout()
        layout2.setRowWrapPolicy(QFormLayout.DontWrapRows)
        layout2.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
        layout2.setLabelAlignment(Qt.AlignLeft)

        self.border_color.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)
        self.fill_color.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)

        layout2.addRow(l1, self.border_color)
        layout2.addRow(l2, self.border_width)
        layout2.addRow(l3, self.fill_color)
        group2.setLayout(layout2)

        layout = QVBoxLayout()
        layout.addWidget(group1)
        layout.addWidget(group2)
        self.setLayout(layout)

    # 设置可选属性
    def setAttributes(self, attributes: list):
        self.attributes = attributes
        self.p1.setAttributes(attributes)
        self.p2.setAttributes(attributes)
        self.p3.setAttributes(attributes)
        self.border_width.setCompleter(QCompleter(attributes))

    def updateInfo(self):
        self.default_properties['Center X'] = self.cx_pos
        self.default_properties['Center Y'] = self.cy_pos

        points: list = []
        for p in self.points:
            points.append((p.getX(), p.getY()))

        self.default_properties["Points"] = points

        self.default_properties['Border Width'] = self.border_width.text()
        self.default_properties['Border Color'] = self.border_color.getRGB()
        self.default_properties['Fill Color'] = self.fill_color.getRGB()

    def loadSetting(self):
        # 加载参数设置
        self.cx_pos = self.default_properties["Center X"]
        self.cy_pos = self.default_properties["Center Y"]

        l1 = len(self.points)
        l2 = len(self.default_properties["Points"])
        if l1 > l2:
            for i in range(l1 - l2):
                self.del_bt.click()
        else:
            for i in range(l2 - l1):
                self.add_bt.click()
        for i, j in zip(self.points, self.default_properties["Points"]):
            i.set(j[0], j[1])
        self.border_color.setCurrentText(self.default_properties["Border Color"])
        self.border_width.setText(self.default_properties["Border Width"])
        self.fill_color.setCurrentText(self.default_properties['Fill Color'])

    def setPosition(self, x, y):
        self.cx_pos = int(x)
        self.cy_pos = int(y)

    def setWh(self, w, h):
        pass

    def updateSceneWHInfo(self, w:int, h:int):
        self.scene_w = w
        self.scene_h = h

    def setVertex(self, points: list):
        for i, j in zip(self.points, points):
            if not i.x.text().startswith("["):
                i.x.setText(str(int(j[0])))
            if not i.y.text().startswith("["):
                i.y.setText(str(int(j[1])))

    def setItemColor(self, rgb: str):
        if not self.fill_color.currentText().startswith("["):
            self.fill_color.setCurrentText(rgb)

    def setLineColor(self, rgb: str):
        if not self.border_color.currentText().startswith("["):
            self.border_color.setCurrentText(rgb)

    def setBorderWidth(self, width: str):
        if not self.border_width.text().startswith("["):
            self.border_width.setText(width)

    def setBorderColor(self, rgb: str):
        if not self.border_width.text().startswith("["):
            self.border_color.setCurrentText(rgb)
