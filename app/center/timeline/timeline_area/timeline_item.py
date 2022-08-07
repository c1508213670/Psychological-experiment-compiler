from PyQt5.QtCore import (QSize, Qt, pyqtSignal, QMimeData, QDataStream, QIODevice, QByteArray, QPoint, QRect,
                          pyqtProperty, QPropertyAnimation)
from PyQt5.QtGui import QDrag
from PyQt5.QtWidgets import QLabel

from app.func import Func
from app.info import Info


class TimelineItem(QLabel):
    """
    it is widget_type item in timeline.
    """

    # when item clicked, emit its widget id
    clicked = pyqtSignal(str)
    doubleClicked = pyqtSignal(str)
    # if Info.OS_TYPE == 2:
    if Info.IS_RETINA_SCR_LINUX:
        IconSize = 80
    else:
        IconSize = 48
    # 500ms
    MoveSpeed = 500

    def __init__(self, widget_type: str = "", widget_id: str = ""):
        """
        init item
        @param parent:
        @param widget_type: its widget add_type, such as timeline
        @param widget_id: if widget_id has provided, we don't need to generate a new widget_id
        """
        super(TimelineItem, self).__init__(None)
        # set its qss id
        self.setObjectName("TimelineItem")
        # bind timeline name item to it
        self.timeline_name_item = None
        # set data
        self.widget_id = widget_id
        self.widget_type = widget_type
        self.direction = 0
        # frame_animation
        self.frame_animation = QPropertyAnimation(self, b"frame_rect")
        self.geometry_animation = QPropertyAnimation(self, b"geometry")
        # if widget_id has provided, widget type may be not provided
        if not widget_type:
            if not widget_id:
                exit()
            self.widget_type = Func.getWidgetType(widget_id)
        # if not, we need to generate a new widget_id
        if not self.widget_id:
            self.widget_id = Func.generateWidgetId(widget_type)
        # select its widget_type according to its widget type.
        pixmap = Func.getImageObject(f"widgets/{self.widget_type}",
                                     size=QSize(TimelineItem.IconSize, TimelineItem.IconSize))
        # set its pixmap
        self.setPixmap(pixmap)
        self.setAlignment(Qt.AlignCenter)

    def _set_frame_rect(self, frame_rect: QRect):
        """
        frame_animation
        @param frame_rect:
        @return:
        """
        # save direct
        self.setFrameRect(frame_rect)

    frame_rect = pyqtProperty(QRect, fset=_set_frame_rect)

    def startFrameAnimation(self, end: QRect, direction: int = -1):
        """
        give end dot and its direction
        0: left
        1: right
        @return:
        """
        if direction != -1:
            self.direction = direction
        self.frame_animation.setDuration(self.MoveSpeed)
        self.frame_animation.setStartValue(self.frameRect())
        self.frame_animation.setEndValue(end)
        self.frame_animation.start()

    def startGeometryAnimation(self, end: QRect):
        """

        @param end:
        @return:
        """
        self.geometry_animation.setDuration(self.MoveSpeed)
        self.geometry_animation.setStartValue(self.geometry())
        self.geometry_animation.setEndValue(end)
        self.geometry_animation.start()

    def mousePressEvent(self, e):
        """
        emit click signal
        @param e:
        @return:
        """
        super(TimelineItem, self).mousePressEvent(e)
        self.clicked.emit(self.widget_id)

    def mouseDoubleClickEvent(self, e):
        """
        emit double click signal
        @param e:
        @return:
        """
        super(TimelineItem, self).mouseDoubleClickEvent(e)
        self.doubleClicked.emit(self.widget_id)

    def setWidgetId(self, widget_id: int):
        """
        change its widget id
        @param widget_id:
        @return:
        """
        self.widget_id = widget_id

    def mouseMoveEvent(self, e):
        """
        drag event and discern copy and move by modifiers
        @param e:
        @return:
        """
        if e.modifiers() == Qt.ControlModifier:
            # copy timeline item
            if self.widget_type != Info.LOOP:
                self.copyDrag()
        else:
            # move timeline item
            self.moveDrag()

    def moveDrag(self):
        """
        move widget in this timeline
        @return:
        """
        data = QByteArray()
        stream = QDataStream(data, QIODevice.WriteOnly)
        stream.writeInt(self.timeline_name_item.column())
        mime_data = QMimeData()
        mime_data.setData(Info.MoveInTimeline, data)
        drag = QDrag(self)
        drag.setMimeData(mime_data)
        drag.setHotSpot(QPoint(24, 24))
        drag.setPixmap(Func.getImageObject(f"widgets/{self.widget_type}", size=QSize(48, 48)))
        drag.exec()

    def copyDrag(self):
        """
        copy widget in this timeline
        @return:
        """
        data = QByteArray()
        stream = QDataStream(data, QIODevice.WriteOnly)
        stream.writeQString(self.widget_id)
        mime_data = QMimeData()
        mime_data.setData(Info.CopyInTimeline, data)
        drag = QDrag(self)
        drag.setMimeData(mime_data)
        drag.setHotSpot(QPoint(24, 24))
        drag.setPixmap(Func.getImageObject(f"widgets/{self.widget_type}", size=QSize(48, 48)))
        drag.exec()
