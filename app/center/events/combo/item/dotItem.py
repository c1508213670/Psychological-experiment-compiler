import math
import random

from PyQt5.QtCore import Qt, QRectF, QTimer
from PyQt5.QtGui import QPainterPath, QBrush, QColor, QPen
from PyQt5.QtWidgets import QGraphicsItem

from app.func import Func
from .dot.dotProperty import DotProperty
from app.info import Info


class DotItem(QGraphicsItem):
    Dot = 12
    name = {
        Dot: Info.ITEM_DOT_MOTION,
    }

    Interval = 300

    def __init__(self, item_type, item_name: str = ""):
        super(DotItem, self).__init__()

        self.item_type = item_type
        self.item_name = item_name if item_name else self.generateItemName()

        self.pro_window = DotProperty()
        self.pro_window.ok_bt.clicked.connect(self.ok)
        self.pro_window.cancel_bt.clicked.connect(self.cancel)
        self.pro_window.apply_bt.clicked.connect(self.apply)

        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)

        self.properties = self.pro_window.default_properties
        self.default_properties = {
            'Name': self.item_name,
            'Z': self.zValue(),
            'X': 1,
            'Y': 1,
            "Properties": self.properties
        }

        self.rect = QRectF(-100, -100, 200, 200)
        self.dot_position: list = []

        self.is_oval: bool = True
        self.dot_cnt: int = 50
        self.dot_type: int = 0
        self.dot_size: int = 5
        self.move_direction: float = 0
        self.speed: float = 20

        self.dot_color: QColor = QColor(Qt.black)
        self.coherence: float = 100

        self.fill_color: QColor = QColor(Qt.transparent)
        self.border_color: QColor = QColor(Qt.transparent)

        self.border_width: int = 0

        self.generateDotPosition()

        self.timer = QTimer()
        self.timer.timeout.connect(self.updateDotPosition)
        self.timer.start(DotItem.Interval)

    def mouseDoubleClickEvent(self, event):
        self.openPro()

    def setAttributes(self, attributes):
        self.pro_window.setAttributes(attributes)

    def generateItemName(self) -> str:
        name = self.name[self.item_type]
        cnt = Info.COMBO_COUNT.get(name)
        item_name = f"{name}_{cnt}"
        Info.COMBO_COUNT[name] += 1
        return item_name

    def openPro(self):
        self.setPosition()
        self.setWh()
        self.pro_window.show()

    def setWh(self):
        self.pro_window.setWh(self.rect.width(), self.rect.height())

    def setPosition(self):
        self.pro_window.setPosition(self.scenePos().x(), self.scenePos().y())

    def getName(self):
        return self.item_name

    def ok(self):
        self.apply()
        self.pro_window.close()

    def cancel(self):
        self.pro_window.loadSetting()

    def apply(self):
        self.updateInfo()
        self.changeSomething()

    def updateInfo(self):
        self.pro_window.updateInfo()
        self.default_properties["X"] = self.scenePos().x()
        self.default_properties["Y"] = self.scenePos().y()
        self.default_properties["Z"] = self.zValue()

    def getInfo(self):
        self.updateInfo()
        return self.default_properties

    def changeSomething(self):
        # __cx = self.properties["Center X"]
        # cx = int(__cx) if __cx.isdigit() else self.scenePos().x()
        # __cy = self.properties["Center Y"]
        # cy = int(__cy) if __cy.isdigit() else self.scenePos().y()
        #
        # positions
        cx = self.getItemPos(self.properties["Center X"], True)
        cy = self.getItemPos(self.properties["Center Y"], False)

        self.setPos(cx, cy)

        # __w = self.properties["Width"]
        # w = int(__w) if __w.isdigit() else self.rect.width()
        # __h = self.properties["Height"]
        # h = int(__h) if __h.isdigit() else self.rect.height()

        w = self.getItemPos(self.properties["Width"], True, True)
        h = self.getItemPos(self.properties["Height"], False, True)

        self.rect = QRectF(-w / 2, -h / 2, w, h)

        __is_oval = self.properties["Is Oval"]
        if __is_oval in ("yes", "no"):
            self.is_oval = __is_oval == "yes"

        __move_direction = self.properties["Move Direction"]
        if not __move_direction.startswith("["):
            self.move_direction = float(__move_direction)

        __speed = self.properties["Speed"]
        if not __speed.startswith("["):
            self.speed = float(__speed)

        __coherence = self.properties["Coherence"]
        if not __coherence.startswith("["):
            self.coherence = float(__coherence)

        __dot_num = self.properties["Dot Num"]
        if __dot_num.isdigit():
            self.dot_cnt = int(__dot_num)

        self.generateDotPosition()

        __dot_type = self.properties["Dot Type"]
        if __dot_type.isdigit():
            self.dot_type = int(__dot_type)

        __dot_size = self.properties["Dot Size"]
        if __dot_size.isdigit():
            self.dot_size = int(__dot_size)

        __dot_color = self.pro_window.general.dot_color.getColor()
        if isinstance(__dot_color, QColor):
            self.dot_color = __dot_color

        __fill_color = self.pro_window.general.fill_color.getColor()
        if __fill_color:
            self.fill_color = __fill_color

        __border_color = self.pro_window.general.border_color.getColor()
        if __border_color:
            self.border_color = __border_color
        __border_width = self.properties["Border Width"]
        if __border_width.isdigit():
            self.border_width = int(__border_width)
        self.update()

    def boundingRect(self):
        w, h = self.rect.width(), self.rect.height()
        bigger_rect = QRectF(-w / 2 - 10, -h / 2 - 10, w+20, h+20)
        return bigger_rect

    def shape(self):
        path = QPainterPath()
        if self.is_oval:
            path.addEllipse(self.rect)
        else:
            path.addRect(self.rect)
        return path

    def generateDotPosition(self):
        """
        """
        w = self.rect.width()
        h = self.rect.height()

        ps = list()
        #
        for iP in range(self.dot_cnt):
            # cPointNum += 1

            x = (random.random() - 0.5) * w
            y = (random.random() - 0.5) * h

            if iP > (self.coherence * self.dot_cnt) / 100 - 1:
                d = random.random() * 360
            else:
                d = self.move_direction

            if self.is_oval:
                isShow = 4 * (x * x) / (w * w) + 4 * (y * y) / (h * h) <= 1
            else:
                isShow = True

            # X,Y, direction, showOrNot
            ps.append([x, y, d, isShow])

        self.dot_position = ps

    def updateDotPosition(self):

        w = self.rect.width()
        h = self.rect.height()

        move_dis = self.speed * DotItem.Interval / 1000

        ps = list()

        for cP in self.dot_position:

            x, y, d, s = cP

            x += move_dis * math.cos(math.pi * d / 180)
            y += move_dis * math.sin(math.pi * d / 180)

            if x < -w / 2:
                x += w

            if x > w / 2:
                x -= w

            if y < -h / 2:
                y += h

            if y > h / 2:
                y -= h

            if self.is_oval:
                isShow = 4 * (x * x) / (w * w) + 4 * (y * y) / (h * h) <= 1
            else:
                isShow = True

            ps.append([x, y, d, isShow])

        self.dot_position = ps

        self.update()

    def paint(self, painter, option, widget=None):
        # draw border
        # if self.border_width:
        #     pen = QPen()
        #     pen.setColor(self.border_color)
        #     pen.setWidth(self.border_width)
        #     painter.setPen(pen)
        #     if self.is_oval:
        #         painter.drawEllipse(self.rect)
        #     else:
        #         painter.drawRect(self.rect)
        #
        # painter.setPen(Qt.NoPen)
        # # draw fill color
        # painter.setBrush(QBrush(self.fill_color))
        # if self.is_oval:
        #     painter.drawEllipse(self.rect)
        # else:
        #     painter.drawRect(self.rect)

        # draw dots
        painter.setBrush(QBrush(self.dot_color))
        for p in self.dot_position:
            p: tuple
            x = p[0]
            y = p[1]
            if p[3]:
                rect = QRectF(x - self.dot_size / 2, y - self.dot_size / 2, self.dot_size, self.dot_size)
                if self.dot_type == 0 or self.dot_type == 4:
                    painter.drawEllipse(rect)
                else:
                    painter.drawRect(rect)

    def setProperties(self, properties: dict):
        self.pro_window.setProperties(properties.get("Properties"))
        self.default_properties["X"] = properties["X"]
        self.default_properties["Y"] = properties["Y"]
        self.default_properties["Z"] = properties["Z"]
        self.loadSetting()

    def loadSetting(self):
        x = self.default_properties.get("X", 0)
        y = self.default_properties.get("Y", 0)
        z = self.default_properties.get("Z", 0)
        self.setPos(x, y)
        self.setZValue(z)

    def clone(self):
        self.updateInfo()
        new = DotItem(self.item_type)
        new.setProperties(self.default_properties.copy())
        new.changeSomething()
        return new

    def setZValue(self, z: float) -> None:
        self.default_properties["Z"] = z
        super(DotItem, self).setZValue(z)

    def setItemColor(self, color: QColor):
        pass
        # self.fill_color = color
        # old_rgb = self.properties["Fill Color"]
        # if not old_rgb.startswith("["):
        #     rgb = f"{color.red()},{color.green()},{color.blue()}"
        #     self.properties["Back Color"] = rgb
        #     self.pro_window.general.setFillColor(rgb)

    def setWidth(self, width: int):
        pass

        # self.border_width = width
        # self.update()
        #
        # old_width = self.properties["Border Width"]
        # if not old_width.startswith("["):
        #     self.properties["Border Width"] = str(width)
        #     self.pro_window.general.setBorderWidth(str(width))

    def setLineColor(self, color: QColor):
        pass
        # self.border_color = color
        # self.update()
        #
        # old_rgb = self.properties["Border Color"]
        # if not old_rgb.startswith("["):
        #     rgb = f"{color.red()},{color.green()},{color.blue()}"
        #     self.properties["Border Color"] = rgb
        #     self.pro_window.general.setBorderColor(rgb)

    def getItemPos(self, posStr, isX: bool = True, isWH: bool = False, decNum: int = 0):
        """
        :param posStr:
        :param isX:  is x or y
        :param isWH: is width and height or center XY
        :param decNum:
        :return:
        """
        if isinstance(posStr, str):
            if Func.isPercentStr(posStr):
                # percent
                if isX:
                    posStr = round(float(posStr[0:-1]) * self.scene().width() / 100, decNum)
                else:
                    posStr = round(float(posStr[0:-1]) * self.scene().height() / 100, decNum)
            elif posStr.isdigit():
                # digit
                posStr = round(float(posStr), decNum)
            else:
                # all others: ref
                if isWH:
                    if isX:
                        posStr = self.rect.width()
                    else:
                        posStr = self.rect.height()
                else:
                    if isX:
                        posStr = self.scenePos().x()
                    else:
                        posStr = self.scenePos().y()

        return posStr