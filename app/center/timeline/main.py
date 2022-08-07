from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QVBoxLayout

from app.info import Info
from lib import TabItemWidget
from .icon_bar import IconBar
from .timeline_area import TimelineArea


class Timeline(TabItemWidget):
    """
    timeline widget: 1. icon bar to choose item
                     2. area to place item
    """

    # add new item, emit item's widget id and its index in timeline. (parent_widget_id, widget_id, widget_name, index)
    itemAdded = pyqtSignal(str, str, str, int)
    # item copied, emit signal (parent_widget_id, origin_widget_id, new_widget_id, new_widget_name, index)
    itemCopied = pyqtSignal(str, str, str, str, int)
    # item referenced, emit signal (parent_widget_id, origin_widget_id, new_widget_id, index)
    itemReferenced = pyqtSignal(str, str, str, int)
    # item move, emit signal. (origin_timeline, dest_timeline, widget_id, origin index, new index)
    itemMoved = pyqtSignal(str, str, str, int, int)
    # item delete. (sender_widget, widget_id)
    itemDeleted = pyqtSignal(int, str)
    # when item's name changed, emit its widget id. (sender_widget, widget_id, new_text)
    itemNameChanged = pyqtSignal(int, str, str)
    # when item is clicked, emit its widget id. (widget_id)
    itemClicked = pyqtSignal(str)
    # when item is double clicked, emit its widget id. (widget_id)
    itemDoubleClicked = pyqtSignal(str)

    def __init__(self, widget_id: str, widget_name: str):
        super(Timeline, self).__init__(widget_id, widget_name)
        # set its qss id
        self.setObjectName("Timeline")
        # set its icon bar and timeline area
        self.icon_bar = IconBar()
        self.timeline_area = TimelineArea(self)
        # set its layout
        layout = QVBoxLayout()
        layout.addWidget(self.icon_bar, 1)
        layout.addWidget(self.timeline_area, 5)
        self.setLayout(layout)

        # link signals
        self.linkSignals()

    def linkSignals(self) -> None:
        """
        link signals
        """
        #
        self.timeline_area.itemAdded.connect(
            lambda widget_id, widget_name, index: self.itemAdded.emit(self.widget_id, widget_id, widget_name, index))
        #
        self.timeline_area.itemCopied.connect(
            lambda origin_widget_id, new_widget_id, new_widget_name, index: self.itemCopied.emit(self.widget_id,
                                                                                                 origin_widget_id,
                                                                                                 new_widget_id,
                                                                                                 new_widget_name,
                                                                                                 index))
        #
        self.timeline_area.itemReferenced.connect(
            lambda origin_widget_id, new_widget_id, index: self.itemReferenced.emit(self.widget_id, origin_widget_id,
                                                                                    new_widget_id, index))
        #
        self.timeline_area.itemMoved.connect(
            lambda origin_timeline, widget_id, origin_index, new_index: self.itemMoved.emit(origin_timeline,
                                                                                            self.widget_id, widget_id,
                                                                                            origin_index,
                                                                                            new_index))
        #
        self.timeline_area.itemDeleted.connect(lambda widget_id: self.itemDeleted.emit(Info.TimelineSend, widget_id))
        #
        self.timeline_area.itemNameChanged.connect(
            lambda widget_id, text: self.itemNameChanged.emit(Info.TimelineSend, widget_id, text))
        self.timeline_area.itemClicked.connect(lambda widget_id: self.itemClicked.emit(widget_id))
        self.timeline_area.itemDoubleClicked.connect(lambda widget_id: self.itemDoubleClicked.emit(widget_id))

    def addItem(self, widget_type: str = None, widget_id: str = None, widget_name: str = None, index: int = 0) -> (
            str, str, int):
        """
        add timeline item into its timeline area
        """
        return self.timeline_area.addItem(widget_type, widget_id, widget_name, index)

    def deleteItemByWidgetName(self, widget_name: str):
        """
        delete timeline item in its timeline area through item's name
        """
        widget_id = self.itemWidgetId(widget_name)
        self.deleteItemByWidgetId(widget_id)

    def deleteItemByWidgetId(self, widget_id: str):
        """
        delete timeline item in its timeline area through item's widget id
        """
        self.timeline_area.deleteItem(widget_id)

    def renameItem(self, origin_widget_name: str, new_widget_name: str):
        """
        change item's name.
        @param origin_widget_name:
        @param new_widget_name:
        @return:
        """
        self.timeline_area.renameItem(origin_widget_name, new_widget_name)

    def itemCount(self):
        """
        the num of timeline items
        @return:
        """
        return self.timeline_area.timeline_table.item_count

    def itemWidgetId(self, widget_name: str):
        """

        @param widget_name:
        @return:
        """
        return self.timeline_area.itemWidgetId(widget_name)

    def store(self):
        """
        return necessary data for restoring this widget.
        @return:
        """
        return self.timeline_area.store()

    def restore(self, data: dict):
        """
        restore this widget according to data.
        @param data: necessary data for restoring this widget
        @return:
        """
        self.timeline_area.restore(data)
