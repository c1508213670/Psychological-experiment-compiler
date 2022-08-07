from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPalette
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFontComboBox, QGridLayout, QGroupBox, QPushButton

from app.center.events.combo.item import TextItem
from app.func import Func
from app.info import Info
from lib import VarComboBox, ColComboBox


class FontPref(QWidget):
    def __init__(self, parent=None):
        super(FontPref, self).__init__(parent=parent)

        self.default_properties = Info.FONT_DEFAULT_PREF

        self.default_properties.update({
            "Fore Color": "0,0,0",
            "Back Color": "255,255,255",
            "Back Color Item": "0,0,0,0",
            "Font Size": "12",
            "Style": "normal_0",
            "Font Family": "Times"
        })

        self.setWindowTitle("Font Default")
        self.setWindowModality(2)
        self.setWindowIcon(QIcon(Func.getImage("common/icon.png")))
        self.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint)

        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(QPalette.Background, Qt.white)
        self.setPalette(p)

        self.fore_color = ColComboBox()
        self.fore_color.setAcceptDrops(False)
        self.fore_color.setCurrentText("Black")
        # self.fore_color.colorChanged.connect(self.changeColor)

        self.back_color = ColComboBox()
        self.back_color.setAcceptDrops(False)
        # self.back_color.colorChanged.connect(self.changeColor)
        self.back_item_color = ColComboBox()
        self.back_item_color.setAcceptDrops(False)
        self.back_item_color.addTransparent()
        self.back_item_color.setCurrentText("Transparent")

        self.font_box = QFontComboBox()
        self.font_box.setAcceptDrops(False)
        # self.font_box.currentFontChanged.connect(self.changeFont)

        self.style_box = VarComboBox()
        self.style_box.setAcceptDrops(False)
        self.style_box.setEditable(True)
        self.style_box.addItems(
            ("normal_0", "bold_1", "italic_2", "underline_4", "outline_8", "overline_16", "condense_32", "extend_64"))
        self.style_box.setToolTip("! not all platform support all style. See detail by running \"Screen 'TextStyle?'\" in MATLAB.")
        # self.style_box.currentTextChanged.connect(self.changeFont)

        self.font_size_box = VarComboBox()
        self.font_size_box.setAcceptDrops(False)
        self.font_size_box.setReg(VarComboBox.Integer)
        self.font_size_box.setEditable(True)
        for i in range(12, 72, 2):
            self.font_size_box.addItem(str(i))

        # self.font_size_box.currentIndexChanged.connect(self.changeFont)
        # bottom
        self.ok_bt = QPushButton("OK")
        self.cancel_bt = QPushButton("Cancel")
        self.apply_bt = QPushButton("Apply")

        self.ok_bt.clicked.connect(self.ok)
        self.cancel_bt.clicked.connect(self.cancel)
        self.apply_bt.clicked.connect(self.apply)

        self.setUI()

    def setUI(self):

        l02 = QLabel("Foreground Color:")
        l12 = QLabel("Background Color:")
        l22 = QLabel("Background Color for Text in Scene:")

        l50 = QLabel("Font Family:")
        l52 = QLabel("Style:")
        l60 = QLabel("Font Size:")

        l02.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l12.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l22.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l50.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l52.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l60.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        group1 = QGroupBox("")
        layout1 = QGridLayout()

        layout1.addWidget(l02, 0, 2)
        layout1.addWidget(self.fore_color, 0, 3)
        layout1.addWidget(l12, 1, 2)
        layout1.addWidget(self.back_color, 1, 3)
        layout1.addWidget(l22, 2, 2)
        layout1.addWidget(self.back_item_color, 2, 3)

        layout1.addWidget(l50, 3, 0)
        layout1.addWidget(self.font_box, 3, 1, 1, 3)
        layout1.addWidget(l52, 4, 2)
        layout1.addWidget(self.style_box, 4, 3)
        layout1.addWidget(l60, 4, 0)
        layout1.addWidget(self.font_size_box, 4, 1)
        group1.setLayout(layout1)

        below_layout = QHBoxLayout()
        below_layout.addStretch(10)
        below_layout.addWidget(self.ok_bt, 1)
        below_layout.addWidget(self.cancel_bt, 1)
        below_layout.addWidget(self.apply_bt, 1)
        below_layout.setContentsMargins(0, 0, 0, 0)

        layout = QVBoxLayout()
        layout.addWidget(group1, 5)
        layout.addSpacing(1)
        layout.addLayout(below_layout, 1)
        layout.setSpacing(10)

        self.setLayout(layout)

    def ok(self):
        self.apply()
        # print(f"{self.default_properties}")
        self.close()

    def cancel(self):
        self.loadSetting()

    def apply(self):
        self.updateInfo()
        for wid, cWidget in Info.WID_WIDGET.items():
            # for event type of Text
            if Func.isWidgetType(wid, Info.TEXT):
                cWidget.loadDefaultFontInfo()

            # for text items in event type of Scene
            elif Func.isWidgetType(wid, Info.COMBO):
                for item in cWidget.scene.items():
                    if isinstance(item, TextItem):
                        item.loadDefaultFontInfo()

    def updateInfo(self):

        self.default_properties["Fore Color"] = self.fore_color.getRGB()
        self.default_properties["Back Color"] = self.back_color.getRGB()
        self.default_properties["Back Color Item"] = self.back_item_color.getRGB()

        self.default_properties["Font Family"] = self.font_box.currentText()
        self.default_properties["Font Size"] = self.font_size_box.currentText()
        self.default_properties["Style"] = self.style_box.currentText()

    def loadSetting(self):

        self.fore_color.setCurrentText(self.default_properties["Fore Color"])
        self.back_color.setCurrentText(self.default_properties["Back Color"])
        self.back_item_color.setCurrentText(self.default_properties["Back Color Item"])

        self.font_box.setCurrentText(self.default_properties["Font Family"])
        self.font_size_box.setCurrentText(self.default_properties["Font Size"])
        self.style_box.setCurrentText(self.default_properties["Style"])
