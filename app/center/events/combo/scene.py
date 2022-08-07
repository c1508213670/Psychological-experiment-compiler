import datetime

from PyQt5.QtCore import pyqtSignal, Qt, QLineF, QPointF, QRectF
from PyQt5.QtGui import QPen, QTransform, QColor, QImage, QPainter, QMouseEvent
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsLineItem, QGraphicsItem, QGraphicsRectItem, QGraphicsPolygonItem

from app.defi import *
from ...events.combo.item import *


class Scene(QGraphicsScene):
    NormalMode, LineMode, LassoMode = range(3)

    itemAdd = pyqtSignal(str, bool)
    itemSelected = pyqtSignal()

    def __init__(self, parent=None):
        super(Scene, self).__init__(parent)
        self.my_mode = Scene.NormalMode

        self.frame_enable = False

        self.attributes: list = []
        self.line = None
        self.lasso = None

        self.h = 0
        self.w = 0

        self.line_color = QColor(Qt.black)
        self.fill_color = Qt.transparent
        self.border_color = QColor(Qt.black)
        self.border_width = 2

        self.t = QTransform()

        self.border: QGraphicsRectItem = QGraphicsRectItem()
        self.addItem(self.border)

        self.frame: QGraphicsRectItem = QGraphicsRectItem()
        self.addItem(self.frame)

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("application/x-icon-and-text"):
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat("application/x-icon-and-text"):
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasFormat("application/x-icon-and-text"):
            # 添加子控件
            item_type, ok = event.mimeData().data("item-type").toUInt()
            if TextItem.Text == item_type:
                item = TextItem(item_type)
            elif PixItem.Image <= item_type <= PixItem.Sound:
                item = PixItem(item_type)
            elif OtherItem.Snow <= item_type <= OtherItem.Gabor:
                item = OtherItem(item_type)
            elif DiaItem.Polygon <= item_type <= DiaItem.Rect:
                item = DiaItem(item_type)
            elif DotItem.Dot == item_type:
                item = DotItem(item_type)
            self.addItem(item)
            item.setPos(event.scenePos())  # move the item in the scene

            item.setPosition()  # update the general tab
            item.updateInfo()  # get default_property from general tab

            # todo
            if item_type == DiaItem.Polygon:
                # item.setPosition()
                item.pro_window.general.add_bt.click()
                item.pro_window.general.del_bt.click()

            item.setAttributes(self.attributes)

            self.update()
            self.itemAdd.emit(item.getName(), True)
            action = Qt.MoveAction
            event.setDropAction(action)
            event.accept()
        else:
            event.ignore()

    def contextMenuEvent(self, event) -> None:
        it = self.itemAt(event.scenePos().x(), event.scenePos().y(), self.t)
        if it:
            self.clearSelection()
            it.setSelected(True)
            self.menu.exec_(event.screenPos())

    def setLineColor(self, color: QColor):
        self.line_color = color
        for item in self.selectedItems():
            if isinstance(item, LineItem) or isinstance(item, DiaItem) or isinstance(item, DotItem):
                item.setLineColor(color)

    def setItemColor(self, color: QColor):
        for item in self.selectedItems():
            if isinstance(item, DiaItem) or isinstance(item, DotItem):
                item.setItemColor(color)  # update the default properties in GeneralTab

    def setLineWidth(self, width: int):
        self.border_width = width
        for item in self.selectedItems():
            if isinstance(item, LineItem) or isinstance(item, DiaItem) or isinstance(item, DotItem):
                item.setWidth(width)

    def setMode(self, mode: int):
        self.my_mode = mode

    def mousePressEvent(self, event):
        # if self.lasso:
        #     self.removeItem(self.lasso)
        #     self.lasso = None
        if event.button() == Qt.LeftButton:
            if self.my_mode == self.LineMode:
                self.line = QGraphicsLineItem(QLineF(event.scenePos(),
                                                     event.scenePos()))
                self.line.setPen(QPen(self.line_color, self.border_width))
                self.addItem(self.line)
            elif self.my_mode == self.LassoMode:
                x = event.scenePos().x()
                y = event.scenePos().y()
                self.lasso = Lasso(x, y)
                self.addItem(self.lasso)
        super(Scene, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.my_mode == self.LineMode and self.line:
            line = self.line.line()
            p2 = event.scenePos()
            # straight line
            if event.modifiers() == Qt.ShiftModifier:
                dx = p2.x() - line.x1()
                dy = p2.y() - line.y1()
                if abs(dx) < abs(dy):
                    p2.setX(line.x1())
                if abs(dx) > abs(dy):
                    p2.setY(line.y1())
            new_line = QLineF(line.p1(), p2)
            self.line.setLine(new_line)
        # Update point coordinates in real time
        # elif self.my_mode == self.NormalMode:
        #     # item = self.mouseGrabberItem()
        #     # if hasattr(item, "setPosition"):
        #     #     item.setPosition()
        #     self.update()
        #     super(Scene, self).mouseMoveEvent(event)
        # 套索模式
        elif self.my_mode == self.LassoMode and self.lasso:
            self.lasso: Lasso
            x = event.scenePos().x()
            y = event.scenePos().y()
            self.lasso.draw(x, y)
            self.update()
            # self.lasso.center = self.lasso.polygon().boundingRect().center()
            self.setSelectionArea(self.lasso.path, self.t)
        else:
            self.update()
            super(Scene, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, e: QMouseEvent):
        if self.line and self.my_mode == self.LineMode:
            item = LineItem(LineItem.Line)
            l: QLineF = self.line.line()
            cx, cy = self.line.line().center().x(), self.line.line().center().y()
            item.setPos(self.line.line().center())
            line = QLineF(l.x1() - cx, l.y1() - cy, l.x2() - cx, l.y2() - cy)
            item.setLine(line)
            item.setPosition()
            item.setLineColor(self.line_color)
            item.setWidth(self.border_width)
            self.addItem(item)

            self.itemAdd.emit(item.getName(), False)
            self.update()
            self.removeItem(self.line)
            self.line = None
        if self.lasso and self.my_mode == self.LassoMode:
            self.removeItem(self.lasso)
            self.lasso = None
            self.itemSelected.emit()
            self.setMode(Scene.NormalMode)
        super(Scene, self).mouseReleaseEvent(e)

    def getInfo(self):
        item_info: dict = {}
        for item in self.items():
            if item is not self.border and item is not self.frame:
                item.setPosition()
                item_info[item.getName()] = item.getInfo()
        return item_info

    def getFilename(self, fileType: int = 1) -> dict:
        """
        :param fileType: 1,2,4 for image, sound, and video file respectively
        :return: List of String (relative filepath)
        """
        listedItemTypes = list()

        if (fileType >> 0) & 1:
            listedItemTypes.append(PixItem.Image)

        if (fileType >> 1) & 1:
            listedItemTypes.append(PixItem.Sound)

        if (fileType >> 2) & 1:
            listedItemTypes.append(PixItem.Video)

        fileInfo: dict = dict()

        for item in self.items():
            if isinstance(item, PixItem) and item.item_type in listedItemTypes:
                fileInfo.update({item.getName(): item.getFilename()})
        return fileInfo

    def refresh(self):
        for item in self.items():
            if item is not self.border and item is not self.frame:
                item.setAttributes(self.attributes)

    def setProperties(self, properties: dict):
        self.clear()

        self.border: QGraphicsRectItem = QGraphicsRectItem()
        self.addItem(self.border)

        self.frame: QGraphicsRectItem = QGraphicsRectItem()
        self.addItem(self.frame)

        for k, v in properties.items():
            k: str
            if k.startswith(ITEM_IMAGE):
                item = PixItem(PixItem.Image, k)
            elif k.startswith(ITEM_TEXT):
                item = TextItem(TextItem.Text, k)
            elif k.startswith(ITEM_VIDEO):
                item = PixItem(PixItem.Video, k)
            elif k.startswith(ITEM_SOUND):
                item = PixItem(PixItem.Sound, k)
            elif k.startswith(ITEM_SNOW):
                item = OtherItem(OtherItem.Snow, k)
            elif k.startswith(ITEM_GABOR):
                item = OtherItem(OtherItem.Gabor, k)
            elif k.startswith(ITEM_POLYGON):
                item = DiaItem(DiaItem.Polygon, k)
            elif k.startswith(ITEM_ARC):
                item = DiaItem(DiaItem.Arc, k)
            elif k.startswith(ITEM_RECT):
                item = DiaItem(DiaItem.Rect, k)
            elif k.startswith(ITEM_CIRCLE):
                item = DiaItem(DiaItem.Circle, k)
            elif k.startswith(ITEM_LINE):
                item = LineItem(LineItem.Line, k)
            elif k.startswith(ITEM_DOT_MOTION):
                item = DotItem(DotItem.Dot, k)

            self.addItem(item)
            self.itemAdd.emit(item.getName(), True)
            item.setProperties(v)
            item.apply()

    def setAttributes(self, attributes: list):
        self.attributes = attributes
        for item in self.items():
            if item is not self.border and item is not self.frame:
                item.setAttributes(attributes)

    def copyItem(self, item: QGraphicsItem):
        new_item = item.clone()
        new_pos = QPointF(item.scenePos().x() + 20, item.scenePos().y() + 20)
        self.addItem(new_item)
        new_item.setPos(new_pos)
        new_item.setPosition()
        new_item.updateInfo()
        new_item.setAttributes(self.attributes)
        self.update()
        self.itemAdd.emit(new_item.getName(), True)

        item.setSelected(False)
        new_item.setSelected(True)

    def setBorderRect(self, rect: QRectF, scr_color: QColor = Qt.transparent) -> None:
        self.border: QGraphicsRectItem
        self.border.setRect(QRectF(0, 0, rect.width(), rect.height()))
        self.border.setBrush(scr_color)

        pen = self.border.pen()

        if scr_color == QColor(0,0,0):
            bc = QColor(128, 128, 128)
        else:
            bc = QColor(0, 0, 0)

        pen.setWidth(1)
        pen.setColor(bc)
        self.border.setPen(pen)

        self.border.update()

    def setFrame(self, x1: int, y1: int, w: int, h: int, bk_color: QColor, bc: QColor, bw: int = 0):
        # import sip
        # self.frame: QGraphicsRectItem

        # if self.frame not in self.items():
        #     self.addItem(self.frame)
        self.frame.setRect(QRectF(x1, y1, w, h))
        self.frame.setBrush(bk_color)
        # if bw:
        pen = self.frame.pen()
        pen.setWidth(bw)
        pen.setColor(bc)
        self.frame.setPen(pen)

        # self.border.update()

    def downFrame(self, z: float):
        self.frame.setZValue(z)

    # def screenshot(self):
    #     try:
    #         file_name = f"Scene_{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S-%f')}.png"
    #         self.image = QImage(self.border.boundingRect().width(),
    #                             self.border.boundingRect().height(),
    #                             QImage.Format_ARGB32)
    #         painter = QPainter(self.image)
    #         painter.setRenderHint(QPainter.Antialiasing)
    #         self.render(painter)
    #         self.image.save(file_name)
    #     except Exception as e:
    #         print(e)

    def updateSceneWHInfo(self):
        for item in self.items():
            if item is not self.border and item is not self.frame:
                item.updateSceneWHInfo()
