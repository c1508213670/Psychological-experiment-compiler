from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGridLayout, QLabel, QGroupBox, QVBoxLayout, QWidget, QPushButton, QCheckBox, \
    QFileDialog, QCompleter

from app.func import Func
from lib import VarLineEdit, VarComboBox


# image event专属页面
class ImageGeneral(QWidget):
    def __init__(self, parent=None):
        super(ImageGeneral, self).__init__(parent)

        # 当前页面属性
        self.default_properties = {
            "File Name": "",
            "Mirror Up/Down": False,
            "Mirror Left/Right": False,
            "Rotate": "0",
            "Stretch": False,
            "Stretch Mode": "Both",
            "Back Color": "255,255,255",
            "Transparent": "100%",
            "Center X": "50%",
            "Center Y": "50%",
            "Width": "100%",
            "Height": "100%",
        }
        # 打开文件
        self.file_name = VarLineEdit()

        self.open_bt = QPushButton("Open file")
        self.open_bt.clicked.connect(self.openFile)

        # 镜像模式
        self.mirrorUD = QCheckBox("Mirror up/down")
        self.mirrorLR = QCheckBox("Mirror left/right")

        # Rotate
        self.rotate = VarComboBox(True)
        self.rotate.addItems(("0", "90", "180", "270", "360"))
        self.rotate.setReg(VarComboBox.Integer)
        self.rotate.setItemData(0,"0 to 360 degrees",Qt.ToolTipRole)
        # 拉伸模式
        self.stretch = QCheckBox("Stretching")
        self.stretch_mode = VarComboBox()
        self.stretch_mode.addItems(("Both", "Horizontal", "Vertical"))

        # 背景色、透明度
        self.transparent = VarComboBox(True)
        self.transparent.addItems(("0%", "25%", "50%", "75%", "100%"))
        self.transparent.setCurrentText("100%")
        self.transparent.setReg(VarComboBox.Percentage)

        self.x_pos = VarLineEdit()
        # self.x_pos.setRegularExpress(VarLineEdit.Integer)
        self.y_pos = VarLineEdit()
        # self.y_pos.setRegularExpress(VarLineEdit.Integer)
        self._width = VarComboBox(True)
        self._width.addItems(("25%", "50%", "75%", "100%"))
        self._width.setCurrentText("100%")
        self._width.setReg(r"\d+%?")
        self._height = VarComboBox(True)
        self._height.addItems(("25%", "50%", "75%", "100%"))
        self._height.setCurrentText("100%")
        self._height.setReg(r"\d+%?")

        self.setGeneral()

    def setGeneral(self):
        # 打开文件按钮布局
        group1 = QGroupBox("File")

        layout1 = QGridLayout()
        layout1.addWidget(QLabel("File Name"), 0, 0, 1, 1)
        layout1.addWidget(self.file_name, 0, 1, 1, 4)
        layout1.addWidget(self.open_bt, 0, 5, 1, 1)

        self.stretch.stateChanged.connect(self.stretchChecked)
        self.stretch_mode.setEnabled(False)
        layout1.addWidget(self.mirrorUD, 1, 0)
        layout1.setColumnMinimumWidth(1, 40)

        layout1.addWidget(self.mirrorLR, 2, 0)
        l0 = QLabel("Rotate (0 to 360 in degrees):")
        l0.setAlignment(Qt.AlignRight | Qt.AlignVCenter)


        layout1.addWidget(l0, 1, 2)
        layout1.addWidget(self.rotate, 1, 3, 1, 2)

        l_tra = QLabel("Transparency:")
        l_tra.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        layout1.addWidget(l_tra, 2, 2)
        layout1.addWidget(self.transparent, 2, 3, 1, 2)
        layout1.addWidget(self.stretch, 3, 0)
        layout1.addWidget(self.stretch_mode, 3, 2)
        group1.setLayout(layout1)

        group2 = QGroupBox("Geometry")
        layout2 = QGridLayout()
        layout2.setVerticalSpacing(10)

        l_x_pos = QLabel("Center X:")
        l_y_pos = QLabel("Center Y:")
        l_width = QLabel("Maximum Width:")
        l_height = QLabel("Maximum Height:")

        l_x_pos.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l_y_pos.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l_width.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l_height.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        layout2.addWidget(l_x_pos, 0, 0)
        layout2.addWidget(self.x_pos, 0, 1)
        layout2.addWidget(l_y_pos, 0, 2)
        layout2.addWidget(self.y_pos, 0, 3)

        layout2.addWidget(l_width, 1, 0)
        layout2.addWidget(self._width, 1, 1)
        layout2.addWidget(l_height, 1, 2)
        layout2.addWidget(self._height, 1, 3)
        group2.setLayout(layout2)

        layout = QVBoxLayout()
        layout.addWidget(group1)
        layout.addWidget(group2)
        self.setLayout(layout)

    # 打开文件夹
    def openFile(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Find the image file", Func.getFullFilePath(self.file_name.text()),
                                                   "Image File (*.bmp;*.jpeg;*.jpg;*.png)", options=options)
        file_name = Func.getRelativeFilePath(file_name)
        if file_name:
            self.file_name.setText(file_name)

    def stretchChecked(self, e):
        if e == 2:
            self.stretch_mode.setEnabled(True)
        else:
            self.stretch_mode.setEnabled(False)

    def setAttributes(self, attributes):
        self.file_name.setCompleter(QCompleter(attributes))
        self.rotate.setCompleter(QCompleter(attributes))
        self.transparent.setCompleter(QCompleter(attributes))
        self.x_pos.setCompleter(QCompleter(attributes))
        self.y_pos.setCompleter(QCompleter(attributes))
        self._width.setCompleter(QCompleter(attributes))
        self._height.setCompleter(QCompleter(attributes))

    def updateInfo(self):
        """
        历史遗留函数
        :return:
        """
        self.default_properties["File Name"] = self.file_name.text()
        self.default_properties["Mirror Up/Down"] = bool(self.mirrorUD.checkState())
        self.default_properties["Mirror Left/Right"] = bool(self.mirrorLR.checkState())
        self.default_properties["Rotate"] = self.rotate.currentText()
        self.default_properties["Stretch"] = bool(self.stretch.checkState())
        self.default_properties["Stretch Mode"] = self.stretch_mode.currentText()
        self.default_properties["Transparent"] = self.transparent.currentText()
        self.default_properties["Center X"] = self.x_pos.text()
        self.default_properties["Center Y"] = self.y_pos.text()
        self.default_properties["Width"] = self._width.currentText()
        self.default_properties["Height"] = self._height.currentText()

    def setProperties(self, properties: dict):
        self.default_properties.update(properties)
        self.loadSetting()

    def setPosition(self, x, y):
        if not self.x_pos.text().startswith("["):
            self.x_pos.setText(str(int(x)))
        if not self.y_pos.text().startswith("["):
            self.y_pos.setText(str(int(y)))

    def loadSetting(self):
        self.file_name.setText(self.default_properties["File Name"])
        self.mirrorUD.setChecked(self.default_properties["Mirror Up/Down"])
        self.mirrorLR.setChecked(self.default_properties["Mirror Left/Right"])
        self.rotate.setCurrentText(self.default_properties["Rotate"])
        self.stretch.setChecked(self.default_properties["Stretch"])
        self.stretch_mode.setCurrentText(self.default_properties["Stretch Mode"])
        self.transparent.setCurrentText(self.default_properties["Transparent"])
        self.x_pos.setText(self.default_properties["Center X"])
        self.y_pos.setText(self.default_properties["Center Y"])
        self._width.setCurrentText(self.default_properties["Width"])
        self._height.setCurrentText(self.default_properties["Height"])
