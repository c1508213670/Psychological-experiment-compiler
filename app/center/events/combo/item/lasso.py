from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QPainterPath
from PyQt5.QtWidgets import QGraphicsPolygonItem


class Lasso(QGraphicsPolygonItem):
    def __init__(self, x, y):
        super(Lasso, self).__init__()
        self.path = QPainterPath()
        self.start_x = x
        self.start_y = y

        self.path.addRect(QRectF(x, y, 1, 1))
        self.rect = self.path.toFillPolygon()
        self.setPolygon(self.rect)

    def draw(self, x, y):
        """
        优化套索
        :param x:
        :param y:
        :return:
        """
        self.path.clear()
        w = abs(self.start_x - x)
        h = abs(self.start_y - y)
        top_left_x = min(self.start_x, x)
        top_left_y = min(self.start_y, y)
        new_rect = QRectF(top_left_x, top_left_y, w, h)
        self.path.addRect(new_rect)
        rect = self.path.toFillPolygon()
        self.setPolygon(rect)
