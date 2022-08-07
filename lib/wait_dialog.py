from PyQt5.QtCore import QSize, pyqtProperty, QTimer, Qt
from PyQt5.QtGui import QColor, QPainter
from PyQt5.QtWidgets import QDialog

from app.info import Info


class WaitDialog(QDialog):
    Color = QColor(0, 0, 0)
    Clockwise = True
    Delta = 36

    if Info.IS_RETINA_SCR_LINUX:
        wh = 200
    else:
        wh = 100


    def __init__(self, parent=None):
        super(WaitDialog, self).__init__(parent, Qt.FramelessWindowHint)
        self.angle = 0
        self._timer = QTimer(self, timeout=self.update)
        self._timer.start(1)

        self.setAttribute(Qt.WA_TranslucentBackground)
        # self.setModal(True)
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint | Qt.CustomizeWindowHint)
        self.setFixedHeight(self.wh)
        self.setFixedWidth(self.wh)

    def paintEvent(self, event):
        super(WaitDialog, self).paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(self.wh/2, self.wh/2)
        side = 36
        painter.scale(side / 150.0, side / 150.0)
        painter.rotate(self.angle)

        painter.save()
        painter.setPen(Qt.NoPen)
        color = self.Color.toRgb()
        # color.setRgb(255,255,255)
        for i in range(11):
            color.setAlphaF(i / 10.0)
            painter.setBrush(color)
            painter.drawEllipse(40, -10, 25, 25)
            painter.rotate(36)
        painter.restore()

        self.angle += self.Delta if self.Clockwise else -self.Delta
        self.angle %= 360

    @pyqtProperty(QColor)
    def color(self) -> QColor:
        return self.Color

    @color.setter
    def color(self, color: QColor):
        if self.Color != color:
            self.Color = color
            self.update()

    @pyqtProperty(bool)
    def clockwise(self) -> bool:
        return self.Clockwise

    @clockwise.setter
    def clockwise(self, clockwise: bool):
        if self.Clockwise != clockwise:
            self.Clockwise = clockwise
            self.update()

    @pyqtProperty(int)
    def delta(self) -> int:
        return self.Delta

    @delta.setter
    def delta(self, delta: int):
        if self.Delta != delta:
            self.Delta = delta
            self.update()

    def sizeHint(self) -> QSize:
        return QSize(100, 100)
