from PyQt5 import sip
from PyQt5.QtCore import Qt, QRect, QRectF
from PyQt5.QtGui import QIcon, QColor, QIntValidator, QPixmap, QPainter, QBrush
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QGraphicsView, QToolButton, QButtonGroup, QMenu, QAction, \
    QComboBox, QColorDialog, QToolBar, QSlider, QSpinBox

from app.func import Func
from lib import TabItemMainWindow
from .item import *
from .left.leftBox import LeftBox
from .property import ComboProperty
from .scene import Scene


class Combo(TabItemMainWindow):
    def __init__(self, widget_id: str, widget_name: str):
        super(Combo, self).__init__(widget_id, widget_name)
        self.current_wid = widget_id

        self.pro_window = ComboProperty()

        self.scene = Scene()
        self.left_box = LeftBox()

        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(QPainter.Antialiasing)

        width, height = Func.getCurrentScreenRes(self.pro_window.getScreenId())
        self.view.setMaximumSize(width, height)
        self.scene.setSceneRect(QRectF(0, 0, width, height))
        self.w: int = width
        self.h: int = height

        self.scene.w = self.w
        self.scene.h = self.h

        self.screen_color: QColor = QColor(Qt.white)

        self.properties = self.pro_window.default_properties
        self.default_properties: dict = {
            "Items": {},
            "ItemsOrderedKey": [],
            "Properties": self.properties
        }
        self.initMenu()
        self.linkSignal()
        self.setUI()

    def initMenu(self):
        open_action = QAction(QIcon(Func.getImage("menu/setting.png")), "Setting", self)
        open_action.triggered.connect(self.openSettingWindow)

        # save_action = QAction(QIcon(Func.getImage("operate/screenshot.png")), "Screenshot(beta)", self)
        # save_action.triggered.connect(self.scene.screenshot)

        front_action = QAction(QIcon(Func.getImage("operate/sendtoback.png")), "Bring to Front", self)
        front_action.setToolTip("Bring item to front")
        front_action.triggered.connect(self.toFront)

        back_action = QAction(QIcon(Func.getImage("operate/bringtofront.png")), "Send to Back", self)
        back_action.setToolTip("Send item to back")
        back_action.triggered.connect(self.toBack)

        open_item_action = QAction(QIcon(Func.getImage("menu/setting.png")), "Properties", self)
        open_item_action.triggered.connect(self.openItem)

        delete_action = QAction(QIcon(Func.getImage("operate/trash.png")), "Delete", self)
        delete_action.setShortcut("Delete")
        delete_action.setToolTip("Delete item from diagram")
        delete_action.triggered.connect(self.deleteItem)

        copy_action = QAction(QIcon(Func.getImage("operate/copy.png")), "Copy", self)
        copy_action.setShortcut("Ctrl+D")
        copy_action.setToolTip("copy item from diagram")
        copy_action.triggered.connect(self.copyItem)

        self.item_list = QComboBox()
        self.item_list.setMinimumWidth(100)
        self.item_list.addItem("none")
        self.item_list.currentTextChanged.connect(self.selectItem)

        self.item_pro_windows = QAction(QIcon(Func.getImage("operate/item_pro.png")), "open item properties", self)
        self.item_pro_windows.setToolTip("Open current item's properties")
        self.item_pro_windows.triggered.connect(self.openItem)
        self.item_pro_windows.setEnabled(False)

        setting = QToolBar()
        setting.addAction(open_action)
        # setting.addAction(save_action)
        setting.addSeparator()
        setting.addAction(delete_action)
        setting.addAction(copy_action)
        setting.addAction(front_action)
        setting.addAction(back_action)
        setting.addWidget(self.item_list)
        setting.addAction(self.item_pro_windows)

        self.fill_color_bt = QToolButton()
        self.fill_color_bt.setPopupMode(QToolButton.MenuButtonPopup)
        self.fill_color_bt.setMenu(
            self.createColorMenu(self.itemColorChanged, Qt.white))
        self.fill_color_bt.setIcon(
            self.createColorButtonIcon(Func.getImage("operate/floodfill.png"),
                                       Qt.white))

        self.line_color_bt = QToolButton()
        self.line_color_bt.setPopupMode(QToolButton.MenuButtonPopup)
        self.line_color_bt.setMenu(
            self.createColorMenu(self.lineColorChanged, Qt.black))
        self.line_color_bt.setIcon(
            self.createColorButtonIcon(Func.getImage("operate/linecolor.png"),
                                       Qt.black))
        # line size
        self.line_width_com = QComboBox()
        self.line_width_com.setEditable(True)
        for i in range(2, 20, 2):
            self.line_width_com.addItem(str(i))
        validator = QIntValidator(0, 20, self)
        self.line_width_com.setValidator(validator)
        self.line_width_com.currentTextChanged.connect(self.changeLineWidth)

        setting.addWidget(self.fill_color_bt)
        setting.addWidget(self.line_color_bt)
        setting.addWidget(self.line_width_com)

        self.pointer_bt = QToolButton()
        self.pointer_bt.setCheckable(True)
        self.pointer_bt.setChecked(True)
        self.pointer_bt.setIcon(QIcon(Func.getImage("operate/pointer.png")))
        line_bt = QToolButton()
        line_bt.setCheckable(True)
        line_bt.setIcon(QIcon(Func.getImage("widgets/linepointer.png")))
        lasso_bt = QToolButton()
        lasso_bt.setCheckable(True)
        lasso_bt.setIcon(QIcon(Func.getImage("operate/lasso.png")))

        self.pointer_group = QButtonGroup()
        self.pointer_group.addButton(self.pointer_bt, Scene.NormalMode)
        self.pointer_group.addButton(line_bt, Scene.LineMode)
        self.pointer_group.addButton(lasso_bt, Scene.LassoMode)
        self.pointer_group.buttonClicked[int].connect(self.pointerGroupClicked)

        setting.addWidget(self.pointer_bt)
        setting.addWidget(line_bt)
        setting.addWidget(lasso_bt)

        self.background_bt = QToolButton()
        self.background_bt.setPopupMode(QToolButton.MenuButtonPopup)
        self.background_bt.setMenu(
            self.createBackgroundMenu(self.changeBackground))
        self.background_bt.setIcon(QIcon(Func.getImage("widgets/background4.png")))
        setting.addWidget(self.background_bt)

        slider_input = QSpinBox()
        slider_input.setSuffix("%")
        slider_input.setRange(25, 400)
        slider_input.setValue(100)

        slider = QSlider(Qt.Horizontal)
        slider.setMaximumWidth(250)
        slider.setRange(25, 400)
        slider.setValue(100)
        slider.setTickPosition(QSlider.TicksBelow)
        slider.setTickInterval(25)

        slider_input.valueChanged.connect(slider.setValue)
        slider.valueChanged[int].connect(self.zoom)
        slider.valueChanged[int].connect(slider_input.setValue)
        setting.addWidget(slider)
        setting.addWidget(slider_input)

        self.addToolBar(Qt.TopToolBarArea, setting)

        self.scene.menu = QMenu()
        self.scene.menu.addAction(delete_action)
        self.scene.menu.addAction(copy_action)
        self.scene.menu.addSeparator()
        self.scene.menu.addAction(front_action)
        self.scene.menu.addAction(back_action)
        self.scene.menu.addAction(open_item_action)

    def linkSignal(self):
        self.scene.itemAdd.connect(self.addItem)
        self.scene.itemSelected.connect(lambda: self.pointer_bt.setChecked(True))
        self.scene.selectionChanged.connect(self.changeItemList)

        self.pro_window.ok_bt.clicked.connect(self.ok)
        self.pro_window.cancel_bt.clicked.connect(self.cancel)
        self.pro_window.apply_bt.clicked.connect(self.apply)

    def setUI(self):
        self.setWindowTitle("combo")
        layout = QHBoxLayout()
        layout.addWidget(self.left_box, 0, Qt.AlignLeft)
        layout.addWidget(self.view, 1, Qt.AlignHCenter | Qt.AlignVCenter)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def deleteItem(self):
        for item in self.scene.selectedItems():
            self.scene.removeItem(item)
            item_name = item.getName()
            index = self.item_list.findText(item_name, Qt.MatchExactly)
            if index != -1:
                self.item_list.removeItem(index)

    def copyItem(self):
        for item in self.scene.selectedItems():
            self.scene.copyItem(item)

    def toFront(self):
        if not self.scene.selectedItems():
            return
        selected_item = self.scene.selectedItems()[0]
        overlap_items = selected_item.collidingItems()

        for iItem in range(len(overlap_items)-1, -1, -1):
            overlap_items[iItem].stackBefore(selected_item)
            self.scene.update()

        # z_value = 0
        # for item in overlap_items:
        #     if item.zValue() >= z_value:
        #         z_value = item.zValue() + 0.1
        # selected_item.setZValue(z_value)

    def toBack(self):
        if not self.scene.selectedItems():
            return
        selected_item = self.scene.selectedItems()[0]
        overlap_items = selected_item.collidingItems()
        for iItem in range(0, len(overlap_items), 1):
            if overlap_items[iItem] not in [self.scene.frame, self.scene.border]:
                selected_item.stackBefore(overlap_items[iItem])
                self.scene.update()
        # see detail in https://blog.csdn.net/zzwdkxx/article/details/41676219
        # z_value = 0
        # for item in overlap_items:
        #     if isinstance(item, DiaItem) \
        #             or isinstance(item, DotItem) \
        #             or isinstance(item, LineItem) \
        #             or isinstance(item, OtherItem) \
        #             or isinstance(item, PixItem) \
        #             or isinstance(item, TextItem):
        #         if item.zValue() <= z_value:
        #             z_value = item.zValue() - 0.1
        # selected_item.setZValue(z_value)
        # self.scene.downFrame(z_value - 0.1)

    def selectItem(self, item_name: str):
        """
        when choose some items by item list
        :param item_name:
        :return:
        """
        self.blockSignals(True)
        self.item_pro_windows.setEnabled(item_name != "none")
        items = self.scene.selectedItems()
        if items:
            for item in items:
                item.setSelected(item_name == item.getName())

        for item in self.scene.items():
            if isinstance(item, TextItem) or isinstance(item, PixItem) \
                    or isinstance(item, LineItem) \
                    or isinstance(item, OtherItem) \
                    or isinstance(item, DiaItem) \
                    or isinstance(item, DotItem):

                if item_name == item.getName():
                    item.setSelected(True)
                    self.changeTool(item)
                    break
        self.blockSignals(False)

    def openItem(self):
        items = self.scene.selectedItems()
        if items:
            items[0].openPro()

    def addItem(self, item_name: str, is_arrow: bool):
        """
        change item list when item added by drag and drop
        :param is_arrow:
        :type is_arrow:
        :param item_name:
        :return:
        """
        if is_arrow:
            self.pointer_bt.setChecked(True)
            self.scene.setMode(Scene.NormalMode)
        self.item_list.addItem(item_name)

    def changeItemList(self):
        self.blockSignals(True)
        if not sip.isdeleted(self.scene):
        # try:
            items = self.scene.selectedItems()
            if items:
                if items[0].getName() != self.item_list.currentText():
                    self.item_list.setCurrentText(items[0].getName())
            else:
                self.item_list.setCurrentIndex(0)
        # except:
            # try to remove the error:
            # RuntimeError: wrapped C/C++ object of type Scene
            # has been deleted
            # pass

        self.blockSignals(False)

    def changeTool(self, item):
        """
        show item information such as color when selected.
        :param item: selected item
        :return:
        """
        border_width = item.properties.get("Border Width", "1")
        if not border_width.startswith("["):
            self.line_width_com.setCurrentText(border_width)

        border_color: str = item.properties.get("Border Color", "0,0,0")
        if border_color.startswith("["):
            r, g, b, a = 0, 0, 0, 255
        else:
            color = [int(x) for x in border_color.split(",")]
            if len(color) == 3:
                r, g, b = color
                a = 255
            else:
                r, g, b, a = color
        color = QColor(r, g, b, a)
        self.line_color_bt.setIcon(self.createColorButtonIcon(Func.getImage("operate/linecolor.png"), color))

        fill_color: str = item.properties.get("Fill Color", "255,255,255")
        if fill_color.startswith("["):
            r, g, b, a = 255, 255, 255, 255
        else:
            color = [int(x) for x in fill_color.split(",")]
            if len(color) == 3:
                r, g, b = color
                a = 255
            else:
                r, g, b, a = color
        color = QColor(r, g, b, a)
        self.fill_color_bt.setIcon(self.createColorButtonIcon(Func.getImage("operate/floodfill.png"), color))

    def refresh(self):
        self.pro_window.refresh()
        self.scene.refresh()

        self.setScreenRect()
        self.setFrame()

    def setAttributes(self, attributes: list):
        format_attributes = ["[{}]".format(attribute) for attribute in attributes]
        self.pro_window.setAttributes(format_attributes)
        self.scene.setAttributes(format_attributes)

    def getInfo(self):
        self.default_properties["Items"] = self.scene.getInfo()
        # QSettings will not keep the order, so we need to manually save the keys order for items (scene widget)
        self.default_properties["ItemsOrderedKeys"] = list(self.default_properties["Items"].keys())
        self.pro_window.updateInfo()
        return self.default_properties

    def getProperties(self):
        self.refresh()
        return self.pro_window.getProperties()

    def pointerGroupClicked(self, i):
        self.scene.setMode(self.pointer_group.checkedId())

    def itemColorChanged(self):
        color_data = self.sender().data()
        if color_data == 'More..':
            color = QColorDialog.getColor()
            if color.isValid():
                self.fill_color_bt.setIcon(
                    self.createColorButtonIcon(Func.getImage("operate/floodfill.png"), color))
                self.scene.setItemColor(color)
        else:
            self.fill_color_bt.setIcon(
                self.createColorButtonIcon(Func.getImage("operate/floodfill.png"),
                                           QColor(color_data)))
            self.scene.setItemColor(QColor(color_data))

    def lineColorChanged(self):
        color_data = self.sender().data()
        if color_data == 'More..':
            color = QColorDialog.getColor()
            self.line_color_bt.setIcon(
                self.createColorButtonIcon(Func.getImage("operate/linecolor.png"), color))
            self.scene.setLineColor(color)
        else:
            self.line_color_bt.setIcon(
                self.createColorButtonIcon(Func.getImage('operate/linecolor.png'),
                                           QColor(color_data)))
            self.scene.setLineColor(QColor(color_data))

    def changeLineWidth(self, width: str):
        self.scene.setLineWidth(int(width))

    def changeBackground(self):
        fn = f"background{self.sender().data()}.png"
        fp = Func.getImage(f"widgets/{fn}")
        self.background_bt.setIcon(QIcon(fp))
        self.scene.setBackgroundBrush(QBrush(QPixmap(fp)))
        self.scene.update()
        self.view.update()

    def createBackgroundMenu(self, slot):
        back_menu = QMenu(self)
        action1 = QAction(QIcon(Func.getImage("widgets/background1.png")), 'Blue Grid', self)
        action2 = QAction(QIcon(Func.getImage("widgets/background2.png")), 'White Grid', self)
        action3 = QAction(QIcon(Func.getImage("widgets/background3.png")), 'Gray Grid', self)
        action4 = QAction(QIcon(Func.getImage("widgets/background4.png")), 'No Grid', self, )
        action1.setData('1')
        action1.triggered.connect(slot)
        action2.setData('2')
        action2.triggered.connect(slot)
        action3.setData('3')
        action3.triggered.connect(slot)
        action4.setData('4')
        action4.triggered.connect(slot)
        back_menu.setDefaultAction(action4)
        back_menu.addAction(action1)
        back_menu.addAction(action2)
        back_menu.addAction(action3)
        back_menu.addAction(action4)
        return back_menu

    def createColorMenu(self, slot, default_color):
        colors = (Qt.black, Qt.white, Qt.red, Qt.blue, Qt.yellow)
        names = ("Black", "White", "Red", "Blue", "Yellow")

        color_menu = QMenu(self)
        more_action = QAction('More..', self)
        more_action.setData('More..')
        more_action.triggered.connect(slot)
        for color, name in zip(colors, names):
            action = QAction(self.createColorIcon(color), name, self)
            action.triggered.connect(slot)
            action.setData(QColor(color))
            color_menu.addAction(action)
            if color == default_color:
                color_menu.setDefaultAction(action)
        color_menu.addAction(more_action)
        return color_menu

    def zoom(self, value):
        factor = value / 100.0
        matrix = self.view.transform()
        matrix.reset()
        matrix.scale(factor, factor)
        self.view.setTransform(matrix)

    @staticmethod
    def createColorButtonIcon(file_path, color):
        pix = QPixmap(50, 80)
        pix.fill(Qt.transparent)
        painter = QPainter(pix)
        image = QPixmap(file_path)
        target = QRect(0, 0, 50, 60)
        source = QRect(0, 0, 42, 42)
        painter.fillRect(QRect(0, 60, 50, 80), color)
        painter.drawPixmap(target, image, source)
        painter.end()
        return QIcon(pix)

    @staticmethod
    def createColorIcon(color):
        pix = QPixmap(20, 20)
        painter = QPainter(pix)
        painter.setPen(Qt.NoPen)
        painter.fillRect(QRect(0, 0, 20, 20), color)
        painter.end()
        return QIcon(pix)

    def ok(self):
        self.apply()
        self.pro_window.close()

    def cancel(self):
        self.pro_window.loadSetting()

    def apply(self):
        self.getInfo()
        # 发送信号
        self.propertiesChanged.emit(self.widget_id)
        self.setFrame()
        self.setScreenRect()

    def setScreenRect(self):
        width, height, color = Func.getCurrentScreenRes(self.pro_window.getScreenId(), True)
        cScrColor = QColor(*[int(x) for x in color.split(",")])

        if width != self.w or height != self.h or cScrColor != self.screen_color:
            if cScrColor != self.screen_color:
                self.screen_color = cScrColor

            if width != self.w or height != self.h:
                self.setMaximumSize(width, height)
                self.scene.setSceneRect(QRectF(0, 0, width, height))
                self.w = width
                self.h = height

                self.scene.updateSceneWHInfo()

        self.scene.setBorderRect(QRectF(0, 0, width, height), cScrColor)

    def setFrame(self):
        ###################
        # parse parameters
        ###################
        x1, y1, w, h = 0, 0, self.w, self.h
        # frame_fill_color = self.screen_color
        frame_line_width = 0
        # frame_line_color = QColor(Qt.black)

        cx_str: str = self.properties["Frame"]["Center X"]
        if cx_str.endswith("%"):
            x1 = self.w * int(cx_str.rstrip("%")) / 100
        elif cx_str.isdigit():
            x1 = int(cx_str)
        cy_str: str = self.properties["Frame"]["Center Y"]
        if cy_str.endswith("%"):
            y1 = h * int(cy_str.rstrip("%")) / 100
        elif cy_str.isdigit():
            y1 = int(cy_str)

        w_str: str = self.properties["Frame"]["Width"]
        if w_str.endswith("%"):
            w = self.w * int(w_str.rstrip("%")) / 100
        elif w_str.isdigit():
            w = int(w_str)

        h_str: str = self.properties["Frame"]["Height"]
        if h_str.endswith("%"):
            h = self.h * int(h_str.rstrip("%")) / 100
        elif w_str.isdigit():
            h = int(h_str)

        x1 -= w / 2
        y1 -= h / 2

        frame_enable = self.pro_window.frame.enable.currentText()
        if frame_enable == "Yes":
            frame_fill_color = self.pro_window.frame.back_color.getColor()

            bw_str = self.pro_window.frame.border_width.text()
            if bw_str.isdigit():
                frame_line_width = int(bw_str)

            frame_line_color = self.pro_window.frame.border_color.getColor()

            if frame_line_width == 0:
                frame_line_color = Qt.transparent

        else:
            frame_fill_color = Qt.transparent
            frame_line_color = Qt.transparent

        self.scene.setFrame(x1, y1, w, h, frame_fill_color, frame_line_color, frame_line_width)

    """
     Functions that must be complete in new version
     """

    def store(self):
        """
        return necessary data for restoring this widget.
        @return:
        """
        return self.getInfo()

    def restore(self, properties: dict):
        pro = properties.get("Properties")
        self.pro_window.setProperties(pro)

        items: dict = properties.get("Items")

        # recover the item order
        itemsOrderedKeys: list = properties.get("ItemsOrderedKeys", [])

        if not itemsOrderedKeys:
            itemsOrderedKeys = list(items.keys())

        # reversed the item order so that the first item is in the bottom layer
        # 0 -> n  bottom to top layer
        itemsOrderedKeys.reverse()

        items = {cKey: items[cKey] for cKey in itemsOrderedKeys}

        # items.items()
        self.scene.setProperties(items)

        self.item_list.clear()
        self.item_list.addItems(items.keys())
        self.item_list.insertItem(0, "none")

    def clone(self, new_widget_id: str, new_widget_name):
        """
        根据传入的widget_id，复制一个widget
        :param new_widget_name:
        :param new_widget_id:
        :return:
        """
        clone_page = Combo(new_widget_id, new_widget_name)
        self.getInfo()
        clone_page.pro_window.setProperties(self.pro_window.default_properties.copy())
        clone_page.scene.setProperties(self.scene.getInfo())

        return clone_page

    ####################
    # single property
    ###################

    def getClearAfter(self) -> str:
        """
        返回是否clear after
        :return:
        """
        return self.pro_window.general.clear_after.currentText()

    def getScreenName(self) -> str:
        """
        返回Screen Name
        :return:
        """
        return self.pro_window.general.screen_name.currentText()

    def getXAxisCoordinates(self) -> str:
        """
        返回x坐标值
        :return:
        """
        return self.default_properties.get("Properties").get("Frame").get("Center X")

    def getYAxisCoordinates(self) -> str:
        """
        返回y坐标值
        :return:
        """
        return self.default_properties.get("Properties").get("Frame").get("Center Y")

    def getWidth(self) -> str:
        """
        返回宽度
        :return:
        """
        return self.default_properties.get("Properties").get("Frame").get("Width")

    def getHeight(self) -> str:
        """
        返回高度
        :return:
        """
        return self.default_properties.get("Properties").get("Frame").get("Height")

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

    def getItemsInfo(self):
        return self.scene.getInfo()

    def getFilename(self, fileType: int = 1) -> dict:
        """
        :param fileType: 1,2,4 for image, sound, and video file respectively
        :return: List of String (relative filepath)
        """
        return self.scene.getFilename(fileType)
