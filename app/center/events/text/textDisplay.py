from PyQt5.QtCore import Qt, QIODevice, QDataStream
from PyQt5.QtGui import QIcon, QDropEvent, QColor, QFont
from PyQt5.QtWidgets import QToolBar, QAction

from app.func import Func
from app.info import Info
from lib import TabItemMainWindow
from .lighter import AttributeHighlighter
from .smart import SmartTextEdit
from .textProperty import TextProperty


class TextDisplay(TabItemMainWindow):
    def __init__(self, widget_id: str, widget_name: str):
        super(TextDisplay, self).__init__(widget_id, widget_name)

        self.text_label = SmartTextEdit()
        self.setAcceptDrops(True)

        self.pro_window = TextProperty()
        self.default_properties = self.pro_window.default_properties

        self.lighter = AttributeHighlighter(self.text_label.document())

        self.pro_window.ok_bt.clicked.connect(self.ok)
        self.pro_window.cancel_bt.clicked.connect(self.cancel)
        self.pro_window.apply_bt.clicked.connect(self.apply)

        self.setUI()
        self.setAttributesForTextLabel()
        # self.loadDefaultFontInfo()

    def setUI(self):
        self.setWindowTitle("Text")
        self.text_label.setText("Your text will appear here")
        self.text_label.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(self.text_label)
        self.text_label.textChanged.connect(self.updateTextInRealtime)

        tool = QToolBar()
        open_pro = QAction(QIcon(Func.getImage("menu/setting.png")), "setting", self)
        open_pro.triggered.connect(self.openSettingWindow)
        tool.addAction(open_pro)

        self.addToolBar(Qt.TopToolBarArea, tool)
        self.setScrBackGroundColor()
        self.loadDefaultFontInfo()

    def dragEnterEvent(self, e):
        if e.mimeData().hasFormat(Info.AttributesToWidget):
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e: QDropEvent):
        data = e.mimeData().data(Info.AttributesToWidget)
        stream = QDataStream(data, QIODevice.ReadOnly)
        text = f"[{stream.readQString()}]"
        self.text_label.cursor().setPos(e.pos())
        self.text_label.insertPlainText(text)

    def updateTextInRealtime(self):
        self.pro_window.general.text_edit.setHtml(self.text_label.toHtml())

    def openSettingWindow(self):
        self.pro_window.general.text_edit.setHtml(self.text_label.toHtml())
        super(TextDisplay, self).openSettingWindow()

    def refresh(self):
        self.pro_window.refresh()
        self.setScrBackGroundColor()

    def ok(self):
        self.apply()
        self.pro_window.close()

    def cancel(self):
        self.pro_window.loadSetting()

    def apply(self):
        self.updateInfo()
        self.text_label.setHtml(self.default_properties.get("General").get("Html"))
        self.setScrBackGroundColor()

    def updateInfo(self):
        self.pro_window.updateInfo()

    def setScrBackGroundColor(self):
        color = Func.getCurrentScreenColor(self.pro_window.getScreenId())
        # p = self.text_label.palette()
        # r, g, b = [int(x) for x in color.split(",")]
        #
        # p.setColor(QPalette.Active, QPalette.Base, QColor(r, g, b))
        # p.setColor(QPalette.Inactive, QPalette.Base, QColor(r, g, b))

        # self.text_label.setPalette(p)
        #
        # p.setColor(QPalette.Active, QPalette.Base, QColor(0, 255, 0))
        # p.setColor(QPalette.Inactive, QPalette.Base, QColor(200, 0, 0))

        # self.text_label.setAutoFillBackground(True)
        # self.text_label.setPalette(p)

        self.text_label.setStyleSheet("background-color: rgb({});".format(color))
        self.pro_window.general.setScrBackGroundColor()

    # 设置可选参数
    def setAttributes(self, attributes):
        self.lighter.updateRule(attributes)
        format_attributes = ["[{}]".format(attribute) for attribute in attributes]
        self.pro_window.setAttributes(format_attributes)
        # self.text_label.setModelList(format_attributes)

    def setAttributesForTextLabel(self):
        attributes = Func.getWidgetAttributes(self.widget_id)
        self.lighter.updateRule(attributes)
        format_attributes = ["[{}]".format(attribute) for attribute in attributes]
        self.text_label.setModelList(format_attributes)

    def setProperties(self, properties: dict):
        self.pro_window.setProperties(properties)
        self.apply()

    def getProperties(self) -> dict:
        self.refresh()
        return self.pro_window.getProperties()

    def store(self):
        """
        return necessary data for restoring this widget.
        @return:
        """
        self.updateInfo()
        return self.default_properties

    def restore(self, properties: dict):
        self.setProperties(properties)

    def clone(self, new_widget_id: str, new_widget_name):
        self.updateInfo()
        clone_widget = TextDisplay(new_widget_id, new_widget_name)
        clone_widget.setProperties(self.default_properties)
        clone_widget.apply()
        return clone_widget

    def loadDefaultFontInfo(self):
        if Info.FONT_DEFAULT_PREF:
            oldCursor = self.text_label.textCursor()
            self.text_label.selectAll()
            """
            # load default font color 
            """
            fore_color = Info.FONT_DEFAULT_PREF.get("Fore Color", "0,0,0")
            back_color = Info.FONT_DEFAULT_PREF.get("Back Color", "255,255,255")

            r, g, b, *_ = fore_color.split(',')
            if not self.pro_window.general.fore_color.getRGB().startswith('['):
                self.text_label.setTextColor(QColor(int(r), int(g), int(b)))

            r, g, b, *_ = back_color.split(',')
            if not self.pro_window.general.back_color.getRGB().startswith('['):
                self.text_label.setTextBackgroundColor(QColor(int(r), int(g), int(b)))
            """
            # load default font family, size, style
            """
            # all values in FONT_DEFAULT are not citable
            family = Info.FONT_DEFAULT_PREF.get("Font Family", Info.DEFAULT_FONT)
            family = Info.DEFAULT_FONT if self.pro_window.general.font_box.currentText().startswith('[') else family

            size = Info.FONT_DEFAULT_PREF.get("Font Size", "12")

            if size.isdigit():
                size = int(float(size))
            else:
                size = 12
            # self.pro_window.general.font_size_box.currentText().startswith('['):

            style = Info.FONT_DEFAULT_PREF.get("Style", "normal_0")
            style = "normal_0" if self.pro_window.general.style_box.currentText().startswith('[') else style

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
                style = int(float(style)) if style.isdigit() else 0

            font = QFont()
            font.setFamily(family)
            font.setPointSize(size)

            font.setBold(style & 1)
            font.setItalic(style & 2)
            font.setUnderline(style & 4)
            font.setStrikeOut(style & 8)
            font.setOverline(style & 16)
            if style & 32:
                font.setStretch(75)  # condensed 75
            if style & 64:
                font.setStretch(125)  # expanded 125

            self.text_label.setCurrentFont(font)
            # setFont: set all text in one type of font
            # self.text_label.setFont(font)

            self.text_label.setTextCursor(oldCursor)

            # update general GUI
            self.pro_window.general.loadDefaultFontInfo()

    # 返回各项参数
    # 大部分以字符串返回，少数点击选择按钮返回布尔值
    # 因为有些地方引用Attribute
    def getText(self, is_html: bool = False) -> str:
        """
        返回文本信息，纯文本(default)或者html
        :param is_html:
        :return:
        """
        if is_html:
            return self.pro_window.general.text_edit.toHtml()
        else:
            return self.pro_window.general.text_edit.toPlainText()

    def getAlignmentX(self) -> str:
        """
        返回文字对齐方式
        :return:
        """
        return self.pro_window.general.align_x.currentText()

    def getAlignmentY(self) -> str:
        """
        返回文字对齐方式
        :return:
        """
        return self.pro_window.general.align_y.currentText()

    def getForceColor(self) -> str:
        """
        返回前景色
        :return:
        """
        return self.pro_window.general.fore_color.getRGB()

    def getScreenName(self) -> str:
        """
        返回Screen Name
        :return:
        """
        return self.pro_window.general.screen.currentText()

    def getBackColor(self) -> str:
        """
        返回背景颜色
        :return:
        """
        return self.pro_window.general.back_color.getRGB()

    def getTransparent(self) -> str:
        """
        返回图像透明度
        :return:
        """
        return self.pro_window.general.transparent.text()

    def getIsClearAfter(self) -> str:
        """
        返回是否clear after
        :return:
        """
        return self.pro_window.general.clear_after.currentText()

    def getFontFamily(self) -> str:
        """
        返回字体信息
        :return:
        """
        return self.pro_window.general.font_box.currentText()

    def getFontPointSize(self) -> str:
        """
        返回字体大小
        :return:
        """
        return self.pro_window.general.font_size_box.currentText()

    def getWrapatChar(self) -> str:
        """
        返回是否换行
        :return:
        """
        return self.pro_window.general.word_wrap.text()

    def getRightToLeft(self) -> str:
        """
        返回right to left
        :return:
        """
        return self.pro_window.general.right_to_left.currentText()

    def getXAxisCoordinates(self) -> str:
        """
        返回x坐标值
        :return:
        """
        return self.default_properties.get("Frame").get("Center X")

    def getYAxisCoordinates(self) -> str:
        """
        返回y坐标值
        :return:
        """
        return self.default_properties.get("Frame").get("Center Y")

    def getWidth(self) -> str:
        """
        返回宽度
        :return:
        """
        return self.default_properties.get("Frame").get("Width")

    def getHeight(self) -> str:
        """
        返回高度
        :return:
        """
        return self.default_properties.get("Frame").get("Height")

    def getEnable(self) -> str:
        """
        返回frame enable
        :return:
        """
        return self.pro_window.frame.enable.currentText()

    def getFrameTransparent(self) -> str:
        """返回frame transparent"""
        return self.pro_window.frame.transparent.text()

    def getBorderColor(self) -> str:
        """
        返回边框颜色
        :return:
        """
        return self.pro_window.frame.border_color.getRGB()

    def getBorderWidth(self) -> str:
        """
        返回边框宽度
        :return:
        """
        return self.pro_window.frame.border_width.currentText()

    def getFrameFillColor(self) -> str:
        """
        返回边框背景色
        :return:
        """
        return self.pro_window.frame.back_color.getRGB()

    def getDuration(self) -> str:
        """
        返回duration
        :return:
        """
        return self.pro_window.duration.duration.currentText()

    def getOutputDevice(self) -> dict:
        """
        返回输出设备
        :return:
        """
        return self.pro_window.duration.default_properties.get("Output Devices", {})

    def getInputDevice(self) -> dict:
        """
        返回输入设备
        :return: 输入设备字典
        """
        return self.pro_window.duration.default_properties.get("Input Devices", {})

    def getScreenId(self) -> str:
        return self.pro_window.getScreenId()
