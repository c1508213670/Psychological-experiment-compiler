from PyQt5.QtCore import Qt, QFileInfo
from PyQt5.QtGui import QIcon, QImage, QPixmap, QPainter, QColor, QDragEnterEvent, QDropEvent
from PyQt5.QtWidgets import QToolBar, QAction, QScrollArea

from app.func import Func
from lib import TabItemMainWindow
from .imageContainer import ImageContainer
from .imageProperty import ImageProperty


class ImageDisplay(TabItemMainWindow):
    def __init__(self, widget_id: str, widget_name: str):
        super(ImageDisplay, self).__init__(widget_id, widget_name)
        # self.setAcceptDrops(True)

        # 图片展示框
        self.label_scroll = QScrollArea()
        self.label = ImageContainer()
        self.label_scroll.setWidget(self.label)


        # 属性设置窗口
        self.pro_window = ImageProperty()
        self.default_properties = self.pro_window.default_properties

        self.setUI()

        self.linkSignal()
        self.apply()

    def setUI(self):
        """
        UI part, necessary
        :return:
        """
        self.setWindowTitle("Image")
        self.setCentralWidget(self.label_scroll)

        tool = QToolBar()
        open_pro = QAction(QIcon(Func.getImage("menu/setting.png")), "setting", self)
        open_pro.triggered.connect(self.openSettingWindow)
        tool.addAction(open_pro)

        self.addToolBar(Qt.TopToolBarArea, tool)

    def linkSignal(self):
        self.pro_window.ok_bt.clicked.connect(self.ok)
        self.pro_window.cancel_bt.clicked.connect(self.cancel)
        self.pro_window.apply_bt.clicked.connect(self.apply)

    def refresh(self):
        self.pro_window.refresh()
        self.setScrBackgroundColor()

    def ok(self):
        self.apply()
        self.pro_window.close()

    def cancel(self):
        self.pro_window.loadSetting()

    def apply(self):
        # 发送信号
        self.updateInfo()
        self.parseProperties()
        self.propertiesChanged.emit(self.widget_id)

        self.setScrBackgroundColor()

    def updateInfo(self):
        self.pro_window.updateInfo()

    def setAttributes(self, attributes: list):
        format_attributes = ["[{}]".format(attribute) for attribute in attributes]
        self.pro_window.setAttributes(format_attributes)

    def setScrBackgroundColor(self):
        color = Func.getCurrentScreenColor(self.pro_window.getScreenId())
        self.label.setStyleSheet("background-color: rgb({});".format(color))

    def setProperties(self, properties: dict):
        """
        {
        "":{}
        "":{}
        }
        :param properties:
        :return:
        """
        self.pro_window.setProperties(properties)
        self.apply()

    def getProperties(self) -> dict:
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

    def clone(self, new_widget_id: str, new_widget_name: str):
        self.updateInfo()
        clone_widget = ImageDisplay(new_widget_id, new_widget_name)
        clone_widget.setProperties(self.default_properties)
        clone_widget.apply()
        return clone_widget

    def parseProperties(self):
        screen_id = self.pro_window.general.getScreenId()
        w, h = Func.getCurrentScreenRes(screen_id)
        self.label.resize(w, h)

        file_name = self.default_properties["General"]["File Name"]
        file_name = Func.getFullFilePath(file_name)
        
        if QFileInfo(file_name).isFile():
            img = QImage(file_name)
            mup = self.default_properties["General"]["Mirror Up/Down"]
            mlr = self.default_properties["General"]["Mirror Left/Right"]

            it = self.default_properties["General"]["Transparent"]
            if it.endswith("%"):
                img_tra = int(int(it.rstrip("%")) / 100 * 255)
            elif it.isdigit():
                img_tra = int(it)
            else:
                img_tra = 255
            p = QPainter()
            p.begin(img)
            p.setCompositionMode(QPainter.CompositionMode_DestinationIn)
            # todo
            p.fillRect(img.rect(), QColor(0, 0, 0, img_tra))
            p.end()

            pix = QPixmap().fromImage(img.mirrored(mlr, mup))
            is_stretch = self.default_properties["General"]["Stretch"]
            if is_stretch:
                mode = self.pro_window.general.stretch_mode.currentText()
                if mode == "Both":
                    pix = pix.scaled(w, h, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
                elif mode == "Horizontal":
                    pix = pix.scaledToWidth(w, Qt.FastTransformation)
                else:
                    pix = pix.scaledToHeight(h, Qt.FastTransformation)
            self.label.pix = pix

            rotate = self.default_properties["General"]["Rotate"]
            if rotate.isdigit():
                self.label.rotate = int(rotate)

            cx: str = self.default_properties["Frame"]["Center X"]
            if cx.endswith("%"):
                self.label.cx = w * int(cx.rstrip("%")) / 100
            elif cx.isdigit():
                self.label.cx = int(cx)
            cy: str = self.default_properties["Frame"]["Center Y"]
            if cy.endswith("%"):
                self.label.cy = h * int(cy.rstrip("%")) / 100
            elif cy.isdigit():
                self.label.cy = int(cy)
            self.label_scroll.horizontalScrollBar().setValue(self.label.cx / self.label.width() * (
                        self.label_scroll.horizontalScrollBar().maximum() - self.label_scroll.horizontalScrollBar().minimum()))
            self.label_scroll.verticalScrollBar().setValue(self.label.cy / self.label.height() * (
                        self.label_scroll.horizontalScrollBar().maximum() - self.label_scroll.horizontalScrollBar().minimum()))

            enable = self.default_properties["Frame"]["Enable"]
            if enable == "Yes":
                boc = self.default_properties["Frame"]["Border Color"]
                if not boc.startswith("["):
                    self.label.setColor(boc, 0)
                bow = self.default_properties["Frame"]["Border Width"]
                if bow.isdigit():
                    self.label.border_width = int(bow)
                bac = self.default_properties["Frame"]["Frame Fill Color"]
                if not bac.startswith("["):
                    self.label.setColor(bac, 1)

                ft = self.default_properties["Frame"]["Frame Transparent"]
                if ft.endswith("%"):
                    self.label.setFrameTransparent(int(int(ft.rstrip("%")) / 100 * 255))
                elif ft.isdigit():
                    self.label.setFrameTransparent(int(ft))

            self.label.update()

        else:
            self.label_scroll.horizontalScrollBar().setValue(0)
            self.label_scroll.verticalScrollBar().setValue(0)
            self.label.pix = None

    ##########################################
    # return single attribute
    # most of them return string
    # you can see this as a document。
    ##########################################
    def getFilename(self) -> str:
        """
        返回图片文件名（relative path）
        :return:
        """
        return self.default_properties.get("General").get("File Name")

    def getIsMirrorUpAndDown(self) -> bool:
        """
        返回图片是否上下镜像
        :return:
        """
        return self.default_properties.get("General").get("Mirror Up/Down")

    def getIsMirrorLeftAndRight(self) -> bool:
        """
        返回图片是否左右镜像
        :return:
        """
        return self.default_properties.get("General").get("Mirror Left/Aright")

    def getRotate(self) -> str:
        """
        返回Rotate
        :return:
        """
        return self.default_properties.get("General").get("Rotate")

    def getStretchMode(self) -> str:
        """
        返回图像拉伸模式
        未拉伸返回0
        上下拉伸返回1
        左右拉伸返回2
        全拉伸返回3
        :return: ""、Both、LeftRight、Vertical、[attr]
        """
        if self.default_properties.get("General").get("Stretch"):
            return self.default_properties.get("General").get("Stretch Mode")
        return ""

    def getTransparent(self) -> str:
        """
        返回图像透明度
        :return:
        """
        return self.default_properties.get("General").get("Transparent")

    def getClearAfter(self) -> str:
        """
        返回是否clear after
        :return:
        """
        return self.default_properties.get("General").get("Clear After")

    def getScreenName(self) -> str:
        """
        返回Screen Name
        :return:
        """
        return self.default_properties.get("General").get("Screen Name")

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
