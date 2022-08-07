from PyQt5.QtCore import Qt, QIODevice, QDataStream
from PyQt5.QtGui import QColor, QFont, QDropEvent
from PyQt5.QtWidgets import QGridLayout, QLabel, QGroupBox, QVBoxLayout, QWidget, QTextEdit, \
    QFontComboBox, QCompleter, QComboBox

from app.info import Info
from lib.var_font_combo_box import VarFontComboBox
from .lighter import AttributeHighlighter
from .smart import SmartTextEdit
from app.func import Func
from lib import VarComboBox, VarLineEdit, ColComboBox


class TextTab1(QWidget):
    def __init__(self, parent=None):
        super(TextTab1, self).__init__(parent)

        self.default_properties = {
            "Html": "",
            "Text": "",
            "Alignment": "center",
            "Fore Color": "0,0,0",
            "Back Color": "255,255,255",
            "Screen Name": "screen_0",
            "Transparent": "100%",
            "Word Wrap": 0,
            "Clear After": "Yes"
        }

        self.text_edit = SmartTextEdit()
        self.text_edit.setLineWrapMode(QTextEdit.FixedColumnWidth)
        # self.setAcceptDrops(True)

        self.lighter = AttributeHighlighter(self.text_edit.document())

        self.align_mode = "center"

        self.align_x = VarComboBox()
        self.align_x.setEditable(True)
        self.align_x.currentTextChanged.connect(self.changeAlign)
        self.align_y = VarComboBox()
        self.align_y.setEditable(True)
        self.align_y.currentTextChanged.connect(self.changeAlign)

        self.fore_color = ColComboBox()
        self.back_color = ColComboBox()
        self.fore_color.setCurrentText("Black")
        self.fore_color.colorChanged.connect(self.changeColor)
        self.back_color.colorChanged.connect(self.changeColor)

        self.clear_after = VarComboBox()
        self.transparent = VarLineEdit("100%")
        self.transparent.setRegularExpress(VarLineEdit.Percentage)
        self.word_wrap = VarLineEdit("80")
        self.word_wrap.setRegularExpress(VarLineEdit.Integer)
        self.word_wrap.textChanged.connect(self.changeWrap)
        self.word_wrap.setToolTip("Maximal number of characters for each line")
        self.text_edit.setLineWrapColumnOrWidth(80)

        self.flip_horizontal = VarComboBox()
        self.flip_horizontal.addItems(("No", "Yes"))
        self.flip_vertical = VarComboBox()
        self.flip_vertical.addItems(("No", "Yes"))

        self.font_box = VarFontComboBox()
        # self.font_box.setAcceptDrops(True)

        self.font_box.currentFontChanged.connect(self.changeFont)
        self.font_box.currentTextChanged.connect(self.changeFont)


        self.style_box = VarComboBox()
        self.style_box.setEditable(True)
        self.style_box.addItems(
            ("normal_0", "bold_1", "italic_2", "underline_4", "outline_8", "overline_16", "condense_32", "extend_64"))
        self.style_box.currentTextChanged.connect(self.changeFont)

        self.font_size_box = VarComboBox()
        self.font_size_box.setReg(VarComboBox.Integer)
        self.font_size_box.setEditable(True)
        for i in range(12, 72, 2):
            self.font_size_box.addItem(str(i))

        # self.font_size_box.currentIndexChanged.connect(self.changeFont)
        self.font_size_box.currentTextChanged.connect(self.changeFont)

        self.right_to_left = VarComboBox()
        self.right_to_left.addItems(("No", "Yes"))

        self.using_screen_id: str = "screen.0"
        self.screen = QComboBox()
        self.screen_info = Func.getDeviceInfo("screen")
        self.screen.addItems(self.screen_info.values())
        self.screen.currentTextChanged.connect(self.changeScreen)

        self.setUI()
        self.setScrBackGroundColor()
        # self.loadDefaultFontInfo()
        # General UI to default_properties
        # self.updateInfo()

    def setUI(self):
        l0 = QLabel("Text:")

        l00 = QLabel("Alignment X:")
        l10 = QLabel("Alignment Y:")

        l02 = QLabel("Foreground Color:")
        l12 = QLabel("Background Color:")

        l20 = QLabel("Don't Clear After:")
        l22 = QLabel("Screen Name:")

        l30 = QLabel("Transparency:")
        l32 = QLabel("Wrapat Chars:")

        l40 = QLabel("Horizontal Flip:")
        l42 = QLabel("Vertical Flip:")

        l50 = QLabel("Font Family:")
        l52 = QLabel("Style:")
        l60 = QLabel("Font Size:")
        l70 = QLabel("Right to Left:")

        l0.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l00.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l02.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l10.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l12.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l20.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l22.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l30.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l32.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l40.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l42.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l50.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l52.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l60.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l70.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.align_x.addItems(("center", "left", "right", "justify"))
        self.align_y.addItem("center")

        self.clear_after.addItems(("clear_0", "notClear_1", "doNothing_2"))
        self.screen.addItem("screen_0")

        group1 = QGroupBox("Text")
        layout1 = QGridLayout()
        layout1.addWidget(self.text_edit, 0, 0)
        group1.setLayout(layout1)

        group2 = QGroupBox("")
        layout2 = QGridLayout()
        layout2.addWidget(l00, 0, 0)
        layout2.addWidget(self.align_x, 0, 1)
        layout2.addWidget(l10, 1, 0)
        layout2.addWidget(self.align_y, 1, 1)

        layout2.addWidget(l02, 0, 2)
        layout2.addWidget(self.fore_color, 0, 3)
        layout2.addWidget(l12, 1, 2)
        layout2.addWidget(self.back_color, 1, 3)

        layout2.addWidget(l20, 2, 0)
        layout2.addWidget(self.clear_after, 2, 1)
        layout2.addWidget(l22, 2, 2)
        layout2.addWidget(self.screen, 2, 3)

        layout2.addWidget(l30, 3, 0)
        layout2.addWidget(self.transparent, 3, 1)
        layout2.addWidget(l32, 3, 2)
        layout2.addWidget(self.word_wrap, 3, 3)

        layout2.addWidget(l40, 4, 0)
        layout2.addWidget(self.flip_horizontal, 4, 1)
        layout2.addWidget(l42, 4, 2)
        layout2.addWidget(self.flip_vertical, 4, 3)

        layout2.addWidget(l50, 5, 0)
        layout2.addWidget(self.font_box, 5, 1, 1, 3)
        layout2.addWidget(l52, 6, 2)
        layout2.addWidget(self.style_box, 6, 3)
        layout2.addWidget(l60, 6, 0)
        layout2.addWidget(self.font_size_box, 6, 1)
        layout2.addWidget(l70, 7, 0)
        layout2.addWidget(self.right_to_left, 7, 1)
        group2.setLayout(layout2)

        layout = QVBoxLayout()
        layout.addWidget(group1, 1)
        layout.addWidget(group2, 2)
        self.setLayout(layout)

    def dragEnterEvent(self, e):
        if e.mimeData().hasFormat(Info.AttributesToWidget):
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e: QDropEvent):
        data = e.mimeData().data(Info.AttributesToWidget)
        stream = QDataStream(data, QIODevice.ReadOnly)
        text = f"[{stream.readQString()}]"
        self.text_edit.cursor().setPos(e.pos())
        self.text_edit.insertPlainText(text)

    def refresh(self):
        self.screen_info = Func.getDeviceInfo("screen")
        screen_id = self.using_screen_id
        self.screen.clear()
        self.screen.addItems(self.screen_info.values())
        screen_name = self.screen_info.get(screen_id)
        if screen_name:
            self.screen.setCurrentText(screen_name)
            self.using_screen_id = screen_id
        self.updateInfo()

    def setScrBackGroundColor(self):
        color = Func.getCurrentScreenColor(self.using_screen_id)
        #
        # p = self.text_edit.palette()
        #
        # r, g, b = [int(x) for x in color.split(",")]
        # p.setColor(QPalette.Active, QPalette.Base, QColor(r, g, b))
        # p.setColor(QPalette.Inactive, QPalette.Base, QColor(r, g, b))
        #
        # self.text_edit.setPalette(p)
        self.text_edit.setStyleSheet("background-color: rgb({});".format(color))

    def changeScreen(self, screen):
        for k, v in self.screen_info.items():
            if v == screen:
                self.using_screen_id = k
                break

    def changeColor(self, color: str):
        oldCursor = self.text_edit.textCursor()
        self.text_edit.selectAll()

        r, g, b = 255, 255, 255
        if "," in color:
            r, g, b = [int(x) for x in color.split(",")]

        if self.sender() is self.fore_color:
            self.text_edit.setTextColor(QColor(r, g, b))
        elif self.sender() is self.back_color:
            self.text_edit.setTextBackgroundColor(QColor(r, g, b))

        self.text_edit.setTextCursor(oldCursor)

    def changeAlign(self, align_mode: str):
        oldCursor = self.text_edit.textCursor()
        self.text_edit.selectAll()

        # html中要小写
        self.align_mode = align_mode.lower()
        if align_mode == "center":
            self.text_edit.setAlignment(Qt.AlignCenter)
        elif align_mode == "left":
            self.text_edit.setAlignment(Qt.AlignLeft)
        elif align_mode == "right":
            self.text_edit.setAlignment(Qt.AlignRight)
        elif align_mode == "justify":
            self.text_edit.setAlignment(Qt.AlignJustify)

        self.text_edit.setTextCursor(oldCursor)

    def changeWrap(self, chars: str):
        oldCursor = self.text_edit.textCursor()
        self.text_edit.selectAll()

        if chars.isdigit():
            self.text_edit.setLineWrapColumnOrWidth(int(chars))

        self.text_edit.setTextCursor(oldCursor)

    def changeFont(self):
        oldCursor = self.text_edit.textCursor()
        self.text_edit.selectAll()

        # family = self.font_box.currentFont().family()
        family = self.font_box.currentText()
        if family.startswith('['):
            family = Info.DEFAULT_FONT

        size = self.font_size_box.currentText()
        size = int(size) if size.isdigit() else 8

        font = QFont()
        font.setFamily(family)
        font.setPointSize(size)

        style = self.style_box.currentText()
        if style == "normal_0":
            style = 0
        elif style == "bold_1":
            style = 1
        elif style == "italic_2":
            style = 2
        elif style == "underline_4":
            style = 4
        elif style == "outline_8":
            style = 8
        elif style == "overline_16":
            style = 16
        elif style == "condense_32":
            style = 32
        elif style == "extend_64":
            style = 64
        else:
            style = int(style) if style.isdigit() else 0

        font.setBold(style & 1)
        font.setItalic(style & 2)
        font.setUnderline(style & 4)
        font.setStrikeOut(style & 8)
        font.setOverline(style & 16)
        if style & 32:
            font.setStretch(75)  # condensed 75
        if style & 64:
            font.setStretch(125)  # expanded 125

        self.text_edit.setCurrentFont(font)
        # set all text in one type of font
        # self.text_edit.setFont(font)
        self.text_edit.setTextCursor(oldCursor)

    def setAttributes(self, attributes):
        self.text_edit.setModelList(attributes)
        self.lighter.updateRule(attributes)
        self.align_x.setCompleter(QCompleter(attributes))
        self.align_y.setCompleter(QCompleter(attributes))
        self.fore_color.setCompleter(QCompleter(attributes))
        self.back_color.setCompleter(QCompleter(attributes))
        self.transparent.setCompleter(QCompleter(attributes))
        self.word_wrap.setCompleter(QCompleter(attributes))
        self.font_size_box.setCompleter(QCompleter(attributes))
        self.style_box.setCompleter(QCompleter(attributes))

    def updateInfo(self):

        self.default_properties["Html"] = self.text_edit.toHtml()
        self.default_properties["Text"] = self.text_edit.toPlainText()
        self.default_properties["Alignment X"] = self.align_x.currentText()
        self.default_properties["Alignment Y"] = self.align_y.currentText()
        self.default_properties["Fore Color"] = self.fore_color.getRGB()
        self.default_properties["Back Color"] = self.back_color.getRGB()
        self.default_properties["Screen Name"] = self.screen.currentText()
        self.default_properties["Transparent"] = self.transparent.text()
        self.default_properties["Clear After"] = self.clear_after.currentText()
        self.default_properties["Font Family"] = self.font_box.currentText()
        self.default_properties["Font Size"] = self.font_size_box.currentText()
        self.default_properties["Wrapat Chars"] = self.word_wrap.text()
        self.default_properties["Style"] = self.style_box.currentText()
        self.default_properties["Flip Horizontal"] = self.flip_horizontal.currentText()
        self.default_properties["Flip Vertical"] = self.flip_vertical.currentText()
        self.default_properties["Right To Left"] = self.right_to_left.currentText()

    def getProperties(self):
        return self.default_properties

    def setProperties(self, properties: dict):
        self.default_properties.update(properties)
        self.loadSetting()

    def loadSetting(self):
        self.align_x.setCurrentText(self.default_properties["Alignment X"])
        self.align_y.setCurrentText(self.default_properties["Alignment Y"])
        self.fore_color.setCurrentText(self.default_properties["Fore Color"])
        self.back_color.setCurrentText(self.default_properties["Back Color"])
        self.screen.setCurrentText(self.default_properties["Screen Name"])
        self.transparent.setText(self.default_properties["Transparent"])
        self.word_wrap.setText(self.default_properties["Wrapat Chars"])
        self.clear_after.setCurrentText(self.default_properties["Clear After"])
        self.font_box.setCurrentText(self.default_properties["Font Family"])
        self.font_size_box.setCurrentText(self.default_properties["Font Size"])
        self.style_box.setCurrentText(self.default_properties["Style"])
        self.flip_horizontal.setCurrentText(self.default_properties["Flip Horizontal"])
        self.flip_vertical.setCurrentText(self.default_properties["Flip Vertical"])
        self.right_to_left.setCurrentText(self.default_properties["Right To Left"])
        self.text_edit.setHtml(self.default_properties["Html"])

    def loadDefaultFontInfo(self):
        if Info.FONT_DEFAULT_PREF:

            if not self.back_color.getRGB().startswith('['):
                self.back_color.setCurrentText(Info.FONT_DEFAULT_PREF.get("Back Color", "255,255,255"))

            if not self.fore_color.getRGB().startswith('['):
                self.fore_color.setCurrentText(Info.FONT_DEFAULT_PREF.get("Fore Color", "0,0,0"))

            if not self.style_box.currentText().startswith('['):
                self.style_box.setCurrentText(Info.FONT_DEFAULT_PREF.get("Style", "normal_0"))

            if not self.font_size_box.currentText().startswith('['):
                self.font_size_box.setCurrentText(Info.FONT_DEFAULT_PREF.get("Font Size", "12"))

            if not self.font_box.currentText().startswith('['):
                self.font_box.setCurrentText(Info.FONT_DEFAULT_PREF.get("Font Family", "Times"))
