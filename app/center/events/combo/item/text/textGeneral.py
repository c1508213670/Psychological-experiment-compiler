from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGridLayout, QLabel, QGroupBox, QVBoxLayout, QWidget, QFontComboBox, QCompleter

from app.info import Info
from lib import VarComboBox, VarLineEdit, ColComboBox
from lib.var_font_combo_box import VarFontComboBox


class TextGeneral(QWidget):
    def __init__(self, parent=None):
        super(TextGeneral, self).__init__(parent)

        self.default_properties = {
            "Center X": "0",
            "Center Y": "0",
            "Fore Color": "0,0,0",
            "Back Color": "0,0,0,0",
            "Transparent": "100%",
            "Right To Left": "",
            "Font Family": "",
            "Font Size": "12",
            "Style": "normal_0",
        }

        self.left_x = VarLineEdit()
        self.left_x.setRegularExpress(VarLineEdit.Integer)
        self.top_y = VarLineEdit()
        self.top_y.setRegularExpress(VarLineEdit.Integer)

        self.fore_color = ColComboBox()
        self.fore_color.setCurrentText("Black")

        self.back_color = ColComboBox()
        self.back_color.addTransparent()
        self.back_color.setCurrentText("Transparent")

        self.transparent = VarLineEdit("100%")
        self.transparent.setRegularExpress(VarLineEdit.Percentage)

        self.font_box = VarFontComboBox()
        # self.font_box.setAcceptDrops(True)

        self.style_box = VarComboBox(True)
        self.style_box.addItems(
            ("normal_0", "bold_1", "italic_2", "underline_4", "outline_8", "overline_16", "condense_32", "extend_64"))
        self.style_box.setToolTip("! not all platform support all style. See detail by running \"Screen 'TextStyle?'\" in MATLAB.")
        self.font_size_box = VarComboBox(True)
        self.font_size_box.setReg(VarComboBox.Integer)
        for i in range(12, 72, 2):
            self.font_size_box.addItem(str(i))
            self.font_size_box.setCurrentText('12')

        self.right_to_left = VarComboBox()
        self.right_to_left.addItems(("No", "Yes"))

        self.setUI()

    def setUI(self):
        l00 = QLabel("Left X:")
        l01 = QLabel("Top  Y:")

        l10 = QLabel("Foreground Color:")
        l11 = QLabel("Background Color:")

        l20 = QLabel("Transparent:")
        l21 = QLabel("Right to Left:")

        l3 = QLabel("Font Family:")
        l40 = QLabel("Font Size:")
        l41 = QLabel("Style:")

        l00.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l10.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l01.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l11.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l20.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l3.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l41.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l40.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l21.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        group2 = QGroupBox("")
        layout2 = QGridLayout()
        layout2.addWidget(l00, 0, 0)
        layout2.addWidget(self.left_x, 0, 1)
        layout2.addWidget(l01, 0, 2)
        layout2.addWidget(self.top_y, 0, 3)

        layout2.addWidget(l10, 1, 0)
        layout2.addWidget(self.fore_color, 1, 1)
        layout2.addWidget(l11, 1, 2)
        layout2.addWidget(self.back_color, 1, 3)

        layout2.addWidget(l20, 2, 0)
        layout2.addWidget(self.transparent, 2, 1)

        layout2.addWidget(l21, 2, 2)
        layout2.addWidget(self.right_to_left, 2, 3)

        layout2.addWidget(l3, 3, 0)
        layout2.addWidget(self.font_box, 3, 1, 1, 3)

        layout2.addWidget(l40, 4, 0)
        layout2.addWidget(self.font_size_box, 4, 1)
        layout2.addWidget(l41, 4, 2)
        layout2.addWidget(self.style_box, 4, 3)

        group2.setLayout(layout2)
        layout = QVBoxLayout()
        layout.addWidget(group2, 1)
        self.setLayout(layout)

    def setAttributes(self, attributes):
        self.left_x.setCompleter(QCompleter(attributes))
        self.top_y.setCompleter(QCompleter(attributes))
        self.fore_color.setCompleter(QCompleter(attributes))
        self.back_color.setCompleter(QCompleter(attributes))
        self.transparent.setCompleter(QCompleter(attributes))
        self.font_size_box.setCompleter(QCompleter(attributes))
        self.style_box.setCompleter(QCompleter(attributes))

    def updateInfo(self):
        self.default_properties["Left X"] = self.left_x.text()
        self.default_properties["Top Y"] = self.top_y.text()
        self.default_properties["Fore Color"] = self.fore_color.getRGB()
        self.default_properties["Back Color"] = self.back_color.getRGB()
        self.default_properties["Transparent"] = self.transparent.text()
        self.default_properties["Right To Left"] = self.right_to_left.currentText()
        self.default_properties["Font Family"] = self.font_box.currentText()
        self.default_properties["Font Size"] = self.font_size_box.currentText()
        self.default_properties["Style"] = self.style_box.currentText()

    def setProperties(self, properties: dict):
        self.default_properties.update(properties)
        self.loadSetting()

    def setPosition(self, x, y):
        if not self.left_x.text().startswith("["):
            self.left_x.setText(str(int(x)))
        if not self.top_y.text().startswith("["):
            self.top_y.setText(str(int(y)))

    def loadSetting(self):
        self.left_x.setText(self.default_properties["Left X"])
        self.top_y.setText(self.default_properties["Top Y"])
        self.fore_color.setCurrentText(self.default_properties["Fore Color"])
        self.back_color.setCurrentText(self.default_properties["Back Color"])
        self.transparent.setText(self.default_properties["Transparent"])
        self.right_to_left.setCurrentText(self.default_properties["Right To Left"])
        self.font_box.setCurrentText(self.default_properties["Font Family"])
        self.font_size_box.setCurrentText(self.default_properties["Font Size"])
        self.style_box.setCurrentText(self.default_properties["Style"])

    def loadDefaultFontInfo(self):
        if Info.FONT_DEFAULT_PREF:
            if not self.back_color.getRGB().startswith('['):
                self.back_color.setCurrentText(Info.FONT_DEFAULT_PREF.get("Back Color Item", "0,0,0,0"))

            if not self.fore_color.getRGB().startswith('['):
                self.fore_color.setCurrentText(Info.FONT_DEFAULT_PREF.get("Fore Color", "0,0,0"))

            if not self.style_box.currentText().startswith('['):
                self.style_box.setCurrentText(Info.FONT_DEFAULT_PREF.get("Style", "normal_0"))

            if not self.font_size_box.currentText().startswith('['):
                self.font_size_box.setCurrentText(Info.FONT_DEFAULT_PREF.get("Font Size", "12"))

            if not self.font_box.currentText().startswith('['):
                self.font_box.setCurrentText(Info.FONT_DEFAULT_PREF.get("Font Family", Info.DEFAULT_FONT))

            self.updateInfo()