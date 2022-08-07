from PyQt5.QtCore import Qt, QByteArray, QDataStream, QIODevice, QMimeData, pyqtSignal, QSize
from PyQt5.QtGui import QDrag, QIcon
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QPushButton, QWidget, QGridLayout, QLabel, QToolBox, QSizePolicy, QFormLayout, QDockWidget

from app.func import Func
from app.info import Info


class LeftBox(QToolBox):
    Line, Open, Polygon, Circle, Arc, Rect, Image, Video, Text, Sound, Snow, Gabor, Dot = range(13)

    def __init__(self, parent=None):
        super(LeftBox, self).__init__(parent=parent)
        # here to create geometries items
        self.basic = QWidget()
        open = Item("3D", self.Open)
        open.setEnabled(False)
        polygon = Item("Polygon", self.Polygon)
        circle = Item("Circle", self.Circle)
        arc = Item("Arc", self.Arc)
        rect = Item("Rect", self.Rect)

        self.stimuli = QWidget()
        image = Item(Info.ITEM_IMAGE.capitalize(), LeftBox.Image)
        video = Item(Info.ITEM_VIDEO.capitalize(), LeftBox.Video)
        text = Item(Info.ITEM_TEXT.capitalize(), LeftBox.Text)
        sound = Item(Info.ITEM_SOUND.capitalize(), LeftBox.Sound)
        snow = Item(Info.ITEM_SNOW.capitalize(), LeftBox.Snow)
        gabor = Item(Info.ITEM_GABOR.capitalize(), LeftBox.Gabor)
        dot_motion = Item(Info.ITEM_DOT_MOTION.capitalize(), LeftBox.Dot)
        # dot_motion.setEnabled(False)

        self.addItem(self.basic, "Geometries")
        self.addItem(self.stimuli, "Stimuli")

        self.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Ignored))

        basic_layout = QFormLayout()
        basic_layout.setAlignment(Qt.AlignCenter)

        basic_layout.addWidget(open)
        basic_layout.addWidget(polygon)
        basic_layout.addWidget(circle)
        basic_layout.addWidget(arc)
        basic_layout.addWidget(rect)

        stim_Layout = QFormLayout()
        stim_Layout.setAlignment(Qt.AlignCenter)

        stim_Layout.addWidget(image)
        stim_Layout.addWidget(video)
        stim_Layout.addWidget(text)
        stim_Layout.addWidget(sound)
        stim_Layout.addWidget(snow)
        stim_Layout.addWidget(gabor)
        stim_Layout.addWidget(dot_motion)

        self.basic.setLayout(basic_layout)
        self.stimuli.setLayout(stim_Layout)

        # here to insert geometries layout
        geom_layout = QFormLayout()
        geom_layout.setAlignment(Qt.AlignCenter)


class Item(QWidget):
    itemType = pyqtSignal(int)

    def __init__(self, text: str, item_type: int, parent=None):
        super(Item, self).__init__(parent=parent)
        self.text = text
        self.item_type = item_type
        self.bt = Button(text, item_type)
        self.bt.clicked.connect(lambda: self.itemType.emit(self.item_type))
        self.setUI()

    def setUI(self):
        layout = QGridLayout()
        layout.addWidget(self.bt, 0, 0, Qt.AlignHCenter)
        layout.addWidget(QLabel(self.text), 1, 0, Qt.AlignCenter)
        self.setLayout(layout)


class Button(QPushButton):
    def __init__(self, text: str, item_type: int, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)
        self.item_type = item_type
        self.setStyleSheet("border:none")

        if text.lower() == Info.ITEM_TEXT.lower():
            text = "textpointer"
        elif text.lower() == "3d":
            text = "open"
        elif text.lower() == Info.ITEM_DOT_MOTION.lower():
            text = "Dot_motion"

        fp = QPixmap(Func.getImage(f"widgets/{text}.png")).scaled(50, 50)
        self.setIcon(QIcon(fp))
        self.setIconSize(QSize(50, 50))
        self.setMouseTracking(True)

    def mouseMoveEvent(self, e):
        if e.buttons() != Qt.LeftButton:
            return

        icon = self.icon()
        data = QByteArray()
        stream = QDataStream(data, QIODevice.WriteOnly)
        stream << icon
        mime_data = QMimeData()
        mime_data.setData("application/x-icon-and-text", data)
        t = QByteArray()
        t.setNum(self.item_type)
        mime_data.setData("item-type", t)

        drag = QDrag(self)
        drag.setMimeData(mime_data)
        drag.setHotSpot(e.pos() - self.rect().topLeft())
        drag.exec_()
