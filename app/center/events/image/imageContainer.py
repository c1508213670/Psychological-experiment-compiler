from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QPaintEvent, QPainter, QPen, QColor, QPalette
from PyQt5.QtWidgets import QFrame


class ImageContainer(QFrame):
    def __init__(self):
        super(ImageContainer, self).__init__()

        self.pix = None

        self.rotate = 0
        self.cx = 960
        self.cy = 540

        self.back_color: QColor = QColor(Qt.transparent)
        self.border_color: QColor = QColor(Qt.transparent)
        self.border_width = 0

        self.frame_transparent = 255

    def setColor(self, rgb: str, target=0):
        r, g, b = [int(i) for i in rgb.split(",")]
        if target == 0:
            self.border_color = QColor(r, g, b)
        else:
            self.back_color = QColor(r, g, b)

    def setFrameTransparent(self, value: int):
        self.back_color.setAlpha(value)

    def paintEvent(self, a0: QPaintEvent) -> None:
        super(QFrame, self).paintEvent(a0)

        if self.pix is None:
            painter = QPainter(self)
            painter.drawText(100, 100, "Your image will appear here")
        else:
            palette: QPalette = self.palette()
            palette.setColor(QPalette.Background, self.back_color)
            self.setPalette(palette)

            painter = QPainter(self)

            rect = QRect(- self.pix.width() // 2,
                         - self.pix.height() // 2,
                         self.pix.width(),
                         self.pix.height())

            painter.resetTransform()
            painter.translate(self.cx, self.cy)
            painter.rotate(self.rotate)
            painter.drawPixmap(rect, self.pix)

            if self.border_width:
                painter.setPen(QPen(self.border_color, self.border_width))
                painter.drawRect(rect)
