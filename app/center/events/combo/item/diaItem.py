import numpy as np
from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtGui import QColor, QPainterPath
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsPolygonItem

from app.func import Func
from app.info import Info
from .arc import ArcProperty
from .circle import CircleProperty
from .polygon import PolygonProperty
from .rect import RectProperty


class DiaItem(QGraphicsPolygonItem):
    Polygon, Circle, Arc, Rect = range(2, 6)

    name: dict = {
        Polygon: Info.ITEM_POLYGON,
        Arc: Info.ITEM_ARC,
        Circle: Info.ITEM_CIRCLE,
        Rect: Info.ITEM_RECT,
    }

    def __init__(self, item_type, item_name: str = ""):
        super(DiaItem, self).__init__()
        self.item_type = item_type
        self.item_name = item_name if item_name else self.generateItemName()

        path = QPainterPath()
        # circle
        if self.item_type == self.Circle:
            path.addEllipse(QRectF(-100, -100, 200, 200))
            self.pro_window = CircleProperty()

        #  rectangle
        elif self.item_type == self.Rect:
            path.addRect(QRectF(-100, -100, 200, 200))
            self.pro_window = RectProperty()

        # arc
        elif self.item_type == self.Arc:
            path.arcTo(QRectF(-100, -100, 200, 200), 90 - 0, -270)
            self.pro_window = ArcProperty()

        # polygon
        elif self.item_type == self.Polygon:
            # added by yang to plot the triangle
            self.pro_window = PolygonProperty()
            n = 3
            points = []
            for p in range(n):
                x = int(100 * np.cos(np.pi / 2 - p * 2 * np.pi / n))
                y = int(100 * np.sin(p * 2 * np.pi / n - np.pi / 2))
                points.append((x, y))
                if p == 0:
                    path.moveTo(points[p][0], points[p][1])
                else:
                    path.lineTo(points[p][0], points[p][1])
            path.lineTo(points[0][0], points[0][1])

        self.pro_window.ok_bt.clicked.connect(self.ok)
        self.pro_window.cancel_bt.clicked.connect(self.cancel)
        self.pro_window.apply_bt.clicked.connect(self.apply)

        self.setPolygon(path.toFillPolygon())
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)

        self.arbitrary_resize = False
        self.keep_resize = False
        self.resizingFlag = False

        self.fill_color = '0,0,0'
        self.border_color = '255,255,255'
        self.border_width = 1

        self.properties = self.pro_window.default_properties
        self.default_properties = {
            'Name': self.item_name,
            'Z': self.zValue(),
            'X': 1,
            'Y': 1,
            "Properties": self.properties,
        }

    def generateItemName(self) -> str:
        name = self.name[self.item_type]
        cnt = Info.COMBO_COUNT.get(name)
        item_name = f"{name}_{cnt}"
        Info.COMBO_COUNT[name] += 1
        return item_name

    def getName(self):
        return self.item_name

    def mouseMoveEvent(self, event):
        x = event.pos().x()
        y = event.pos().y()

        bounding_rect = self.polygon().boundingRect()

        # if self.item_type == self.Arc:
        #     __w = self.properties["Width"]
        #     w = int(__w) if __w.isdigit() else 100
        #
        #     __h = self.properties["Height"]
        #     h = int(__h) if __h.isdigit() else 100
        #
        #     cx = bounding_rect.center().x()
        #     cy = bounding_rect.center().y()
        #
        #     bounding_rect = QRectF(cx - w/2, cy - h/2, w, h)
        height = bounding_rect.height()
        width = bounding_rect.width()

        x0 = bounding_rect.left()
        y0 = bounding_rect.top()
        # Non equal proportion
        if self.arbitrary_resize:
            self.resizingFlag = True
        # Equal proportion
        if self.keep_resize:
            self.resizingFlag = True

            # make sure the zoom in/out ratio equal for h and w
            ratio = height / width  # positive

            # if (y - height) > ratio * (x - width):
            #     y = ratio * (x - width) + height
            # else:
            #     x = (y - height) / ratio + width
            if (y - y0) > ratio * (x - x0):
                y = ratio * (x - x0) + y0
            else:
                x = (y - y0) / ratio + x0

        # todo temp disable arc zoom in/out
        if self.item_type == self.Arc or self.item_type == self.Polygon:
            self.resizingFlag = False

        if self.resizingFlag:
            path = QPainterPath()

            new_width = x - x0
            new_height = y - y0

            new_rect = QRectF(x0 - (new_width - width) / 2, y0 - (new_height - height) / 2, new_width, new_height)

            if self.item_type == self.Circle:
                path.addEllipse(new_rect)

            elif self.item_type == self.Arc:
                path.moveTo(new_rect.center())
                __start_angle = self.properties["Angle Start"]
                start_angle = 0 if __start_angle.startswith("[") else float(__start_angle)
                __angle_length = self.properties["Angle Length"]
                angle_length = 270 if __angle_length.startswith("[") else float(__angle_length)

                path.arcTo(new_rect, 90 - start_angle, -angle_length)

            elif self.item_type == self.Rect:
                path.addRect(new_rect)

            elif self.item_type == self.Polygon:
                h_ratio = (x - x0) / width
                v_ratio = (y - y0) / height
                if self.keep_resize:
                    if h_ratio > v_ratio:
                        v_ratio = h_ratio
                    else:
                        h_ratio = v_ratio

                for v in range(len(self.polygon())):
                    c_x = self.polygon().value(v).x() * h_ratio
                    c_y = self.polygon().value(v).y() * v_ratio

                    if v == 0:
                        path.moveTo(c_x, c_y)
                    else:
                        path.lineTo(c_x, c_y)
            else:
                raise Exception("item_type should be of 'Arc','Rectangle', 'Polygon', or 'Circle' !")

            self.mPolygon = path.toFillPolygon()
            self.setPolygon(self.mPolygon)
            self.update()

            self.setPosition(new_width, new_height)

        else:
            super(DiaItem, self).mouseMoveEvent(event)

    def mousePressEvent(self, event):
        if event.button() != Qt.LeftButton:
            return
        if event.modifiers() == Qt.AltModifier:
            self.arbitrary_resize = True
            self.setCursor(Qt.SizeAllCursor)

        elif event.modifiers() == Qt.ShiftModifier:
            self.keep_resize = True
            self.setCursor(Qt.SizeAllCursor)

        super(DiaItem, self).mousePressEvent(event)

    def mouseReleaseEvent(self, mouseEvent):
        self.unsetCursor()
        self.resizingFlag = False
        self.arbitrary_resize = False
        self.keep_resize = False
        super(DiaItem, self).mouseReleaseEvent(mouseEvent)

    def mouseDoubleClickEvent(self, mouseEvent):
        self.openPro()

    def openPro(self):
        self.pro_window.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setPosition()
        self.setWh()
        self.pro_window.show()

    def setAttributes(self, attributes):
        self.pro_window.setAttributes(attributes)

    def ok(self):
        self.apply()
        self.pro_window.close()

    def cancel(self):
        # 加载之前的default_properties
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
        new = DiaItem(self.item_type)
        new.setProperties(self.default_properties.copy())
        new.changeSomething()
        return new

    def changeSomething(self):
        # fill color
        fill_color = self.pro_window.general.fill_color.getColor()
        if fill_color:
            self.setBrush(fill_color)

        border_width = self.properties["Border Width"]
        if not border_width.startswith("["):
            self.border_width = int(border_width)
        pen = self.pen()
        pen.setWidth(self.border_width)

        # border color
        border_color = self.pro_window.general.border_color.getColor()
        if border_color:
            pen.setColor(border_color)
        self.setPen(pen)

        # positions
        cx = self.getItemPos(self.properties["Center X"], True)
        cy = self.getItemPos(self.properties["Center Y"], False)

        path = QPainterPath()
        if self.item_type == self.Polygon:
            points = self.properties["Points"]
            flag = True
            for p in points:
                x, y = p
                if Func.isRef(x) or Func.isRef(y):
                    flag = False
                    break
            if flag:
                for i, p in enumerate(points):
                    x = int(p[0])
                    y = int(p[1])
                    if i == 0:
                        path.moveTo(x - cx, y - cy)
                    else:
                        path.lineTo(x - cx, y - cy)
                path.lineTo(int(points[0][0]) - cx, int(points[0][1]) - cy)

        else:
            # __cx = int(cx) if cx.isdigit() else self.scenePos().x()
            # __cy = int(cy) if cy.isdigit() else self.scenePos().y()

            self.setPos(cx, cy)
            # if cx.isdigit() and cy.isdigit():
            #     self.setPos(int(cx), int(cy))
            # __w = self.properties["Width"]
            # w = int(__w) if __w.isdigit() else 100
            # __h = self.properties["Height"]
            # h = int(__h) if __h.isdigit() else 100

            w = self.getItemPos(self.properties["Width"], True, True)
            h = self.getItemPos(self.properties["Height"], False, True)

            if self.item_type == self.Circle:
                rect = QRectF(-w / 2, -h / 2, w, h)
                path.addEllipse(rect)

            elif self.item_type == self.Arc:
                rect = QRectF(-w / 2, -h / 2, w, h)
                __start = self.properties["Angle Start"]
                start = 0 if __start.startswith("[") else float(__start)

                __length = self.properties["Angle Length"]
                length = 360 if __length.startswith("[") else float(__length)

                # added extra 90 degree to compatible with PTB
                path.arcTo(rect, 90 - start, -length)

            elif self.item_type == self.Rect:
                # w = w - self.border_width/2
                # h = h - self.border_width/2
                rect = QRectF(-w / 2, -h / 2, w, h)
                path.addRect(rect)

        self.setPolygon(path.toFillPolygon())
        self.update()

    ##############
    # change from main window
    ###############
    def setPosition(self, w: int = None, h: int = None):
        if self.item_type == self.Polygon:
            self.setVertex()
        if self.item_type in (self.Arc, self.Rect, self.Circle):
            self.setWh(w, h)

        self.pro_window.general.setPosition(self.scenePos().x(), self.scenePos().y())

    def setWh(self, w: int = None, h: int = None):
        if self.item_type == self.Rect:
            self.pro_window.general.setWh(self.boundingRect().width() - self.pen().width(),
                                          self.boundingRect().height() - self.pen().width())
        elif self.item_type == self.Arc:
            # todo maybe a bug here need to be confirmed
            if not w:
                __w = self.properties["Width"]
                w = int(__w) if __w.isdigit() else 100

            if not h:
                __h = self.properties["Height"]
                h = int(__h) if __h.isdigit() else 100

            # print(f"line 365: {h}, {w}")
            self.pro_window.general.setWh(w - self.pen().width() + 1,
                                          h - self.pen().width() + 1)
        else:
            self.pro_window.general.setWh(self.boundingRect().width() - self.pen().width() + 1,
                                          self.boundingRect().height() - self.pen().width() + 1)

    def setVertex(self):
        points = []
        for p in range(len(self.polygon()) - 1):
            points.append(
                (self.polygon()[p].x() + self.scenePos().x(),
                 self.polygon()[p].y() + self.scenePos().y()))

        self.pro_window.general.setVertex(points)

    def setWidth(self, width):
        pen = self.pen()
        pen.setWidth(width)
        self.setPen(pen)
        self.update()

        old_width = self.properties["Border Width"]
        if not old_width.startswith("["):
            self.properties["Border Width"] = str(width)
            self.pro_window.general.setBorderWidth(str(width))

    def setLineColor(self, color: QColor):
        pen = self.pen()
        pen.setColor(color)
        self.setPen(pen)
        self.update()

        old_rgb = self.properties["Border Color"]
        if not old_rgb.startswith("["):
            rgb = f"{color.red()},{color.green()},{color.blue()}"
            self.properties["Border Color"] = rgb
            self.pro_window.general.setBorderColor(rgb)

    def setItemColor(self, color: QColor):
        self.setBrush(color)

        old_rgb = self.properties["Fill Color"]
        if not old_rgb.startswith("["):
            rgb = f"{color.red()},{color.green()},{color.blue()}"
            self.properties["Fill Color"] = rgb
            self.pro_window.general.setItemColor(rgb)

    def setZValue(self, z: float) -> None:
        self.default_properties["Z"] = z
        super(DiaItem, self).setZValue(z)

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
                        posStr = self.boundingRect().width()
                    else:
                        posStr = self.boundingRect().height()
                else:
                    if isX:
                        posStr = self.scenePos().x()
                    else:
                        posStr = self.scenePos().y()

        return posStr

    def updateSceneWHInfo(self):
        self.pro_window.general.updateSceneWHInfo(self.scene().width(), self.scene().height())